"""Generate streaming result tables from measured progress and Parquet sinks."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.spark_session import build_spark


def read_progress(path: Path, run_ids: set[str]) -> list[dict[str, Any]]:
    """Read current query runs, counting each committed batch once."""
    batches: dict[tuple[str, int], dict[str, Any]] = {}
    if not path.is_file():
        return []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        progress = json.loads(line)
        if str(progress.get("runId")) not in run_ids:
            continue
        key = (str(progress["runId"]), int(progress["batchId"]))
        previous = batches.get(key)
        if previous is None or progress.get("numInputRows", 0) >= previous.get("numInputRows", 0):
            batches[key] = progress
    return sorted(
        batches.values(), key=lambda row: (row.get("timestamp", ""), row["name"], row["batchId"])
    )


def watermark_drops(progress: dict[str, Any]) -> int:
    """Sum watermark drops within a query batch, across its state operators."""
    return sum(
        int(operator.get("numRowsDroppedByWatermark", 0))
        for operator in progress.get("stateOperators", [])
    )


def read_sink(spark: SparkSession, cfg: Config, name: str, run_id: str) -> DataFrame | None:
    """Read the current application's output, or return none before any output."""
    path = Path(io.layer_path(cfg, "streaming", str(cfg.streaming.sinks[name])))
    if not path.is_dir():
        return None
    if name == "matched_events":
        metadata = path / "_spark_metadata"
        if metadata.is_dir() and not any(
            entry.name.split(".")[0].isdigit() for entry in metadata.iterdir()
        ):
            return None
        paths = [str(path)] if any(path.glob("*.parquet")) else []
    else:
        # Stopping a query can leave an uncommitted batch in _temporary.
        paths = [str(batch) for batch in path.glob("batch_id=*") if (batch / "_SUCCESS").is_file()]
    if not paths:
        return None
    return spark.read.parquet(*paths).where(F.col("application_run_id") == run_id)


def result_table(frame: DataFrame | None, title: str, limit: int) -> io.ReportTable:
    """Collect a bounded, generated result table."""
    if frame is None:
        return io.ReportTable(["rows"], [[0]], title=title)
    columns, rows = io.collect_rows(frame, limit)
    return io.ReportTable(columns, rows, title=title)


def summarize_windows(aggregate: DataFrame) -> DataFrame:
    """Roll page-grain counts up without averaging page averages equally."""
    return (
        aggregate.groupBy("window", "wiki", "entity_type", "bot")
        .agg(
            F.sum("edits").alias("edits"),
            F.try_divide(F.sum("total_size_delta"), F.sum("size_delta_observations")).alias(
                "avg_size_delta"
            ),
        )
        .select(
            F.col("window.start").alias("window_start"),
            F.col("window.end").alias("window_end"),
            "wiki",
            "entity_type",
            "bot",
            "edits",
            "avg_size_delta",
        )
        .orderBy("window_start", "wiki", "entity_type", "bot")
    )


def run(
    spark: SparkSession, cfg: Config, manifest: dict[str, Any] | None = None
) -> list[io.ReportTable]:
    """Write tables only; cross-query inputs and sliding counts are never summed."""
    settings = cfg.streaming
    if manifest is None:
        manifest = json.loads(
            io.output_path(cfg, str(settings.run_file)).read_text(encoding="utf-8")
        )
    run_id = str(manifest["application_run_id"])
    query_runs = {str(query["runId"]) for query in manifest.get("queries", [])}
    progress = read_progress(io.output_path(cfg, str(settings.progress_file)), query_runs)
    batch_rows = []
    totals: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])
    for record in progress:
        name = str(record["name"])
        dropped = watermark_drops(record)
        totals[name][0] += 1
        totals[name][1] += int(record.get("numInputRows", 0))
        totals[name][2] += dropped
        batch_rows.append(
            [
                name,
                record["batchId"],
                record.get("numInputRows", 0),
                record.get("inputRowsPerSecond", 0),
                record.get("processedRowsPerSecond", 0),
                record.get("durationMs", {}).get("triggerExecution", 0),
                dropped,
                record.get("eventTime", {}).get("watermark"),
            ]
        )
    columns = [
        "query",
        "batch_id",
        "input_rows",
        "input_rows_per_second",
        "processed_rows_per_second",
        "trigger_ms",
        "rows_dropped_by_watermark",
        "watermark",
    ]
    tables = [
        io.ReportTable(
            ["query", "batches", "input_rows", "rows_dropped_by_watermark"],
            [[name, *counts] for name, counts in sorted(totals.items())],
            title="Totals per query (independent Kafka reads)",
        ),
        io.ReportTable(
            columns, batch_rows[-int(settings.report.max_batch_rows) :], title="Latest batches"
        ),
    ]
    io.write_csv(io.output_path(cfg, "streaming", "batches.csv"), columns, batch_rows)
    matched = read_sink(spark, cfg, "matched_events", run_id)
    event_count = matched.count() if matched is not None else 0
    tables.append(
        io.ReportTable(
            ["counter", "value"], [["matched_events", event_count]], title="Matched sink"
        )
    )
    if matched is not None:
        tables.extend(
            [
                result_table(
                    matched.groupBy("wiki", "entity_type", "bot", "match_reason")
                    .count()
                    .orderBy(F.col("count").desc(), "wiki", "entity_type"),
                    "Relevant edits by wiki, entity type and bot flag",
                    int(settings.report.max_window_rows),
                ),
                result_table(
                    matched.groupBy("wiki", "page_title_normalized")
                    .count()
                    .orderBy(F.col("count").desc(), "wiki", "page_title_normalized"),
                    "Top pages (matched events)",
                    int(settings.report.max_examples),
                ),
                result_table(
                    matched.select(
                        "event_time", "wiki", "title", "imdb_id", "entity_type", "match_reason"
                    ).orderBy(F.col("event_time").desc(), "wiki", "title"),
                    "Match examples",
                    int(settings.report.max_examples),
                ),
            ]
        )
    for name in ("tumbling", "sliding"):
        aggregate = read_sink(spark, cfg, name, run_id)
        totals = summarize_windows(aggregate) if aggregate is not None else None
        tables.append(
            result_table(totals, f"Finalized {name} windows", int(settings.report.max_window_rows))
        )
        if aggregate is not None:
            aggregate = aggregate.select(
                F.col("window.start").alias("window_start"),
                F.col("window.end").alias("window_end"),
                "wiki",
                "entity_type",
                "bot",
                "page_title_normalized",
                "edits",
                "avg_size_delta",
            ).orderBy("window_start", F.col("edits").desc(), "wiki", "page_title_normalized")
        tables.append(
            result_table(
                aggregate, f"Finalized {name} page windows", int(settings.report.max_window_rows)
            )
        )
    injection_file = io.output_path(cfg, str(settings.late_events.report_file))
    if injection_file.is_file():
        injection = json.loads(injection_file.read_text(encoding="utf-8"))
        if injection.get("application_run_id") == run_id:
            ids = [event["event_id"] for event in injection["events"]]
            accepted = (
                set()
                if matched is None or not ids
                else {
                    row.event_id
                    for row in matched.where(F.col("event_id").isin(ids))
                    .select("event_id")
                    .collect()
                }
            )
            tables.append(
                io.ReportTable(
                    ["event_id", "offset_minutes", "event_time", "present_in_matched_sink"],
                    [
                        [
                            event["event_id"],
                            event["offset_minutes"],
                            event["event_time"],
                            event["event_id"] in accepted,
                        ]
                        for event in injection["events"]
                    ],
                    title="Injected event observations",
                )
            )
    io.write_markdown(
        io.output_path(cfg, str(settings.summary_file)),
        "Streaming summary",
        tables,
        parameters={
            "application_run_id": run_id,
            "status": manifest["status"],
            "duration_seconds": manifest.get("duration_seconds"),
            "watermark_delay": settings.watermark_delay,
            "tumbling": settings.tumbling.to_dict(),
            "sliding": settings.sliding.to_dict(),
            "late_injection": manifest.get("late_injection"),
            "aggregate_output": "append; finalized windows only",
            "window_scope": "finalized in this run; resumed state can contain prior-run edits",
            "checkpoint_policy": "resume; independent checkpoints per query",
            "matched_events": event_count,
        },
    )
    return tables


def main() -> None:
    """Regenerate the summary from the saved manifest and sinks."""
    args = add_config_argument(argparse.ArgumentParser(description=__doc__)).parse_args()
    cfg = load_config(args.config)
    spark = build_spark(cfg, "streaming_summary")
    try:
        run(spark, cfg)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
