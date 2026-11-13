"""Inject uniquely identified, timestamp-shifted copies of matched events."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import time
import uuid
from pathlib import Path
from typing import Any

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.spark_session import build_spark


def event_timestamp(text: str) -> dt.datetime:
    """Parse an ISO timestamp and normalise it to UTC."""
    parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    return parsed.replace(tzinfo=dt.UTC) if parsed.tzinfo is None else parsed.astimezone(dt.UTC)


def shifted_event(
    event: dict[str, Any], offset_minutes: float, reference: dt.datetime
) -> dict[str, Any]:
    """Copy an event, change its timestamp and assign a new deduplication key."""
    shifted = copy.deepcopy(event)
    shifted["meta"]["id"] = f"{event['meta']['id']}-late-{uuid.uuid4().hex}"
    shifted["meta"]["dt"] = (
        (reference - dt.timedelta(minutes=offset_minutes)).isoformat().replace("+00:00", "Z")
    )
    shifted["imdb_project_injection"] = {
        "original_event_id": event["meta"]["id"],
        "offset_minutes": float(offset_minutes),
    }
    return shifted


def publish(
    cfg: Config,
    events: list[dict[str, Any]],
    reference: dt.datetime,
    application_run_id: str,
    kafka_producer: Any | None = None,
) -> dict[str, Any]:
    """Publish shifted samples and record delivery outcomes even after errors."""
    from confluent_kafka import Producer

    settings = cfg.streaming.late_events
    producer = kafka_producer or Producer({"bootstrap.servers": str(cfg.kafka.bootstrap_servers)})
    report: dict[str, Any] = {
        "application_run_id": application_run_id,
        "reference_event_time": reference.isoformat(),
        "status": "running",
        "events": [],
        "delivery_errors": [],
        "undelivered": 0,
    }

    def delivered(error: Any, message: Any) -> None:
        if error is not None:
            report["delivery_errors"].append(str(error))

    try:
        for event in events:
            for offset in settings.offsets_minutes:
                shifted = shifted_event(event, float(offset), reference)
                deadline = time.monotonic() + float(settings.enqueue_timeout_seconds)
                while True:
                    try:
                        producer.produce(
                            str(cfg.kafka.topic),
                            key=shifted["meta"]["id"].encode("utf-8"),
                            value=json.dumps(shifted, ensure_ascii=False).encode("utf-8"),
                            on_delivery=delivered,
                        )
                        break
                    except BufferError:
                        if time.monotonic() >= deadline:
                            raise TimeoutError(
                                "Kafka queue remained full during late injection"
                            ) from None
                        producer.poll(float(settings.poll_seconds))
                producer.poll(0)
                report["events"].append(
                    {
                        "event_id": shifted["meta"]["id"],
                        "event_time": shifted["meta"]["dt"],
                        "offset_minutes": float(offset),
                    }
                )
        report["status"] = "injected"
    except BaseException:
        report["status"] = "failed"
        raise
    finally:
        try:
            report["undelivered"] = producer.flush(float(settings.flush_timeout_seconds)) or 0
            if report["undelivered"] or report["delivery_errors"]:
                report["status"] = "failed"
        finally:
            target = io.output_path(cfg, str(settings.report_file))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if report["status"] == "failed":
        raise RuntimeError("Late-event delivery failed; see the injection report")
    return report


def run(
    spark: SparkSession,
    cfg: Config,
    reference: dt.datetime | None = None,
    application_run_id: str | None = None,
) -> dict[str, Any] | None:
    """Sample only matched events of the current run and inject their copies."""
    if application_run_id is None:
        manifest = json.loads(
            io.output_path(cfg, str(cfg.streaming.run_file)).read_text(encoding="utf-8")
        )
        application_run_id = str(manifest["application_run_id"])
        if reference is None and manifest.get("greatest_event_time"):
            reference = event_timestamp(manifest["greatest_event_time"])
    path = io.layer_path(cfg, "streaming", str(cfg.streaming.sinks.matched_events))
    if not Path(path).is_dir() or not any(Path(path).glob("*.parquet")):
        return None
    samples = (
        spark.read.parquet(path)
        .where(F.col("application_run_id") == application_run_id)
        .orderBy(F.col("event_time").desc(), "event_id")
        .select("raw_json", "event_time")
        .limit(int(cfg.streaming.late_events.sample_size))
        .collect()
    )
    if not samples:
        return None
    if reference is None:
        reference = samples[0].event_time.replace(tzinfo=dt.UTC)
    return publish(
        cfg, [json.loads(row.raw_json) for row in samples], reference, application_run_id
    )


def main() -> None:
    """Inject from a completed or active run, using its observed event frontier."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    parser.add_argument("--reference-time", default=None)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    cfg = load_config(args.config)
    spark = build_spark(cfg, "late_event_injector")
    try:
        reference = event_timestamp(args.reference_time) if args.reference_time else None
        run(spark, cfg, reference, args.run_id)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
