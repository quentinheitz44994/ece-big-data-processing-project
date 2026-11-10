"""Kafka topic administration (idempotent topic creation).

Adapted from ``admin.py`` of the course lab 05. Run by the one-shot ``kafka-init``
compose service::

    python -m imdb_project.streaming.admin
"""

from __future__ import annotations

import argparse
import time

from confluent_kafka import KafkaError, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic

from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.logging import get_logger

LOGGER = get_logger(__name__)


def wait_for_broker(
    admin: AdminClient, timeout_seconds: float, poll_seconds: float = 2.0
) -> set[str]:
    """Wait until the broker answers a metadata request.

    Args:
        admin: Kafka admin client.
        timeout_seconds: Maximum time to wait.
        poll_seconds: Pause between two attempts.

    Returns:
        The names of the existing topics.

    Raises:
        TimeoutError: If the broker is still unreachable after the timeout.
    """
    deadline = time.monotonic() + timeout_seconds
    while True:
        try:
            return set(admin.list_topics(timeout=5).topics)
        except KafkaException as exc:
            if time.monotonic() >= deadline:
                raise TimeoutError(f"Kafka broker unreachable: {exc}") from exc
            LOGGER.info("Waiting for the Kafka broker (%s)", exc)
            time.sleep(poll_seconds)


def ensure_topic(
    bootstrap_servers: str,
    topic: str,
    num_partitions: int = 1,
    replication_factor: int = 1,
    timeout_seconds: float = 90.0,
) -> bool:
    """Create ``topic`` unless it already exists.

    Args:
        bootstrap_servers: Kafka bootstrap servers.
        topic: Topic name.
        num_partitions: Number of partitions of a newly created topic.
        replication_factor: Replication factor of a newly created topic.
        timeout_seconds: Maximum time to wait for the broker.

    Returns:
        ``True`` when the topic was created, ``False`` when it already existed.
    """
    admin = AdminClient({"bootstrap.servers": bootstrap_servers})
    if topic in wait_for_broker(admin, timeout_seconds):
        LOGGER.info("Topic %s already exists", topic)
        return False
    futures = admin.create_topics(
        [NewTopic(topic, num_partitions=num_partitions, replication_factor=replication_factor)]
    )
    try:
        futures[topic].result(timeout=30)
    except KafkaException as exc:
        if exc.args and exc.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
            LOGGER.info("Topic %s already exists", topic)
            return False
        raise
    LOGGER.info("Topic %s created (%d partition(s))", topic, num_partitions)
    return True


def run(cfg: Config) -> bool:
    """Create the project topic from the ``kafka`` section of the settings."""
    kafka = cfg.kafka
    return ensure_topic(
        bootstrap_servers=kafka.bootstrap_servers,
        topic=kafka.topic,
        num_partitions=int(kafka.get("num_partitions", 1)),
        replication_factor=int(kafka.get("replication_factor", 1)),
        timeout_seconds=float(kafka.get("startup_timeout_seconds", 90)),
    )


def main() -> None:
    """CLI entry point."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    args = parser.parse_args()
    run(load_config(args.config))


if __name__ == "__main__":
    main()
