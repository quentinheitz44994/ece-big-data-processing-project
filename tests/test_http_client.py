from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import pytest

from fakes import FakeResponse, FakeSession, make_client
from imdb_project.enrichment import fetch_wikidata, http_client

API = "https://en.wikipedia.org/w/api.php"
SPARQL = "https://query.wikidata.org/sparql"
WIKIPEDIA_ROBOTS = "User-agent: *\nAllow: /w/api.php?action=mobileview&\nDisallow: /w/\n"


def test_user_agent_requires_a_contact(cfg):
    with pytest.raises(http_client.MissingContactError, match="WIKIMEDIA_CONTACT_EMAIL"):
        http_client.build_user_agent(cfg.with_overrides({"wikimedia.contact": ""}).wikimedia)
    agent = http_client.build_user_agent(
        cfg.with_overrides({"wikimedia.contact": "someone@example.org"}).wikimedia
    )
    assert agent.startswith("ECE-BigData-IMDb-Project/1.0 (someone@example.org) python-requests/")


def test_parse_retry_after():
    now = dt.datetime(2026, 11, 10, 12, 0, 0, tzinfo=dt.UTC)
    assert http_client.parse_retry_after("7") == 7.0
    assert http_client.parse_retry_after(" 0.5 ") == 0.5
    assert http_client.parse_retry_after("Tue, 10 Nov 2026 12:00:30 GMT", now) == 30.0
    assert http_client.parse_retry_after("Tue, 10 Nov 2026 11:00:00 GMT", now) == 0.0
    assert http_client.parse_retry_after("soon") is None
    assert http_client.parse_retry_after(None) is None


def test_requests_are_sequential_and_rate_limited(cfg):
    client, session, clock = make_client(cfg, max_requests_per_second=0.5)
    session.script(API, FakeResponse({"ok": 1}), FakeResponse({"ok": 2}), FakeResponse({"ok": 3}))
    assert client.request_json(API, {"action": "query"}) == {"ok": 1}
    assert client.request_json(API, {"action": "query"}) == {"ok": 2}
    clock.now += 5  # a slow caller does not have to wait again
    assert client.request_json(API, {"action": "query"}) == {"ok": 3}
    # 2 s between the robots.txt fetch, request 1 and request 2; none before request 3.
    assert clock.sleeps == [2.0, 2.0]
    assert session.headers["User-Agent"].startswith(
        "ECE-BigData-IMDb-Project/1.0 (tests@example.org)"
    )
    assert client.stats.requests == 3


def test_maxlag_parameter_and_retry(cfg):
    client, session, clock = make_client(cfg)
    lagged = FakeResponse(
        {"error": {"code": "maxlag", "info": "lagged"}}, headers={"Retry-After": "9"}
    )
    session.script(API, lagged, FakeResponse({"query": {}}))
    assert client.request_json(API, {"action": "query"}, use_maxlag=True) == {"query": {}}
    assert [call[2]["maxlag"] for call in session.calls] == [5, 5]
    assert client.stats.maxlag_waits == 1 and client.stats.retries == 1
    assert 9.0 in clock.sleeps


def test_retry_after_and_backoff_on_429_and_503(cfg):
    client, session, clock = make_client(cfg, backoff_base_seconds=2.0)
    session.script(
        SPARQL,
        FakeResponse(status_code=429, headers={"Retry-After": "30"}),
        FakeResponse(status_code=503),
        FakeResponse({"results": {"bindings": []}}),
    )
    assert client.request_json(SPARQL, {"query": "x"}, method="POST")["results"] == {"bindings": []}
    assert (client.stats.http_429, client.stats.http_5xx, client.stats.retries) == (1, 1, 2)
    assert 30.0 in clock.sleeps  # Retry-After honoured
    assert 4.0 in clock.sleeps  # exponential back-off on the second attempt (2 * 2**1)
    assert all(call[0] == "POST" for call in session.calls)


def test_gives_up_after_max_retries_and_fails_fast_on_client_errors(cfg):
    client, session, _ = make_client(cfg, max_retries=2)
    session.script(SPARQL, lambda *_: FakeResponse(status_code=503))
    with pytest.raises(RuntimeError, match="Giving up"):
        client.request_json(SPARQL, {"query": "x"})
    assert client.stats.requests == 3 and client.stats.failed == 1

    session.script(API, FakeResponse(status_code=400, text="bad request"))
    with pytest.raises(RuntimeError, match="HTTP 400"):
        client.request_json(API, {})
    assert len([call for call in session.calls if call[1] == API]) == 1


def test_robots_verdict_is_reported_or_enforced(cfg):
    session = FakeSession(robots={"en.wikipedia.org": WIKIPEDIA_ROBOTS})
    client, session, _ = make_client(cfg, session)
    session.script(API, FakeResponse({"ok": 1}), FakeResponse({"ok": 2}))
    assert client.request_json(API, {}) == {"ok": 1}  # "report": proceeds
    assert client.request_json(API, {}) == {"ok": 2}
    assert client.stats.robots == {"en.wikipedia.org/w/api.php": "disallowed"}
    assert client.check_robots("https://en.wikipedia.org/wiki/Some_page") is True

    strict, strict_session, _ = make_client(
        cfg,
        FakeSession(robots={"en.wikipedia.org": WIKIPEDIA_ROBOTS}),
        **{"robots.policy": "enforce"},
    )
    with pytest.raises(http_client.RobotsDisallowedError):
        strict.request_json(API, {})
    assert strict_session.calls == []  # nothing was requested

    unknown, unknown_session, _ = make_client(cfg)
    unknown_session.script(SPARQL, FakeResponse({"ok": 1}))
    unknown.request_json(SPARQL, {})
    assert unknown.stats.robots == {"query.wikidata.org/sparql": "unavailable"}


def test_raw_cache_roundtrip_and_fetch_cached(tmp_path):
    cache = http_client.RawCache(tmp_path / "raw")
    calls = []

    def fetch():
        calls.append(1)
        return [{"value": "é"}]

    stats = http_client.ClientStats()
    first = http_client.fetch_cached(None, cache, "src", "k1", {"ids": ["a"]}, fetch, stats)
    second = http_client.fetch_cached(None, cache, "src", "k1", {"ids": ["a"]}, fetch, stats)
    assert first == second and len(calls) == 1
    assert (stats.cache_misses, stats.cache_hits) == (1, 1)
    assert first["request"] == {"ids": ["a"]} and first["retrieved_at"].endswith("Z")

    path = cache.path("src", "k1")
    text = path.read_text(encoding="utf-8")
    assert text.count("\n") == 1 and json.loads(text)["responses"] == [{"value": "é"}]
    assert not list(path.parent.glob("*.part"))

    http_client.fetch_cached(None, cache, "src", "k1", {}, fetch, stats, refresh=True)
    assert len(calls) == 2
    path.write_text("{broken", encoding="utf-8")
    assert cache.load("src", "k1") is None
    assert http_client.batch_key("p", ["a", "b"]) == http_client.batch_key("p", ["a", "b"])
    assert http_client.batch_key("p", ["a", "b"]) != http_client.batch_key("p", ["a", "c"])


def test_sparql_queries_validate_identifiers():
    query = fetch_wikidata.sitelinks_query(["tt0000001", "nm0000002"], ["enwiki", "frwiki"])
    assert 'VALUES ?imdb { "tt0000001" "nm0000002" }' in query
    assert "<https://en.wikipedia.org/>, <https://fr.wikipedia.org/>" in query
    assert "wdt:P345" in query
    assert "wdt:P364" in fetch_wikidata.film_languages_query(["tt0000001"])
    facts = fetch_wikidata.person_facts_query(["nm0000002"])
    assert all(prop in facts for prop in ("wdt:P569", "wdt:P570", "wdt:P19", "wdt:P27"))
    with pytest.raises(ValueError, match="Not IMDb identifiers"):
        fetch_wikidata.sitelinks_query(['tt1" } UNION { ?s ?p ?o'], ["enwiki"])
    with pytest.raises(ValueError, match="Unsupported wiki"):
        fetch_wikidata.wiki_site_url("en.wikipedia.org/evil")
    assert fetch_wikidata.wiki_site_url("zh_min_nanwiki") == "https://zh-min-nan.wikipedia.org/"


def _sparql_handler(method, url, payload):
    ids = [part.strip('"') for part in payload["query"].split("{", 2)[2].split("}")[0].split()]
    bindings = [
        {
            "imdb": {"type": "literal", "value": imdb_id},
            "item": {"type": "uri", "value": f"http://www.wikidata.org/entity/Q{imdb_id[2:]}"},
            "wiki": {"type": "uri", "value": "https://en.wikipedia.org/"},
            "title": {"type": "literal", "value": f"Page of {imdb_id}"},
        }
        for imdb_id in ids
        if not imdb_id.endswith("9")  # identifiers ending with 9 are unknown to Wikidata
    ]
    return FakeResponse(
        {"head": {"vars": ["imdb", "item", "wiki", "title"]}, "results": {"bindings": bindings}}
    )


def test_collect_batches_caches_and_records_stats(cfg):
    cfg = cfg.with_overrides({"wikimedia.sparql_batch_size": 2})
    ids = ["tt0000003", "tt0000001", "tt0000002", "tt0000009", "tt0000001"]
    client, session, _ = make_client(cfg)
    session.script(SPARQL, _sparql_handler)

    records = fetch_wikidata.collect(cfg, "sitelinks", ids, "test-step", client=client)
    assert len(records) == 2 and len(session.calls) == 2  # 4 distinct ids, batches of 2
    assert records[0]["request"]["ids"] == ["tt0000001", "tt0000002"]
    rows = [row for record in records for row in fetch_wikidata.iter_bindings(record)]
    assert sorted(row["imdb"] for row in rows) == ["tt0000001", "tt0000002", "tt0000003"]
    assert rows[0]["title"].startswith("Page of ")

    again, again_session, _ = make_client(cfg)
    fetch_wikidata.collect(cfg, "sitelinks", ids, "test-step", client=again)
    assert again_session.calls == []  # everything served from the cache
    assert again.stats.cache_hits == 2

    stats_file = Path(cfg.paths.enrichment, "stats", "collection_runs.jsonl")
    runs = [json.loads(line) for line in stats_file.read_text("utf-8").splitlines()]
    assert [run["requests"] for run in runs] == [2, 0]
    assert runs[0]["ids_requested"] == 4 and runs[0]["ids_found_in_wikidata"] == 3
    assert runs[0]["robots"] == {"query.wikidata.org/sparql": "unavailable"}
    cached = sorted(Path(cfg.paths.enrichment, "raw", "wikidata_sitelinks").glob("*.json"))
    assert len(cached) == 2
