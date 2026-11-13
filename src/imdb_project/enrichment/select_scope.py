"""Enrichment scope (Spark): which films and which people are enriched.

* Films: rated feature films released between ``year_min`` and ``year_max``,
  the ``top_n`` of each (genre, year) ranked by ``rank_by`` (descending, ties
  broken by ``tconst``). A film selected through several genres is kept once,
  with the list of its (genre, year, rank) selections.
* People: for each selected film, the first ``principals_per_film`` distinct
  people by ``ordering`` among the ``principal_categories``.

No scope constant is baked into the logic: setting ``top_n``, ``year_min``,
``year_max``, ``principals_per_film`` or ``principal_categories`` to null in the
settings removes the corresponding restriction, up to the whole dataset.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.logging import get_logger
from imdb_project.common.spark_session import build_spark
from imdb_project.exploration import base

LOGGER = get_logger(__name__)

SCOPE_FILMS = "scope_films.parquet"
SCOPE_PEOPLE = "scope_people.parquet"


def scope_films(
    films: DataFrame,
    year_min: int | None,
    year_max: int | None,
    top_n: int | None,
    rank_by: Sequence[str],
) -> DataFrame:
    """Select the films to enrich.

    Args:
        films: Rated feature films (``tconst``, titles, ``startYear``, ``genres``,
            ``averageRating``, ``numVotes``).
        year_min: First release year kept (no lower bound when ``None``).
        year_max: Last release year kept (no upper bound when ``None``).
        top_n: Films kept per (genre, year) (all when ``None``).
        rank_by: Columns ranking the films of a (genre, year), all descending.

    Returns:
        One row per film with ``selections`` (array of ``genre``, ``year``,
        ``rank``) and ``best_rank``.
    """
    candidates = films.where(F.col("startYear").isNotNull())
    if year_min is not None:
        candidates = candidates.where(F.col("startYear") >= int(year_min))
    if year_max is not None:
        candidates = candidates.where(F.col("startYear") <= int(year_max))

    order = [F.col(column).desc() for column in rank_by] + [F.col("tconst")]
    ranked = base.explode_genres(candidates).withColumn(
        "rank", F.row_number().over(Window.partitionBy("genre", "startYear").orderBy(*order))
    )
    if top_n is not None:
        ranked = ranked.where(F.col("rank") <= int(top_n))

    selection = F.struct(
        F.col("genre").alias("genre"), F.col("startYear").alias("year"), F.col("rank").alias("rank")
    )
    return ranked.groupBy(
        "tconst", "primaryTitle", "originalTitle", "startYear", "averageRating", "numVotes"
    ).agg(
        F.sort_array(F.collect_list(selection)).alias("selections"),
        F.min("rank").alias("best_rank"),
    )


def scope_people(
    principals: DataFrame,
    films: DataFrame,
    categories: Sequence[str] | None,
    principals_per_film: int | None,
) -> DataFrame:
    """Select the principals to enrich for each film of the scope.

    Args:
        principals: Silver ``title_principals``.
        films: Output of :func:`scope_films`.
        categories: Principal categories kept (all when ``None``).
        principals_per_film: People kept per film (all when ``None``).

    Returns:
        One row per (film, person): ``ordering`` (first credit of the person on
        the film), ``categories`` and ``rank_in_film``.
    """
    credits = principals.join(F.broadcast(films.select("tconst")), "tconst", "left_semi")
    if categories is not None:
        credits = credits.where(F.col("category").isin(list(categories)))
    per_person = credits.groupBy("tconst", "nconst").agg(
        F.min("ordering").alias("ordering"),
        F.sort_array(F.collect_set("category")).alias("categories"),
    )
    by_film = Window.partitionBy("tconst").orderBy(F.col("ordering"), F.col("nconst"))
    ranked = per_person.withColumn("rank_in_film", F.row_number().over(by_film))
    if principals_per_film is not None:
        ranked = ranked.where(F.col("rank_in_film") <= int(principals_per_film))
    return ranked


def run(spark: SparkSession, cfg: Config) -> tuple[DataFrame, DataFrame]:
    """Build both scope tables, write them and the scope report."""
    scope = cfg.require("enrichment.scope")
    year_min, year_max, top_n = scope.get("year_min"), scope.get("year_max"), scope.get("top_n")
    rank_by = list(scope.get("rank_by", ["numVotes", "averageRating"]))
    categories = scope.get("principal_categories")
    per_film = scope.get("principals_per_film")

    films = base.with_ratings(
        base.feature_films(base.read_silver(spark, cfg, "title_basics"), cfg),
        base.read_silver(spark, cfg, "title_ratings"),
    )
    films_path = io.layer_path(cfg, "enrichment", SCOPE_FILMS)
    io.write_parquet(scope_films(films, year_min, year_max, top_n, rank_by), films_path)
    selected_films = spark.read.parquet(films_path)

    people_path = io.layer_path(cfg, "enrichment", SCOPE_PEOPLE)
    io.write_parquet(
        scope_people(
            base.read_silver(spark, cfg, "title_principals"), selected_films, categories, per_film
        ),
        people_path,
    )
    selected_people = spark.read.parquet(people_path)

    slots = selected_films.select(F.explode("selections").alias("s"))
    per_film_counts = selected_people.groupBy("tconst").count()
    with_enough = (
        per_film_counts.where(F.col("count") >= int(per_film)).count() if per_film else None
    )
    counters = [
        ["(genre, year) groups", slots.select("s.genre", "s.year").distinct().count()],
        ["(film, genre, year) selections", slots.count()],
        ["distinct films", selected_films.count()],
        ["distinct genres", slots.select("s.genre").distinct().count()],
        ["(film, person) pairs", selected_people.count()],
        ["distinct people", selected_people.select("nconst").distinct().count()],
        ["films with at least one selected principal", per_film_counts.count()],
        ["films with principals_per_film selected principals", with_enough],
    ]
    by_decade = (
        selected_films.withColumn("decade", (F.floor(F.col("startYear") / 10) * 10).cast("int"))
        .groupBy("decade")
        .agg(F.count(F.lit(1)).alias("films"))
        .orderBy("decade")
    )
    io.write_markdown(
        io.output_path(cfg, "enrichment", "scope.md"),
        "Enrichment scope",
        [
            io.ReportTable(["counter", "value"], counters, title="Scope size"),
            base.table_from(by_decade, "Films per decade"),
        ],
        parameters={
            **base.feature_film_parameters(cfg),
            "year_min": year_min,
            "year_max": year_max,
            "top_n": top_n,
            "rank_by": [f"{column} desc" for column in rank_by] + ["tconst asc"],
            "principal_categories": categories,
            "principals_per_film": per_film,
            "principal_order": "ordering asc (first credit of each person on the film)",
        },
    )
    LOGGER.info(
        "scope: %d films, %d distinct people",
        selected_films.count(),
        selected_people.select("nconst").distinct().count(),
    )
    return selected_films, selected_people


def main() -> None:
    """CLI entry point."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    args = parser.parse_args()
    cfg = load_config(args.config)
    spark = build_spark(cfg, "enrichment_scope")
    try:
        run(spark, cfg)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
