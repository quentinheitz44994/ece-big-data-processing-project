from __future__ import annotations

from pathlib import Path

import pytest

from helpers import crew, movie, person, principal, rating, silver_df, write_silver
from imdb_project.open_question import collaborations as oq

FILMS_SCHEMA = (
    "tconst string, primaryTitle string, startYear int, averageRating double, numVotes int"
)
CREDITS_SCHEMA = "tconst string, nconst string"


def _films(spark, rows):
    return spark.createDataFrame(
        [(t, f"Film {t}", year, value, 5000) for t, year, value in rows], FILMS_SCHEMA
    )


def _credits(spark, rows):
    return spark.createDataFrame(rows, CREDITS_SCHEMA)


def _collabs(spark):
    """d1 directs t1..t5; a1 plays in t1, t3, t4; d1 also acts in t2."""
    films = _films(
        spark,
        [
            ("t1", 2000, 6.0),
            ("t2", 2001, 7.0),
            ("t3", 2002, 7.0),
            ("t4", 2002, 8.0),
            ("t5", 2004, 5.0),
            ("t6", 2003, 9.0),
        ],
    )
    directing = _credits(
        spark, [("t1", "d1"), ("t2", "d1"), ("t3", "d1"), ("t4", "d1"), ("t5", "d1"), ("t6", "d2")]
    )
    acting = _credits(
        spark,
        [("t1", "a1"), ("t3", "a1"), ("t4", "a1"), ("t2", "d1"), ("t5", "a2"), ("t6", "a1")],
    )
    return films, directing, acting


def test_collaboration_films_ranks_and_self_direction(spark):
    films, directing, acting = _collabs(spark)
    rows = oq.collaboration_films(directing, acting, films).collect()
    pairs = {
        (r.director_nconst, r.actor_nconst, r.tconst): (r.collab_rank, r.n_collabs) for r in rows
    }
    assert pairs[("d1", "a1", "t1")] == (1, 3)
    assert pairs[("d1", "a1", "t3")] == (2, 3)
    assert pairs[("d1", "a1", "t4")] == (3, 3)  # same year as t3: ordered by tconst
    assert pairs[("d2", "a1", "t6")] == (1, 1)
    assert ("d1", "d1", "t2") not in pairs
    kept = oq.collaboration_films(directing, acting, films, exclude_self=False).collect()
    assert any(r.director_nconst == r.actor_nconst == "d1" for r in kept)


def test_pair_summary_delta_and_outcome(spark):
    films, directing, acting = _collabs(spark)
    collabs = oq.collaboration_films(directing, acting, films)
    (pair,) = oq.pair_summary(collabs, 2, 0.05).collect()
    assert (pair.director_nconst, pair.actor_nconst, pair.n_collabs) == ("d1", "a1", 3)
    assert (pair.first_tconst, pair.first_year, pair.last_year) == ("t1", 2000, 2002)
    assert pair.first_rating == 6.0
    assert pair.repeat_avg_rating == pytest.approx(7.5)
    assert pair.delta == pytest.approx(1.5)
    assert pair.outcome == "higher"
    assert oq.pair_summary(collabs, 4, 0.05).count() == 0
    with pytest.raises(ValueError):
        oq.pair_summary(collabs, 1, 0.05)


@pytest.mark.parametrize(
    ("first", "repeat", "expected"),
    [(6.0, 6.04, "equal"), (6.0, 5.9, "lower"), (6.0, 6.1, "higher")],
)
def test_pair_summary_tolerance(spark, first, repeat, expected):
    films = _films(spark, [("t1", 2000, first), ("t2", 2001, repeat)])
    directing = _credits(spark, [("t1", "d1"), ("t2", "d1")])
    acting = _credits(spark, [("t1", "a1"), ("t2", "a1")])
    collabs = oq.collaboration_films(directing, acting, films)
    (pair,) = oq.pair_summary(collabs, 2, 0.05).collect()
    assert pair.outcome == expected


def test_director_baseline_uses_later_films_without_the_actor(spark):
    films, directing, acting = _collabs(spark)
    collabs = oq.collaboration_films(directing, acting, films)
    director_films = directing.withColumnRenamed("nconst", "director_nconst").join(
        films.select("tconst", "startYear", "averageRating"), "tconst"
    )
    pairs = oq.pair_summary(collabs, 2, 0.05)
    (row,) = oq.director_baseline(pairs, collabs, director_films).collect()
    # d1's films after t1 without a1: t2 (7.0) and t5 (5.0).
    assert row.baseline_films == 2
    assert row.baseline_avg_rating == pytest.approx(6.0)
    assert row.excess == pytest.approx(1.5)


def test_director_baseline_without_other_films(spark):
    films = _films(spark, [("t1", 2000, 6.0), ("t2", 2001, 7.0)])
    directing = _credits(spark, [("t1", "d1"), ("t2", "d1")])
    acting = _credits(spark, [("t1", "a1"), ("t2", "a1")])
    collabs = oq.collaboration_films(directing, acting, films)
    director_films = directing.withColumnRenamed("nconst", "director_nconst").join(
        films.select("tconst", "startYear", "averageRating"), "tconst"
    )
    (row,) = oq.director_baseline(
        oq.pair_summary(collabs, 2, 0.0), collabs, director_films
    ).collect()
    assert row.baseline_films == 0
    assert row.baseline_avg_rating is None and row.excess is None


def test_rank_profile_groups_high_ranks(spark):
    rows = [(f"t{i}", 2000 + i, 5.0 + i) for i in range(1, 5)]
    films = _films(spark, rows)
    directing = _credits(spark, [(t, "d1") for t, _, _ in rows])
    acting = _credits(spark, [(t, "a1") for t, _, _ in rows])
    collabs = oq.collaboration_films(directing, acting, films)
    pairs = oq.pair_summary(collabs, 2, 0.0)
    profile = oq.rank_profile(collabs, pairs, 3).collect()
    assert [r.collab_rank for r in profile] == ["1", "2", "3+"]
    assert [r.films for r in profile] == [1, 1, 2]
    assert profile[2].avg_rating == pytest.approx(8.5)
    assert profile[2].avg_diff_vs_first == pytest.approx(2.5)
    with pytest.raises(ValueError):
        oq.rank_profile(collabs, pairs, 1)


def test_bucket_labels(spark):
    df = spark.createDataFrame([(n,) for n in (2, 3, 4, 5, 6, 9)], "n_collabs int")
    labels = [r.label for r in df.select(oq.bucket_label([2, 3, 4, 6]).alias("label")).collect()]
    assert labels == ["2", "3", "4-5", "4-5", "6+", "6+"]


def test_actor_credits_filters_categories(spark):
    principals = silver_df(
        spark,
        "title_principals",
        [
            principal("tt1", 1, "nm1", "actor"),
            principal("tt1", 2, "nm2", "actress"),
            principal("tt1", 3, "nm3", "director"),
            principal("tt1", 4, "nm1", "actor"),
        ],
    )
    credits = oq.actor_credits(principals, ["actor", "actress"]).collect()
    assert sorted((r.tconst, r.nconst) for r in credits) == [("tt1", "nm1"), ("tt1", "nm2")]


def test_open_question_end_to_end(spark, cfg):
    years = {"tt1": 2000, "tt2": 2002, "tt3": 2004, "tt4": 2001, "tt5": 2003, "tt6": 1999}
    values = {"tt1": 6.0, "tt2": 7.0, "tt3": 8.0, "tt4": 6.5, "tt5": 7.5, "tt6": 9.0}
    titles = [movie(t, y, 100, ["Drama"]) for t, y in years.items()]
    titles.append(movie("tt7", 2005, 20, ["Drama"]))  # too short: not a feature film
    write_silver(spark, cfg, "title_basics", titles)
    ratings = [rating(t, v, 5000) for t, v in values.items()]
    ratings.append(rating("tt7", 9.9, 5000))
    write_silver(spark, cfg, "title_ratings", ratings)
    write_silver(
        spark,
        cfg,
        "title_crew",
        [crew(t, ["nm1"]) for t in ("tt1", "tt2", "tt3", "tt4", "tt5", "tt7")]
        + [crew("tt6", ["nm9"])],
    )
    write_silver(
        spark,
        cfg,
        "title_principals",
        [principal(t, 1, "nm2", "actor") for t in ("tt1", "tt2", "tt3", "tt7")]
        + [principal("tt4", 1, "nm3", "actress"), principal("tt6", 1, "nm2", "actor")],
    )
    write_silver(
        spark,
        cfg,
        "name_basics",
        [person("nm1", "Dee Rector"), person("nm2", "Ace Tor"), person("nm3", "Ann Tress")],
    )

    result = oq.run(spark, cfg).collect()

    assert len(result) == 1
    (pair,) = result
    assert (pair.director, pair.actor, pair.n_collabs) == ("Dee Rector", "Ace Tor", 3)
    assert pair.delta == pytest.approx(1.5)
    # nm1's later films without nm2: tt4 (6.5, 2001) and tt5 (7.5, 2003).
    assert pair.baseline_avg_rating == pytest.approx(7.0)
    assert pair.excess == pytest.approx(0.5)

    outputs = Path(cfg.paths.outputs) / "open_question"
    summary = (outputs / "summary.md").read_text(encoding="utf-8")
    assert summary.startswith("# Open question - Recurring director-actor collaborations")
    for heading in ("## Parameters", "## Overall", "## Recurring pairs by collaboration rank"):
        assert heading in summary
    assert "Dee Rector" in summary
    for name in ("pairs", "by_rank", "by_count", "overall"):
        assert (outputs / f"collaborations_{name}.csv").is_file()
    assert (Path(cfg.paths.gold) / "open_question" / "collaboration_pairs").is_dir()
