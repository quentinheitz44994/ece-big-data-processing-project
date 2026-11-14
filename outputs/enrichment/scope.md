# Enrichment scope

## Parameters

| parameter | value |
| --- | --- |
| feature_film.title_types | movie |
| feature_film.min_runtime_minutes | 40 |
| feature_film.include_adult | false |
| year_min | 1980 |
| year_max | 2025 |
| top_n | 10 |
| rank_by | numVotes desc, averageRating desc, tconst asc |
| principal_categories | actor, actress, director, writer |
| principals_per_film | 3 |
| principal_order | ordering asc (first credit of each person on the film) |

## Scope size

| counter | value |
| --- | --- |
| (genre, year) groups | 1027 |
| (film, genre, year) selections | 9832 |
| distinct films | 6821 |
| distinct genres | 25 |
| (film, person) pairs | 19645 |
| distinct people | 9759 |
| films with at least one selected principal | 6809 |
| films with principals_per_film selected principals | 6319 |

## Films per decade

| decade | films |
| --- | --- |
| 1980 | 1403 |
| 1990 | 1433 |
| 2000 | 1443 |
| 2010 | 1595 |
| 2020 | 947 |
