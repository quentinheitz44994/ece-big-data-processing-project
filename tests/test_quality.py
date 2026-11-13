from __future__ import annotations

from pathlib import Path

import pytest
from pyspark.sql import functions as F

from imdb_project.common.schemas import TABLES
from imdb_project.preparation import quality_checks, rules
from imdb_project.preparation.standardize import (
    CAST_ERRORS_COLUMN,
    load_standardized,
    standardize_table,
)

# Expected number of violating rows on the synthetic mini dataset (tests/factory.py).
EXPECTED = {
    ("DQ01", "name_basics"): 1,
    ("DQ02", "name_basics"): 2,
    ("DQ03", "title_principals"): 2,
    ("DQ04", "title_principals"): 1,
    ("DQ05:knownForTitles", "name_basics"): 1,
    ("DQ05:tconst", "title_principals"): 1,
    ("DQ05:nconst", "title_principals"): 1,
    ("DQ05:tconst", "title_ratings"): 1,
    ("DQ05:tconst", "title_crew"): 1,
    ("DQ05:directors", "title_crew"): 1,
    ("DQ05:tconst", "title_episode"): 1,
    ("DQ05:parentTconst", "title_episode"): 1,
    ("DQ05:titleId", "title_akas"): 1,
    ("DQ06", "title_basics"): 1,
    ("DQ07", "title_basics"): 1,
    ("DQ08", "title_basics"): 2,
    ("DQ09", "name_basics"): 1,
    ("DQ09", "title_akas"): 1,
    ("DQ09", "title_basics"): 2,
    ("DQ09", "title_principals"): 1,
    ("DQ10", "name_basics"): 4,
    ("DQ10", "title_principals"): 2,
    ("DQ11", "title_episode"): 1,
    ("DQ12", "title_ratings"): 2,
    ("DQ13", "title_basics"): 1,
    ("DQ14", "title_episode"): 2,
    ("DQ15", "name_basics"): 1,
}


@pytest.fixture(scope="module")
def quality_cfg(bronze_cfg):
    return bronze_cfg.with_overrides({"preparation.quality.reference_year": 2026})


def test_standardize_types_and_missing_markers(spark):
    spec = TABLES["title_basics"]
    df = spark.createDataFrame(
        [
            ("tt1", "movie", " Padded ", "\\N", "1", "1999", "", "90", "Drama, Comedy,"),
            ("tt2", "movie", "   ", "T", "2", "19x9", "\\N", "-5", "\\N"),
        ],
        ",".join(f"{column} string" for column in spec.columns),
    )
    first, second = standardize_table(df, spec).orderBy("tconst").collect()

    assert first["primaryTitle"] == "Padded"
    assert first["originalTitle"] is None
    assert first["isAdult"] is True
    assert (first["startYear"], first["endYear"], first["runtimeMinutes"]) == (1999, None, 90)
    assert first["genres"] == ["Drama", "Comedy"]
    assert first[CAST_ERRORS_COLUMN] == []

    assert second["primaryTitle"] is None
    assert second["isAdult"] is None
    assert second["startYear"] is None
    assert second["runtimeMinutes"] == -5
    assert second["genres"] is None
    assert sorted(second[CAST_ERRORS_COLUMN]) == ["isAdult", "startYear"]


def test_standardize_array_encodings(spark):
    akas = standardize_table(
        spark.createDataFrame(
            [("tt1", "1", "T", "US", "en", "dvd\x02video", "\\N", "0")],
            ",".join(f"{column} string" for column in TABLES["title_akas"].columns),
        ),
        TABLES["title_akas"],
    ).first()
    assert akas["types"] == ["dvd", "video"]
    assert akas["attributes"] is None
    assert akas["isOriginalTitle"] is False
    assert akas["ordering"] == 1

    principals = standardize_table(
        spark.createDataFrame(
            [
                ("tt1", "1", "nm1", "actor", "\\N", '["A","B, C"]'),
                ("tt1", "2", "nm2", "actor", "\\N", "[]"),
                ("tt1", "3", "nm3", "actor", "\\N", "[broken"),
            ],
            ",".join(f"{column} string" for column in TABLES["title_principals"].columns),
        ),
        TABLES["title_principals"],
    )
    rows = {row["ordering"]: row for row in principals.collect()}
    assert rows[1]["characters"] == ["A", "B, C"]
    assert rows[2]["characters"] is None and rows[2][CAST_ERRORS_COLUMN] == []
    assert rows[3]["characters"] is None and rows[3][CAST_ERRORS_COLUMN] == ["characters"]


def test_rule_ids_are_unique_per_table():
    all_rules = rules.build_rules()
    pairs = [(rule.rule_id, rule.table) for rule in all_rules]
    assert len(pairs) == len(set(pairs))
    assert {rule.rule_id.split(":")[0] for rule in all_rules} == {
        f"DQ{number:02d}" for number in range(1, 16)
    }
    assert all(rule.table in TABLES for rule in all_rules)


def test_orphan_and_duplicate_key_builders(spark):
    child = spark.createDataFrame([("a",), ("b",), ("b",), (None,)], "fk string")
    parent = spark.createDataFrame([("a",), ("c",)], "pk string")
    assert [row.fk for row in rules.orphan_keys(child, "fk", parent, "pk").collect()] == ["b"]

    owners = spark.createDataFrame(
        [("r1", ["a", "x"]), ("r2", ["a"]), ("r3", None)], "id string, items array<string>"
    )
    keys = rules.orphan_array_owner_keys(owners, "items", ["id"], parent, "pk")
    assert [row.id for row in keys.collect()] == ["r1"]

    dup = spark.createDataFrame(
        [("k", 1), ("k", 1), ("j", 1), (None, 2), (None, 2)], "a string, b int"
    )
    assert [tuple(row) for row in rules.duplicate_keys(dup, ["a", "b"]).collect()] == [("k", 1)]


def test_credit_before_birth_ignores_running_series(spark, quality_cfg):
    tables = {
        "name_basics": spark.createDataFrame(
            [("nm1", 1990, None)], "nconst string, birthYear int, deathYear int"
        ),
        "title_basics": spark.createDataFrame(
            [
                ("tt1", "movie", 1985, None),
                ("tt2", "tvSeries", 1985, None),
                ("tt3", "tvSeries", 1980, 1988),
                ("tt4", "tvSeries", 1985, 2010),
            ],
            "tconst string, titleType string, startYear int, endYear int",
        ),
        "title_principals": spark.createDataFrame(
            [(t, 1, "nm1", "actor", None, None) for t in ("tt1", "tt2", "tt3", "tt4")],
            "tconst string, ordering int, nconst string, category string, job string, "
            "characters array<string>",
        ),
    }
    keys = rules.credit_before_birth_keys(tables, quality_cfg)
    assert sorted(row.tconst for row in keys.collect()) == ["tt1", "tt3"]


def test_posthumous_rule_exemptions(spark, quality_cfg):
    tables = {
        "name_basics": spark.createDataFrame(
            [("nm1", 1900, 1950)], "nconst string, birthYear int, deathYear int"
        ),
        "title_basics": spark.createDataFrame(
            [("tt1", "movie", 2000, None), ("tt2", "movie", 1954, None)],
            "tconst string, titleType string, startYear int, endYear int",
        ),
        "title_principals": spark.createDataFrame(
            [
                ("tt1", 1, "nm1", "actor", None, ["Hero"]),
                ("tt1", 2, "nm1", "writer", "novel", None),
                ("tt1", 3, "nm1", "archive_footage", None, None),
                ("tt1", 4, "nm1", "self", None, ["Self (archive footage)"]),
                ("tt1", 5, "nm1", "actor", "archive sound", None),
                ("tt2", 1, "nm1", "actor", None, None),
            ],
            "tconst string, ordering int, nconst string, category string, job string, "
            "characters array<string>",
        ),
    }
    keys = rules.posthumous_credit_keys(tables, quality_cfg)
    assert [(row.tconst, row.ordering) for row in keys.collect()] == [("tt1", 1)]


def test_evaluate_rules_on_mini_dataset(spark, quality_cfg):
    results = quality_checks.run(spark, quality_cfg)
    counts = {(r.rule_id, r.table): r.n_violations for r in results}
    assert {key: value for key, value in counts.items() if value} == EXPECTED

    by_key = {(r.rule_id, r.table): r for r in results}
    dq01 = by_key[("DQ01", "name_basics")]
    assert dq01.n_rows == 14
    assert dq01.pct_of_table == pytest.approx(100 / 14)
    assert dq01.sample_rows[0][0] == "nm0000003"
    assert by_key[("DQ10", "title_basics")].sample_rows == []

    out = Path(quality_cfg.paths.outputs, "preparation")
    report = (out / "quality_report.md").read_text("utf-8")
    assert "| reference_year | 2026 |" in report
    assert "| DQ12 | title_ratings |" in report
    samples = (out / "quality_samples.md").read_text("utf-8")
    assert "## DQ05:titleId - title_akas" in samples
    assert "## DQ10 - title_basics" not in samples


def test_row_rule_conditions_handle_nulls(spark, quality_cfg):
    tables = load_standardized(spark, quality_cfg)
    all_rules = rules.build_rules()
    for rule in all_rules:
        if isinstance(rule, rules.RowRule):
            flagged = tables[rule.table].where(rule.condition(quality_cfg)).count()
            assert flagged == EXPECTED.get((rule.rule_id, rule.table), 0), rule.rule_id
    hal = tables["name_basics"].where(F.col("nconst") == "nm0000008").first()
    assert hal["birthYear"] is None and hal["primaryProfession"] is None
