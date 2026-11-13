from __future__ import annotations

import json

import pytest

from helpers import movie, principal, rating, silver_df
from imdb_project.streaming import build_lookup, producer, relevance
from streaming_fakes import FakeKafkaProducer, change

LOOKUP_SCHEMA = (
    "wiki string, page_title_normalized string, imdb_id string, entity_type string, "
    "qid string, source_url string"
)


# -------------------------------------------------------------------- producer


def test_iter_sse_events_parses_fields_comments_and_multiline_data():
    lines = [
        ":ok",
        "",
        "event: message",
        'id: [{"topic":"eqiad.mediawiki.recentchange","partition":0,"offset":1}]',
        b'data: {"a": 1}',
        "",
        "data: first",
        "data:second",
        "",
        "event: ping",
        "",
    ]
    events = list(producer.iter_sse_events(lines))
    assert [(e.event, e.data) for e in events] == [
        ("message", '{"a": 1}'),
        ("message", "first\nsecond"),
    ]
    assert events[0].id.startswith('[{"topic"') and events[1].id is None


def test_keep_event_filter():
    def keep(event):
        return producer.keep_event(event, {"enwiki", "frwiki"}, {"edit", "new"}, {0})

    assert keep(change("1", "A", "2026-11-10T12:00:00Z"))
    assert keep(change("2", "A", "2026-11-10T12:00:00Z", wiki="frwiki", kind="new"))
    assert not keep(change("3", "A", "2026-11-10T12:00:00Z", wiki="dewiki"))
    assert not keep(change("4", "A", "2026-11-10T12:00:00Z", kind="log"))
    assert not keep(change("5", "Talk:A", "2026-11-10T12:00:00Z", ns=1))
    assert not keep({"wiki": "enwiki", "type": "edit", "namespace": 0, "meta": {}})


class _StreamResponse:
    status_code = 200

    def __init__(self, lines):
        self._lines = lines

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def raise_for_status(self):
        return None

    def iter_lines(self):
        return iter(self._lines)


class _StreamSession:
    def __init__(self, lines):
        self.headers, self.requests, self._lines = {}, [], lines
        self.closed = False

    def get(self, url, **kwargs):
        if url.endswith("/robots.txt"):
            return type(
                "Robots", (), {"status_code": 200, "text": "User-agent: *\nDisallow: /\n"}
            )()
        self.requests.append(kwargs.get("headers", {}))
        lines, self._lines = self._lines, []
        return _StreamResponse(lines)

    def close(self):
        self.closed = True


def _one_event_session():
    event = change("id-1", "Alpha (film)", "2026-11-10T12:00:00Z")
    return _StreamSession(["id: offset-1", "data: " + json.dumps(event), ""])


def test_producer_retries_the_same_event_when_the_queue_is_full(cfg):
    stop = producer.StopFlag()

    class SaturatedProducer(FakeKafkaProducer):
        attempts = 0

        def produce(self, *args, **kwargs):
            self.attempts += 1
            if self.attempts <= 2:
                raise BufferError("Local: Queue full")
            super().produce(*args, **kwargs)

        def poll(self, timeout):
            if timeout == 0:
                stop.request()

    kafka, session = SaturatedProducer(), _one_event_session()
    stats = producer.run(
        cfg.with_overrides({"wikimedia.contact": "tests@example.org"}),
        duration_minutes=0,
        kafka_producer=kafka,
        http_session=session,
        stop=stop,
    )
    assert kafka.attempts == 3 and len(kafka.messages) == stats.produced == 1
    assert kafka.messages[0][1] == b"id-1"
    assert kafka.flushed and session.closed


def test_producer_can_stop_while_its_queue_remains_full(cfg):
    stop = producer.StopFlag()

    class BlockedProducer(FakeKafkaProducer):
        def produce(self, *args, **kwargs):
            raise BufferError("Local: Queue full")

        def poll(self, timeout):
            stop.request()

    kafka, session = BlockedProducer(), _one_event_session()
    stats = producer.run(
        cfg.with_overrides({"wikimedia.contact": "tests@example.org"}),
        duration_minutes=0,
        kafka_producer=kafka,
        http_session=session,
        stop=stop,
    )
    assert stats.produced == 0 and kafka.flushed and session.closed


def test_producer_flushes_and_records_stats_after_an_unexpected_error(cfg, tmp_path):
    class BrokenProducer(FakeKafkaProducer):
        def produce(self, *args, **kwargs):
            raise RuntimeError("Unexpected Kafka failure")

    kafka, session = BrokenProducer(), _one_event_session()
    stats_path = tmp_path / "producer.json"
    configured = cfg.with_overrides(
        {
            "wikimedia.contact": "tests@example.org",
            "streaming.producer.stats_path": str(stats_path),
        }
    )
    with pytest.raises(RuntimeError, match="Unexpected Kafka failure"):
        producer.run(configured, 0, kafka_producer=kafka, http_session=session)
    assert kafka.flushed and session.closed
    assert json.loads(stats_path.read_text())["finished_at"] is not None


def test_producer_reports_records_left_after_flush(cfg, tmp_path):
    stop = producer.StopFlag()

    class UndeliveredProducer(FakeKafkaProducer):
        def poll(self, timeout):
            stop.request()

        def flush(self, timeout):
            self.flushed = True
            return 2

    kafka, session = UndeliveredProducer(), _one_event_session()
    stats_path = tmp_path / "producer.json"
    configured = cfg.with_overrides(
        {
            "wikimedia.contact": "tests@example.org",
            "streaming.producer.stats_path": str(stats_path),
        }
    )
    with pytest.raises(RuntimeError, match="2 undelivered"):
        producer.run(configured, 0, kafka_producer=kafka, http_session=session, stop=stop)
    assert json.loads(stats_path.read_text())["undelivered"] == 2
    assert kafka.flushed and session.closed


def test_producer_publishes_raw_json_keyed_by_event_id(cfg, tmp_path):
    kept = change("id-1", "Alpha (film)", "2026-11-10T12:00:00Z")
    lines = []
    for index, payload in enumerate(
        [
            json.dumps(kept),
            json.dumps(change("id-2", "Beta", "2026-11-10T12:00:01Z", wiki="dewiki")),
            "{not json",
        ]
    ):
        lines += [f"id: offset-{index}", f"data: {payload}", ""]
    cfg = cfg.with_overrides(
        {
            "wikimedia.contact": "tests@example.org",
            "streaming.producer.reconnect_delay_seconds": 0,
            "streaming.producer.stats_path": str(tmp_path / "stats" / "producer.json"),
        }
    )
    kafka, session = FakeKafkaProducer(), _StreamSession(lines)
    stats = producer.run(cfg, duration_minutes=0.002, kafka_producer=kafka, http_session=session)

    assert (stats.received, stats.produced, stats.filtered_out, stats.invalid) == (2, 1, 1, 1)
    topic, key, value = kafka.messages[0]
    assert (topic, key) == (cfg.kafka.topic, b"id-1")
    assert json.loads(value) == kept and value == json.dumps(kept).encode("utf-8")
    assert kafka.flushed
    assert session.headers["User-Agent"].startswith(
        "ECE-BigData-IMDb-Project/1.0 (tests@example.org)"
    )
    assert "Last-Event-ID" not in session.requests[0]
    assert session.requests[1]["Last-Event-ID"] == "offset-2"  # resumes after the last event seen
    assert stats.robots == {"stream.wikimedia.org/v2/stream/recentchange": "disallowed"}
    assert json.loads((tmp_path / "stats" / "producer.json").read_text())["produced"] == 1

    strict = cfg.with_overrides({"wikimedia.robots.policy": "enforce"})
    with pytest.raises(Exception, match="robots.txt disallows"):
        producer.run(
            strict, 0.001, kafka_producer=FakeKafkaProducer(), http_session=_StreamSession([])
        )


# ------------------------------------------------------------------- relevance


def test_title_patterns_and_normalisation(spark, cfg):
    patterns = relevance.title_patterns(cfg)
    titles = {
        "Alpha (film)": "film",
        "Alpha_(2010_film)": "film",
        "Alpha (1999 American film)": "film",
        "Alpha (film, 2010)": "film",
        "Beta (TV series)": "tv_series",
        "Beta (American TV series)": "tv_series",
        "Beta (miniseries)": "tv_series",
        "Beta (série télévisée)": "tv_series",
        "Ada Alpha (actress)": "person",
        "Bob Beta (English actor)": "person",
        "Cy Gamma (director)": "person",
        "Di Delta (réalisatrice)": "person",
        "Film": None,
        "List of films (disambiguation)": None,
        "The Actor": None,
    }
    df = spark.createDataFrame([(title,) for title in titles], "title string")
    rows = df.select(
        "title",
        relevance.pattern_entity_type(relevance.normalize_title("title"), patterns).alias("kind"),
    ).collect()
    assert {r.title: r.kind for r in rows} == titles
    assert relevance.normalize_title_text("  Alpha_(2010_film) ") == "Alpha (2010 film)"
    assert relevance.matches_any_pattern("Alpha (2010 film)", patterns)
    assert not relevance.matches_any_pattern("Alpha", patterns)


def test_flag_relevant_lookup_or_pattern(spark, cfg):
    lookup = spark.createDataFrame(
        [
            (
                "enwiki",
                "Alpha (film)",
                "tt1",
                "film",
                "Q1",
                "https://en.wikipedia.org/wiki/Alpha_(film)",
            ),
            (
                "enwiki",
                "Ada Alpha",
                "nm1",
                "person",
                "Q2",
                "https://en.wikipedia.org/wiki/Ada_Alpha",
            ),
            ("frwiki", "Gamma", "tt3", "tv_series", "Q3", "https://fr.wikipedia.org/wiki/Gamma"),
        ],
        LOOKUP_SCHEMA,
    )
    events = spark.createDataFrame(
        [
            ("e1", "enwiki", "Alpha_(film)"),  # in the lookup and matching a pattern
            ("e2", "enwiki", "Ada Alpha"),  # lookup only
            ("e3", "enwiki", "Unknown (TV series)"),  # pattern only
            ("e4", "enwiki", "Gamma"),  # the lookup entry is for frwiki
            ("e5", "frwiki", "Gamma"),
            ("e6", "enwiki", "Paris"),
        ],
        "event_id string, wiki string, title string",
    )
    rows = {
        r.event_id: r
        for r in relevance.flag_relevant(events, lookup, relevance.title_patterns(cfg)).collect()
    }
    assert {k: (v.match_reason, v.entity_type, v.imdb_id) for k, v in rows.items()} == {
        "e1": ("lookup+title_pattern", "film", "tt1"),
        "e2": ("lookup", "person", "nm1"),
        "e3": ("title_pattern", "tv_series", None),
        "e5": ("lookup", "tv_series", "tt3"),
    }
    assert rows["e1"].page_title_normalized == "Alpha (film)"
    assert rows["e1"].lookup_source_url.endswith("Alpha_(film)")


# ---------------------------------------------------------------------- lookup


def test_lookup_scope_and_table(spark):
    titles = silver_df(
        spark,
        "title_basics",
        [
            movie("tt1", 2000, 100, ["Drama"]),
            movie("tt2", 2001, 100, ["Drama"], title_type="tvSeries"),
            movie("tt3", 2002, 100, ["Drama"], title_type="tvEpisode"),  # type not kept
            movie("tt4", 2003, 100, ["Drama"]),
        ],
    )
    ratings = silver_df(
        spark,
        "title_ratings",
        [
            rating("tt1", 8.0, 900),
            rating("tt2", 8.0, 500),
            rating("tt3", 8.0, 999),
            rating("tt4", 8.0, 10),
        ],
    )
    types = {"movie": "film", "tvSeries": "tv_series"}
    top = build_lookup.top_titles(titles, ratings, types, 2).collect()
    assert [(r.imdb_id, r.entity_type, r.score) for r in top] == [
        ("tt1", "film", 900),
        ("tt2", "tv_series", 500),
    ]
    assert build_lookup.top_titles(titles, ratings, types, None).count() == 3

    principals = silver_df(
        spark,
        "title_principals",
        [
            principal("tt1", 1, "nm1", "actor"),
            principal("tt2", 1, "nm1", "actor"),
            principal("tt2", 2, "nm2", "director"),
            principal("tt1", 3, "nm3", "producer"),  # category not kept
        ],
    )
    scored = build_lookup.top_titles(titles, ratings, types, 2)
    people = build_lookup.top_people(principals, scored, ["actor", "director"], 5).collect()
    assert [(r.imdb_id, r.entity_type, r.score) for r in people] == [
        ("nm1", "person", 1400),
        ("nm2", "person", 500),
    ]

    links = spark.createDataFrame(
        [
            ("tt1", "Q1", "enwiki", "Alpha_(film)"),
            ("tt1", "Q1", "frwiki", "Alpha (film, 2000)"),
            ("tt1", "Q1", "dewiki", "Alpha (Film)"),  # wiki not followed
            ("nm1", "Q9", "enwiki", "Shared page"),
            ("tt2", "Q2", "enwiki", "Shared page"),  # a title wins over a person
            ("tt9", "Q8", "enwiki", "Out of scope"),
        ],
        "imdb_id string, qid string, wiki string, page_title string",
    )
    entities = spark.createDataFrame(
        [("tt1", "film"), ("tt2", "tv_series"), ("nm1", "person")],
        "imdb_id string, entity_type string",
    )
    table = build_lookup.build_lookup_table(links, entities, ["enwiki", "frwiki"]).collect()
    rows = {(r.wiki, r.page_title_normalized): r for r in table}
    assert set(rows) == {
        ("enwiki", "Alpha (film)"),
        ("frwiki", "Alpha (film, 2000)"),
        ("enwiki", "Shared page"),
    }
    assert rows[("enwiki", "Shared page")].imdb_id == "tt2"
    assert (
        rows[("enwiki", "Alpha (film)")].source_url == "https://en.wikipedia.org/wiki/Alpha_(film)"
    )
    assert (
        rows[("frwiki", "Alpha (film, 2000)")].source_url
        == "https://fr.wikipedia.org/wiki/Alpha_(film,_2000)"
    )
