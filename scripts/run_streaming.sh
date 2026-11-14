#!/usr/bin/env bash
# Build/reuse the lookup, stream for N minutes, inject late samples, stop and report.
# Usage (inside Spark): bash scripts/run_streaming.sh [minutes]

source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"

if [[ "$#" -gt 1 ]]; then
  echo "Usage: bash scripts/run_streaming.sh [minutes]" >&2
  exit 2
fi
if [[ "$#" -eq 1 ]]; then
  submit streaming/stream_job.py --run-minutes "$1"
else
  submit streaming/stream_job.py
fi
