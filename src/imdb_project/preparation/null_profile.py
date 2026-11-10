r"""Missing-value profiling of the bronze layer (preparation questions 1 and 2).

For every column of every table, one pass over the table counts the different
ways a value can be missing:

* ``n_null``: SQL null in bronze, i.e. an empty raw field or a field absent from
  a line that is too short (Spark's CSV reader surfaces both as null);
* ``n_backslash_n``: the IMDb marker ``\N``;
* ``n_empty``: empty string;
* ``n_whitespace``: non-empty string made of whitespace only;
* ``n_empty_array``: ``[]`` in a multi-valued column encoded as text.

The categories are mutually exclusive, ``n_missing_total`` is their sum and
``pct_missing = 100 * n_missing_total / n_total``.
"""

from __future__ import annotations

import argparse
from collections.abc import Collection, Sequence
from typing import Any

from pyspark.sql import Column, DataFrame, SparkSession
from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.logging import get_logger
from imdb_project.common.schemas import TABLES
from imdb_project.common.spark_session import build_spark

LOGGER = get_logger(__name__)

IMDB_NULL_MARKER = "\\N"
#: Whitespace-only values (ASCII whitespace and non-breaking space).
WHITESPACE_ONLY_PATTERN = r"^[\s ]+$"

METRICS = ("n_null", "n_backslash_n", "n_empty", "n_whitespace", "n_empty_array")
PROFILE_COLUMNS = (
    "table",
    "column",
    "n_total",
    *METRICS,
    "n_missing_total",
    "pct_missing",
)


def _count_if(condition: Column) -> Column:
    return F.sum(F.when(condition, 1).otherwise(0))


def missing_value_aggregates(column: str, is_array: bool) -> list[Column]:
    """Build the conditional counts of one column.

    Args:
        column: Column name.
        is_array: Whether the column is a multi-valued column encoded as text.

    Returns:
        One aggregate expression per metric, aliased ``<column>__<metric>``.
    """
    value = F.col(column)
    trimmed = F.trim(value)
    empty_array = _count_if(trimmed == "[]") if is_array else F.lit(0)
    return [
        _count_if(value.isNull()).alias(f"{column}__n_null"),
        _count_if(value == IMDB_NULL_MARKER).alias(f"{column}__n_backslash_n"),
        _count_if(value == "").alias(f"{column}__n_empty"),
        _count_if(value.rlike(WHITESPACE_ONLY_PATTERN)).alias(f"{column}__n_whitespace"),
        empty_array.alias(f"{column}__n_empty_array"),
    ]


def profile_table(
    df: DataFrame,
    table: str,
    columns: Sequence[str],
    array_columns: Collection[str] = (),
) -> list[dict[str, Any]]:
    """Profile the missing values of one table in a single pass.

    Args:
        df: Bronze table (string columns).
        table: Table name reported in the result.
        columns: Columns to profile.
        array_columns: Subset of ``columns`` holding text-encoded arrays.

    Returns:
        One dictionary per column with the keys of :data:`PROFILE_COLUMNS`.
    """
    aggregates = [F.count(F.lit(1)).alias("__n_total")]
    for column in columns:
        aggregates.extend(missing_value_aggregates(column, column in array_columns))
    result = df.agg(*aggregates).first()

    n_total = int(result["__n_total"])
    rows = []
    for column in columns:
        counts = {metric: int(result[f"{column}__{metric}"] or 0) for metric in METRICS}
        missing = sum(counts.values())
        rows.append(
            {
                "table": table,
                "column": column,
                "n_total": n_total,
                **counts,
                "n_missing_total": missing,
                "pct_missing": 100.0 * missing / n_total if n_total else 0.0,
            }
        )
    return rows


def top_missing_columns(profile: Sequence[dict[str, Any]], top_n: int) -> list[dict[str, Any]]:
    """Return the ``top_n`` columns of the whole dataset by ``pct_missing``.

    Ties are broken by the number of missing values, then by table and column
    name, so that the ranking is deterministic.
    """
    ranked = sorted(
        profile,
        key=lambda row: (
            -row["pct_missing"],
            -row["n_missing_total"],
            row["table"],
            row["column"],
        ),
    )
    return ranked[:top_n]


def run(spark: SparkSession, cfg: Config) -> list[dict[str, Any]]:
    """Profile every bronze table and write the two reports.

    Args:
        spark: Active Spark session.
        cfg: Project configuration.

    Returns:
        The full profile, sorted by table and column.
    """
    profile: list[dict[str, Any]] = []
    for name in sorted(TABLES):
        spec = TABLES[name]
        bronze = io.read_parquet(spark, io.layer_path(cfg, "bronze", name))
        rows = profile_table(bronze, name, spec.columns, set(spec.arrays))
        LOGGER.info("profiled %s (%d rows, %d columns)", name, rows[0]["n_total"], len(rows))
        profile.extend(rows)
    profile.sort(key=lambda row: (row["table"], row["column"]))

    top_n = int(cfg.get("preparation.null_profile.top_n", 5))
    columns = list(PROFILE_COLUMNS)
    all_rows = [[row[column] for column in columns] for row in profile]
    definitions = {
        "n_null": "SQL null in bronze (empty raw field, or field absent from a short line)",
        "n_backslash_n": "value equal to the IMDb marker \\N",
        "n_empty": "empty string",
        "n_whitespace": "non-empty value made of whitespace only",
        "n_empty_array": "[] in a multi-valued column encoded as text",
        "n_missing_total": "sum of the five counts (mutually exclusive)",
        "pct_missing": "100 * n_missing_total / n_total",
    }
    io.write_markdown(
        io.output_path(cfg, "preparation", "null_profile.md"),
        "Missing values per column",
        [io.ReportTable(columns, all_rows, title="All tables and columns")],
        parameters=definitions,
        float_format=".4f",
    )
    io.write_csv(io.output_path(cfg, "preparation", "null_profile.csv"), columns, all_rows)

    top = top_missing_columns(profile, top_n)
    top_columns = ["rank", *columns]
    top_rows = [[rank, *[row[column] for column in columns]] for rank, row in enumerate(top, 1)]
    io.write_markdown(
        io.output_path(cfg, "preparation", "top5_null_columns.md"),
        f"Top {top_n} columns by percentage of missing values",
        [io.ReportTable(top_columns, top_rows, title="Whole dataset")],
        parameters={"top_n": top_n, "ranking": "pct_missing desc, n_missing_total desc"},
        float_format=".4f",
    )
    io.write_csv(io.output_path(cfg, "preparation", "top5_null_columns.csv"), top_columns, top_rows)
    return profile


def main() -> None:
    """CLI entry point."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    args = parser.parse_args()
    cfg = load_config(args.config)
    spark = build_spark(cfg, "null_profile")
    try:
        run(spark, cfg)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
