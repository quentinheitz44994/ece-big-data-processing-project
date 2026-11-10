#!/usr/bin/env bash
# Shared helpers for the run_*.sh entry points. Sourced, never executed directly.
#
# All scripts are meant to run inside the spark container:
#   docker compose exec spark bash scripts/<script>.sh

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

export PYTHONPATH="${PROJECT_ROOT}/src${PYTHONPATH:+:${PYTHONPATH}}"
CONFIG="${IMDB_PROJECT_CONFIG:-conf/settings.yaml}"

log() {
  printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"
}

# submit <module path under src/imdb_project> [job arguments...]
# Runs a job module with spark-submit (local mode, driver memory from the
# SPARK_DRIVER_MEMORY environment variable).
submit() {
  local module="$1"
  shift
  log "spark-submit ${module} $*"
  spark-submit \
    --driver-memory "${SPARK_DRIVER_MEMORY:-6g}" \
    --conf spark.ui.showConsoleProgress=false \
    "${PROJECT_ROOT}/src/imdb_project/${module}" --config "${CONFIG}" "$@"
}
