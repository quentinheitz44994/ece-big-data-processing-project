# Q8 - Multi-talented professionals: multi-role films versus single-role films

## Parameters

| parameter | value |
| --- | --- |
| feature_film.title_types | movie |
| feature_film.min_runtime_minutes | 40 |
| feature_film.include_adult | false |
| min_votes | 1000 |
| role_categories | actor->actor, actress->actor, director->director, writer->writer |
| crew_roles | title.crew.directors -> director, title.crew.writers -> writer |
| min_titles_per_role | 3 |
| multi_talented | at least 2 roles with min_titles_per_role films each |
| multi_role_film | film on which the person holds 2 or more roles |
| diff | per person: mean rating of multi-role films - mean rating of single-role films |
| multi_talented_people | 3653 |
| people_with_multi_and_single_role_films | 2734 |

## Multi-talented people per set of career roles

| career_roles | people |
| --- | --- |
| actor+director | 152 |
| actor+director+writer | 440 |
| actor+writer | 392 |
| director+writer | 2669 |

## Paired comparison per role combination on the same film

| combination | people | multi_role_films | mean_rating_multi_role | mean_rating_single_role | mean_diff | median_diff | std_diff | pct_people_better_multi_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| any combination | 2734 | 14226 | 6.29 | 6.17 | 0.11 | 0.12 | 0.78 | 57.57 |
| actor+director | 169 | 332 | 6.15 | 6.21 | -0.06 | 0.06 | 0.86 | 55.03 |
| actor+director+writer | 540 | 1299 | 6.20 | 6.13 | 0.07 | 0.10 | 0.97 | 53.89 |
| actor+writer | 468 | 1323 | 6.16 | 6.05 | 0.11 | 0.13 | 0.94 | 57.26 |
| director+writer | 2296 | 11272 | 6.31 | 6.20 | 0.12 | 0.12 | 0.79 | 57.45 |

## People with the most multi-role films

_Showing 30 of 2734 rows_

| primaryName | career_roles | n_multi | avg_multi | n_single | avg_single | diff |
| --- | --- | --- | --- | --- | --- | --- |
| Woody Allen | actor+director+writer | 54 | 6.89 | 7 | 5.87 | 1.02 |
| Werner Herzog | actor+director+writer | 41 | 7.11 | 6 | 6.47 | 0.64 |
| Claude Chabrol | actor+director+writer | 37 | 6.82 | 8 | 6.75 | 0.07 |
| Ingmar Bergman | actor+director+writer | 36 | 7.33 | 6 | 7.20 | 0.13 |
| Jean-Luc Godard | actor+director+writer | 35 | 6.65 | 5 | 6.22 | 0.43 |
| Tyler Perry | actor+director+writer | 35 | 5.36 | 7 | 6.43 | -1.07 |
| Akira Kurosawa | director+writer | 31 | 7.54 | 10 | 6.96 | 0.58 |
| Jesús Franco | actor+director+writer | 30 | 4.86 | 8 | 4.54 | 0.33 |
| Satyajit Ray | director+writer | 28 | 7.93 | 6 | 7.05 | 0.88 |
| Wim Wenders | director+writer | 27 | 7.00 | 8 | 6.41 | 0.58 |
| Clint Eastwood | actor+director | 26 | 6.89 | 40 | 6.90 | -0.01 |
| Billy Wilder | director+writer | 26 | 7.38 | 16 | 6.98 | 0.40 |
| Sylvester Stallone | actor+director+writer | 25 | 6.32 | 38 | 5.61 | 0.71 |
| Luis Buñuel | director+writer | 25 | 7.36 | 4 | 7.28 | 0.09 |
| Éric Rohmer | director+writer | 25 | 7.15 | 1 | 5.50 | 1.65 |
| Kamal Haasan | actor+director+writer | 25 | 7.51 | 28 | 7.69 | -0.18 |
| Yasujirō Ozu | director+writer | 25 | 7.61 | 2 | 7.00 | 0.61 |
| Mani Ratnam | director+writer | 25 | 7.41 | 3 | 6.33 | 1.07 |
| Blake Edwards | director+writer | 24 | 6.17 | 16 | 6.46 | -0.29 |
| Hark Tsui | actor+director+writer | 24 | 6.37 | 30 | 6.23 | 0.14 |
| Priyadarshan | director+writer | 24 | 6.86 | 15 | 7.12 | -0.26 |
| Carlo Verdone | actor+director+writer | 24 | 6.23 | 8 | 6.33 | -0.10 |
| Jing Wong | actor+director+writer | 24 | 6.12 | 11 | 6.56 | -0.45 |
| Federico Fellini | director+writer | 23 | 7.25 | 7 | 7.46 | -0.21 |
| Rainer Werner Fassbinder | actor+director+writer | 23 | 7.04 | 4 | 6.52 | 0.52 |
| Neri Parenti | director+writer | 23 | 5.24 | 1 | 4.60 | 0.64 |
| François Truffaut | actor+director+writer | 22 | 7.30 | 5 | 6.66 | 0.64 |
| Ethan Coen | director+writer | 21 | 7.13 | 7 | 6.30 | 0.83 |
| Takeshi Kitano | actor+director+writer | 21 | 6.90 | 7 | 6.67 | 0.23 |
| Samuel Fuller | actor+director+writer | 21 | 6.75 | 12 | 6.12 | 0.62 |

## CSV exports

| file | total_rows | exported_rows | truncated | gold_directory |
| --- | --- | --- | --- | --- |
| q8_multi_talented_summary.csv | 5 | 5 | false | data/gold/exploration |
| q8_multi_talented_career_roles.csv | 4 | 4 | false | data/gold/exploration |
| q8_multi_talented.csv | 6207 | 6207 | false | data/gold/exploration |
