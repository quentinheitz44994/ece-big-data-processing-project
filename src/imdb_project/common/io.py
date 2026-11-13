"""I/O helpers: layer paths, Parquet read/write and report tables (Markdown, CSV).

Report files written under ``outputs/`` only contain generated material: a title,
the parameters used by the job and result tables. They never contain prose.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path, PurePosixPath
from typing import Any

from pyspark.sql import DataFrame, SparkSession

from imdb_project.common.config import Config

DEFAULT_FLOAT_FORMAT = ".2f"


@dataclass(frozen=True)
class ReportTable:
    """A result table of a generated report.

    Attributes:
        columns: Column names.
        rows: Row values, aligned with ``columns``.
        title: Optional heading printed above the table.
        note: Optional one-line, programmatically built caption
            (e.g. ``"Showing 20 of 1234 rows"``).
        float_format: Optional format spec overriding the report default.
    """

    columns: Sequence[str]
    rows: Sequence[Sequence[Any]]
    title: str | None = None
    note: str | None = None
    float_format: str | None = None


# --------------------------------------------------------------------------- paths


def layer_path(cfg: Config, layer: str, *parts: str) -> str:
    """Build a path inside a data layer declared in ``paths`` of the settings.

    Args:
        cfg: Project configuration.
        layer: Key of the ``paths`` section (``raw``, ``bronze``, ``silver``...).
        *parts: Sub-directories / file name appended to the layer root.

    Returns:
        The POSIX path as a string (jobs run in Linux containers).
    """
    return str(PurePosixPath(cfg.require(f"paths.{layer}"), *parts))


def output_path(cfg: Config, *parts: str) -> Path:
    """Return a path under the versioned ``outputs/`` folder, creating parents."""
    path = Path(cfg.require("paths.outputs"), *parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


# ------------------------------------------------------------------------- parquet


def read_parquet(spark: SparkSession, path: str) -> DataFrame:
    """Read a Parquet dataset."""
    return spark.read.parquet(path)


def write_parquet(
    df: DataFrame,
    path: str,
    mode: str = "overwrite",
    partition_by: Sequence[str] | None = None,
    max_records_per_file: int | None = None,
) -> None:
    """Write a DataFrame as Parquet.

    Args:
        df: Data to write.
        path: Target directory.
        mode: Spark save mode.
        partition_by: Optional partition columns.
        max_records_per_file: Optional cap on the number of rows per file.
    """
    writer = df.write.mode(mode)
    if max_records_per_file:
        writer = writer.option("maxRecordsPerFile", int(max_records_per_file))
    if partition_by:
        writer = writer.partitionBy(*partition_by)
    writer.parquet(path)


def collect_rows(df: DataFrame, limit: int | None = None) -> tuple[list[str], list[list[Any]]]:
    """Collect a (small) DataFrame to the driver as column names and row lists.

    Args:
        df: An aggregate or an already limited DataFrame.
        limit: Optional maximum number of rows to bring back.

    Returns:
        ``(columns, rows)``.
    """
    limited = df.limit(limit) if limit is not None else df
    return list(df.columns), [list(row) for row in limited.collect()]


# ------------------------------------------------------------------ report writers


def _plain(value: Any) -> Any:
    """Convert Spark ``Row`` / nested containers to JSON-friendly Python values."""
    if hasattr(value, "asDict"):
        return {key: _plain(item) for key, item in value.asDict().items()}
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_plain(item) for item in value]
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (dt.datetime, dt.date)):
        return value.isoformat()
    return value


def format_cell(value: Any, float_format: str = DEFAULT_FLOAT_FORMAT, list_sep: str = ", ") -> str:
    """Render one value as text for a report cell.

    Args:
        value: Any value collected from Spark.
        float_format: Format spec applied to floats and decimals.
        list_sep: Separator used to join the items of array values.

    Returns:
        A single-line string (``""`` for ``None``).
    """
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (float, Decimal)):
        number = float(value)
        if math.isnan(number) or math.isinf(number):
            return str(number)
        return format(number, float_format)
    if isinstance(value, (dt.datetime, dt.date)):
        return value.isoformat()
    plain = _plain(value)
    if isinstance(plain, list):
        if all(not isinstance(item, (dict, list)) for item in plain):
            return list_sep.join(format_cell(item, float_format, list_sep) for item in plain)
        return json.dumps(plain, ensure_ascii=False)
    if isinstance(plain, dict):
        return json.dumps(plain, ensure_ascii=False)
    return " ".join(str(plain).split())


def _md_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("|", "\\|")


def markdown_table(
    columns: Sequence[str],
    rows: Sequence[Sequence[Any]],
    float_format: str = DEFAULT_FLOAT_FORMAT,
) -> str:
    """Render a GitHub-flavoured Markdown table.

    Args:
        columns: Header names.
        rows: Row values.
        float_format: Format spec applied to floats.

    Returns:
        The table as text (header and separator only when ``rows`` is empty).
    """
    lines = [
        "| " + " | ".join(_md_escape(str(column)) for column in columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = (_md_escape(format_cell(value, float_format)) for value in row)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_markdown(
    path: str | Path,
    title: str,
    tables: Sequence[ReportTable],
    parameters: Mapping[str, Any] | None = None,
    float_format: str = DEFAULT_FLOAT_FORMAT,
) -> Path:
    """Write a generated report: title, parameters table and result tables.

    Args:
        path: Target ``.md`` file.
        title: First-level heading of the file.
        tables: Result tables, written in order.
        parameters: Parameters used by the job, printed before the tables.
        float_format: Default float format of the tables.

    Returns:
        The path written.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    blocks: list[str] = [f"# {title}"]
    if parameters:
        rows = [[key, format_cell(value, "g")] for key, value in parameters.items()]
        blocks.append("## Parameters")
        blocks.append(markdown_table(["parameter", "value"], rows))
    for table in tables:
        if table.title:
            blocks.append(f"## {table.title}")
        if table.note:
            blocks.append(f"_{table.note}_")
        blocks.append(markdown_table(table.columns, table.rows, table.float_format or float_format))
    target.write_text("\n\n".join(blocks) + "\n", encoding="utf-8", newline="\n")
    return target


def write_csv(path: str | Path, columns: Sequence[str], rows: Sequence[Sequence[Any]]) -> Path:
    """Write rows as a UTF-8 CSV file (full float precision, ``|``-joined arrays).

    Args:
        path: Target ``.csv`` file.
        columns: Header names.
        rows: Row values.

    Returns:
        The path written.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(columns)
        for row in rows:
            writer.writerow(
                [
                    repr(value) if isinstance(value, float) else format_cell(value, "g", "|")
                    for value in row
                ]
            )
    return target
