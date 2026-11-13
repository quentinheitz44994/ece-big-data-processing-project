#!/usr/bin/env bash
# Section 3 - Data enrichment (Wikipedia / Wikidata).
#
# Usage (inside the spark container): bash scripts/run_enrichment.sh [--limit N] [--refresh]
#
# Steps:
#   1. select_scope (Spark):      films and principals to enrich -> data/enrichment/scope_*.parquet
#   2. fetch_wikipedia (Python):  Wikidata mapping and statements, Wikipedia text.
#                                 Sequential, rate-limited, cached under
#                                 data/enrichment/raw/: an interrupted run resumes
#                                 where it stopped when the script is started again.
#   3. build_enrichment (Spark):  schema enforcement, cleaning, lineage ->
#                                 data/gold/enriched_films/, data/gold/enriched_people/
#
# --limit N   collect only the first N films and N people (quick test)
# --refresh   ignore the cache and query the APIs again
#
# The collection needs WIKIMEDIA_CONTACT_EMAIL in .env (Wikimedia User-Agent policy).

source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"

submit enrichment/select_scope.py

log "collecting from Wikidata and Wikipedia (long step, resumable)"
python -m imdb_project.enrichment.fetch_wikipedia --config "${CONFIG}" "$@"

submit enrichment/build_enrichment.py

log "enrichment finished, reports are in outputs/enrichment/"
