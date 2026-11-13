"""Kafka recentchange parsing, deduplication and append-only windowed queries."""

from __future__ import annotations

import argparse
import json
import time
import uuid
from functools import partial
from pathlib import Path
from typing import Any

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.sql.streaming import StreamingQuery

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.spark_session import build_spark
from imdb_project.enrichment.http_client import utc_now
from imdb_project.streaming import build_lookup, late_event_injector, relevance
from imdb_project.streaming.admin import run as ensure_topic
from imdb_project.streaming.metrics_listener import MetricsListener

RECENTCHANGE_SCHEMA = T.StructType(
    [
        T.StructField(
            "meta",
            T.StructType(
                [T.StructField("id", T.StringType()), T.StructField("dt", T.StringType())]
            ),
        ),
        *[
            T.StructField(name, T.StringType())
            for name in ("title", "wiki", "type", "user", "comment", "server_name")
        ],
        T.StructField("namespace", T.LongType()),
        T.StructField("bot", T.BooleanType()),
        T.StructField("minor", T.BooleanType()),
        *[
            T.StructField(
                name,
                T.StructType(
                    [T.StructField("old", T.LongType()), T.StructField("new", T.LongType())]
                ),
            )
            for name in ("length", "revision")
        ],
        T.StructField(
            "imdb_project_injection",
            T.StructType(
                [
                    T.StructField("original_event_id", T.StringType()),
                    T.StructField("offset_minutes", T.DoubleType()),
                ]
            ),
        ),
    ]
)


def parse_events(records: DataFrame) -> DataFrame:
    """Parse a Kafka value using an explicit schema, dropping unusable events."""
    decoded = records.select(F.col("value").cast("string").alias("raw_json")).withColumn(
        "event", F.from_json("raw_json", RECENTCHANGE_SCHEMA)
    )
    parsed = decoded.select(
        "raw_json",
        F.col("event.meta.id").alias("event_id"),
        F.try_to_timestamp("event.meta.dt").alias("event_time"),
        *[
            F.col(f"event.{name}").alias(name)
            for name in ("title", "wiki", "type", "namespace", "user", "comment", "server_name")
        ],
        F.coalesce(F.col("event.bot"), F.lit(False)).alias("bot"),
        F.coalesce(F.col("event.minor"), F.lit(False)).alias("minor"),
        F.col("event.length.old").alias("old_length"),
        F.col("event.length.new").alias("new_length"),
        F.col("event.revision.old").alias("old_revision"),
        F.col("event.revision.new").alias("new_revision"),
        F.col("event.imdb_project_injection.offset_minutes").alias("injection_offset_minutes"),
    ).withColumn("size_delta", F.col("new_length") - F.col("old_length"))
    return parsed.where(
        F.col("event_id").isNotNull()
        & (F.length("event_id") > 0)
        & F.col("event_time").isNotNull()
        & F.col("wiki").isNotNull()
        & F.col("title").isNotNull()
    )


def matched_events(
    records: DataFrame, lookup: DataFrame, cfg: Config, application_run_id: str
) -> DataFrame:
    """Apply the producer scope, watermark, deduplication and shared relevance."""
    parsed = parse_events(records).where(
        F.col("wiki").isin(list(cfg.streaming.wikis))
        & F.col("type").isin(list(cfg.streaming.producer.change_types))
        & F.col("namespace").isin(list(cfg.streaming.producer.namespaces))
    )
    unique = parsed.withWatermark("event_time", str(cfg.streaming.watermark_delay))
    unique = unique.dropDuplicatesWithinWatermark(["event_id"])
    return relevance.flag_relevant(unique, lookup, relevance.title_patterns(cfg)).withColumn(
        "application_run_id", F.lit(application_run_id)
    )


def window_counts(events: DataFrame, duration: str, slide: str) -> DataFrame:
    """Count edits at page/wiki/entity/bot grain in event-time windows."""
    return events.groupBy(
        F.window("event_time", duration, slide).alias("window"),
        "wiki",
        "entity_type",
        "bot",
        "page_title_normalized",
    ).agg(
        F.count(F.lit(1)).alias("edits"),
        F.avg("size_delta").alias("avg_size_delta"),
        F.sum("size_delta").alias("total_size_delta"),
        F.count("size_delta").alias("size_delta_observations"),
    )


def write_aggregate_batch(batch: DataFrame, batch_id: int, path: str, console_rows: int) -> None:
    """Append one finalized batch with retry-safe batch directories and console output."""
    batch.persist()
    try:
        # A replay of a failed foreachBatch overwrites only the same batch id.
        batch.write.mode("overwrite").parquet(str(Path(path) / f"batch_id={batch_id}"))
        if console_rows > 0:
            batch.orderBy("window.start", F.col("edits").desc(), "page_title_normalized").show(
                console_rows, truncate=False
            )
    finally:
        batch.unpersist()


def start_queries(
    records: DataFrame, lookup: DataFrame, cfg: Config, application_run_id: str
) -> list[StreamingQuery]:
    """Start the three independent queries, stopping any partial startup on error."""
    events = matched_events(records, lookup, cfg, application_run_id)
    settings = cfg.streaming
    queries = []
    try:
        queries.append(
            events.writeStream.queryName("matched_events")
            .outputMode("append")
            .format("parquet")
            .option(
                "checkpointLocation",
                io.layer_path(cfg, "streaming", settings.checkpoints.matched_events),
            )
            .trigger(processingTime=str(settings.trigger_interval))
            .start(io.layer_path(cfg, "streaming", settings.sinks.matched_events))
        )
        for name in ("tumbling", "sliding"):
            window = settings[name]
            counts = window_counts(events, str(window.duration), str(window.slide)).withColumn(
                "application_run_id", F.lit(application_run_id)
            )
            writer = partial(
                write_aggregate_batch,
                path=io.layer_path(cfg, "streaming", settings.sinks[name]),
                console_rows=int(settings.console_rows),
            )
            queries.append(
                counts.writeStream.queryName(name)
                .outputMode("append")
                .foreachBatch(writer)
                .option(
                    "checkpointLocation",
                    io.layer_path(cfg, "streaming", settings.checkpoints[name]),
                )
                .trigger(processingTime=str(settings.trigger_interval))
                .start()
            )
        return queries
    except BaseException:
        for query in queries:
            query.stop()
        raise


def write_json(path: Path, document: dict[str, Any]) -> None:
    """Atomically write a small execution manifest."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    temporary.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def stop_queries(
    queries: list[StreamingQuery], grace_seconds: float, poll_seconds: float
) -> list[Exception]:
    """Prefer idle trigger boundaries, then stop all queries within a bounded grace."""
    pending = list(queries)
    errors = []
    deadline = time.monotonic() + grace_seconds
    while pending:
        for query in pending[:]:
            if (
                not query.isActive
                or not query.status.get("isTriggerActive", False)
                or time.monotonic() >= deadline
            ):
                try:
                    query.stop()
                except Exception as exc:
                    errors.append(exc)
                pending.remove(query)
        if pending:
            time.sleep(min(poll_seconds, max(0, deadline - time.monotonic())))
    return errors


def run(spark: SparkSession, cfg: Config, run_minutes: float | None = None) -> dict[str, Any]:
    """Build/reuse the lookup, run for the configured duration, inject and summarize."""
    from imdb_project.streaming import summary

    settings = cfg.streaming
    minutes = float(settings.run_minutes if run_minutes is None else run_minutes)
    if minutes <= 0 or float(settings.controller_poll_seconds) <= 0:
        raise ValueError("Run duration and controller poll interval must be positive")
    lookup_path = io.layer_path(cfg, "gold", build_lookup.LOOKUP_TABLE)
    if not (Path(lookup_path) / "_SUCCESS").is_file():
        build_lookup.run_scope(spark, cfg)
        build_lookup.run_collect(spark, cfg)
        build_lookup.run_build(spark, cfg)
    lookup = spark.read.parquet(lookup_path)
    ensure_topic(cfg)
    spark.conf.set("spark.sql.shuffle.partitions", int(settings.shuffle_partitions))
    spark.conf.set("spark.sql.adaptive.enabled", "false")
    records = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", str(cfg.kafka.bootstrap_servers))
        .option("subscribe", str(cfg.kafka.topic))
        .option("startingOffsets", str(settings.starting_offsets))
        .option("maxOffsetsPerTrigger", int(settings.max_offsets_per_trigger))
        .load()
    )
    application_run_id = uuid.uuid4().hex
    manifest: dict[str, Any] = {
        "application_run_id": application_run_id,
        "started_at": utc_now(),
        "status": "running",
        "run_minutes": minutes,
        "queries": [],
        "late_injection": "not_attempted",
    }
    run_file = io.output_path(cfg, str(settings.run_file))
    listener = MetricsListener(io.output_path(cfg, str(settings.progress_file)))
    spark.streams.addListener(listener)
    queries: list[StreamingQuery] = []
    failure: BaseException | None = None
    started = time.monotonic()
    frontier = None
    try:
        queries = start_queries(records, lookup, cfg, application_run_id)
        manifest["queries"] = [
            {"name": q.name, "id": str(q.id), "runId": str(q.runId)} for q in queries
        ]
        started = time.monotonic()
        write_json(run_file, manifest)
        while time.monotonic() - started < minutes * 60:
            for query in queries:
                if query.exception() is not None:
                    raise RuntimeError(str(query.exception()))
                if not query.isActive:
                    raise RuntimeError(f"Query {query.name} stopped before the run deadline")
                maximum = (query.lastProgress or {}).get("eventTime", {}).get("max")
                if maximum:
                    observed = late_event_injector.event_timestamp(maximum)
                    frontier = max(frontier, observed) if frontier is not None else observed
                    manifest["greatest_event_time"] = frontier.isoformat()
            watermarks = {
                q.name: (q.lastProgress or {}).get("eventTime", {}).get("watermark")
                for q in queries
            }
            ready = all(value and not value.startswith("1970-") for value in watermarks.values())
            if (
                settings.late_events.enabled
                and manifest["late_injection"] == "not_attempted"
                and time.monotonic() - started >= float(settings.late_events.after_minutes) * 60
                and frontier is not None
                and ready
            ):
                injected = late_event_injector.run(spark, cfg, frontier, application_run_id)
                if injected is not None:
                    injected["watermarks_before_injection"] = watermarks
                    write_json(io.output_path(cfg, str(settings.late_events.report_file)), injected)
                    manifest["late_injection"] = "injected"
                    write_json(run_file, manifest)
            time.sleep(
                min(
                    float(settings.controller_poll_seconds),
                    max(0, minutes * 60 - (time.monotonic() - started)),
                )
            )
        manifest["status"] = "completed"
    except BaseException as exc:
        failure = exc
        manifest["status"] = "failed"
        manifest["error"] = str(exc)
    finally:
        stop_errors = stop_queries(
            queries,
            float(settings.stop_grace_seconds) if failure is None else 0,
            float(settings.controller_poll_seconds),
        )
        if stop_errors:
            failure = failure or stop_errors[0]
        if queries and not listener.wait_for_termination(
            {str(q.runId) for q in queries}, float(settings.listener_wait_seconds)
        ):
            failure = failure or RuntimeError("Timed out waiting for streaming metrics callbacks")
        spark.streams.removeListener(listener)
        if listener.errors:
            failure = failure or RuntimeError("; ".join(listener.errors))
        manifest["duration_seconds"] = round(time.monotonic() - started, 2)
        manifest["finished_at"] = utc_now()
        if failure is not None:
            manifest.update(status="failed", error=str(failure))
        write_json(run_file, manifest)
        try:
            summary.run(spark, cfg, manifest)
        except Exception as exc:
            manifest["summary_error"] = str(exc)
            write_json(run_file, manifest)
            if failure is None:
                raise
    if failure is not None:
        raise failure
    return manifest


def main() -> None:
    """Run the timed streaming job from spark-submit."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    parser.add_argument("--run-minutes", type=float, default=None)
    args = parser.parse_args()
    cfg = load_config(args.config)
    spark = build_spark(cfg, "streaming")
    try:
        run(spark, cfg, args.run_minutes)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
