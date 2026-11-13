#!/usr/bin/env bash
# Section 1 - Data preparation.
#
# Usage (inside the spark container): bash scripts/run_preparation.sh
#
# Steps:
#   1. ingest: raw TSV files -> bronze Parquet (data/bronze/<table>/)

source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"

submit preparation/ingest.py "$@"

log "preparation finished, reports are in outputs/preparation/"
