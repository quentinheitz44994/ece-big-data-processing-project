"""Enriched tables (Spark): synopsis of films and biography of their principals.

Reads the raw API responses cached by the collectors with enforced schemas,
then does all the processing in Spark:

* films: the plot section of the Wikipedia article is cut out of the plain-text
  article (first heading of ``plot_section_titles`` found), cleaned, and joined
  to the scope. Without a plot section the lead section is used and the record
  is marked ``no_plot_section``;
* people: lead section of the Wikipedia article plus raw Wikidata statements
  (dates of birth and death, place of birth, citizenship).

Every record carries its lineage: ``source_name``, ``source_url``,
``source_revision_id``, ``source_permalink``, ``retrieved_at``, ``license``,
``enrichment_status`` (``ok``, ``partial``, ``no_plot_section``, ``not_found``)
and ``enrichment_note``, a programmatic explanation when information is missing.
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Sequence
from pathlib import Path

from pyspark.sql import Column, DataFrame, SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql.types import (
    ArrayType,
    BooleanType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
)

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.logging import get_logger
from imdb_project.common.spark_session import build_spark
from imdb_project.enrichment import raw_reader
from imdb_project.enrichment.fetch_wikidata import SOURCE_PERSON_FACTS, SOURCE_SITELINKS
from imdb_project.enrichment.fetch_wikipedia import SOURCE_FILM_PAGES, SOURCE_PERSON_INTROS
from imdb_project.enrichment.select_scope import SCOPE_FILMS, SCOPE_PEOPLE
from imdb_project.exploration import base

LOGGER = get_logger(__name__)

STATUS_OK = "ok"
STATUS_PARTIAL = "partial"
STATUS_NO_PLOT = "no_plot_section"
STATUS_NOT_FOUND = "not_found"
TYPE_PLOT = "plot_section"
TYPE_LEAD = "lead_section"

LINEAGE_COLUMNS = (
    "source_name",
    "source_url",
    "source_revision_id",
    "source_permalink",
    "retrieved_at",
    "license",
    "enrichment_status",
    "enrichment_note",
)

_TITLE_MAP = ArrayType(
    StructType([StructField("from", StringType(), True), StructField("to", StringType(), True)])
)
_REVISION = StructType(
    [
        StructField("revid", LongType(), True),
        StructField("parentid", LongType(), True),
        StructField("timestamp", StringType(), True),
    ]
)
_PAGE = StructType(
    [
        StructField("pageid", LongType(), True),
        StructField("ns", IntegerType(), True),
        StructField("title", StringType(), True),
        StructField("missing", BooleanType(), True),
        StructField("invalid", BooleanType(), True),
        StructField("extract", StringType(), True),
        StructField("canonicalurl", StringType(), True),
        StructField("fullurl", StringType(), True),
        StructField("lastrevid", LongType(), True),
        StructField("revisions", ArrayType(_REVISION), True),
    ]
)
#: Enforced schema of the cached MediaWiki Action API responses.
WIKIPEDIA_RECORD_SCHEMA = raw_reader.envelope_schema(
    StructType(
        [
            StructField("language", StringType(), True),
            StructField(
                "items",
                ArrayType(
                    StructType(
                        [
                            StructField("imdb_id", StringType(), True),
                            StructField("title", StringType(), True),
                        ]
                    )
                ),
                True,
            ),
        ]
    ),
    StructType(
        [
            StructField(
                "query",
                StructType(
                    [
                        StructField("normalized", _TITLE_MAP, True),
                        StructField("redirects", _TITLE_MAP, True),
                        StructField("pages", ArrayType(_PAGE), True),
                    ]
                ),
                True,
            )
        ]
    ),
)


# ----------------------------------------------------------------- raw parsing


def wikipedia_items(records: DataFrame) -> DataFrame:
    """Return one row per requested page with the content returned by the API.

    Requested titles are followed through the ``normalized`` and ``redirects``
    maps of the response; a page split over several continuation responses is
    merged (first non-null value of each field).

    Args:
        records: Cache records read with :data:`WIKIPEDIA_RECORD_SCHEMA`.

    Returns:
        ``imdb_id``, ``language``, ``requested_title``, ``page_title``,
        ``page_id``, ``page_missing``, ``extract``, ``canonical_url``,
        ``revision_id``, ``revision_timestamp``, ``retrieved_at``; the most recent
        record is kept when an identifier was collected several times.
    """

    def present(value: Column) -> Column:
        return value.isNotNull()

    def gather(field: str) -> Column:
        parts = F.transform("responses", lambda response: response["query"][field])
        return F.flatten(F.filter(parts, present))

    def follow(mapping: Column, title: Column) -> Column:
        target = F.get(F.filter(mapping, lambda entry: entry["from"] == title), 0)["to"]
        return F.coalesce(target, title)

    prepared = records.select(
        "retrieved_at",
        F.col("request.language").alias("language"),
        F.explode("request.items").alias("item"),
        gather("normalized").alias("normalized"),
        gather("redirects").alias("redirects"),
        gather("pages").alias("pages"),
    )
    requested = F.col("item.title")
    final_title = follow(F.col("redirects"), follow(F.col("normalized"), requested))
    matched = F.filter(F.col("pages"), lambda page: page["title"] == final_title)

    def first(field: str) -> Column:
        return F.get(F.filter(F.transform(matched, lambda page: page[field]), present), 0)

    revision = F.get(
        F.flatten(F.filter(F.transform(matched, lambda page: page["revisions"]), present)), 0
    )
    items = prepared.select(
        F.col("item.imdb_id").alias("imdb_id"),
        "language",
        requested.alias("requested_title"),
        F.when(F.size(matched) > 0, final_title).alias("page_title"),
        first("pageid").alias("page_id"),
        (
            F.coalesce(first("missing"), F.lit(False)) | F.coalesce(first("invalid"), F.lit(False))
        ).alias("page_missing"),
        first("extract").alias("extract"),
        F.coalesce(first("canonicalurl"), first("fullurl")).alias("canonical_url"),
        F.coalesce(revision["revid"], first("lastrevid")).alias("revision_id"),
        revision["timestamp"].alias("revision_timestamp"),
        "retrieved_at",
    )
    latest = Window.partitionBy("imdb_id").orderBy(F.col("retrieved_at").desc())
    return items.withColumn("rank", F.row_number().over(latest)).where("rank = 1").drop("rank")


def lookup_attempts(spark: SparkSession, cfg: Config) -> DataFrame:
    """Return, per IMDb identifier, when its Wikidata mapping was last queried."""
    records = raw_reader.read_raw_records(
        spark, cfg, SOURCE_SITELINKS, raw_reader.SPARQL_RECORD_SCHEMA
    )
    return (
        records.select(F.explode("request.ids").alias("imdb_id"), "retrieved_at")
        .groupBy("imdb_id")
        .agg(F.max("retrieved_at").alias("mapping_retrieved_at"))
    )


def person_facts(spark: SparkSession, cfg: Config) -> DataFrame:
    """Parse the raw Wikidata statements of people.

    Returns:
        One row per (``imdb_id``, ``qid``): ``birth_date`` and ``death_date``
        (``YYYY-MM-DD`` strings, earliest value when several), ``birth_place``
        and ``citizenships`` (sorted labels).
    """
    value = raw_reader.binding_value

    def day(name: str) -> Column:
        extracted = F.regexp_extract(value(name), r"^(\d{4}-\d{2}-\d{2})", 1)
        return F.when(extracted != "", extracted)

    rows = raw_reader.read_sparql_bindings(spark, cfg, SOURCE_PERSON_FACTS).select(
        value("imdb").alias("imdb_id"),
        raw_reader.qid(value("item")).alias("qid"),
        day("birthDate").alias("birth_date"),
        day("deathDate").alias("death_date"),
        F.trim(value("birthPlaceLabel")).alias("birth_place"),
        F.trim(value("citizenshipLabel")).alias("citizenship"),
    )
    return (
        rows.where(F.col("imdb_id").isNotNull() & F.col("qid").isNotNull())
        .groupBy("imdb_id", "qid")
        .agg(
            F.min("birth_date").alias("birth_date"),
            F.min("death_date").alias("death_date"),
            F.min("birth_place").alias("birth_place"),
            F.sort_array(F.collect_set("citizenship")).alias("citizenships"),
        )
        .withColumn("citizenships", F.when(F.size("citizenships") > 0, F.col("citizenships")))
    )


# ------------------------------------------------------------------- cleaning


def clean_text(text: Column) -> Column:
    """Clean a plain-text extract.

    Removes sub-section heading lines and reference markers such as ``[1]`` or
    ``[citation needed]``, collapses whitespace and trims. Empty results become
    null.
    """
    without_headings = F.regexp_replace(text, r"(?m)^=+[^=\n]+=+[ \t]*$", " ")
    without_markers = F.regexp_replace(
        without_headings, r"\[(?:\d+|[a-z]|note \d+|citation needed)\]", ""
    )
    collapsed = F.trim(F.regexp_replace(without_markers, r"[\s\u00a0]+", " "))
    return F.when(F.length(collapsed) > 0, collapsed)


def section_text(extract: Column, heading: str) -> Column:
    """Return the body of a level-2 section of a plain-text article (null if absent)."""
    pattern = rf"(?is)(?:^|\n)==[ \t]*{re.escape(heading)}[ \t]*==[ \t]*\n(.*?)(?=\n==[^=]|\z)"
    body = F.regexp_extract(extract, pattern, 1)
    return F.when(F.length(F.trim(body)) > 0, body)


def lead_text(extract: Column) -> Column:
    """Return the lead section (text before the first level-2 heading)."""
    body = F.regexp_extract(extract, r"(?s)^(.*?)(?=\n==[^=]|\z)", 1)
    return F.when(F.length(F.trim(body)) > 0, body)


def with_synopsis(pages: DataFrame, headings: Sequence[str]) -> DataFrame:
    """Add ``synopsis``, ``synopsis_type`` and ``synopsis_section`` to film pages.

    Args:
        pages: Output of :func:`wikipedia_items` for the films.
        headings: Accepted plot section headings, in order of preference.

    Returns:
        ``pages`` with the cleaned synopsis: the first plot section found, else
        the lead section.
    """
    extract = F.col("extract")
    sections = [(heading, clean_text(section_text(extract, heading))) for heading in headings]
    plot = F.coalesce(*[text for _, text in sections])
    heading_found = F.coalesce(
        *[F.when(text.isNotNull(), F.lit(heading)) for heading, text in sections]
    )
    lead = clean_text(lead_text(extract))
    return (
        pages.withColumn("synopsis_section", heading_found)
        .withColumn("synopsis", F.coalesce(plot, lead))
        .withColumn(
            "synopsis_type",
            F.when(plot.isNotNull(), F.lit(TYPE_PLOT)).when(lead.isNotNull(), F.lit(TYPE_LEAD)),
        )
    )


# -------------------------------------------------------------------- lineage


def _quoted(column: str) -> Column:
    return F.concat(F.lit("'"), F.coalesce(F.col(column), F.lit("?")), F.lit("'"))


def with_lineage(df: DataFrame, cfg: Config, text_column: str, id_column: str) -> DataFrame:
    """Add the lineage columns shared by films and people.

    Expects the columns ``wikidata_qid``, ``wikipedia_title``, ``page_missing``,
    ``page_collected``, ``canonical_url``, ``revision_id``, ``page_retrieved_at``,
    ``mapping_retrieved_at``, ``language``, ``enrichment_status`` and
    ``enrichment_note`` (status and note of the text itself, or null).

    Args:
        df: Joined scope, mapping and page data.
        cfg: Project configuration.
        text_column: Column holding the collected text.
        id_column: IMDb identifier column, quoted in the notes.

    Returns:
        ``df`` with the columns of :data:`LINEAGE_COLUMNS` filled for every row.
    """
    enrichment = cfg.enrichment
    language = str(enrichment.wikipedia_language)
    wiki = f"{language.replace('-', '_')}wiki"
    site = f"https://{language}.wikipedia.org"
    endpoint = str(cfg.wikimedia.sparql_endpoint)
    has_item = F.col("wikidata_qid").isNotNull()
    has_link = F.col("wikipedia_title").isNotNull()
    has_page = F.col("page_collected") & ~F.col("page_missing")
    has_text = F.col(text_column).isNotNull()
    item_url = F.concat(F.lit("https://www.wikidata.org/wiki/"), F.col("wikidata_qid"))
    identifier = F.concat(F.lit("P345="), F.col(id_column))

    missing_note = (
        F.when(~has_item, F.concat(F.lit("No Wikidata item with "), identifier))
        .when(
            ~has_link,
            F.concat(
                F.lit(f"No {wiki} sitelink for "),
                F.col("wikidata_qid"),
                F.lit(" ("),
                identifier,
                F.lit(")"),
            ),
        )
        .when(
            ~F.col("page_collected"),
            F.concat(F.lit("Wikipedia page "), _quoted("wikipedia_title"), F.lit(" not collected")),
        )
        .when(
            F.col("page_missing"),
            F.concat(
                F.lit("Wikipedia page "), _quoted("wikipedia_title"), F.lit(" does not exist")
            ),
        )
        .when(
            ~has_text,
            F.concat(F.lit("Empty text extract for Wikipedia page "), _quoted("wikipedia_title")),
        )
    )
    status = F.when(has_page & has_text, F.col("enrichment_status")).otherwise(
        F.lit(STATUS_NOT_FOUND)
    )
    return (
        df.withColumn(
            "source_name",
            F.when(has_page, F.lit(f"Wikipedia ({language})"))
            .when(has_item, F.lit("Wikidata"))
            .otherwise(F.lit("Wikidata Query Service")),
        )
        .withColumn(
            "source_url",
            F.when(has_page, F.col("canonical_url"))
            .when(has_item, item_url)
            .otherwise(F.lit(endpoint)),
        )
        .withColumn("source_revision_id", F.when(has_page, F.col("revision_id")))
        .withColumn(
            "source_permalink",
            F.when(
                has_page & F.col("revision_id").isNotNull(),
                F.concat(F.lit(f"{site}/w/index.php?oldid="), F.col("revision_id").cast("string")),
            ),
        )
        .withColumn(
            "retrieved_at",
            F.when(has_page, F.col("page_retrieved_at")).otherwise(F.col("mapping_retrieved_at")),
        )
        .withColumn(
            "license",
            F.when(has_page, F.lit(str(enrichment.text_license))).otherwise(
                F.lit(str(enrichment.facts_license))
            ),
        )
        .withColumn("enrichment_note", F.coalesce(missing_note, F.col("enrichment_note")))
        .withColumn("enrichment_status", status)
    )


def _page_columns(pages: DataFrame, id_column: str) -> DataFrame:
    return pages.select(
        F.col("imdb_id").alias(id_column),
        F.lit(True).alias("page_collected_flag"),
        "page_missing",
        "extract",
        "canonical_url",
        "revision_id",
        "revision_timestamp",
        F.col("retrieved_at").alias("page_retrieved_at"),
    )


def _with_mapping(
    scope: DataFrame,
    id_column: str,
    items: DataFrame,
    links: DataFrame,
    attempts: DataFrame,
    pages: DataFrame,
    wiki: str,
) -> DataFrame:
    mapped_items = items.select(
        F.col("imdb_id").alias(id_column), F.col("qid").alias("wikidata_qid")
    )
    mapped_links = links.where(F.col("wiki") == wiki).select(
        F.col("imdb_id").alias(id_column), F.col("page_title").alias("wikipedia_title")
    )
    mapped_attempts = attempts.select(F.col("imdb_id").alias(id_column), "mapping_retrieved_at")
    joined = (
        scope.join(mapped_items, id_column, "left")
        .join(mapped_links, id_column, "left")
        .join(mapped_attempts, id_column, "left")
        .join(_page_columns(pages, id_column), id_column, "left")
    )
    return (
        joined.withColumn("page_collected", F.coalesce("page_collected_flag", F.lit(False)))
        .withColumn("page_missing", F.coalesce("page_missing", F.lit(False)))
        .drop("page_collected_flag")
    )


# --------------------------------------------------------------- final tables


def build_films(
    scope: DataFrame,
    items: DataFrame,
    links: DataFrame,
    attempts: DataFrame,
    pages: DataFrame,
    cfg: Config,
) -> DataFrame:
    """Build the enriched films table (one row per film of the scope)."""
    enrichment = cfg.enrichment
    language = str(enrichment.wikipedia_language)
    headings = list(enrichment.plot_section_titles)
    minimum = int(enrichment.get("min_synopsis_chars", 200))
    joined = _with_mapping(
        scope, "tconst", items, links, attempts, pages, f"{language.replace('-', '_')}wiki"
    )
    parsed = with_synopsis(joined, headings).withColumn("synopsis_chars", F.length("synopsis"))

    is_plot = F.col("synopsis_type") == TYPE_PLOT
    short = F.col("synopsis_chars") < minimum
    status = (
        F.when(is_plot & ~short, F.lit(STATUS_OK))
        .when(is_plot, F.lit(STATUS_PARTIAL))
        .otherwise(F.lit(STATUS_NO_PLOT))
    )
    note = F.when(
        is_plot & short,
        F.concat(
            F.lit("Section "),
            _quoted("synopsis_section"),
            F.lit(f" shorter than {minimum} characters ("),
            F.col("synopsis_chars").cast("string"),
            F.lit(")"),
        ),
    ).when(
        ~is_plot,
        F.concat(
            F.lit(f"No section among ({', '.join(headings)}) in Wikipedia page "),
            _quoted("wikipedia_title"),
            F.lit("; lead section used instead"),
        ),
    )
    described = parsed.withColumn("enrichment_status", status).withColumn("enrichment_note", note)
    return with_lineage(described, cfg, "synopsis", "tconst").select(
        "tconst",
        "primaryTitle",
        "originalTitle",
        "startYear",
        "averageRating",
        "numVotes",
        "selections",
        "wikidata_qid",
        "wikipedia_title",
        "synopsis",
        "synopsis_type",
        "synopsis_section",
        "synopsis_chars",
        *LINEAGE_COLUMNS,
    )


def build_people(
    scope: DataFrame,
    names: DataFrame,
    items: DataFrame,
    links: DataFrame,
    attempts: DataFrame,
    pages: DataFrame,
    facts: DataFrame,
    cfg: Config,
) -> DataFrame:
    """Build the enriched people table (one row per person of the scope)."""
    enrichment = cfg.enrichment
    language = str(enrichment.wikipedia_language)
    minimum = int(enrichment.get("min_biography_chars", 100))
    people = (
        scope.groupBy("nconst")
        .agg(F.count(F.lit(1)).alias("n_scope_films"))
        .join(names.select("nconst", "primaryName", "birthYear", "deathYear"), "nconst", "left")
    )
    joined = _with_mapping(
        people, "nconst", items, links, attempts, pages, f"{language.replace('-', '_')}wiki"
    )
    with_facts = joined.join(
        facts.select(
            F.col("imdb_id").alias("nconst"),
            F.col("qid").alias("wikidata_qid"),
            "birth_date",
            "death_date",
            "birth_place",
            "citizenships",
        ),
        ["nconst", "wikidata_qid"],
        "left",
    )
    parsed = with_facts.withColumn("biography", clean_text(F.col("extract"))).withColumn(
        "biography_chars", F.length("biography")
    )
    short = F.col("biography_chars") < minimum
    described = parsed.withColumn(
        "enrichment_status", F.when(short, F.lit(STATUS_PARTIAL)).otherwise(F.lit(STATUS_OK))
    ).withColumn(
        "enrichment_note",
        F.when(
            short,
            F.concat(
                F.lit(f"Lead section shorter than {minimum} characters ("),
                F.col("biography_chars").cast("string"),
                F.lit(")"),
            ),
        ),
    )
    has_facts = (
        F.col("birth_date").isNotNull()
        | F.col("death_date").isNotNull()
        | F.col("birth_place").isNotNull()
        | F.col("citizenships").isNotNull()
    )
    lineage = with_lineage(described, cfg, "biography", "nconst")
    # A person without Wikipedia text but with Wikidata statements is "partial".
    status = F.when(
        (F.col("enrichment_status") == STATUS_NOT_FOUND) & has_facts, F.lit(STATUS_PARTIAL)
    ).otherwise(F.col("enrichment_status"))
    note = F.when(
        (F.col("enrichment_status") == STATUS_NOT_FOUND) & has_facts,
        F.concat(F.col("enrichment_note"), F.lit("; Wikidata statements only")),
    ).otherwise(F.col("enrichment_note"))
    item_url = F.concat(F.lit("https://www.wikidata.org/wiki/"), F.col("wikidata_qid"))
    return (
        lineage.withColumn("enrichment_note", note)
        .withColumn("enrichment_status", status)
        .withColumn("facts_source_url", F.when(has_facts, item_url))
        .withColumn("facts_license", F.when(has_facts, F.lit(str(enrichment.facts_license))))
        .select(
            "nconst",
            "primaryName",
            "birthYear",
            "deathYear",
            "n_scope_films",
            "wikidata_qid",
            "wikipedia_title",
            "biography",
            "biography_chars",
            "birth_date",
            "death_date",
            "birth_place",
            "citizenships",
            "facts_source_url",
            "facts_license",
            *LINEAGE_COLUMNS,
        )
    )


# -------------------------------------------------------------------- reports


def _status_table(df: DataFrame, title: str) -> io.ReportTable:
    total = df.count()
    counts = (
        df.groupBy("enrichment_status")
        .agg(F.count(F.lit(1)).alias("records"))
        .withColumn("pct", 100.0 * F.col("records") / F.lit(total))
        .orderBy(F.col("records").desc())
    )
    return base.table_from(counts, title)


def _truncate(column: str, width: int) -> Column:
    text = F.col(column)
    return F.when(
        F.length(text) > width, F.concat(F.substring(text, 1, width), F.lit("…"))
    ).otherwise(text)


def collection_stats(spark: SparkSession, cfg: Config) -> list[io.ReportTable]:
    """Summarise ``collection_runs.jsonl`` (requests, retries, waits, robots.txt)."""
    path = Path(io.layer_path(cfg, "enrichment", "stats", "collection_runs.jsonl"))
    if not path.is_file():
        return []
    runs = spark.read.json(str(path))
    counters = [
        name
        for name in (
            "requests",
            "retries",
            "http_429",
            "http_5xx",
            "maxlag_waits",
            "network_errors",
            "failed",
            "cache_hits",
            "cache_misses",
            "seconds_waited",
            "duration_seconds",
        )
        if name in runs.columns
    ]
    per_step = (
        runs.groupBy("step")
        .agg(
            F.count(F.lit(1)).alias("runs"),
            *[F.sum(name).alias(name) for name in counters],
            F.max("ids_requested").alias("ids_requested"),
        )
        .orderBy("step")
    )
    tables = [base.table_from(per_step, "Collection statistics per step (all runs)")]
    if "robots" in runs.columns:
        robots_fields = runs.schema["robots"].dataType.fieldNames()
        verdicts = sorted(
            {
                (field, row[field])
                for row in runs.select("robots.*").distinct().collect()
                for field in robots_fields
                if row[field]
            }
        )
        tables.append(
            io.ReportTable(
                ["endpoint", "robots_txt_verdict", "robots_policy"],
                [
                    [endpoint, verdict, cfg.wikimedia.get("robots.policy")]
                    for endpoint, verdict in verdicts
                ],
                title="robots.txt verdict per endpoint",
            )
        )
    return tables


def write_reports(
    spark: SparkSession, cfg: Config, films: DataFrame, people: DataFrame, links: DataFrame
) -> None:
    """Write the coverage, sample and collection reports of the enrichment."""
    enrichment = cfg.enrichment
    sample_rows = int(enrichment.get("sample_rows", 10))
    width = int(enrichment.get("sample_text_chars", 300))
    has_text = F.col("synopsis").isNotNull()

    decade = (F.floor(F.col("startYear") / 10) * 10).cast("int")
    by_decade = (
        films.groupBy(decade.alias("decade"))
        .agg(
            F.count(F.lit(1)).alias("films"),
            *[
                F.sum(F.when(F.col("enrichment_status") == status, 1).otherwise(0)).alias(status)
                for status in (STATUS_OK, STATUS_PARTIAL, STATUS_NO_PLOT, STATUS_NOT_FOUND)
            ],
            (100.0 * F.avg(F.when(has_text, 1.0).otherwise(0.0))).alias("pct_with_synopsis"),
        )
        .orderBy("decade")
    )
    text_stats = (
        films.where(has_text)
        .groupBy("synopsis_type")
        .agg(
            F.count(F.lit(1)).alias("films"),
            F.avg("synopsis_chars").alias("avg_chars"),
            F.percentile("synopsis_chars", 0.5).alias("median_chars"),
            F.min("synopsis_chars").alias("min_chars"),
            F.max("synopsis_chars").alias("max_chars"),
        )
    )
    sections = (
        films.where(F.col("synopsis_section").isNotNull())
        .groupBy("synopsis_section")
        .agg(F.count(F.lit(1)).alias("films"))
        .orderBy(F.col("films").desc())
    )
    with_bio = F.col("biography").isNotNull()
    people_facts = people.agg(
        F.count(F.lit(1)).alias("people"),
        F.sum(F.when(with_bio, 1).otherwise(0)).alias("with_biography"),
        F.sum(F.when(F.col("birth_date").isNotNull(), 1).otherwise(0)).alias("with_birth_date"),
        F.sum(F.when(F.col("death_date").isNotNull(), 1).otherwise(0)).alias("with_death_date"),
        F.sum(F.when(F.col("birth_place").isNotNull(), 1).otherwise(0)).alias("with_birth_place"),
        F.sum(F.when(F.col("citizenships").isNotNull(), 1).otherwise(0)).alias("with_citizenship"),
    )
    per_film = (
        links.groupBy("tconst")
        .agg(
            F.count(F.lit(1)).alias("principals_selected"),
            F.sum(F.when(F.col("has_biography"), 1).otherwise(0)).alias(
                "principals_with_biography"
            ),
        )
        .groupBy("principals_selected", "principals_with_biography")
        .agg(F.count(F.lit(1)).alias("films"))
        .orderBy("principals_selected", "principals_with_biography")
    )
    parameters = {
        "text_source": f"Wikipedia ({enrichment.wikipedia_language})",
        "identifier_and_statement_source": "Wikidata",
        "plot_section_titles": list(enrichment.plot_section_titles),
        "min_synopsis_chars": enrichment.get("min_synopsis_chars"),
        "min_biography_chars": enrichment.get("min_biography_chars"),
        "text_license": enrichment.text_license,
        "facts_license": enrichment.facts_license,
        "films": films.count(),
        "people": people.count(),
    }
    io.write_markdown(
        io.output_path(cfg, "enrichment", "coverage.md"),
        "Enrichment coverage",
        [
            _status_table(films, "Films per enrichment status"),
            base.table_from(by_decade, "Films per decade and status"),
            base.table_from(text_stats, "Synopsis length (characters)"),
            base.table_from(sections, "Section heading used for the synopsis"),
            _status_table(people, "People per enrichment status"),
            base.table_from(people_facts, "People: available information"),
            base.table_from(per_film, "Films per number of principals with a biography"),
        ],
        parameters=parameters,
    )

    film_sample = films.orderBy(F.col("numVotes").desc(), "tconst").select(
        "tconst",
        "primaryTitle",
        "startYear",
        "enrichment_status",
        "synopsis_type",
        _truncate("synopsis", width).alias("synopsis"),
        "source_permalink",
        "retrieved_at",
        "license",
        "enrichment_note",
    )
    missing_sample = (
        films.where(F.col("enrichment_status") != STATUS_OK)
        .orderBy(F.col("numVotes").desc(), "tconst")
        .select(
            "tconst",
            "primaryTitle",
            "startYear",
            "enrichment_status",
            "source_url",
            "enrichment_note",
        )
    )
    people_sample = people.orderBy(F.col("n_scope_films").desc(), "nconst").select(
        "nconst",
        "primaryName",
        "enrichment_status",
        _truncate("biography", width).alias("biography"),
        "birth_date",
        "death_date",
        "birth_place",
        "citizenships",
        "source_permalink",
        "license",
    )
    io.write_markdown(
        io.output_path(cfg, "enrichment", "sample.md"),
        "Enrichment sample",
        [
            base.table_from(film_sample, "Films (most voted first)", limit=sample_rows),
            base.table_from(
                missing_sample, "Films without a plot section (most voted first)", limit=sample_rows
            ),
            base.table_from(people_sample, "People (most scope films first)", limit=sample_rows),
        ],
        parameters={"sample_rows": sample_rows, "text_truncated_at": width},
    )
    stats_tables = collection_stats(spark, cfg)
    if stats_tables:
        wikimedia = cfg.wikimedia
        io.write_markdown(
            io.output_path(cfg, "enrichment", "collection_stats.md"),
            "Collection statistics",
            stats_tables,
            parameters={
                "user_agent_product": wikimedia.user_agent_product,
                "max_requests_per_second": wikimedia.max_requests_per_second,
                "maxlag_seconds": wikimedia.maxlag_seconds,
                "max_retries": wikimedia.max_retries,
                "robots.policy": wikimedia.get("robots.policy"),
                "requests": "sequential, network requests only (cache hits are not requests)",
            },
        )


def run(spark: SparkSession, cfg: Config) -> tuple[DataFrame, DataFrame]:
    """Build the enriched tables, write them to gold and write the reports."""
    scope_f = spark.read.parquet(io.layer_path(cfg, "enrichment", SCOPE_FILMS))
    scope_p = spark.read.parquet(io.layer_path(cfg, "enrichment", SCOPE_PEOPLE))
    items = raw_reader.wikidata_items(spark, cfg).persist()
    links = raw_reader.sitelinks(spark, cfg).persist()
    attempts = lookup_attempts(spark, cfg).persist()

    def pages_of(source: str) -> DataFrame:
        try:
            records = raw_reader.read_raw_records(spark, cfg, source, WIKIPEDIA_RECORD_SCHEMA)
        except FileNotFoundError:
            LOGGER.warning("%s: nothing collected yet", source)
            records = spark.createDataFrame([], WIKIPEDIA_RECORD_SCHEMA)
        return wikipedia_items(records)

    films = build_films(scope_f, items, links, attempts, pages_of(SOURCE_FILM_PAGES), cfg)
    films_path = io.layer_path(cfg, "gold", "enriched_films")
    io.write_parquet(films, films_path)
    films = spark.read.parquet(films_path)

    try:
        facts = person_facts(spark, cfg)
    except FileNotFoundError:
        LOGGER.warning("%s: nothing collected yet", SOURCE_PERSON_FACTS)
        facts = spark.createDataFrame(
            [],
            "imdb_id string, qid string, birth_date string, death_date string, "
            "birth_place string, citizenships array<string>",
        )
    names = base.read_silver(spark, cfg, "name_basics")
    people = build_people(
        scope_p, names, items, links, attempts, pages_of(SOURCE_PERSON_INTROS), facts, cfg
    )
    people_path = io.layer_path(cfg, "gold", "enriched_people")
    io.write_parquet(people, people_path)
    people = spark.read.parquet(people_path)

    film_principals = scope_p.join(
        people.select(
            "nconst",
            F.col("biography").isNotNull().alias("has_biography"),
            F.col("enrichment_status").alias("person_enrichment_status"),
        ),
        "nconst",
        "left",
    )
    links_path = io.layer_path(cfg, "gold", "enriched_film_principals")
    io.write_parquet(film_principals, links_path)

    write_reports(spark, cfg, films, people, spark.read.parquet(links_path))
    LOGGER.info("enrichment built: %d films, %d people", films.count(), people.count())
    return films, people


def main() -> None:
    """CLI entry point."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    args = parser.parse_args()
    cfg = load_config(args.config)
    spark = build_spark(cfg, "build_enrichment")
    try:
        run(spark, cfg)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
