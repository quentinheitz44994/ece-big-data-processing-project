"""Test doubles for the HTTP layer: no test ever touches the network."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class FakeResponse:
    """Minimal stand-in for ``requests.Response``."""

    def __init__(
        self,
        payload: Any = None,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        text: str | None = None,
    ) -> None:
        self._payload = payload
        self.status_code = status_code
        self.headers = headers or {}
        self.text = text if text is not None else str(payload)

    def json(self) -> Any:
        if self._payload is None:
            raise ValueError("no JSON body")
        return self._payload


class FakeSession:
    """Scripted session: each call pops the next response registered for its URL.

    A handler may also be a callable ``(method, url, payload) -> FakeResponse``.
    ``robots`` maps a host to the text of its robots.txt (404 when absent).
    """

    def __init__(self, robots: dict[str, str] | None = None) -> None:
        self.headers: dict[str, str] = {}
        self.robots = robots or {}
        self.scripts: dict[str, list[Any]] = {}
        self.calls: list[tuple[str, str, dict[str, Any]]] = []
        self.closed = False

    def script(self, url: str, *responses: Any) -> None:
        self.scripts.setdefault(url, []).extend(responses)

    def _respond(self, method: str, url: str, payload: dict[str, Any]) -> FakeResponse:
        if url.endswith("/robots.txt"):
            host = url.split("/")[2]
            if host in self.robots:
                return FakeResponse(text=self.robots[host])
            return FakeResponse(status_code=404, text="")
        self.calls.append((method, url, dict(payload or {})))
        queue = self.scripts.get(url)
        if not queue:
            raise AssertionError(f"Unexpected request: {method} {url} {payload}")
        handler = queue[0] if len(queue) == 1 and callable(queue[0]) else queue.pop(0)
        if callable(handler) and not isinstance(handler, FakeResponse):
            return handler(method, url, dict(payload or {}))
        return handler

    def get(self, url: str, params: dict[str, Any] | None = None, timeout: Any = None):
        return self._respond("GET", url, params or {})

    def post(self, url: str, data: dict[str, Any] | None = None, timeout: Any = None):
        return self._respond("POST", url, data or {})

    def close(self) -> None:
        self.closed = True


class FakeClock:
    """Deterministic clock: sleeping advances the time, nothing actually waits."""

    def __init__(self) -> None:
        self.now = 1000.0
        self.sleeps: list[float] = []

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def make_client(cfg, session: FakeSession | None = None, **overrides: Any):
    """Build a ``WikimediaClient`` wired to fakes; returns ``(client, session, clock)``."""
    from imdb_project.enrichment.http_client import WikimediaClient

    values = {
        "wikimedia.contact": "tests@example.org",
        **{f"wikimedia.{k}": v for k, v in overrides.items()},
    }
    session = session or FakeSession()
    clock = FakeClock()
    client = WikimediaClient(
        cfg.with_overrides(values).wikimedia,
        session=session,
        sleep=clock.sleep,
        monotonic=clock.monotonic,
    )
    return client, session, clock


Handler = Callable[[str, str, dict[str, Any]], FakeResponse]
