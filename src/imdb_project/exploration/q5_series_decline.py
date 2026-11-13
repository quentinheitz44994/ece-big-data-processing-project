"""Q5 - Series whose best episode came early and whose worst episode came last.

Episodes considered: rated episodes (at least ``min_votes_episode`` votes) with a
known, positive season number, belonging to a title of type ``series_types``.

A series is selected when:

* it has at least ``min_seasons`` seasons with at least
  ``min_episodes_per_season`` such episodes;
* its worst episode (lowest ``averageRating``) is in its last season, i.e. the
  highest positive season number in the source episode table, before vote filtering;
* its best episode (highest ``averageRating``) is in a season numbered
  ``<= first_seasons``.

When several episodes tie for best or worst, ``tie_policy`` decides: ``all``
requires every tied episode to satisfy the condition, ``any`` requires one.
"""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from imdb_project.common.config import Config
from imdb_project.common.logging import get_logger
from imdb_project.exploration import base

LOGGER = get_logger(__name__)
NAME = "q5_series_decline"
TIE_POLICIES = ("all", "any")


def rated_series_episodes(
    episodes: DataFrame,
    titles: DataFrame,
    ratings: DataFrame,
    series_types: list[str],
    min_votes_episode: int,
) -> DataFrame:
    """Return the rated episodes of series with a usable season number.

    Args:
        episodes: Silver ``title_episode``.
        titles: Silver ``title_basics``.
        ratings: Silver ``title_ratings``.
        series_types: Title types accepted for the parent title.
        min_votes_episode: Minimum number of votes of an episode.

    Returns:
        Columns ``parentTconst``, ``tconst``, ``seasonNumber``, ``episodeNumber``,
        ``averageRating``, ``numVotes``, ``last_season`` (before vote filtering).
    """
    series = titles.where(F.col("titleType").isin(series_types)).select(
        F.col("tconst").alias("parentTconst")
    )
    usable = episodes.where(F.col("seasonNumber") > 0).select(
        "tconst", "parentTconst", "seasonNumber", "episodeNumber"
    )
    final_seasons = usable.groupBy("parentTconst").agg(F.max("seasonNumber").alias("last_season"))
    return (
        base.with_ratings(usable, ratings, min_votes_episode)
        .join(F.broadcast(series), "parentTconst", "left_semi")
        .join(final_seasons, "parentTconst")
    )


def series_decline(
    episodes: DataFrame,
    min_seasons: int,
    min_episodes_per_season: int,
    first_seasons: int,
    tie_policy: str,
) -> DataFrame:
    """Select the series matching the "early best, late worst" pattern.

    Args:
        episodes: Output of :func:`rated_series_episodes`.
        min_seasons: Minimum number of eligible seasons.
        min_episodes_per_season: Rated episodes needed for a season to be eligible.
        first_seasons: The best episode must be in a season ``<=`` this number.
        tie_policy: ``all`` or ``any`` (see module docstring).

    Returns:
        One row per selected series with its best and worst episodes.

    Raises:
        ValueError: If ``tie_policy`` is unknown.
    """
    if tie_policy not in TIE_POLICIES:
        raise ValueError(f"tie_policy must be one of {TIE_POLICIES}, got {tie_policy!r}")

    eligible = (
        episodes.groupBy("parentTconst", "seasonNumber")
        .agg(F.count(F.lit(1)).alias("n_episodes"))
        .where(F.col("n_episodes") >= min_episodes_per_season)
        .groupBy("parentTconst")
        .agg(F.count(F.lit(1)).alias("n_eligible_seasons"))
        .where(F.col("n_eligible_seasons") >= min_seasons)
    )
    candidates = episodes.join(eligible, "parentTconst")
    stats = candidates.groupBy("parentTconst").agg(
        F.min("averageRating").alias("worst_rating"),
        F.max("averageRating").alias("best_rating"),
        F.max("last_season" if "last_season" in episodes.columns else "seasonNumber").alias(
            "last_season"
        ),
        F.countDistinct("seasonNumber").alias("n_seasons"),
        F.count(F.lit(1)).alias("n_rated_episodes"),
    )
    marked = candidates.drop("last_season").join(stats, "parentTconst")
    is_worst = F.col("averageRating") == F.col("worst_rating")
    is_best = F.col("averageRating") == F.col("best_rating")
    position = F.struct(
        F.col("seasonNumber").alias("season"),
        F.coalesce(F.col("episodeNumber"), F.lit(0)).alias("episode"),
        F.col("tconst"),
    )
    summary = marked.groupBy(
        "parentTconst",
        "n_eligible_seasons",
        "n_seasons",
        "n_rated_episodes",
        "last_season",
        "best_rating",
        "worst_rating",
    ).agg(
        F.sum(F.when(is_worst, 1).otherwise(0)).alias("n_worst_episodes"),
        F.sum(
            F.when(is_worst & (F.col("seasonNumber") == F.col("last_season")), 1).otherwise(0)
        ).alias("n_worst_in_last_season"),
        F.sum(F.when(is_best, 1).otherwise(0)).alias("n_best_episodes"),
        F.sum(F.when(is_best & (F.col("seasonNumber") <= first_seasons), 1).otherwise(0)).alias(
            "n_best_in_first_seasons"
        ),
        F.min(F.when(is_best, position)).alias("best"),
        F.max(F.when(is_worst, position)).alias("worst"),
    )
    if tie_policy == "all":
        condition = (F.col("n_worst_in_last_season") == F.col("n_worst_episodes")) & (
            F.col("n_best_in_first_seasons") == F.col("n_best_episodes")
        )
    else:
        condition = (F.col("n_worst_in_last_season") > 0) & (F.col("n_best_in_first_seasons") > 0)
    return summary.where(condition & (F.col("best_rating") > F.col("worst_rating"))).select(
        "parentTconst",
        "n_seasons",
        "n_eligible_seasons",
        "n_rated_episodes",
        "last_season",
        "best_rating",
        F.col("best.season").alias("best_season"),
        F.col("best.episode").alias("best_episode"),
        F.col("best.tconst").alias("best_tconst"),
        "n_best_episodes",
        "worst_rating",
        F.col("worst.season").alias("worst_season"),
        F.col("worst.episode").alias("worst_episode"),
        F.col("worst.tconst").alias("worst_tconst"),
        "n_worst_episodes",
    )


def run(spark: SparkSession, cfg: Config) -> DataFrame:
    """Answer Q5 and write the gold table and the reports."""
    series_types = list(base.question_setting(cfg, "q5", "series_types"))
    min_seasons = int(base.question_setting(cfg, "q5", "min_seasons", 3))
    min_episodes = int(base.question_setting(cfg, "q5", "min_episodes_per_season", 10))
    min_votes_episode = int(base.question_setting(cfg, "q5", "min_votes_episode", 50))
    first_seasons = int(base.question_setting(cfg, "q5", "first_seasons", 2))
    tie_policy = str(base.question_setting(cfg, "q5", "tie_policy", "all"))
    max_rows = int(base.question_setting(cfg, "q5", "max_md_rows", 50))

    titles = base.read_silver(spark, cfg, "title_basics")
    episodes = rated_series_episodes(
        base.read_silver(spark, cfg, "title_episode"),
        titles,
        base.read_silver(spark, cfg, "title_ratings"),
        series_types,
        min_votes_episode,
    ).persist()
    selected = series_decline(
        episodes, min_seasons, min_episodes, first_seasons, tie_policy
    ).persist()

    series_info = titles.select(
        F.col("tconst").alias("parentTconst"),
        F.col("primaryTitle").alias("series_title"),
        F.col("startYear").alias("start_year"),
        F.col("endYear").alias("end_year"),
    )
    episode_titles = titles.where(F.col("titleType") == "tvEpisode").select(
        "tconst", "primaryTitle"
    )
    best_titles = episode_titles.select(
        F.col("tconst").alias("best_tconst"), F.col("primaryTitle").alias("best_episode_title")
    )
    worst_titles = episode_titles.select(
        F.col("tconst").alias("worst_tconst"), F.col("primaryTitle").alias("worst_episode_title")
    )
    result = (
        series_info.join(F.broadcast(selected), "parentTconst")
        .join(best_titles, "best_tconst", "left")
        .join(worst_titles, "worst_tconst", "left")
        .select(
            "parentTconst",
            "series_title",
            "start_year",
            "end_year",
            "n_seasons",
            "n_eligible_seasons",
            "n_rated_episodes",
            "best_rating",
            "best_season",
            "best_episode",
            "best_episode_title",
            "n_best_episodes",
            "worst_rating",
            "worst_season",
            "worst_episode",
            "worst_episode_title",
            "n_worst_episodes",
            "last_season",
        )
    )
    path = base.write_gold(result, cfg, NAME)
    result = spark.read.parquet(path).orderBy(F.col("n_rated_episodes").desc(), "parentTconst")
    total = result.count()
    n_candidates = (
        episodes.groupBy("parentTconst", "seasonNumber")
        .count()
        .where(F.col("count") >= min_episodes)
        .groupBy("parentTconst")
        .count()
        .where(F.col("count") >= min_seasons)
        .count()
    )
    LOGGER.info("Q5: %d series selected out of %d candidates", total, n_candidates)

    parameters = {
        "series_types": series_types,
        "min_seasons": min_seasons,
        "min_episodes_per_season": min_episodes,
        "min_votes_episode": min_votes_episode,
        "first_seasons": first_seasons,
        "tie_policy": tie_policy,
        "last_season": "highest positive season number before rating and vote filtering",
        "series_with_enough_eligible_seasons": n_candidates,
        "series_selected": total,
        "sorted_by": "n_rated_episodes desc",
    }
    base.write_report(
        cfg,
        NAME,
        "Q5 - Series with the best episode in the first seasons and the worst in the last",
        parameters,
        [base.table_from(result.drop("parentTconst"), "Series", limit=max_rows, total=total)],
        csv_exports={"": result},
    )
    episodes.unpersist()
    selected.unpersist()
    return result


if __name__ == "__main__":
    base.run_job(NAME, run, __doc__)
