"""Persist streaming progress and wait for asynchronous termination callbacks."""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any, override

from pyspark.sql.streaming import StreamingQueryListener


class MetricsListener(StreamingQueryListener):
    """Write each progress event as one JSON line, including its query identity.

    Args:
        path: JSON Lines target (append across checkpointed runs).
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._condition = threading.Condition()
        self.terminated: set[str] = set()
        self.errors: list[str] = []

    @override
    def onQueryStarted(self, event: Any) -> None:
        """Receive the synchronous start notification."""

    @override
    def onQueryProgress(self, event: Any) -> None:
        """Store the full Spark progress, including state and watermark metrics."""
        try:
            progress = json.loads(event.progress.json)
            with self._condition, self.path.open("a", encoding="utf-8", newline="\n") as handle:
                handle.write(json.dumps(progress, ensure_ascii=False) + "\n")
        except Exception as exc:
            with self._condition:
                self.errors.append(str(exc))

    @override
    def onQueryIdle(self, event: Any) -> None:
        """Keep idle notifications out of the progress file."""

    @override
    def onQueryTerminated(self, event: Any) -> None:
        """Mark callbacks drained for a query run, including failed queries."""
        with self._condition:
            self.terminated.add(str(event.runId))
            if event.exception:
                self.errors.append(str(event.exception))
            self._condition.notify_all()

    def wait_for_termination(self, run_ids: set[str], timeout: float) -> bool:
        """Wait until the listener has observed termination of every query run."""
        with self._condition:
            return self._condition.wait_for(lambda: run_ids <= self.terminated, timeout)
