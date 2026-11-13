"""Kafka producer: Wikimedia recent changes (EventStreams, SSE) to a Kafka topic.

Reads the single ``recentchange`` stream of Wikimedia EventStreams and publishes
the events passing a light filter (configured wikis, change types and
namespaces). The Kafka key is the event id (``meta.id``) and the value is the raw
JSON of the event, untouched.

The connection identifies itself with the project User-Agent, resumes after a
disconnection with the ``Last-Event-ID`` header, stops after
``streaming.producer.duration_minutes`` (or on SIGTERM) and flushes the producer
before exiting. Run by the ``producer`` compose service::

    python -m imdb_project.streaming.producer
"""

from __future__ import annotations

import argparse
import json
import signal
import socket
import time
from collections.abc import Collection, Iterable, Iterator
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import requests

from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.logging import get_logger
from imdb_project.enrichment.http_client import WikimediaClient, utc_now
from imdb_project.streaming.admin import ensure_topic

LOGGER = get_logger(__name__)


@dataclass
class SseEvent:
    """One Server-Sent Event."""

    event: str = "message"
    data: str = ""
    id: str | None = None


@dataclass
class ProducerStats:
    """Counters of a producer run."""

    started_at: str = field(default_factory=utc_now)
    finished_at: str | None = None
    received: int = 0
    produced: int = 0
    filtered_out: int = 0
    invalid: int = 0
    delivery_errors: int = 0
    undelivered: int = 0
    reconnects: int = 0
    robots: dict[str, str] = field(default_factory=dict)


def iter_sse_events(lines: Iterable[str | bytes]) -> Iterator[SseEvent]:
    """Parse the lines of a ``text/event-stream`` response.

    Args:
        lines: Lines of the stream, without their line terminator.

    Yields:
        One :class:`SseEvent` per event (blank line = end of event). Comment lines
        (starting with ``:``) are ignored.
    """
    current = SseEvent()
    data: list[str] = []
    for raw in lines:
        line = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else raw
        if line == "":
            if data or current.id is not None:
                current.data = "\n".join(data)
                yield current
            current, data = SseEvent(), []
            continue
        if line.startswith(":"):
            continue
        name, _, value = line.partition(":")
        value = value[1:] if value.startswith(" ") else value
        if name == "data":
            data.append(value)
        elif name == "event":
            current.event = value
        elif name == "id":
            current.id = value


def keep_event(
    change: dict[str, Any],
    wikis: Collection[str],
    types: Collection[str],
    namespaces: Collection[int],
) -> bool:
    """Return whether a recent change passes the producer filter.

    Args:
        change: Decoded ``recentchange`` event.
        wikis: Accepted wiki database names (``enwiki``...).
        types: Accepted change types (``edit``, ``new``...).
        namespaces: Accepted namespaces (0 = articles).
    """
    return (
        change.get("wiki") in wikis
        and change.get("type") in types
        and change.get("namespace") in namespaces
        and bool(change.get("meta", {}).get("id"))
    )


class StopFlag:
    """Stop request, set by a signal handler (SIGTERM / SIGINT)."""

    def __init__(self) -> None:
        self.requested = False

    def request(self, *_: Any) -> None:
        """Ask the producer loop to stop (usable as a signal handler)."""
        self.requested = True


def run(
    cfg: Config,
    duration_minutes: float | None = None,
    kafka_producer: Any | None = None,
    http_session: Any | None = None,
    stop: StopFlag | None = None,
) -> ProducerStats:
    """Stream recent changes to Kafka until the duration elapses.

    Args:
        cfg: Project configuration.
        duration_minutes: Overrides ``streaming.producer.duration_minutes``
            (0 = run until stopped).
        kafka_producer: Kafka producer to use (injected in tests).
        http_session: HTTP session to use (injected in tests).
        stop: Flag checked between events to stop before the duration elapses.

    Returns:
        The counters of the run.
    """
    settings = cfg.streaming.producer
    topic = str(cfg.kafka.topic)
    url = str(cfg.wikimedia.eventstreams_url)
    wikis = set(cfg.streaming.wikis)
    types = set(settings.change_types)
    namespaces = {int(value) for value in settings.namespaces}
    minutes = float(settings.duration_minutes if duration_minutes is None else duration_minutes)
    reconnect_delay = float(settings.get("reconnect_delay_seconds", 5))
    queue_poll_seconds = float(settings.get("queue_poll_seconds", 0.1))
    flush_timeout_seconds = float(settings.get("flush_timeout_seconds", 30))
    if queue_poll_seconds <= 0 or flush_timeout_seconds < 0:
        raise ValueError(
            "queue_poll_seconds must be positive and flush_timeout_seconds nonnegative"
        )

    stats = ProducerStats()
    client = WikimediaClient(cfg.wikimedia, session=http_session)

    def on_delivery(error: Any, _message: Any) -> None:
        if error is not None:
            stats.delivery_errors += 1

    stop = stop or StopFlag()
    deadline = time.monotonic() + minutes * 60 if minutes > 0 else None
    last_event_id: str | None = None
    last_log = time.monotonic()

    def finished() -> bool:
        return stop.requested or (deadline is not None and time.monotonic() >= deadline)

    try:
        client.check_robots(url)  # raises with the "enforce" policy
        stats.robots = dict(client.stats.robots)
        if kafka_producer is None:
            from confluent_kafka import Producer

            ensure_topic(
                str(cfg.kafka.bootstrap_servers),
                topic,
                int(cfg.kafka.get("num_partitions", 1)),
                int(cfg.kafka.get("replication_factor", 1)),
                float(cfg.kafka.get("startup_timeout_seconds", 90)),
            )
            kafka_producer = Producer(
                {
                    "bootstrap.servers": str(cfg.kafka.bootstrap_servers),
                    "client.id": socket.gethostname(),
                    "compression.type": "lz4",
                    "linger.ms": 100,
                }
            )

        LOGGER.info(
            "producing %s to topic %s for %s minute(s), wikis=%s", url, topic, minutes, wikis
        )
        while not finished():
            headers = {"Accept": "text/event-stream"}
            if last_event_id:
                headers["Last-Event-ID"] = last_event_id
            try:
                with client.session.get(
                    url, headers=headers, stream=True, timeout=(10, 60)
                ) as response:
                    response.raise_for_status()
                    for event in iter_sse_events(response.iter_lines()):
                        if event.event == "message" and event.data:
                            try:
                                change = json.loads(event.data)
                            except ValueError:
                                stats.invalid += 1
                                change = None
                            if change is not None:
                                stats.received += 1
                                if keep_event(change, wikis, types, namespaces):
                                    queued = False
                                    while not finished():
                                        try:
                                            kafka_producer.produce(
                                                topic,
                                                key=str(change["meta"]["id"]).encode("utf-8"),
                                                value=event.data.encode("utf-8"),
                                                on_delivery=on_delivery,
                                            )
                                        except BufferError:
                                            kafka_producer.poll(queue_poll_seconds)
                                        else:
                                            queued = True
                                            stats.produced += 1
                                            kafka_producer.poll(0)
                                            break
                                    if not queued:
                                        break  # keep the last successfully handled SSE offset
                                else:
                                    stats.filtered_out += 1
                        if event.id:
                            last_event_id = event.id
                        if time.monotonic() - last_log >= 60:
                            last_log = time.monotonic()
                            LOGGER.info("received=%d produced=%d", stats.received, stats.produced)
                        if finished():
                            break
            except requests.RequestException as exc:
                if finished():
                    break
                stats.reconnects += 1
                LOGGER.warning("stream interrupted (%s), reconnecting in %ss", exc, reconnect_delay)
                time.sleep(reconnect_delay)
    finally:
        try:
            if kafka_producer is not None:
                stats.undelivered = kafka_producer.flush(flush_timeout_seconds) or 0
        finally:
            stats.finished_at = utc_now()
            LOGGER.info("producer finished: %s", asdict(stats))
            try:
                stats_path = settings.get("stats_path")
                if stats_path:
                    path = Path(str(stats_path))
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(json.dumps(asdict(stats)) + "\n", encoding="utf-8")
            finally:
                client.close()
    if stats.undelivered or stats.delivery_errors:
        raise RuntimeError(
            f"Kafka delivery failed: {stats.undelivered} undelivered, "
            f"{stats.delivery_errors} delivery errors"
        )
    return stats


def main() -> None:
    """CLI entry point."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    parser.add_argument(
        "--duration-minutes",
        type=float,
        default=None,
        help="Run duration (default: streaming.producer.duration_minutes; 0 = until stopped).",
    )
    args = parser.parse_args()
    stop = StopFlag()
    for signum in (signal.SIGTERM, signal.SIGINT):
        signal.signal(signum, stop.request)  # `docker stop` flushes and exits cleanly
    run(load_config(args.config), args.duration_minutes, stop=stop)


if __name__ == "__main__":
    main()
