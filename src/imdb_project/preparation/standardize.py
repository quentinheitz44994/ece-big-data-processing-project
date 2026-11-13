r"""Standardisation of bronze tables: missing markers, types and arrays.

Shared by the quality checks and by the silver cleaning job, so that both look at
exactly the same typed values:

* ``\N``, empty and whitespace-only values become null, other strings are trimmed;
* scalar columns are converted with ``try_cast`` (a value that cannot be converted
  becomes null and its column name is recorded in ``_cast_errors``);
* multi-valued columns encoded as text become ``array<string>``.

Nothing is imputed: a value is either kept, converted or set to null.
"""

from __future__ import annotations

from collections.abc import Mapping

from pyspark.sql import Column, DataFrame, SparkSession
from pyspark.sql import functions as F

from imdb_project.common import io
from imdb_project.common.config import Config
from imdb_project.common.schemas import (
    ARRAY_COMMA,
    ARRAY_CTRL_B,
    ARRAY_JSON,
    CORRUPT_RECORD_COLUMN,
    TABLES,
    TableSpec,
)

IMDB_NULL_MARKER = "\\N"
#: Technical column listing the columns of a row whose value could not be converted.
CAST_ERRORS_COLUMN = "_cast_errors"

_ARRAY_SEPARATORS = {ARRAY_COMMA: ",", ARRAY_CTRL_B: "\u0002"}
#: Characters treated like spaces when testing for a blank value: non-breaking
#: space (U+00A0) and tab. Ordinary spaces are handled by ``trim``.
_EXTRA_SPACES = chr(0xA0) + chr(0x09)


def is_missing(value: Column) -> Column:
    r"""Return whether a raw string is null, ``\N``, empty or whitespace-only.

    Implemented with ``translate`` and ``trim`` rather than a regular expression:
    the predicate runs on every column of every row of tables holding up to a
    hundred million rows.
    """
    blank = F.trim(F.translate(value, _EXTRA_SPACES, "  ")) == ""
    return value.isNull() | (value == IMDB_NULL_MARKER) | blank


def clean_string(value: Column) -> Column:
    """Return the trimmed string, or null when the raw value is missing."""
    return F.when(~is_missing(value), F.trim(value))


def parse_array(value: Column, encoding: str) -> Column:
    """Convert a text-encoded multi-valued column to ``array<string>``.

    Args:
        value: Raw string column.
        encoding: One of the ``ARRAY_*`` encodings of :mod:`imdb_project.common.schemas`.

    Returns:
        The array of trimmed, non-empty items, or null when there is none.
    """
    cleaned = clean_string(value)
    if encoding == ARRAY_JSON:
        items = F.from_json(cleaned, "array<string>")
    else:
        items = F.split(cleaned, _ARRAY_SEPARATORS[encoding])
    kept = F.filter(
        F.transform(items, lambda item: F.trim(item)),
        lambda item: item.isNotNull() & (item != "") & (item != IMDB_NULL_MARKER),
    )
    return F.when(F.size(kept) > 0, kept)


def typed_column(spec: TableSpec, column: str) -> Column:
    """Return the silver-typed expression of one raw column."""
    raw = F.col(column)
    if column in spec.arrays:
        return parse_array(raw, spec.arrays[column])
    value = clean_string(raw)
    target = spec.casts.get(column)
    if target == "boolean":
        return F.when(value == "1", F.lit(True)).when(value == "0", F.lit(False))
    if target:
        return value.try_cast(target)
    return value


def _is_missing_raw(spec: TableSpec, column: str) -> Column:
    raw = F.col(column)
    if column in spec.arrays:
        return is_missing(raw) | (F.trim(raw) == "[]")
    return is_missing(raw)


def standardize_table(df: DataFrame, spec: TableSpec) -> DataFrame:
    """Standardise one bronze table.

    Args:
        df: Bronze table (string columns, optional ``_corrupt_record``).
        spec: Specification of the table.

    Returns:
        A DataFrame with the typed columns of ``spec``, ``_cast_errors``
        (``array<string>``: columns holding a value that could not be converted)
        and ``_corrupt_record``.
    """
    converted = [column for column in spec.columns if column in spec.casts or column in spec.arrays]
    failures = [
        F.when(~_is_missing_raw(spec, column) & typed_column(spec, column).isNull(), F.lit(column))
        for column in converted
    ]
    cast_errors = (
        F.array_compact(F.array(*failures)) if failures else F.array().cast("array<string>")
    )
    corrupt = (
        F.col(CORRUPT_RECORD_COLUMN)
        if CORRUPT_RECORD_COLUMN in df.columns
        else F.lit(None).cast("string")
    )
    return df.select(
        *[typed_column(spec, column).alias(column) for column in spec.columns],
        cast_errors.alias(CAST_ERRORS_COLUMN),
        corrupt.alias(CORRUPT_RECORD_COLUMN),
    )


def load_standardized(spark: SparkSession, cfg: Config) -> Mapping[str, DataFrame]:
    """Load every bronze table and standardise it (lazily).

    Args:
        spark: Active Spark session.
        cfg: Project configuration.

    Returns:
        Mapping of table name to standardised DataFrame.
    """
    return {
        name: standardize_table(io.read_parquet(spark, io.layer_path(cfg, "bronze", name)), spec)
        for name, spec in TABLES.items()
    }
