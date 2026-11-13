# Top 5 columns by percentage of missing values

## Parameters

| parameter | value |
| --- | --- |
| top_n | 5 |
| ranking | pct_missing desc, n_missing_total desc |

## Whole dataset

| rank | table | column | n_total | n_null | n_backslash_n | n_empty | n_whitespace | n_empty_array | n_missing_total | pct_missing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | title_akas | attributes | 60321594 | 0 | 60004431 | 0 | 0 | 0 | 60004431 | 99.4742 |
| 2 | title_basics | endYear | 12951113 | 0 | 12786793 | 0 | 0 | 0 | 12786793 | 98.7312 |
| 3 | name_basics | deathYear | 15803779 | 0 | 15538408 | 0 | 0 | 0 | 15538408 | 98.3208 |
| 4 | name_basics | birthYear | 15803779 | 0 | 15118179 | 0 | 0 | 0 | 15118179 | 95.6618 |
| 5 | title_principals | job | 102649609 | 0 | 82794746 | 0 | 0 | 0 | 82794746 | 80.6576 |
