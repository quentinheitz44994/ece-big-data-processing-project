from __future__ import annotations

import csv
from pathlib import Path

import pytest

from helpers import movie, rating, silver_df, write_silver
from imdb_project.exploration import base, q1_runtime_outliers, q2_top_genres, q3_top_vs_rest

RUNTIMES = [50, 90, 90, 90, 90, 100, 100, 100, 100, 110, 110, 110, 110, 400]


def test_csv_export_limits_are_reported_explicitly(spark, cfg):
    configured = cfg.with_overrides({"exploration.max_csv_rows": 1})
    df = spark.createDataFrame([(1,), (2,), (3,)], "value int").orderBy("value")
    base.write_report(configured, "review", "Review", {}, [], csv_exports={"": df})
    folder = Path(cfg.paths.outputs, "exploration")
    with (folder / "review_exports.csv").open() as handle:
        (export,) = csv.DictReader(handle)
    assert export["total_rows"] == "3" and export["exported_rows"] == "1"
    assert export["truncated"] == "true" and export["gold_directory"].endswith("exploration")
    assert "| review.csv | 3 | 1 | true |" in (folder / "review.md").read_text()
    assert (folder / "review.csv").read_text().splitlines() == ["value", "1"]


def _genre_films(spark):
    rows = [
        (f"tt{i:03d}", f"Film {i}", 2000, runtime, "Drama") for i, runtime in enumerate(RUNTIMES)
    ]
    rows += [
        (f"tt9{i:02d}", f"Doc {i}", 2001, runtime, "Documentary")
        for i, runtime in enumerate([60, 61])
    ]
    return spark.createDataFrame(
        rows, "tconst string, primaryTitle string, startYear int, runtimeMinutes int, genre string"
    )


def test_feature_film_definition(spark, cfg):
    titles = silver_df(
        spark,
        "title_basics",
        [
            movie("tt1", 2000, 90, ["Drama"]),
            movie("tt2", 2000, 39, ["Drama"]),  # too short
            movie("tt3", 2000, None, ["Drama"]),  # unknown runtime
            movie("tt4", 2000, 90, ["Drama"], is_adult=True),
            movie("tt5", 2000, 90, ["Drama"], title_type="tvMovie"),
            movie("tt6", 2000, 40, None),  # exactly the threshold, no genre
        ],
    )
    assert sorted(r.tconst for r in base.feature_films(titles, cfg).collect()) == ["tt1", "tt6"]
    with_adult = cfg.with_overrides({"exploration.feature_film.include_adult": True})
    assert base.feature_films(titles, with_adult).count() == 3
    assert base.explode_genres(base.feature_films(titles, cfg)).count() == 1


def test_question_setting_falls_back_to_section(cfg):
    assert base.question_setting(cfg, "q2", "min_votes") == cfg.exploration.min_votes
    custom = cfg.with_overrides({"exploration.q2.min_votes": 5})
    assert base.question_setting(custom, "q2", "min_votes") == 5
    assert base.question_setting(cfg, "q2", "unknown", "fallback") == "fallback"


def test_q1_stats_and_outlier_methods(spark):
    films = _genre_films(spark)
    stats = {r.genre: r for r in q1_runtime_outliers.genre_runtime_stats(films, 1.5).collect()}
    drama = stats["Drama"]
    assert (drama.n_films, drama.q1, drama.median, drama.q3) == (14, 90.0, 100.0, 110.0)
    assert (drama.lower_fence, drama.upper_fence) == (60.0, 140.0)
    assert drama.mean_runtime == pytest.approx(sum(RUNTIMES) / 14)

    analysed = q1_runtime_outliers.genre_runtime_stats(films, 1.5).where("n_films >= 5")
    outliers = q1_runtime_outliers.runtime_outliers(films, analysed, 2.0).collect()
    found = {(r.runtimeMinutes, r.method, r.direction) for r in outliers}
    assert found == {(400, "zscore+iqr", "longer"), (50, "iqr", "shorter")}
    assert {r.genre for r in outliers} == {"Drama"}  # Documentary has too few films

    top = q1_runtime_outliers.top_outliers_per_genre(
        q1_runtime_outliers.runtime_outliers(films, analysed, 2.0), 1
    ).collect()
    assert [(r.runtimeMinutes, r.rank_in_genre) for r in top] == [(400, 1)]


def _films_2000(spark):
    rows = [
        ("tt1", 2000, "Drama", 8.0, 5000),
        ("tt2", 2000, "Drama", 6.0, 3000),
        ("tt3", 2000, "Comedy", 7.0, 4000),
        ("tt4", 2000, "Action", 5.0, 2000),
        ("tt5", 2000, "Horror", 4.0, 1000),
        ("tt6", 2001, "Horror", 9.0, 9000),
        ("tt6", 2001, "Drama", 9.0, 9000),  # same film, second genre: tie at rank 1
        ("tt7", 2001, "Comedy", 5.0, 100),
    ]
    return spark.createDataFrame(
        rows, "tconst string, startYear int, genre string, averageRating double, numVotes int"
    )


def test_q2_popularity_ranking(spark):
    popularity = q2_top_genres.genre_year_popularity(_films_2000(spark))
    rows = {(r.startYear, r.genre): r for r in popularity.collect()}
    drama = rows[(2000, "Drama")]
    assert (drama.total_votes, drama.n_films, drama.rank) == (8000, 2, 1)
    assert drama.weighted_rating == pytest.approx(7.25)
    assert drama.vote_share_pct == pytest.approx(100 * 8000 / 15000)
    assert rows[(2000, "Comedy")].rank == 2
    assert rows[(2000, "Horror")].rank == 4
    assert rows[(2001, "Horror")].rank == rows[(2001, "Drama")].rank == 1  # dense_rank tie
    assert rows[(2001, "Comedy")].rank == 2

    top = q2_top_genres.top_genres(popularity, 3)
    assert top.where("startYear = 2000").count() == 3
    wide = {r.year: r for r in q2_top_genres.wide_top_table(top, 3).collect()}
    assert wide[2000].rank_1 == "Drama (53.3%)"
    assert wide[2001].rank_1 == "Drama (49.7%) / Horror (49.7%)"
    assert wide[2001].rank_3 is None


def test_q3_top_versus_rest(spark):
    popularity = q2_top_genres.genre_year_popularity(_films_2000(spark))
    grouped = q3_top_vs_rest.with_group(popularity, 3)
    yearly = {r.startYear: r for r in q3_top_vs_rest.compare_groups(grouped, "startYear").collect()}
    y2000 = yearly[2000]
    assert (y2000.top_votes, y2000.rest_votes) == (14000, 1000)
    assert (y2000.top_films, y2000.rest_films) == (4, 1)
    assert y2000.top_vote_share_pct == pytest.approx(100 * 14 / 15)
    assert y2000.votes_ratio_top_rest == pytest.approx(14.0)
    assert y2000.top_votes_per_film == pytest.approx(3500.0)
    assert y2000.top_weighted_rating == pytest.approx(96000 / 14000)
    assert y2000.weighted_rating_diff_top_rest == pytest.approx(96000 / 14000 - 4.0)
    # 2001: every genre is in the top 3, the "rest" side is empty.
    assert yearly[2001].rest_votes is None
    assert yearly[2001].top_vote_share_pct == pytest.approx(100.0)
    assert yearly[2001].votes_ratio_top_rest is None

    stability = {r.genre: r for r in q3_top_vs_rest.podium_stability(grouped).collect()}
    assert stability["Drama"].years_in_top == 2
    assert stability["Drama"].years_ranked_first == 2
    assert stability["Action"].years_in_top == 1
    assert stability["Horror"].first_year_in_top == 2001
    assert stability["Drama"].pct_years_in_top == pytest.approx(100.0)


def test_genre_questions_end_to_end(spark, cfg):
    titles, ratings = [], []
    for i, runtime in enumerate(RUNTIMES):
        tconst = f"tt{i:03d}"
        genres = ["Drama", "Comedy"] if i % 2 else ["Drama"]
        titles.append(movie(tconst, 1990 + i, runtime, genres))
        ratings.append(rating(tconst, 5.0 + i / 4, 1000 * (i + 1)))
    titles.append(movie("tt900", 1995, 95, ["Horror"]))
    ratings.append(rating("tt900", 6.0, 10))  # below min_votes
    titles.append(movie("tt901", 1970, 95, ["Drama"]))  # before year_min
    ratings.append(rating("tt901", 6.0, 99999))
    write_silver(spark, cfg, "title_basics", titles)
    write_silver(spark, cfg, "title_ratings", ratings)
    cfg = cfg.with_overrides({"exploration.q1.min_films_per_genre": 5})

    outliers = q1_runtime_outliers.run(spark, cfg)
    assert {r.runtimeMinutes for r in outliers.where("genre = 'Drama'").collect()} == {50, 400}
    top = q2_top_genres.run(spark, cfg)
    assert top.where("genre = 'Horror'").count() == 0
    assert top.where("startYear = 1970").count() == 0
    yearly = q3_top_vs_rest.run(spark, cfg)
    assert yearly.count() == len(RUNTIMES)

    out = Path(cfg.paths.outputs, "exploration")
    for name in (
        "q1_runtime_outliers.md",
        "q1_runtime_outliers.csv",
        "q1_runtime_outliers_summary.csv",
        "q2_top_genres.md",
        "q2_top_genres.csv",
        "q3_top_vs_rest.md",
        "q3_top_vs_rest_by_decade.csv",
    ):
        assert (out / name).is_file(), name
    q1 = (out / "q1_runtime_outliers.md").read_text("utf-8")
    assert "| z_threshold | 2 |" in q1 and "| feature_film.min_runtime_minutes | 40 |" in q1
    assert "| min_votes | 1000 |" in (out / "q2_top_genres.md").read_text("utf-8")
