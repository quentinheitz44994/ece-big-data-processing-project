"""Q7 - Long-career actors and actresses whose popularity peaked early.

Population: people credited as ``categories`` (actor / actress) in rated feature
films, with a career of at least ``min_career_years`` years (last minus first
release year) and at least ``min_films`` such films.

A career "peaked early" when both conditions hold:

* the best-rated film (ties: most votes, then earliest) was released within the
  first ``early_fraction`` of the career;
* the mean rating of the first half of the career is higher than the mean rating
  of the second half.

Two additional measures are reported for every person of the population: the
slope of the linear regression ``rating ~ year`` and the mean career position of
the ``top_k`` best-rated films (0 = first year, 1 = last year).
"""

from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction

from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F

from imdb_project.common.config import Config
from imdb_project.common.logging import get_logger
from imdb_project.exploration import base

LOGGER = get_logger(__name__)
NAME = "q7_early_peak_actors"


def career_fraction(cfg: Config) -> float:
    """Resolve the early-career fraction without rounding a configured ratio."""
    value = base.question_setting(cfg, "q7", "early_fraction", 1 / 3)
    fraction = (
        float(Fraction(value["numerator"], value["denominator"]))
        if isinstance(value, Mapping)
        else float(value)
    )
    if not 0 < fraction <= 1:
        raise ValueError("early_fraction must be in (0, 1]")
    return fraction


def actor_filmography(principals: DataFrame, films: DataFrame, categories: list[str]) -> DataFrame:
    """Return one row per (person, film) for the acting categories.

    Args:
        principals: ``title_principals`` rows.
        films: Rated feature films with ``startYear``, ``averageRating``, ``numVotes``.
        categories: Principal categories counted as acting credits.

    Returns:
        Columns ``nconst``, ``tconst``, ``startYear``, ``averageRating``, ``numVotes``.
    """
    credits = (
        principals.where(F.col("category").isin(categories)).select("nconst", "tconst").distinct()
    )
    dated = films.where(F.col("startYear").isNotNull()).select(
        "tconst", "startYear", "averageRating", "numVotes"
    )
    return credits.join(dated, "tconst")


def career_profiles(filmography: DataFrame, min_career_years: int, min_films: int) -> DataFrame:
    """Aggregate each career and keep the long ones.

    Args:
        filmography: Output of :func:`actor_filmography`.
        min_career_years: Minimum span between first and last film.
        min_films: Minimum number of films.

    Returns:
        One row per person: ``first_year``, ``last_year``, ``career_years``,
        ``n_films``, ``avg_rating``, the best film (``peak_tconst``, ``peak_year``,
        ``peak_rating``) and its career position ``peak_position`` in [0, 1].
    """
    best = F.max(
        F.struct(
            F.col("averageRating").alias("rating"),
            F.col("numVotes").alias("votes"),
            (-F.col("startYear")).alias("minus_year"),
            F.col("tconst"),
        )
    )
    profiles = (
        filmography.groupBy("nconst")
        .agg(
            F.min("startYear").alias("first_year"),
            F.max("startYear").alias("last_year"),
            F.count(F.lit(1)).alias("n_films"),
            F.avg("averageRating").alias("avg_rating"),
            best.alias("best"),
        )
        .withColumn("career_years", F.col("last_year") - F.col("first_year"))
        .where((F.col("career_years") >= min_career_years) & (F.col("n_films") >= min_films))
    )
    peak_year = -F.col("best.minus_year")
    return profiles.select(
        "nconst",
        "first_year",
        "last_year",
        "career_years",
        "n_films",
        "avg_rating",
        F.col("best.tconst").alias("peak_tconst"),
        peak_year.alias("peak_year"),
        F.col("best.rating").alias("peak_rating"),
        ((peak_year - F.col("first_year")) / F.col("career_years")).alias("peak_position"),
    )


def early_peak(
    filmography: DataFrame, profiles: DataFrame, early_fraction: float, top_k: int
) -> DataFrame:
    """Compute the early-peak indicators of every long career.

    Args:
        filmography: Output of :func:`actor_filmography`.
        profiles: Output of :func:`career_profiles`.
        early_fraction: Share of the career in which the best film must fall.
        top_k: Number of best-rated films averaged in ``top_k_mean_position``.

    Returns:
        ``profiles`` with ``first_half_avg``, ``second_half_avg``, ``rating_slope``
        (rating points per year), ``top_k_mean_position`` and ``early_peak``.
    """
    films = filmography.join(F.broadcast(profiles), "nconst")
    position = (F.col("startYear") - F.col("first_year")) / F.col("career_years")
    midpoint = F.col("first_year") + F.col("career_years") / 2.0
    by_rating = Window.partitionBy("nconst").orderBy(
        F.col("averageRating").desc(), F.col("numVotes").desc(), F.col("startYear"), F.col("tconst")
    )
    ranked = films.withColumn("position", position).withColumn(
        "rating_rank", F.row_number().over(by_rating)
    )
    in_first_half = F.col("startYear") <= midpoint
    indicators = ranked.groupBy("nconst").agg(
        F.avg(F.when(in_first_half, F.col("averageRating"))).alias("first_half_avg"),
        F.avg(F.when(~in_first_half, F.col("averageRating"))).alias("second_half_avg"),
        F.try_divide(F.covar_samp("startYear", "averageRating"), F.var_samp("startYear")).alias(
            "rating_slope"
        ),
        F.avg(F.when(F.col("rating_rank") <= top_k, F.col("position"))).alias(
            "top_k_mean_position"
        ),
    )
    is_early = (F.col("peak_position") <= early_fraction) & (
        F.col("first_half_avg") > F.col("second_half_avg")
    )
    return profiles.join(indicators, "nconst").withColumn(
        "early_peak", F.coalesce(is_early, F.lit(False))
    )


def run(spark: SparkSession, cfg: Config) -> DataFrame:
    """Answer Q7 and write the gold table and the reports."""
    categories = list(base.question_setting(cfg, "q7", "categories", ["actor", "actress"]))
    min_career = int(base.question_setting(cfg, "q7", "min_career_years", 20))
    min_films = int(base.question_setting(cfg, "q7", "min_films", 15))
    early_fraction = career_fraction(cfg)
    top_k = int(base.question_setting(cfg, "q7", "top_k", 3))
    min_votes = int(base.question_setting(cfg, "q7", "min_votes", 0))
    max_rows = int(base.question_setting(cfg, "q7", "max_md_rows", 50))

    titles = base.read_silver(spark, cfg, "title_basics")
    films = (
        base.with_ratings(
            base.feature_films(titles, cfg),
            base.read_silver(spark, cfg, "title_ratings"),
            min_votes,
        )
        .select("tconst", "primaryTitle", "startYear", "averageRating", "numVotes")
        .persist()
    )
    principals = (
        base.read_silver(spark, cfg, "title_principals")
        .where(F.col("category").isin(categories))
        .join(F.broadcast(films.select("tconst")), "tconst", "left_semi")
    )
    filmography = actor_filmography(principals, films, categories).persist()
    profiles = career_profiles(filmography, min_career, min_films)
    careers = early_peak(filmography, profiles, early_fraction, top_k)

    names = base.read_silver(spark, cfg, "name_basics").select("nconst", "primaryName", "birthYear")
    peak_titles = films.select(
        F.col("tconst").alias("peak_tconst"), F.col("primaryTitle").alias("peak_title")
    )
    result = (
        careers.join(names, "nconst", "left")
        .join(F.broadcast(peak_titles), "peak_tconst", "left")
        .select(
            "nconst",
            "primaryName",
            "birthYear",
            "first_year",
            "last_year",
            "career_years",
            "n_films",
            "avg_rating",
            "peak_title",
            "peak_year",
            "peak_rating",
            "peak_position",
            "first_half_avg",
            "second_half_avg",
            "rating_slope",
            "top_k_mean_position",
            "early_peak",
        )
    )
    path = base.write_gold(result, cfg, NAME)
    result = spark.read.parquet(path)
    early = result.where(F.col("early_peak")).orderBy(
        (F.col("first_half_avg") - F.col("second_half_avg")).desc(), "nconst"
    )
    population = result.count()
    n_early = early.count()
    LOGGER.info("Q7: %d early peaks among %d long careers", n_early, population)

    summary = (
        result.groupBy("early_peak")
        .agg(
            F.count(F.lit(1)).alias("people"),
            F.avg("career_years").alias("avg_career_years"),
            F.avg("n_films").alias("avg_films"),
            F.avg("peak_position").alias("avg_peak_position"),
            F.avg("top_k_mean_position").alias("avg_top_k_mean_position"),
            F.avg(F.col("first_half_avg") - F.col("second_half_avg")).alias(
                "avg_first_minus_second_half"
            ),
            F.avg("rating_slope").alias("avg_rating_slope"),
            (100.0 * F.avg(F.when(F.col("rating_slope") < 0, 1.0).otherwise(0.0))).alias(
                "pct_negative_slope"
            ),
        )
        .orderBy(F.col("early_peak").desc())
    )
    parameters = {
        **base.feature_film_parameters(cfg),
        "min_votes": min_votes,
        "categories": categories,
        "min_career_years": min_career,
        "min_films": min_films,
        "early_fraction": early_fraction,
        "top_k": top_k,
        "career_years": "last release year - first release year of the films considered",
        "early_peak": (
            "peak_position <= early_fraction AND first_half_avg > second_half_avg "
            "(peak = best-rated film; ties: most votes, then earliest)"
        ),
        "rating_slope": "covar_samp(year, rating) / var_samp(year), rating points per year",
        "long_career_people": population,
        "early_peak_people": n_early,
        "sorted_by": "first_half_avg - second_half_avg desc",
    }
    base.write_report(
        cfg,
        NAME,
        "Q7 - Long-career actors and actresses whose ratings peaked early",
        parameters,
        [
            base.table_from(summary, "Population summary (early peak versus others)"),
            base.table_from(
                early.drop("nconst", "early_peak"),
                "Actors and actresses with an early peak",
                limit=max_rows,
                total=n_early,
            ),
        ],
        csv_exports={"": early, "summary": summary},
    )
    films.unpersist()
    filmography.unpersist()
    return result


if __name__ == "__main__":
    base.run_job(NAME, run, __doc__)
