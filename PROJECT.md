# PROJECT.md - Execution and operations guide

IMDb analytics with Apache Spark (PySpark batch and Structured Streaming) and
Apache Kafka. Course: ECE Paris, Big Data Processing, fall 2026.

- Results and methodology: [REPORT.md](REPORT.md)
- Course instructions: [project_instructions.md](project_instructions.md)

## 1. Contributors

| Name | GitHub username | Email |
| --- | --- | --- |
| Quentin HEITZ | quentinheitz44994 | EMAIL_TO_COMPLETE |
| Maxence SIMONET | maxence808 | maxence.simonet@outlook.com |

Group: gr-XX

## 2. Prerequisites

| Requirement | Detail |
| --- | --- |
| Docker | Docker Desktop, or Docker Engine with the Compose v2 plugin |
| Shell | PowerShell on Windows; bash on Linux, macOS, or WSL2 |
| Memory | 16 GB on the host, about 10 GB available to Docker |
| Disk | about 25 GB free (Spark image 7 GB, data layers about 9 GB, Spark temporary files) |
| Network | `datasets.imdbws.com`, `quay.io`, Docker Hub, Maven Central (image build), Wikimedia APIs |

On Windows, Docker Compose commands can run directly from PowerShell with Docker
Desktop using Linux containers. Bash scripts run **inside** the Spark container
through `docker compose exec spark bash ...`; a separate Ubuntu installation is
not required. A WSL2 terminal is also supported.

When Docker Desktop uses its WSL2 backend, give Docker 10 GB by creating or editing
`C:\Users\<you>\.wslconfig`:

```ini
[wsl2]
memory=10GB
```

then run `wsl --shutdown` and restart Docker Desktop. With less memory, lower
`SPARK_DRIVER_MEMORY` in `.env` (the runs of the report were done with `5g` on an
8 GB Docker VM).

The container user is `jovyan` (uid 1000). On a Linux host whose user has another
uid, make the existing mounted output folders writable first:
`chmod -R a+rwX data outputs`. Apply the same permission adjustment to `REPORT.md`
after that file has been created.

## 3. Run the project from scratch

All commands are run from the repository root. Each `run_*.sh` script is
idempotent: it can be run again and overwrites its own results.

### 3.1 Environment

```bash
cp .env.example .env
# Edit .env: set WIKIMEDIA_CONTACT_EMAIL to a real contact address. It is sent in
# the User-Agent of every Wikipedia / Wikidata request (Wikimedia policy) and the
# collection steps refuse to run without it.
docker compose up -d --build
```

In PowerShell, use `Copy-Item .env.example .env` for the copy step; the Docker
Compose commands are identical. Preserve an existing `.env` when resuming.

Checks:

```bash
docker compose ps -a              # kafka and spark "running", kafka-init "exited (0)"
docker compose logs kafka-init    # "Topic wikistreams created" (or "already exists")
docker compose exec spark pytest  # optional: unit tests on synthetic data
```

Jupyter is available on <http://localhost:8888> (token in `docker compose logs spark`)
and the Spark UI on <http://localhost:4040> while a job runs. Notebooks are optional
and not needed to reproduce the report.

### 3.2 Pipeline

| Step | Command | Duration (*) | Main outputs |
| --- | --- | --- | --- |
| 1. Download IMDb files | `docker compose exec spark bash scripts/download_imdb.sh` | DURATION_DOWNLOAD | `data/raw/*.tsv.gz`, `outputs/data_snapshot.md` |
| 2. Data preparation | `docker compose exec spark bash scripts/run_preparation.sh` | DURATION_PREPARATION | `data/bronze/`, `data/silver/`, `data/quarantine/`, `outputs/preparation/` |
| 3. Data exploration | `docker compose exec spark bash scripts/run_exploration.sh` | DURATION_EXPLORATION | `data/gold/exploration/`, `outputs/exploration/` |
| 4. Data enrichment | `docker compose exec spark bash scripts/run_enrichment.sh` | DURATION_ENRICHMENT | `data/enrichment/`, `data/gold/enriched_*`, `outputs/enrichment/` |
| 5a. Start the producer | `docker compose --profile streaming up -d producer` | a few seconds | events in the Kafka topic `wikistreams` |
| 5b. Streaming job (pending implementation) | `docker compose exec spark bash scripts/run_streaming.sh` | DURATION_STREAMING | planned: `data/gold/wiki_lookup/`, `data/streaming/`, `outputs/streaming/` |
| 6. Open question (pending author choice and implementation) | `docker compose exec spark bash scripts/run_open_question.sh` | DURATION_OPEN_QUESTION | planned: `data/gold/open_question/`, `outputs/open_question/` |
| 7. Render the report (pending implementation) | `docker compose exec spark python scripts/render_report.py` | not measured | planned: generated tables injected in `REPORT.md` |

(*) Measured on a 12-core laptop, Docker VM with 8 GB, `SPARK_DRIVER_MEMORY=5g`,
repository on the Windows drive.

Notes per step:

Steps 5b, 6 and 7 describe the planned interface. Their scripts and `REPORT.md` are
not delivered by PRs #1–#13 or the review-fix branch. Run those steps only after
the corresponding implementations have landed and been tested. `DURATION_*`
fields are placeholders, not measurements from Maxence's installation.

1. **Download.** Existing files are checked with `gzip --test` before being
   skipped (`--force` downloads again). An invalid existing archive fails the step
   with a request to download it again.
   The IMDb files change every day: the snapshot used is recorded in
   `outputs/data_snapshot.md`.
2. **Preparation** chains four jobs: `ingest` (TSV to bronze Parquet),
   `null_profile`, `quality_checks` (rules DQ01 to DQ16) and `cleaning` (silver
   and quarantine). `SKIP_INGEST=1` reuses an existing bronze layer:
   `docker compose exec -e SKIP_INGEST=1 spark bash scripts/run_preparation.sh`.
3. **Exploration** runs the eight questions; one or several can be selected:
   `bash scripts/run_exploration.sh q4 q5`. Q6 queries Wikidata (original language
   of the successful films), through the same client and cache as the enrichment.
   CSV exports are capped by `exploration.max_csv_rows`; each report and its
   `<question>_exports.csv` manifest show total/exported rows, truncation, and the
   gold directory containing the complete results.
4. **Enrichment** has a long collection step (sequential requests, at most one
   per second). Every raw response is cached under `data/enrichment/raw/`: if the
   step is interrupted, run the script again and it resumes where it stopped.
   `bash scripts/run_enrichment.sh --limit 50` is a quick end-to-end test.
5. **Streaming.** The producer container reads Wikimedia EventStreams for
   `streaming.producer.duration_minutes` (30 by default) and then stops; start it
   just before the streaming job. `run_streaming.sh` builds the lookup table of
   Wikipedia pages linked to IMDb identifiers (first run only), runs the three
   streaming queries for `streaming.run_minutes` (20 by default; another duration
   can be given as argument, e.g. `bash scripts/run_streaming.sh 30`), injects the
   late test events and writes the summary. Follow the producer with
   `docker compose logs -f producer`.
7. **Report.** `render_report.py` only replaces the blocks between `AUTO` markers
   of `REPORT.md`; the text written by the authors is never touched.
   `python scripts/render_report.py --check` tells whether the report is up to date.

### 3.3 Stop and clean

```bash
docker compose --profile streaming down      # stop the containers
docker compose --profile streaming down -v   # also remove the anonymous volumes
```

To remove generated data, select the intended `data/` subdirectories in your host
shell or file manager. Keep `data/raw/` to reuse the downloaded IMDb archives.

## 4. Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `port is already allocated` at `docker compose up` | Another service uses 8888, 4040 or 9092: change `JUPYTER_PORT`, `SPARK_UI_PORT` or `KAFKA_EXTERNAL_PORT` in `.env`. |
| `MissingContactError` during a collection step | `WIKIMEDIA_CONTACT_EMAIL` is empty: set it in `.env`, then `docker compose up -d` to recreate the containers. |
| A Spark job is killed or the container exits with code 137 | Out of memory: give Docker more memory (section 2) or lower `SPARK_DRIVER_MEMORY`, then `docker compose up -d`. |
| `No space left on device` | Spark temporary files fill the Docker disk: `docker compose restart spark` clears `/tmp`, and `docker system prune` frees unused images. |
| `bash\r: No such file or directory` | The scripts were checked out with CRLF line endings: clone again (the repository forces LF through `.gitattributes`) or run `git checkout -- scripts`. |
| The streaming job reports no relevant event | The producer is not running or has finished: `docker compose --profile streaming up -d producer`, check `docker compose logs producer`. |
| `UnknownTopicOrPartitionException` | The topic was not created: `docker compose up -d kafka-init`. |
| `RobotsDisallowedError` | `wikimedia.robots.policy` is set to `enforce` in `conf/settings.yaml` (see section 6). |
| A batch job fails after an interrupted run | Run the script again: batch jobs overwrite their outputs and collectors reuse successful cached API responses. The pending streaming job must document its own checkpoint/reset behaviour. |

## 5. Repository structure

```text
.
├── PROJECT.md, REPORT.md, README.md, project_instructions.md
├── CLAUDE.md                     # brief given to the AI coding tool (see section 7)
├── compose.yaml                  # kafka, kafka-init, spark, producer (profile "streaming")
├── docker/spark/Dockerfile       # pinned pyspark-notebook image + Kafka connector
├── docker/producer/Dockerfile    # python:3.12-slim for kafka-init and the producer
├── conf/settings.yaml            # every parameter of the project
├── scripts/                      # download_imdb.sh, run_*.sh, render_report.py
├── src/imdb_project/
│   ├── common/                   # config, Spark session, I/O and report writers, table schemas
│   ├── preparation/              # ingest, null_profile, standardize, rules, quality_checks, cleaning
│   ├── exploration/              # base + one module per question (q1 ... q8)
│   ├── enrichment/               # http_client, fetch_wikidata, fetch_wikipedia, raw_reader,
│   │                             # select_scope, build_enrichment
│   ├── streaming/                # admin, producer, relevance, build_lookup, stream_job,
│   │                             # metrics_listener, late_event_injector, summary
│   └── open_question/            # planned; question and module chosen by the authors
├── tests/                        # pytest, synthetic data only, no network access
├── outputs/                      # generated tables (Markdown, CSV) injected in REPORT.md
├── notebooks/                    # optional interactive exploration
└── data/                         # git-ignored: raw, bronze, silver, quarantine, gold, ...
```

Every job is a Python module with a `run(spark, cfg)` function and a command-line
entry point, launched with `spark-submit` by the `run_*.sh` scripts. No threshold
is hard-coded: years, top-N, vote thresholds, window durations, rate limits and
paths all come from `conf/settings.yaml`.

Code quality checks:

```bash
docker compose exec spark ruff check .
docker compose exec spark black --check .
docker compose exec spark pytest
```

## 6. Data sources, licences and access policies

| Source | Use | Licence / terms |
| --- | --- | --- |
| [IMDb non-commercial datasets](https://developer.imdb.com/non-commercial-datasets/) | The seven base tables | Personal and non-commercial use; the files are downloaded by script and never committed |
| [Wikipedia](https://en.wikipedia.org/) (English), MediaWiki Action API | Film synopsis, biography lead section | Text under CC BY-SA 4.0; each record keeps the page URL, revision id and permanent link |
| [Wikidata](https://www.wikidata.org/), Wikidata Query Service | IMDb identifier (P345) to page mapping, structured statements (dates, places, languages) | CC0 1.0 |
| [Wikimedia EventStreams](https://stream.wikimedia.org/) | Live `recentchange` stream for the streaming section | Public stream |

Access rules implemented in `imdb_project.enrichment.http_client` and used by
every collection step:

- identifying User-Agent `ECE-BigData-IMDb-Project/1.0 (<contact>)`;
- strictly sequential requests, at most `wikimedia.max_requests_per_second` (1);
- `maxlag=5` on MediaWiki API calls; `Retry-After` honoured on HTTP 429 / 503 and
  on `maxlag` errors, exponential back-off otherwise;
- disk cache of every raw response: a request is never sent twice;
- only human-written text is collected (Wikipedia article text); no machine
  generated text, no Wikidata descriptions.

`robots.txt`: the client reads the `robots.txt` of each host and records its
verdict in `outputs/enrichment/collection_stats.md` and in the streaming summary.
The Wikimedia `robots.txt` files address web crawlers and disallow `/w/` (hence
`/w/api.php`), `/sparql` and the whole `stream.wikimedia.org` host for them,
whereas these endpoints are the documented programmatic interfaces. With the
default `wikimedia.robots.policy: report` the verdict is reported and the
documented API is used; with `enforce` any disallowed URL is refused and nothing
is collected.

## 7. AI / LLM tools declaration

| Tool | Model | Tasks that relied on it |
| --- | --- | --- |
| Claude Code (Anthropic), agentic coding assistant, in sessions driven by Quentin HEITZ | Claude Fable 5.2 (as declared by the author) | Generation and debugging of the code delivered in PRs #1–#13: Docker and Compose configuration, PySpark preparation/exploration/enrichment jobs, Wikimedia HTTP clients, Kafka producer and lookup, shell scripts, settings and unit tests. Generation of the existing preparation tables in `outputs/`. Drafting of commit messages, PR descriptions, `README.md` and `PROJECT.md`. The Structured Streaming job, open question implementation and report renderer remain pending. |
| Codex (OpenAI), in sessions driven by Maxence SIMONET | GPT-6 | Windows PowerShell and Docker setup; execution of tests, Ruff and Black; review of PRs #1–#13, synthetic reproductions, merge-conflict checks and publication of review comments. Implementation of the review corrections and regression tests for primary keys, array cleanup, Q5/Q7, API errors, language-scoped caching, Kafka backpressure, download integrity and CSV export metadata. Updates to the execution guide and preparation of the correction PR. No `REPORT.md` prose was generated. |

- The brief given to the tool is versioned in [CLAUDE.md](CLAUDE.md): it fixes the
  architecture, the definitions and the default thresholds that the tool
  implemented. Implementation choices that the brief left open (for example the
  categories exempt from the posthumous credit rule, the language fallback of
  exploration Q6, or the handling of `robots.txt` described in section 6) were
  proposed by the tool; they are parameters of `conf/settings.yaml` and are listed
  in the pull request descriptions.
- The tables between `AUTO` markers in `REPORT.md` are produced by the code.
- **No AI tool was used to write the explanations and the reasoning of
  `REPORT.md`** (methodological explanations, alternatives and trade-offs, key
  takeaways, description of the open question): these parts are written by the
  authors.
