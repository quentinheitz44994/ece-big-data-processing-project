"""Q3 - How the top three genres of a year compare to the other genres.

Built on the (year, genre) popularity table of Q2. For each year the genres are
split into ``top`` (rank <= ``top_n``) and ``rest``; the two groups are compared
on votes, number of films, votes per film and vote-weighted rating. The same
comparison is aggregated per decade, and the stability of the podium is measured
by the number of years each genre spends in it.

A film counts once in each of its genres, so the sums are over (film, genre) pairs.
"""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from imdb_project.common.config import Config
from imdb_project.exploration import base
from imdb_project.exploration.q2_top_genres import genre_year_popularity, rated_films_by_genre

NAME = "q3_top_vs_rest"
GROUP_TOP = "top"
GROUP_REST = "rest"


def with_group(popularity: DataFrame, top_n: int) -> DataFrame:
    """Label each (year, genre) row as ``top`` or ``rest``."""
    group = F.when(F.col("rank") <= top_n, F.lit(GROUP_TOP)).otherwise(F.lit(GROUP_REST))
    return popularity.withColumn("genre_group", group)


def compare_groups(grouped: DataFrame, period_column: str) -> DataFrame:
    """Compare the ``top`` and ``rest`` groups over a period (year or decade).

    Args:
        grouped: Output of :func:`with_group`, with the period column.
        period_column: Column identifying the period.

    Returns:
        One row per period with, for each group, the number of genres (average
        per year), film-genre pairs, votes, votes per film and weighted rating,
        plus the share of votes of the top group and the top/rest ratios.
    """
    weighted_sum = F.col("weighted_rating") * F.col("total_votes")
    per_group = grouped.groupBy(period_column, "genre_group").agg(
        (F.count(F.lit(1)) / F.countDistinct("startYear")).alias("genres_per_year"),
        F.sum("n_films").alias("films"),
        F.sum("total_votes").alias("votes"),
        (F.sum(weighted_sum) / F.sum("total_votes")).alias("weighted_rating"),
    )
    per_group = per_group.withColumn("votes_per_film", F.col("votes") / F.col("films"))

    def side(group: str) -> DataFrame:
        prefix = f"{group}_"
        return per_group.where(F.col("genre_group") == group).select(
            period_column,
            *[
                F.col(name).alias(prefix + name)
                for name in (
                    "genres_per_year",
                    "films",
                    "votes",
                    "votes_per_film",
                    "weighted_rating",
                )
            ],
        )

    joined = side(GROUP_TOP).join(side(GROUP_REST), period_column, "left")
    total_votes = F.col("top_votes") + F.coalesce(F.col("rest_votes"), F.lit(0))
    return (
        joined.withColumn("top_vote_share_pct", 100.0 * F.col("top_votes") / total_votes)
        .withColumn("votes_ratio_top_rest", F.try_divide(F.col("top_votes"), F.col("rest_votes")))
        .withColumn(
            "votes_per_film_ratio_top_rest",
            F.try_divide(F.col("top_votes_per_film"), F.col("rest_votes_per_film")),
        )
        .withColumn(
            "weighted_rating_diff_top_rest",
            F.col("top_weighted_rating") - F.col("rest_weighted_rating"),
        )
        .orderBy(period_column)
    )


def podium_stability(grouped: DataFrame) -> DataFrame:
    """Count, per genre, the years spent in the top group and at rank 1.

    Args:
        grouped: Output of :func:`with_group`.

    Returns:
        One row per genre that reached the top group at least once.
    """
    in_top = F.col("genre_group") == GROUP_TOP
    n_years = grouped.select("startYear").distinct().count()
    return (
        grouped.groupBy("genre")
        .agg(
            F.sum(F.when(in_top, 1).otherwise(0)).alias("years_in_top"),
            F.sum(F.when(F.col("rank") == 1, 1).otherwise(0)).alias("years_ranked_first"),
            F.min(F.when(in_top, F.col("startYear"))).alias("first_year_in_top"),
            F.max(F.when(in_top, F.col("startYear"))).alias("last_year_in_top"),
            F.avg("rank").alias("average_rank"),
            F.avg("vote_share_pct").alias("average_vote_share_pct"),
        )
        .where(F.col("years_in_top") > 0)
        .withColumn("pct_years_in_top", 100.0 * F.col("years_in_top") / F.lit(n_years))
        .orderBy(F.col("years_in_top").desc(), F.col("average_rank"))
    )


def run(spark: SparkSession, cfg: Config) -> DataFrame:
    """Answer Q3 and write the gold table and the reports."""
    top_n = int(base.question_setting(cfg, "q2", "top_n", 3))
    popularity = genre_year_popularity(rated_films_by_genre(spark, cfg, "q2"))
    grouped = (
        with_group(popularity, top_n)
        .withColumn("decade", (F.floor(F.col("startYear") / 10) * 10).cast("int"))
        .persist()
    )
    yearly = compare_groups(grouped, "startYear").withColumnRenamed("startYear", "year")
    path = base.write_gold(yearly, cfg, NAME)
    yearly = spark.read.parquet(path).orderBy("year")
    by_decade = compare_groups(grouped, "decade")
    stability = podium_stability(grouped)

    display = [
        "top_vote_share_pct",
        "votes_ratio_top_rest",
        "top_films",
        "rest_films",
        "top_votes_per_film",
        "rest_votes_per_film",
        "votes_per_film_ratio_top_rest",
        "top_weighted_rating",
        "rest_weighted_rating",
        "weighted_rating_diff_top_rest",
        "rest_genres_per_year",
    ]
    parameters = {
        **base.feature_film_parameters(cfg),
        "min_votes": int(base.question_setting(cfg, "q2", "min_votes", 0)),
        "year_min": int(base.question_setting(cfg, "q2", "year_min")),
        "year_max": int(base.question_setting(cfg, "q2", "year_max")),
        "top_n": top_n,
        "top": "genres ranked <= top_n in the year (Q2 ranking)",
        "rest": "all the other genres of the year",
        "films": "(film, genre) pairs: a film counts once in each of its genres",
        "weighted_rating": "sum(averageRating * numVotes) / sum(numVotes)",
    }
    base.write_report(
        cfg,
        NAME,
        f"Q3 - Top {top_n} genres versus the other genres",
        parameters,
        [
            base.table_from(by_decade.select("decade", *display), "Comparison per decade"),
            base.table_from(yearly.select("year", *display), "Comparison per year"),
            base.table_from(stability, f"Stability of the top {top_n} (years spent in it)"),
        ],
        csv_exports={"yearly": yearly, "by_decade": by_decade, "stability": stability},
    )
    grouped.unpersist()
    return yearly


if __name__ == "__main__":
    base.run_job(NAME, run, __doc__)
