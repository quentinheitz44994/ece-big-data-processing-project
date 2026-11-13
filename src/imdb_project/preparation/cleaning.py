"""Silver layer (preparation question 4): standardise, flag, quarantine, correct.

For each table:

1. the bronze table is standardised (missing markers to null, types, arrays);
2. every quality rule is evaluated and the ids of the violated rules are stored
   in ``dq_flags`` (flagging rather than deleting);
3. structurally invalid rows (malformed line, duplicated primary key, orphan
   foreign key of a fact table) go to ``data/quarantine/<table>/`` with a
   ``dq_reason`` and are excluded from silver. When all the rows sharing a primary
   key are identical, one copy is kept in silver;
4. deterministic corrections replace impossible values by null. No value is ever
   imputed.

Parent tables are cleaned first, so that the foreign keys of the other tables are
checked against the rows actually present in silver.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from pyspark.sql import Column, DataFrame, SparkSession, Window
from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.logging import get_logger
from imdb_project.common.schemas import CORRUPT_RECORD_COLUMN, DQ_FLAGS_COLUMN, TABLES, TableSpec
from imdb_project.common.spark_session import build_spark
from imdb_project.preparation.rules import (
    KeyRule,
    RowRule,
    Rule,
    build_rules,
    quality_settings,
    reference_year,
    rules_for_table,
)
from imdb_project.preparation.standardize import load_standardized

LOGGER = get_logger(__name__)

DQ_REASON_COLUMN = "dq_reason"
DUPLICATE_RULE_ID = "DQ10"
REASON_EXACT_DUPLICATE = "DQ10:exact_duplicate"
REASON_CONFLICTING_KEY = "DQ10:conflicting_primary_key"
#: Parents first: their silver version is the reference of the foreign key rules.
CLEANING_ORDER = (
    "title_basics",
    "name_basics",
    "title_ratings",
    "title_crew",
    "title_episode",
    "title_akas",
    "title_principals",
)

_DUP_REASON = "__dup_reason"


@dataclass(frozen=True)
class Correction:
    """Deterministic correction: an impossible value is replaced by null.

    Attributes:
        table: Table the correction applies to.
        column: Corrected column.
        description: Short description used in the summary report.
        invalid: Builds the condition identifying the values to set to null.
    """

    table: str
    column: str
    description: str
    invalid: Callable[[Config], Column]


def build_corrections() -> list[Correction]:
    """Return the deterministic corrections applied when writing silver."""
    return [
        Correction(
            "title_basics",
            "runtimeMinutes",
            "runtimeMinutes <= 0 set to null",
            lambda cfg: F.col("runtimeMinutes") <= 0,
        ),
        Correction(
            "title_ratings",
            "averageRating",
            "averageRating outside [rating_min, rating_max] set to null",
            lambda cfg: (
                (F.col("averageRating") < float(quality_settings(cfg).rating_min))
                | (F.col("averageRating") > float(quality_settings(cfg).rating_max))
            ),
        ),
        Correction(
            "title_ratings",
            "numVotes",
            "numVotes <= 0 set to null",
            lambda cfg: F.col("numVotes") <= 0,
        ),
        Correction(
            "title_episode",
            "seasonNumber",
            "negative seasonNumber set to null",
            lambda cfg: F.col("seasonNumber") < 0,
        ),
        Correction(
            "title_episode",
            "episodeNumber",
            "negative episodeNumber set to null",
            lambda cfg: F.col("episodeNumber") < 0,
        ),
        Correction(
            "name_basics",
            "birthYear",
            "birthYear after the reference year set to null",
            lambda cfg: F.col("birthYear") > reference_year(cfg),
        ),
        Correction(
            "name_basics",
            "deathYear",
            "deathYear after the reference year set to null",
            lambda cfg: F.col("deathYear") > reference_year(cfg),
        ),
    ]


def add_flags(
    df: DataFrame,
    row_rules: Sequence[RowRule],
    key_sets: Sequence[tuple[KeyRule, DataFrame, bool]],
    cfg: Config,
) -> DataFrame:
    """Add the ``dq_flags`` column listing the rules violated by each row.

    Args:
        df: Standardised table.
        row_rules: Row-level rules of the table.
        key_sets: ``(rule, violating keys, broadcast?)`` for the key rules of the
            table that have at least one violation.
        cfg: Project configuration.

    Returns:
        ``df`` with an ``array<string>`` column ``dq_flags`` (empty when clean).
    """
    flagged = df
    flags = [F.when(rule.condition(cfg), F.lit(rule.rule_id)) for rule in row_rules]
    markers = []
    for index, (rule, keys, broadcast) in enumerate(key_sets):
        marker = f"__key_{index}"
        marked = keys.select(*rule.key_columns).withColumn(marker, F.lit(True))
        flagged = flagged.join(
            F.broadcast(marked) if broadcast else marked, list(rule.key_columns), "left"
        )
        flags.append(F.when(F.col(marker), F.lit(rule.rule_id)))
        markers.append(marker)
    all_flags = F.array(*flags) if flags else F.array().cast("array<string>")
    return flagged.withColumn(DQ_FLAGS_COLUMN, F.array_compact(all_flags)).drop(*markers)


def resolve_duplicates(duplicates: DataFrame, spec: TableSpec) -> DataFrame:
    """Decide what happens to the rows sharing a primary key.

    Args:
        duplicates: Rows whose primary key is carried by several rows.
        spec: Specification of the table.

    Returns:
        ``duplicates`` with a ``__dup_reason`` column: null for the single copy
        kept when all the rows of a key are identical, otherwise the reason why
        the row is quarantined.
    """
    content = F.sha2(F.to_json(F.struct(*[F.col(column) for column in spec.columns])), 256)
    by_key = Window.partitionBy(*spec.primary_key)
    ranked = (
        duplicates.withColumn("__content", content)
        .withColumn("__variants", F.size(F.collect_set("__content").over(by_key)))
        .withColumn("__rank", F.row_number().over(by_key.orderBy("__content")))
    )
    reason = F.when(F.col("__variants") > 1, F.lit(REASON_CONFLICTING_KEY)).when(
        F.col("__rank") > 1, F.lit(REASON_EXACT_DUPLICATE)
    )
    return ranked.withColumn(_DUP_REASON, reason).drop("__content", "__variants", "__rank")


def add_quarantine_reason(df: DataFrame, quarantine_rule_ids: Sequence[str]) -> DataFrame:
    """Add ``dq_reason``: null for silver rows, the ``;``-joined reasons otherwise.

    Args:
        df: Flagged table with the ``__dup_reason`` column.
        quarantine_rule_ids: Ids of the quarantine rules of the table (the
            duplicate rule is handled through ``__dup_reason``).

    Returns:
        ``df`` with ``dq_reason`` and without ``__dup_reason``.
    """
    structural = [rule_id for rule_id in quarantine_rule_ids if rule_id != DUPLICATE_RULE_ID]
    from_flags = F.filter(F.col(DQ_FLAGS_COLUMN), lambda flag: flag.isin(structural))
    reasons = F.array_compact(F.concat(from_flags, F.array(F.col(_DUP_REASON))))
    reason = F.when(F.size(reasons) > 0, F.array_join(reasons, ";"))
    return df.withColumn(DQ_REASON_COLUMN, reason).drop(_DUP_REASON)


def apply_corrections(df: DataFrame, corrections: Sequence[Correction], cfg: Config) -> DataFrame:
    """Replace the invalid values targeted by ``corrections`` by null."""
    corrected = df
    for correction in corrections:
        column = F.col(correction.column)
        corrected = corrected.withColumn(
            correction.column, F.when(correction.invalid(cfg), None).otherwise(column)
        )
    return corrected


def clean_table(
    tables: Mapping[str, DataFrame],
    cfg: Config,
    spec: TableSpec,
    rules: Sequence[Rule],
    corrections: Sequence[Correction],
) -> tuple[DataFrame, DataFrame, dict[str, DataFrame]]:
    """Build the silver and quarantine DataFrames of one table.

    Args:
        tables: Standardised tables (parents already replaced by their silver version).
        cfg: Project configuration.
        spec: Specification of the table to clean.
        rules: Every quality rule (filtered on the table here).
        corrections: Every correction (filtered on the table here).

    Returns:
        ``(silver, quarantine, persisted key sets)``. The caller unpersists the
        key sets once both DataFrames have been written.
    """
    table_rules = rules_for_table(rules, spec.name)
    row_rules = [rule for rule in table_rules if isinstance(rule, RowRule)]
    broadcast_max_keys = int(quality_settings(cfg).get("broadcast_max_keys", 2_000_000))

    persisted: dict[str, DataFrame] = {}
    key_sets: list[tuple[KeyRule, DataFrame, bool]] = []
    for rule in table_rules:
        if not isinstance(rule, KeyRule):
            continue
        keys = rule.keys(tables, cfg).persist()
        n_keys = keys.count()
        LOGGER.info("%s %s: %d violating key(s)", spec.name, rule.rule_id, n_keys)
        if n_keys:
            persisted[rule.rule_id] = keys
            key_sets.append((rule, keys, n_keys <= broadcast_max_keys))
        else:
            keys.unpersist()

    flagged = add_flags(tables[spec.name], row_rules, key_sets, cfg)
    if DUPLICATE_RULE_ID in persisted:
        is_duplicate = F.array_contains(F.col(DQ_FLAGS_COLUMN), DUPLICATE_RULE_ID)
        resolved = resolve_duplicates(flagged.where(is_duplicate), spec).persist()
        persisted["__resolved_duplicates"] = resolved
        unique = flagged.where(~is_duplicate).withColumn(_DUP_REASON, F.lit(None).cast("string"))
        flagged = unique.unionByName(resolved)
    else:
        flagged = flagged.withColumn(_DUP_REASON, F.lit(None).cast("string"))

    quarantine_ids = sorted({rule.rule_id for rule in table_rules if rule.quarantine})
    decided = add_quarantine_reason(flagged, quarantine_ids)

    table_corrections = [c for c in corrections if c.table == spec.name]
    silver = apply_corrections(
        decided.where(F.col(DQ_REASON_COLUMN).isNull()), table_corrections, cfg
    ).select(*spec.columns, DQ_FLAGS_COLUMN)
    quarantine = decided.where(F.col(DQ_REASON_COLUMN).isNotNull()).select(
        *spec.columns, CORRUPT_RECORD_COLUMN, DQ_FLAGS_COLUMN, DQ_REASON_COLUMN
    )
    return silver, quarantine, persisted


def count_corrections(
    standardized: DataFrame,
    quarantined: DataFrame,
    spec: TableSpec,
    corrections: Sequence[Correction],
    cfg: Config,
) -> list[list[Any]]:
    """Count the values set to null by each correction of a table.

    Quarantined rows keep their uncorrected values, so the number of corrected
    silver values is the number of invalid values of the whole table minus the
    number of invalid values found in quarantine.
    """
    table_corrections = [c for c in corrections if c.table == spec.name]
    if not table_corrections:
        return []
    aggregates = [
        F.sum(F.when(c.invalid(cfg), 1).otherwise(0)).alias(f"c{index}")
        for index, c in enumerate(table_corrections)
    ]
    total = standardized.agg(*aggregates).first()
    excluded = quarantined.agg(*aggregates).first()
    return [
        [
            c.table,
            c.column,
            c.description,
            int(total[f"c{index}"] or 0) - int(excluded[f"c{index}"] or 0),
        ]
        for index, c in enumerate(table_corrections)
    ]


def run(spark: SparkSession, cfg: Config) -> dict[str, list[list[Any]]]:
    """Build the silver and quarantine layers and write the cleaning summary.

    Args:
        spark: Active Spark session.
        cfg: Project configuration.

    Returns:
        The rows of the summary tables, keyed by table title.
    """
    tables = dict(load_standardized(spark, cfg))
    rules = build_rules()
    corrections = build_corrections()

    overview: list[list[Any]] = []
    flag_rows: list[list[Any]] = []
    reason_rows: list[list[Any]] = []
    correction_rows: list[list[Any]] = []

    for name in CLEANING_ORDER:
        spec = TABLES[name]
        standardized = tables[name]
        silver, quarantine, persisted = clean_table(tables, cfg, spec, rules, corrections)
        silver_path = io.layer_path(cfg, "silver", name)
        quarantine_path = io.layer_path(cfg, "quarantine", name)
        try:
            io.write_parquet(silver, silver_path, partition_by=spec.partition_by or None)
            io.write_parquet(quarantine, quarantine_path)
        finally:
            for frame in persisted.values():
                frame.unpersist()

        written = io.read_parquet(spark, silver_path)
        rejected = io.read_parquet(spark, quarantine_path)
        bronze_rows = standardized.count()
        silver_rows = written.count()
        quarantined_rows = rejected.count()
        flagged_rows = written.where(F.size(DQ_FLAGS_COLUMN) > 0).count()
        if silver_rows + quarantined_rows != bronze_rows:
            raise RuntimeError(
                f"{name}: {silver_rows} silver + {quarantined_rows} quarantined rows "
                f"!= {bronze_rows} bronze rows"
            )
        overview.append(
            [
                name,
                bronze_rows,
                silver_rows,
                quarantined_rows,
                100.0 * quarantined_rows / bronze_rows if bronze_rows else 0.0,
                flagged_rows,
                100.0 * flagged_rows / silver_rows if silver_rows else 0.0,
            ]
        )
        flag_counts = (
            written.select(F.explode(DQ_FLAGS_COLUMN).alias("flag")).groupBy("flag").count()
        )
        flag_rows.extend(
            [name, row["flag"], row["count"]] for row in flag_counts.orderBy("flag").collect()
        )
        reason_counts = rejected.groupBy(DQ_REASON_COLUMN).count().orderBy(DQ_REASON_COLUMN)
        reason_rows.extend(
            [name, row[DQ_REASON_COLUMN], row["count"]] for row in reason_counts.collect()
        )
        correction_rows.extend(count_corrections(standardized, rejected, spec, corrections, cfg))
        LOGGER.info(
            "silver %s: %d rows kept, %d quarantined, %d flagged",
            name,
            silver_rows,
            quarantined_rows,
            flagged_rows,
        )
        # Children are checked against the rows that actually reached silver.
        tables[name] = written

    overview.sort(key=lambda row: row[0])
    summary_tables = [
        io.ReportTable(
            [
                "table",
                "bronze_rows",
                "silver_rows",
                "quarantined_rows",
                "pct_quarantined",
                "silver_rows_with_flags",
                "pct_silver_rows_with_flags",
            ],
            overview,
            title="Rows before and after cleaning",
        ),
        io.ReportTable(
            ["table", "dq_reason", "rows"], sorted(reason_rows), title="Quarantined rows per reason"
        ),
        io.ReportTable(
            ["table", "dq_flag", "rows"], sorted(flag_rows), title="Silver rows per quality flag"
        ),
        io.ReportTable(
            ["table", "column", "correction", "values_set_to_null"],
            sorted(correction_rows),
            title="Deterministic corrections",
        ),
    ]
    quarantine_rules = sorted({rule.rule_id for rule in rules if rule.quarantine})
    io.write_markdown(
        io.output_path(cfg, "preparation", "cleaning_summary.md"),
        "Cleaning summary (bronze to silver)",
        summary_tables,
        parameters={
            "reference_year": reference_year(cfg),
            "quarantine_rules": quarantine_rules,
            "duplicate_handling": (
                "identical rows sharing a primary key: one copy kept, others quarantined; "
                "conflicting rows: all quarantined"
            ),
            "foreign_keys_checked_against": "silver parent tables",
            "silver_path": cfg.paths.silver,
            "quarantine_path": cfg.paths.quarantine,
        },
        float_format=".4f",
    )
    for table in summary_tables:
        slug = str(table.title).lower().replace(" ", "_")
        io.write_csv(
            io.output_path(cfg, "preparation", f"cleaning_{slug}.csv"), table.columns, table.rows
        )
    return {str(table.title): [list(row) for row in table.rows] for table in summary_tables}


def main() -> None:
    """CLI entry point."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    args = parser.parse_args()
    cfg = load_config(args.config)
    spark = build_spark(cfg, "cleaning")
    try:
        run(spark, cfg)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
