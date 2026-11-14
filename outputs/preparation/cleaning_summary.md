# Cleaning summary (bronze to silver)

## Parameters

| parameter | value |
| --- | --- |
| reference_year | 2026 |
| quarantine_rules | DQ05:nconst, DQ05:parentTconst, DQ05:tconst, DQ05:titleId, DQ10, DQ15, DQ16 |
| duplicate_handling | identical rows sharing a primary key: one copy kept, others quarantined; conflicting rows: all quarantined |
| foreign_keys_checked_against | silver parent tables |
| silver_path | data/silver |
| quarantine_path | data/quarantine |

## Rows before and after cleaning

| table | bronze_rows | silver_rows | quarantined_rows | pct_quarantined | silver_rows_with_flags | pct_silver_rows_with_flags |
| --- | --- | --- | --- | --- | --- | --- |
| name_basics | 15811387 | 15811387 | 0 | 0.0000 | 36 | 0.0002 |
| title_akas | 60385482 | 60385482 | 0 | 0.0000 | 0 | 0.0000 |
| title_basics | 12958477 | 12958477 | 0 | 0.0000 | 449 | 0.0035 |
| title_crew | 12958477 | 12958477 | 0 | 0.0000 | 1033 | 0.0080 |
| title_episode | 10030795 | 10030790 | 5 | 0.0000 | 7125 | 0.0710 |
| title_principals | 102738762 | 102730499 | 8263 | 0.0080 | 24901 | 0.0242 |
| title_ratings | 1731756 | 1731756 | 0 | 0.0000 | 0 | 0.0000 |

## Quarantined rows per reason

| table | dq_reason | rows |
| --- | --- | --- |
| title_episode | DQ05:parentTconst | 5 |
| title_principals | DQ05:nconst | 8263 |

## Silver rows per quality flag

| table | dq_flag | rows |
| --- | --- | --- |
| name_basics | DQ01 | 28 |
| name_basics | DQ02 | 2 |
| name_basics | DQ05:knownForTitles | 6 |
| title_basics | DQ07 | 3 |
| title_basics | DQ08 | 446 |
| title_crew | DQ05:directors | 419 |
| title_crew | DQ05:writers | 812 |
| title_episode | DQ14 | 7125 |
| title_principals | DQ03 | 23742 |
| title_principals | DQ04 | 1159 |

## Deterministic corrections

| table | column | correction | values_set_to_null |
| --- | --- | --- | --- |
| name_basics | birthYear | birthYear after the reference year set to null | 0 |
| name_basics | deathYear | deathYear after the reference year set to null | 0 |
| title_basics | runtimeMinutes | runtimeMinutes <= 0 set to null | 4 |
| title_episode | episodeNumber | negative episodeNumber set to null | 0 |
| title_episode | seasonNumber | negative seasonNumber set to null | 0 |
| title_ratings | averageRating | averageRating outside [rating_min, rating_max] set to null | 0 |
| title_ratings | numVotes | numVotes <= 0 set to null | 0 |
