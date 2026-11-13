"""Q2 - Top three most popular movie genres for each year (1980-2025).

Popularity of a genre in a year = sum of ``numVotes`` of the feature films of
that genre released that year. The number of films and the vote-weighted average
rating are reported alongside. Genres are ranked per year with ``dense_rank``.
"""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F

from imdb_project.common.config import Config
from imdb_project.exploration import base

NAME = "q2_top_genres"


def rated_films_by_genre(spark: SparkSession, cfg: Config, question: str) -> DataFrame:
    """Rated feature films of the analysed years, one row per (film, genre).

    Args:
        spark: Active Spark session.
        cfg: Project configuration.
        question: Question key used to resolve ``min_votes``, ``year_min``, ``year_max``.

    Returns:
        Columns ``tconst``, ``startYear``, ``genre``, ``averageRating``, ``numVotes``.
    """
    min_votes = int(base.question_setting(cfg, question, "min_votes", 0))
    year_min = int(base.question_setting(cfg, question, "year_min"))
    year_max = int(base.question_setting(cfg, question, "year_max"))
    films = base.feature_films(base.read_silver(spark, cfg, "title_basics"), cfg).where(
        F.col("startYear").between(year_min, year_max)
    )
    rated = base.with_ratings(films, base.read_silver(spark, cfg, "title_ratings"), min_votes)
    return base.explode_genres(rated).select(
        "tconst", "startYear", "genre", "averageRating", "numVotes"
    )


def genre_year_popularity(films_by_genre: DataFrame) -> DataFrame:
    """Aggregate popularity per (year, genre) and rank the genres of each year.

    Args:
        films_by_genre: One row per (film, genre) with ``startYear``,
            ``averageRating`` and ``numVotes``.

    Returns:
        One row per (year, genre): ``total_votes``, ``n_films``,
        ``weighted_rating``, ``vote_share_pct`` (share of the votes of the year,
        all genres summed) and ``rank`` (``dense_rank`` by ``total_votes`` desc).
    """
    per_year = Window.partitionBy("startYear")
    aggregated = films_by_genre.groupBy("startYear", "genre").agg(
        F.sum("numVotes").alias("total_votes"),
        F.count(F.lit(1)).alias("n_films"),
        (F.sum(F.col("averageRating") * F.col("numVotes")) / F.sum("numVotes")).alias(
            "weighted_rating"
        ),
    )
    return aggregated.withColumn(
        "vote_share_pct", 100.0 * F.col("total_votes") / F.sum("total_votes").over(per_year)
    ).withColumn("rank", F.dense_rank().over(per_year.orderBy(F.col("total_votes").desc())))


def top_genres(popularity: DataFrame, top_n: int) -> DataFrame:
    """Keep the ``top_n`` genres of each year."""
    return popularity.where(F.col("rank") <= top_n)


def wide_top_table(top: DataFrame, top_n: int) -> DataFrame:
    """Pivot the yearly top genres to one row per year (``#1``, ``#2``...)."""
    label = F.format_string("%s (%.1f%%)", F.col("genre"), F.col("vote_share_pct").cast("double"))
    by_rank = top.groupBy("startYear", "rank").agg(
        F.array_join(F.sort_array(F.collect_list(label)), " / ").alias("genres")
    )
    wide = (
        by_rank.groupBy("startYear").pivot("rank", list(range(1, top_n + 1))).agg(F.first("genres"))
    )
    for rank in range(1, top_n + 1):
        wide = wide.withColumnRenamed(str(rank), f"rank_{rank}")
    return wide.withColumnRenamed("startYear", "year").orderBy("year")


def run(spark: SparkSession, cfg: Config) -> DataFrame:
    """Answer Q2 and write the gold table and the reports."""
    top_n = int(base.question_setting(cfg, "q2", "top_n", 3))
    popularity = genre_year_popularity(rated_films_by_genre(spark, cfg, "q2"))
    path = base.write_gold(popularity, cfg, "q2_genre_year_popularity")
    popularity = spark.read.parquet(path)
    top = top_genres(popularity, top_n)

    long_format = top.select(
        F.col("startYear").alias("year"),
        "rank",
        "genre",
        "total_votes",
        "vote_share_pct",
        "n_films",
        "weighted_rating",
    ).orderBy("year", "rank", "genre")
    parameters = {
        **base.feature_film_parameters(cfg),
        "min_votes": int(base.question_setting(cfg, "q2", "min_votes", 0)),
        "year_min": int(base.question_setting(cfg, "q2", "year_min")),
        "year_max": int(base.question_setting(cfg, "q2", "year_max")),
        "top_n": top_n,
        "popularity": "sum of numVotes of the films of the genre released in the year",
        "vote_share_pct": "genre votes / votes of all genres of the year (film-genre pairs)",
        "ranking": "dense_rank by total_votes desc within the year",
    }
    base.write_report(
        cfg,
        NAME,
        f"Q2 - Top {top_n} most popular movie genres per year",
        parameters,
        [
            base.table_from(
                wide_top_table(top, top_n), f"Top {top_n} genres per year (share of the votes)"
            ),
            base.table_from(long_format, "Detail per year and rank"),
        ],
        csv_exports={
            "": long_format,
            "all_genres": popularity.withColumnRenamed("startYear", "year").orderBy(
                "year", "rank", "genre"
            ),
        },
    )
    return top


if __name__ == "__main__":
    base.run_job(NAME, run, __doc__)
