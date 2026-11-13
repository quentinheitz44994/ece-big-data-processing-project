"""Q1 - Feature films whose runtime is notably different from their genre average.

Per genre: mean, standard deviation and quartiles of ``runtimeMinutes``. A film
is reported for a genre when ``|z-score| > z_threshold`` **or** when its runtime
lies outside ``[Q1 - k * IQR, Q3 + k * IQR]`` (``k = iqr_multiplier``). Genres
with fewer than ``min_films_per_genre`` films are not analysed.
"""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F

from imdb_project.common.config import Config
from imdb_project.common.logging import get_logger
from imdb_project.exploration import base

LOGGER = get_logger(__name__)
NAME = "q1_runtime_outliers"

METHOD_BOTH = "zscore+iqr"
METHOD_ZSCORE = "zscore"
METHOD_IQR = "iqr"


def genre_runtime_stats(films_by_genre: DataFrame, iqr_multiplier: float) -> DataFrame:
    """Compute the runtime distribution of each genre.

    Args:
        films_by_genre: One row per (film, genre) with ``runtimeMinutes``.
        iqr_multiplier: Multiplier ``k`` of the interquartile range fences.

    Returns:
        One row per genre: ``n_films``, ``mean_runtime``, ``std_runtime``, ``q1``,
        ``median``, ``q3``, ``iqr``, ``lower_fence``, ``upper_fence``.
    """
    quartiles = F.percentile("runtimeMinutes", [0.25, 0.5, 0.75])
    stats = films_by_genre.groupBy("genre").agg(
        F.count(F.lit(1)).alias("n_films"),
        F.avg("runtimeMinutes").alias("mean_runtime"),
        F.stddev_samp("runtimeMinutes").alias("std_runtime"),
        quartiles.alias("quartiles"),
    )
    return (
        stats.withColumn("q1", F.col("quartiles")[0])
        .withColumn("median", F.col("quartiles")[1])
        .withColumn("q3", F.col("quartiles")[2])
        .withColumn("iqr", F.col("q3") - F.col("q1"))
        .withColumn("lower_fence", F.col("q1") - iqr_multiplier * F.col("iqr"))
        .withColumn("upper_fence", F.col("q3") + iqr_multiplier * F.col("iqr"))
        .drop("quartiles")
    )


def runtime_outliers(films_by_genre: DataFrame, stats: DataFrame, z_threshold: float) -> DataFrame:
    """Return the (film, genre) pairs whose runtime is an outlier for the genre.

    Args:
        films_by_genre: One row per (film, genre) with ``runtimeMinutes``.
        stats: Output of :func:`genre_runtime_stats` (analysed genres only).
        z_threshold: Absolute z-score above which a film is an outlier.

    Returns:
        The outliers with ``z_score``, ``method`` (``zscore``, ``iqr`` or
        ``zscore+iqr``) and ``direction`` (``longer`` / ``shorter``).
    """
    scored = films_by_genre.join(F.broadcast(stats), "genre").withColumn(
        "z_score",
        F.try_divide(F.col("runtimeMinutes") - F.col("mean_runtime"), F.col("std_runtime")),
    )
    by_z = F.coalesce(F.abs(F.col("z_score")) > z_threshold, F.lit(False))
    by_iqr = (F.col("runtimeMinutes") < F.col("lower_fence")) | (
        F.col("runtimeMinutes") > F.col("upper_fence")
    )
    method = (
        F.when(by_z & by_iqr, F.lit(METHOD_BOTH))
        .when(by_z, F.lit(METHOD_ZSCORE))
        .otherwise(F.lit(METHOD_IQR))
    )
    direction = F.when(F.col("runtimeMinutes") > F.col("mean_runtime"), "longer").otherwise(
        "shorter"
    )
    return (
        scored.where(by_z | by_iqr)
        .withColumn("method", method)
        .withColumn("direction", direction)
        .select(
            "genre",
            "tconst",
            "primaryTitle",
            "startYear",
            "runtimeMinutes",
            F.col("mean_runtime").alias("genre_mean_runtime"),
            "z_score",
            "lower_fence",
            "upper_fence",
            "method",
            "direction",
        )
    )


def top_outliers_per_genre(outliers: DataFrame, top_n: int) -> DataFrame:
    """Keep the ``top_n`` outliers of each genre by absolute z-score."""
    ranking = Window.partitionBy("genre").orderBy(F.abs(F.col("z_score")).desc(), F.col("tconst"))
    return (
        outliers.withColumn("rank_in_genre", F.row_number().over(ranking))
        .where(F.col("rank_in_genre") <= top_n)
        .orderBy("genre", "rank_in_genre")
    )


def run(spark: SparkSession, cfg: Config) -> DataFrame:
    """Answer Q1 and write the gold table and the reports."""
    z_threshold = float(base.question_setting(cfg, "q1", "z_threshold", 2.0))
    iqr_multiplier = float(base.question_setting(cfg, "q1", "iqr_multiplier", 1.5))
    min_films = int(base.question_setting(cfg, "q1", "min_films_per_genre", 30))
    top_per_genre = int(base.question_setting(cfg, "q1", "top_per_genre", 20))

    films = base.feature_films(base.read_silver(spark, cfg, "title_basics"), cfg)
    films_by_genre = (
        base.explode_genres(films)
        .select("tconst", "primaryTitle", "startYear", "runtimeMinutes", "genre")
        .persist()
    )
    all_stats = genre_runtime_stats(films_by_genre, iqr_multiplier).persist()
    stats = all_stats.where(F.col("n_films") >= min_films)
    outliers = runtime_outliers(films_by_genre, stats, z_threshold)
    path = base.write_gold(outliers, cfg, NAME)
    outliers = spark.read.parquet(path)

    per_genre = outliers.groupBy("genre").agg(
        F.count(F.lit(1)).alias("n_outliers"),
        F.sum(F.when(F.col("direction") == "longer", 1).otherwise(0)).alias("n_longer"),
        F.sum(F.when(F.col("direction") == "shorter", 1).otherwise(0)).alias("n_shorter"),
        F.sum(F.when(F.col("method") == METHOD_BOTH, 1).otherwise(0)).alias("n_zscore_and_iqr"),
        F.sum(F.when(F.col("method") == METHOD_ZSCORE, 1).otherwise(0)).alias("n_zscore_only"),
        F.sum(F.when(F.col("method") == METHOD_IQR, 1).otherwise(0)).alias("n_iqr_only"),
    )
    summary = (
        all_stats.join(per_genre, "genre", "left")
        .na.fill(0, [c for c in per_genre.columns if c != "genre"])
        .withColumn("analysed", F.col("n_films") >= min_films)
        .withColumn("pct_outliers", 100.0 * F.col("n_outliers") / F.col("n_films"))
        .select(
            "genre",
            "n_films",
            "analysed",
            "mean_runtime",
            "std_runtime",
            "q1",
            "median",
            "q3",
            "lower_fence",
            "upper_fence",
            "n_outliers",
            "pct_outliers",
            "n_longer",
            "n_shorter",
            "n_zscore_and_iqr",
            "n_zscore_only",
            "n_iqr_only",
        )
        .orderBy("genre")
    )
    n_pairs = outliers.count()
    n_films = outliers.select("tconst").distinct().count()
    LOGGER.info("Q1: %d outlier (film, genre) pairs, %d distinct films", n_pairs, n_films)

    top = top_outliers_per_genre(outliers, top_per_genre).drop("lower_fence", "upper_fence")
    parameters = {
        **base.feature_film_parameters(cfg),
        "z_threshold": z_threshold,
        "iqr_multiplier": iqr_multiplier,
        "min_films_per_genre": min_films,
        "top_per_genre": top_per_genre,
        "outlier_rule": "abs(z_score) > z_threshold OR runtime outside the IQR fences",
        "feature_films": films_by_genre.select("tconst").distinct().count(),
        "outlier_film_genre_pairs": n_pairs,
        "outlier_distinct_films": n_films,
    }
    base.write_report(
        cfg,
        NAME,
        "Q1 - Feature films with a runtime notably different from their genre",
        parameters,
        [
            base.table_from(summary, "Runtime distribution and outliers per genre"),
            base.table_from(
                top, f"Top {top_per_genre} outliers per genre (by absolute z-score)", total=n_pairs
            ),
        ],
        csv_exports={
            "summary": summary,
            "": outliers.orderBy("genre", F.abs(F.col("z_score")).desc(), "tconst"),
        },
    )
    films_by_genre.unpersist()
    all_stats.unpersist()
    return outliers


if __name__ == "__main__":
    base.run_job(NAME, run, __doc__)
