# Report

## 1. Data Preparation

### Results

<!-- AUTO:preparation:start -->
<!-- AUTO:preparation:end -->

### Methodological Explanation

#### Methodology and why it was chosen

The pipeline is split into layers (`raw` → `bronze` → `silver`, plus a `quarantine` area). Each layer can be re-run and checked on its own.

- **Bronze ingestion.** We read the seven TSV files with an explicit schema in which every column is a string. Quoting is disabled and `\N` is left as it is. The result is written once to Parquet. Reading everything as text means nothing is converted silently before we have looked at it. A value that fails to cast would otherwise become a null, and we could not tell it apart from a value that is really missing. Quoting is disabled because some IMDb titles contain unbalanced `"` characters, which would merge lines together. We also count malformed lines (lines with the wrong number of fields). There were none in 216.6 M rows.
- **Missing-value profile.** For each of the 39 columns, we count Spark nulls, `\N`, empty strings, whitespace-only strings and empty arrays separately, in a single pass per table. Keeping the forms apart shows where the missing values come from. In this snapshot, every missing value is an IMDb `\N`: no column contains Spark nulls, empty strings, whitespace-only values or empty arrays.
- **Standardisation.** `\N`, empty and blank values become null. Columns are cast to their real types, and multi-valued columns (`genres`, `directors`, `knownForTitles`, `characters`, …) become `array<string>`. Values that cannot be cast are recorded in a `_cast_errors` column instead of being dropped. We use only native Spark functions, with no Python UDFs, so the job stays fast on 100 M+ rows.
- **Quality rules.** Each check is a declarative rule `(rule_id, table, description, condition)`, from DQ01 to DQ16. One generic engine evaluates them and returns the number of violations, the share of the table and a sample of 10 rows. Adding a rule is a one-line change. Foreign keys are checked with anti-joins.
- **Handling.** We treat two kinds of problems differently:
  - Rows that are *structurally* broken go to `data/quarantine/<table>/`, with a `dq_reason` column. This means a duplicate or missing primary key, or a fact row that points to a person or series that does not exist. These rows cannot be joined correctly. If we kept them in silver, they would cause silent losses or wrong counts later.
  - Rows that are *probably wrong but still usable* stay in silver. This covers cases such as death before birth, a credit after death, an extreme runtime or season 0. Each of these rows gets a `dq_flags` array that lists the rules it breaks, and each analysis decides whether to exclude it.

  The only value we change is a runtime ≤ 0, which we set to null (4 values), because such a duration has no meaning. We never impute.

The three layers reconcile exactly: 216,606,868 silver rows + 8,268 quarantined rows = 216,615,136 bronze rows.

Everything had to run on a 16 GB laptop, with about 10 GB available to Docker. Converting to Parquet once means later jobs read only the columns they need, in compressed form, instead of parsing gzipped TSV again. Our first cleaning run on `title_principals` (102 M rows) ran out of native memory. We then lowered the settings to `local[4]` with a 4 GB driver and 64 shuffle partitions (with AQE), and used smaller Parquet batches.

#### Alternatives considered and trade-offs

- **Schema inference** (`inferSchema`): simpler, but it costs an extra full pass over the data, and `\N` would push numeric columns to strings anyway. We chose explicit schemas, defined once in `common/schemas.py`.
- **Dropping invalid rows**: silver would look cleaner, but we would lose information and the row counts would no longer reconcile. Quarantine keeps every rejected row together with its reason.
- **Imputation** (e.g. median runtime per genre, estimated birth years): this fills gaps by inventing values, and those values would then feed the exploration (outliers in Q1, career lengths in Q7). The missing values are concentrated in columns we barely use, so we would have gained little and risked a lot.
- **Correcting rows by hand** (e.g. the 28 cases of death before birth): not reproducible, and we cannot know which of the two years is wrong. The sample also shows that most of these rows are not real errors: they are ancient authors such as Aeschylus, Homer or Virgil, whose BC dates are stored as positive years.
- **pandas**: not realistic for `title_principals` and `title_akas` with 16 GB of RAM.

The cost of flagging rather than deleting is that downstream queries must remember to filter on `dq_flags` when it matters.

### Key takeaways

- IMDb is structurally clean: no malformed lines, no duplicate keys, and only 8,268 rows (0.004 %) had to be quarantined. Almost all of them (8,263) are principals pointing to a person who is missing from `name.basics`.
- Missing values are concentrated in a few columns: `title_akas.attributes` (99.5 %), `endYear` (98.7 %), `deathYear` (98.3 %), `birthYear` (95.7 %) and `principals.job` (80.7 %). `endYear` and `deathYear` are mostly empty for normal reasons (ongoing series, living people). However, `birthYear` is missing for 96 % of people, which limits any age-based analysis.
- Logical errors are rare but real: 23,742 credits more than 5 years after death (archive footage, writers and composers excluded), 1,159 credits before birth (all composers on silent films in the sample), 446 extreme runtimes and 7,125 episodes with a season or episode number ≤ 0. These are small numbers compared with the table sizes, so flagging them is enough.
- A flag is not a verdict. DQ02 flags Jeanne Calment, who really lived to 122, and DQ01 mostly flags ancient authors with BC dates. Deleting these rows would have removed correct data.

## 2. Data Exploration

### Q1. Runtime outliers by genre

#### Results

<!-- AUTO:q1:start -->
<!-- AUTO:q1:end -->

### Q2. Most popular genres by year

#### Results

<!-- AUTO:q2:start -->
<!-- AUTO:q2:end -->

### Q3. Top genres versus the rest

#### Results

<!-- AUTO:q3:start -->
<!-- AUTO:q3:end -->

### Q4. Directors with one highly rated film

#### Results

<!-- AUTO:q4:start -->
<!-- AUTO:q4:end -->

### Q5. Series with a decline in their final season

#### Results

<!-- AUTO:q5:start -->
<!-- AUTO:q5:end -->

### Q6. Actors successful across languages

#### Results

<!-- AUTO:q6:start -->
<!-- AUTO:q6:end -->

### Q7. Actors with an early career peak

#### Results

<!-- AUTO:q7:start -->
<!-- AUTO:q7:end -->

### Q8. Professionals with multiple roles

#### Results

<!-- AUTO:q8:start -->
<!-- AUTO:q8:end -->

### Methodological Explanation

#### Methodology and why it was chosen

All eight questions read the silver tables and share the same conventions, defined in `conf/settings.yaml` and `exploration/base.py`:

- A **feature-length movie** is a title with `titleType = movie` and a runtime of at least 40 minutes, adult titles excluded. 40 minutes is the usual threshold for a feature film.
- Any analysis based on ratings keeps only movies with **at least 1,000 votes**, which leaves 49,434 movies. With fewer votes, a handful of users can give a movie almost any score.
- Genres are **exploded**: a movie tagged `Drama,Romance` counts in both genres.
- **Popularity** means the number of votes.

Each question writes a Markdown summary, with its parameters at the top, and a CSV containing the full results. This way, the thresholds always appear next to the numbers.

**Q1.** For each genre with at least 30 movies, we compute the mean, the standard deviation and the quartiles of the runtime. A movie is an outlier when |z| > 2 **or** when it falls outside the fences [Q1 − 1.5·IQR, Q3 + 1.5·IQR]. We use two methods because runtimes are very skewed. A few extremely long documentaries push the standard deviation of Documentary to 223 minutes, which makes the z-score threshold so wide that it catches almost nothing. The IQR fences rely on quartiles and are not affected by those extremes. In practice, most outliers are found by the IQR alone (for Drama: 6,743 by IQR only, 1,964 by both, 0 by z-score only). We keep the union and record which method fired.

**Q2.** We sum `numVotes` per (year, genre) for 1980–2025 and rank genres with `dense_rank`, so that ties share a rank. We also keep the number of movies and the vote-weighted rating, to see whether a genre is popular because it has many movies or a few very-watched ones. Votes measure audience. A count of movies would measure production, and an average rating says nothing about how many people watched.

**Q3.** For each year, we compare the top 3 genres with all other genres combined: share of votes, vote-weighted rating and ratio between the two groups. We then aggregate by decade and count how many years each genre appears in the top 3.

**Q4.** Directors come from the union of `title.crew.directors` and the `director` category of `title.principals`, deduplicated, because each source misses some credits. We keep directors with exactly one movie rated ≥ 8.0 and at least two other movies whose average rating is ≤ 6.0. We read "multiple" as "at least two".

**Q5.** We keep series with at least 3 seasons that each have ≥ 10 rated episodes (≥ 50 votes per episode). The last season is identified *before* the vote filter. Otherwise, a recent season with few votes would disappear, and the season before it would wrongly be treated as the last one. Ties are handled in `all` mode: when several episodes share the worst or best rating, all of them must sit in the expected seasons.

**Q6.** A movie is a success if it is rated ≥ 7.0 with ≥ 10,000 votes. Its original language comes from Wikidata (property P364, found through the IMDb ID, P345), with `title.akas` as a fallback. `title.akas` lists release titles by *region*, and a region is not a language. An Indian film has region `IN` whether it is in Hindi, Tamil or Telugu, which matters for actors like Prakash Raj. Movies with several original languages are excluded, so that a single film cannot add two languages to an actor's count. Together with the 70 movies whose language is unknown, this leaves 4,311 of the 4,974 successful movies.

**Q7.** We keep actors and actresses whose career lasts at least 20 years (from their first to their last rated movie) and who have at least 15 rated movies. A career has an *early peak* when the best movie falls in the first third of the career **and** the average rating of the first half is higher than that of the second half. Requiring both conditions avoids calling a career "early peak" because of one lucky early hit. We also compute the slope of rating against year (`covar_samp / var_samp`) as a continuous measure.

**Q8.** A person is multi-talented if they hold at least two of the roles {director, writer, actor}, with at least 3 movies in each. For each person, we compare the average rating of the movies where they combine roles with the movies where they hold a single role. The comparison is done *per person*, so each person is their own control. Comparing all multi-role movies with all single-role movies would mostly compare different people.

#### Alternatives considered and trade-offs

- **Thresholds.** `min_votes = 1,000` trades coverage for reliability. A threshold of 10,000 would remove most older and non-English movies. With 100, obscure titles rated 9+ would dominate, and even at 1,000 this still happens in Q4 with very recent films. We considered a Bayesian weighted rating, which pulls low-vote ratings toward the mean, but it adds a parameter and makes the results harder to explain.
- **Q1.** We could have used only the z-score (simple, but unreliable on skewed genres), only the IQR, or a robust z-score based on the median absolute deviation. We kept the two standard methods side by side.
- **Q2/Q3.** We could have measured popularity by number of movies or by average rating. Votes favour recent movies, because IMDb users vote more for what they watch now. We accepted this bias because the question is about popularity.
- **Q6.** Using `title.akas` alone would have avoided an external source, but it confuses region and language. Wikidata adds a dependency and gives the language of 98.4 % of the movies.
- **Q7.** We could have used only one of the two measures. The slope is affected by the general decline of ratings over careers. The halves-and-third rule is closer to the wording of the question.
- **Q8.** A regression with one fixed effect per person would test the same idea and give a confidence interval. We kept the simpler paired comparison.

### Key takeaways

- **Drama dominates.** It ranks first in 41 of the 46 years and appears in the top 3 every year, with 15–33 % of the votes (peak in 1994). Part of this is mechanical: Drama is the most common tag (196,130 of the 456,414 feature films), and with exploded genres, every "drama + something" movie adds its votes to Drama.
- **The top 3 genres take 42–47 % of all votes** and are slightly better rated than the rest (+0.02 to +0.25 points depending on the decade). This means more than half of the audience goes to the ~18 other genres.
- **The lead of the top 3 comes partly from volume.** In the 1990s and 2000s, top-3 films actually get fewer votes per film than the rest (ratio 0.88 and 0.84): these genres win because they have more films. The rating gap is not stable either; in some years the rest is better rated (−0.34 in 2008).
- **Runtime outliers are mostly long movies** (30,234 longer than normal against 5,323 shorter), and the count depends heavily on the method used. The most extreme cases are experimental works (*Logistics*, 2012, listed at 51,420 minutes) and silent-era serials (*Les Vampires*, 421 minutes), not mainstream films.
- **Rating-based results are sensitive to vote counts.** The first two directors in Q4 owe their place to 2026 films rated 9.8 and 9.3 with only 5,026 and 1,760 votes. Ratings from early, enthusiastic voters like these will probably drop. Irvin Kershner is the textbook case: *The Empire Strikes Back* is rated 8.7 with 1.5 M votes, while his 9 other movies average 5.94. M. Night Shyamalan (*The Sixth Sense*, 15 other movies averaging 5.87) and James McTeigue (*V for Vendetta*) are also on the list of 47. Two rows (Sateesh Paramveda and Satish Paramvedha) look like the same person under two IMDb IDs, a duplicate that our key checks cannot detect.
- **171 of 1,364 eligible series (12.5 %)** have their worst episode in the last season and their best in the first two (e.g. *The Flash*: 9.6 in season 1, 3.8 in season 9).
- **650 people succeeded in ≥ 2 languages and 74 in ≥ 3.** English dominates the successful movies (2,802), followed by Hindi, French and Japanese. Indian cinema produces many multilingual careers (Prakash Raj: 4 languages). One limit is that the language labels are noisy. Wikidata separates Cantonese and Yue Chinese (Jackie Chan, Maggie Cheung, Carina Lau), tags *Red Cliff II* as German and *Quest for Fire* as an "artistic language". A few counts are therefore one language too high.
- **44 % of long careers (1,557 of 3,528) peak early** (e.g. Edward Furlong with *Terminator 2*, Shelley Duvall with *The Shining*), but even among the others, two thirds have a negative slope. Ratings tend to decline over a career in general. The likely reasons are that old movies still rated today are the ones remembered for being good, and that actors take smaller roles later in their career.
- **Combining roles goes with a small gain**: +0.12 points in median, and 57.6 % of people are rated higher when they combine roles. The effect is small next to the spread between people (standard deviation 0.78), but with 2,734 people the mean difference is about 7 standard errors above zero, so it is unlikely to be noise. Individual cases go both ways: Woody Allen gains +1.02 when he combines roles, Tyler Perry loses −1.07. The gain probably reflects selection: people write and direct their personal projects. Actor + director is the only combination with a negative mean difference (−0.06).

## 3. Data Enrichment

### Results

<!-- AUTO:enrichment:start -->
<!-- AUTO:enrichment:end -->

### Methodological Explanation

#### Methodology and why it was chosen

- **Scope (Spark).** We take feature films from 1980–2025 and keep the top 10 per (genre, year), ranked by votes then by rating. This gives 9,832 selections and 6,821 distinct films. For each film, we take the first 3 principals among actor, actress, director and writer, in IMDb `ordering`, which gives 9,759 people. The scope depends only on parameters: with `top_n: null` and `year_min: null`, the same code processes the whole dataset. The HTTP layer works in batches and resumes from its cache, so a larger scope changes the run time, not the code.
- **Source.** We use English Wikipedia for text (CC BY-SA 4.0). Wikidata (CC0) serves only to map IMDb IDs (P345) to Wikipedia pages and to retrieve structured facts about people: birth date and place, death date and nationality. We use a single source, as the instructions allow, because Wikipedia covers these films well and its text is written by people.
- **Matching by ID, not by title.** We run Wikidata SPARQL queries in batches (`VALUES ?imdb {…}` on P345). An exact ID match avoids homonyms such as *Crash* or *It*, which a title search would confuse.
- **Text.** We use the MediaWiki API. For films, we take the Plot section (or Synopsis, Premise, Summary, …). If no such section exists, we take the lead section and set the status to `no_plot_section`. For people, we take the introduction (`exintro`, `explaintext`), in batches of 20. We also store the `revid`, so each record links to the exact revision we read.
- **Collection (Python, outside Spark, as allowed).** A single-threaded client sends at most 1 request per second, with `maxlag=5`. It honours `Retry-After` on 429/503 responses, with exponential backoff and at most 6 attempts. It identifies itself with a User-Agent that includes a contact email. Every raw response is cached on disk, so an interrupted run resumes without sending any request twice.
- **Everything else in Spark.** Spark reads the JSON cache with an enforced schema and cleans the text: trimming, collapsing whitespace, removing `[1]`-style reference markers, and applying a minimum length of 200 characters for a synopsis and 100 for a biography. It then joins the result to silver and writes `data/gold/enriched_films/` and `enriched_people/`.
- **Lineage.** Every record carries `source_name`, `source_url`, `source_revision_id`, `source_permalink`, `retrieved_at`, `license`, `enrichment_status` and `enrichment_note`. When information is missing, the note is built by code from a fixed template (for example, "no English Wikipedia page"). It states the status and contains no generated content about the film.

**No machine-generated text.** Every text we keep was written by Wikipedia editors. We deliberately ignore Wikidata descriptions. They are very short ("2010 film by …"), and many were created by bots, so we cannot guarantee that a person wrote them.

**Rate limits and `robots.txt`.** Before collecting, the client reads the `robots.txt` of each domain. For generic user agents, both endpoints we call (`en.wikipedia.org/w/api.php` and `query.wikidata.org/sparql`) come out as disallowed. Our policy is set to `report`: this is logged in the output, but it does not block the run. Our view is that `robots.txt` targets crawlers that follow links across a site. Wikimedia publishes separate rules for API clients (User-Agent policy and API etiquette: serial requests, `maxlag`, identification), and those are the rules we followed. We also fetch a fixed list of pages instead of crawling. We prefer to state this openly rather than hide it.

#### Alternatives considered and trade-offs

- **Scraping the HTML pages**: more fragile (it breaks when the layout changes), heavier on Wikimedia's servers, and closer to what `robots.txt` forbids. The API returns clean text and revision IDs.
- **Wikipedia dumps**: no rate-limit concerns, and the best option for the full IMDb scale. However, downloading and parsing tens of GB for about 16,000 pages was out of proportion for our scope.
- **TMDb / OMDb**: good synopsis coverage, but they need API keys, their terms restrict reuse, and their text is not under an open licence.
- **Other Wikipedia languages as a fallback**: better coverage for non-English films, but the output would mix languages, and the instructions do not require a second source.
- **Parallel requests**: much faster than our ~2 h 10 min of collection, but incompatible with the 1 request per second etiquette. We accepted the slower run.

### Key takeaways

- **86.6 % of films got a full synopsis** from a plot-like section, 5.4 % fell back to the introduction, 7.2 % have no English page and 0.8 % are partial. A plot section is far richer than an introduction (median of 3,605 characters against 483), so the introduction is a fallback, not an equivalent. Films without a plot section are mostly documentaries (*Man on Wire*, *March of the Penguins*), whose articles naturally have no Plot heading.
- **People are harder to cover**: 73.6 % `ok`, 15.2 % `not_found` and 11.2 % `partial`. Less-known principals often have no article.
- **Coverage depends on the decade**: 92.8 % (1980s), 94.9 % (1990s), 95.1 % (2000s), 91.2 % (2010s) and 88.7 % (2020s). Recent films are less likely to have a page or a written plot yet.
- **The polite collection worked**: 6,850 requests and 0 failures. The client retried 10 times (3 HTTP 429, 1 HTTP 5xx, 6 network errors), and every retry succeeded. Thanks to the cache, the interruption when the machine went to sleep overnight had no effect.
- **3 principals per film is not always reachable**: 6,319 films have 3 selected principals, and 5,049 have a biography for all three.

## 4. Streaming

### Results

<!-- AUTO:streaming:start -->
<!-- AUTO:streaming:end -->

### Methodological Explanation

#### Methodology and why it was chosen

The pipeline is: Wikimedia EventStreams (`recentchange`, SSE) → Python producer → Kafka topic `wikistreams` → Spark Structured Streaming → Parquet + console.

- **Producer.** It reads the SSE stream and keeps only `enwiki`/`frwiki` events of type `edit`/`new` in namespace 0 (articles). It publishes the raw JSON to Kafka, with `meta.id` as the key. After a disconnection, it resumes with `Last-Event-ID`, so no events are skipped. The cost is that a few events may be sent twice, which the dedup step handles downstream.
- **Lookup table.** Before the stream starts, a Spark batch job builds `data/gold/wiki_lookup/`. It maps the 30,000 most-voted titles and 20,000 people to their enwiki/frwiki pages through Wikidata, which gives 88,273 pages with a normalised title, the IMDb ID and the entity type. The table is small enough to be broadcast.
- **Relevance.** An event is relevant if its (wiki, normalised title) is in the lookup **or** if its title matches a pattern such as "(film)", "(TV series)", "(actor)" or "(série télévisée)". The `match_reason` column records which rule fired. The lookup links an edit to an exact IMDb ID. The patterns catch pages outside the lookup, such as less-voted titles or new pages. Together, they ensure that several events match within the test window: we got 72 in 20 minutes.
- **Streaming job.** Spark reads Kafka with an explicit JSON schema and uses `meta.dt` (the time of the edit on Wikipedia) as event time. It applies a 10-minute watermark and `dropDuplicatesWithinWatermark(event_id)`. Three independent queries run, each with its own checkpoint:
  1. relevant events → Parquet (append);
  2. 5-minute tumbling windows;
  3. 10-minute sliding windows with a 5-minute slide.

  The window queries count events per wiki, entity type, bot/human and page, and compute the average size change. They write in append mode through `foreachBatch`, to Parquet and to the console.
- **Metrics.** A `StreamingQueryListener` writes every progress event to `outputs/streaming/progress.jsonl`: input rows, rates, durations, watermark and rows dropped by the watermark.
- The job stops cleanly after the configured duration.

**Why Kafka.** Kafka decouples the source from Spark. Spark has no native SSE source and cannot replay the Wikimedia stream itself. With Kafka in between, events wait in the topic if Spark restarts, and Spark resumes from the offsets saved in its checkpoint. Several queries can also read the same topic independently.

**Why two window types.** Tumbling windows do not overlap, so their counts add up to the total, which is convenient for reporting. Sliding windows count each event twice and give a smoother trend, which shows bursts that straddle a window boundary.

#### Alternatives considered and trade-offs

- **Reading the SSE stream directly from Spark** (custom source or socket): no replay and no buffer, and Spark would depend on the availability of the source.
- **Patterns only**: no lookup to build (about 17 minutes on the first run), but they miss pages whose title gives no hint, such as *Slow Horses* or *John Steinbeck*. **Lookup only** misses films outside the top 30,000. Each rule found events the other missed: 34 by the lookup only, 26 by the patterns only, 12 by both.
- **Matching against the full IMDb title list**: far larger, and full of false positives, because common words ("Home", "Love") are also IMDb titles.
- **`update` or `complete` output mode**: earlier results, but windows get rewritten, which does not fit an append-only Parquet sink, and `complete` keeps all the state forever.
- **Processing-time windows**: no late-data problem, but the counts would reflect when Spark processed events, not when the edits happened.

### Late-arriving data

Events can arrive late for several reasons: a reconnection of the producer, lag in Kafka, or Spark restarting and reading a backlog. We work in **event time** (`meta.dt`) and use a **10-minute watermark**. Spark tracks the latest event time it has seen and assumes that no event older than that time minus 10 minutes will still arrive. In practice:

- an event up to 10 minutes late is still counted in its correct window;
- an older event is dropped by the stateful operators (window aggregation and dedup) and counted in `numRowsDroppedByWatermark`;
- in append mode, a window is written only once the watermark has passed its end. A 5-minute window is therefore final about 10 minutes after it closes, and it is never rewritten;
- state older than the watermark (old windows, seen IDs) is purged, so memory stays bounded however long the stream runs.

**Why 10 minutes.** The `recentchange` stream is close to real time, and normal delays are a few seconds. Ten minutes covers a producer reconnection or a short Spark restart, while keeping the delay before results acceptable in a 20-minute run and the state small. The trade-off is simple: a larger watermark gives more complete counts, but later results and more state; a smaller one gives faster results, but drops more events.

**Deduplication.** `dropDuplicatesWithinWatermark(event_id)` removes duplicates caused by the `Last-Event-ID` replay or by producer retries (Kafka is at-least-once here). Because it is bounded by the watermark, the set of seen IDs does not grow forever. A plain `dropDuplicates` on `event_id` would have to remember every ID.

**Experiment.** After 12 minutes, an injector republished 10 real events with new IDs, so that the dedup would not remove them: 5 with `meta.dt` moved back by 5 minutes, and 5 moved back by 30 minutes.

| Injected delay | Expected | Observed |
|---|---|---|
| 5 min (< watermark) | accepted | accepted, present in the sink |
| 30 min (> watermark) | dropped | dropped: 5 rows in `numRowsDroppedByWatermark` for each query |

The behaviour matches the theory. The 5-minute-late events carried an event time of 14:58:19 UTC, which was still above the watermark; the 30-minute-late ones (14:33:19 UTC) were below it.

The cost of the watermark is visible in the window outputs too. When the job stopped, the watermark was about 10 minutes behind the latest event, so only the windows ending at 14:55 and 15:00 UTC were finalized and written. Edits from the last ten minutes of the run were still sitting in open windows.

The limit is that dropped events are lost from the aggregates and only counted. If they mattered, we could compare their event time with the current watermark in `foreachBatch`, send them to a separate sink, and reconcile them later in batch.

### Key takeaways

- In 20 minutes, the matched-events query read **2,113 events** (each window query read 2,055, since every query reads Kafka on its own), at about 1 to 2.6 events per second after the producer filter. **72 were relevant** (67 real + 5 injected), or about 3.4 %. This is well above "multiple matches" for the test window.
- enwiki accounts for 50 of the relevant events and frwiki for 22. By type: 32 films, 20 people and 20 series. 14 edits (19 %) came from bots, 13 of them on enwiki, which do a visible share of maintenance even on film pages. The bot flag is kept so they can be filtered out.
- The lookup and the patterns are complementary (34 / 26 / 12): neither would have been enough alone. People are found almost only through the lookup (17 of 20), because their page titles rarely carry a hint like "(actor)". Bot edits, in contrast, were mostly caught by the patterns (10 of 14).
- A trigger takes about 5–7 seconds for the window queries and 10–20 seconds for the matched-events query, and the input rate is low. The bottleneck is the source, not Spark, so a single local container is enough.
- The injection experiment confirms that the watermark accepts events that are slightly late and drops events that are too late, as designed.

## 5. Open Question

### Question and motivation

**Do repeated director–actor collaborations produce better-rated films than the first one?**

Many directors work with the same actors again and again: Kurosawa with Toshirō Mifune and Takashi Shimura, Ozu with Chishū Ryū, Bergman with Gunnar Björnstrand. Two stories are possible. Either familiarity improves the work, or a director brings an actor back after a success and the following films do not live up to it. IMDb lets us test this on tens of thousands of pairs. The question needs joins between four tables and window functions per pair, which makes it a non-trivial Spark problem.

### Data

IMDb only, with no external data:

- `title.basics` (type, year, runtime) and `title.ratings`: the same 49,434 rated feature films as the exploration (≥ 1,000 votes);
- `title.crew` and `title.principals` for directors, using the same union as Q4;
- `title.principals` for actors and actresses;
- `name.basics` for names.

Films where the director also acts are excluded from the pairs, because directing yourself is not a collaboration.

### Results

<!-- AUTO:open_question:start -->
<!-- AUTO:open_question:end -->

### Key takeaways

- **Collaborations rarely repeat**: only 26,630 of the 469,141 pairs (5.7 %) worked together on at least two films.
- **The first film of a recurring pair is already rated well above average**: 6.61 against 6.13 for one-off pairs. A success makes a new collaboration more likely.
- **Follow-up films are rated lower than the first**: −0.28 on average (median −0.20, t = −53.7), and 60.8 % of pairs decline. The gap stays between −0.24 and −0.40 at every collaboration rank.
- **However, the pair still does better than the director's other work**: the follow-ups are rated +0.12 above the films the same director made, over the same period, without that actor, and 57.1 % of pairs are above this baseline. This excess grows with the number of collaborations (+0.10 for pairs with 2 films, +0.22 for pairs with 6 or more), while the delta stays around −0.28.
- **Kartal Tibet and Kemal Sunal show both effects at once.** Their first film, *Tosun Pasha* (8.8), was never matched (delta −1.97), but their 25 other films are still rated 1.43 points above Tibet's work without Sunal.
- **How we read it.** The decline relative to the first film looks like regression to the mean. Pairs are selected on a good first film, so the next films can only be expected to fall back toward the director's usual level. The general decline of ratings over careers, seen in Q7, adds to this effect. The positive excess suggests that working again with the same actor goes with slightly better films than the director's other work. Familiarity seems to help a little, but it does not repeat the first success.
- **This is correlation, not causation.** Directors may cast their regular actors in their more personal or better-funded projects.

### Methodological Explanation

#### Methodology and why it was chosen

- **Pairs.** We join director credits and actor credits on the same `tconst`, excluding cases where the director and the actor are the same person.
- **Order.** A Spark window partitioned by pair and ordered by year (then `tconst` for ties) numbers the films of each pair.
- **Delta.** For each recurring pair, the delta is the average rating of the follow-up films minus the rating of the first film. Averaging the follow-ups gives each pair exactly one value, so a pair with 26 films does not weigh more than a pair with two.
- **Excess.** The excess is the average rating of the follow-ups minus the average rating of the director's films *without* that actor, released after the pair's first film. This baseline controls for the director's general level and for the period. 21,573 pairs have such a baseline.
- **Statistics.** We compute a paired t statistic on the delta, and use a tolerance of 0.05 to classify each pair as better, equal or worse. We also build profiles by collaboration rank and by number of collaborations, and list the most frequent pairs.

We chose this design because it is simple to explain and each pair serves as its own control. We added the director baseline after seeing that the negative delta could be explained by selection alone.

#### Alternatives considered and trade-offs

- **Comparing all films of recurring pairs with all films of one-off pairs**: easy, but it mixes first films and follow-ups, and selection drives the result (6.61 against 6.13 before any follow-up is made).
- **A regression with director, actor and year effects**: it would separate the effects better and give proper confidence intervals, but it is heavier to build in Spark and harder to explain. We kept paired comparisons.
- **Matching each follow-up with a film the same director made in the same year**: a closer control, but many directors do not make a film every year, so far fewer pairs would remain.
- **Weighting by number of votes**: famous pairs would dominate the result. We gave every pair the same weight.
- **External data (budgets, box office)**: would help control for the size of the project, but we found no open, human-written source with good coverage, and budgets in Wikipedia infoboxes are patchy.

One limit of our approach is that the t statistic assumes the pairs are independent. Pairs that share a director or an actor are not independent, so t = −53.7 overstates how certain the result is. The sign and the size of the effect remain informative.
