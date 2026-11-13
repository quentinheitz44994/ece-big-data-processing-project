from __future__ import annotations

import json
from pathlib import Path

import pytest

from fakes import FakeResponse, FakeSession, make_client
from helpers import movie, person, principal, rating, silver_df, write_silver
from imdb_project.common import io
from imdb_project.enrichment import build_enrichment, fetch_wikipedia, select_scope

SPARQL = "https://query.wikidata.org/sparql"
API = "https://en.wikipedia.org/w/api.php"
ENTITY = "http://www.wikidata.org/entity/"
ROBOTS = {
    "en.wikipedia.org": "User-agent: *\nDisallow: /w/\n",
    "query.wikidata.org": "User-agent: *\nDisallow: /sparql\n",
}

LONG_PLOT = "A retired sailor returns to the harbour town of his youth. " * 6

FILM_PAGES = {
    "Alpha (film)": {
        "pageid": 11,
        "title": "Alpha (film)",
        "extract": (
            "Alpha is a 2000 drama film.\n\n\n== Plot ==\n"
            + LONG_PLOT
            + "[1]\n\n=== Act two ===\nHe  buys   a boat.[citation needed]\n\n\n== Cast ==\nAda Alpha"
        ),
        "revid": 1001,
    },
    "Beta (film)": {
        "pageid": 12,
        "title": "Beta (film)",
        "extract": "Beta is a 2000 film directed by nobody.\n\n\n== Cast ==\nAda Alpha",
        "revid": 1002,
    },
    "Zeta (2000 film)": {
        "pageid": 16,
        "title": "Zeta (2000 film)",
        "extract": "Zeta is a film.\n\n\n== Synopsis ==\nShort synopsis.\n\n\n== Reception ==\nGood.",
        "revid": 1006,
    },
}
REDIRECTS = {"Zeta (film)": "Zeta (2000 film)"}

FILM_ITEMS = {  # tconst: (qid, {wiki site: title})
    "tt0000001": ("Q1", {"https://en.wikipedia.org/": "Alpha (film)"}),
    "tt0000002": ("Q2", {"https://en.wikipedia.org/": "Beta (film)"}),
    "tt0000003": ("Q3", {"https://fr.wikipedia.org/": "Gamma (film)"}),
    "tt0000005": ("Q5", {"https://en.wikipedia.org/": "Epsilon (film)"}),
    "tt0000006": ("Q6", {"https://en.wikipedia.org/": "Zeta (film)"}),
    "nm0000001": ("Q101", {"https://en.wikipedia.org/": "Ada Alpha"}),
    "nm0000002": ("Q102", {}),
}
PERSON_FACTS = {
    "nm0000001": ("Q101", "1950-01-02T00:00:00Z", None, "Lyon", ["France", "Canada"]),
    "nm0000002": ("Q102", "1960-05-06T00:00:00Z", "2020-07-08T00:00:00Z", None, []),
}


def _cell(value, kind="literal"):
    return {"type": kind, "value": value}


def _sparql(method, url, payload):
    query = payload["query"]
    bindings = []
    if "schema:about" in query:
        for imdb_id, (qid, links) in FILM_ITEMS.items():
            if f'"{imdb_id}"' not in query:
                continue
            base = {"imdb": _cell(imdb_id), "item": _cell(ENTITY + qid, "uri")}
            if not links:
                bindings.append(base)
            for site, title in links.items():
                bindings.append({**base, "wiki": _cell(site, "uri"), "title": _cell(title)})
    else:
        for imdb_id, (qid, birth, death, place, countries) in PERSON_FACTS.items():
            if f'"{imdb_id}"' not in query:
                continue
            base = {
                "imdb": _cell(imdb_id),
                "item": _cell(ENTITY + qid, "uri"),
                "birthDate": _cell(birth),
            }
            if death:
                base["deathDate"] = _cell(death)
            if place:
                base["birthPlaceLabel"] = _cell(place)
            for country in countries or [None]:
                row = dict(base)
                if country:
                    row["citizenshipLabel"] = _cell(country)
                bindings.append(row)
    return FakeResponse({"results": {"bindings": bindings}})


def _page(spec, with_extract=True):
    title = spec["title"]
    page = {
        "pageid": spec["pageid"],
        "ns": 0,
        "title": title,
        "canonicalurl": "https://en.wikipedia.org/wiki/" + title.replace(" ", "_"),
        "lastrevid": spec["revid"],
        "revisions": [{"revid": spec["revid"], "parentid": 1, "timestamp": "2026-10-01T10:00:00Z"}],
    }
    if with_extract:
        page["extract"] = spec["extract"]
    return page


def _wikipedia(method, url, payload):
    assert payload["maxlag"] == 5 and payload["action"] == "query"
    titles = [title for title in payload["titles"].split("\u001f") if title]
    if "exintro" in payload:
        assert titles == ["Ada Alpha"]
        spec = {
            "pageid": 201,
            "title": "Ada Alpha",
            "revid": 2001,
            "extract": "Ada Alpha (born 2 January 1950) is a French-Canadian actress known for stage and screen work. "
            * 2,
        }
        if "excontinue" not in payload:  # first response: the extract comes with the continuation
            return FakeResponse(
                {
                    "continue": {"excontinue": 1, "continue": "||revisions|info"},
                    "query": {"pages": [_page(spec, False)]},
                }
            )
        return FakeResponse({"batchcomplete": True, "query": {"pages": [_page(spec)]}})
    (title,) = titles
    query = {}
    if title in REDIRECTS:
        query["redirects"] = [{"from": title, "to": REDIRECTS[title]}]
        title = REDIRECTS[title]
    if title in FILM_PAGES:
        query["pages"] = [_page(FILM_PAGES[title])]
    else:
        query["pages"] = [{"ns": 0, "title": title, "missing": True}]
    return FakeResponse({"batchcomplete": True, "query": query})


def _films_df(spark):
    rows = [
        ("t1", "A", "A", 2000, ["Drama", "Comedy"], 8.0, 900),
        ("t2", "B", "B", 2000, ["Drama"], 7.0, 800),
        ("t3", "C", "C", 2000, ["Comedy"], 9.0, 800),
        ("t4", "D", "D", 2001, ["Drama"], 5.0, 100),
        ("t5", "E", "E", 1970, ["Drama"], 5.0, 999),
        ("t6", "F", "F", None, ["Drama"], 5.0, 999),
    ]
    return spark.createDataFrame(
        rows,
        "tconst string, primaryTitle string, originalTitle string, startYear int, "
        "genres array<string>, averageRating double, numVotes int",
    )


def test_scope_films_top_n_per_genre_and_year(spark):
    scoped = select_scope.scope_films(
        _films_df(spark), 1980, 2025, 1, ["numVotes", "averageRating"]
    )
    rows = {r.tconst: r for r in scoped.collect()}
    assert set(rows) == {"t1", "t4"}  # t1 tops Drama 2000 and Comedy 2000; t4 tops Drama 2001
    assert [(s.genre, s.year, s.rank) for s in rows["t1"].selections] == [
        ("Comedy", 2000, 1),
        ("Drama", 2000, 1),
    ]

    two = select_scope.scope_films(_films_df(spark), 1980, 2025, 2, ["numVotes", "averageRating"])
    ranks = {r.tconst: r.best_rank for r in two.collect()}
    assert ranks == {"t1": 1, "t2": 2, "t3": 2, "t4": 1}

    # Ranking column order matters: by rating first, t3 tops Comedy 2000.
    by_rating = select_scope.scope_films(_films_df(spark), 1980, 2025, 1, ["averageRating"])
    assert {r.tconst for r in by_rating.collect()} == {"t1", "t3", "t4"}

    # No restriction at all: every dated film of the dataset.
    everything = select_scope.scope_films(_films_df(spark), None, None, None, ["numVotes"])
    assert {r.tconst for r in everything.collect()} == {"t1", "t2", "t3", "t4", "t5"}


def test_scope_people_first_principals(spark):
    films = spark.createDataFrame([("t1",), ("t2",)], "tconst string")
    principals = silver_df(
        spark,
        "title_principals",
        [
            principal("t1", 1, "nm1", "producer"),  # category not kept
            principal("t1", 2, "nm2", "actor"),
            principal("t1", 3, "nm2", "writer"),  # same person, second credit
            principal("t1", 4, "nm3", "director"),
            principal("t1", 5, "nm4", "actress"),
            principal("t1", 6, "nm5", "actor"),
            principal("t2", 1, "nm2", "actor"),
            principal("t9", 1, "nm9", "actor"),  # film outside the scope
        ],
    )
    categories = ["actor", "actress", "director", "writer"]
    people = select_scope.scope_people(principals, films, categories, 3).collect()
    assert sorted((r.tconst, r.rank_in_film, r.nconst) for r in people) == [
        ("t1", 1, "nm2"),
        ("t1", 2, "nm3"),
        ("t1", 3, "nm4"),
        ("t2", 1, "nm2"),
    ]
    nm2 = next(r for r in people if r.tconst == "t1" and r.nconst == "nm2")
    assert (nm2.ordering, nm2.categories) == (2, ["actor", "writer"])
    unrestricted = select_scope.scope_people(principals, films, None, None)
    assert unrestricted.where("tconst = 't1'").count() == 5


def test_text_cleaning_and_section_extraction(spark):
    extract = (
        "Lead paragraph.[1]\n\nSecond lead paragraph.\n\n\n== Production ==\nShot in 1999.\n\n\n"
        "== plot summary ==\nFirst part.[2]\n\n=== Ending ===\nSecond\u00a0part.[citation needed]\n\n\n"
        "== Cast ==\nSomebody"
    )
    df = spark.createDataFrame(
        [(extract,), (None,), ("== Plot ==\n   \n== Cast ==\nx",)], "extract string"
    )
    rows = df.select(
        build_enrichment.clean_text(build_enrichment.section_text("extract", "Plot summary")).alias(
            "plot"
        ),
        build_enrichment.clean_text(build_enrichment.section_text("extract", "Plot")).alias(
            "exact"
        ),
        build_enrichment.clean_text(build_enrichment.lead_text("extract")).alias("lead"),
    ).collect()
    assert rows[0].plot == "First part. Second part."
    assert rows[0].exact is None  # "Plot" does not match the heading "plot summary"
    assert rows[0].lead == "Lead paragraph. Second lead paragraph."
    assert (rows[1].plot, rows[1].lead) == (None, None)
    assert rows[2].exact is None  # empty section


@pytest.fixture()
def enrichment_cfg(spark, cfg):
    titles = [
        movie(f"tt000000{i}", 2000, 100, ["Drama"], title=name)
        for i, name in enumerate(["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta"], start=1)
    ]
    titles.append(movie("tt0000007", 1975, 100, ["Drama"], title="Too old"))
    write_silver(spark, cfg, "title_basics", titles)
    write_silver(
        spark,
        cfg,
        "title_ratings",
        [rating(f"tt000000{i}", 7.0, 1000 * (10 - i)) for i in range(1, 8)],
    )
    principals = []
    for i in range(1, 7):
        tconst = f"tt000000{i}"
        principals += [
            principal(tconst, 1, "nm0000001", "actress"),
            principal(tconst, 2, "nm0000002", "director"),
            principal(tconst, 3, "nm0000003", "writer"),
            principal(tconst, 4, "nm0000004", "actor"),
        ]
    write_silver(spark, cfg, "title_principals", principals)
    write_silver(
        spark,
        cfg,
        "name_basics",
        [
            person("nm0000001", "Ada Alpha", 1950),
            person("nm0000002", "Bob Beta", 1960, 2020),
            person("nm0000003", "Cy Gamma"),
        ],
    )
    return cfg


def test_enrichment_pipeline_end_to_end(spark, enrichment_cfg):
    cfg = enrichment_cfg
    films_scope, people_scope = select_scope.run(spark, cfg)
    assert films_scope.count() == 6 and people_scope.count() == 18
    assert people_scope.select("nconst").distinct().count() == 3
    assert "| distinct films | 6 |" in Path(cfg.paths.outputs, "enrichment", "scope.md").read_text(
        "utf-8"
    )

    client, session, _ = make_client(cfg, FakeSession(robots=ROBOTS))
    session.script(SPARQL, _sparql)
    session.script(API, _wikipedia)
    counters = fetch_wikipedia.run(cfg, client=client)
    assert counters == {"films": 6, "people": 3, "films_with_page": 4, "people_with_page": 1}
    api_calls = [call for call in session.calls if call[1] == API]
    assert len(api_calls) == 4 + 2  # one per film page, two for the person batch (continuation)
    assert len([call for call in session.calls if call[1] == SPARQL]) == 3

    again, again_session, _ = make_client(cfg, FakeSession(robots=ROBOTS))
    fetch_wikipedia.run(cfg, client=again)
    assert again_session.calls == []  # resumed entirely from the cache

    films, people = build_enrichment.run(spark, cfg)
    by_film = {r.tconst: r for r in films.collect()}
    assert {t: r.enrichment_status for t, r in by_film.items()} == {
        "tt0000001": "ok",
        "tt0000002": "no_plot_section",
        "tt0000003": "not_found",
        "tt0000004": "not_found",
        "tt0000005": "not_found",
        "tt0000006": "partial",
    }
    alpha = by_film["tt0000001"]
    assert alpha.synopsis == (LONG_PLOT + " He buys a boat.").replace("  ", " ")
    assert (alpha.synopsis_type, alpha.synopsis_section) == ("plot_section", "Plot")
    assert alpha.source_name == "Wikipedia (en)"
    assert alpha.source_url == "https://en.wikipedia.org/wiki/Alpha_(film)"
    assert alpha.source_revision_id == 1001
    assert alpha.source_permalink == "https://en.wikipedia.org/w/index.php?oldid=1001"
    assert alpha.license == "CC BY-SA 4.0" and alpha.enrichment_note is None
    assert alpha.retrieved_at.endswith("Z") and alpha.wikidata_qid == "Q1"

    beta = by_film["tt0000002"]
    assert beta.synopsis == "Beta is a 2000 film directed by nobody."
    assert beta.synopsis_type == "lead_section"
    assert beta.enrichment_note.startswith("No section among (Plot, Synopsis")
    assert "'Beta (film)'; lead section used instead" in beta.enrichment_note

    gamma, delta, epsilon, zeta = (by_film[f"tt000000{i}"] for i in (3, 4, 5, 6))
    assert gamma.enrichment_note == "No enwiki sitelink for Q3 (P345=tt0000003)"
    assert gamma.source_url == "https://www.wikidata.org/wiki/Q3" and gamma.license == "CC0 1.0"
    assert delta.enrichment_note == "No Wikidata item with P345=tt0000004"
    assert delta.source_url == SPARQL and delta.retrieved_at is not None
    assert epsilon.enrichment_note == "Wikipedia page 'Epsilon (film)' does not exist"
    assert (gamma.synopsis, delta.synopsis, epsilon.synopsis) == (None, None, None)
    assert zeta.synopsis == "Short synopsis." and zeta.synopsis_section == "Synopsis"
    assert zeta.enrichment_note == "Section 'Synopsis' shorter than 200 characters (15)"
    assert zeta.source_url == "https://en.wikipedia.org/wiki/Zeta_(2000_film)"  # redirect followed
    for row in by_film.values():
        assert row.source_name and row.source_url and row.license and row.retrieved_at

    by_person = {r.nconst: r for r in people.collect()}
    ada, bob, cy = (by_person[f"nm000000{i}"] for i in (1, 2, 3))
    assert ada.enrichment_status == "ok" and ada.biography.startswith(
        "Ada Alpha (born 2 January 1950)"
    )
    assert (ada.birth_date, ada.death_date, ada.birth_place) == ("1950-01-02", None, "Lyon")
    assert ada.citizenships == ["Canada", "France"]
    assert ada.source_permalink == "https://en.wikipedia.org/w/index.php?oldid=2001"
    assert (
        ada.facts_source_url == "https://www.wikidata.org/wiki/Q101"
        and ada.facts_license == "CC0 1.0"
    )
    assert ada.n_scope_films == 6
    assert bob.enrichment_status == "partial" and bob.biography is None
    assert (
        bob.enrichment_note
        == "No enwiki sitelink for Q102 (P345=nm0000002); Wikidata statements only"
    )
    assert (bob.birth_date, bob.death_date) == ("1960-05-06", "2020-07-08")
    assert cy.enrichment_status == "not_found"
    assert cy.enrichment_note == "No Wikidata item with P345=nm0000003"

    links = spark.read.parquet(io.layer_path(cfg, "gold", "enriched_film_principals"))
    assert links.where("has_biography").count() == 6  # Ada, on each of the six films

    out = Path(cfg.paths.outputs, "enrichment")
    coverage = (out / "coverage.md").read_text("utf-8")
    assert "| not_found | 3 | 50.00 |" in coverage
    assert "| 3 | 1 | 6 |" in coverage  # 3 principals selected, 1 with a biography, 6 films
    sample = (out / "sample.md").read_text("utf-8")
    assert "https://en.wikipedia.org/w/index.php?oldid=1001" in sample
    stats = (out / "collection_stats.md").read_text("utf-8")
    assert "| en.wikipedia.org/w/api.php | disallowed | report |" in stats
    assert "| query.wikidata.org/sparql | disallowed | report |" in stats
    runs = [
        json.loads(line)
        for line in Path(cfg.paths.enrichment, "stats", "collection_runs.jsonl")
        .read_text("utf-8")
        .splitlines()
    ]
    first_run = {run["step"]: run["requests"] for run in runs[:5]}
    assert first_run == {
        "enrichment:film_sitelinks": 1,
        "enrichment:person_sitelinks": 1,
        "enrichment:person_facts": 1,
        "enrichment:film_pages": 4,
        "enrichment:person_intros": 2,
    }
    assert sum(run["requests"] for run in runs[5:]) == 0


def test_enrichment_scales_without_code_change(spark, enrichment_cfg):
    cfg = enrichment_cfg.with_overrides(
        {
            "enrichment.scope.top_n": None,
            "enrichment.scope.year_min": None,
            "enrichment.scope.year_max": None,
            "enrichment.scope.principals_per_film": None,
            "enrichment.scope.principal_categories": None,
        }
    )
    films_scope, people_scope = select_scope.run(spark, cfg)
    assert films_scope.count() == 7  # the 1975 film is now included
    assert people_scope.select("nconst").distinct().count() == 4
