# Report

IMDb snapshot of 13 November 2026. This report shows the key results of each part. The complete outputs (every row, every parameter) are in `outputs/` as Markdown and CSV files, and in `data/gold/`.

## 1. Data Preparation

### Results

<!-- AUTO:preparation:start -->
#### Ingestion (bronze)

All seven files were read as text and written to Parquet. No malformed line was found.

| Table | Rows | Columns | Malformed rows |
| --- | ---: | ---: | ---: |
| name_basics | 15,811,387 | 6 | 0 |
| title_akas | 60,385,482 | 8 | 0 |
| title_basics | 12,958,477 | 9 | 0 |
| title_crew | 12,958,477 | 3 | 0 |
| title_episode | 10,030,795 | 4 | 0 |
| title_principals | 102,738,762 | 6 | 0 |
| title_ratings | 1,731,756 | 3 | 0 |
| **Total** | **216,615,136** | | **0** |

#### Missing values

39 columns profiled. Every missing value is an IMDb `\N`: the counts of Spark nulls, empty strings, whitespace-only values and empty arrays are all 0.

| Rank | Table | Column | Missing | % missing |
| ---: | --- | --- | ---: | ---: |
| 1 | title_akas | attributes | 60,068,229 | 99.47 % |
| 2 | title_basics | endYear | 12,794,047 | 98.73 % |
| 3 | name_basics | deathYear | 15,545,911 | 98.32 % |
| 4 | name_basics | birthYear | 15,125,575 | 95.66 % |
| 5 | title_principals | job | 82,869,755 | 80.66 % |

Other columns above 30 %: `title_akas.types` (66.9 %), `title_basics.runtimeMinutes` (62.2 %), `title_principals.characters` (51.3 %), `title_crew.writers` (49.6 %), `title_crew.directors` (44.7 %), `title_akas.language` (32.5 %).

#### Data quality issues

47 rule/table checks (DQ01–DQ16). Only the rules with at least one violation are listed. DQ06 and DQ09 to DQ16 found none: no duplicate or missing keys, no unknown genre, no rating out of range.

| Rule | Table | Issue | Violations |
| --- | --- | --- | ---: |
| DQ01 | name_basics | deathYear earlier than birthYear | 28 |
| DQ02 | name_basics | age at death above 120 years | 2 |
| DQ03 | title_principals | credited more than 5 years after death (archive footage, writers, composers excluded) | 23,742 |
| DQ04 | title_principals | credited on a title released before birth | 1,159 |
| DQ05 | title_principals | `nconst` missing from name_basics | 8,263 |
| DQ05 | title_crew | orphan directors / orphan writers | 419 / 812 |
| DQ05 | name_basics | orphan `knownForTitles` | 6 |
| DQ05 | title_episode | `parentTconst` missing from title_basics | 5 |
| DQ07 | title_basics | startYear more than 5 years in the future | 3 |
| DQ08 | title_basics | runtime ≤ 0 or above 1,000 min | 446 |
| DQ14 | title_episode | season or episode number ≤ 0 | 7,125 |

Examples from the samples: DQ01 is mostly ancient authors (Aeschylus 525–456, Homer, Virgil), DQ02 contains Jeanne Calment (1875–1997), and the DQ04 sample is made only of composers credited on silent films.

#### Cleaning (bronze → silver)

| Table | Bronze | Silver | Quarantined | Flagged rows |
| --- | ---: | ---: | ---: | ---: |
| name_basics | 15,811,387 | 15,811,387 | 0 | 36 |
| title_akas | 60,385,482 | 60,385,482 | 0 | 0 |
| title_basics | 12,958,477 | 12,958,477 | 0 | 449 |
| title_crew | 12,958,477 | 12,958,477 | 0 | 1,033 |
| title_episode | 10,030,795 | 10,030,790 | 5 | 7,125 |
| title_principals | 102,738,762 | 102,730,499 | 8,263 | 24,901 |
| title_ratings | 1,731,756 | 1,731,756 | 0 | 0 |

- Quarantine reasons: 8,263 principals pointing to a missing person (DQ05:nconst) and 5 episodes pointing to a missing series (DQ05:parentTconst).
- Deterministic corrections: 4 runtimes ≤ 0 set to null. No other value changed, no imputation.
- 216,606,868 silver rows + 8,268 quarantined rows = 216,615,136 bronze rows.
<!-- AUTO:preparation:end -->

### Methodological Explanation

#### Methodology and why it was chosen

The pipeline is split into layers (`raw` → `bronze` → `silver`, plus a `quarantine` area). Each layer can be re-run and checked on its own.

- **Bronze ingestion.** We read the seven TSV files with an explicit schema in which every column is a string. Quoting is disabled and `\N` is left as it is. The result is written once to Parquet. Reading everything as text means nothing is converted silently before we have looked at it. A value that fails to cast would otherwise become a null, and we could not tell it apart from a value that is really missing. Quoting is disabled because some IMDb titles contain unbalanced `"` characters, which would merge lines together.
- **Missing-value profile.** For each of the 39 columns, we count Spark nulls, `\N`, empty strings, whitespace-only strings and empty arrays separately, in a single pass per table. Keeping the forms apart shows where the missing values come from.
- **Standardisation.** `\N`, empty and blank values become null. Columns are cast to their real types, and multi-valued columns (`genres`, `directors`, `knownForTitles`, `characters`, …) become `array<string>`. Values that cannot be cast are recorded in a `_cast_errors` column instead of being dropped. We use only native Spark functions, with no Python UDFs, so the job stays fast on 100 M+ rows.
- **Quality rules.** Each check is a declarative rule `(rule_id, table, description, condition)`. One generic engine evaluates them and returns the number of violations, the share of the table and a sample of 10 rows. Adding a rule is a one-line change. Foreign keys are checked with anti-joins.
- **Handling.** We treat two kinds of problems differently:
  - Rows that are *structurally* broken go to `data/quarantine/<table>/`, with a `dq_reason` column. This means a duplicate or missing primary key, or a fact row that points to a person or series that does not exist. These rows cannot be joined correctly. If we kept them in silver, they would cause silent losses or wrong counts later.
  - Rows that are *probably wrong but still usable* stay in silver. Each of these rows gets a `dq_flags` array that lists the rules it breaks, and each analysis decides whether to exclude it.

  The only value we change is a runtime ≤ 0, which we set to null, because such a duration has no meaning. We never impute.

Everything had to run on a 16 GB laptop, with about 10 GB available to Docker. Converting to Parquet once means later jobs read only the columns they need, in compressed form, instead of parsing gzipped TSV again. Our first cleaning run on `title_principals` (102 M rows) ran out of native memory. We then lowered the settings to `local[4]` with a 4 GB driver and 64 shuffle partitions (with AQE), and used smaller Parquet batches.

#### Alternatives considered and trade-offs

- **Schema inference** (`inferSchema`): simpler, but it costs an extra full pass over the data, and `\N` would push numeric columns to strings anyway. We chose explicit schemas, defined once in `common/schemas.py`.
- **Dropping invalid rows**: silver would look cleaner, but we would lose information and the row counts would no longer reconcile. Quarantine keeps every rejected row together with its reason.
- **Imputation** (e.g. median runtime per genre, estimated birth years): this fills gaps by inventing values, and those values would then feed the exploration (outliers in Q1, career lengths in Q7). The missing values are concentrated in columns we barely use, so we would have gained little and risked a lot.
- **Correcting rows by hand** (e.g. the 28 cases of death before birth): not reproducible, and we cannot know which of the two years is wrong. Most of these rows are not even real errors: they are ancient authors whose BC dates are stored as positive years.
- **pandas**: not realistic for `title_principals` and `title_akas` with 16 GB of RAM.

The cost of flagging rather than deleting is that downstream queries must remember to filter on `dq_flags` when it matters.

### Key takeaways

- IMDb is structurally clean: no malformed lines, no duplicate keys, and only 8,268 rows (0.004 %) had to be quarantined.
- Missing values are concentrated in a few columns. `endYear` and `deathYear` are mostly empty for normal reasons (ongoing series, living people), but `birthYear` is missing for 96 % of people, which limits any age-based analysis.
- Logical errors are rare: 23,742 posthumous credits, 1,159 credits before birth, 446 extreme runtimes and 7,125 episodes numbered ≤ 0. They are small compared with the table sizes, so flagging them is enough.
- A flag is not a verdict. DQ02 flags Jeanne Calment, who really lived to 122, and DQ01 mostly flags ancient authors. Deleting these rows would have removed correct data.

## 2. Data Exploration

Shared conventions: feature film = `movie` with a runtime ≥ 40 min, adult titles excluded; rating analyses keep movies with ≥ 1,000 votes (49,434 movies); genres are exploded.

### Q1. Runtime outliers by genre

#### Results

<!-- AUTO:q1:start -->
Rule: outlier if |z| > 2 **or** runtime outside [Q1 − 1.5·IQR, Q3 + 1.5·IQR], for genres with at least 30 films (Game-Show, 7 films, is skipped).

- 456,414 feature films → **35,557 outlier (film, genre) pairs**, i.e. **24,177 distinct films**.
- 30,234 are longer than their genre's norm, 5,323 shorter.

Main genres:

| Genre | Films | Mean (min) | Std (min) | Median (min) | Outliers | % | z + IQR | z only | IQR only |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Drama | 196,130 | 96.1 | 37.0 | 93 | 8,707 | 4.4 % | 1,964 | 0 | 6,743 |
| Documentary | 116,181 | 78.0 | 223.4 | 74 | 2,079 | 1.8 % | 58 | 0 | 2,021 |
| Comedy | 95,772 | 93.3 | 28.7 | 91 | 7,237 | 7.6 % | 1,613 | 0 | 5,624 |
| Romance | 42,197 | 99.2 | 25.1 | 96 | 2,252 | 5.3 % | 1,987 | 82 | 183 |
| Action | 40,364 | 101.2 | 33.8 | 94 | 1,892 | 4.7 % | 841 | 0 | 1,051 |
| Crime | 34,410 | 95.7 | 25.6 | 93 | 2,101 | 6.1 % | 1,188 | 0 | 913 |
| Thriller | 34,052 | 96.1 | 21.8 | 93 | 2,526 | 7.4 % | 2,092 | 0 | 434 |
| Horror | 30,559 | 88.7 | 22.3 | 88 | 2,064 | 6.8 % | 707 | 0 | 1,357 |
| Biography | 16,107 | 89.2 | 29.4 | 88 | 469 | 2.9 % | 324 | 145 | 0 |
| Western | 6,353 | 76.5 | 28.7 | 70 | 148 | 2.3 % | 133 | 15 | 0 |

Most extreme cases:

| Film | Year | Genre | Runtime (min) | z-score |
| --- | ---: | --- | ---: | ---: |
| Logistics | 2012 | Documentary | 51,420 | 229.8 |
| Ambiancé | 2020 | Documentary | 43,200 | 193.0 |
| Carnets Filmés (Liste Complète) | 2019 | Documentary | 28,643 | 127.9 |
| Hunger! | 2015 | Drama | 6,000 | 159.6 |
| London EC1 | 2015 | Comedy | 5,460 | 186.7 |
<!-- AUTO:q1:end -->

### Q2. Most popular genres by year

#### Results

<!-- AUTO:q2:start -->
Popularity = sum of `numVotes` per (year, genre), 1980–2025, ranked with `dense_rank`. In brackets: the genre's share of the year's votes.

| Year | 1st | 2nd | 3rd |
| --- | --- | --- | --- |
| 1980 | Drama (17.8 %) | Adventure (14.5 %) | Horror (12.1 %) |
| 1981 | Adventure (20.6 %) | Drama (14.7 %) | Horror (11.6 %) |
| 1982 | Drama (17.9 %) | Sci-Fi (14.9 %) | Action (11.1 %) |
| 1983 | Drama (19.0 %) | Action (13.6 %) | Adventure (13.4 %) |
| 1984 | Action (17.0 %) | Adventure (13.7 %) | Drama (13.6 %) |
| 1985 | Comedy (21.4 %) | Adventure (16.2 %) | Drama (14.0 %) |
| 1986 | Drama (18.8 %) | Adventure (14.3 %) | Comedy (13.1 %) |
| 1987 | Drama (17.1 %) | Comedy (15.4 %) | Action (9.9 %) |
| 1988 | Comedy (17.9 %) | Drama (17.9 %) | Action (11.0 %) |
| 1989 | Comedy (20.9 %) | Drama (16.2 %) | Adventure (12.4 %) |
| 1990 | Drama (20.6 %) | Comedy (13.1 %) | Crime (11.8 %) |
| 1991 | Drama (19.6 %) | Crime (13.2 %) | Comedy (11.2 %) |
| 1992 | Drama (20.4 %) | Comedy (13.6 %) | Crime (12.2 %) |
| 1993 | Drama (24.3 %) | Comedy (12.1 %) | Crime (8.2 %) |
| 1994 | Drama (32.9 %) | Crime (13.6 %) | Comedy (11.8 %) |
| 1995 | Drama (23.2 %) | Crime (14.5 %) | Comedy (11.3 %) |
| 1996 | Drama (20.6 %) | Comedy (12.5 %) | Crime (11.8 %) |
| 1997 | Drama (22.2 %) | Action (12.0 %) | Comedy (9.8 %) |
| 1998 | Drama (21.7 %) | Comedy (18.2 %) | Crime (11.5 %) |
| 1999 | Drama (21.8 %) | Comedy (11.5 %) | Crime (10.2 %) |
| 2000 | Drama (20.6 %) | Comedy (13.2 %) | Adventure (11.2 %) |
| 2001 | Drama (18.5 %) | Comedy (12.0 %) | Adventure (11.8 %) |
| 2002 | Drama (21.1 %) | Adventure (10.9 %) | Action (10.5 %) |
| 2003 | Drama (16.8 %) | Action (15.0 %) | Comedy (13.6 %) |
| 2004 | Drama (17.4 %) | Action (12.3 %) | Comedy (11.6 %) |
| 2005 | Drama (16.6 %) | Comedy (12.4 %) | Action (11.2 %) |
| 2006 | Drama (21.5 %) | Comedy (12.1 %) | Adventure (9.0 %) |
| 2007 | Drama (18.0 %) | Comedy (11.4 %) | Adventure (8.8 %) |
| 2008 | Drama (16.6 %) | Action (12.9 %) | Comedy (10.7 %) |
| 2009 | Drama (16.7 %) | Comedy (12.9 %) | Action (11.7 %) |
| 2010 | Drama (15.8 %) | Action (12.2 %) | Adventure (12.1 %) |
| 2011 | Drama (18.3 %) | Action (15.4 %) | Comedy (12.4 %) |
| 2012 | Drama (18.0 %) | Action (13.5 %) | Comedy (11.2 %) |
| 2013 | Drama (16.8 %) | Action (13.3 %) | Comedy (11.4 %) |
| 2014 | Drama (18.2 %) | Action (15.8 %) | Adventure (13.4 %) |
| 2015 | Drama (18.9 %) | Action (14.6 %) | Adventure (13.4 %) |
| 2016 | Drama (18.1 %) | Action (15.2 %) | Adventure (11.0 %) |
| 2017 | Drama (19.1 %) | Action (15.6 %) | Adventure (10.5 %) |
| 2018 | Drama (16.6 %) | Action (14.8 %) | Adventure (13.1 %) |
| 2019 | Drama (20.5 %) | Action (11.7 %) | Comedy (11.4 %) |
| 2020 | Drama (20.1 %) | Comedy (12.6 %) | Action (12.1 %) |
| 2021 | Drama (17.7 %) | Action (16.2 %) | Adventure (12.9 %) |
| 2022 | Drama (18.6 %) | Action (16.0 %) | Comedy (11.9 %) |
| 2023 | Drama (18.7 %) | Action (13.8 %) | Comedy (12.4 %) |
| 2024 | Drama (18.1 %) | Action (13.8 %) | Comedy (11.0 %) |
| 2025 | Drama (15.0 %) | Action (13.8 %) | Comedy (10.3 %) |
<!-- AUTO:q2:end -->

### Q3. Top genres versus the rest

#### Results

<!-- AUTO:q3:start -->
"Top" = the 3 genres ranked first in the year (Q2); "rest" = the other genres of the year (about 18 per year). Weighted rating = Σ(rating × votes) / Σ(votes).

| Decade | Top-3 share of votes | Votes per film, top / rest | Weighted rating, top | Weighted rating, rest | Difference |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1980s | 46.3 % | 1.24 | 7.35 | 7.11 | +0.24 |
| 1990s | 47.4 % | 0.88 | 7.43 | 7.18 | +0.25 |
| 2000s | 41.7 % | 0.84 | 7.06 | 7.03 | +0.02 |
| 2010s | 44.2 % | 1.18 | 6.97 | 6.90 | +0.07 |
| 2020s | 44.5 % | 1.03 | 6.67 | 6.57 | +0.11 |

Stability of the top 3 over the 46 years:

| Genre | Years in top 3 | Years ranked 1st | Average share of votes |
| --- | ---: | ---: | ---: |
| Drama | 46 | 41 | 18.8 % |
| Comedy | 33 | 3 | 12.1 % |
| Action | 28 | 1 | 11.6 % |
| Adventure | 19 | 1 | 10.5 % |
| Crime | 9 (all in 1990–1999) | 0 | 7.8 % |
| Horror | 2 (1980–1981) | 0 | 4.6 % |
| Sci-Fi | 1 (1982) | 0 | 5.1 % |

The yearly gap in weighted rating ranges from −0.34 (2008) to +0.61 (1998).
<!-- AUTO:q3:end -->

### Q4. Directors with one highly rated film

#### Results

<!-- AUTO:q4:start -->
Exactly one movie rated ≥ 8.0 and at least 2 other movies averaging ≤ 6.0. Directors = `title.crew.directors` ∪ `title.principals` (director). **47 directors found.**

| Director | Hit film (year) | Rating | Votes | Other films | Their average |
| --- | --- | ---: | ---: | ---: | ---: |
| Harish Vyas | Om Ka Hari (2026) | 9.8 | 5,026 | 2 | 5.75 |
| Saurabh Varma | The Great Punjab Robbery (2026) | 9.3 | 1,760 | 2 | 5.90 |
| Irvin Kershner | Star Wars: Episode V - The Empire Strikes Back (1980) | 8.7 | 1,533,117 | 9 | 5.94 |
| David Leland | Concert for George (2003) | 8.6 | 2,330 | 4 | 5.85 |
| Harry Baweja | Chaar Sahibzaade 2: Rise of Banda Singh Bahadur (2016) | 8.6 | 1,051 | 6 | 5.30 |
| Christopher Ashley | Come from Away (2021) | 8.5 | 5,015 | 2 | 5.60 |
| Kamal Tabrizi | The Lizard (2004) | 8.4 | 24,813 | 4 | 5.53 |
| R. Madhesh | Mudhalvan (1999) | 8.4 | 9,594 | 3 | 5.87 |
| Sangeeth Sivan | Yoddha (1992) | 8.4 | 5,499 | 4 | 5.25 |
| Sateesh Paramveda | Seetha Kalyana Vaibhogame (2024) | 8.4 | 2,362 | 2 | 5.80 |
| Satish Paramvedha | Seetha Kalyana Vaibhogame (2024) | 8.4 | 2,362 | 2 | 5.80 |
| Ezhil | Thulladha Manamum Thullum (1999) | 8.3 | 7,363 | 2 | 4.55 |
| Carlos Bolado | Promises (2001) | 8.3 | 2,796 | 2 | 5.85 |
| M. Night Shyamalan | The Sixth Sense (1999) | 8.2 | 1,177,469 | 15 | 5.87 |
| Dharani | Ghilli (2004) | 8.2 | 19,436 | 5 | 5.44 |
| Nalan Kumarasamy | Soodhu Kavvum (2013) | 8.2 | 13,775 | 2 | 5.95 |
| P. Vasu | Aapthamitra (2004) | 8.2 | 1,464 | 5 | 5.24 |
| James McTeigue | V for Vendetta (2005) | 8.1 | 1,261,778 | 4 | 5.98 |
| Tate Taylor | The Help (2011) | 8.1 | 535,066 | 6 | 5.88 |
| Umesh Shukla | OMG: Oh My God! (2012) | 8.1 | 72,471 | 6 | 5.60 |
| Vikas Bahl | Queen (2013) | 8.1 | 72,021 | 6 | 5.83 |
| Mert Baykal | Pardon (2005) | 8.1 | 24,941 | 3 | 5.90 |
| Karthick Naren | Dhuruvangal Pathinaaru (2016) | 8.1 | 19,417 | 2 | 5.15 |
| Ravikanth Perepu | Kshanam (2016) | 8.1 | 6,712 | 2 | 5.95 |
| Ananth Mahadevan | Phule (2025) | 8.1 | 3,248 | 4 | 5.15 |
| Johny Antony | C.I.D. Moosa (2003) | 8.1 | 2,817 | 2 | 5.80 |
| Richard Kelly | Donnie Darko (2001) | 8.0 | 925,354 | 2 | 5.45 |
| Robert Rodriguez | Sin City (2005) | 8.0 | 825,724 | 22 | 5.94 |
| Frank Miller | Sin City (2005) | 8.0 | 825,724 | 2 | 5.65 |
| Martin Campbell | Casino Royale (2006) | 8.0 | 758,789 | 16 | 5.92 |
| Garth Davis | Lion (2016) | 8.0 | 270,305 | 2 | 5.65 |
| Wai Keung Lau | Infernal Affairs (2002) | 8.0 | 139,912 | 21 | 6.00 |
| Vincent Paronnaud | Persepolis (2007) | 8.0 | 107,510 | 3 | 5.70 |
| Billy Bob Thornton | Sling Blade (1996) | 8.0 | 105,234 | 3 | 5.93 |
| Predrag Antonijevic | Dara of Jasenovac (2020) | 8.0 | 82,508 | 5 | 5.70 |
| Ajay Bahl | Section 375 (2019) | 8.0 | 21,947 | 3 | 4.63 |
| J.P. Dutta | Border (1997) | 8.0 | 20,780 | 4 | 5.33 |
| Puri Jagannadh | Pokiri (2006) | 8.0 | 17,308 | 18 | 5.80 |
| Sinan Çetin | Abbas in Flower (1982) | 8.0 | 12,168 | 7 | 4.84 |
| Gunasekhar | Okkadu (2003) | 8.0 | 11,854 | 6 | 5.38 |
| Denis Sanders | Elvis: That's the Way It Is (1970) | 8.0 | 3,536 | 2 | 5.60 |
| Prince | Sign 'o' the Times (1987) | 8.0 | 3,058 | 2 | 4.90 |
| David Hogan | Sign 'o' the Times (1987) | 8.0 | 3,058 | 2 | 4.60 |
| Albert Magnoli | Sign 'o' the Times (1987) | 8.0 | 3,058 | 4 | 5.80 |
| Suseenthiran | Jeeva (2014) | 8.0 | 2,448 | 5 | 5.96 |
| Marcus Raboy | Conan O'Brien: The Kennedy Center Mark Twain Prize for American Humor (2025) | 8.0 | 1,584 | 2 | 5.45 |
| Ismael Rodríguez | Two Careful Fellows (1953) | 8.0 | 1,141 | 2 | 5.95 |
<!-- AUTO:q4:end -->

### Q5. Series with a decline in their final season

#### Results

<!-- AUTO:q5:start -->
Series with ≥ 3 seasons of ≥ 10 rated episodes (≥ 50 votes each); worst episode in the last season, best in seasons 1–2; ties in `all` mode. **1,364 candidate series → 171 selected.** The 10 series with the most rated episodes:

| Series | Years | Seasons | Rated episodes | Best (season) | Worst (season) |
| --- | --- | ---: | ---: | --- | --- |
| The Beverly Hillbillies | 1962–1971 | 9 | 274 | 8.8 (S2) | 5.8 (S9) |
| Coach | 1989–1997 | 9 | 199 | 9.1 (S2) | 6.7 (S9) |
| The Cosby Show | 1984–1992 | 8 | 197 | 8.5 (S2) | 5.4 (S8) |
| 24 | 2001–2010 | 8 | 192 | 9.3 (S1) | 7.6 (S8) |
| The Flash | 2014–2023 | 9 | 184 | 9.6 (S1) | 3.8 (S9) |
| Wings | 1990–1997 | 8 | 172 | 8.6 (S2) | 6.4 (S8) |
| Soy Luna | 2016–2026 | 4 | 160 | 9.1 (S2) | 2.8 (S4) |
| Talking Tom & Friends | 2014–2021 | 5 | 158 | 9.2 (S1) | 5.4 (S5) |
| NCIS: New Orleans | 2014–2021 | 7 | 155 | 8.4 (S2) | 6.5 (S7) |
| The Outer Limits | 1995–2002 | 7 | 152 | 8.4 (S2) | 5.2 (S7) |

Other well-known series in the list: *Weeds*, *Nip/Tuck*, *Chuck*, *Alias*, *True Blood*, *Sliders*.
<!-- AUTO:q5:end -->

### Q6. Actors successful across languages

#### Results

<!-- AUTO:q6:start -->
Success = rating ≥ 7.0 and ≥ 10,000 votes → **4,974 successful films**, of which 4,311 are used (593 multilingual and 70 with an unknown language are left out). Original language from Wikidata P364 for 98.43 % of the films, from `title.akas` for 0.16 %, unknown for 1.41 %.

Most frequent languages: English 2,802 · Hindi 271 · French 202 · Japanese 185 · Turkish 86 · Italian 80 · Tamil 79 · Spanish 78 · German 65 · Korean 59.

| Number of languages | People |
| ---: | ---: |
| 2 | 576 |
| 3 | 68 |
| 4 | 6 |
| **≥ 2** | **650** |
| **≥ 3** | **74** |

All people with 4 languages, and the 3-language people with the most successful films:

| Actor / actress | Languages | Successful films |
| --- | --- | ---: |
| Prakash Raj | Hindi, Kannada, Tamil, Telugu | 24 |
| Jackie Chan | Cantonese, English, Mandarin, Yue Chinese | 17 |
| Ashish Vidyarthi | Hindi, Malayalam, Tamil, Telugu | 7 |
| Bruno Ganz | English, German, Italian, Modern Greek | 6 |
| Sobhita Dhulipala | Hindi, Malayalam, Tamil, Telugu | 5 |
| Franco Nero | English, German, Italian, Spanish | 4 |
| Amitabh Bachchan | English, Hindi, Telugu | 26 |
| Nassar | Hindi, Tamil, Telugu | 21 |
| Max von Sydow | English, French, Swedish | 13 |
| Catherine Deneuve | English, French, Spanish | 11 |
| Sanjay Dutt | Hindi, Kannada, Tamil | 11 |
| Ron Perlman | English, French, "artistic language" | 10 |
| Madhavan | English, Hindi, Tamil | 10 |
| Fahadh Faasil | Malayalam, Tamil, Telugu | 10 |

The full lists (650 and 74 people) are in `outputs/exploration/q6_multilingual_actors*.csv`.
<!-- AUTO:q6:end -->

### Q7. Actors with an early career peak

#### Results

<!-- AUTO:q7:start -->
Careers of ≥ 20 years with ≥ 15 rated films → **3,528 people**. Early peak = best film in the first third of the career **and** first-half average > second-half average → **1,557 people (44 %)**.

| Group | People | Avg career (years) | Avg films | 1st half − 2nd half | Avg slope (pts/year) | Negative slope |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Early peak | 1,557 | 35.2 | 27.2 | +0.66 | −0.04 | 96.9 % |
| Others | 1,971 | 33.7 | 28.4 | +0.18 | −0.01 | 67.4 % |

Examples of early-peak careers (large gap between the two halves):

| Actor / actress | Career | Films | Peak film (year) | Peak rating | 1st half avg | 2nd half avg |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| Halit Akçatepe | 1972–2005 | 24 | The Chaos Class (1975) | 9.1 | 7.63 | 3.45 |
| Wendell Corey | 1947–1968 | 22 | Rear Window (1954) | 8.4 | 7.01 | 3.65 |
| Cüneyt Arkın | 1964–2014 | 18 | The Mine (1978) | 7.5 | 6.34 | 3.50 |
| Evelyn Keyes | 1939–1989 | 17 | Gone with the Wind (1939) | 8.2 | 6.97 | 4.15 |
| Madhan Bob | 1992–2021 | 16 | Thevar Magan (1992) | 8.6 | 7.52 | 4.83 |
| James Duval | 1993–2024 | 22 | Donnie Darko (2001) | 8.0 | 6.11 | 3.79 |
| Corey Feldman | 1984–2021 | 15 | Stand by Me (1986) | 8.1 | 6.26 | 4.05 |
| Edward Furlong | 1991–2015 | 30 | Terminator 2: Judgment Day (1991) | 8.6 | 6.55 | 4.65 |
<!-- AUTO:q7:end -->

### Q8. Professionals with multiple roles

#### Results

<!-- AUTO:q8:start -->
Multi-talented = at least 2 roles among {director, writer, actor}, with ≥ 3 films in each → **3,653 people**. 2,734 of them have both multi-role and single-role films and can be compared.

| Roles over the career | People |
| --- | ---: |
| director + writer | 2,669 |
| actor + director + writer | 440 |
| actor + writer | 392 |
| actor + director | 152 |

Paired comparison (per person: mean rating of multi-role films − mean rating of single-role films):

| Roles on the same film | People | Multi-role films | Rating, multi-role | Rating, single role | Mean diff | Median diff | Better when combining |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Any combination | 2,734 | 14,226 | 6.29 | 6.17 | +0.11 | +0.12 | 57.6 % |
| director + writer | 2,296 | 11,272 | 6.31 | 6.20 | +0.12 | +0.12 | 57.4 % |
| actor + writer | 468 | 1,323 | 6.16 | 6.05 | +0.11 | +0.13 | 57.3 % |
| actor + director + writer | 540 | 1,299 | 6.20 | 6.13 | +0.07 | +0.10 | 53.9 % |
| actor + director | 169 | 332 | 6.15 | 6.21 | −0.06 | +0.06 | 55.0 % |

Selected people among those with the most multi-role films:

| Name | Roles | Multi-role films (avg) | Single-role films (avg) | Diff |
| --- | --- | --- | --- | ---: |
| Woody Allen | actor + director + writer | 54 (6.89) | 7 (5.87) | +1.02 |
| Werner Herzog | actor + director + writer | 41 (7.11) | 6 (6.47) | +0.64 |
| Claude Chabrol | actor + director + writer | 37 (6.82) | 8 (6.75) | +0.07 |
| Ingmar Bergman | actor + director + writer | 36 (7.33) | 6 (7.20) | +0.13 |
| Jean-Luc Godard | actor + director + writer | 35 (6.65) | 5 (6.22) | +0.43 |
| Tyler Perry | actor + director + writer | 35 (5.36) | 7 (6.43) | −1.07 |
| Akira Kurosawa | director + writer | 31 (7.54) | 10 (6.96) | +0.58 |
| Satyajit Ray | director + writer | 28 (7.93) | 6 (7.05) | +0.88 |
| Clint Eastwood | actor + director | 26 (6.89) | 40 (6.90) | −0.01 |
| Sylvester Stallone | actor + director + writer | 25 (6.32) | 38 (5.61) | +0.71 |
<!-- AUTO:q8:end -->

### Methodological Explanation

#### Methodology and why it was chosen

All eight questions read the silver tables and share the conventions above, defined in `conf/settings.yaml` and `exploration/base.py`. The 40-minute threshold is the usual definition of a feature film. Below 1,000 votes, a handful of users can give a movie almost any score. Popularity means the number of votes. Each question writes a Markdown summary, with its parameters at the top, and a CSV containing the full results.

**Q1.** We use two methods because runtimes are very skewed. A few extremely long documentaries push the standard deviation of Documentary to 223 minutes, which makes the z-score threshold so wide that it catches almost nothing. The IQR fences rely on quartiles and are not affected by those extremes. We keep the union and record which method fired.

**Q2.** Votes measure audience. A count of movies would measure production, and an average rating says nothing about how many people watched. We also keep the number of movies and the vote-weighted rating of each genre, to see whether a genre is popular because it has many movies or a few very-watched ones.

**Q3.** For each year, we compare the top 3 genres with all other genres combined (share of votes, votes per film, weighted rating), then aggregate by decade and count how many years each genre spends in the top 3.

**Q4.** Each director source misses some credits, so we take the union of both. We read "multiple other movies" as "at least two".

**Q5.** The last season is identified *before* the vote filter. Otherwise, a recent season with few votes would disappear, and the season before it would wrongly be treated as the last one. In `all` mode, when several episodes share the worst or best rating, all of them must sit in the expected seasons.

**Q6.** The original language comes from Wikidata (P364, found through the IMDb ID, P345), with `title.akas` as a fallback. `title.akas` lists release titles by *region*, and a region is not a language: an Indian film has region `IN` whether it is in Hindi, Tamil or Telugu. Multilingual movies are excluded so that a single film cannot add two languages to an actor's count.

**Q7.** Requiring both conditions (peak in the first third *and* a better first half) avoids calling a career "early peak" because of one lucky early hit. We also compute the slope of rating against year (`covar_samp / var_samp`) as a continuous measure.

**Q8.** The comparison is done *per person*, so each person is their own control. Comparing all multi-role movies with all single-role movies would mostly compare different people.

#### Alternatives considered and trade-offs

- **Thresholds.** `min_votes = 1,000` trades coverage for reliability. A threshold of 10,000 would remove most older and non-English movies. With 100, obscure titles rated 9+ would dominate, and even at 1,000 this still happens in Q4 with very recent films. We considered a Bayesian weighted rating, which pulls low-vote ratings toward the mean, but it adds a parameter and makes the results harder to explain.
- **Q1.** We could have used only the z-score (simple, but unreliable on skewed genres), only the IQR, or a robust z-score based on the median absolute deviation. We kept the two standard methods side by side.
- **Q2/Q3.** We could have measured popularity by number of movies or by average rating. Votes favour recent movies, because IMDb users vote more for what they watch now. We accepted this bias because the question is about popularity.
- **Q6.** Using `title.akas` alone would have avoided an external source, but it confuses region and language. Wikidata adds a dependency and gives the language of 98.4 % of the movies.
- **Q7.** We could have used only one of the two measures. The slope is affected by the general decline of ratings over careers. The halves-and-third rule is closer to the wording of the question.
- **Q8.** A regression with one fixed effect per person would test the same idea and give a confidence interval. We kept the simpler paired comparison.

### Key takeaways

- **Drama dominates.** It ranks first in 41 of the 46 years and appears in the top 3 every year, with 15–33 % of the votes. Part of this is mechanical: Drama is the most common tag (196,130 of the 456,414 feature films), and with exploded genres, every "drama + something" movie adds its votes to Drama.
- **The top 3 genres take 42–47 % of all votes** and are slightly better rated than the rest (+0.02 to +0.25 depending on the decade), so more than half of the audience goes to the ~18 other genres. Their lead comes partly from volume: in the 1990s and 2000s, top-3 films actually get fewer votes per film than the rest (ratio 0.88 and 0.84).
- **Runtime outliers are mostly long movies** (30,234 against 5,323), and the count depends heavily on the method. The most extreme cases are experimental works such as *Logistics* (51,420 minutes), not mainstream films.
- **Rating-based results are sensitive to vote counts.** The first two directors in Q4 owe their place to 2026 films rated 9.8 and 9.3 with only 5,026 and 1,760 votes; such early ratings will probably drop. Irvin Kershner is the textbook case (*The Empire Strikes Back*, 8.7 with 1.5 M votes, against 5.94 for his 9 other films). Sateesh Paramveda and Satish Paramvedha look like the same person under two IMDb IDs, a duplicate our key checks cannot see.
- **171 of 1,364 eligible series (12.5 %)** have their worst episode in the last season and their best in the first two, with *The Flash* as the sharpest case (9.6 in season 1, 3.8 in season 9).
- **650 people succeeded in ≥ 2 languages and 74 in ≥ 3.** Indian cinema produces many multilingual careers (Prakash Raj: 4 languages). Language labels are noisy, though: Wikidata separates Cantonese and Yue Chinese (Jackie Chan, Maggie Cheung), tags *Red Cliff II* as German and *Quest for Fire* as an "artistic language", so a few counts are one too high.
- **44 % of long careers peak early**, but even among the others, two thirds have a negative slope. Ratings tend to decline over a career in general, probably because the old films still rated today are the ones remembered for being good, and because actors take smaller roles later on.
- **Combining roles goes with a small gain**: +0.12 in median, and 57.6 % of people are rated higher when they combine roles. The effect is small next to the spread between people (standard deviation 0.78), but with 2,734 people the mean difference is about 7 standard errors above zero. Individual cases go both ways (Woody Allen +1.02, Tyler Perry −1.07). The gain probably reflects selection: people write and direct their personal projects.

## 3. Data Enrichment

### Results

<!-- AUTO:enrichment:start -->
#### Scope

Feature films 1980–2025, top 10 per (genre, year) ranked by votes then rating; first 3 principals per film among actor, actress, director, writer (IMDb `ordering`).

| Counter | Value |
| --- | ---: |
| (genre, year) groups | 1,027 |
| (film, genre, year) selections | 9,832 |
| **Distinct films** | **6,821** |
| **Distinct people** | **9,759** |
| Films with 3 selected principals | 6,319 |

#### Coverage

Text from English Wikipedia (CC BY-SA 4.0); identifiers and facts from Wikidata (CC0).

| Film status | Films | % |
| --- | ---: | ---: |
| ok | 5,908 | 86.6 % |
| not_found (no English page) | 492 | 7.2 % |
| no_plot_section (lead section used) | 365 | 5.4 % |
| partial | 56 | 0.8 % |

| Decade | Films | With a synopsis |
| --- | ---: | ---: |
| 1980s | 1,403 | 92.8 % |
| 1990s | 1,433 | 94.9 % |
| 2000s | 1,443 | 95.1 % |
| 2010s | 1,595 | 91.2 % |
| 2020s | 947 | 88.7 % |

- Synopsis length: median 3,605 characters from a plot section (5,964 films), 483 from a lead section (365 films).
- Section used: Plot 5,570, Synopsis 263, Summary 57, Premise 43, Plot summary 24, other 7.
- People: ok 7,184 (73.6 %), not_found 1,485 (15.2 %), partial 1,090 (11.2 %). Available: biography 7,525, birth date 8,084, birth place 7,826, citizenship 8,066, death date 1,427.
- 5,049 films have a biography for all 3 principals.

#### Collection

Sequential requests, ≤ 1 request/s, `maxlag=5`, up to 6 retries, identified User-Agent, disk cache.

| Step | Requests | Retries | HTTP 429 | Failed | Duration (s) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Film pages (Wikipedia) | 6,334 | 4 | 0 | 0 | 6,602 |
| Film sitelinks (Wikidata) | 35 | 0 | 0 | 0 | 131 |
| Person sitelinks (Wikidata) | 53 | 4 | 2 | 0 | 373 |
| Person facts (Wikidata) | 51 | 2 | 1 | 0 | 334 |
| Person intros (Wikipedia) | 377 | 0 | 0 | 0 | 392 |
| **Total** | **6,850** | **10** | **3** | **0** | **7,832 (≈ 2 h 10)** |

`robots.txt` verdict (policy `report`): `en.wikipedia.org/w/api.php` and `query.wikidata.org/sparql` both disallowed for generic user agents.

#### Lineage examples

| tconst | Title | Status | Source | Note |
| --- | --- | --- | --- | --- |
| tt0111161 | The Shawshank Redemption | ok | https://en.wikipedia.org/w/index.php?oldid=1384720571 | |
| tt14992922 | The Tinder Swindler | no_plot_section | https://en.wikipedia.org/wiki/The_Tinder_Swindler | No section among (Plot, Synopsis, …) in Wikipedia page 'The Tinder Swindler'; lead section used instead |
| tt0892255 | Che: Part One | not_found | https://www.wikidata.org/wiki/Q860425 | No enwiki sitelink for Q860425 (P345=tt0892255) |

Each record also carries `source_name`, `source_revision_id`, `retrieved_at` and `license`.
<!-- AUTO:enrichment:end -->

### Methodological Explanation

#### Methodology and why it was chosen

- **Scope (Spark).** The scope depends only on parameters: with `top_n: null` and `year_min: null`, the same code processes the whole dataset. The HTTP layer works in batches and resumes from its cache, so a larger scope changes the run time, not the code.
- **Source.** We use a single source, as the instructions allow, because Wikipedia covers these films well and its text is written by people. Wikidata serves only to map IMDb IDs to Wikipedia pages and to retrieve structured facts about people.
- **Matching by ID, not by title.** We run Wikidata SPARQL queries in batches (`VALUES ?imdb {…}` on P345). An exact ID match avoids homonyms such as *Crash* or *It*, which a title search would confuse.
- **Text.** We use the MediaWiki API. For films, we take the Plot section (or Synopsis, Premise, Summary, …); if there is none, we take the lead section and set the status to `no_plot_section`. For people, we take the introduction (`exintro`, `explaintext`), in batches of 20. We store the `revid`, so each record links to the exact revision we read.
- **Collection (Python, outside Spark, as allowed).** A single-threaded client sends at most 1 request per second, with `maxlag=5`. It honours `Retry-After` on 429/503 responses, with exponential backoff. It identifies itself with a User-Agent that includes a contact email. Every raw response is cached on disk, so an interrupted run resumes without sending any request twice.
- **Everything else in Spark.** Spark reads the JSON cache with an enforced schema and cleans the text: trimming, collapsing whitespace, removing `[1]`-style reference markers, and applying a minimum length of 200 characters for a synopsis and 100 for a biography. It then joins the result to silver and writes `data/gold/enriched_films/` and `enriched_people/`.
- **Lineage.** When information is missing, `enrichment_note` is built by code from a fixed template (see the examples above). It states the status and contains no generated content about the film.

**No machine-generated text.** Every text we keep was written by Wikipedia editors. We deliberately ignore Wikidata descriptions. They are very short ("2010 film by …"), and many were created by bots, so we cannot guarantee that a person wrote them.

**Rate limits and `robots.txt`.** Our `robots.txt` policy is set to `report`: the verdict is logged in the output, but it does not block the run. Our view is that `robots.txt` targets crawlers that follow links across a site. Wikimedia publishes separate rules for API clients (User-Agent policy and API etiquette: serial requests, `maxlag`, identification), and those are the rules we followed. We also fetch a fixed list of pages instead of crawling. We prefer to state this openly rather than hide it.

#### Alternatives considered and trade-offs

- **Scraping the HTML pages**: more fragile (it breaks when the layout changes), heavier on Wikimedia's servers, and closer to what `robots.txt` forbids. The API returns clean text and revision IDs.
- **Wikipedia dumps**: no rate-limit concerns, and the best option for the full IMDb scale. However, downloading and parsing tens of GB for about 16,000 pages was out of proportion for our scope.
- **TMDb / OMDb**: good synopsis coverage, but they need API keys, their terms restrict reuse, and their text is not under an open licence.
- **Other Wikipedia languages as a fallback**: better coverage for non-English films, but the output would mix languages, and the instructions do not require a second source.
- **Parallel requests**: much faster than our ~2 h 10 min of collection, but incompatible with the 1 request per second etiquette. We accepted the slower run.

### Key takeaways

- **86.6 % of films got a full synopsis** from a plot-like section. A plot section is far richer than an introduction (median of 3,605 characters against 483), so the introduction is a fallback, not an equivalent. Films without a plot section are mostly documentaries (*Man on Wire*, *March of the Penguins*), whose articles naturally have no Plot heading.
- **People are harder to cover** (73.6 % `ok`): less-known principals often have no article.
- **Coverage depends on the decade**, from 95.1 % in the 2000s down to 88.7 % in the 2020s. Recent films are less likely to have a page or a written plot yet.
- **The polite collection worked**: 6,850 requests and 0 failures. The 10 retries (3 HTTP 429, 1 HTTP 5xx, 6 network errors) all succeeded, and thanks to the cache, the interruption when the machine went to sleep overnight had no effect.

## 4. Streaming

### Results

<!-- AUTO:streaming:start -->
#### Lookup table

The 30,000 most-voted titles and 20,000 people, linked to their Wikipedia pages through Wikidata (P345 + sitelinks): **88,273 pages** (enwiki 48,825, frwiki 39,448).

| Entity type | IMDb identifiers | With a page | % |
| --- | ---: | ---: | ---: |
| film | 25,450 | 24,326 | 95.6 % |
| person | 25,192 | 19,622 | 77.9 % |
| tv_series | 5,973 | 5,437 | 91.0 % |

#### Run summary

| Parameter | Value |
| --- | --- |
| Duration | 1,237 s (≈ 20.6 min), 14 Nov 2026, ~14:50–15:11 UTC |
| Watermark | 10 minutes |
| Windows | tumbling 5 min; sliding 10 min, slide 5 min |
| Output mode | append (finalized windows only) |
| Input rate | 1.0–2.6 events/s |
| Trigger duration | 5–7 s (window queries), 10–20 s (matched events) |

| Query | Batches | Input rows | Rows dropped by watermark |
| --- | ---: | ---: | ---: |
| matched_events | 117 | 2,113 | 5 |
| tumbling | 120 | 2,055 | 5 |
| sliding | 120 | 2,055 | 5 |

#### Relevant edits

**72 relevant events** (67 real + 5 injected): enwiki 50 (13 by bots), frwiki 22 (1 by a bot).

| Entity type | Lookup only | Title pattern only | Both | Total | Bots |
| --- | ---: | ---: | ---: | ---: | ---: |
| film | 9 | 16 | 7 | 32 | 7 |
| person | 17 | 3 | 0 | 20 | 0 |
| tv_series | 8 | 7 | 5 | 20 | 7 |
| **Total** | **34** | **26** | **12** | **72** | **14** |

Most edited pages: *Christophe Colomb (film, 1949)* (frwiki, 4), *Slow Horses* (3), then *Beautiful Boy (2018 film)*, *Tangled: Before Ever After*, *Ti West*, *Drew Barrymore* and *Jacqueline Bisset* (2 each).

#### Finalized windows

| Window | Type | Relevant edits |
| --- | --- | ---: |
| 14:50–14:55 | tumbling | 11 |
| 14:55–15:00 | tumbling | 23 |
| 14:45–14:55 | sliding | 11 |
| 14:50–15:00 | sliding | 34 |

#### Late-data injection

| Injected delay | Events | Event time (UTC) | In the matched sink |
| --- | ---: | --- | ---: |
| 5 minutes | 5 | 14:58:19 | 5 / 5 |
| 30 minutes | 5 | 14:33:19 | 0 / 5 (dropped by the watermark) |

Per-batch metrics (`numInputRows`, rates, durations, watermark, dropped rows) are in `outputs/streaming/progress.jsonl`.
<!-- AUTO:streaming:end -->

### Methodological Explanation

#### Methodology and why it was chosen

The pipeline is: Wikimedia EventStreams (`recentchange`, SSE) → Python producer → Kafka topic `wikistreams` → Spark Structured Streaming → Parquet + console.

- **Producer.** It reads the SSE stream and keeps only `enwiki`/`frwiki` events of type `edit`/`new` in namespace 0 (articles). It publishes the raw JSON to Kafka, with `meta.id` as the key. After a disconnection, it resumes with `Last-Event-ID`, so no events are skipped. The cost is that a few events may be sent twice, which the dedup step handles downstream.
- **Lookup table.** Before the stream starts, a Spark batch job builds `data/gold/wiki_lookup/` (normalised page title, IMDb ID, entity type). The table is small enough to be broadcast.
- **Relevance.** An event is relevant if its (wiki, normalised title) is in the lookup **or** if its title matches a pattern such as "(film)", "(TV series)", "(actor)" or "(série télévisée)". The `match_reason` column records which rule fired. The lookup links an edit to an exact IMDb ID; the patterns catch pages outside the lookup, such as less-voted titles or new pages.
- **Streaming job.** Spark reads Kafka with an explicit JSON schema and uses `meta.dt` (the time of the edit on Wikipedia) as event time. It applies a 10-minute watermark and `dropDuplicatesWithinWatermark(event_id)`. Three independent queries run, each with its own checkpoint: relevant events to Parquet, 5-minute tumbling windows, and 10-minute sliding windows with a 5-minute slide. The window queries count events per wiki, entity type, bot/human and page, and compute the average size change. They write in append mode through `foreachBatch`, to Parquet and to the console.
- **Metrics.** A `StreamingQueryListener` writes every progress event to `outputs/streaming/progress.jsonl`.

**Why Kafka.** Kafka decouples the source from Spark. Spark has no native SSE source and cannot replay the Wikimedia stream itself. With Kafka in between, events wait in the topic if Spark restarts, and Spark resumes from the offsets saved in its checkpoint. Several queries can also read the same topic independently.

**Why two window types.** Tumbling windows do not overlap, so their counts add up to the total, which is convenient for reporting. Sliding windows count each event twice and give a smoother trend, which shows bursts that straddle a window boundary.

#### Alternatives considered and trade-offs

- **Reading the SSE stream directly from Spark** (custom source or socket): no replay and no buffer, and Spark would depend on the availability of the source.
- **Patterns only**: no lookup to build (about 17 minutes on the first run), but they miss pages whose title gives no hint, such as *Slow Horses* or *John Steinbeck*. **Lookup only** misses films outside the top 30,000. Each rule found events the other missed (34 / 26 / 12).
- **Matching against the full IMDb title list**: far larger, and full of false positives, because common words ("Home", "Love") are also IMDb titles.
- **`update` or `complete` output mode**: earlier results, but windows get rewritten, which does not fit an append-only Parquet sink, and `complete` keeps all the state forever.
- **Processing-time windows**: no late-data problem, but the counts would reflect when Spark processed events, not when the edits happened.

### Late-arriving data

Events can arrive late for several reasons: a reconnection of the producer, lag in Kafka, or Spark restarting and reading a backlog. We work in **event time** (`meta.dt`) and use a **10-minute watermark**. Spark tracks the latest event time it has seen and assumes that no event older than that time minus 10 minutes will still arrive. In practice:

- an event up to 10 minutes late is still counted in its correct window;
- an older event is dropped by the stateful operators (window aggregation and dedup) and counted in `numRowsDroppedByWatermark`;
- in append mode, a window is written only once the watermark has passed its end. A 5-minute window is therefore final about 10 minutes after it closes, and it is never rewritten;
- state older than the watermark (old windows, seen IDs) is purged, so memory stays bounded however long the stream runs.

**Why 10 minutes.** The `recentchange` stream is close to real time, and normal delays are a few seconds. Ten minutes covers a producer reconnection or a short Spark restart, while keeping the delay before results acceptable in a 20-minute run and the state small. A larger watermark gives more complete counts, but later results and more state; a smaller one gives faster results, but drops more events.

**Deduplication.** `dropDuplicatesWithinWatermark(event_id)` removes duplicates caused by the `Last-Event-ID` replay or by producer retries (Kafka is at-least-once here). Because it is bounded by the watermark, the set of seen IDs does not grow forever, whereas a plain `dropDuplicates` on `event_id` would have to remember every ID.

**Experiment.** After 12 minutes, an injector republished 10 real events with new IDs, so that the dedup would not remove them: 5 with `meta.dt` moved back by 5 minutes, and 5 moved back by 30 minutes. As the results show, the first five (event time 14:58:19) were still above the watermark and reached the sink; the other five (14:33:19) were below it and were dropped, in each of the three queries.

The cost of the watermark is also visible: when the job stopped, the watermark was about 10 minutes behind the latest event, so only the windows ending at 14:55 and 15:00 UTC were finalized. Edits from the last ten minutes of the run were still sitting in open windows.

The limit of this method is that dropped events are lost from the aggregates and only counted. If they mattered, we could compare their event time with the current watermark in `foreachBatch`, send them to a separate sink, and reconcile them later in batch.

### Key takeaways

- About 3.4 % of the filtered edits were relevant (72 out of 2,113 in 20 minutes), well above "multiple matches" for the test window.
- The lookup and the patterns are complementary. People are found almost only through the lookup (17 of 20), because their page titles rarely carry a hint like "(actor)". Bot edits, in contrast, were mostly caught by the patterns (10 of 14).
- enwiki brings more than twice as many relevant edits as frwiki (50 against 22), and almost all bot edits (13 of 14).
- The input rate is low (1–2.6 events/s) and triggers take a few seconds: the bottleneck is the source, not Spark, so a single local container is enough.
- The injection experiment confirms that the watermark accepts events that are slightly late and drops events that are too late, as designed.

## 5. Open Question

### Question and motivation

**Do repeated director–actor collaborations produce better-rated films than the first one?**

Many directors work with the same actors again and again: Kurosawa with Toshirō Mifune and Takashi Shimura, Ozu with Chishū Ryū, Bergman with Gunnar Björnstrand. Two stories are possible. Either familiarity improves the work, or a director brings an actor back after a success and the following films do not live up to it. IMDb lets us test this on tens of thousands of pairs. The question needs joins between four tables and window functions per pair, which makes it a non-trivial Spark problem.

### Data

IMDb only, with no external data:

- `title.basics` and `title.ratings`: the same 49,434 rated feature films as the exploration (≥ 1,000 votes);
- `title.crew` and `title.principals` for directors, using the same union as Q4;
- `title.principals` for actors and actresses;
- `name.basics` for names.

This gives 507,560 (director, actor, film) rows. Films where the director also acts are excluded from the pairs, because directing yourself is not a collaboration.

### Results

<!-- AUTO:open_question:start -->
| Metric | Value |
| --- | ---: |
| Director–actor pairs (≥ 1 film) | 469,141 |
| Recurring pairs (≥ 2 films) | **26,630** (5.7 %) |
| Mean rating, films of one-off pairs | 6.13 |
| Mean rating, first film of recurring pairs | **6.61** |
| Mean rating of the follow-up films | 6.33 |
| Mean delta (follow-ups − first) | **−0.28** (median −0.20, std 0.85) |
| Paired t statistic | −53.7 |
| Pairs whose follow-ups are better / equal / worse | 32.9 % / 6.3 % / 60.8 % |
| Mean excess vs the director's films without that actor | **+0.12** (57.1 % positive, 21,573 pairs) |

By collaboration rank:

| Rank | Films | Mean rating | Gap with the 1st film |
| --- | ---: | ---: | ---: |
| 1 | 26,630 | 6.61 | 0.00 |
| 2 | 26,630 | 6.36 | −0.24 |
| 3 | 6,587 | 6.40 | −0.35 |
| 4 | 2,431 | 6.44 | −0.37 |
| 5+ | 2,771 | 6.42 | −0.40 |

By number of collaborations:

| Films together | Pairs | First film | Follow-ups | Delta | Excess vs director |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2 | 20,043 | 6.56 | 6.28 | −0.28 | +0.10 |
| 3 | 4,156 | 6.71 | 6.43 | −0.28 | +0.15 |
| 4–5 | 1,850 | 6.79 | 6.48 | −0.31 | +0.17 |
| 6+ | 581 | 6.85 | 6.60 | −0.25 | +0.22 |

Most frequent pairs:

| Director | Actor | Films | Years | First film (rating) | Follow-ups | Delta | Excess |
| --- | --- | ---: | --- | --- | ---: | ---: | ---: |
| Kartal Tibet | Kemal Sunal | 26 | 1976–1990 | Tosun Pasha (8.8) | 6.83 | −1.97 | +1.43 |
| Gerald Thomas | Joan Sims | 25 | 1959–1978 | Carry on Nurse (6.2) | 6.03 | −0.17 | +0.31 |
| Gerald Thomas | Kenneth Williams | 25 | 1958–1978 | Carry on Sergeant (6.3) | 6.12 | −0.18 | +0.63 |
| Gerald Thomas | Charles Hawtrey | 23 | 1958–1972 | Carry on Sergeant (6.3) | 6.29 | −0.01 | +1.08 |
| Gerald Thomas | Sidney James | 21 | 1960–1974 | Carry on Constable (6.2) | 6.27 | +0.07 | +1.12 |
| Yasujirō Ozu | Chishū Ryū | 20 | 1930–1962 | That Night's Wife (6.9) | 7.69 | +0.79 | +0.36 |
| Johnnie To | Suet Lam | 20 | 1998–2016 | Expect the Unexpected (7.0) | 6.76 | −0.24 | +0.10 |
| Akira Kurosawa | Takashi Shimura | 19 | 1943–1963 | Sanshiro Sugata (6.7) | 7.62 | +0.92 | +0.13 |
| Ingmar Bergman | Gunnar Björnstrand | 16 | 1946–1978 | It Rains on Our Love (6.6) | 7.58 | +0.98 | +0.43 |
| Akira Kurosawa | Toshirō Mifune | 16 | 1948–1965 | Drunken Angel (7.6) | 7.83 | +0.23 | +0.09 |
<!-- AUTO:open_question:end -->

### Key takeaways

- **Collaborations rarely repeat**: only 5.7 % of pairs worked together on at least two films.
- **The first film of a recurring pair is already rated well above average** (6.61 against 6.13 for one-off pairs). A success makes a new collaboration more likely.
- **Follow-up films are rated lower than the first**: −0.28 on average, and 60.8 % of pairs decline. The gap stays between −0.24 and −0.40 at every rank.
- **However, the pair still does better than the director's other work**: +0.12 above the films the same director made, over the same period, without that actor. This excess grows with the number of collaborations (+0.10 for 2 films, +0.22 for 6 or more), while the delta stays around −0.28.
- **Kartal Tibet and Kemal Sunal show both effects at once**: their first film, *Tosun Pasha* (8.8), was never matched (delta −1.97), but their 25 other films are still rated 1.43 points above Tibet's work without Sunal.
- **How we read it.** The decline relative to the first film looks like regression to the mean: pairs are selected on a good first film, so the next films fall back toward the director's usual level. The general decline of ratings over careers (Q7) adds to this. The positive excess suggests that working again with the same actor goes with slightly better films than the director's other work. Familiarity seems to help a little, but it does not repeat the first success.
- **This is correlation, not causation.** Directors may cast their regular actors in their more personal or better-funded projects.

### Methodological Explanation

#### Methodology and why it was chosen

- **Pairs.** We join director credits and actor credits on the same `tconst`, excluding cases where the director and the actor are the same person.
- **Order.** A Spark window partitioned by pair and ordered by year (then `tconst` for ties) numbers the films of each pair.
- **Delta.** For each recurring pair, the delta is the average rating of the follow-up films minus the rating of the first film. Averaging the follow-ups gives each pair exactly one value, so a pair with 26 films does not weigh more than a pair with two.
- **Excess.** The excess is the average rating of the follow-ups minus the average rating of the director's films *without* that actor, released after the pair's first film. This baseline controls for the director's general level and for the period.
- **Statistics.** We compute a paired t statistic on the delta, and use a tolerance of 0.05 to classify each pair as better, equal or worse. We also build profiles by collaboration rank and by number of collaborations.

We chose this design because it is simple to explain and each pair serves as its own control. We added the director baseline after seeing that the negative delta could be explained by selection alone.

#### Alternatives considered and trade-offs

- **Comparing all films of recurring pairs with all films of one-off pairs**: easy, but it mixes first films and follow-ups, and selection drives the result (6.61 against 6.13 before any follow-up is made).
- **A regression with director, actor and year effects**: it would separate the effects better and give proper confidence intervals, but it is heavier to build in Spark and harder to explain. We kept paired comparisons.
- **Matching each follow-up with a film the same director made in the same year**: a closer control, but many directors do not make a film every year, so far fewer pairs would remain.
- **Weighting by number of votes**: famous pairs would dominate the result. We gave every pair the same weight.
- **External data (budgets, box office)**: would help control for the size of the project, but we found no open, human-written source with good coverage, and budgets in Wikipedia infoboxes are patchy.

One limit of our approach is that the t statistic assumes the pairs are independent. Pairs that share a director or an actor are not independent, so t = −53.7 overstates how certain the result is. The sign and the size of the effect remain informative.
