# Top 5 columns by percentage of missing values

## Parameters

| parameter | value |
| --- | --- |
| top_n | 5 |
| ranking | pct_missing desc, n_missing_total desc |

## Whole dataset

| rank | table | column | n_total | n_null | n_backslash_n | n_empty | n_whitespace | n_empty_array | n_missing_total | pct_missing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | title_akas | attributes | 60385482 | 0 | 60068229 | 0 | 0 | 0 | 60068229 | 99.4746 |
| 2 | title_basics | endYear | 12958477 | 0 | 12794047 | 0 | 0 | 0 | 12794047 | 98.7311 |
| 3 | name_basics | deathYear | 15811387 | 0 | 15545911 | 0 | 0 | 0 | 15545911 | 98.3210 |
| 4 | name_basics | birthYear | 15811387 | 0 | 15125575 | 0 | 0 | 0 | 15125575 | 95.6625 |
| 5 | title_principals | job | 102738762 | 0 | 82869755 | 0 | 0 | 0 | 82869755 | 80.6607 |
