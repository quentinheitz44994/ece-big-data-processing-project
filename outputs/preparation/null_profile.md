# Missing values per column

## Parameters

| parameter | value |
| --- | --- |
| n_null | SQL null in bronze (empty raw field, or field absent from a short line) |
| n_backslash_n | value equal to the IMDb marker \\N |
| n_empty | empty string |
| n_whitespace | non-empty value made of whitespace only |
| n_empty_array | [] in a multi-valued column encoded as text |
| n_missing_total | sum of the five counts (mutually exclusive) |
| pct_missing | 100 * n_missing_total / n_total |

## All tables and columns

| table | column | n_total | n_null | n_backslash_n | n_empty | n_whitespace | n_empty_array | n_missing_total | pct_missing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| name_basics | birthYear | 15803779 | 0 | 15118179 | 0 | 0 | 0 | 15118179 | 95.6618 |
| name_basics | deathYear | 15803779 | 0 | 15538408 | 0 | 0 | 0 | 15538408 | 98.3208 |
| name_basics | knownForTitles | 15803779 | 0 | 1915916 | 0 | 0 | 0 | 1915916 | 12.1232 |
| name_basics | nconst | 15803779 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| name_basics | primaryName | 15803779 | 0 | 89 | 0 | 0 | 0 | 89 | 0.0006 |
| name_basics | primaryProfession | 15803779 | 0 | 3217014 | 0 | 0 | 0 | 3217014 | 20.3560 |
| title_akas | attributes | 60321594 | 0 | 60004431 | 0 | 0 | 0 | 60004431 | 99.4742 |
| title_akas | isOriginalTitle | 60321594 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_akas | language | 60321594 | 0 | 19639034 | 0 | 0 | 0 | 19639034 | 32.5572 |
| title_akas | ordering | 60321594 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_akas | region | 60321594 | 0 | 12991240 | 0 | 0 | 0 | 12991240 | 21.5366 |
| title_akas | title | 60321594 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_akas | titleId | 60321594 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_akas | types | 60321594 | 0 | 40342236 | 0 | 0 | 0 | 40342236 | 66.8786 |
| title_basics | endYear | 12951113 | 0 | 12786793 | 0 | 0 | 0 | 12786793 | 98.7312 |
| title_basics | genres | 12951113 | 0 | 547430 | 0 | 0 | 0 | 547430 | 4.2269 |
| title_basics | isAdult | 12951113 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_basics | originalTitle | 12951113 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_basics | primaryTitle | 12951113 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_basics | runtimeMinutes | 12951113 | 0 | 8052653 | 0 | 0 | 0 | 8052653 | 62.1773 |
| title_basics | startYear | 12951113 | 0 | 1487768 | 0 | 0 | 0 | 1487768 | 11.4876 |
| title_basics | tconst | 12951113 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_basics | titleType | 12951113 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_crew | directors | 12951113 | 0 | 5784884 | 0 | 0 | 0 | 5784884 | 44.6671 |
| title_crew | tconst | 12951113 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_crew | writers | 12951113 | 0 | 6426266 | 0 | 0 | 0 | 6426266 | 49.6194 |
| title_episode | episodeNumber | 10023959 | 0 | 2119873 | 0 | 0 | 0 | 2119873 | 21.1481 |
| title_episode | parentTconst | 10023959 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_episode | seasonNumber | 10023959 | 0 | 2119873 | 0 | 0 | 0 | 2119873 | 21.1481 |
| title_episode | tconst | 10023959 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_principals | category | 102649609 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_principals | characters | 102649609 | 0 | 52649325 | 0 | 0 | 0 | 52649325 | 51.2903 |
| title_principals | job | 102649609 | 0 | 82794746 | 0 | 0 | 0 | 82794746 | 80.6576 |
| title_principals | nconst | 102649609 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_principals | ordering | 102649609 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_principals | tconst | 102649609 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_ratings | averageRating | 1730885 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_ratings | numVotes | 1730885 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_ratings | tconst | 1730885 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
