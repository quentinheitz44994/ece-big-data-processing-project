r"""Bronze ingestion: raw IMDb ``*.tsv.gz`` files to Parquet, one folder per table.

The bronze layer is a faithful copy of the raw files:

* every column is read as a string (explicit schema, no type inference);
* quoting is disabled, because titles contain unbalanced double quotes;
* the ``\N`` marker is *not* converted to null, so that the null profiling can
  tell the different kinds of missing values apart;
* a line whose number of fields does not match the header is kept, with the raw
  text stored in ``_corrupt_record``.

Note that Spark's CSV reader surfaces an empty raw field as a SQL null.
"""

from __future__ import annotations

import argparse
import time
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.logging import get_logger
from imdb_project.common.schemas import CORRUPT_RECORD_COLUMN, TABLES, TableSpec
from imdb_project.common.spark_session import build_spark

LOGGER = get_logger(__name__)


def read_raw_tsv(spark: SparkSession, path: str, spec: TableSpec) -> DataFrame:
    """Read one raw IMDb file with the all-string bronze schema.

    Args:
        spark: Active Spark session.
        path: Path of the ``.tsv`` or ``.tsv.gz`` file.
        spec: Specification of the table.

    Returns:
        A DataFrame with the raw columns plus ``_corrupt_record``.
    """
    return (
        spark.read.option("sep", "\t")
        .option("header", True)
        # No quote character: double quotes are ordinary characters in IMDb titles.
        .option("quote", "\u0000")
        .option("mode", "PERMISSIVE")
        .option("columnNameOfCorruptRecord", CORRUPT_RECORD_COLUMN)
        # Fail fast if IMDb ever changes the columns or their order.
        .option("enforceSchema", False)
        .option("encoding", "UTF-8")
        .schema(spec.bronze_schema)
        .csv(path)
    )


def ingest_table(spark: SparkSession, cfg: Config, spec: TableSpec) -> dict[str, object]:
    """Convert one raw file to bronze Parquet and return its row counts.

    Args:
        spark: Active Spark session.
        cfg: Project configuration.
        spec: Specification of the table to ingest.

    Returns:
        A summary row: table, source file, rows, columns, malformed rows, seconds.

    Raises:
        FileNotFoundError: If the raw file has not been downloaded.
    """
    source = io.layer_path(cfg, "raw", spec.source_file)
    target = io.layer_path(cfg, "bronze", spec.name)
    if not Path(source).is_file():
        raise FileNotFoundError(f"{source} not found: run scripts/download_imdb.sh first")

    started = time.monotonic()
    # A gzip file is read by a single task. Capping the rows per output file
    # gives every later job one input split per file, hence parallel scans.
    io.write_parquet(
        read_raw_tsv(spark, source, spec),
        target,
        max_records_per_file=int(cfg.get("ingestion.max_records_per_file", 2_000_000)),
    )
    bronze = io.read_parquet(spark, target)
    counts = bronze.agg(
        F.count(F.lit(1)).alias("rows"),
        F.count(F.col(CORRUPT_RECORD_COLUMN)).alias("malformed_rows"),
    ).first()
    summary = {
        "table": spec.name,
        "source_file": spec.source_file,
        "rows": counts["rows"],
        "columns": len(spec.columns),
        "malformed_rows": counts["malformed_rows"],
        "seconds": round(time.monotonic() - started, 1),
    }
    LOGGER.info("bronze %s", summary)
    return summary


def run(
    spark: SparkSession, cfg: Config, tables: Iterable[str] | None = None
) -> list[dict[str, object]]:
    """Ingest the selected tables (all by default) and write the summary report.

    Each gzip file is a single non-splittable Spark task, so several tables are
    converted concurrently to use more than one core.

    Args:
        spark: Active Spark session.
        cfg: Project configuration.
        tables: Optional subset of table names.

    Returns:
        One summary row per table, sorted by table name.
    """
    specs = [TABLES[name] for name in (tables or TABLES)]
    workers = max(1, int(cfg.get("ingestion.parallel_tables", 3)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        summaries = list(pool.map(lambda spec: ingest_table(spark, cfg, spec), specs))
    summaries.sort(key=lambda row: str(row["table"]))

    columns = ["table", "source_file", "rows", "columns", "malformed_rows"]
    rows = [[summary[column] for column in columns] for summary in summaries]
    io.write_markdown(
        io.output_path(cfg, "preparation", "ingestion_summary.md"),
        "Bronze ingestion summary",
        [io.ReportTable(columns, rows, title="Rows per table")],
        parameters={
            "raw_path": cfg.paths.raw,
            "bronze_path": cfg.paths.bronze,
            "bronze_column_type": "string (all columns)",
            "malformed_rows": "lines whose number of fields differs from the header",
        },
    )
    io.write_csv(io.output_path(cfg, "preparation", "ingestion_summary.csv"), columns, rows)
    return summaries


def main() -> None:
    """CLI entry point."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    parser.add_argument(
        "--tables",
        nargs="+",
        choices=sorted(TABLES),
        default=None,
        help="Subset of tables to ingest (default: all).",
    )
    args = parser.parse_args()
    cfg = load_config(args.config)
    spark = build_spark(cfg, "ingest")
    try:
        run(spark, cfg, args.tables)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
