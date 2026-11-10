from __future__ import annotations

from pathlib import Path

import pytest

from imdb_project.preparation import null_profile


def _by_column(rows):
    return {(row["table"], row["column"]): row for row in rows}


def test_profile_table_counts_each_kind_of_missing_value(spark):
    df = spark.createDataFrame(
        [
            ("a", "x,y"),
            (None, "\\N"),
            ("\\N", "[]"),
            ("", " [] "),
            ("  ", ""),
            (" ", "z"),
            ("b", None),
        ],
        "scalar string, multi string",
    )
    rows = _by_column(null_profile.profile_table(df, "t", ["scalar", "multi"], {"multi"}))

    scalar = rows[("t", "scalar")]
    assert scalar["n_total"] == 7
    assert (scalar["n_null"], scalar["n_backslash_n"], scalar["n_empty"]) == (1, 1, 1)
    assert (scalar["n_whitespace"], scalar["n_empty_array"]) == (2, 0)
    assert scalar["n_missing_total"] == 5
    assert scalar["pct_missing"] == pytest.approx(100 * 5 / 7)

    multi = rows[("t", "multi")]
    assert (multi["n_null"], multi["n_backslash_n"], multi["n_empty"]) == (1, 1, 1)
    assert (multi["n_whitespace"], multi["n_empty_array"]) == (0, 2)
    assert multi["n_missing_total"] == 5


def test_profile_table_on_empty_dataframe(spark):
    df = spark.createDataFrame([], "c string")
    (row,) = null_profile.profile_table(df, "t", ["c"])
    assert row["n_total"] == 0
    assert row["pct_missing"] == 0.0


def test_top_missing_columns_is_deterministic():
    profile = [
        {"table": "b", "column": "y", "pct_missing": 50.0, "n_missing_total": 5},
        {"table": "a", "column": "x", "pct_missing": 50.0, "n_missing_total": 5},
        {"table": "c", "column": "z", "pct_missing": 50.0, "n_missing_total": 9},
        {"table": "d", "column": "w", "pct_missing": 99.0, "n_missing_total": 1},
        {"table": "e", "column": "v", "pct_missing": 1.0, "n_missing_total": 100},
    ]
    top = null_profile.top_missing_columns(profile, 3)
    assert [(row["table"], row["column"]) for row in top] == [("d", "w"), ("c", "z"), ("a", "x")]


def test_run_profiles_the_mini_dataset(spark, bronze_cfg):
    rows = _by_column(null_profile.run(spark, bronze_cfg))
    assert len(rows) == 39  # total number of columns of the seven tables

    end_year = rows[("title_basics", "endYear")]
    assert end_year["n_total"] == 13
    assert end_year["n_backslash_n"] == 12

    birth = rows[("name_basics", "birthYear")]
    assert birth["n_null"] == 1  # the empty raw field
    assert birth["n_backslash_n"] == 1

    known_for = rows[("name_basics", "knownForTitles")]
    assert known_for["n_null"] == 1  # column absent from the malformed short line
    assert rows[("name_basics", "primaryName")]["n_whitespace"] == 1

    out = Path(bronze_cfg.paths.outputs, "preparation")
    assert "| title_basics | endYear | 13 |" in (out / "null_profile.md").read_text("utf-8")
    top = (out / "top5_null_columns.md").read_text("utf-8")
    assert top.count("\n| ") == 4 + 7  # parameters table (4 lines) and top-5 table (7 lines)
    assert (out / "null_profile.csv").read_text("utf-8").count("\n") == 40
