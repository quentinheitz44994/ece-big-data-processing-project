"""Wikipedia collection (outside Spark): article text of films and people.

Source: the MediaWiki Action API of the configured Wikipedia (English by
default). Only human-written article text is collected, as plain text produced by
the TextExtracts extension:

* films: the whole article (``prop=extracts&explaintext``), one request per film.
  The plot section is cut out later with Spark;
* people: the lead section (``exintro``), up to ``person_batch_size`` pages per
  request.

Each request also returns the revision id of the page (``prop=revisions``) and
its canonical URL (``prop=info``), used for the lineage of every record. Raw
responses are cached under ``data/enrichment/raw/<source>/``; nothing is parsed
or cleaned here.
"""

from __future__ import annotations

import argparse
import time
from collections.abc import Sequence
from typing import Any

from imdb_project.common import io
from imdb_project.common.config import Config, add_config_argument, load_config
from imdb_project.common.logging import get_logger
from imdb_project.enrichment import fetch_wikidata
from imdb_project.enrichment.http_client import (
    RawCache,
    WikimediaClient,
    batch_key,
    fetch_cached,
)
from imdb_project.enrichment.select_scope import SCOPE_FILMS, SCOPE_PEOPLE

LOGGER = get_logger(__name__)

SOURCE_FILM_PAGES = "wikipedia_film_pages"
SOURCE_PERSON_INTROS = "wikipedia_person_intros"

#: MediaWiki accepts U+001F as multi-value separator, so titles may contain "|".
_MULTI_VALUE_SEPARATOR = "\u001f"
_MAX_CONTINUATIONS = 50

Item = tuple[str, str]  # (IMDb identifier, Wikipedia page title)


def api_url(cfg: Config, language: str) -> str:
    """Return the Action API endpoint of a Wikipedia language edition."""
    return str(cfg.wikimedia.wikipedia_api).format(language=language)


def _base_params() -> dict[str, str]:
    return {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "extracts|revisions|info",
        "explaintext": "1",
        "exsectionformat": "wiki",
        "rvprop": "ids|timestamp",
        "inprop": "url",
        "redirects": "1",
    }


def film_page_params(title: str) -> dict[str, str]:
    """Parameters returning the full plain-text article of one page."""
    return {**_base_params(), "titles": title}


def person_intro_params(titles: Sequence[str]) -> dict[str, str]:
    """Parameters returning the plain-text lead section of several pages."""
    joined = _MULTI_VALUE_SEPARATOR + _MULTI_VALUE_SEPARATOR.join(titles)
    return {**_base_params(), "exintro": "1", "exlimit": "max", "titles": joined}


def query_all(client: WikimediaClient, url: str, params: dict[str, str]) -> list[dict[str, Any]]:
    """Run an Action API query and follow its ``continue`` tokens.

    Args:
        client: Rate-limited HTTP client.
        url: Action API endpoint.
        params: Query parameters.

    Returns:
        The raw responses, in order (one, plus one per continuation).
    """
    responses = []
    current = dict(params)
    for _ in range(_MAX_CONTINUATIONS):
        response = client.request_json(url, current, use_maxlag=True)
        responses.append(response)
        token = response.get("continue")
        if not token:
            break
        current = {**params, **{key: str(value) for key, value in token.items()}}
    return responses


def collect_films(
    cfg: Config,
    items: Sequence[Item],
    client: WikimediaClient,
    cache: RawCache,
    refresh: bool = False,
) -> int:
    """Fetch the article of each film (one cached request per film).

    Args:
        cfg: Project configuration.
        items: ``(tconst, page title)`` pairs.
        client: Rate-limited HTTP client.
        cache: Raw response cache.
        refresh: Ignore cached responses.

    Returns:
        The number of films processed.
    """
    language = str(cfg.enrichment.wikipedia_language)
    url = api_url(cfg, language)
    for index, (imdb_id, title) in enumerate(items, start=1):
        params = film_page_params(title)
        key = f"{language}_{imdb_id}"
        request = {"language": language, "items": [{"imdb_id": imdb_id, "title": title}]}
        # Reuse matching legacy entries without sharing responses across languages.
        if not refresh and not cache.has(SOURCE_FILM_PAGES, key):
            legacy = cache.load(SOURCE_FILM_PAGES, imdb_id)
            if legacy is not None and legacy.get("request") == request:
                cache.store(SOURCE_FILM_PAGES, key, legacy)
        fetch_cached(
            client,
            cache,
            SOURCE_FILM_PAGES,
            key,
            request,
            lambda params=params: query_all(client, url, params),
            refresh=refresh,
        )
        if index % 200 == 0 or index == len(items):
            LOGGER.info(
                "%s: %d/%d (requests=%d, cache hits=%d, 429=%d)",
                SOURCE_FILM_PAGES,
                index,
                len(items),
                client.stats.requests,
                client.stats.cache_hits,
                client.stats.http_429,
            )
    return len(items)


def collect_people(
    cfg: Config,
    items: Sequence[Item],
    client: WikimediaClient,
    cache: RawCache,
    refresh: bool = False,
) -> int:
    """Fetch the lead section of each person, in batches of pages.

    Args:
        cfg: Project configuration.
        items: ``(nconst, page title)`` pairs.
        client: Rate-limited HTTP client.
        cache: Raw response cache.
        refresh: Ignore cached responses.

    Returns:
        The number of batches processed.
    """
    language = str(cfg.enrichment.wikipedia_language)
    url = api_url(cfg, language)
    batch_size = int(cfg.enrichment.get("person_batch_size", 20))
    ordered = sorted(set(items))
    batches = [ordered[start : start + batch_size] for start in range(0, len(ordered), batch_size)]
    for index, batch in enumerate(batches, start=1):
        params = person_intro_params([title for _, title in batch])
        fetch_cached(
            client,
            cache,
            SOURCE_PERSON_INTROS,
            batch_key(language, [imdb_id for imdb_id, _ in batch]),
            {
                "language": language,
                "items": [{"imdb_id": imdb_id, "title": title} for imdb_id, title in batch],
            },
            lambda params=params: query_all(client, url, params),
            refresh=refresh,
        )
        if index % 25 == 0 or index == len(batches):
            LOGGER.info("%s: %d/%d batches", SOURCE_PERSON_INTROS, index, len(batches))
    return len(batches)


def resolve_titles(records: Sequence[dict[str, Any]], wiki: str) -> dict[str, str]:
    """Map IMDb identifiers to the page title of one wiki from cached sitelinks.

    When an identifier is carried by several Wikidata items, the item with the
    lowest numeric id is used (same rule as the Spark reader).
    """
    site = fetch_wikidata.wiki_site_url(wiki)
    best: dict[str, tuple[int, str]] = {}
    for record in records:
        for row in fetch_wikidata.iter_bindings(record):
            if row.get("wiki") != site or not row.get("title") or not row.get("imdb"):
                continue
            item = row.get("item", "")
            number = int(item.rsplit("Q", 1)[-1]) if item.rsplit("Q", 1)[-1].isdigit() else 0
            current = best.get(row["imdb"])
            if current is None or (number, row["title"]) < current:
                best[row["imdb"]] = (number, row["title"])
    return {imdb_id: title for imdb_id, (_, title) in best.items()}


def run(
    cfg: Config,
    limit: int | None = None,
    refresh: bool = False,
    client: WikimediaClient | None = None,
) -> dict[str, int]:
    """Collect everything the enrichment needs, in order, with one HTTP client.

    Steps: Wikidata sitelinks of the films and people of the scope, Wikidata
    facts of the people, Wikipedia articles of the films, Wikipedia lead sections
    of the people.

    Args:
        cfg: Project configuration.
        limit: Only the first N films and N people (quick tests).
        refresh: Ignore cached responses.
        client: Optional client to reuse (a new one is created otherwise).

    Returns:
        Counters of the run.
    """
    language = str(cfg.enrichment.wikipedia_language)
    wiki = f"{language.replace('-', '_')}wiki"
    film_ids = fetch_wikidata.read_ids(
        io.layer_path(cfg, "enrichment", SCOPE_FILMS), "tconst", limit
    )
    person_ids = fetch_wikidata.read_ids(
        io.layer_path(cfg, "enrichment", SCOPE_PEOPLE), "nconst", limit
    )
    LOGGER.info("collecting %d films and %d people", len(film_ids), len(person_ids))

    client = client or WikimediaClient(cfg.wikimedia)
    cache = RawCache(io.layer_path(cfg, "enrichment", "raw"))
    counters = {"films": len(film_ids), "people": len(person_ids)}
    try:
        film_links = fetch_wikidata.collect(
            cfg, "sitelinks", film_ids, "enrichment:film_sitelinks", client, refresh
        )
        person_links = fetch_wikidata.collect(
            cfg, "sitelinks", person_ids, "enrichment:person_sitelinks", client, refresh
        )
        fetch_wikidata.collect(
            cfg, "person_facts", person_ids, "enrichment:person_facts", client, refresh
        )
        film_titles = resolve_titles(film_links, wiki)
        person_titles = resolve_titles(person_links, wiki)
        counters["films_with_page"] = len(film_titles)
        counters["people_with_page"] = len(person_titles)

        step_started = time.monotonic()
        collect_films(cfg, sorted(film_titles.items()), client, cache, refresh)
        fetch_wikidata.append_run_stats(
            cfg,
            "enrichment:film_pages",
            client,
            {
                "kind": SOURCE_FILM_PAGES,
                "ids_requested": len(film_titles),
                "duration_seconds": round(time.monotonic() - step_started, 1),
            },
        )
        step_started = time.monotonic()
        collect_people(cfg, sorted(person_titles.items()), client, cache, refresh)
        fetch_wikidata.append_run_stats(
            cfg,
            "enrichment:person_intros",
            client,
            {
                "kind": SOURCE_PERSON_INTROS,
                "ids_requested": len(person_titles),
                "duration_seconds": round(time.monotonic() - step_started, 1),
            },
        )
    finally:
        client.close()
    LOGGER.info("collection finished: %s, stats=%s", counters, client.stats.as_dict())
    return counters


def main() -> None:
    """CLI entry point."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    parser.add_argument("--limit", type=int, default=None, help="Only the first N films / people.")
    parser.add_argument("--refresh", action="store_true", help="Ignore cached responses.")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume an interrupted collection (default behaviour: cached responses are reused).",
    )
    args = parser.parse_args()
    run(load_config(args.config), args.limit, args.refresh)


if __name__ == "__main__":
    main()
