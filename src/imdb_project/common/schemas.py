"""Table specifications of the seven IMDb datasets.

One :class:`TableSpec` per file describes the raw columns, the primary key and
how each column is typed in the silver layer. The bronze schema keeps every
column as a string so that nothing is lost or silently coerced at ingestion.

Reference: https://developer.imdb.com/non-commercial-datasets/
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from pyspark.sql.types import (
    ArrayType,
    BooleanType,
    DataType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

#: Column receiving the raw line of rows whose number of fields is wrong.
CORRUPT_RECORD_COLUMN = "_corrupt_record"
#: Column of the silver tables listing the quality rules violated by a row.
DQ_FLAGS_COLUMN = "dq_flags"

#: Encodings of multi-valued columns in the raw files.
ARRAY_COMMA = "comma"  # a,b,c
ARRAY_CTRL_B = "ctrl_b"  # values separated by the 0x02 control character
ARRAY_JSON = "json"  # ["a","b"]

_SILVER_TYPES: Mapping[str, DataType] = MappingProxyType(
    {"int": IntegerType(), "double": DoubleType(), "boolean": BooleanType()}
)


@dataclass(frozen=True)
class TableSpec:
    """Description of one IMDb table.

    Attributes:
        name: Table name used for the bronze / silver folders.
        source_file: File name on https://datasets.imdbws.com/.
        columns: Raw column names, in file order.
        primary_key: Columns identifying a row.
        casts: Scalar columns typed in silver (``int``, ``double``, ``boolean``).
        arrays: Multi-valued columns and their raw encoding.
        partition_by: Partition columns of the silver table.
    """

    name: str
    source_file: str
    columns: tuple[str, ...]
    primary_key: tuple[str, ...]
    casts: Mapping[str, str] = field(default_factory=dict)
    arrays: Mapping[str, str] = field(default_factory=dict)
    partition_by: tuple[str, ...] = ()

    @property
    def bronze_schema(self) -> StructType:
        """All-string schema used to read the raw file (plus the corrupt column)."""
        fields = [StructField(column, StringType(), True) for column in self.columns]
        fields.append(StructField(CORRUPT_RECORD_COLUMN, StringType(), True))
        return StructType(fields)

    @property
    def silver_schema(self) -> StructType:
        """Typed schema of the silver table (with the ``dq_flags`` column)."""
        fields = []
        for column in self.columns:
            if column in self.arrays:
                data_type: DataType = ArrayType(StringType(), True)
            else:
                data_type = (
                    _SILVER_TYPES[self.casts[column]] if column in self.casts else StringType()
                )
            fields.append(StructField(column, data_type, True))
        fields.append(StructField(DQ_FLAGS_COLUMN, ArrayType(StringType(), False), False))
        return StructType(fields)


NAME_BASICS = TableSpec(
    name="name_basics",
    source_file="name.basics.tsv.gz",
    columns=(
        "nconst",
        "primaryName",
        "birthYear",
        "deathYear",
        "primaryProfession",
        "knownForTitles",
    ),
    primary_key=("nconst",),
    casts={"birthYear": "int", "deathYear": "int"},
    arrays={"primaryProfession": ARRAY_COMMA, "knownForTitles": ARRAY_COMMA},
)

TITLE_AKAS = TableSpec(
    name="title_akas",
    source_file="title.akas.tsv.gz",
    columns=(
        "titleId",
        "ordering",
        "title",
        "region",
        "language",
        "types",
        "attributes",
        "isOriginalTitle",
    ),
    primary_key=("titleId", "ordering"),
    casts={"ordering": "int", "isOriginalTitle": "boolean"},
    arrays={"types": ARRAY_CTRL_B, "attributes": ARRAY_CTRL_B},
)

TITLE_BASICS = TableSpec(
    name="title_basics",
    source_file="title.basics.tsv.gz",
    columns=(
        "tconst",
        "titleType",
        "primaryTitle",
        "originalTitle",
        "isAdult",
        "startYear",
        "endYear",
        "runtimeMinutes",
        "genres",
    ),
    primary_key=("tconst",),
    casts={"isAdult": "boolean", "startYear": "int", "endYear": "int", "runtimeMinutes": "int"},
    arrays={"genres": ARRAY_COMMA},
    partition_by=("titleType",),
)

TITLE_CREW = TableSpec(
    name="title_crew",
    source_file="title.crew.tsv.gz",
    columns=("tconst", "directors", "writers"),
    primary_key=("tconst",),
    arrays={"directors": ARRAY_COMMA, "writers": ARRAY_COMMA},
)

TITLE_EPISODE = TableSpec(
    name="title_episode",
    source_file="title.episode.tsv.gz",
    columns=("tconst", "parentTconst", "seasonNumber", "episodeNumber"),
    primary_key=("tconst",),
    casts={"seasonNumber": "int", "episodeNumber": "int"},
)

TITLE_PRINCIPALS = TableSpec(
    name="title_principals",
    source_file="title.principals.tsv.gz",
    columns=("tconst", "ordering", "nconst", "category", "job", "characters"),
    primary_key=("tconst", "ordering"),
    casts={"ordering": "int"},
    arrays={"characters": ARRAY_JSON},
)

TITLE_RATINGS = TableSpec(
    name="title_ratings",
    source_file="title.ratings.tsv.gz",
    columns=("tconst", "averageRating", "numVotes"),
    primary_key=("tconst",),
    casts={"averageRating": "double", "numVotes": "int"},
)

#: Every table of the dataset, keyed by table name.
TABLES: Mapping[str, TableSpec] = MappingProxyType(
    {
        spec.name: spec
        for spec in (
            NAME_BASICS,
            TITLE_AKAS,
            TITLE_BASICS,
            TITLE_CREW,
            TITLE_EPISODE,
            TITLE_PRINCIPALS,
            TITLE_RATINGS,
        )
    }
)
