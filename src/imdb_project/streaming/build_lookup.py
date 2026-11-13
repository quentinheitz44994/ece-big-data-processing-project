"""Static lookup of Wikipedia pages linked to the IMDb dataset (Spark batch).

The streaming job decides whether a change is relevant by joining it with this
table. It lists, for the wikis followed by the producer, the Wikipedia page of:

* the films and people already mapped by the enrichment;
* a wider set: the ``lookup.titles`` most voted titles of ``lookup.title_types``
  and the ``lookup.people`` people with the most votes on the titles they are
  credited in (``lookup.principal_categories``).

The IMDb identifiers are mapped to page titles through Wikidata (P345 and
sitelinks) with the same rate-limited client and the same cache as the
enrichment.

Stages: ``scope`` (Spark), ``collect`` (plain Python), ``build`` (Spark). Output:
``data/gold/wiki_lookup/`` with ``wiki``, ``page_title_normalized``, ``imdb_id``,
``entity_type``, ``source_url``.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.logging import get_logger
from imdb_project.common.spark_session import build_spark
from imdb_project.enrichment import fetch_wikidata, raw_reader
from imdb_project.enrichment.select_scope import SCOPE_FILMS, SCOPE_PEOPLE
from imdb_project.exploration import base
from imdb_project.streaming.relevance import normalize_title

LOGGER = get_logger(__name__)

ENTITY_FILM = "film"
ENTITY_SERIES = "tv_series"
ENTITY_PERSON = "person"
LOOKUP_SCOPE = "lookup_scope"
LOOKUP_TABLE = "wiki_lookup"


def top_titles(
    titles: DataFrame,
    ratings: DataFrame,
    title_types: dict[str, str],
    limit: int | None,
) -> DataFrame:
    """Return the most voted titles of the accepted types.

    Args:
        titles: Silver ``title_basics``.
        ratings: Silver ``title_ratings``.
        title_types: Mapping of IMDb ``titleType`` to lookup entity type.
        limit: Number of titles kept (all when ``None``).

    Returns:
        ``imdb_id``, ``entity_type``, ``score`` (number of votes).
    """
    mapping = F.create_map(*[F.lit(part) for item in title_types.items() for part in item])
    scored = base.with_ratings(
        titles.where(F.col("titleType").isin(list(title_types))), ratings
    ).select(
        F.col("tconst").alias("imdb_id"),
        F.try_element_at(mapping, F.col("titleType")).alias("entity_type"),
        F.col("numVotes").cast("long").alias("score"),
    )
    ordered = scored.orderBy(F.col("score").desc(), F.col("imdb_id"))
    return ordered.limit(int(limit)) if limit is not None else ordered


def top_people(
    principals: DataFrame,
    scored_titles: DataFrame,
    categories: list[str] | None,
    limit: int | None,
) -> DataFrame:
    """Return the people with the most votes over the titles they are credited in.

    Args:
        principals: Silver ``title_principals``.
        scored_titles: Output of :func:`top_titles`.
        categories: Principal categories kept (all when ``None``).
        limit: Number of people kept (all when ``None``).

    Returns:
        ``imdb_id``, ``entity_type`` (``person``), ``score`` (sum of votes).
    """
    credits = (
        principals if categories is None else principals.where(F.col("category").isin(categories))
    )
    votes = F.broadcast(scored_titles.select(F.col("imdb_id").alias("tconst"), "score"))
    scored = (
        credits.select("tconst", "nconst")
        .distinct()
        .join(votes, "tconst")
        .groupBy(F.col("nconst").alias("imdb_id"))
        .agg(F.sum("score").alias("score"))
        .withColumn("entity_type", F.lit(ENTITY_PERSON))
        .select("imdb_id", "entity_type", "score")
    )
    ordered = scored.orderBy(F.col("score").desc(), F.col("imdb_id"))
    return ordered.limit(int(limit)) if limit is not None else ordered


def build_lookup_table(links: DataFrame, entities: DataFrame, wikis: list[str]) -> DataFrame:
    """Build the lookup table from the sitelinks and the entity types.

    Args:
        links: Output of ``raw_reader.sitelinks`` (``imdb_id``, ``qid``, ``wiki``,
            ``page_title``).
        entities: ``imdb_id`` and ``entity_type`` of the identifiers of interest.
        wikis: Wikis followed by the streaming job.

    Returns:
        One row per (``wiki``, ``page_title_normalized``). When several
        identifiers share a page, titles win over people, then the lowest
        identifier is kept.
    """
    site = F.concat(
        F.lit("https://"),
        F.regexp_replace(F.regexp_replace("wiki", "wiki$", ""), "_", "-"),
        F.lit(".wikipedia.org/wiki/"),
    )
    rows = (
        links.where(F.col("wiki").isin(wikis))
        .join(entities.select("imdb_id", "entity_type").dropDuplicates(["imdb_id"]), "imdb_id")
        .withColumn("page_title_normalized", normalize_title(F.col("page_title")))
        .withColumn(
            "source_url", F.concat(site, F.regexp_replace("page_title_normalized", " ", "_"))
        )
    )
    preferred = Window.partitionBy("wiki", "page_title_normalized").orderBy(
        F.when(F.col("entity_type") == ENTITY_PERSON, 1).otherwise(0), F.col("imdb_id")
    )
    return (
        rows.withColumn("rank", F.row_number().over(preferred))
        .where(F.col("rank") == 1)
        .select("wiki", "page_title_normalized", "imdb_id", "entity_type", "qid", "source_url")
    )


def _scope_path(cfg: Config) -> str:
    return io.layer_path(cfg, "streaming", LOOKUP_SCOPE)


def run_scope(spark: SparkSession, cfg: Config) -> DataFrame:
    """Stage 1 (Spark): choose the IMDb identifiers to map and write them."""
    settings = cfg.streaming.lookup
    titles = base.read_silver(spark, cfg, "title_basics")
    scored_titles = top_titles(
        titles,
        base.read_silver(spark, cfg, "title_ratings"),
        dict(settings.title_types),
        settings.get("titles"),
    ).persist()
    categories = settings.get("principal_categories")
    people = top_people(
        base.read_silver(spark, cfg, "title_principals").join(
            F.broadcast(scored_titles.select(F.col("imdb_id").alias("tconst"))),
            "tconst",
            "left_semi",
        ),
        scored_titles,
        list(categories) if categories is not None else None,
        settings.get("people"),
    )
    scope = scored_titles.unionByName(people)

    films_path = Path(io.layer_path(cfg, "enrichment", SCOPE_FILMS))
    people_path = Path(io.layer_path(cfg, "enrichment", SCOPE_PEOPLE))
    if films_path.exists() and people_path.exists():
        enriched_films = spark.read.parquet(str(films_path)).select(
            F.col("tconst").alias("imdb_id"),
            F.lit(ENTITY_FILM).alias("entity_type"),
            F.col("numVotes").cast("long").alias("score"),
        )
        enriched_people = (
            spark.read.parquet(str(people_path))
            .select(F.col("nconst").alias("imdb_id"))
            .distinct()
            .withColumn("entity_type", F.lit(ENTITY_PERSON))
            .withColumn("score", F.lit(None).cast("long"))
        )
        scope = scope.unionByName(enriched_films).unionByName(enriched_people)
    scope = scope.groupBy("imdb_id").agg(
        F.first("entity_type").alias("entity_type"), F.max("score").alias("score")
    )
    io.write_parquet(scope, _scope_path(cfg))
    scored_titles.unpersist()
    written = spark.read.parquet(_scope_path(cfg))
    LOGGER.info("lookup scope: %d identifiers", written.count())
    return written


def run_collect(spark: SparkSession, cfg: Config, limit: int | None = None) -> None:
    """Stage 2 (plain Python): map the identifiers to page titles through Wikidata."""
    rows = spark.read.parquet(_scope_path(cfg)).select("imdb_id").collect()
    ids = sorted(row.imdb_id for row in rows)
    fetch_wikidata.collect(
        cfg, "sitelinks", ids[:limit] if limit else ids, "streaming:lookup_sitelinks"
    )


def run_build(spark: SparkSession, cfg: Config) -> DataFrame:
    """Stage 3 (Spark): build the lookup table and write it with its report."""
    wikis = list(cfg.streaming.wikis)
    scope = spark.read.parquet(_scope_path(cfg))
    lookup = build_lookup_table(raw_reader.sitelinks(spark, cfg), scope, wikis)
    path = io.layer_path(cfg, "gold", LOOKUP_TABLE)
    io.write_parquet(lookup, path)
    lookup = spark.read.parquet(path)

    per_type = (
        lookup.groupBy("wiki", "entity_type")
        .agg(F.count(F.lit(1)).alias("pages"))
        .orderBy("wiki", "entity_type")
    )
    scope_counts = scope.groupBy("entity_type").agg(F.count(F.lit(1)).alias("identifiers"))
    mapped = lookup.groupBy("entity_type").agg(
        F.countDistinct("imdb_id").alias("identifiers_with_a_page")
    )
    coverage = (
        scope_counts.join(mapped, "entity_type", "left")
        .na.fill(0, ["identifiers_with_a_page"])
        .withColumn(
            "pct_with_a_page", 100.0 * F.col("identifiers_with_a_page") / F.col("identifiers")
        )
        .orderBy("entity_type")
    )
    settings = cfg.streaming.lookup
    io.write_markdown(
        io.output_path(cfg, "streaming", "lookup.md"),
        "Streaming lookup table (Wikipedia pages linked to IMDb identifiers)",
        [
            base.table_from(coverage, "IMDb identifiers of the lookup scope"),
            base.table_from(per_type, "Pages per wiki and entity type"),
        ],
        parameters={
            "wikis": wikis,
            "lookup.titles": settings.get("titles"),
            "lookup.title_types": [f"{k}->{v}" for k, v in dict(settings.title_types).items()],
            "lookup.people": settings.get("people"),
            "lookup.principal_categories": settings.get("principal_categories"),
            "identifier_mapping": "Wikidata P345 and sitelinks",
            "pages": lookup.count(),
        },
    )
    LOGGER.info("lookup table: %d pages", lookup.count())
    return lookup


def main() -> None:
    """CLI entry point."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    parser.add_argument("--stage", choices=["all", "scope", "collect", "build"], default="all")
    parser.add_argument("--limit", type=int, default=None, help="Map only the first N identifiers.")
    args = parser.parse_args()
    cfg = load_config(args.config)
    spark = build_spark(cfg, "build_lookup")
    try:
        if args.stage in ("all", "scope"):
            run_scope(spark, cfg)
        if args.stage in ("all", "collect"):
            run_collect(spark, cfg, args.limit)
        if args.stage in ("all", "build"):
            run_build(spark, cfg)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
