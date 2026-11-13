"""Q8 - "Multi-talented" professionals and their results when combining roles.

Roles are normalised to ``actor``, ``director`` and ``writer`` from
``title.principals.category`` (``role_categories``) and from ``title.crew``
(``directors``, ``writers``), on rated feature films.

* A person is *multi-talented* when they hold at least two distinct roles over
  their career, with at least ``min_titles_per_role`` films in each.
* For each of them, the films where they combine two or more roles are compared
  with the films where they hold a single role (paired comparison per person):
  mean rating on each side, difference, share of people doing better when
  combining roles. The comparison is also broken down by role combination.
"""

from __future__ import annotations

from collections.abc import Mapping

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from imdb_project.common.config import Config
from imdb_project.common.logging import get_logger
from imdb_project.exploration import base

LOGGER = get_logger(__name__)
NAME = "q8_multi_talented"
ANY_COMBINATION = "any combination"


def person_title_roles(
    principals: DataFrame, crew: DataFrame, role_categories: Mapping[str, str]
) -> DataFrame:
    """Return the distinct (person, film, role) triples from both sources.

    Args:
        principals: ``title_principals`` rows.
        crew: ``title_crew`` rows.
        role_categories: Mapping of principal category to normalised role.

    Returns:
        Columns ``nconst``, ``tconst``, ``role``.
    """
    mapping = F.create_map(*[F.lit(part) for item in role_categories.items() for part in item])
    from_principals = principals.select(
        "nconst", "tconst", F.try_element_at(mapping, F.col("category")).alias("role")
    ).where(F.col("role").isNotNull())
    directors = crew.select(
        F.explode("directors").alias("nconst"), "tconst", F.lit("director").alias("role")
    )
    writers = crew.select(
        F.explode("writers").alias("nconst"), "tconst", F.lit("writer").alias("role")
    )
    return from_principals.unionByName(directors).unionByName(writers).distinct()


def multi_talented(roles: DataFrame, min_titles_per_role: int) -> DataFrame:
    """Return the people with at least two sufficiently practised roles.

    Args:
        roles: Output of :func:`person_title_roles` (rated feature films only).
        min_titles_per_role: Films needed in a role for it to count.

    Returns:
        Columns ``nconst``, ``career_roles`` (sorted, ``+``-joined), ``n_career_roles``.
    """
    practised = (
        roles.groupBy("nconst", "role")
        .agg(F.countDistinct("tconst").alias("n_titles"))
        .where(F.col("n_titles") >= min_titles_per_role)
    )
    return (
        practised.groupBy("nconst")
        .agg(F.sort_array(F.collect_set("role")).alias("roles"))
        .where(F.size("roles") >= 2)
        .select(
            "nconst",
            F.array_join("roles", "+").alias("career_roles"),
            F.size("roles").alias("n_career_roles"),
        )
    )


def title_combinations(roles: DataFrame, films: DataFrame) -> DataFrame:
    """Return, per (person, film), the combination of roles held on that film.

    Args:
        roles: Output of :func:`person_title_roles`.
        films: Rated films (``tconst``, ``averageRating``, ``numVotes``).

    Returns:
        Columns ``nconst``, ``tconst``, ``combination`` (``actor+director``...),
        ``n_roles``, ``averageRating``, ``numVotes``.
    """
    per_title = roles.groupBy("nconst", "tconst").agg(
        F.sort_array(F.collect_set("role")).alias("roles")
    )
    return per_title.select(
        "nconst",
        "tconst",
        F.array_join("roles", "+").alias("combination"),
        F.size("roles").alias("n_roles"),
    ).join(films.select("tconst", "averageRating", "numVotes"), "tconst")


def person_comparison(combinations: DataFrame, talents: DataFrame) -> DataFrame:
    """Compare, per multi-talented person, multi-role films with single-role films.

    Returns:
        One row per person and per multi-role combination they practised, plus one
        row per person for :data:`ANY_COMBINATION`. Columns: ``nconst``,
        ``career_roles``, ``combination``, ``n_multi``, ``avg_multi``,
        ``n_single``, ``avg_single``, ``diff`` (``avg_multi - avg_single``).
        People without films on both sides are dropped.
    """
    scoped = combinations.join(talents, "nconst")
    single = (
        scoped.where(F.col("n_roles") == 1)
        .groupBy("nconst")
        .agg(F.count(F.lit(1)).alias("n_single"), F.avg("averageRating").alias("avg_single"))
    )
    multi = scoped.where(F.col("n_roles") >= 2)
    per_combination = multi.groupBy("nconst", "career_roles", "combination").agg(
        F.count(F.lit(1)).alias("n_multi"), F.avg("averageRating").alias("avg_multi")
    )
    overall = (
        multi.groupBy("nconst", "career_roles")
        .agg(F.count(F.lit(1)).alias("n_multi"), F.avg("averageRating").alias("avg_multi"))
        .withColumn("combination", F.lit(ANY_COMBINATION))
    )
    return (
        per_combination.unionByName(overall)
        .join(single, "nconst")
        .withColumn("diff", F.col("avg_multi") - F.col("avg_single"))
    )


def summarize(comparison: DataFrame) -> DataFrame:
    """Aggregate the paired comparison per role combination.

    Returns:
        One row per combination: number of people, mean of the per-person means on
        each side, mean and median difference, share of people rated higher when
        combining roles.
    """
    return (
        comparison.groupBy("combination")
        .agg(
            F.count(F.lit(1)).alias("people"),
            F.sum("n_multi").alias("multi_role_films"),
            F.avg("avg_multi").alias("mean_rating_multi_role"),
            F.avg("avg_single").alias("mean_rating_single_role"),
            F.avg("diff").alias("mean_diff"),
            F.percentile("diff", 0.5).alias("median_diff"),
            F.stddev_samp("diff").alias("std_diff"),
            (100.0 * F.avg(F.when(F.col("diff") > 0, 1.0).otherwise(0.0))).alias(
                "pct_people_better_multi_role"
            ),
        )
        .orderBy(F.when(F.col("combination") == ANY_COMBINATION, 0).otherwise(1), "combination")
    )


def run(spark: SparkSession, cfg: Config) -> DataFrame:
    """Answer Q8 and write the gold table and the reports."""
    role_categories = dict(base.question_setting(cfg, "q8", "role_categories"))
    min_titles = int(base.question_setting(cfg, "q8", "min_titles_per_role", 3))
    min_votes = int(base.question_setting(cfg, "q8", "min_votes", 0))
    max_rows = int(base.question_setting(cfg, "q8", "max_md_rows", 30))

    films = (
        base.with_ratings(
            base.feature_films(base.read_silver(spark, cfg, "title_basics"), cfg),
            base.read_silver(spark, cfg, "title_ratings"),
            min_votes,
        )
        .select("tconst", "averageRating", "numVotes")
        .persist()
    )
    film_ids = F.broadcast(films.select("tconst"))
    principals = (
        base.read_silver(spark, cfg, "title_principals")
        .where(F.col("category").isin(list(role_categories)))
        .join(film_ids, "tconst", "left_semi")
    )
    crew = base.read_silver(spark, cfg, "title_crew").join(film_ids, "tconst", "left_semi")
    roles = person_title_roles(principals, crew, role_categories).persist()
    talents = multi_talented(roles, min_titles).persist()
    combinations = title_combinations(roles, F.broadcast(films))
    comparison = person_comparison(combinations, talents)

    names = base.read_silver(spark, cfg, "name_basics").select("nconst", "primaryName")
    result = comparison.join(names, "nconst", "left").select(
        "nconst",
        "primaryName",
        "career_roles",
        "combination",
        "n_multi",
        "avg_multi",
        "n_single",
        "avg_single",
        "diff",
    )
    path = base.write_gold(result, cfg, NAME)
    result = spark.read.parquet(path)

    summary = summarize(result)
    career_distribution = (
        talents.groupBy("career_roles")
        .agg(F.count(F.lit(1)).alias("people"))
        .orderBy("career_roles")
    )
    overall = result.where(F.col("combination") == ANY_COMBINATION)
    top = overall.orderBy(F.col("n_multi").desc(), "nconst")
    n_talents = talents.count()
    n_compared = overall.count()
    LOGGER.info("Q8: %d multi-talented people, %d with both kinds of films", n_talents, n_compared)

    parameters = {
        **base.feature_film_parameters(cfg),
        "min_votes": min_votes,
        "role_categories": [f"{key}->{value}" for key, value in role_categories.items()],
        "crew_roles": "title.crew.directors -> director, title.crew.writers -> writer",
        "min_titles_per_role": min_titles,
        "multi_talented": "at least 2 roles with min_titles_per_role films each",
        "multi_role_film": "film on which the person holds 2 or more roles",
        "diff": "per person: mean rating of multi-role films - mean rating of single-role films",
        "multi_talented_people": n_talents,
        "people_with_multi_and_single_role_films": n_compared,
    }
    base.write_report(
        cfg,
        NAME,
        "Q8 - Multi-talented professionals: multi-role films versus single-role films",
        parameters,
        [
            base.table_from(career_distribution, "Multi-talented people per set of career roles"),
            base.table_from(summary, "Paired comparison per role combination on the same film"),
            base.table_from(
                top.drop("nconst", "combination"),
                "People with the most multi-role films",
                limit=max_rows,
                total=n_compared,
            ),
        ],
        csv_exports={
            "summary": summary,
            "career_roles": career_distribution,
            "": result.orderBy(F.col("n_multi").desc(), "nconst", "combination"),
        },
    )
    for frame in (films, roles, talents):
        frame.unpersist()
    return result


if __name__ == "__main__":
    base.run_job(NAME, run, __doc__)
