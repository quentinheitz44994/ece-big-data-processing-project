"""Data quality report (preparation question 3).

Evaluates every rule of :mod:`imdb_project.preparation.rules` on the standardised
bronze tables and reports, per rule and table, the number of violating rows, the
share of the table they represent and a sample of rows.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from pyspark import StorageLevel
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.logging import get_logger
from imdb_project.common.schemas import CORRUPT_RECORD_COLUMN, TABLES
from imdb_project.common.spark_session import build_spark
from imdb_project.preparation.rules import (
    KeyRule,
    RowRule,
    Rule,
    build_rules,
    quality_settings,
    reference_year,
)
from imdb_project.preparation.standardize import CAST_ERRORS_COLUMN, load_standardized

LOGGER = get_logger(__name__)

REPORT_COLUMNS = ("rule_id", "table", "description", "n_violations", "n_rows", "pct_of_table")
_SAMPLE_TEXT_WIDTH = 60


@dataclass
class RuleResult:
    """Outcome of one rule on one table."""

    rule_id: str
    table: str
    description: str
    n_violations: int
    n_rows: int
    sample_columns: list[str] = field(default_factory=list)
    sample_rows: list[list[Any]] = field(default_factory=list)

    @property
    def pct_of_table(self) -> float:
        """Share of the table rows violating the rule, in percent."""
        return 100.0 * self.n_violations / self.n_rows if self.n_rows else 0.0

    def as_row(self) -> list[Any]:
        """Return the values of :data:`REPORT_COLUMNS`."""
        return [
            self.rule_id,
            self.table,
            self.description,
            self.n_violations,
            self.n_rows,
            self.pct_of_table,
        ]


def match_keys(
    table: DataFrame,
    keys: DataFrame,
    key_columns: Sequence[str],
    broadcast: bool,
    how: str = "left_semi",
) -> DataFrame:
    """Keep (``left_semi``) or drop (``left_anti``) the rows matching a key set.

    Args:
        table: Table to filter.
        keys: Distinct key values (columns ``key_columns``).
        key_columns: Join columns.
        broadcast: Whether the key set is small enough to be broadcast.
        how: ``left_semi`` or ``left_anti``.

    Returns:
        The filtered table.
    """
    right = F.broadcast(keys) if broadcast else keys
    return table.join(right, list(key_columns), how)


def _truncate(value: Any) -> Any:
    if isinstance(value, str) and len(value) > _SAMPLE_TEXT_WIDTH:
        return value[: _SAMPLE_TEXT_WIDTH - 1] + "…"
    return value


def _sample(violations: DataFrame, table: str, size: int) -> tuple[list[str], list[list[Any]]]:
    """Return the first ``size`` violating rows, ordered by primary key.

    Sorting makes the sample deterministic and lets Spark compute it in a single
    parallel pass (top-k per partition) instead of scanning partitions one by one.
    """
    columns = [*TABLES[table].columns, CAST_ERRORS_COLUMN, CORRUPT_RECORD_COLUMN]
    ordered = violations.select(*columns).orderBy(*TABLES[table].primary_key)
    names, rows = io.collect_rows(ordered, limit=size)
    return names, [[_truncate(value) for value in row] for row in rows]


def evaluate_rules(
    tables: Mapping[str, DataFrame], cfg: Config, rules: Sequence[Rule]
) -> list[RuleResult]:
    """Evaluate the rules and collect counts and samples.

    Row rules of a table are counted together in one pass over that table. Key
    rules compute their key set once (persisted on disk) and match it against
    the table.

    Args:
        tables: Standardised tables.
        cfg: Project configuration.
        rules: Rules to evaluate.

    Returns:
        One :class:`RuleResult` per rule, in the order of ``rules``.
    """
    quality = quality_settings(cfg)
    sample_size = int(quality.get("sample_size", 10))
    broadcast_max_keys = int(quality.get("broadcast_max_keys", 2_000_000))
    results: dict[tuple[str, str], RuleResult] = {}
    table_rows: dict[str, int] = {}

    for table in sorted({rule.table for rule in rules}):
        row_rules = [r for r in rules if r.table == table and isinstance(r, RowRule)]
        table_rows[table] = tables[table].count()
        # One scan of the table: the rows violating at least one row rule are
        # kept (with the indexes of the violated rules) and persisted; counts
        # and samples of every rule are then taken from this small set.
        violated = F.array_compact(
            F.array(
                *[F.when(rule.condition(cfg), F.lit(index)) for index, rule in enumerate(row_rules)]
            )
        )
        violating = (
            tables[table]
            .withColumn("__rules", violated)
            .where(F.size("__rules") > 0)
            .persist(StorageLevel.DISK_ONLY)
        )
        try:
            for index, rule in enumerate(row_rules):
                matches = violating.where(F.array_contains("__rules", index))
                result = RuleResult(rule.rule_id, table, rule.description, 0, table_rows[table])
                result.n_violations = matches.count()
                if result.n_violations:
                    result.sample_columns, result.sample_rows = _sample(matches, table, sample_size)
                results[(rule.rule_id, table)] = result
                LOGGER.info("%s %s: %d violation(s)", rule.rule_id, table, result.n_violations)
        finally:
            violating.unpersist()

    for rule in rules:
        if not isinstance(rule, KeyRule):
            continue
        keys = rule.keys(tables, cfg).persist(StorageLevel.DISK_ONLY)
        try:
            n_keys = keys.count()
            result = RuleResult(
                rule.rule_id, rule.table, rule.description, 0, table_rows[rule.table]
            )
            if n_keys:
                violations = match_keys(
                    tables[rule.table], keys, rule.key_columns, n_keys <= broadcast_max_keys
                )
                result.n_violations = violations.count()
                result.sample_columns, result.sample_rows = _sample(
                    violations, rule.table, sample_size
                )
            results[(rule.rule_id, rule.table)] = result
            LOGGER.info(
                "%s %s: %d violation(s), %d key(s)",
                rule.rule_id,
                rule.table,
                result.n_violations,
                n_keys,
            )
        finally:
            keys.unpersist()

    return [results[(rule.rule_id, rule.table)] for rule in rules]


def report_parameters(cfg: Config) -> dict[str, Any]:
    """Return the rule parameters printed at the top of the reports."""
    quality = quality_settings(cfg)
    names = (
        "max_age_years",
        "posthumous_grace_years",
        "posthumous_exempt_categories",
        "archive_pattern",
        "max_future_years",
        "max_runtime_minutes",
        "rating_min",
        "rating_max",
        "episode_parent_types",
        "known_genres",
    )
    parameters: dict[str, Any] = {"reference_year": reference_year(cfg)}
    parameters.update({name: quality.get(name) for name in names})
    parameters["evaluated_on"] = "standardised bronze tables (before cleaning)"
    return parameters


def write_reports(cfg: Config, results: Sequence[RuleResult]) -> None:
    """Write ``quality_report`` (Markdown and CSV) and ``quality_samples``."""
    rows = [result.as_row() for result in results]
    parameters = report_parameters(cfg)
    io.write_markdown(
        io.output_path(cfg, "preparation", "quality_report.md"),
        "Data quality report",
        [io.ReportTable(REPORT_COLUMNS, rows, title="Violations per rule and table")],
        parameters=parameters,
        float_format=".4f",
    )
    io.write_csv(io.output_path(cfg, "preparation", "quality_report.csv"), REPORT_COLUMNS, rows)

    sample_size = int(quality_settings(cfg).get("sample_size", 10))
    samples = [
        io.ReportTable(
            result.sample_columns,
            result.sample_rows,
            title=f"{result.rule_id} - {result.table}",
            note=(
                f"{result.description}. Showing {len(result.sample_rows)} of "
                f"{result.n_violations} violating row(s)."
            ),
        )
        for result in results
        if result.sample_rows
    ]
    io.write_markdown(
        io.output_path(cfg, "preparation", "quality_samples.md"),
        "Data quality report - sample rows",
        samples,
        parameters={"sample_size": sample_size, "text_truncated_at": _SAMPLE_TEXT_WIDTH},
    )


def run(spark: SparkSession, cfg: Config) -> list[RuleResult]:
    """Evaluate every rule on the bronze layer and write the reports."""
    results = evaluate_rules(load_standardized(spark, cfg), cfg, build_rules())
    write_reports(cfg, results)
    return results


def main() -> None:
    """CLI entry point."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    args = parser.parse_args()
    cfg = load_config(args.config)
    spark = build_spark(cfg, "quality_checks")
    try:
        run(spark, cfg)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
