"""Wikidata collection (outside Spark): identifier mapping and structured facts.

Wikidata is only used as a bridge and for raw structured statements, never for
its textual descriptions:

* ``sitelinks``: IMDb identifier (property P345) to Wikidata item and Wikipedia
  page title, for the configured wikis;
* ``person_facts``: date of birth (P569), date of death (P570), place of birth
  (P19) and country of citizenship (P27) of people;
* ``film_languages``: original language of films (P364) with its language codes.

Identifiers are sent in batches (``VALUES``) to the Wikidata Query Service and
every raw response is cached under ``data/enrichment/raw/<source>/``. Cleaning
and schema enforcement of these responses are done later with Spark.
"""

from __future__ import annotations

import argparse
import json
import re
import time
from collections.abc import Callable, Iterable, Iterator, Sequence
from pathlib import Path
from typing import Any

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.logging import get_logger
from imdb_project.enrichment.http_client import (
    RawCache,
    WikimediaClient,
    batch_key,
    fetch_cached,
    utc_now,
)

LOGGER = get_logger(__name__)

SOURCE_SITELINKS = "wikidata_sitelinks"
SOURCE_PERSON_FACTS = "wikidata_person_facts"
SOURCE_FILM_LANGUAGES = "wikidata_film_languages"

IMDB_ID_PATTERN = re.compile(r"^(tt|nm)\d{5,10}$")

_PREFIXES = (
    "PREFIX wdt: <http://www.wikidata.org/prop/direct/>\n"
    "PREFIX schema: <http://schema.org/>\n"
    "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n"
)


def wiki_site_url(wiki: str) -> str:
    """Return the site URL of a Wikipedia database name (``enwiki`` -> ``https://en.wikipedia.org/``)."""
    if not re.fullmatch(r"[a-z_]{2,20}wiki", wiki):
        raise ValueError(f"Unsupported wiki name: {wiki!r}")
    return f"https://{wiki[:-4].replace('_', '-')}.wikipedia.org/"


def _values(ids: Sequence[str]) -> str:
    invalid = [value for value in ids if not IMDB_ID_PATTERN.match(value)]
    if invalid:
        raise ValueError(f"Not IMDb identifiers: {invalid[:5]}")
    return " ".join(f'"{value}"' for value in ids)


def sitelinks_query(ids: Sequence[str], wikis: Sequence[str]) -> str:
    """Build the SPARQL query mapping IMDb ids to items and Wikipedia titles."""
    sites = ", ".join(f"<{wiki_site_url(wiki)}>" for wiki in wikis)
    return (
        f"{_PREFIXES}"
        "SELECT ?imdb ?item ?wiki ?title WHERE {\n"
        f"  VALUES ?imdb {{ {_values(ids)} }}\n"
        "  ?item wdt:P345 ?imdb .\n"
        "  OPTIONAL {\n"
        "    ?article schema:about ?item ; schema:isPartOf ?wiki ; schema:name ?title .\n"
        f"    FILTER(?wiki IN ({sites}))\n"
        "  }\n"
        "}"
    )


def person_facts_query(ids: Sequence[str], label_language: str = "en") -> str:
    """Build the SPARQL query returning raw biographical statements of people."""
    return (
        f"{_PREFIXES}"
        "SELECT ?imdb ?item ?birthDate ?deathDate ?birthPlace ?birthPlaceLabel "
        "?citizenship ?citizenshipLabel WHERE {\n"
        f"  VALUES ?imdb {{ {_values(ids)} }}\n"
        "  ?item wdt:P345 ?imdb .\n"
        "  OPTIONAL { ?item wdt:P569 ?birthDate . }\n"
        "  OPTIONAL { ?item wdt:P570 ?deathDate . }\n"
        "  OPTIONAL {\n"
        "    ?item wdt:P19 ?birthPlace .\n"
        "    OPTIONAL { ?birthPlace rdfs:label ?birthPlaceLabel . "
        f'FILTER(LANG(?birthPlaceLabel) = "{label_language}") }}\n'
        "  }\n"
        "  OPTIONAL {\n"
        "    ?item wdt:P27 ?citizenship .\n"
        "    OPTIONAL { ?citizenship rdfs:label ?citizenshipLabel . "
        f'FILTER(LANG(?citizenshipLabel) = "{label_language}") }}\n'
        "  }\n"
        "}"
    )


def film_languages_query(ids: Sequence[str], label_language: str = "en") -> str:
    """Build the SPARQL query returning the original language(s) of films."""
    return (
        f"{_PREFIXES}"
        "SELECT ?imdb ?item ?language ?languageLabel ?iso1 ?ietf WHERE {\n"
        f"  VALUES ?imdb {{ {_values(ids)} }}\n"
        "  ?item wdt:P345 ?imdb .\n"
        "  OPTIONAL {\n"
        "    ?item wdt:P364 ?language .\n"
        "    OPTIONAL { ?language wdt:P218 ?iso1 . }\n"
        "    OPTIONAL { ?language wdt:P305 ?ietf . }\n"
        "    OPTIONAL { ?language rdfs:label ?languageLabel . "
        f'FILTER(LANG(?languageLabel) = "{label_language}") }}\n'
        "  }\n"
        "}"
    )


def chunked(values: Sequence[str], size: int) -> Iterator[list[str]]:
    """Yield consecutive chunks of ``values`` of at most ``size`` items."""
    for start in range(0, len(values), size):
        yield list(values[start : start + size])


def iter_bindings(record: dict[str, Any]) -> Iterator[dict[str, str]]:
    """Yield the result rows of a cached SPARQL record as ``{variable: value}``."""
    for response in record.get("responses", []):
        for binding in response.get("results", {}).get("bindings", []):
            yield {name: cell.get("value") for name, cell in binding.items()}


def fetch_sparql_batches(
    client: WikimediaClient,
    cache: RawCache,
    source: str,
    ids: Iterable[str],
    build_query: Callable[[Sequence[str]], str],
    endpoint: str,
    batch_size: int,
    key_prefix: str = "batch",
    refresh: bool = False,
) -> list[dict[str, Any]]:
    """Run one SPARQL query per batch of identifiers, through the cache.

    Args:
        client: Rate-limited HTTP client.
        cache: Raw response cache.
        source: Cache sub-folder.
        ids: IMDb identifiers (de-duplicated and sorted for stable batches).
        build_query: Builds the SPARQL query of a batch.
        endpoint: SPARQL endpoint URL.
        batch_size: Number of identifiers per query.
        key_prefix: Prefix of the cache keys (distinguishes query variants).
        refresh: Ignore cached responses.

    Returns:
        The cached records, one per batch.
    """
    unique = sorted(set(ids))
    batches = list(chunked(unique, batch_size))
    records = []
    for index, batch in enumerate(batches, start=1):
        query = build_query(batch)
        record = fetch_cached(
            client,
            cache,
            source,
            batch_key(key_prefix, batch),
            {"endpoint": endpoint, "ids": batch},
            lambda query=query: [
                client.request_json(endpoint, {"query": query, "format": "json"}, method="POST")
            ],
            refresh=refresh,
        )
        records.append(record)
        if index % 25 == 0 or index == len(batches):
            LOGGER.info("%s: %d/%d batches", source, index, len(batches))
    return records


def read_ids(path: str, column: str, limit: int | None = None) -> list[str]:
    """Read a column of identifiers from a Parquet dataset written by Spark.

    Args:
        path: Parquet file or folder.
        column: Column holding the identifiers.
        limit: Optional maximum number of identifiers (quick tests).

    Returns:
        Sorted distinct identifiers.
    """
    import pyarrow.dataset as ds

    table = ds.dataset(path, format="parquet").to_table(columns=[column])
    values = sorted({value for value in table.column(column).to_pylist() if value})
    return values[:limit] if limit else values


def append_run_stats(
    cfg: Config, step: str, client: WikimediaClient, extra: dict[str, Any]
) -> None:
    """Append the statistics of a collection step to ``collection_runs.jsonl``."""
    path = Path(io.layer_path(cfg, "enrichment", "stats", "collection_runs.jsonl"))
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {"step": step, "finished_at": utc_now(), **client.stats_delta(), **extra}
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def collect(
    cfg: Config,
    kind: str,
    ids: Sequence[str],
    step: str,
    client: WikimediaClient | None = None,
    refresh: bool = False,
) -> list[dict[str, Any]]:
    """Collect one kind of Wikidata data for a list of IMDb identifiers.

    Args:
        cfg: Project configuration.
        kind: ``sitelinks``, ``person_facts`` or ``film_languages``.
        ids: IMDb identifiers.
        step: Name of the step in the collection statistics.
        client: Optional client to reuse (a new one is created otherwise).
        refresh: Ignore cached responses.

    Returns:
        The cached records.
    """
    wikimedia = cfg.wikimedia
    wikis = list(wikimedia.get("sitelink_wikis", ["enwiki"]))
    label_language = str(wikimedia.get("label_language", "en"))
    builders: dict[str, tuple[str, str, Callable[[Sequence[str]], str]]] = {
        "sitelinks": (
            SOURCE_SITELINKS,
            "-".join(wikis),
            lambda batch: sitelinks_query(batch, wikis),
        ),
        "person_facts": (
            SOURCE_PERSON_FACTS,
            label_language,
            lambda batch: person_facts_query(batch, label_language),
        ),
        "film_languages": (
            SOURCE_FILM_LANGUAGES,
            label_language,
            lambda batch: film_languages_query(batch, label_language),
        ),
    }
    if kind not in builders:
        raise ValueError(f"Unknown kind {kind!r}, expected one of {sorted(builders)}")
    source, key_prefix, build_query = builders[kind]

    own_client = client is None
    client = client or WikimediaClient(wikimedia)
    cache = RawCache(io.layer_path(cfg, "enrichment", "raw"))
    started = time.monotonic()
    records: list[dict[str, Any]] = []
    try:
        records = fetch_sparql_batches(
            client,
            cache,
            source,
            ids,
            build_query,
            str(wikimedia.sparql_endpoint),
            int(wikimedia.get("sparql_batch_size", 200)),
            key_prefix,
            refresh,
        )
    finally:
        # Statistics are recorded even when the collection is interrupted, so
        # that the requests of every run are accounted for.
        found = {
            row["imdb"] for record in records for row in iter_bindings(record) if "imdb" in row
        }
        append_run_stats(
            cfg,
            step,
            client,
            {
                "kind": kind,
                "ids_requested": len(set(ids)),
                "ids_found_in_wikidata": len(found),
                "duration_seconds": round(time.monotonic() - started, 1),
            },
        )
        if own_client:
            client.close()
    LOGGER.info("%s: %d/%d identifiers found in Wikidata", step, len(found), len(set(ids)))
    return records


def main() -> None:
    """CLI entry point."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    parser.add_argument(
        "--kind", required=True, choices=["sitelinks", "person_facts", "film_languages"]
    )
    parser.add_argument("--ids", required=True, help="Parquet dataset holding the identifiers.")
    parser.add_argument("--column", required=True, help="Identifier column of the dataset.")
    parser.add_argument("--step", default=None, help="Step name in the collection statistics.")
    parser.add_argument("--limit", type=int, default=None, help="Only the first N identifiers.")
    parser.add_argument("--refresh", action="store_true", help="Ignore cached responses.")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume an interrupted collection (default behaviour: cached responses are reused).",
    )
    args = parser.parse_args()
    cfg = load_config(args.config)
    ids = read_ids(args.ids, args.column, args.limit)
    collect(cfg, args.kind, ids, args.step or f"{args.kind}:{args.column}", refresh=args.refresh)


if __name__ == "__main__":
    main()
