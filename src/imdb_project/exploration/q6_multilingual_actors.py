"""Q6 - Actors and actresses successful in films of several original languages.

* A film is *successful* when ``averageRating >= min_rating`` and
  ``numVotes >= min_votes`` (feature films only).
* Its original language comes from Wikidata (property P364, looked up through the
  IMDb identifier P345) for this bounded set of films. When Wikidata has no
  language, ``title.akas`` is used as a fallback: the language of the original
  title row, then the region of the rows carrying the original title (mapped with
  ``region_languages``, kept only when it designates a single language). The
  origin of each value is kept in ``language_source``.
* Films with several original languages are excluded by default
  (``multilingual_films: exclude``) so that each film counts for one language.
* An actor or actress is listed with the number of distinct original languages of
  their successful films (at least 2, then at least 3).

Stages: ``scope`` (Spark) selects the successful films, ``collect`` (plain Python,
rate-limited HTTP client, cached) queries Wikidata, ``analysis`` (Spark) builds
the result.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping

from pyspark.sql import Column, DataFrame, SparkSession, Window
from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.logging import get_logger
from imdb_project.common.spark_session import build_spark
from imdb_project.enrichment import fetch_wikidata, raw_reader
from imdb_project.exploration import base

LOGGER = get_logger(__name__)
NAME = "q6_multilingual_actors"
SCOPE_NAME = "q6_successful_films"

SOURCE_WIKIDATA = "wikidata_P364"
SOURCE_AKAS_LANGUAGE = "akas_original_language"
SOURCE_AKAS_REGION = "akas_region"
EXCLUDE = "exclude"


def successful_films(films: DataFrame, min_rating: float, min_votes: int) -> DataFrame:
    """Keep the rated films reaching both success thresholds."""
    return films.where((F.col("averageRating") >= min_rating) & (F.col("numVotes") >= min_votes))


def _lookup(mapping: Mapping[str, str], key: Column) -> Column:
    if not mapping:
        return F.lit(None).cast("string")
    literal = F.create_map(*[F.lit(part) for item in mapping.items() for part in item])
    return F.try_element_at(literal, key)


def normalize_language(code: Column, aliases: Mapping[str, str]) -> Column:
    """Lower-case a language code and apply the configured aliases."""
    lowered = F.lower(F.trim(code))
    return F.coalesce(_lookup(aliases, lowered), lowered)


def wikidata_film_languages(bindings: DataFrame, aliases: Mapping[str, str]) -> DataFrame:
    """Parse the cached Wikidata answers into (film, original language) rows.

    The language code is the ISO 639-1 code of the language item (P218), else the
    primary subtag of its IETF tag (P305), else its Wikidata id.

    Args:
        bindings: Output of ``raw_reader.read_sparql_bindings`` for the
            ``wikidata_film_languages`` source.
        aliases: Language code aliases (``cmn -> zh``...).

    Returns:
        Distinct ``tconst``, ``language``, ``language_label``.
    """
    value = raw_reader.binding_value
    code = F.coalesce(
        value("iso1"), F.split(value("ietf"), "-").getItem(0), raw_reader.qid(value("language"))
    )
    rows = bindings.select(
        value("imdb").alias("tconst"),
        normalize_language(code, aliases).alias("language"),
        value("languageLabel").alias("language_label"),
    ).where(F.col("tconst").isNotNull() & F.col("language").isNotNull())
    return rows.groupBy("tconst", "language").agg(F.min("language_label").alias("language_label"))


def akas_film_languages(
    akas: DataFrame,
    films: DataFrame,
    region_languages: Mapping[str, str],
    aliases: Mapping[str, str],
) -> DataFrame:
    """Derive an original language from ``title.akas`` (fallback source).

    Args:
        akas: Silver ``title_akas`` restricted to the films of interest.
        films: Films with ``tconst`` and ``originalTitle``.
        region_languages: Mapping of akas region to language code.
        aliases: Language code aliases.

    Returns:
        ``tconst``, ``language``, ``language_source``: at most one row per film,
        the language of the original title row when present, otherwise the single
        language designated by the regions using the original title.
    """
    scoped = akas.join(films.select("tconst", "originalTitle"), akas["titleId"] == films["tconst"])
    explicit = (
        scoped.where(F.col("isOriginalTitle") & F.col("language").isNotNull())
        .select("tconst", normalize_language(F.col("language"), aliases).alias("language"))
        .groupBy("tconst")
        .agg(F.collect_set("language").alias("languages"))
        .where(F.size("languages") == 1)
        .select("tconst", F.col("languages")[0].alias("language"))
        .withColumn("language_source", F.lit(SOURCE_AKAS_LANGUAGE))
    )
    mapped = _lookup(region_languages, F.col("region"))
    by_region = (
        scoped.where((F.col("title") == F.col("originalTitle")) & mapped.isNotNull())
        .select("tconst", normalize_language(mapped, aliases).alias("language"))
        .groupBy("tconst")
        .agg(F.collect_set("language").alias("languages"))
        .where(F.size("languages") == 1)
        .select("tconst", F.col("languages")[0].alias("language"))
        .withColumn("language_source", F.lit(SOURCE_AKAS_REGION))
    )
    return explicit.unionByName(by_region.join(explicit, "tconst", "left_anti"))


def film_languages(wikidata: DataFrame, fallback: DataFrame) -> DataFrame:
    """Combine Wikidata languages with the akas fallback.

    Args:
        wikidata: Output of :func:`wikidata_film_languages`.
        fallback: Output of :func:`akas_film_languages`.

    Returns:
        One row per (film, language): ``language_label`` (most frequent Wikidata
        label of the code, else the code), ``language_source`` and
        ``n_languages`` (number of original languages of the film).
    """
    from_wikidata = wikidata.select("tconst", "language").withColumn(
        "language_source", F.lit(SOURCE_WIKIDATA)
    )
    combined = from_wikidata.unionByName(fallback.join(wikidata, "tconst", "left_anti"))
    labels = (
        wikidata.where(F.col("language_label").isNotNull())
        .groupBy("language")
        .agg(F.mode("language_label").alias("language_label"))
    )
    return (
        combined.join(F.broadcast(labels), "language", "left")
        .withColumn("language_label", F.coalesce("language_label", "language"))
        .withColumn("n_languages", F.count(F.lit(1)).over(Window.partitionBy("tconst")))
    )


def actor_languages(credits: DataFrame, languages: DataFrame, films: DataFrame) -> DataFrame:
    """Aggregate, per person, the original languages of their successful films.

    Args:
        credits: Distinct (``nconst``, ``tconst``) acting credits.
        languages: (film, language) rows kept for the analysis.
        films: Successful films with ``primaryTitle``, ``startYear``, ``numVotes``.

    Returns:
        One row per person: ``n_languages``, ``languages`` (sorted labels),
        ``n_successful_films`` and ``examples`` (most voted film per language).
    """
    rows = credits.join(languages.select("tconst", "language", "language_label"), "tconst").join(
        films.select("tconst", "primaryTitle", "startYear", "numVotes"), "tconst"
    )
    most_voted = Window.partitionBy("nconst", "language").orderBy(
        F.col("numVotes").desc(), F.col("tconst")
    )
    example = F.format_string(
        "%s: %s (%s)",
        F.col("language_label"),
        F.col("primaryTitle"),
        F.coalesce(F.col("startYear").cast("string"), F.lit("?")),
    )
    ranked = rows.withColumn("rank", F.row_number().over(most_voted))
    return ranked.groupBy("nconst").agg(
        F.countDistinct("language").alias("n_languages"),
        F.sort_array(F.collect_set("language_label")).alias("languages"),
        F.countDistinct("tconst").alias("n_successful_films"),
        F.array_join(F.sort_array(F.collect_list(F.when(F.col("rank") == 1, example))), "; ").alias(
            "examples"
        ),
    )


def _rated_feature_films(spark: SparkSession, cfg: Config) -> DataFrame:
    return base.with_ratings(
        base.feature_films(base.read_silver(spark, cfg, "title_basics"), cfg),
        base.read_silver(spark, cfg, "title_ratings"),
    ).select("tconst", "primaryTitle", "originalTitle", "startYear", "averageRating", "numVotes")


def run_scope(spark: SparkSession, cfg: Config) -> DataFrame:
    """Stage 1 (Spark): select the successful films and write them to gold."""
    min_rating = float(base.question_setting(cfg, "q6", "min_rating", 7.0))
    min_votes = int(base.question_setting(cfg, "q6", "min_votes", 10_000))
    scope = successful_films(_rated_feature_films(spark, cfg), min_rating, min_votes)
    path = base.write_gold(scope, cfg, SCOPE_NAME)
    scope = spark.read.parquet(path)
    LOGGER.info("Q6: %d successful films", scope.count())
    return scope


def run_collect(spark: SparkSession, cfg: Config, limit: int | None = None) -> None:
    """Stage 2 (plain Python): query Wikidata for the language of the films."""
    path = io.layer_path(cfg, "gold", base.SECTION, SCOPE_NAME)
    ids = sorted(row.tconst for row in spark.read.parquet(path).select("tconst").collect())
    fetch_wikidata.collect(
        cfg, "film_languages", ids[:limit] if limit else ids, "q6:film_languages"
    )


def run_analysis(spark: SparkSession, cfg: Config) -> DataFrame:
    """Stage 3 (Spark): build the result and write the gold table and reports."""
    min_rating = float(base.question_setting(cfg, "q6", "min_rating", 7.0))
    min_votes = int(base.question_setting(cfg, "q6", "min_votes", 10_000))
    categories = list(base.question_setting(cfg, "q6", "categories", ["actor", "actress"]))
    aliases = dict(base.question_setting(cfg, "q6", "language_aliases", {}) or {})
    region_languages = dict(base.question_setting(cfg, "q6", "region_languages", {}) or {})
    multilingual = str(base.question_setting(cfg, "q6", "multilingual_films", EXCLUDE))
    max_rows = int(base.question_setting(cfg, "q6", "max_md_rows", 50))

    films = spark.read.parquet(io.layer_path(cfg, "gold", base.SECTION, SCOPE_NAME)).persist()
    film_ids = F.broadcast(films.select("tconst"))
    try:
        bindings = raw_reader.read_sparql_bindings(spark, cfg, fetch_wikidata.SOURCE_FILM_LANGUAGES)
        wikidata = wikidata_film_languages(bindings, aliases).join(film_ids, "tconst", "left_semi")
    except FileNotFoundError:
        LOGGER.warning("Q6: no Wikidata response in the cache, using the akas fallback only")
        wikidata = spark.createDataFrame(
            [], "tconst string, language string, language_label string"
        )
    akas = base.read_silver(spark, cfg, "title_akas").join(
        film_ids, F.col("titleId") == film_ids["tconst"], "left_semi"
    )
    fallback = akas_film_languages(akas, films, region_languages, aliases)
    languages = film_languages(wikidata, fallback).persist()
    kept = languages.where(F.col("n_languages") == 1) if multilingual == EXCLUDE else languages

    principals = (
        base.read_silver(spark, cfg, "title_principals")
        .where(F.col("category").isin(categories))
        .join(film_ids, "tconst", "left_semi")
    )
    credits = principals.select("nconst", "tconst").distinct()
    names = base.read_silver(spark, cfg, "name_basics").select("nconst", "primaryName")
    result = (
        actor_languages(credits, kept, films)
        .where(F.col("n_languages") >= 2)
        .join(names, "nconst", "left")
        .select(
            "nconst", "primaryName", "n_languages", "languages", "n_successful_films", "examples"
        )
    )
    path = base.write_gold(result, cfg, NAME)
    result = spark.read.parquet(path).orderBy(
        F.col("n_languages").desc(), F.col("n_successful_films").desc(), "nconst"
    )

    n_films = films.count()
    per_film = languages.groupBy("tconst").agg(
        F.first("language_source").alias("language_source"),
        F.first("n_languages").alias("n_languages"),
    )
    status = F.when(F.col("language_source").isNull(), F.lit("unknown")).otherwise(
        F.col("language_source")
    )
    coverage = (
        films.select("tconst")
        .join(per_film, "tconst", "left")
        .groupBy(status.alias("language_source"))
        .agg(
            F.count(F.lit(1)).alias("films"),
            F.sum(F.when(F.col("n_languages") > 1, 1).otherwise(0)).alias(
                "films_with_several_languages"
            ),
        )
        .withColumn("pct_of_successful_films", 100.0 * F.col("films") / F.lit(n_films))
        .orderBy(F.col("films").desc())
    )
    distribution = (
        result.groupBy("n_languages").agg(F.count(F.lit(1)).alias("people")).orderBy("n_languages")
    )
    top_languages = (
        kept.groupBy("language", "language_label")
        .agg(F.countDistinct("tconst").alias("films"))
        .orderBy(F.col("films").desc())
    )
    three_plus = result.where(F.col("n_languages") >= 3)
    n_two, n_three = result.count(), three_plus.count()
    LOGGER.info("Q6: %d people with >= 2 languages, %d with >= 3", n_two, n_three)

    parameters = {
        **base.feature_film_parameters(cfg),
        "min_rating": min_rating,
        "min_votes": min_votes,
        "categories": categories,
        "multilingual_films": multilingual,
        "language_aliases": [f"{k}->{v}" for k, v in aliases.items()],
        "language_sources": [SOURCE_WIKIDATA, SOURCE_AKAS_LANGUAGE, SOURCE_AKAS_REGION],
        "successful_films": n_films,
        "films_used_in_the_analysis": kept.select("tconst").distinct().count(),
        "people_with_2_or_more_languages": n_two,
        "people_with_3_or_more_languages": n_three,
    }
    base.write_report(
        cfg,
        NAME,
        "Q6 - Actors and actresses successful in several original languages",
        parameters,
        [
            base.table_from(coverage, "Original language coverage of the successful films"),
            base.table_from(top_languages, "Most frequent original languages", limit=15),
            base.table_from(distribution, "People per number of languages"),
            base.table_from(
                three_plus.drop("nconst"),
                "Successful in 3 or more languages",
                limit=max_rows,
                total=n_three,
            ),
            base.table_from(
                result.drop("nconst"),
                "Successful in 2 or more languages",
                limit=max_rows,
                total=n_two,
            ),
        ],
        csv_exports={"": result, "three_or_more": three_plus, "coverage": coverage},
    )
    films.unpersist()
    languages.unpersist()
    return result


def run(spark: SparkSession, cfg: Config, limit: int | None = None) -> DataFrame:
    """Run the three stages."""
    run_scope(spark, cfg)
    run_collect(spark, cfg, limit)
    return run_analysis(spark, cfg)


def main() -> None:
    """CLI entry point."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    parser.add_argument("--stage", choices=["all", "scope", "collect", "analysis"], default="all")
    parser.add_argument("--limit", type=int, default=None, help="Collect only the first N films.")
    args = parser.parse_args()
    cfg = load_config(args.config)
    spark = build_spark(cfg, NAME)
    try:
        if args.stage in ("all", "scope"):
            run_scope(spark, cfg)
        if args.stage in ("all", "collect"):
            run_collect(spark, cfg, args.limit)
        if args.stage in ("all", "analysis"):
            run_analysis(spark, cfg)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
