#!/usr/bin/env bash
# Section 1 - Data preparation.
#
# Usage (inside the spark container): bash scripts/run_preparation.sh
#
# Steps:
#   1. ingest:       raw TSV files -> bronze Parquet (data/bronze/<table>/)
#   2. null_profile: missing values per column -> outputs/preparation/null_profile.md
#
# Set SKIP_INGEST=1 to reuse an existing bronze layer.

source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"

if [[ "${SKIP_INGEST:-0}" != "1" ]]; then
  submit preparation/ingest.py
fi
submit preparation/null_profile.py

log "preparation finished, reports are in outputs/preparation/"
