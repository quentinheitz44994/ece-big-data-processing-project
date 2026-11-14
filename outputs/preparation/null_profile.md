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
| name_basics | birthYear | 15811387 | 0 | 15125575 | 0 | 0 | 0 | 15125575 | 95.6625 |
| name_basics | deathYear | 15811387 | 0 | 15545911 | 0 | 0 | 0 | 15545911 | 98.3210 |
| name_basics | knownForTitles | 15811387 | 0 | 1916998 | 0 | 0 | 0 | 1916998 | 12.1242 |
| name_basics | nconst | 15811387 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| name_basics | primaryName | 15811387 | 0 | 89 | 0 | 0 | 0 | 89 | 0.0006 |
| name_basics | primaryProfession | 15811387 | 0 | 3219428 | 0 | 0 | 0 | 3219428 | 20.3615 |
| title_akas | attributes | 60385482 | 0 | 60068229 | 0 | 0 | 0 | 60068229 | 99.4746 |
| title_akas | isOriginalTitle | 60385482 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_akas | language | 60385482 | 0 | 19655399 | 0 | 0 | 0 | 19655399 | 32.5499 |
| title_akas | ordering | 60385482 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_akas | region | 60385482 | 0 | 12998541 | 0 | 0 | 0 | 12998541 | 21.5259 |
| title_akas | title | 60385482 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_akas | titleId | 60385482 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_akas | types | 60385482 | 0 | 40375080 | 0 | 0 | 0 | 40375080 | 66.8622 |
| title_basics | endYear | 12958477 | 0 | 12794047 | 0 | 0 | 0 | 12794047 | 98.7311 |
| title_basics | genres | 12958477 | 0 | 547930 | 0 | 0 | 0 | 547930 | 4.2284 |
| title_basics | isAdult | 12958477 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_basics | originalTitle | 12958477 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_basics | primaryTitle | 12958477 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_basics | runtimeMinutes | 12958477 | 0 | 8056989 | 0 | 0 | 0 | 8056989 | 62.1754 |
| title_basics | startYear | 12958477 | 0 | 1487875 | 0 | 0 | 0 | 1487875 | 11.4819 |
| title_basics | tconst | 12958477 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_basics | titleType | 12958477 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_crew | directors | 12958477 | 0 | 5789625 | 0 | 0 | 0 | 5789625 | 44.6783 |
| title_crew | tconst | 12958477 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_crew | writers | 12958477 | 0 | 6430569 | 0 | 0 | 0 | 6430569 | 49.6244 |
| title_episode | episodeNumber | 10030795 | 0 | 2123916 | 0 | 0 | 0 | 2123916 | 21.1740 |
| title_episode | parentTconst | 10030795 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_episode | seasonNumber | 10030795 | 0 | 2123916 | 0 | 0 | 0 | 2123916 | 21.1740 |
| title_episode | tconst | 10030795 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_principals | category | 102738762 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_principals | characters | 102738762 | 0 | 52680715 | 0 | 0 | 0 | 52680715 | 51.2764 |
| title_principals | job | 102738762 | 0 | 82869755 | 0 | 0 | 0 | 82869755 | 80.6607 |
| title_principals | nconst | 102738762 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_principals | ordering | 102738762 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_principals | tconst | 102738762 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_ratings | averageRating | 1731756 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_ratings | numVotes | 1731756 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
| title_ratings | tconst | 1731756 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0000 |
