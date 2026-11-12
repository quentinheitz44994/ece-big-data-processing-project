#!/usr/bin/env bash
# Section 2 - Data exploration (silver -> gold).
#
# Usage (inside the spark container): bash scripts/run_exploration.sh [q1 q2 ...]
#
# Without argument the available questions are run in order. Each question writes
# its complete result to data/gold/exploration/ and its tables to
# outputs/exploration/.

source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"

declare -A MODULES=(
  [q1]=q1_runtime_outliers
  [q2]=q2_top_genres
  [q3]=q3_top_vs_rest
)

if [[ $# -gt 0 ]]; then
  QUESTIONS=("$@")
else
  QUESTIONS=(q1 q2 q3)
fi

for question in "${QUESTIONS[@]}"; do
  module="${MODULES[${question}]:-}"
  if [[ -z "${module}" ]]; then
    echo "Unknown question: ${question} (expected q1 ... q3)" >&2
    exit 2
  fi
  submit "exploration/${module}.py"
done

log "exploration finished, reports are in outputs/exploration/"
