# Open question - Recurring director-actor collaborations

## Parameters

| parameter | value |
| --- | --- |
| feature_film.title_types | movie |
| feature_film.min_runtime_minutes | 40 |
| feature_film.include_adult | false |
| min_votes | 1000 |
| actor_categories | actor, actress |
| director_sources | title.crew.directors UNION title.principals (category = director) |
| exclude_self_direction | true |
| min_collaborations | 2 |
| equal_tolerance | 0.05 |
| pair_ordering | startYear asc, tconst asc |
| rated_feature_films | 49434 |
| collaboration_rows | 507560 |
| recurring_pairs | 26630 |

## Overall

| metric | value |
| --- | --- |
| director-actor pairs (at least one film) | 469141 |
| recurring pairs (>= 2 films) | 26630 |
| share of pairs that are recurring | 0.057 |
| mean rating, films of one-off pairs | 6.128 |
| mean rating, first film of recurring pairs | 6.606 |
| mean of pair repeat-film mean ratings | 6.325 |
| mean delta (repeat - first) | -0.281 |
| median delta (approx.) | -0.200 |
| standard deviation of delta | 0.853 |
| paired t statistic of delta | -53.674 |
| share of pairs: repeats higher | 0.329 |
| share of pairs: repeats equal | 0.063 |
| share of pairs: repeats lower | 0.608 |
| recurring pairs with a director baseline | 21573 |
| mean excess vs director baseline | 0.118 |
| share of pairs with positive excess | 0.571 |

## Recurring pairs by collaboration rank

| collab_rank | films | avg_rating | avg_diff_vs_first | avg_votes |
| --- | --- | --- | --- | --- |
| 1 | 26630 | 6.61 | 0.00 | 48622.84 |
| 2 | 26630 | 6.36 | -0.24 | 36250.71 |
| 3 | 6587 | 6.40 | -0.35 | 40428.08 |
| 4 | 2431 | 6.44 | -0.37 | 35037.10 |
| 5+ | 2771 | 6.42 | -0.40 | 19510.01 |

## Recurring pairs by number of collaborations

| collaborations | pairs | avg_first_rating | avg_repeat_rating | avg_delta | share_higher | avg_excess_vs_director |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 20043 | 6.56 | 6.28 | -0.28 | 0.34 | 0.10 |
| 3 | 4156 | 6.71 | 6.43 | -0.28 | 0.30 | 0.15 |
| 4-5 | 1850 | 6.79 | 6.48 | -0.31 | 0.29 | 0.17 |
| 6+ | 581 | 6.85 | 6.60 | -0.25 | 0.30 | 0.22 |

## Most frequent recurring pairs

_Showing 30 of 26630 rows_

| director | actor | n_collabs | first_title | first_year | last_year | first_rating | repeat_avg_rating | delta | baseline_avg_rating | excess |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kartal Tibet | Kemal Sunal | 26 | Tosun Pasha | 1976 | 1990 | 8.80 | 6.83 | -1.97 | 5.40 | 1.43 |
| Gerald Thomas | Joan Sims | 25 | Carry on Nurse | 1959 | 1978 | 6.20 | 6.03 | -0.17 | 5.72 | 0.31 |
| Gerald Thomas | Kenneth Williams | 25 | Carry on Sergeant | 1958 | 1978 | 6.30 | 6.12 | -0.18 | 5.49 | 0.63 |
| Gerald Thomas | Charles Hawtrey | 23 | Carry on Sergeant | 1958 | 1972 | 6.30 | 6.29 | -0.01 | 5.21 | 1.08 |
| Gerald Thomas | Sidney James | 21 | Carry on Constable | 1960 | 1974 | 6.20 | 6.27 | 0.07 | 5.15 | 1.12 |
| Yasujirō Ozu | Chishū Ryū | 20 | That Night's Wife | 1930 | 1962 | 6.90 | 7.69 | 0.79 | 7.33 | 0.36 |
| Johnnie To | Suet Lam | 20 | Expect the Unexpected | 1998 | 2016 | 7.00 | 6.76 | -0.24 | 6.67 | 0.10 |
| Akira Kurosawa | Takashi Shimura | 19 | Sanshiro Sugata | 1943 | 1963 | 6.70 | 7.62 | 0.92 | 7.49 | 0.13 |
| Gerald Thomas | Kenneth Connor | 17 | Carry on Sergeant | 1958 | 1978 | 6.30 | 5.84 | -0.46 | 6.12 | -0.28 |
| Ingmar Bergman | Gunnar Björnstrand | 16 | It Rains on Our Love | 1946 | 1978 | 6.60 | 7.58 | 0.98 | 7.15 | 0.43 |
| Erik Balling | Ove Sprogøe | 16 | Summer in Tyrol | 1964 | 1984 | 6.70 | 6.93 | 0.23 |  |  |
| Akira Kurosawa | Toshirō Mifune | 16 | Drunken Angel | 1948 | 1965 | 7.60 | 7.83 | 0.23 | 7.73 | 0.09 |
| Kunihiko Yuyama | Ikue Otani | 16 | Pokémon: The First Movie - Mewtwo Strikes Back | 1998 | 2019 | 6.40 | 5.95 | -0.45 | 5.97 | -0.02 |
| David Dhawan | Govinda | 16 | Swarg | 1990 | 2009 | 6.70 | 5.95 | -0.75 | 4.96 | 1.00 |
| Ertem Eğilmez | Adile Naşit | 15 | Sev Kardesim | 1972 | 1984 | 6.60 | 8.10 | 1.50 | 7.56 | 0.54 |
| Priyadarshan | Mohanlal | 15 | Boeing Boeing | 1985 | 2021 | 7.30 | 7.53 | 0.23 | 6.62 | 0.91 |
| Erik Balling | Poul Bundgaard | 15 | Martha | 1967 | 1984 | 7.10 | 6.92 | -0.18 |  |  |
| Claude Chabrol | Stéphane Audran | 15 | The Cousins | 1959 | 1992 | 7.20 | 6.92 | -0.28 | 6.67 | 0.25 |
| John Ford | Ward Bond | 14 | Up the River | 1930 | 1957 | 5.90 | 7.13 | 1.23 | 6.95 | 0.18 |
| Ertem Eğilmez | Halit Akçatepe | 14 | Sweet Talker | 1972 | 1977 | 7.10 | 8.11 | 1.01 | 7.49 | 0.62 |
| Gerald Thomas | Bernard Bresslaw | 14 | Carry on Cowboy | 1965 | 1975 | 6.20 | 6.22 | 0.02 | 5.13 | 1.09 |
| Erik Balling | Morten Grunwald | 14 | Martha | 1967 | 1981 | 7.10 | 6.93 | -0.17 | 6.80 | 0.13 |
| Ishirō Honda | Kenji Sahara | 14 | Rodan | 1956 | 1970 | 6.20 | 5.82 | -0.38 | 6.07 | -0.25 |
| John Ford | John Wayne | 14 | Stagecoach | 1939 | 1963 | 7.80 | 7.21 | -0.59 | 6.96 | 0.25 |
| Priyadarshan | Paresh Rawal | 14 | Hera Pheri | 2000 | 2026 | 8.20 | 6.39 | -1.81 | 6.34 | 0.06 |
| Ertem Eğilmez | Kemal Sunal | 13 | Sweet Talker | 1972 | 1977 | 7.10 | 8.25 | 1.15 | 7.35 | 0.90 |
| Ertem Eğilmez | Münir Özkul | 13 | Sweet Talker | 1972 | 1989 | 7.10 | 7.93 | 0.83 | 7.84 | 0.09 |
| Erik Balling | Kirsten Walther | 13 | The Olsen Gang | 1968 | 1981 | 6.60 | 6.96 | 0.36 | 6.80 | 0.16 |
| Togan Gökbakar | Şahan Gökbakar | 13 | Gen | 2006 | 2024 | 4.30 | 3.96 | -0.34 |  |  |
| Gerald Thomas | Peter Butterworth | 13 | Carry on Cowboy | 1965 | 1978 | 6.20 | 5.80 | -0.40 | 5.89 | -0.09 |

## CSV exports

| file | total_rows | exported_rows | truncated |
| --- | --- | --- | --- |
| collaborations_pairs.csv | 26630 | 26630 | false |
| collaborations_by_rank.csv | 5 | 5 | false |
| collaborations_by_count.csv | 4 | 4 | false |
