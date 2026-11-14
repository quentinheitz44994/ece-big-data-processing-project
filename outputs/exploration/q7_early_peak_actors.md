# Q7 - Long-career actors and actresses whose ratings peaked early

## Parameters

| parameter | value |
| --- | --- |
| feature_film.title_types | movie |
| feature_film.min_runtime_minutes | 40 |
| feature_film.include_adult | false |
| min_votes | 1000 |
| categories | actor, actress |
| min_career_years | 20 |
| min_films | 15 |
| early_fraction | 0.333333 |
| top_k | 3 |
| career_years | last release year - first release year of the films considered |
| early_peak | peak_position <= early_fraction AND first_half_avg > second_half_avg (peak = best-rated film; ties: most votes, then earliest) |
| rating_slope | covar_samp(year, rating) / var_samp(year), rating points per year |
| long_career_people | 3528 |
| early_peak_people | 1557 |
| sorted_by | first_half_avg - second_half_avg desc |

## Population summary (early peak versus others)

| early_peak | people | avg_career_years | avg_films | avg_peak_position | avg_top_k_mean_position | avg_first_minus_second_half | avg_rating_slope | pct_negative_slope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| true | 1557 | 35.18 | 27.24 | 0.14 | 0.27 | 0.66 | -0.04 | 96.85 |
| false | 1971 | 33.74 | 28.35 | 0.57 | 0.48 | 0.18 | -0.01 | 67.38 |

## Actors and actresses with an early peak

_Showing 50 of 1557 rows_

| primaryName | birthYear | first_year | last_year | career_years | n_films | avg_rating | peak_title | peak_year | peak_rating | peak_position | first_half_avg | second_half_avg | rating_slope | top_k_mean_position |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Halit Akçatepe | 1938 | 1972 | 2005 | 33 | 24 | 7.28 | The Chaos Class | 1975 | 9.10 | 0.09 | 7.63 | 3.45 | -0.13 | 0.11 |
| Wendell Corey | 1914 | 1947 | 1968 | 21 | 22 | 6.40 | Rear Window | 1954 | 8.40 | 0.33 | 7.01 | 3.65 | -0.21 | 0.14 |
| Cüneyt Arkın | 1937 | 1964 | 2014 | 50 | 18 | 5.87 | The Mine | 1978 | 7.50 | 0.28 | 6.34 | 3.50 | -0.07 | 0.21 |
| Evelyn Keyes | 1916 | 1939 | 1989 | 50 | 17 | 6.64 | Gone with the Wind | 1939 | 8.20 | 0.00 | 6.97 | 4.15 | -0.06 | 0.11 |
| Madhan Bob | 1953 | 1992 | 2021 | 29 | 16 | 6.84 | Thevar Magan | 1992 | 8.60 | 0.00 | 7.52 | 4.83 | -0.16 | 0.13 |
| Ranjeet Bedi | 1942 | 1979 | 2017 | 38 | 17 | 5.48 | Satte Pe Satta | 1982 | 7.20 | 0.08 | 6.72 | 4.08 | -0.08 | 0.07 |
| James Duval | 1972 | 1993 | 2024 | 31 | 22 | 4.95 | Donnie Darko | 2001 | 8.00 | 0.26 | 6.11 | 3.79 | -0.14 | 0.24 |
| Steve Brodie | 1919 | 1947 | 1988 | 41 | 20 | 6.10 | Out of the Past | 1947 | 7.90 | 0.00 | 6.44 | 4.13 | -0.08 | 0.03 |
| Baiju Santhosh |  | 1989 | 2026 | 37 | 18 | 6.19 | Vadakkunokkiyantram | 1989 | 8.30 | 0.00 | 8.30 | 6.06 | -0.08 | 0.50 |
| Corey Feldman |  | 1984 | 2021 | 37 | 15 | 5.67 | Stand by Me | 1986 | 8.10 | 0.05 | 6.26 | 4.05 | -0.09 | 0.03 |
| Tulasi | 1967 | 1980 | 2026 | 46 | 25 | 6.67 | Sankarabharanam | 1980 | 8.80 | 0.00 | 8.70 | 6.50 | -0.06 | 0.35 |
| Metin Akpınar | 1941 | 1973 | 2018 | 45 | 19 | 6.36 | My Dear Brother | 1973 | 8.60 | 0.00 | 7.28 | 5.10 | -0.08 | 0.01 |
| Geetha | 1962 | 1983 | 2025 | 42 | 17 | 6.52 | Sagara Sangamam | 1983 | 8.70 | 0.00 | 7.93 | 5.75 | -0.09 | 0.16 |
| Max Perlich | 1968 | 1989 | 2020 | 31 | 19 | 5.41 | Drugstore Cowboy | 1989 | 7.20 | 0.00 | 5.87 | 3.70 | -0.11 | 0.10 |
| Robert LaSardo | 1963 | 1991 | 2024 | 33 | 24 | 4.04 | Out for Justice | 1991 | 6.10 | 0.00 | 6.10 | 3.95 | -0.06 | 0.49 |
| Andrew Duggan | 1923 | 1957 | 1987 | 30 | 16 | 5.95 | Seven Days in May | 1964 | 7.80 | 0.23 | 6.48 | 4.35 | -0.10 | 0.23 |
| Andrew Stevens | 1955 | 1976 | 2022 | 46 | 16 | 5.03 | Death Hunt | 1981 | 6.90 | 0.11 | 5.43 | 3.30 | -0.06 | 0.07 |
| Mahima Chaudhry | 1973 | 1997 | 2025 | 28 | 15 | 5.88 | Sehar | 2005 | 7.70 | 0.29 | 6.16 | 4.05 | -0.08 | 0.17 |
| Mehmet Ali Erbil | 1957 | 1981 | 2024 | 43 | 15 | 3.53 | The Chaos Class: Bye Bye | 1981 | 6.30 | 0.00 | 5.08 | 2.96 | -0.10 | 0.30 |
| Johnny Messner | 1970 | 2003 | 2023 | 20 | 27 | 4.57 | Running Scared | 2006 | 7.30 | 0.15 | 5.82 | 3.72 | -0.15 | 0.07 |
| Nandamuri Balakrishna | 1960 | 1991 | 2025 | 34 | 17 | 6.14 | Aditya 369 | 1991 | 8.40 | 0.00 | 7.72 | 5.65 | -0.09 | 0.11 |
| Ayşen Gruda | 1944 | 1975 | 2016 | 41 | 31 | 7.13 | Tosun Pasha | 1976 | 8.80 | 0.02 | 7.53 | 5.45 | -0.06 | 0.03 |
| Nandhu |  | 1994 | 2026 | 32 | 19 | 6.13 | Thenmavin Kombath | 1994 | 8.10 | 0.00 | 8.10 | 6.02 | -0.08 | 0.50 |
| Güven Kıraç | 1968 | 1997 | 2026 | 29 | 16 | 6.59 | Innocence | 1997 | 8.00 | 0.00 | 7.24 | 5.16 | -0.11 | 0.09 |
| John Phillip Law | 1937 | 1966 | 2002 | 36 | 15 | 5.35 | The Russians Are Coming the Russians Are Coming | 1966 | 7.00 | 0.00 | 5.90 | 3.82 | -0.07 | 0.07 |
| Rosemary DeCamp | 1910 | 1941 | 1981 | 40 | 17 | 6.65 | Yankee Doodle Dandy | 1942 | 7.60 | 0.03 | 6.77 | 4.70 | -0.05 | 0.10 |
| Michael Sarrazin | 1940 | 1967 | 2002 | 35 | 15 | 5.99 | They Shoot Horses, Don't They? | 1969 | 7.80 | 0.06 | 6.26 | 4.20 | -0.08 | 0.06 |
| Jim Dale | 1935 | 1964 | 1992 | 28 | 15 | 6.08 | Carry on Screaming! | 1966 | 6.70 | 0.07 | 6.35 | 4.35 | -0.08 | 0.06 |
| William McNamara |  | 1987 | 2025 | 38 | 15 | 4.72 | Opera | 1987 | 6.90 | 0.00 | 5.51 | 3.53 | -0.08 | 0.08 |
| Mohanlal | 1960 | 1985 | 2026 | 41 | 101 | 6.97 | Kireedam | 1989 | 8.80 | 0.10 | 8.07 | 6.09 | -0.07 | 0.11 |
| Paul Koslo | 1944 | 1971 | 1993 | 22 | 17 | 5.79 | Vanishing Point | 1971 | 7.20 | 0.00 | 6.49 | 4.52 | -0.12 | 0.20 |
| Sharmila Tagore | 1944 | 1959 | 2023 | 64 | 19 | 7.07 | The World of Apu | 1959 | 8.40 | 0.00 | 7.88 | 5.96 | -0.04 | 0.12 |
| Edward Furlong | 1977 | 1991 | 2015 | 24 | 30 | 5.48 | Terminator 2: Judgment Day | 1991 | 8.60 | 0.00 | 6.55 | 4.65 | -0.11 | 0.12 |
| Raquel Welch | 1940 | 1966 | 2017 | 51 | 21 | 5.92 | The Last of Sheila | 1973 | 7.20 | 0.14 | 6.10 | 4.20 | -0.03 | 0.14 |
| Tusshar Kapoor | 1976 | 2001 | 2025 | 24 | 25 | 5.31 | Golmaal: Fun Unlimited | 2006 | 7.50 | 0.21 | 5.84 | 3.94 | -0.09 | 0.24 |
| Jason London | 1972 | 1991 | 2024 | 33 | 19 | 4.87 | Dazed and Confused | 1993 | 7.60 | 0.06 | 5.96 | 4.07 | -0.10 | 0.06 |
| Aldo Ray | 1926 | 1952 | 1990 | 38 | 22 | 5.81 | We're No Angels | 1955 | 7.30 | 0.08 | 6.50 | 4.61 | -0.09 | 0.11 |
| Karisma Kapoor | 1974 | 1992 | 2012 | 20 | 30 | 5.61 | Andaz Apna Apna | 1994 | 8.00 | 0.10 | 5.74 | 3.85 | -0.10 | 0.17 |
| Prabhu | 1956 | 1988 | 2026 | 38 | 36 | 6.19 | Kaalapani | 1996 | 8.50 | 0.21 | 7.70 | 5.82 | -0.06 | 0.23 |
| Arjun Sarja | 1962 | 1993 | 2026 | 33 | 19 | 6.64 | Kuruthipunal | 1995 | 8.50 | 0.06 | 8.12 | 6.25 | -0.08 | 0.26 |
| Zeki Alasya | 1943 | 1972 | 2009 | 37 | 20 | 6.38 | From the Village to the City | 1974 | 8.20 | 0.05 | 7.03 | 5.17 | -0.06 | 0.33 |
| Kovai Sarala | 1962 | 1994 | 2026 | 32 | 19 | 6.16 | Vasantha Vaasal | 1996 | 8.30 | 0.06 | 7.60 | 5.77 | -0.07 | 0.03 |
| William Sanderson | 1944 | 1977 | 2008 | 31 | 15 | 5.56 | Blade Runner | 1982 | 8.10 | 0.16 | 6.29 | 4.47 | -0.10 | 0.13 |
| Jaya Bachchan | 1948 | 1963 | 2023 | 60 | 20 | 6.98 | Koshish | 1972 | 8.40 | 0.15 | 7.80 | 5.99 | -0.05 | 0.12 |
| Massimo Boldi | 1945 | 1982 | 2005 | 23 | 17 | 4.89 | The Country Boy | 1984 | 6.90 | 0.09 | 6.05 | 4.25 | -0.10 | 0.06 |
| Ashokan | 1961 | 1986 | 2026 | 40 | 18 | 7.02 | Thoovanathumbikal | 1987 | 8.60 | 0.03 | 8.20 | 6.42 | -0.05 | 0.08 |
| Shelley Duvall | 1949 | 1970 | 2000 | 30 | 18 | 6.37 | The Shining | 1980 | 8.40 | 0.33 | 7.24 | 5.49 | -0.08 | 0.27 |
| Brendan Sexton III | 1980 | 1995 | 2024 | 29 | 21 | 5.76 | Boys Don't Cry | 1999 | 7.50 | 0.14 | 6.59 | 4.85 | -0.07 | 0.21 |
| Stella Stevens | 1938 | 1959 | 2005 | 46 | 22 | 5.74 | The Ballad of Cable Hogue | 1970 | 7.20 | 0.24 | 6.14 | 4.40 | -0.06 | 0.20 |
| Govardhan Asrani | 1941 | 1971 | 2026 | 55 | 43 | 5.91 | Koshish | 1972 | 8.40 | 0.02 | 7.07 | 5.36 | -0.07 | 0.21 |

## CSV exports

| file | total_rows | exported_rows | truncated | gold_directory |
| --- | --- | --- | --- | --- |
| q7_early_peak_actors.csv | 1557 | 1557 | false | data/gold/exploration |
| q7_early_peak_actors_summary.csv | 2 | 2 | false | data/gold/exploration |
