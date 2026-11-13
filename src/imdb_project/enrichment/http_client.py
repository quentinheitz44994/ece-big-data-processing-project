"""Polite HTTP client and raw response cache for the Wikimedia APIs.

Every network access of the project (Wikipedia Action API, Wikidata Query
Service) goes through :class:`WikimediaClient`, which applies the Wikimedia
policies:

* identifying ``User-Agent`` with a contact address
  (https://foundation.wikimedia.org/wiki/Policy:User-Agent_policy);
* strictly sequential requests with a minimum delay between two requests;
* ``maxlag`` on MediaWiki API calls, ``Retry-After`` honoured on 429 / 503 and
  ``maxlag`` errors, exponential back-off otherwise
  (https://www.mediawiki.org/wiki/API:Etiquette);
* ``robots.txt`` of each host is read and its verdict recorded. Wikimedia's
  ``robots.txt`` addresses crawlers and disallows ``/w/`` and ``/sparql`` for
  them, while these endpoints are the documented programmatic APIs: with the
  default ``report`` policy the verdict is logged and reported, with ``enforce``
  a disallowed URL raises :class:`RobotsDisallowedError` and nothing is fetched.

:class:`RawCache` stores each raw response on disk so that an interrupted
collection resumes without repeating any request.
"""

from __future__ import annotations

import datetime as dt
import email.utils
import hashlib
import json
import os
import time
import urllib.robotparser
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import requests

from imdb_project.common.config import Config
from imdb_project.common.logging import get_logger

LOGGER = get_logger(__name__)

ROBOTS_REPORT = "report"
ROBOTS_ENFORCE = "enforce"


class RobotsDisallowedError(RuntimeError):
    """Raised with the ``enforce`` policy when robots.txt disallows a URL."""


class MissingContactError(RuntimeError):
    """Raised when no contact address is configured for the User-Agent."""


@dataclass
class ClientStats:
    """Counters of a collection run."""

    requests: int = 0
    retries: int = 0
    http_429: int = 0
    http_5xx: int = 0
    maxlag_waits: int = 0
    network_errors: int = 0
    failed: int = 0
    seconds_waited: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    started_at: str = field(
        default_factory=lambda: dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    )
    robots: dict[str, str] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        """Return the counters as a plain dictionary."""
        return asdict(self)


def build_user_agent(wikimedia: Config) -> str:
    """Build the User-Agent header required by the Wikimedia policy.

    Args:
        wikimedia: The ``wikimedia`` section of the settings.

    Returns:
        ``<product>/<version> (<contact>) python-requests/<version>``.

    Raises:
        MissingContactError: If ``wikimedia.contact`` is empty.
    """
    contact = str(wikimedia.get("contact") or "").strip()
    if not contact:
        raise MissingContactError(
            "No Wikimedia contact configured: set WIKIMEDIA_CONTACT_EMAIL in .env "
            "(see .env.example). The Wikimedia User-Agent policy requires one."
        )
    product = wikimedia.get("user_agent_product", "ECE-BigData-IMDb-Project/1.0")
    return f"{product} ({contact}) python-requests/{requests.__version__}"


def parse_retry_after(value: str | None, now: dt.datetime | None = None) -> float | None:
    """Parse a ``Retry-After`` header (delay in seconds or HTTP date).

    Args:
        value: Raw header value.
        now: Current time, for testing.

    Returns:
        The delay in seconds (never negative), or ``None`` when absent or invalid.
    """
    if not value:
        return None
    text = value.strip()
    try:
        return max(0.0, float(text))
    except ValueError:
        pass
    try:
        target = email.utils.parsedate_to_datetime(text)
    except (TypeError, ValueError):
        return None
    if target.tzinfo is None:
        target = target.replace(tzinfo=dt.UTC)
    return max(0.0, (target - (now or dt.datetime.now(dt.UTC))).total_seconds())


class WikimediaClient:
    """Sequential, rate-limited JSON client for the Wikimedia APIs.

    Args:
        wikimedia: The ``wikimedia`` section of the settings.
        session: Optional ``requests``-like session (injected in tests).
        sleep: Sleep function (injected in tests).
        monotonic: Monotonic clock (injected in tests).
    """

    def __init__(
        self,
        wikimedia: Config,
        session: Any | None = None,
        sleep: Callable[[float], None] = time.sleep,
        monotonic: Callable[[], float] = time.monotonic,
    ) -> None:
        self.user_agent = build_user_agent(wikimedia)
        rate = float(wikimedia.get("max_requests_per_second", 1.0))
        self.min_interval = 1.0 / rate if rate > 0 else 0.0
        self.maxlag_seconds = int(wikimedia.get("maxlag_seconds", 5))
        self.timeout = float(wikimedia.get("timeout_seconds", 60))
        self.max_retries = int(wikimedia.get("max_retries", 6))
        self.backoff_base = float(wikimedia.get("backoff_base_seconds", 2.0))
        self.backoff_max = float(wikimedia.get("backoff_max_seconds", 120.0))
        self.retry_statuses = {
            int(s) for s in wikimedia.get("retry_statuses", [429, 500, 502, 503, 504])
        }
        self.retry_api_errors = set(
            wikimedia.get("retry_api_errors", ["maxlag", "ratelimited", "readonly"])
        )
        self.robots_policy = str(wikimedia.get("robots.policy", ROBOTS_REPORT))
        if self.robots_policy not in (ROBOTS_REPORT, ROBOTS_ENFORCE):
            raise ValueError(f"Unknown robots policy: {self.robots_policy!r}")

        self.session = session or requests.Session()
        self.session.headers.update(
            {"User-Agent": self.user_agent, "Accept": "application/json", "Accept-Encoding": "gzip"}
        )
        self._sleep = sleep
        self._monotonic = monotonic
        self._last_request: float | None = None
        self._robots: dict[str, urllib.robotparser.RobotFileParser | None] = {}
        self.stats = ClientStats()
        self._reported: dict[str, float] = {}

    def stats_delta(self) -> dict[str, Any]:
        """Return the counters accumulated since the previous call.

        Lets several collection steps share one client while reporting their own
        numbers of requests, retries and waiting time.
        """
        current = {
            name: value
            for name, value in self.stats.as_dict().items()
            if isinstance(value, (int, float)) and not isinstance(value, bool)
        }
        delta = {
            name: round(value - self._reported.get(name, 0), 3) for name, value in current.items()
        }
        self._reported = current
        return {**delta, "robots": dict(self.stats.robots)}

    # ------------------------------------------------------------------ pacing

    def _wait(self, seconds: float) -> None:
        if seconds > 0:
            self.stats.seconds_waited += seconds
            self._sleep(seconds)

    def _throttle(self) -> None:
        if self._last_request is not None:
            self._wait(self.min_interval - (self._monotonic() - self._last_request))
        self._last_request = self._monotonic()

    def _backoff(self, attempt: int, retry_after: float | None) -> float:
        delay = min(self.backoff_max, self.backoff_base * (2**attempt))
        if retry_after is not None:
            delay = min(max(retry_after, self.min_interval), max(self.backoff_max, retry_after))
        return delay

    # ------------------------------------------------------------------ robots

    def _robots_parser(self, scheme: str, host: str) -> urllib.robotparser.RobotFileParser | None:
        if host not in self._robots:
            parser: urllib.robotparser.RobotFileParser | None = None
            try:
                self._throttle()
                response = self.session.get(f"{scheme}://{host}/robots.txt", timeout=self.timeout)
                if response.status_code == 200:
                    parser = urllib.robotparser.RobotFileParser()
                    parser.parse(response.text.lstrip("\ufeff").splitlines())
            except requests.RequestException as exc:
                LOGGER.warning("robots.txt of %s could not be read: %s", host, exc)
            self._robots[host] = parser
        return self._robots[host]

    def check_robots(self, url: str) -> bool | None:
        """Return the robots.txt verdict for ``url`` and apply the policy.

        Args:
            url: URL about to be requested (without query string).

        Returns:
            ``True`` / ``False`` when robots.txt allows / disallows the path for
            this client, ``None`` when robots.txt is unavailable.

        Raises:
            RobotsDisallowedError: With the ``enforce`` policy, when disallowed.
        """
        parts = urlsplit(url)
        key = f"{parts.netloc}{parts.path}"
        parser = self._robots_parser(parts.scheme, parts.netloc)
        allowed = None if parser is None else parser.can_fetch(self.user_agent, url)
        verdict = {True: "allowed", False: "disallowed", None: "unavailable"}[allowed]
        if key not in self.stats.robots:
            self.stats.robots[key] = verdict
            if allowed is False:
                LOGGER.warning(
                    "robots.txt of %s disallows %s for crawlers (policy: %s)",
                    parts.netloc,
                    parts.path,
                    self.robots_policy,
                )
        if allowed is False and self.robots_policy == ROBOTS_ENFORCE:
            raise RobotsDisallowedError(f"robots.txt disallows {url}")
        return allowed

    # ---------------------------------------------------------------- requests

    def request_json(
        self,
        url: str,
        params: Mapping[str, Any],
        method: str = "GET",
        use_maxlag: bool = False,
    ) -> dict[str, Any]:
        """Send one request (with retries) and return the decoded JSON body.

        Args:
            url: Endpoint URL.
            params: Query parameters (GET) or form fields (POST).
            method: ``GET`` or ``POST``.
            use_maxlag: Add the MediaWiki ``maxlag`` parameter and retry on
                ``maxlag`` errors.

        Returns:
            The JSON document.

        Raises:
            RobotsDisallowedError: See :meth:`check_robots`.
            RuntimeError: When the request still fails after ``max_retries`` retries.
        """
        self.check_robots(url)
        payload = dict(params)
        if use_maxlag:
            payload.setdefault("maxlag", self.maxlag_seconds)

        last_error = "no attempt"
        for attempt in range(self.max_retries + 1):
            if attempt:
                self.stats.retries += 1
            self._throttle()
            self.stats.requests += 1
            try:
                if method.upper() == "POST":
                    response = self.session.post(url, data=payload, timeout=self.timeout)
                else:
                    response = self.session.get(url, params=payload, timeout=self.timeout)
            except requests.RequestException as exc:
                self.stats.network_errors += 1
                last_error = f"network error: {exc}"
                self._wait(self._backoff(attempt, None))
                continue

            retry_after = parse_retry_after(response.headers.get("Retry-After"))
            if response.status_code in self.retry_statuses:
                if response.status_code == 429:
                    self.stats.http_429 += 1
                else:
                    self.stats.http_5xx += 1
                last_error = f"HTTP {response.status_code}"
                self._wait(self._backoff(attempt, retry_after))
                continue
            if response.status_code >= 400:
                self.stats.failed += 1
                raise RuntimeError(f"HTTP {response.status_code} for {url}: {response.text[:200]}")

            try:
                document = response.json()
            except ValueError as exc:
                last_error = f"invalid JSON: {exc}"
                self._wait(self._backoff(attempt, retry_after))
                continue
            if not isinstance(document, dict):
                self.stats.failed += 1
                raise RuntimeError(f"Expected a JSON object from {url}")
            error = document.get("error")
            if error:
                code = str(error.get("code", "unknown")) if isinstance(error, dict) else "unknown"
                if code not in self.retry_api_errors:
                    self.stats.failed += 1
                    raise RuntimeError(f"API error {code} for {url}: {error}")
                if code == "maxlag":
                    self.stats.maxlag_waits += 1
                    retry_after = retry_after or float(self.maxlag_seconds)
                last_error = f"API error {code}"
                self._wait(self._backoff(attempt, retry_after))
                continue
            return document

        self.stats.failed += 1
        raise RuntimeError(f"Giving up on {url} after {self.max_retries} retries ({last_error})")

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self.session.close()


class RawCache:
    """Disk cache of raw API responses: ``<root>/<source>/<key>.json``.

    Each file is one compact JSON document on a single line (readable by Spark as
    JSON Lines) holding the request, the retrieval time and the raw response(s).

    Args:
        root: Cache root folder (``data/enrichment/raw``).
    """

    def __init__(self, root: str | os.PathLike[str]) -> None:
        self.root = Path(root)

    def path(self, source: str, key: str) -> Path:
        """Return the file of a cache entry."""
        return self.root / source / f"{key}.json"

    def has(self, source: str, key: str) -> bool:
        """Return whether the entry exists."""
        return self.path(source, key).is_file()

    def load(self, source: str, key: str) -> dict[str, Any] | None:
        """Return a cached record, or ``None`` when absent or unreadable."""
        path = self.path(source, key)
        if not path.is_file():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            LOGGER.warning("Ignoring unreadable cache file %s", path)
            return None

    def store(self, source: str, key: str, record: Mapping[str, Any]) -> Path:
        """Write a record atomically (temporary file then rename)."""
        path = self.path(source, key)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(".json.part")
        temporary.write_text(
            json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        os.replace(temporary, path)
        return path


def batch_key(prefix: str, ids: list[str]) -> str:
    """Return a stable cache key for a batch of identifiers."""
    digest = hashlib.sha1("|".join(ids).encode("utf-8")).hexdigest()[:16]  # noqa: S324
    return f"{prefix}_{digest}"


def utc_now() -> str:
    """Return the current UTC time as an ISO 8601 string (second precision)."""
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def fetch_cached(
    client: WikimediaClient | None,
    cache: RawCache,
    source: str,
    key: str,
    request: Mapping[str, Any],
    fetch: Callable[[], list[dict[str, Any]]],
    stats: ClientStats | None = None,
    refresh: bool = False,
) -> dict[str, Any]:
    """Return the cached record of a request, fetching it when needed.

    Args:
        client: Client used by ``fetch`` (only for its statistics).
        cache: Raw response cache.
        source: Cache sub-folder (one per kind of request).
        key: Cache key.
        request: Description of the request, stored with the response.
        fetch: Performs the request(s) and returns the raw response(s).
        stats: Statistics object when no client is given.
        refresh: Ignore an existing cache entry.

    Returns:
        The record: ``source``, ``key``, ``request``, ``retrieved_at``, ``responses``.
    """
    counters = stats or (client.stats if client else ClientStats())
    if not refresh:
        cached = cache.load(source, key)
        if cached is not None and not any(
            isinstance(response, Mapping) and response.get("error")
            for response in cached.get("responses", [])
        ):
            counters.cache_hits += 1
            return cached
    counters.cache_misses += 1
    record = {
        "source": source,
        "key": key,
        "request": dict(request),
        "retrieved_at": utc_now(),
        "responses": fetch(),
    }
    cache.store(source, key, record)
    return record
