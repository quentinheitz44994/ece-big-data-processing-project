"""Conventions shared by the exploration questions.

* Feature film: ``titleType`` in ``exploration.feature_film.title_types`` with
  ``runtimeMinutes >= min_runtime_minutes``; adult titles excluded unless
  ``include_adult`` is set.
* Any rating analysis only uses titles with at least ``min_votes`` votes.
* Genres are exploded: a film counts once in each of its genres.

Every question writes its complete result to ``data/gold/exploration/<name>/``
and generated tables (Markdown, CSV) to ``outputs/exploration/``.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.spark_session import build_spark

SECTION = "exploration"


def read_silver(spark: SparkSession, cfg: Config, table: str) -> DataFrame:
    """Read one silver table."""
    return io.read_parquet(spark, io.layer_path(cfg, "silver", table))


def question_setting(cfg: Config, question: str, name: str, default: Any = None) -> Any:
    """Return a question parameter, falling back to the section-wide value.

    Args:
        cfg: Project configuration.
        question: Question key (``q1`` ... ``q8``).
        name: Parameter name.
        default: Value used when neither level defines the parameter.

    Returns:
        ``exploration.<question>.<name>`` if set, else ``exploration.<name>``.
    """
    value = cfg.get(f"{SECTION}.{question}.{name}")
    if value is None:
        value = cfg.get(f"{SECTION}.{name}", default)
    return value


def feature_films(titles: DataFrame, cfg: Config) -> DataFrame:
    """Keep the feature-length films of ``title_basics``.

    Args:
        titles: Silver ``title_basics``.
        cfg: Project configuration (``exploration.feature_film``).

    Returns:
        The rows matching the feature film definition.
    """
    definition = cfg.require(f"{SECTION}.feature_film")
    condition = F.col("titleType").isin(list(definition.title_types)) & (
        F.col("runtimeMinutes") >= int(definition.min_runtime_minutes)
    )
    if not definition.get("include_adult", False):
        condition = condition & ~F.coalesce(F.col("isAdult"), F.lit(False))
    return titles.where(condition)


def with_ratings(titles: DataFrame, ratings: DataFrame, min_votes: int | None = None) -> DataFrame:
    """Join titles with their rating, optionally keeping well-voted titles only.

    Args:
        titles: Any DataFrame with a ``tconst`` column.
        ratings: Silver ``title_ratings``.
        min_votes: Minimum ``numVotes`` (no filter when ``None`` or 0).

    Returns:
        ``titles`` with ``averageRating`` and ``numVotes`` (rated titles only).
    """
    rated = ratings.select("tconst", "averageRating", "numVotes").where(
        F.col("averageRating").isNotNull() & F.col("numVotes").isNotNull()
    )
    if min_votes:
        rated = rated.where(F.col("numVotes") >= int(min_votes))
    return titles.join(rated, "tconst")


def explode_genres(titles: DataFrame) -> DataFrame:
    """Return one row per (title, genre); titles without genre are dropped."""
    return titles.withColumn("genre", F.explode("genres"))


def feature_film_parameters(cfg: Config) -> dict[str, Any]:
    """Return the feature film definition for the header of a report."""
    definition = cfg.require(f"{SECTION}.feature_film")
    return {
        "feature_film.title_types": list(definition.title_types),
        "feature_film.min_runtime_minutes": definition.min_runtime_minutes,
        "feature_film.include_adult": bool(definition.get("include_adult", False)),
    }


def write_gold(df: DataFrame, cfg: Config, name: str) -> str:
    """Write the complete result of a question to the gold layer and return its path."""
    path = io.layer_path(cfg, "gold", SECTION, name)
    io.write_parquet(df, path)
    return path


def table_from(
    df: DataFrame,
    title: str,
    limit: int | None = None,
    total: int | None = None,
    float_format: str | None = None,
) -> io.ReportTable:
    """Collect a (small or limited) DataFrame into a report table.

    Args:
        df: Result to display, already sorted.
        title: Heading of the table.
        limit: Maximum number of rows displayed.
        total: Total number of rows of the complete result, for the caption.
        float_format: Optional float format of the table.

    Returns:
        The report table, with a "Showing n of total rows" caption when truncated.
    """
    columns, rows = io.collect_rows(df, limit)
    note = None
    if total is not None and total > len(rows):
        note = f"Showing {len(rows)} of {total} rows"
    return io.ReportTable(columns, rows, title=title, note=note, float_format=float_format)


def write_report(
    cfg: Config,
    name: str,
    title: str,
    parameters: Mapping[str, Any],
    tables: Sequence[io.ReportTable],
    csv_exports: Mapping[str, DataFrame] | None = None,
) -> None:
    """Write the Markdown report of a question and its CSV exports.

    Args:
        cfg: Project configuration.
        name: Base name of the files (``q1_runtime_outliers``...).
        title: Title of the Markdown report.
        parameters: Parameters used, printed at the top of the report.
        tables: Tables of the Markdown report.
        csv_exports: Sorted DataFrames exported to ``<name>_<key>.csv`` (or
            ``<name>.csv`` for the key ``""``), capped at
            ``exploration.max_csv_rows`` rows.
    """
    max_rows = int(cfg.get(f"{SECTION}.max_csv_rows", 50_000))
    if max_rows < 1:
        raise ValueError("exploration.max_csv_rows must be positive")
    exports = []
    for key, df in (csv_exports or {}).items():
        total = df.count()
        columns, rows = io.collect_rows(df, max_rows)
        suffix = f"_{key}" if key else ""
        filename = f"{name}{suffix}.csv"
        io.write_csv(io.output_path(cfg, SECTION, filename), columns, rows)
        exports.append(
            [filename, total, len(rows), len(rows) < total, io.layer_path(cfg, "gold", SECTION)]
        )
    report_tables = list(tables)
    if exports:
        columns = ["file", "total_rows", "exported_rows", "truncated", "gold_directory"]
        report_tables.append(io.ReportTable(columns, exports, title="CSV exports"))
        io.write_csv(io.output_path(cfg, SECTION, f"{name}_exports.csv"), columns, exports)
    io.write_markdown(io.output_path(cfg, SECTION, f"{name}.md"), title, report_tables, parameters)


def run_job(name: str, run: Callable[[SparkSession, Config], Any], description: str) -> None:
    """Standard CLI wrapper of a question module (``--config`` option)."""
    parser = add_config_argument(argparse.ArgumentParser(description=description))
    args = parser.parse_args()
    cfg = load_config(args.config)
    spark = build_spark(cfg, name)
    try:
        run(spark, cfg)
    finally:
        spark.stop()
