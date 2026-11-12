from __future__ import annotations

import pytest

from imdb_project.enrichment import raw_reader
from imdb_project.enrichment.fetch_wikidata import SOURCE_SITELINKS
from imdb_project.enrichment.http_client import RawCache


def _cell(value, kind="literal"):
    return {"type": kind, "value": value}


def _row(imdb, item, wiki=None, title=None):
    row = {"imdb": _cell(imdb), "item": _cell(f"http://www.wikidata.org/entity/{item}", "uri")}
    if wiki:
        row["wiki"] = _cell(wiki, "uri")
        row["title"] = _cell(title)
    return row


def _store(cfg, key, bindings, retrieved_at="2026-11-10T20:00:00Z"):
    cache = RawCache(raw_reader.raw_source_path(cfg, "x").rsplit("/", 1)[0])
    cache.store(
        SOURCE_SITELINKS,
        key,
        {
            "source": SOURCE_SITELINKS,
            "key": key,
            "request": {"endpoint": "https://query.wikidata.org/sparql", "ids": ["tt1"]},
            "retrieved_at": retrieved_at,
            "responses": [{"head": {"vars": []}, "results": {"bindings": bindings}}],
        },
    )
    return cache


def test_sitelinks_and_items_from_cache(spark, cfg):
    _store(
        cfg,
        "batch_a",
        [
            _row("tt0000001", "Q100", "https://en.wikipedia.org/", "Alpha (film)"),
            _row("tt0000001", "Q100", "https://fr.wikipedia.org/", "Alpha (film, 1985)"),
            _row("tt0000002", "Q200"),  # item without any sitelink
            _row("nm0000001", "Q300", "https://zh-min-nan.wikipedia.org/", " Ada "),
        ],
    )
    _store(
        cfg,
        "batch_b",
        [
            # tt0000003 is carried by two items: the lowest id wins.
            _row("tt0000003", "Q999", "https://en.wikipedia.org/", "Newer duplicate"),
            _row("tt0000003", "Q50", "https://en.wikipedia.org/", "Gamma"),
        ],
    )

    items = {r.imdb_id: r for r in raw_reader.wikidata_items(spark, cfg).collect()}
    assert {k: v.qid for k, v in items.items()} == {
        "tt0000001": "Q100",
        "tt0000002": "Q200",
        "tt0000003": "Q50",
        "nm0000001": "Q300",
    }
    assert items["tt0000003"].n_items == 2 and items["tt0000001"].n_items == 1

    links = {(r.imdb_id, r.wiki): r for r in raw_reader.sitelinks(spark, cfg).collect()}
    assert set(links) == {
        ("tt0000001", "enwiki"),
        ("tt0000001", "frwiki"),
        ("tt0000003", "enwiki"),
        ("nm0000001", "zh_min_nanwiki"),
    }
    assert links[("tt0000003", "enwiki")].page_title == "Gamma"
    assert links[("nm0000001", "zh_min_nanwiki")].page_title == "Ada"
    assert links[("tt0000001", "enwiki")].retrieved_at == "2026-11-10T20:00:00Z"


def test_corrupt_cache_files_are_controlled(spark, cfg):
    cache = _store(cfg, "batch_a", [_row("tt0000001", "Q100")])
    cache.path(SOURCE_SITELINKS, "broken").write_text("{not json\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="corrupt cache record"):
        raw_reader.read_sparql_bindings(spark, cfg, SOURCE_SITELINKS)
    tolerant = cfg.with_overrides({"enrichment.max_corrupt_records": 1})
    assert raw_reader.read_sparql_bindings(spark, tolerant, SOURCE_SITELINKS).count() == 1


def test_missing_cache_is_reported(spark, cfg):
    with pytest.raises(FileNotFoundError, match="run the collection step first"):
        raw_reader.read_sparql_bindings(spark, cfg, SOURCE_SITELINKS)
