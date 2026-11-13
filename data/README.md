# data/

This folder is **git-ignored** (only this file is versioned). Nothing in it is
ever committed: the IMDb non-commercial datasets may not be redistributed, and
every other layer can be rebuilt from the raw files with the project scripts.

| Folder | Content | Produced by |
| --- | --- | --- |
| `raw/` | The seven IMDb `*.tsv.gz` files | `scripts/download_imdb.sh` |
| `bronze/<table>/` | Raw tables as Parquet, every column kept as string | `scripts/run_preparation.sh` |
| `silver/<table>/` | Typed, standardised tables with a `dq_flags` column | `scripts/run_preparation.sh` |
| `quarantine/<table>/` | Structurally invalid rows excluded from silver, with `dq_reason` | `scripts/run_preparation.sh` |
| `gold/` | Analytical results, enriched tables and the streaming lookup | exploration, enrichment, streaming and open question scripts |
| `enrichment/` | Enrichment scope and raw API response cache (`raw/<source>/`) | `scripts/run_enrichment.sh` |
| `streaming/` | Streaming sinks and checkpoints | `scripts/run_streaming.sh` |

Source of the raw files: <https://datasets.imdbws.com/> (documentation:
<https://developer.imdb.com/non-commercial-datasets/>). The files are refreshed
daily by IMDb; the snapshot date used for the report is recorded in
`outputs/data_snapshot.md`.
