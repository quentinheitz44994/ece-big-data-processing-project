# Bronze ingestion summary

## Parameters

| parameter | value |
| --- | --- |
| raw_path | data/raw |
| bronze_path | data/bronze |
| bronze_column_type | string (all columns) |
| malformed_rows | lines whose number of fields differs from the header |

## Rows per table

| table | source_file | rows | columns | malformed_rows |
| --- | --- | --- | --- | --- |
| name_basics | name.basics.tsv.gz | 15811387 | 6 | 0 |
| title_akas | title.akas.tsv.gz | 60385482 | 8 | 0 |
| title_basics | title.basics.tsv.gz | 12958477 | 9 | 0 |
| title_crew | title.crew.tsv.gz | 12958477 | 3 | 0 |
| title_episode | title.episode.tsv.gz | 10030795 | 4 | 0 |
| title_principals | title.principals.tsv.gz | 102738762 | 6 | 0 |
| title_ratings | title.ratings.tsv.gz | 1731756 | 3 | 0 |
