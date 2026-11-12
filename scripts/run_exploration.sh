#!/usr/bin/env bash
# Section 2 - Data exploration (silver -> gold).
#
# Usage (inside the spark container): bash scripts/run_exploration.sh [q1 q2 ...]
#
# Without argument the eight questions are run in order. Each question writes
# its complete result to data/gold/exploration/ and its tables to
# outputs/exploration/.
#
# Q6 queries Wikidata (original language of the successful films) through the
# rate-limited, cached HTTP client: it needs WIKIMEDIA_CONTACT_EMAIL in .env.

source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"

declare -A MODULES=(
  [q1]=q1_runtime_outliers
  [q2]=q2_top_genres
  [q3]=q3_top_vs_rest
  [q4]=q4_one_hit_directors
  [q5]=q5_series_decline
  [q6]=q6_multilingual_actors
  [q7]=q7_early_peak_actors
  [q8]=q8_multi_talented
)

if [[ $# -gt 0 ]]; then
  QUESTIONS=("$@")
else
  QUESTIONS=(q1 q2 q3 q4 q5 q6 q7 q8)
fi

for question in "${QUESTIONS[@]}"; do
  module="${MODULES[${question}]:-}"
  if [[ -z "${module}" ]]; then
    echo "Unknown question: ${question} (expected q1 ... q8)" >&2
    exit 2
  fi
  submit "exploration/${module}.py"
done

log "exploration finished, reports are in outputs/exploration/"
