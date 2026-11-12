"""Q4 - Directors with exactly one film rated >= 8.0 and mediocre other films.

A director is listed when, among the rated feature films they directed:

* exactly one has ``averageRating >= high_rating``;
* at least ``min_other_films`` other films exist, and their mean rating is
  ``<= low_average``.

Directing credits are the union of ``title.crew.directors`` and of the
``director`` category of ``title.principals``, de-duplicated per (film, person).
Only films with at least ``min_votes`` votes are considered.
"""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from imdb_project.common.config import Config
from imdb_project.common.logging import get_logger
from imdb_project.exploration import base

LOGGER = get_logger(__name__)
NAME = "q4_one_hit_directors"


def director_credits(crew: DataFrame, principals: DataFrame) -> DataFrame:
    """Return the distinct (``tconst``, ``nconst``) directing credits.

    Args:
        crew: ``title_crew`` rows (``directors`` array).
        principals: ``title_principals`` rows.

    Returns:
        One row per (film, director), from both sources.
    """
    from_crew = crew.select("tconst", F.explode("directors").alias("nconst"))
    from_principals = principals.where(F.col("category") == "director").select("tconst", "nconst")
    return from_crew.unionByName(from_principals).distinct()


def one_hit_directors(
    filmography: DataFrame, high_rating: float, low_average: float, min_other_films: int
) -> DataFrame:
    """Select the directors matching the "one hit" pattern.

    Args:
        filmography: One row per (director ``nconst``, film) with ``tconst``,
            ``primaryTitle``, ``startYear``, ``averageRating``, ``numVotes``.
        high_rating: Rating from which a film is a hit.
        low_average: Maximum mean rating of the other films.
        min_other_films: Minimum number of other films.

    Returns:
        One row per selected director with the hit and the statistics of the
        other films.
    """
    is_hit = F.col("averageRating") >= high_rating
    hit = F.struct(
        F.col("averageRating").alias("rating"),
        F.col("numVotes").alias("votes"),
        "tconst",
        "primaryTitle",
        "startYear",
    )
    other_rating = F.when(~is_hit, F.col("averageRating"))
    per_director = filmography.groupBy("nconst").agg(
        F.count(F.lit(1)).alias("n_films"),
        F.sum(F.when(is_hit, 1).otherwise(0)).alias("n_hits"),
        F.max(F.when(is_hit, hit)).alias("hit"),
        F.count(other_rating).alias("n_other_films"),
        F.avg(other_rating).alias("avg_other_rating"),
        F.min(other_rating).alias("min_other_rating"),
        F.max(other_rating).alias("max_other_rating"),
    )
    return per_director.where(
        (F.col("n_hits") == 1)
        & (F.col("n_other_films") >= min_other_films)
        & (F.col("avg_other_rating") <= low_average)
    ).select(
        "nconst",
        F.col("hit.tconst").alias("hit_tconst"),
        F.col("hit.primaryTitle").alias("hit_title"),
        F.col("hit.startYear").alias("hit_year"),
        F.col("hit.rating").alias("hit_rating"),
        F.col("hit.votes").alias("hit_votes"),
        "n_other_films",
        "avg_other_rating",
        "min_other_rating",
        "max_other_rating",
    )


def run(spark: SparkSession, cfg: Config) -> DataFrame:
    """Answer Q4 and write the gold table and the reports."""
    high_rating = float(base.question_setting(cfg, "q4", "high_rating", 8.0))
    low_average = float(base.question_setting(cfg, "q4", "low_average", 6.0))
    min_other = int(base.question_setting(cfg, "q4", "min_other_films", 2))
    min_votes = int(base.question_setting(cfg, "q4", "min_votes", 0))
    max_rows = int(base.question_setting(cfg, "q4", "max_md_rows", 50))

    films = (
        base.with_ratings(
            base.feature_films(base.read_silver(spark, cfg, "title_basics"), cfg),
            base.read_silver(spark, cfg, "title_ratings"),
            min_votes,
        )
        .select("tconst", "primaryTitle", "startYear", "averageRating", "numVotes")
        .persist()
    )
    film_ids = F.broadcast(films.select("tconst"))
    crew = base.read_silver(spark, cfg, "title_crew").join(film_ids, "tconst", "left_semi")
    principals = (
        base.read_silver(spark, cfg, "title_principals")
        .where(F.col("category") == "director")
        .join(film_ids, "tconst", "left_semi")
    )
    filmography = director_credits(crew, principals).join(F.broadcast(films), "tconst")
    selected = one_hit_directors(filmography, high_rating, low_average, min_other)
    names = base.read_silver(spark, cfg, "name_basics").select("nconst", "primaryName")
    result = selected.join(names, "nconst", "left").select(
        "nconst", "primaryName", *[c for c in selected.columns if c != "nconst"]
    )
    path = base.write_gold(result, cfg, NAME)
    result = spark.read.parquet(path).orderBy(
        F.col("hit_rating").desc(), F.col("hit_votes").desc(), "nconst"
    )
    total = result.count()
    LOGGER.info("Q4: %d director(s)", total)

    parameters = {
        **base.feature_film_parameters(cfg),
        "min_votes": min_votes,
        "high_rating": high_rating,
        "low_average": low_average,
        "min_other_films": min_other,
        "director_sources": "title.crew.directors UNION title.principals (category = director)",
        "rated_feature_films": films.count(),
        "directors_found": total,
        "sorted_by": "hit_rating desc, hit_votes desc",
    }
    base.write_report(
        cfg,
        NAME,
        "Q4 - Directors with exactly one highly rated film and low-rated other films",
        parameters,
        [base.table_from(result.drop("hit_tconst"), "Directors", limit=max_rows, total=total)],
        csv_exports={"": result},
    )
    films.unpersist()
    return result


if __name__ == "__main__":
    base.run_job(NAME, run, __doc__)
