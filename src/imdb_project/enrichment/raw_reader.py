"""Spark readers of the raw API response cache, with enforced schemas.

The collectors only store raw responses. Everything else (schema enforcement,
parsing, cleaning) happens here and in the jobs built on these readers:

* every cache folder is read with an explicit ``StructType``;
* unparsable files end up in a controlled ``_corrupt_record`` column, are counted
  and make the job fail above ``max_corrupt_records``.
"""

from __future__ import annotations

from pathlib import Path

from pyspark.sql import Column, DataFrame, SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql.types import ArrayType, MapType, StringType, StructField, StructType

from imdb_project.common import io
from imdb_project.common.config import Config
from imdb_project.common.logging import get_logger
from imdb_project.enrichment.fetch_wikidata import SOURCE_SITELINKS

LOGGER = get_logger(__name__)

CORRUPT_COLUMN = "_corrupt_record"

_SPARQL_CELL = StructType(
    [StructField("type", StringType(), True), StructField("value", StringType(), True)]
)
_SPARQL_RESPONSE = StructType(
    [
        StructField(
            "results",
            StructType(
                [StructField("bindings", ArrayType(MapType(StringType(), _SPARQL_CELL)), True)]
            ),
            True,
        )
    ]
)


def envelope_schema(request: StructType, response: StructType) -> StructType:
    """Return the schema of a cache record wrapping a request and its responses.

    Args:
        request: Schema of the ``request`` object stored by the collector.
        response: Schema of one raw API response.

    Returns:
        The explicit schema of the cache files, with the corrupt record column.
    """
    return StructType(
        [
            StructField("source", StringType(), True),
            StructField("key", StringType(), True),
            StructField("request", request, True),
            StructField("retrieved_at", StringType(), True),
            StructField("responses", ArrayType(response), True),
            StructField(CORRUPT_COLUMN, StringType(), True),
        ]
    )


SPARQL_RECORD_SCHEMA = envelope_schema(
    StructType(
        [
            StructField("endpoint", StringType(), True),
            StructField("ids", ArrayType(StringType()), True),
        ]
    ),
    _SPARQL_RESPONSE,
)


def raw_source_path(cfg: Config, source: str) -> str:
    """Return the cache folder of a source."""
    return io.layer_path(cfg, "enrichment", "raw", source)


def read_raw_records(
    spark: SparkSession, cfg: Config, source: str, schema: StructType
) -> DataFrame:
    """Read the cache files of a source with an enforced schema.

    Args:
        spark: Active Spark session.
        cfg: Project configuration.
        source: Cache sub-folder.
        schema: Explicit schema of the files (see :func:`envelope_schema`).

    Returns:
        The valid records, cached, without the corrupt record column.

    Raises:
        FileNotFoundError: If nothing has been collected for this source.
        RuntimeError: If more than ``enrichment.max_corrupt_records`` files are corrupt.
    """
    folder = Path(raw_source_path(cfg, source))
    if not folder.is_dir() or not any(folder.glob("*.json")):
        raise FileNotFoundError(f"No cached response in {folder}: run the collection step first")
    records = (
        spark.read.schema(schema)
        .option("mode", "PERMISSIVE")
        .option("columnNameOfCorruptRecord", CORRUPT_COLUMN)
        .json(str(folder / "*.json"))
        .cache()
    )
    is_corrupt = F.col(CORRUPT_COLUMN).isNotNull() | F.col("responses").isNull()
    n_corrupt = records.where(is_corrupt).count()
    max_corrupt = int(cfg.get("enrichment.max_corrupt_records", 0))
    if n_corrupt:
        LOGGER.warning("%s: %d corrupt cache record(s) ignored", source, n_corrupt)
    if n_corrupt > max_corrupt:
        raise RuntimeError(
            f"{source}: {n_corrupt} corrupt cache record(s) (max_corrupt_records={max_corrupt}). "
            "Delete the corrupt files and run the collection again."
        )
    return records.where(~is_corrupt).drop(CORRUPT_COLUMN)


def read_sparql_bindings(spark: SparkSession, cfg: Config, source: str) -> DataFrame:
    """Return one row per SPARQL result row of a source.

    Returns:
        Columns ``key``, ``retrieved_at`` and ``binding`` (map of variable name to
        ``struct<type, value>``); use :func:`binding_value` to read a variable.
    """
    records = read_raw_records(spark, cfg, source, SPARQL_RECORD_SCHEMA)
    return records.select("key", "retrieved_at", F.explode("responses").alias("response")).select(
        "key", "retrieved_at", F.explode("response.results.bindings").alias("binding")
    )


def binding_value(name: str) -> Column:
    """Return the value of a SPARQL variable (null when unbound)."""
    return F.try_element_at(F.col("binding"), F.lit(name))["value"]


def qid(uri: Column) -> Column:
    """Extract the ``Q...`` identifier from a Wikidata entity URI (null if none)."""
    extracted = F.regexp_extract(uri, r"(Q\d+)$", 1)
    return F.when(extracted != "", extracted)


def wiki_name(site_url: Column) -> Column:
    """Convert a Wikipedia site URL to its database name (``enwiki``)."""
    language = F.regexp_extract(site_url, r"^https://([a-z-]+)\.wikipedia\.org/$", 1)
    return F.when(language != "", F.concat(F.regexp_replace(language, "-", "_"), F.lit("wiki")))


def wikidata_items(spark: SparkSession, cfg: Config) -> DataFrame:
    """Return the Wikidata item of each IMDb identifier found by the mapping.

    When several items carry the same IMDb identifier, the one with the lowest
    numeric id is kept and ``n_items`` records how many there were.

    Returns:
        Columns ``imdb_id``, ``qid``, ``n_items``, ``retrieved_at``.
    """
    rows = read_sparql_bindings(spark, cfg, SOURCE_SITELINKS).select(
        binding_value("imdb").alias("imdb_id"),
        qid(binding_value("item")).alias("qid"),
        "retrieved_at",
    )
    per_item = (
        rows.where(F.col("imdb_id").isNotNull() & F.col("qid").isNotNull())
        .groupBy("imdb_id", "qid")
        .agg(F.max("retrieved_at").alias("retrieved_at"))
    )
    by_id = Window.partitionBy("imdb_id")
    number = F.regexp_extract("qid", r"(\d+)", 1).cast("long")
    return (
        per_item.withColumn("n_items", F.count(F.lit(1)).over(by_id))
        .withColumn("rank", F.row_number().over(by_id.orderBy(number)))
        .where(F.col("rank") == 1)
        .drop("rank")
    )


def sitelinks(spark: SparkSession, cfg: Config) -> DataFrame:
    """Return the Wikipedia page titles linked to IMDb identifiers.

    Returns:
        One row per (``imdb_id``, ``wiki``): ``qid``, ``page_title``,
        ``retrieved_at``, for the item selected by :func:`wikidata_items`.
    """
    rows = read_sparql_bindings(spark, cfg, SOURCE_SITELINKS).select(
        binding_value("imdb").alias("imdb_id"),
        qid(binding_value("item")).alias("qid"),
        wiki_name(binding_value("wiki")).alias("wiki"),
        F.trim(binding_value("title")).alias("page_title"),
        "retrieved_at",
    )
    links = (
        rows.where(F.col("wiki").isNotNull() & (F.length("page_title") > 0))
        .groupBy("imdb_id", "qid", "wiki")
        .agg(F.min("page_title").alias("page_title"), F.max("retrieved_at").alias("retrieved_at"))
    )
    kept = wikidata_items(spark, cfg).select("imdb_id", "qid")
    return links.join(kept, ["imdb_id", "qid"], "left_semi")
