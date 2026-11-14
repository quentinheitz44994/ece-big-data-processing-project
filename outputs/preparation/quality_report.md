# Data quality report

## Parameters

| parameter | value |
| --- | --- |
| reference_year | 2026 |
| max_age_years | 120 |
| posthumous_grace_years | 5 |
| posthumous_exempt_categories | archive_footage, archive_sound, writer, composer |
| archive_pattern | (?i)archive |
| max_future_years | 5 |
| max_runtime_minutes | 1000 |
| rating_min | 1 |
| rating_max | 10 |
| episode_parent_types | tvSeries, tvMiniSeries |
| known_genres | Action, Adult, Adventure, Animation, Biography, Comedy, Crime, Documentary, Drama, Family, Fantasy, Film-Noir, Game-Show, History, Horror, Music, Musical, Mystery, News, Reality-TV, Romance, Sci-Fi, Short, Sport, Talk-Show, Thriller, War, Western |
| evaluated_on | standardised bronze tables (before cleaning) |

## Violations per rule and table

| rule_id | table | description | n_violations | n_rows | pct_of_table |
| --- | --- | --- | --- | --- | --- |
| DQ01 | name_basics | deathYear earlier than birthYear | 28 | 15811387 | 0.0002 |
| DQ02 | name_basics | Age at death above max_age_years, or birthYear / deathYear after the reference year | 2 | 15811387 | 0.0000 |
| DQ03 | title_principals | Principal credited on a title released more than posthumous_grace_years after their death (archive material and exempt categories excluded) | 23742 | 102738762 | 0.0231 |
| DQ04 | title_principals | Principal credited on a title that was released (or, for a series, ended) before their birth year | 1159 | 102738762 | 0.0011 |
| DQ05:directors | title_crew | Orphan foreign key: at least one value of title_crew.directors has no parent row in name_basics.nconst | 419 | 12958477 | 0.0032 |
| DQ05:knownForTitles | name_basics | Orphan foreign key: at least one value of name_basics.knownForTitles has no parent row in title_basics.tconst | 6 | 15811387 | 0.0000 |
| DQ05:nconst | title_principals | Orphan foreign key: title_principals.nconst has no parent row in name_basics.nconst | 8263 | 102738762 | 0.0080 |
| DQ05:parentTconst | title_episode | Orphan foreign key: title_episode.parentTconst has no parent row in title_basics.tconst | 5 | 10030795 | 0.0000 |
| DQ05:tconst | title_crew | Orphan foreign key: title_crew.tconst has no parent row in title_basics.tconst | 0 | 12958477 | 0.0000 |
| DQ05:tconst | title_episode | Orphan foreign key: title_episode.tconst has no parent row in title_basics.tconst | 0 | 10030795 | 0.0000 |
| DQ05:tconst | title_principals | Orphan foreign key: title_principals.tconst has no parent row in title_basics.tconst | 0 | 102738762 | 0.0000 |
| DQ05:tconst | title_ratings | Orphan foreign key: title_ratings.tconst has no parent row in title_basics.tconst | 0 | 1731756 | 0.0000 |
| DQ05:titleId | title_akas | Orphan foreign key: title_akas.titleId has no parent row in title_basics.tconst | 0 | 60385482 | 0.0000 |
| DQ05:writers | title_crew | Orphan foreign key: at least one value of title_crew.writers has no parent row in name_basics.nconst | 812 | 12958477 | 0.0063 |
| DQ06 | title_basics | endYear earlier than startYear | 0 | 12958477 | 0.0000 |
| DQ07 | title_basics | startYear later than the reference year + max_future_years | 3 | 12958477 | 0.0000 |
| DQ08 | title_basics | runtimeMinutes <= 0 or above max_runtime_minutes | 446 | 12958477 | 0.0034 |
| DQ09 | name_basics | Value that cannot be converted to its expected type (birthYear, deathYear, knownForTitles, primaryProfession), e.g. non-numeric number or flag not in {0,1} | 0 | 15811387 | 0.0000 |
| DQ09 | title_akas | Value that cannot be converted to its expected type (attributes, isOriginalTitle, ordering, types), e.g. non-numeric number or flag not in {0,1} | 0 | 60385482 | 0.0000 |
| DQ09 | title_basics | Value that cannot be converted to its expected type (endYear, genres, isAdult, runtimeMinutes, startYear), e.g. non-numeric number or flag not in {0,1} | 0 | 12958477 | 0.0000 |
| DQ09 | title_principals | Value that cannot be converted to its expected type (characters, ordering), e.g. non-numeric number or flag not in {0,1} | 0 | 102738762 | 0.0000 |
| DQ09 | title_ratings | Value that cannot be converted to its expected type (averageRating, numVotes), e.g. non-numeric number or flag not in {0,1} | 0 | 1731756 | 0.0000 |
| DQ10 | name_basics | Duplicated primary key (nconst) | 0 | 15811387 | 0.0000 |
| DQ10 | title_akas | Duplicated primary key (titleId, ordering) | 0 | 60385482 | 0.0000 |
| DQ10 | title_basics | Duplicated primary key (tconst) | 0 | 12958477 | 0.0000 |
| DQ10 | title_crew | Duplicated primary key (tconst) | 0 | 12958477 | 0.0000 |
| DQ10 | title_episode | Duplicated primary key (tconst) | 0 | 10030795 | 0.0000 |
| DQ10 | title_principals | Duplicated primary key (tconst, ordering) | 0 | 102738762 | 0.0000 |
| DQ10 | title_ratings | Duplicated primary key (tconst) | 0 | 1731756 | 0.0000 |
| DQ11 | title_episode | Episode whose parent title is not of an episode_parent_types type | 0 | 10030795 | 0.0000 |
| DQ12 | title_ratings | averageRating outside [rating_min, rating_max] or numVotes <= 0 | 0 | 1731756 | 0.0000 |
| DQ13 | title_basics | Genre outside the known_genres list | 0 | 12958477 | 0.0000 |
| DQ14 | title_episode | seasonNumber or episodeNumber <= 0 or non-numeric | 7125 | 10030795 | 0.0710 |
| DQ15 | name_basics | Malformed line: number of fields different from the header | 0 | 15811387 | 0.0000 |
| DQ15 | title_akas | Malformed line: number of fields different from the header | 0 | 60385482 | 0.0000 |
| DQ15 | title_basics | Malformed line: number of fields different from the header | 0 | 12958477 | 0.0000 |
| DQ15 | title_crew | Malformed line: number of fields different from the header | 0 | 12958477 | 0.0000 |
| DQ15 | title_episode | Malformed line: number of fields different from the header | 0 | 10030795 | 0.0000 |
| DQ15 | title_principals | Malformed line: number of fields different from the header | 0 | 102738762 | 0.0000 |
| DQ15 | title_ratings | Malformed line: number of fields different from the header | 0 | 1731756 | 0.0000 |
| DQ16 | name_basics | Missing primary key component (nconst) | 0 | 15811387 | 0.0000 |
| DQ16 | title_akas | Missing primary key component (titleId, ordering) | 0 | 60385482 | 0.0000 |
| DQ16 | title_basics | Missing primary key component (tconst) | 0 | 12958477 | 0.0000 |
| DQ16 | title_crew | Missing primary key component (tconst) | 0 | 12958477 | 0.0000 |
| DQ16 | title_episode | Missing primary key component (tconst) | 0 | 10030795 | 0.0000 |
| DQ16 | title_principals | Missing primary key component (tconst, ordering) | 0 | 102738762 | 0.0000 |
| DQ16 | title_ratings | Missing primary key component (tconst) | 0 | 1731756 | 0.0000 |
