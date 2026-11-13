from __future__ import annotations

from pathlib import Path

import pytest

from helpers import crew, episode, movie, person, principal, rating, silver_df, write_silver
from imdb_project.exploration import q4_one_hit_directors, q5_series_decline

FILMOGRAPHY_SCHEMA = (
    "nconst string, tconst string, primaryTitle string, startYear int, "
    "averageRating double, numVotes int"
)


def test_director_credits_merges_both_sources(spark):
    crew_df = silver_df(spark, "title_crew", [crew("tt1", ["nm1", "nm2"]), crew("tt2", None)])
    principals = silver_df(
        spark,
        "title_principals",
        [
            principal("tt1", 1, "nm1", "director"),  # duplicate of the crew credit
            principal("tt2", 1, "nm3", "director"),  # only in principals
            principal("tt2", 2, "nm4", "actor"),
        ],
    )
    credits = q4_one_hit_directors.director_credits(crew_df, principals)
    assert sorted((r.tconst, r.nconst) for r in credits.collect()) == [
        ("tt1", "nm1"),
        ("tt1", "nm2"),
        ("tt2", "nm3"),
    ]


def test_one_hit_directors_conditions(spark):
    rows = [
        # nm1: one hit, two others averaging 5.5 -> selected
        ("nm1", "tt1", "Hit", 2000, 8.4, 9000),
        ("nm1", "tt2", "Meh", 2001, 5.0, 2000),
        ("nm1", "tt3", "Meh 2", 2002, 6.0, 2000),
        # nm2: two hits -> rejected
        ("nm2", "tt4", "Hit A", 2000, 8.0, 9000),
        ("nm2", "tt5", "Hit B", 2001, 9.0, 9000),
        ("nm2", "tt6", "Low", 2002, 3.0, 2000),
        ("nm2", "tt7", "Low 2", 2003, 3.0, 2000),
        # nm3: one hit but a single other film -> rejected
        ("nm3", "tt8", "Hit", 2000, 8.5, 9000),
        ("nm3", "tt9", "Low", 2001, 4.0, 2000),
        # nm4: one hit, others average 6.5 -> rejected
        ("nm4", "tt10", "Hit", 2000, 8.1, 9000),
        ("nm4", "tt11", "Ok", 2001, 6.0, 2000),
        ("nm4", "tt12", "Ok 2", 2002, 7.0, 2000),
        # nm5: no hit -> rejected
        ("nm5", "tt13", "Low", 2000, 5.0, 2000),
        ("nm5", "tt14", "Low 2", 2001, 5.0, 2000),
        ("nm5", "tt15", "Low 3", 2002, 5.0, 2000),
    ]
    filmography = spark.createDataFrame(rows, FILMOGRAPHY_SCHEMA)
    (selected,) = q4_one_hit_directors.one_hit_directors(filmography, 8.0, 6.0, 2).collect()
    assert selected.nconst == "nm1"
    assert (selected.hit_title, selected.hit_year, selected.hit_rating) == ("Hit", 2000, 8.4)
    assert selected.n_other_films == 2
    assert selected.avg_other_rating == pytest.approx(5.5)
    assert (selected.min_other_rating, selected.max_other_rating) == (5.0, 6.0)


def _episodes(spark, rows):
    return spark.createDataFrame(
        rows,
        "parentTconst string, tconst string, seasonNumber int, episodeNumber int, "
        "averageRating double, numVotes int",
    )


def _series(parent, ratings_by_season):
    rows = []
    for season, ratings in ratings_by_season.items():
        for number, value in enumerate(ratings, start=1):
            rows.append((parent, f"{parent}s{season}e{number}", season, number, float(value), 100))
    return rows


def test_series_decline_selection_and_ties(spark):
    rows = (
        # A: best (9.5) in season 1, worst (3.0) in the last season -> selected
        _series("A", {1: [9.5, 8.0, 8.0], 2: [8.0, 7.5, 7.0], 3: [6.0, 5.0, 3.0]})
        # B: worst episode in season 2 -> rejected
        + _series("B", {1: [9.5, 8.0, 8.0], 2: [2.0, 7.5, 7.0], 3: [6.0, 5.0, 3.0]})
        # C: best episode in season 3 -> rejected
        + _series("C", {1: [8.0, 8.0, 8.0], 2: [8.0, 7.5, 7.0], 3: [9.9, 5.0, 3.0]})
        # D: only two eligible seasons (season 3 has 2 episodes) -> rejected
        + _series("D", {1: [9.5, 8.0, 8.0], 2: [8.0, 7.5, 7.0], 3: [6.0, 3.0]})
        # E: best tied between season 1 and season 3 -> "any" only
        + _series("E", {1: [9.0, 8.0, 8.0], 2: [8.0, 7.5, 7.0], 3: [9.0, 5.0, 3.0]})
        # F: a fourth, short last season holds the worst episode -> selected
        + _series("F", {1: [9.0, 8, 8], 2: [8, 7.5, 7], 3: [6, 5, 4], 4: [2.0]})
    )
    episodes = _episodes(spark, rows)

    strict = {
        r.parentTconst: r
        for r in q5_series_decline.series_decline(episodes, 3, 3, 2, "all").collect()
    }
    assert set(strict) == {"A", "F"}
    a = strict["A"]
    assert (a.best_rating, a.best_season, a.best_episode) == (9.5, 1, 1)
    assert (a.worst_rating, a.worst_season, a.worst_episode) == (3.0, 3, 3)
    assert (a.n_seasons, a.n_eligible_seasons, a.n_rated_episodes, a.last_season) == (3, 3, 9, 3)
    assert (strict["F"].last_season, strict["F"].n_eligible_seasons) == (4, 3)

    loose = q5_series_decline.series_decline(episodes, 3, 3, 2, "any").collect()
    assert {r.parentTconst for r in loose} == {"A", "E", "F"}

    with pytest.raises(ValueError, match="tie_policy"):
        q5_series_decline.series_decline(episodes, 3, 3, 2, "first")


def test_rated_series_episodes_filters(spark):
    titles = silver_df(
        spark,
        "title_basics",
        [
            movie("S1", 2000, 30, ["Drama"], title_type="tvSeries"),
            movie("M1", 2000, 90, ["Drama"]),
        ],
    )
    episodes = silver_df(
        spark,
        "title_episode",
        [
            episode("e1", "S1", 1, 1),
            episode("e2", "S1", None, None),  # unknown season
            episode("e3", "S1", 0, 1),  # season 0
            episode("e4", "S1", 1, 2),  # too few votes
            episode("e5", "S1", 1, 3),  # unrated
            episode("e6", "M1", 1, 1),  # parent is a movie
        ],
    )
    ratings = silver_df(
        spark,
        "title_ratings",
        [rating("e1", 8.0, 60), rating("e2", 8.0, 60), rating("e3", 8.0, 60)]
        + [rating("e4", 8.0, 10), rating("e6", 8.0, 60)],
    )
    kept = q5_series_decline.rated_series_episodes(
        episodes, titles, ratings, ["tvSeries", "tvMiniSeries"], 50
    )
    assert [r.tconst for r in kept.collect()] == ["e1"]


@pytest.mark.parametrize("last_votes", [None, 1])
def test_last_season_is_not_lost_when_rating_coverage_is_missing(spark, last_votes):
    titles = silver_df(
        spark, "title_basics", [movie("S1", 2000, 30, ["Drama"], title_type="tvSeries")]
    )
    episodes = []
    ratings = []
    for season, score in [(1, 9.0), (2, 7.0), (3, 1.0), (4, 5.0)]:
        for number in range(1, 11):
            title = f"ep{season}-{number}"
            episodes.append(episode(title, "S1", season, number))
            if season < 4 or last_votes is not None:
                ratings.append(rating(title, score, 100 if season < 4 else last_votes))
    rated = q5_series_decline.rated_series_episodes(
        silver_df(spark, "title_episode", episodes),
        titles,
        silver_df(spark, "title_ratings", ratings),
        ["tvSeries"],
        50,
    )
    assert {r.last_season for r in rated.select("last_season").distinct().collect()} == {4}
    assert q5_series_decline.series_decline(rated, 3, 10, 2, "all").count() == 0


def test_directors_and_series_end_to_end(spark, cfg):
    titles = [
        movie("tt1", 2000, 100, ["Drama"], title="The Hit"),
        movie("tt2", 2001, 100, ["Drama"]),
        movie("tt3", 2002, 100, ["Drama"]),
        movie("tt4", 2003, 100, ["Drama"]),  # too few votes: ignored
        movie("S1", 2010, 30, ["Drama"], title="Fading Show", title_type="tvSeries", end_year=2013),
    ]
    ratings = [
        rating("tt1", 8.3, 5000),
        rating("tt2", 5.0, 5000),
        rating("tt3", 6.0, 5000),
        rating("tt4", 9.9, 10),
    ]
    episodes = []
    seasons = {1: [9.5] + [8.0] * 9, 2: [8.0] * 10, 3: [6.0] * 9 + [2.5]}
    for season, values in seasons.items():
        for number, value in enumerate(values, start=1):
            tconst = f"ep{season}{number:02d}"
            titles.append(movie(tconst, 2010 + season, 30, ["Drama"], title_type="tvEpisode"))
            ratings.append(rating(tconst, value, 100))
            episodes.append(episode(tconst, "S1", season, number))
    write_silver(spark, cfg, "title_basics", titles)
    write_silver(spark, cfg, "title_ratings", ratings)
    write_silver(spark, cfg, "title_episode", episodes)
    write_silver(spark, cfg, "title_crew", [crew(t, ["nm1"]) for t in ("tt1", "tt2", "tt3", "tt4")])
    write_silver(spark, cfg, "title_principals", [principal("tt1", 1, "nm1", "director")])
    write_silver(spark, cfg, "name_basics", [person("nm1", "Dee Rector")])

    (director,) = q4_one_hit_directors.run(spark, cfg).collect()
    assert (director.primaryName, director.hit_title, director.n_other_films) == (
        "Dee Rector",
        "The Hit",
        2,
    )
    (series,) = q5_series_decline.run(spark, cfg).collect()
    assert series.series_title == "Fading Show"
    assert (series.best_season, series.worst_season, series.last_season) == (1, 3, 3)
    assert series.best_episode_title == "Title ep101"
    assert series.worst_episode_title == "Title ep310"

    out = Path(cfg.paths.outputs, "exploration")
    q4 = (out / "q4_one_hit_directors.md").read_text("utf-8")
    assert "| directors_found | 1 |" in q4 and "Dee Rector" in q4
    q5 = (out / "q5_series_decline.md").read_text("utf-8")
    assert "| tie_policy | all |" in q5 and "Fading Show" in q5
    assert (out / "q5_series_decline.csv").is_file()
