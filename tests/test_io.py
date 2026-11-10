from __future__ import annotations

import datetime as dt

from imdb_project.common import io


def test_format_cell_types():
    assert io.format_cell(None) == ""
    assert io.format_cell(True) == "true"
    assert io.format_cell(3) == "3"
    assert io.format_cell(3.14159) == "3.14"
    assert io.format_cell(3.14159, ".4f") == "3.1416"
    assert io.format_cell(float("nan")) == "nan"
    assert io.format_cell(["a", "b"]) == "a, b"
    assert io.format_cell("line\nbreak  x") == "line break x"
    assert io.format_cell(dt.date(2026, 11, 10)) == "2026-11-10"
    assert io.format_cell({"k": [1, 2]}) == '{"k": [1, 2]}'


def test_markdown_table_escapes_pipes():
    table = io.markdown_table(["title", "n"], [["a|b", 1], [None, 2.5]])
    assert table.splitlines() == [
        "| title | n |",
        "| --- | --- |",
        "| a\\|b | 1 |",
        "|  | 2.50 |",
    ]


def test_write_markdown_and_csv(tmp_path):
    md = io.write_markdown(
        tmp_path / "out" / "report.md",
        "Title",
        [io.ReportTable(["a"], [[1]], title="First", note="Showing 1 of 1 rows")],
        parameters={"min_votes": 1000, "genres": ["Drama", "Comedy"]},
    )
    text = md.read_text(encoding="utf-8")
    assert text.startswith("# Title\n\n## Parameters\n\n| parameter | value |")
    assert "| min_votes | 1000 |" in text
    assert "| genres | Drama, Comedy |" in text
    assert "## First\n\n_Showing 1 of 1 rows_\n\n| a |" in text
    assert "\r" not in text

    csv_path = io.write_csv(
        tmp_path / "out" / "t.csv", ["x", "y", "z"], [[1, 0.1, ["a", "b"]], [None, 2.0, []]]
    )
    assert csv_path.read_text(encoding="utf-8") == "x,y,z\n1,0.1,a|b\n,2.0,\n"


def test_layer_and_output_paths(cfg):
    assert io.layer_path(cfg, "bronze", "title_basics").endswith("bronze/title_basics")
    out = io.output_path(cfg, "preparation", "x.md")
    assert out.parent.is_dir()


def test_parquet_roundtrip_and_collect(spark, tmp_path):
    df = spark.createDataFrame([(1, "a"), (2, "b"), (3, "c")], ["id", "v"])
    path = str(tmp_path / "t")
    io.write_parquet(df, path, partition_by=["v"])
    back = io.read_parquet(spark, path)
    assert back.count() == 3
    columns, rows = io.collect_rows(back.orderBy("id"), limit=2)
    assert columns == ["id", "v"]
    assert rows == [[1, "a"], [2, "b"]]
