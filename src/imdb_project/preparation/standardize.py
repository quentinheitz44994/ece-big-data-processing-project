r"""Standardisation of bronze tables: missing markers, types and arrays.

Shared by the quality checks and by the silver cleaning job, so that both look at
exactly the same typed values:

* ``\N``, empty and whitespace-only values become null, other strings are trimmed;
* scalar columns are converted with ``try_cast`` (a value that cannot be converted
  becomes null and its column name is recorded in ``_cast_errors``);
* multi-valued columns encoded as text become ``array<string>``.

Nothing is imputed: a value is either kept, converted or set to null.

Only native string functions are used (no regular expression on scalar values, no
lambda): these expressions run on every column of every row of tables holding up
to a hundred million rows.
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
#: Characters trimmed from both ends of every value: space, tab and
#: non-breaking space (U+00A0).
TRIM_CHARACTERS = " " + chr(0x09) + chr(0xA0)
#: Comma separator of multi-valued columns, with optional surrounding spaces.
_COMMA_SEPARATOR = " *, *"
#: Control character (0x02) separating the values of some akas columns.
_CTRL_B_SEPARATOR = chr(0x02)


def clean_string(value: Column) -> Column:
    r"""Return the trimmed string, or null when the raw value is missing.

    A value is missing when it is null, empty, made of whitespace only or equal
    to the IMDb marker ``\N``.
    """
    trimmed = F.btrim(value, F.lit(TRIM_CHARACTERS))
    return F.when((trimmed != "") & (trimmed != IMDB_NULL_MARKER), trimmed)


def is_missing(value: Column) -> Column:
    r"""Return whether a raw string is null, ``\N``, empty or whitespace-only."""
    return clean_string(value).isNull()


def parse_array(value: Column, encoding: str) -> Column:
    """Convert a text-encoded multi-valued column to ``array<string>``.

    Args:
        value: Raw string column.
        encoding: One of the ``ARRAY_*`` encodings of :mod:`imdb_project.common.schemas`.

    Returns:
        The array of non-empty items, or null when there is none.

    Raises:
        ValueError: If the encoding is unknown.
    """
    cleaned = clean_string(value)
    if encoding == ARRAY_JSON:
        items = F.array_compact(F.from_json(cleaned, "array<string>"))
    elif encoding == ARRAY_COMMA:
        items = F.split(cleaned, _COMMA_SEPARATOR)
    elif encoding == ARRAY_CTRL_B:
        items = F.split(cleaned, _CTRL_B_SEPARATOR)
    else:
        raise ValueError(f"Unknown array encoding: {encoding!r}")
    kept = F.array_remove(items, "")
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


def _has_value(spec: TableSpec, column: str) -> Column:
    """Whether the raw column holds something to convert (``[]`` is an empty array)."""
    cleaned = clean_string(F.col(column))
    if spec.arrays.get(column) == ARRAY_JSON:
        return cleaned.isNotNull() & (cleaned != "[]")
    return cleaned.isNotNull()


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
    # Conversions that can fail: scalar casts and JSON arrays. Splitting a
    # separated list always succeeds.
    fallible = [
        column
        for column in spec.columns
        if column in spec.casts or spec.arrays.get(column) == ARRAY_JSON
    ]
    corrupt = (
        F.col(CORRUPT_RECORD_COLUMN)
        if CORRUPT_RECORD_COLUMN in df.columns
        else F.lit(None).cast("string")
    )
    # Two projections so that each conversion is evaluated once: the first one
    # converts and records which raw values were present, the second one compares.
    converted = df.select(
        *[typed_column(spec, column).alias(column) for column in spec.columns],
        *[_has_value(spec, column).alias(f"__has_{column}") for column in fallible],
        corrupt.alias(CORRUPT_RECORD_COLUMN),
    )
    failures = [
        F.when(F.col(f"__has_{column}") & F.col(column).isNull(), F.lit(column))
        for column in fallible
    ]
    cast_errors = (
        F.array_compact(F.array(*failures)) if failures else F.array().cast("array<string>")
    )
    return converted.select(
        *spec.columns,
        cast_errors.alias(CAST_ERRORS_COLUMN),
        CORRUPT_RECORD_COLUMN,
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
