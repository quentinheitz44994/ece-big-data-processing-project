#!/usr/bin/env bash
# Download the seven IMDb non-commercial dataset files into data/raw/.
#
# Usage: bash scripts/download_imdb.sh [--force]
#
# Idempotent: a file already present (and non-empty) is skipped unless --force is
# given. The IMDb files are refreshed daily, so the snapshot actually used is
# recorded in outputs/data_snapshot.md (file sizes and timestamps).
#
# Licence: the files are for personal and non-commercial use only and must not
# be redistributed (https://developer.imdb.com/non-commercial-datasets/).

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${PROJECT_ROOT}"

BASE_URL="${IMDB_BASE_URL:-https://datasets.imdbws.com}"
RAW_DIR="${IMDB_RAW_DIR:-data/raw}"
SNAPSHOT_FILE="${IMDB_SNAPSHOT_FILE:-outputs/data_snapshot.md}"
FILES=(
  name.basics.tsv.gz
  title.akas.tsv.gz
  title.basics.tsv.gz
  title.crew.tsv.gz
  title.episode.tsv.gz
  title.principals.tsv.gz
  title.ratings.tsv.gz
)

FORCE=0
for arg in "$@"; do
  case "${arg}" in
    --force) FORCE=1 ;;
    -h | --help)
      sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown argument: ${arg}" >&2
      exit 2
      ;;
  esac
done

log() {
  printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"
}

mkdir -p "${RAW_DIR}" "$(dirname "${SNAPSHOT_FILE}")"

declare -A STATUS
for file in "${FILES[@]}"; do
  target="${RAW_DIR}/${file}"
  if [[ -s "${target}" && "${FORCE}" -eq 0 ]]; then
    if ! gzip --test "${target}"; then
      echo "Invalid existing archive: ${target}. Run again with --force." >&2
      exit 1
    fi
    log "skip ${file} (already present, use --force to download again)"
    STATUS["${file}"]="already present"
    continue
  fi
  log "download ${BASE_URL}/${file}"
  # --remote-time keeps the server Last-Modified date as the file timestamp;
  # the temporary name guarantees that an interrupted download is never kept.
  curl --fail --location --silent --show-error --retry 3 --retry-delay 5 \
    --remote-time --output "${target}.part" "${BASE_URL}/${file}"
  gzip --test "${target}.part"
  mv -f "${target}.part" "${target}"
  STATUS["${file}"]="downloaded"
done

{
  echo "# IMDb data snapshot"
  echo
  echo "## Parameters"
  echo
  echo "| parameter | value |"
  echo "| --- | --- |"
  echo "| source | ${BASE_URL} |"
  echo "| recorded_at_utc | $(date -u +%Y-%m-%dT%H:%M:%SZ) |"
  echo
  echo "## Files"
  echo
  echo "| file | size_bytes | file_timestamp_utc | status |"
  echo "| --- | --- | --- | --- |"
  for file in "${FILES[@]}"; do
    target="${RAW_DIR}/${file}"
    size="$(stat -c %s "${target}")"
    modified="$(date -u -d "@$(stat -c %Y "${target}")" +%Y-%m-%dT%H:%M:%SZ)"
    echo "| ${file} | ${size} | ${modified} | ${STATUS[${file}]} |"
  done
} > "${SNAPSHOT_FILE}"

log "snapshot written to ${SNAPSHOT_FILE}"
