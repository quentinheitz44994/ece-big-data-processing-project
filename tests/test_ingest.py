from __future__ import annotations

import gzip
from pathlib import Path

import pytest
from pyspark.sql import functions as F

import factory
from imdb_project.common import io
from imdb_project.common.schemas import CORRUPT_RECORD_COLUMN, TABLES
from imdb_project.preparation import ingest


def test_schemas_cover_the_seven_files():
    assert len(TABLES) == 7
    assert {spec.source_file for spec in TABLES.values()} == {
        "name.basics.tsv.gz",
        "title.akas.tsv.gz",
        "title.basics.tsv.gz",
        "title.crew.tsv.gz",
        "title.episode.tsv.gz",
        "title.principals.tsv.gz",
        "title.ratings.tsv.gz",
    }
    for spec in TABLES.values():
        assert set(spec.primary_key) <= set(spec.columns)
        assert {f.dataType.simpleString() for f in spec.bronze_schema.fields} == {"string"}
        assert spec.silver_schema.fieldNames()[-1] == "dq_flags"
    silver = TABLES["title_basics"].silver_schema
    assert silver["runtimeMinutes"].dataType.simpleString() == "int"
    assert silver["isAdult"].dataType.simpleString() == "boolean"
    assert silver["genres"].dataType.simpleString() == "array<string>"


def test_bronze_keeps_every_row_as_strings(spark, bronze_cfg):
    for table, rows in factory.DATASET.items():
        bronze = io.read_parquet(spark, io.layer_path(bronze_cfg, "bronze", table))
        assert bronze.count() == len(rows), table
        assert bronze.columns == [*TABLES[table].columns, CORRUPT_RECORD_COLUMN]
        assert {t for _, t in bronze.dtypes} == {"string"}


def test_bronze_preserves_quotes_markers_and_control_characters(spark, bronze_cfg):
    titles = io.read_parquet(spark, io.layer_path(bronze_cfg, "bronze", "title_basics"))
    row = titles.filter(F.col("tconst") == "tt0000001").first()
    assert row["primaryTitle"] == 'Alpha "The Quote" Film'
    assert row["endYear"] == "\\N"

    akas = io.read_parquet(spark, io.layer_path(bronze_cfg, "bronze", "title_akas"))
    types = akas.filter((F.col("titleId") == "tt0000001") & (F.col("ordering") == "3")).first()
    assert types["types"] == "dvd\x02video"


def test_bronze_empty_field_is_null_and_whitespace_is_kept(spark, bronze_cfg):
    names = io.read_parquet(spark, io.layer_path(bronze_cfg, "bronze", "name_basics"))
    assert names.filter(F.col("nconst") == "nm0000011").first()["birthYear"] is None
    assert names.filter(F.col("nconst") == "nm0000009").first()["primaryName"] == "   "


def test_bronze_keeps_malformed_lines(spark, bronze_cfg):
    names = io.read_parquet(spark, io.layer_path(bronze_cfg, "bronze", "name_basics"))
    malformed = names.filter(F.col(CORRUPT_RECORD_COLUMN).isNotNull()).collect()
    assert len(malformed) == 1
    assert malformed[0]["nconst"] == "nm0000012"
    assert malformed[0]["knownForTitles"] is None
    assert malformed[0][CORRUPT_RECORD_COLUMN] == "nm0000012\tShort Row\t1970"


def test_ingestion_summary_report(bronze_cfg):
    report = Path(bronze_cfg.paths.outputs, "preparation", "ingestion_summary.md")
    text = report.read_text(encoding="utf-8")
    assert "| name_basics | name.basics.tsv.gz | 14 | 6 | 1 |" in text
    assert "| title_ratings | title.ratings.tsv.gz | 9 | 3 | 0 |" in text


def test_unexpected_header_is_rejected(spark, cfg):
    raw = Path(cfg.paths.raw)
    raw.mkdir(parents=True)
    with gzip.open(raw / "title.ratings.tsv.gz", "wt", encoding="utf-8") as handle:
        handle.write("tconst\tnumVotes\taverageRating\ntt0000001\t10\t5.0\n")
    with pytest.raises(Exception, match="(?i)header|schema"):
        ingest.run(spark, cfg, ["title_ratings"])


def test_missing_raw_file_is_reported(spark, cfg):
    with pytest.raises(FileNotFoundError, match="download_imdb.sh"):
        ingest.run(spark, cfg, ["title_ratings"])
