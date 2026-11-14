"""Open question - recurring director-actor collaborations.

Question chosen by the authors: are the films of a repeated director-actor
collaboration rated higher than the first film the pair made together?

Definitions (all thresholds in the ``open_question`` section of the settings):

* Films: feature films as defined by ``exploration.feature_film``, with a known
  ``startYear`` and at least ``open_question.min_votes`` votes.
* Directing credits: ``title.crew.directors`` UNION the ``director`` category of
  ``title.principals`` (same rule as Q4). Acting credits: ``title.principals``
  rows whose category is in ``actor_categories``.
* Collaboration: one (director, actor, film) triple. A director acting in their
  own film is not a collaboration when ``exclude_self_direction`` is set.
* The films of a pair are ordered by (``startYear``, ``tconst``); rank 1 is the
  first collaboration. A pair is recurring when it has at least
  ``min_collaborations`` films.
* ``delta`` of a recurring pair: mean rating of its repeat films (rank >= 2)
  minus the rating of its first film. ``outcome`` is ``higher``/``lower`` when
  ``|delta| > equal_tolerance``, else ``equal``.
* Director baseline: mean rating of the director's other films (without that
  actor) released after the pair's first film, in the same ordering. ``excess``
  is the mean repeat rating minus this baseline (null without such films).

Outputs: gold tables ``data/gold/open_question/collaboration_films`` and
``collaboration_pairs``; ``outputs/open_question/summary.md`` and CSV files.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.common.config import Config
from imdb_project.common.logging import get_logger
from imdb_project.exploration import base
from imdb_project.exploration.q4_one_hit_directors import director_credits

LOGGER = get_logger(__name__)
NAME = "collaborations"
SECTION = "open_question"
PAIR = ["director_nconst", "actor_nconst"]


def setting(cfg: Config, name: str, default: Any = None) -> Any:
    """Return ``open_question.<name>`` (or ``default`` when it is not set)."""
    return cfg.get(f"{SECTION}.{name}", default)


def actor_credits(principals: DataFrame, categories: Sequence[str]) -> DataFrame:
    """Return the distinct (``tconst``, ``nconst``) acting credits.

    Args:
        principals: ``title_principals`` rows.
        categories: Categories counted as acting (``actor``, ``actress``).

    Returns:
        One row per (film, performer).
    """
    return (
        principals.where(F.col("category").isin(list(categories)))
        .select("tconst", "nconst")
        .distinct()
    )


def collaboration_films(
    directing: DataFrame, acting: DataFrame, films: DataFrame, exclude_self: bool = True
) -> DataFrame:
    """Build one row per (director, actor, film) with its rank inside the pair.

    Args:
        directing: Distinct (``tconst``, ``nconst``) directing credits.
        acting: Distinct (``tconst``, ``nconst``) acting credits.
        films: One row per film with ``tconst``, ``primaryTitle``, ``startYear``,
            ``averageRating`` and ``numVotes`` (already filtered).
        exclude_self: Drop the triples where the director is the actor.

    Returns:
        Columns ``director_nconst``, ``actor_nconst``, the film columns,
        ``collab_rank`` (1 = first film of the pair) and ``n_collabs``.
    """
    triples = (
        directing.withColumnRenamed("nconst", "director_nconst")
        .join(acting.withColumnRenamed("nconst", "actor_nconst"), "tconst")
        .join(films, "tconst")
    )
    if exclude_self:
        triples = triples.where(F.col("director_nconst") != F.col("actor_nconst"))
    ordered = Window.partitionBy(*PAIR).orderBy("startYear", "tconst")
    whole_pair = Window.partitionBy(*PAIR)
    return triples.withColumn("collab_rank", F.row_number().over(ordered)).withColumn(
        "n_collabs", F.count(F.lit(1)).over(whole_pair)
    )


def pair_summary(collabs: DataFrame, min_collabs: int, tolerance: float) -> DataFrame:
    """Compare the first film of every recurring pair with its repeat films.

    Args:
        collabs: Output of :func:`collaboration_films`.
        min_collabs: Minimum number of films of a recurring pair (>= 2).
        tolerance: Maximum ``|delta|`` reported as ``equal``.

    Returns:
        One row per recurring pair: first film, number and mean rating of the
        repeat films, ``delta`` and ``outcome``.
    """
    if min_collabs < 2:
        raise ValueError("open_question.min_collaborations must be at least 2")
    is_first = F.col("collab_rank") == 1
    repeat_rating = F.when(~is_first, F.col("averageRating"))
    first = F.struct(
        F.col("tconst").alias("tconst"),
        F.col("primaryTitle").alias("title"),
        F.col("startYear").alias("year"),
        F.col("averageRating").alias("rating"),
    )
    pairs = (
        collabs.where(F.col("n_collabs") >= min_collabs)
        .groupBy(*PAIR)
        .agg(
            F.count(F.lit(1)).alias("n_collabs"),
            F.max(F.when(is_first, first)).alias("first"),
            F.avg(repeat_rating).alias("repeat_avg_rating"),
            F.max(F.col("startYear")).alias("last_year"),
        )
    )
    delta = F.col("repeat_avg_rating") - F.col("first.rating")
    return pairs.select(
        *PAIR,
        "n_collabs",
        F.col("first.tconst").alias("first_tconst"),
        F.col("first.title").alias("first_title"),
        F.col("first.year").alias("first_year"),
        "last_year",
        F.col("first.rating").alias("first_rating"),
        "repeat_avg_rating",
        delta.alias("delta"),
        F.when(delta > tolerance, "higher")
        .when(delta < -tolerance, "lower")
        .otherwise("equal")
        .alias("outcome"),
    )


def director_baseline(pairs: DataFrame, collabs: DataFrame, director_films: DataFrame) -> DataFrame:
    """Add the director's baseline over the same period to every pair.

    Args:
        pairs: Output of :func:`pair_summary`.
        collabs: Output of :func:`collaboration_films`.
        director_films: Distinct (``director_nconst``, ``tconst``, ``startYear``,
            ``averageRating``) rows of every rated film of every director.

    Returns:
        ``pairs`` with ``baseline_films`` (0 when none), ``baseline_avg_rating``
        and ``excess`` (both null without baseline films).
    """
    starts = pairs.select(*PAIR, "first_tconst", "first_year")
    after_first = (F.col("startYear") > F.col("first_year")) | (
        (F.col("startYear") == F.col("first_year")) & (F.col("tconst") > F.col("first_tconst"))
    )
    candidates = starts.join(director_films, "director_nconst").where(after_first)
    with_actor = collabs.select(*PAIR, "tconst")
    baseline = (
        candidates.join(with_actor, [*PAIR, "tconst"], "left_anti")
        .groupBy(*PAIR)
        .agg(
            F.count(F.lit(1)).alias("baseline_films"),
            F.avg("averageRating").alias("baseline_avg_rating"),
        )
    )
    return (
        pairs.join(baseline, PAIR, "left")
        .withColumn("baseline_films", F.coalesce(F.col("baseline_films"), F.lit(0)))
        .withColumn("excess", F.col("repeat_avg_rating") - F.col("baseline_avg_rating"))
    )


def rank_label(rank_cap: int) -> F.Column:
    """Return the collaboration rank as a label, ranks >= ``rank_cap`` grouped."""
    return F.when(F.col("collab_rank") >= rank_cap, F.lit(f"{rank_cap}+")).otherwise(
        F.col("collab_rank").cast("string")
    )


def rank_profile(collabs: DataFrame, pairs: DataFrame, rank_cap: int) -> DataFrame:
    """Mean rating of the recurring pairs' films by collaboration rank.

    Args:
        collabs: Output of :func:`collaboration_films`.
        pairs: Recurring pairs (output of :func:`pair_summary`).
        rank_cap: Ranks from this value on are grouped in one row.

    Returns:
        One row per rank with the number of films, the mean rating and the
        mean difference with the first film of the same pair.
    """
    if rank_cap < 2:
        raise ValueError("open_question.rank_cap must be at least 2")
    recurring = collabs.join(pairs.select(*PAIR, "first_rating"), PAIR)
    sort_key = F.least(F.col("collab_rank"), F.lit(rank_cap))
    return (
        recurring.groupBy(rank_label(rank_cap).alias("collab_rank"), sort_key.alias("sort_key"))
        .agg(
            F.count(F.lit(1)).alias("films"),
            F.avg("averageRating").alias("avg_rating"),
            F.avg(F.col("averageRating") - F.col("first_rating")).alias("avg_diff_vs_first"),
            F.avg("numVotes").alias("avg_votes"),
        )
        .orderBy("sort_key")
        .drop("sort_key")
    )


def bucket_label(bounds: Sequence[int]) -> F.Column:
    """Label ``n_collabs`` with the bucket whose lower bound it reaches.

    ``bounds = [2, 3, 4, 6]`` gives the labels ``2``, ``3``, ``4-5`` and ``6+``.
    """
    ordered = sorted(int(b) for b in bounds)
    label = F.lit(None).cast("string")
    for index, low in enumerate(ordered):
        if index + 1 < len(ordered):
            high = ordered[index + 1] - 1
            text = str(low) if high == low else f"{low}-{high}"
        else:
            text = f"{low}+"
        label = F.when(F.col("n_collabs") >= low, F.lit(text)).otherwise(label)
    return label


def bucket_summary(pairs: DataFrame, bounds: Sequence[int]) -> DataFrame:
    """Aggregate the recurring pairs by number of collaborations."""
    return (
        pairs.groupBy(bucket_label(bounds).alias("collaborations"))
        .agg(
            F.count(F.lit(1)).alias("pairs"),
            F.min("n_collabs").alias("sort_key"),
            F.avg("first_rating").alias("avg_first_rating"),
            F.avg("repeat_avg_rating").alias("avg_repeat_rating"),
            F.avg("delta").alias("avg_delta"),
            F.avg(F.when(F.col("outcome") == "higher", 1.0).otherwise(0.0)).alias("share_higher"),
            F.avg("excess").alias("avg_excess_vs_director"),
        )
        .orderBy("sort_key")
        .drop("sort_key")
    )


def overall_metrics(collabs: DataFrame, pairs: DataFrame, min_collabs: int) -> list[list[Any]]:
    """Return the headline metrics as ``[metric, value]`` rows.

    Args:
        collabs: Output of :func:`collaboration_films`.
        pairs: Output of :func:`director_baseline`.
        min_collabs: Minimum number of films of a recurring pair.

    Returns:
        Counts, distribution of ``delta`` (mean, median, standard deviation,
        paired t statistic), outcome shares, comparison with the director
        baseline and with the pairs that never worked together again.
    """
    all_pairs = collabs.select(*PAIR, "n_collabs").distinct()
    counts = all_pairs.agg(
        F.count(F.lit(1)).alias("pairs"),
        F.sum(F.when(F.col("n_collabs") >= min_collabs, 1).otherwise(0)).alias("recurring"),
    ).first()
    stats = pairs.agg(
        F.avg("delta").alias("mean"),
        F.percentile_approx("delta", 0.5, 10_000).alias("median"),
        F.stddev_samp("delta").alias("sd"),
        F.avg(F.when(F.col("outcome") == "higher", 1.0).otherwise(0.0)).alias("higher"),
        F.avg(F.when(F.col("outcome") == "equal", 1.0).otherwise(0.0)).alias("equal"),
        F.avg(F.when(F.col("outcome") == "lower", 1.0).otherwise(0.0)).alias("lower"),
        F.count("excess").alias("with_baseline"),
        F.avg("excess").alias("mean_excess"),
        F.avg(F.when(F.col("excess") > 0, 1.0).when(F.col("excess").isNotNull(), 0.0)).alias(
            "excess_positive"
        ),
        F.avg("first_rating").alias("first_rating"),
        F.avg("repeat_avg_rating").alias("repeat_rating"),
    ).first()
    one_off = (
        collabs.where(F.col("n_collabs") == 1).agg(F.avg("averageRating").alias("rating")).first()
    )
    recurring = counts["recurring"] or 0
    t_stat = None
    if recurring > 1 and stats["sd"]:
        t_stat = stats["mean"] / (stats["sd"] / math.sqrt(recurring))
    return [
        ["director-actor pairs (at least one film)", counts["pairs"] or 0],
        [f"recurring pairs (>= {min_collabs} films)", recurring],
        [
            "share of pairs that are recurring",
            recurring / counts["pairs"] if counts["pairs"] else None,
        ],
        ["mean rating, films of one-off pairs", one_off["rating"]],
        ["mean rating, first film of recurring pairs", stats["first_rating"]],
        ["mean of pair repeat-film mean ratings", stats["repeat_rating"]],
        ["mean delta (repeat - first)", stats["mean"]],
        ["median delta (approx.)", stats["median"]],
        ["standard deviation of delta", stats["sd"]],
        ["paired t statistic of delta", t_stat],
        ["share of pairs: repeats higher", stats["higher"]],
        ["share of pairs: repeats equal", stats["equal"]],
        ["share of pairs: repeats lower", stats["lower"]],
        ["recurring pairs with a director baseline", stats["with_baseline"]],
        ["mean excess vs director baseline", stats["mean_excess"]],
        ["share of pairs with positive excess", stats["excess_positive"]],
    ]


def _export(cfg: Config, filename: str, df: DataFrame, max_rows: int) -> list[Any]:
    total = df.count()
    columns, rows = io.collect_rows(df, max_rows)
    io.write_csv(io.output_path(cfg, SECTION, filename), columns, rows)
    return [filename, total, len(rows), len(rows) < total]


def run(spark: SparkSession, cfg: Config) -> DataFrame:
    """Answer the open question and write the gold tables and the reports."""
    min_votes = int(setting(cfg, "min_votes", 0))
    categories = list(setting(cfg, "actor_categories", ["actor", "actress"]))
    exclude_self = bool(setting(cfg, "exclude_self_direction", True))
    min_collabs = int(setting(cfg, "min_collaborations", 2))
    tolerance = float(setting(cfg, "equal_tolerance", 0.0))
    rank_cap = int(setting(cfg, "rank_cap", 5))
    bounds = list(setting(cfg, "collaboration_buckets", [2, 3, 4, 6]))
    max_md_rows = int(setting(cfg, "max_md_rows", 30))
    max_csv_rows = int(setting(cfg, "max_csv_rows", 50_000))
    if max_csv_rows < 1:
        raise ValueError("open_question.max_csv_rows must be positive")

    films = (
        base.with_ratings(
            base.feature_films(base.read_silver(spark, cfg, "title_basics"), cfg),
            base.read_silver(spark, cfg, "title_ratings"),
            min_votes,
        )
        .where(F.col("startYear").isNotNull())
        .select("tconst", "primaryTitle", "startYear", "averageRating", "numVotes")
        .persist()
    )
    film_ids = F.broadcast(films.select("tconst"))
    crew = base.read_silver(spark, cfg, "title_crew").join(film_ids, "tconst", "left_semi")
    principals = (
        base.read_silver(spark, cfg, "title_principals")
        .where(F.col("category").isin(["director", *categories]))
        .join(film_ids, "tconst", "left_semi")
    )
    directing = director_credits(crew, principals).persist()
    acting = actor_credits(principals, categories)

    collabs_path = io.layer_path(cfg, "gold", SECTION, "collaboration_films")
    io.write_parquet(collaboration_films(directing, acting, films, exclude_self), collabs_path)
    collabs = spark.read.parquet(collabs_path)

    director_films = (
        directing.withColumnRenamed("nconst", "director_nconst")
        .join(films.select("tconst", "startYear", "averageRating"), "tconst")
        .distinct()
    )
    pairs = director_baseline(
        pair_summary(collabs, min_collabs, tolerance), collabs, director_films
    )
    names = base.read_silver(spark, cfg, "name_basics").select("nconst", "primaryName")
    pairs = (
        pairs.join(
            names.withColumnRenamed("nconst", "director_nconst").withColumnRenamed(
                "primaryName", "director"
            ),
            "director_nconst",
            "left",
        )
        .join(
            names.withColumnRenamed("nconst", "actor_nconst").withColumnRenamed(
                "primaryName", "actor"
            ),
            "actor_nconst",
            "left",
        )
        .select("director", "actor", *pairs.columns)
    )
    pairs_path = io.layer_path(cfg, "gold", SECTION, "collaboration_pairs")
    io.write_parquet(pairs, pairs_path)
    pairs = spark.read.parquet(pairs_path).orderBy(
        F.col("n_collabs").desc(), F.col("delta").desc(), *PAIR
    )
    total_pairs = pairs.count()
    LOGGER.info("open question: %d recurring director-actor pair(s)", total_pairs)

    overall = overall_metrics(collabs, pairs, min_collabs)
    ranks = rank_profile(collabs, pairs, rank_cap)
    buckets = bucket_summary(pairs, bounds)
    top_columns = [
        "director", "actor", "n_collabs", "first_title", "first_year", "last_year",
        "first_rating", "repeat_avg_rating", "delta", "baseline_avg_rating", "excess",
    ]  # fmt: skip
    top = pairs.select(*top_columns)

    exports = [
        _export(cfg, f"{NAME}_pairs.csv", pairs, max_csv_rows),
        _export(cfg, f"{NAME}_by_rank.csv", ranks, max_csv_rows),
        _export(cfg, f"{NAME}_by_count.csv", buckets, max_csv_rows),
    ]
    io.write_csv(io.output_path(cfg, SECTION, f"{NAME}_overall.csv"), ["metric", "value"], overall)
    parameters = {
        **base.feature_film_parameters(cfg),
        "min_votes": min_votes,
        "actor_categories": categories,
        "director_sources": "title.crew.directors UNION title.principals (category = director)",
        "exclude_self_direction": exclude_self,
        "min_collaborations": min_collabs,
        "equal_tolerance": tolerance,
        "pair_ordering": "startYear asc, tconst asc",
        "rated_feature_films": films.count(),
        "collaboration_rows": collabs.count(),
        "recurring_pairs": total_pairs,
    }
    tables = [
        io.ReportTable(["metric", "value"], overall, title="Overall", float_format=".3f"),
        base.table_from(ranks, "Recurring pairs by collaboration rank"),
        base.table_from(buckets, "Recurring pairs by number of collaborations"),
        base.table_from(top, "Most frequent recurring pairs", limit=max_md_rows, total=total_pairs),
        io.ReportTable(
            ["file", "total_rows", "exported_rows", "truncated"], exports, title="CSV exports"
        ),
    ]
    io.write_markdown(
        io.output_path(cfg, SECTION, "summary.md"),
        "Open question - Recurring director-actor collaborations",
        tables,
        parameters,
    )
    directing.unpersist()
    films.unpersist()
    return pairs


if __name__ == "__main__":
    base.run_job("open_question", run, __doc__)
