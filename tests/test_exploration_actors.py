from __future__ import annotations

from pathlib import Path

import pytest

from fakes import FakeResponse, make_client
from helpers import crew, movie, person, principal, rating, silver_df, write_silver
from imdb_project.enrichment import fetch_wikidata
from imdb_project.exploration import (
    q6_multilingual_actors,
    q7_early_peak_actors,
    q8_multi_talented,
)

BINDING_SCHEMA = "binding map<string, struct<type:string, value:string>>"
YEARS = list(range(1980, 2011, 2))  # 16 films over a 30-year career


def _binding(**values):
    return ({name: {"type": "literal", "value": value} for name, value in values.items()},)


# ------------------------------------------------------------------------- Q6


def test_q6_wikidata_language_codes(spark):
    lang = "http://www.wikidata.org/entity/"
    bindings = spark.createDataFrame(
        [
            _binding(imdb="tt1", language=lang + "Q1860", languageLabel="English", iso1="en"),
            _binding(
                imdb="tt2", language=lang + "Q7976", languageLabel="American English", ietf="en-US"
            ),
            _binding(imdb="tt3", language=lang + "Q9192", languageLabel="Mandarin", ietf="cmn"),
            _binding(imdb="tt4", language=lang + "Q999999", languageLabel="Rare language"),
            _binding(imdb="tt5"),  # item known to Wikidata, without P364
            _binding(imdb="tt6", language=lang + "Q150", languageLabel="French", iso1="FR"),
            _binding(imdb="tt6", language=lang + "Q1860", languageLabel="English", iso1="en"),
        ],
        BINDING_SCHEMA,
    )
    rows = q6_multilingual_actors.wikidata_film_languages(bindings, {"cmn": "zh"}).collect()
    assert sorted((r.tconst, r.language) for r in rows) == [
        ("tt1", "en"),
        ("tt2", "en"),
        ("tt3", "zh"),
        ("tt4", "q999999"),
        ("tt6", "en"),
        ("tt6", "fr"),
    ]


def test_q6_akas_fallback_and_combination(spark):
    films = spark.createDataFrame(
        [("f1", "Un film"), ("f2", "Der Film"), ("f3", "Movie"), ("f4", "Other")],
        "tconst string, originalTitle string",
    )
    akas = silver_df(
        spark,
        "title_akas",
        [
            {
                "titleId": "f1",
                "ordering": 1,
                "title": "Un film",
                "language": "FR",
                "isOriginalTitle": True,
            },
            {
                "titleId": "f1",
                "ordering": 2,
                "title": "Un film",
                "region": "US",
                "isOriginalTitle": False,
            },
            {"titleId": "f2", "ordering": 1, "title": "Der Film", "isOriginalTitle": True},
            {
                "titleId": "f2",
                "ordering": 2,
                "title": "Der Film",
                "region": "DE",
                "isOriginalTitle": False,
            },
            {
                "titleId": "f2",
                "ordering": 3,
                "title": "Der Film",
                "region": "AT",
                "isOriginalTitle": False,
            },
            {
                "titleId": "f2",
                "ordering": 4,
                "title": "The Film",
                "region": "US",
                "isOriginalTitle": False,
            },
            {
                "titleId": "f3",
                "ordering": 1,
                "title": "Movie",
                "region": "US",
                "isOriginalTitle": False,
            },
            {
                "titleId": "f3",
                "ordering": 2,
                "title": "Movie",
                "region": "FR",
                "isOriginalTitle": False,
            },
            {
                "titleId": "f4",
                "ordering": 1,
                "title": "Other",
                "region": "XX",
                "isOriginalTitle": False,
            },
        ],
    )
    regions = {"US": "en", "FR": "fr", "DE": "de", "AT": "de"}
    fallback = q6_multilingual_actors.akas_film_languages(akas, films, regions, {})
    assert sorted((r.tconst, r.language, r.language_source) for r in fallback.collect()) == [
        ("f1", "fr", "akas_original_language"),
        ("f2", "de", "akas_region"),
    ]

    wikidata = spark.createDataFrame(
        [("f1", "en", "English"), ("f3", "en", "English"), ("f3", "fr", "French")],
        "tconst string, language string, language_label string",
    )
    combined = q6_multilingual_actors.film_languages(wikidata, fallback).collect()
    rows = {(r.tconst, r.language): r for r in combined}
    assert set(rows) == {("f1", "en"), ("f2", "de"), ("f3", "en"), ("f3", "fr")}
    assert rows[("f1", "en")].language_source == "wikidata_P364"  # Wikidata wins over akas
    assert rows[("f2", "de")].language_label == "de"  # no Wikidata label for this code
    assert rows[("f3", "fr")].language_label == "French"
    assert (rows[("f3", "en")].n_languages, rows[("f1", "en")].n_languages) == (2, 1)


def test_q6_actor_languages(spark):
    credits = spark.createDataFrame(
        [("a1", "f1"), ("a1", "f2"), ("a1", "f3"), ("a1", "f4"), ("a2", "f1"), ("a2", "f4")],
        "nconst string, tconst string",
    )
    languages = spark.createDataFrame(
        [
            ("f1", "en", "English"),
            ("f2", "fr", "French"),
            ("f3", "ja", "Japanese"),
            ("f4", "en", "English"),
        ],
        "tconst string, language string, language_label string",
    )
    films = spark.createDataFrame(
        [
            ("f1", "One", 2000, 100),
            ("f2", "Deux", 2001, 100),
            ("f3", "San", None, 100),
            ("f4", "Four", 2003, 900),
        ],
        "tconst string, primaryTitle string, startYear int, numVotes int",
    )
    rows = {
        r.nconst: r
        for r in q6_multilingual_actors.actor_languages(credits, languages, films).collect()
    }
    assert rows["a1"].n_languages == 3
    assert rows["a1"].languages == ["English", "French", "Japanese"]
    assert rows["a1"].n_successful_films == 4
    assert rows["a1"].examples == "English: Four (2003); French: Deux (2001); Japanese: San (?)"
    assert rows["a2"].n_languages == 1


def test_q6_end_to_end_with_cached_wikidata(spark, cfg):
    titles = [
        movie(f"tt000000{i}", 2000 + i, 100, ["Drama"], title=f"Film {i}") for i in range(1, 6)
    ]
    ratings = [rating(f"tt000000{i}", 8.0, 50_000) for i in range(1, 5)]
    ratings.append(rating("tt0000005", 6.0, 50_000))  # not successful
    principals = [principal(f"tt000000{i}", 1, "nm0000001", "actor") for i in range(1, 6)]
    principals += [principal("tt0000001", 2, "nm0000002", "actress")]
    principals += [principal("tt0000002", 2, "nm0000002", "actress")]
    principals += [principal("tt0000003", 3, "nm0000003", "director")]
    write_silver(spark, cfg, "title_basics", titles)
    write_silver(spark, cfg, "title_ratings", ratings)
    write_silver(spark, cfg, "title_principals", principals)
    write_silver(
        spark,
        cfg,
        "name_basics",
        [person("nm0000001", "Polly Glot"), person("nm0000002", "Bi Lingual")],
    )
    write_silver(
        spark,
        cfg,
        "title_akas",
        [
            {
                "titleId": "tt0000003",
                "ordering": 1,
                "title": "Film 3",
                "region": "JP",
                "isOriginalTitle": False,
            }
        ],
    )

    scope = q6_multilingual_actors.run_scope(spark, cfg)
    assert sorted(r.tconst for r in scope.collect()) == [f"tt000000{i}" for i in range(1, 5)]

    known = {
        "tt0000001": [("Q1860", "English", "en")],
        "tt0000002": [("Q150", "French", "fr")],
        "tt0000004": [("Q1860", "English", "en"), ("Q188", "German", "de")],  # multilingual
    }

    def handler(method, url, payload):
        bindings = []
        for imdb_id, languages in known.items():
            if f'"{imdb_id}"' not in payload["query"]:
                continue
            for qid, label, iso in languages:
                bindings.append(
                    {
                        "imdb": {"type": "literal", "value": imdb_id},
                        "language": {
                            "type": "uri",
                            "value": f"http://www.wikidata.org/entity/{qid}",
                        },
                        "languageLabel": {"type": "literal", "value": label},
                        "iso1": {"type": "literal", "value": iso},
                    }
                )
        return FakeResponse({"results": {"bindings": bindings}})

    client, session, _ = make_client(cfg)
    session.script(cfg.wikimedia.sparql_endpoint, handler)
    ids = [r.tconst for r in scope.collect()]
    fetch_wikidata.collect(cfg, "film_languages", ids, "q6:test", client=client)

    result = {r.primaryName: r for r in q6_multilingual_actors.run_analysis(spark, cfg).collect()}
    # tt3 gets "ja" from the akas region fallback; tt4 is excluded (two languages).
    assert result["Polly Glot"].n_languages == 3
    assert result["Polly Glot"].languages == ["English", "French", "ja"]
    assert result["Bi Lingual"].n_languages == 2

    out = Path(cfg.paths.outputs, "exploration")
    report = (out / "q6_multilingual_actors.md").read_text("utf-8")
    assert "| wikidata_P364 | 3 | 1 | 75.00 |" in report
    assert "| akas_region | 1 | 0 | 25.00 |" in report
    assert "| people_with_3_or_more_languages | 1 |" in report
    assert (out / "q6_multilingual_actors_three_or_more.csv").read_text("utf-8").count("\n") == 2

    include = cfg.with_overrides({"exploration.q6.multilingual_films": "include"})
    included = {
        r.primaryName: r for r in q6_multilingual_actors.run_analysis(spark, include).collect()
    }
    assert included["Polly Glot"].n_languages == 4  # German counted through tt4


# ------------------------------------------------------------------------- Q7


def _career(nconst, ratings_by_year):
    return [
        (nconst, f"{nconst}-{year}", year, float(value), 1000)
        for year, value in ratings_by_year.items()
    ]


def _filmography(spark):
    early = {year: (9.0 if year == 1982 else 8.0 if year <= 1994 else 5.0) for year in YEARS}
    late = {year: (9.0 if year == 2008 else 5.0) for year in YEARS}
    short_career = {year: 7.0 for year in range(1980, 1996)}
    few_films = {year: 7.0 for year in range(1980, 2011, 4)}
    one_shot = {year: (9.5 if year == 1980 else 3.0 if year <= 1994 else 6.0) for year in YEARS}
    rows = (
        _career("early", early)
        + _career("late", late)
        + _career("short", short_career)
        + _career("few", few_films)
        + _career("oneshot", one_shot)
    )
    return spark.createDataFrame(
        rows, "nconst string, tconst string, startYear int, averageRating double, numVotes int"
    )


def test_q7_includes_the_exact_first_third_boundary(spark, settings):
    rows = _career(
        "boundary", {year: 9.0 if year == 1990 else 2.0 if year <= 1994 else 1.0 for year in YEARS}
    )
    films = spark.createDataFrame(
        rows, "nconst string, tconst string, startYear int, averageRating double, numVotes int"
    )
    fraction = q7_early_peak_actors.career_fraction(settings)
    (career,) = q7_early_peak_actors.early_peak(
        films, q7_early_peak_actors.career_profiles(films, 20, 15), fraction, 3
    ).collect()
    assert career.peak_position == fraction == 1 / 3
    assert career.early_peak is True


def test_q7_career_profiles_and_early_peak(spark):
    filmography = _filmography(spark)
    profiles = q7_early_peak_actors.career_profiles(filmography, 20, 15)
    by_person = {r.nconst: r for r in profiles.collect()}
    assert set(by_person) == {"early", "late", "oneshot"}
    early = by_person["early"]
    assert (early.first_year, early.last_year, early.career_years, early.n_films) == (
        1980,
        2010,
        30,
        16,
    )
    assert (early.peak_year, early.peak_rating) == (1982, 9.0)
    assert early.peak_position == pytest.approx(2 / 30)
    assert by_person["late"].peak_position == pytest.approx(28 / 30)

    careers = {
        r.nconst: r
        for r in q7_early_peak_actors.early_peak(filmography, profiles, 1 / 3, 3).collect()
    }
    assert careers["early"].early_peak is True
    assert careers["early"].first_half_avg == pytest.approx(65 / 8)
    assert careers["early"].second_half_avg == pytest.approx(5.0)
    assert careers["early"].rating_slope < 0
    assert careers["early"].top_k_mean_position == pytest.approx((2 / 30 + 0 + 4 / 30) / 3)
    assert careers["late"].early_peak is False
    assert careers["late"].rating_slope > 0
    # Best film at the very start, but the second half of the career is rated higher.
    assert careers["oneshot"].peak_position == 0.0
    assert careers["oneshot"].early_peak is False


def test_q7_actor_filmography_deduplicates_credits(spark):
    principals = silver_df(
        spark,
        "title_principals",
        [
            principal("tt1", 1, "nm1", "actor"),
            principal("tt1", 2, "nm1", "actor"),  # two roles in the same film
            principal("tt1", 3, "nm2", "director"),
            principal("tt2", 1, "nm1", "actress"),
            principal("tt3", 1, "nm1", "actor"),  # film without year
        ],
    )
    films = spark.createDataFrame(
        [("tt1", 2000, 7.0, 10), ("tt2", 2001, 6.0, 10), ("tt3", None, 6.0, 10)],
        "tconst string, startYear int, averageRating double, numVotes int",
    )
    rows = q7_early_peak_actors.actor_filmography(principals, films, ["actor", "actress"]).collect()
    assert sorted((r.nconst, r.tconst) for r in rows) == [("nm1", "tt1"), ("nm1", "tt2")]


# ------------------------------------------------------------------------- Q8

ROLE_CATEGORIES = {"actor": "actor", "actress": "actor", "director": "director", "writer": "writer"}


def _roles(spark):
    rows = []
    rows += [("nm1", f"t{i}", "director") for i in range(1, 6)]
    rows += [("nm1", f"t{i}", "actor") for i in range(1, 4)]
    rows += [("nm2", f"t{i}", "actor") for i in range(1, 6)]
    rows += [("nm3", f"t{i}", "writer") for i in range(1, 4)] + [("nm3", "t1", "director")]
    rows += [("nm4", f"t{i}", role) for i in range(6, 9) for role in ("writer", "director")]
    rows += [
        ("nm5", f"t{i}", role) for i in range(1, 4) for role in ("actor", "director", "writer")
    ]
    rows += [("nm5", "t4", "writer")]
    return spark.createDataFrame(rows, "nconst string, tconst string, role string")


def _rated(spark):
    values = {
        "t1": 8.0,
        "t2": 7.0,
        "t3": 6.0,
        "t4": 5.0,
        "t5": 4.0,
        "t6": 7.0,
        "t7": 7.0,
        "t8": 7.0,
    }
    return spark.createDataFrame(
        [(tconst, value, 1000) for tconst, value in values.items()],
        "tconst string, averageRating double, numVotes int",
    )


def test_q8_roles_from_principals_and_crew(spark):
    principals = silver_df(
        spark,
        "title_principals",
        [
            principal("t1", 1, "nm1", "actress"),
            principal("t1", 2, "nm1", "director"),
            principal("t1", 3, "nm2", "composer"),  # not a tracked role
            principal("t1", 4, "nm3", "writer"),
        ],
    )
    crew_df = silver_df(spark, "title_crew", [crew("t1", ["nm1"], ["nm3", "nm4"])])
    roles = q8_multi_talented.person_title_roles(principals, crew_df, ROLE_CATEGORIES)
    assert sorted((r.nconst, r.role) for r in roles.collect()) == [
        ("nm1", "actor"),
        ("nm1", "director"),
        ("nm3", "writer"),
        ("nm4", "writer"),
    ]


def test_q8_multi_talented_and_paired_comparison(spark):
    roles = _roles(spark)
    talents = {r.nconst: r for r in q8_multi_talented.multi_talented(roles, 3).collect()}
    assert {k: v.career_roles for k, v in talents.items()} == {
        "nm1": "actor+director",
        "nm4": "director+writer",
        "nm5": "actor+director+writer",
    }

    combinations = q8_multi_talented.title_combinations(roles, _rated(spark))
    nm1 = {r.tconst: r for r in combinations.where("nconst = 'nm1'").collect()}
    assert (nm1["t1"].combination, nm1["t1"].n_roles) == ("actor+director", 2)
    assert (nm1["t5"].combination, nm1["t5"].n_roles) == ("director", 1)

    comparison = q8_multi_talented.person_comparison(
        combinations, q8_multi_talented.multi_talented(roles, 3)
    )
    rows = {(r.nconst, r.combination): r for r in comparison.collect()}
    # nm4 never works in a single role: no paired comparison is possible.
    assert set(rows) == {
        ("nm1", "actor+director"),
        ("nm1", q8_multi_talented.ANY_COMBINATION),
        ("nm5", "actor+director+writer"),
        ("nm5", q8_multi_talented.ANY_COMBINATION),
    }
    nm1_any = rows[("nm1", q8_multi_talented.ANY_COMBINATION)]
    assert (nm1_any.n_multi, nm1_any.n_single) == (3, 2)
    assert (nm1_any.avg_multi, nm1_any.avg_single, nm1_any.diff) == (7.0, 4.5, 2.5)
    assert rows[("nm5", "actor+director+writer")].diff == pytest.approx(2.0)

    summary = {r.combination: r for r in q8_multi_talented.summarize(comparison).collect()}
    overall = summary[q8_multi_talented.ANY_COMBINATION]
    assert (overall.people, overall.multi_role_films) == (2, 6)
    assert overall.mean_diff == pytest.approx(2.25)
    assert overall.median_diff == pytest.approx(2.25)
    assert overall.pct_people_better_multi_role == pytest.approx(100.0)
    assert summary["actor+director"].people == 1


def test_q7_and_q8_end_to_end(spark, cfg):
    titles, ratings, principals, crews = [], [], [], []
    for index, year in enumerate(YEARS):
        tconst = f"tt{index:04d}"
        titles.append(movie(tconst, year, 100, ["Drama"], title=f"Film {year}"))
        value = 9.0 if year == 1982 else 8.0 if year <= 1994 else 5.0
        ratings.append(rating(tconst, value, 5000))
        principals.append(principal(tconst, 1, "nm1", "actor"))
        directors = ["nm1"] if index < 4 else ["nm9"]
        crews.append(crew(tconst, directors, ["nm1"] if index < 2 else None))
    write_silver(spark, cfg, "title_basics", titles)
    write_silver(spark, cfg, "title_ratings", ratings)
    write_silver(spark, cfg, "title_principals", principals)
    write_silver(spark, cfg, "title_crew", crews)
    write_silver(
        spark, cfg, "name_basics", [person("nm1", "Ada Alpha", 1955), person("nm9", "Nine")]
    )

    (career,) = q7_early_peak_actors.run(spark, cfg).collect()
    assert (career.primaryName, career.early_peak, career.peak_title) == (
        "Ada Alpha",
        True,
        "Film 1982",
    )

    result = q8_multi_talented.run(spark, cfg)
    overall = result.where(f"combination = '{q8_multi_talented.ANY_COMBINATION}'").collect()
    assert [(r.primaryName, r.career_roles, r.n_multi, r.n_single) for r in overall] == [
        ("Ada Alpha", "actor+director", 4, 12)
    ]

    out = Path(cfg.paths.outputs, "exploration")
    q7 = (out / "q7_early_peak_actors.md").read_text("utf-8")
    assert "| early_peak_people | 1 |" in q7 and "Ada Alpha" in q7
    q8 = (out / "q8_multi_talented.md").read_text("utf-8")
    assert "| multi_talented_people | 1 |" in q8
    assert (out / "q8_multi_talented_summary.csv").is_file()
