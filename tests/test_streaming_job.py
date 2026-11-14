from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.streaming import late_event_injector, stream_job, summary
from imdb_project.streaming.metrics_listener import MetricsListener
from streaming_fakes import FakeKafkaProducer, change


def test_explicit_json_parsing_filters_invalid_records(spark):
    valid = change("ok", "Alpha (film)", "2026-11-13T12:01:00Z", old=100, new=150)
    records = spark.createDataFrame(
        [(json.dumps(event),) for event in [valid, change("bad-time", "A", "invalid"), {}]]
        + [("{broken",)],
        "value string",
    )
    (row,) = stream_job.parse_events(records).collect()
    assert row.event_id == "ok" and row.size_delta == 50
    assert row.event_time == dt.datetime(2026, 11, 13, 12, 1)
    assert row.bot is False and row.injection_offset_minutes is None


def test_window_boundaries_and_bot_groups(spark):
    events = spark.createDataFrame(
        [
            ("run", dt.datetime(2026, 11, 13, 12, 4, 59), "enwiki", "film", False, "A", 50),
            ("run", dt.datetime(2026, 11, 13, 12, 5), "enwiki", "film", True, "A", -10),
        ],
        "application_run_id string, event_time timestamp, wiki string, entity_type string, "
        "bot boolean, page_title_normalized string, size_delta long",
    )
    tumbling = stream_job.window_counts(events, "5 minutes", "5 minutes").collect()
    assert sorted((row.window.start.minute, row.bot, row.edits) for row in tumbling) == [
        (0, False, 1),
        (5, True, 1),
    ]
    sliding = stream_job.window_counts(events, "10 minutes", "5 minutes").collect()
    assert len(sliding) == 4 and sum(row.edits for row in sliding) == 4
    assert {row.avg_size_delta for row in sliding} == {-10.0, 50.0}


def test_late_injection_uses_distinct_ids_and_keeps_original_unchanged(cfg):
    reference = dt.datetime(2026, 11, 13, 12, 30, tzinfo=dt.UTC)
    event = change("original", "Alpha (film)", "2026-11-13T12:29:00Z")
    producer = FakeKafkaProducer()
    configured = cfg.with_overrides({"streaming.late_events.offsets_minutes": [30, 5]})
    report = late_event_injector.publish(configured, [event], reference, "run", producer)
    messages = [json.loads(message[2]) for message in producer.messages]
    assert [message["meta"]["dt"] for message in messages] == [
        "2026-11-13T12:00:00Z",
        "2026-11-13T12:25:00Z",
    ]
    assert len({message["meta"]["id"] for message in messages} | {"original"}) == 3
    assert event["meta"]["dt"] == "2026-11-13T12:29:00Z"
    assert report["status"] == "injected" and producer.flushed


def test_listener_and_summary_preserve_query_identity_and_batch_counts(tmp_path):
    path = tmp_path / "progress.jsonl"
    listener = MetricsListener(path)
    progress = {
        "name": "matched_events",
        "runId": "q1",
        "batchId": 1,
        "numInputRows": 3,
        "stateOperators": [{"numRowsDroppedByWatermark": 1}],
    }
    listener.onQueryProgress(SimpleNamespace(progress=SimpleNamespace(json=json.dumps(progress))))
    listener.onQueryProgress(
        SimpleNamespace(progress=SimpleNamespace(json=json.dumps({**progress, "numInputRows": 0})))
    )
    listener.onQueryTerminated(SimpleNamespace(runId="q1", exception=None))
    assert listener.wait_for_termination({"q1"}, 0) and not listener.errors
    (record,) = summary.read_progress(path, {"q1"})
    assert record["numInputRows"] == 3 and summary.watermark_drops(record) == 1
    assert summary.read_progress(path, {"other-run"}) == []


def test_aggregate_batch_replay_is_idempotent(spark, tmp_path):
    path = str(tmp_path / "aggregate")
    batch = spark.createDataFrame([("run", 2)], "application_run_id string, edits long")
    stream_job.write_aggregate_batch(batch, 1, path, 0)
    stream_job.write_aggregate_batch(batch, 1, path, 0)
    assert spark.read.parquet(path).count() == 1


def test_summary_ignores_uncommitted_window_batches(spark, cfg):
    path = Path(io.layer_path(cfg, "streaming", cfg.streaming.sinks.tumbling))
    (path / "batch_id=0" / "_temporary").mkdir(parents=True)
    assert summary.read_sink(spark, cfg, "tumbling", "run") is None
    stream_job.write_aggregate_batch(
        spark.createDataFrame([("run", 2)], "application_run_id string, edits long"),
        1,
        str(path),
        0,
    )
    assert summary.read_sink(spark, cfg, "tumbling", "run").count() == 1


def test_real_streaming_watermark_deduplication_and_finalized_sinks(spark, cfg, tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    records = spark.readStream.schema("value string").json(str(input_dir))
    lookup = spark.createDataFrame(
        [("enwiki", "Alpha (film)", "tt1", "film", "https://en.wikipedia.org/wiki/Alpha_(film)")],
        "wiki string, page_title_normalized string, imdb_id string, "
        "entity_type string, source_url string",
    )
    configured = cfg.with_overrides(
        {"streaming.trigger_interval": "100 milliseconds", "streaming.console_rows": 0}
    )
    listener = MetricsListener(io.output_path(configured, str(configured.streaming.progress_file)))
    spark.streams.addListener(listener)
    queries = []

    def add_batch(index, events):
        (input_dir / f"batch-{index}.json").write_text(
            "\n".join(json.dumps({"value": json.dumps(event)}) for event in events) + "\n",
            encoding="utf-8",
        )
        for query in queries:
            query.processAllAvailable()

    try:
        queries = stream_job.start_queries(records, lookup, configured, "integration")
        first = change("first", "Alpha (film)", "2026-11-13T12:00:00Z")
        add_batch(1, [first, first])
        add_batch(2, [change("advance", "Alpha (film)", "2026-11-13T12:20:00Z")])
        add_batch(
            3,
            [
                change("accepted-late", "Alpha (film)", "2026-11-13T12:15:00Z"),
                change("rejected-late", "Alpha (film)", "2026-11-13T11:50:00Z"),
            ],
        )
        add_batch(4, [change("close-windows", "Alpha (film)", "2026-11-13T12:40:00Z")])
    finally:
        for query in queries:
            query.stop()
        assert listener.wait_for_termination({str(query.runId) for query in queries}, 30)
        spark.streams.removeListener(listener)
    assert not listener.errors
    matched = summary.read_sink(spark, configured, "matched_events", "integration")
    assert {row.event_id for row in matched.collect()} == {
        "first",
        "advance",
        "accepted-late",
        "close-windows",
    }
    assert {row.match_reason for row in matched.collect()} == {"lookup+title_pattern"}
    finalized = summary.read_sink(spark, configured, "tumbling", "integration")
    assert {row.window.start.minute: row.edits for row in finalized.collect()} == {
        0: 1,
        15: 1,
        20: 1,
    }
    sliding = summary.read_sink(spark, configured, "sliding", "integration")
    assert sliding.count() > finalized.count()
    progress = summary.read_progress(listener.path, {str(query.runId) for query in queries})
    assert (
        sum(
            summary.watermark_drops(record)
            for record in progress
            if record["name"] == "matched_events"
        )
        >= 1
    )
    manifest = {
        "application_run_id": "integration",
        "status": "completed",
        "queries": [{"runId": str(query.runId)} for query in queries],
    }
    summary.run(spark, configured, manifest)
    assert (
        "| matched_events | 4 |"
        in io.output_path(configured, str(configured.streaming.summary_file)).read_text()
    )


def test_non_positive_duration_fails_before_starting(spark, cfg):
    with pytest.raises(ValueError, match="positive"):
        stream_job.run(spark, cfg, 0)


def test_shutdown_prefers_idle_batches_and_bounds_the_wait(monkeypatch):
    clock = [0.0]
    stopped = []

    class Query:
        def __init__(self, name, idle_after):
            self.name, self.idle_after = name, idle_after
            self.isActive = True

        @property
        def status(self):
            return {"isTriggerActive": clock[0] < self.idle_after}

        def stop(self):
            stopped.append((self.name, clock[0]))

    monkeypatch.setattr(stream_job.time, "monotonic", lambda: clock[0])
    monkeypatch.setattr(
        stream_job.time, "sleep", lambda seconds: clock.__setitem__(0, clock[0] + seconds)
    )
    errors = stream_job.stop_queries([Query("idle", 1), Query("busy", 100)], 3, 1)
    assert errors == [] and stopped == [("idle", 1), ("busy", 3)]


def test_window_summary_weights_size_deltas_by_observation_count(spark):
    rows = spark.createDataFrame(
        [("enwiki", "film", False, 2, 20, 2), ("enwiki", "film", False, 1, 100, 1)],
        "wiki string, entity_type string, bot boolean, edits long, total_size_delta long, "
        "size_delta_observations long",
    ).withColumn(
        "window",
        F.struct(
            F.lit(dt.datetime(2026, 11, 13, 12, 0)).alias("start"),
            F.lit(dt.datetime(2026, 11, 13, 12, 5)).alias("end"),
        ),
    )
    (window,) = summary.summarize_windows(rows).collect()
    assert window.edits == 3 and window.avg_size_delta == 40.0
