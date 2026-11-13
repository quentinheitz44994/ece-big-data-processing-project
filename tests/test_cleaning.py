from __future__ import annotations

from pathlib import Path

from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.common.schemas import TABLES
from imdb_project.preparation import cleaning

# table: (bronze rows, silver rows, quarantined rows, silver rows with flags)
EXPECTED_OVERVIEW = {
    "name_basics": (14, 10, 4, 6),
    "title_akas": (5, 4, 1, 1),
    "title_basics": (13, 13, 0, 7),
    "title_crew": (5, 4, 1, 1),
    "title_episode": (5, 4, 1, 3),
    "title_principals": (10, 6, 4, 4),
    "title_ratings": (9, 8, 1, 2),
}


def _silver(spark, cfg, table):
    return io.read_parquet(spark, io.layer_path(cfg, "silver", table))


def _quarantine(spark, cfg, table):
    return io.read_parquet(spark, io.layer_path(cfg, "quarantine", table))


def test_resolve_duplicates_keeps_one_identical_copy(spark):
    spec = TABLES["title_ratings"]
    rows = [
        ("tt1", 5.0, 10),
        ("tt1", 5.0, 10),
        ("tt1", 5.0, 10),
        ("tt2", 6.0, 10),
        ("tt2", 6.5, 10),
    ]
    df = spark.createDataFrame(rows, "tconst string, averageRating double, numVotes int")
    resolved = cleaning.resolve_duplicates(df, spec).collect()
    reasons = sorted((row["tconst"], row["__dup_reason"] or "kept") for row in resolved)
    assert reasons == [
        ("tt1", cleaning.REASON_EXACT_DUPLICATE),
        ("tt1", cleaning.REASON_EXACT_DUPLICATE),
        ("tt1", "kept"),
        ("tt2", cleaning.REASON_CONFLICTING_KEY),
        ("tt2", cleaning.REASON_CONFLICTING_KEY),
    ]


def test_apply_corrections_only_nulls_invalid_values(spark, cfg):
    df = spark.createDataFrame(
        [("tt1", 0.5, 0), ("tt2", 7.0, 10), ("tt3", None, -3)],
        "tconst string, averageRating double, numVotes int",
    )
    corrections = [c for c in cleaning.build_corrections() if c.table == "title_ratings"]
    rows = {r["tconst"]: r for r in cleaning.apply_corrections(df, corrections, cfg).collect()}
    assert (rows["tt1"]["averageRating"], rows["tt1"]["numVotes"]) == (None, None)
    assert (rows["tt2"]["averageRating"], rows["tt2"]["numVotes"]) == (7.0, 10)
    assert (rows["tt3"]["averageRating"], rows["tt3"]["numVotes"]) == (None, None)


def test_silver_and_quarantine_row_counts(spark, silver_cfg, cleaning_summary):
    overview = {
        row[0]: (row[1], row[2], row[3], row[5])
        for row in cleaning_summary["Rows before and after cleaning"]
    }
    assert overview == EXPECTED_OVERVIEW
    for table, (_, silver_rows, quarantined_rows, _) in EXPECTED_OVERVIEW.items():
        assert _silver(spark, silver_cfg, table).count() == silver_rows
        assert _quarantine(spark, silver_cfg, table).count() == quarantined_rows


def test_silver_schema_is_typed(spark, silver_cfg):
    for table, spec in TABLES.items():
        silver = _silver(spark, silver_cfg, table)
        expected = {f.name: f.dataType.simpleString() for f in spec.silver_schema.fields}
        actual = {f.name: f.dataType.simpleString() for f in silver.schema.fields}
        assert actual == expected, table
    titles = _silver(spark, silver_cfg, "title_basics")
    alpha = titles.where(F.col("tconst") == "tt0000001").first()
    assert alpha["genres"] == ["Drama", "Comedy"]
    assert alpha["isAdult"] is False
    assert alpha["endYear"] is None
    assert alpha["dq_flags"] == []


def test_flags_and_corrections(spark, silver_cfg):
    titles = {r["tconst"]: r for r in _silver(spark, silver_cfg, "title_basics").collect()}
    assert titles["tt0000002"]["dq_flags"] == ["DQ08"]
    assert titles["tt0000002"]["runtimeMinutes"] is None  # <= 0 corrected to null
    assert titles["tt0000003"]["dq_flags"] == ["DQ08"]
    assert titles["tt0000003"]["runtimeMinutes"] == 5000  # aberrant value only flagged
    assert titles["tt0000010"]["dq_flags"] == ["DQ09"]
    assert titles["tt0000005"]["dq_flags"] == ["DQ13"]

    names = {r["nconst"]: r for r in _silver(spark, silver_cfg, "name_basics").collect()}
    assert names["nm0000001"]["dq_flags"] == ["DQ10"]  # the single copy kept
    assert names["nm0000005"]["birthYear"] is None  # future birth year corrected
    assert names["nm0000005"]["dq_flags"] == ["DQ02"]
    assert names["nm0000007"]["dq_flags"] == ["DQ05:knownForTitles"]
    assert "nm0000010" not in names and "nm0000012" not in names

    ratings = {r["tconst"]: r for r in _silver(spark, silver_cfg, "title_ratings").collect()}
    assert ratings["tt0000005"]["averageRating"] is None
    assert ratings["tt0000004"]["numVotes"] is None

    principals = _silver(spark, silver_cfg, "title_principals")
    flags = {(r["tconst"], r["ordering"]): r["dq_flags"] for r in principals.collect()}
    assert flags[("tt0000001", 1)] == ["DQ10"]
    assert flags[("tt0000001", 3)] == ["DQ04"]
    assert flags[("tt0000005", 1)] == ["DQ03"]
    assert flags[("tt0000003", 1)] == []


def test_quarantine_reasons(spark, silver_cfg, cleaning_summary):
    reasons = {(r[0], r[1]): r[2] for r in cleaning_summary["Quarantined rows per reason"]}
    assert reasons == {
        ("name_basics", "DQ10:conflicting_primary_key"): 2,
        ("name_basics", "DQ10:exact_duplicate"): 1,
        ("name_basics", "DQ15"): 1,
        ("title_akas", "DQ05:titleId"): 1,
        ("title_crew", "DQ05:tconst"): 1,
        ("title_episode", "DQ05:parentTconst;DQ05:tconst"): 1,
        # nm0000010 was quarantined (conflicting key), so its credit is an orphan in silver.
        ("title_principals", "DQ05:nconst"): 2,
        ("title_principals", "DQ05:tconst"): 1,
        ("title_principals", "DQ10:exact_duplicate"): 1,
        ("title_ratings", "DQ05:tconst"): 1,
    }
    malformed = _quarantine(spark, silver_cfg, "name_basics").where(F.col("dq_reason") == "DQ15")
    assert malformed.first()["_corrupt_record"] == "nm0000012\tShort Row\t1970"


def test_cleaning_summary_reports(silver_cfg, cleaning_summary):
    corrections = {(r[0], r[1]): r[3] for r in cleaning_summary["Deterministic corrections"]}
    assert corrections[("title_basics", "runtimeMinutes")] == 1
    assert corrections[("title_ratings", "averageRating")] == 1
    assert corrections[("title_ratings", "numVotes")] == 1
    assert corrections[("name_basics", "birthYear")] == 1
    assert corrections[("name_basics", "deathYear")] == 0

    out = Path(silver_cfg.paths.outputs, "preparation")
    text = (out / "cleaning_summary.md").read_text("utf-8")
    assert "## Rows before and after cleaning" in text
    assert "| title_principals | 10 | 6 | 4 |" in text
    assert (out / "cleaning_rows_before_and_after_cleaning.csv").is_file()


def test_silver_title_basics_is_partitioned(silver_cfg):
    root = Path(silver_cfg.paths.silver, "title_basics")
    assert {p.name for p in root.iterdir() if p.is_dir()} >= {
        "titleType=movie",
        "titleType=tvSeries",
        "titleType=tvEpisode",
        "titleType=short",
    }
