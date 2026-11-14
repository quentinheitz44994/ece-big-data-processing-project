# Report

## 1. Data Preparation

### Results

<!-- AUTO:preparation:start -->

#### IMDb data snapshot

##### Parameters

| parameter | value |
| --- | --- |
| source | https://datasets.imdbws.com |
| recorded_at_utc | 2026-11-13T14:01:07Z |

##### Files

| file | size_bytes | file_timestamp_utc | status |
| --- | --- | --- | --- |
| name.basics.tsv.gz | 312862653 | 2026-11-13T10:26:32Z | already present |
| title.akas.tsv.gz | 522774685 | 2026-11-13T10:29:08Z | already present |
| title.basics.tsv.gz | 230266102 | 2026-11-13T10:28:21Z | already present |
| title.crew.tsv.gz | 84078039 | 2026-11-13T10:27:28Z | already present |
| title.episode.tsv.gz | 55449325 | 2026-11-13T10:26:59Z | already present |
| title.principals.tsv.gz | 790533438 | 2026-11-13T10:29:58Z | already present |
| title.ratings.tsv.gz | 8750131 | 2026-11-13T10:25:56Z | already present |

#### Bronze ingestion summary

##### Parameters

| parameter | value |
| --- | --- |
| raw_path | data/raw |
| bronze_path | data/bronze |
| bronze_column_type | string (all columns) |
| malformed_rows | lines whose number of fields differs from the header |

##### Rows per table

| table | source_file | rows | columns | malformed_rows |
| --- | --- | --- | --- | --- |
| name_basics | name.basics.tsv.gz | 15811387 | 6 | 0 |
| title_akas | title.akas.tsv.gz | 60385482 | 8 | 0 |
| title_basics | title.basics.tsv.gz | 12958477 | 9 | 0 |
| title_crew | title.crew.tsv.gz | 12958477 | 3 | 0 |
| title_episode | title.episode.tsv.gz | 10030795 | 4 | 0 |
| title_principals | title.principals.tsv.gz | 102738762 | 6 | 0 |
| title_ratings | title.ratings.tsv.gz | 1731756 | 3 | 0 |

#### Missing values per column

##### Parameters

| parameter | value |
| --- | --- |
| n_null | SQL null in bronze (empty raw field, or field absent from a short line) |
| n_backslash_n | value equal to the IMDb marker \\N |
| n_empty | empty string |
| n_whitespace | non-empty value made of whitespace only |
| n_empty_array | [] in a multi-valued column encoded as text |
| n_missing_total | sum of the five counts (mutually exclusive) |
| pct_missing | 100 * n_missing_total / n_total |

##### All tables and columns

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

#### Top 5 columns by percentage of missing values

##### Parameters

| parameter | value |
| --- | --- |
| top_n | 5 |
| ranking | pct_missing desc, n_missing_total desc |

##### Whole dataset

| rank | table | column | n_total | n_null | n_backslash_n | n_empty | n_whitespace | n_empty_array | n_missing_total | pct_missing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | title_akas | attributes | 60385482 | 0 | 60068229 | 0 | 0 | 0 | 60068229 | 99.4746 |
| 2 | title_basics | endYear | 12958477 | 0 | 12794047 | 0 | 0 | 0 | 12794047 | 98.7311 |
| 3 | name_basics | deathYear | 15811387 | 0 | 15545911 | 0 | 0 | 0 | 15545911 | 98.3210 |
| 4 | name_basics | birthYear | 15811387 | 0 | 15125575 | 0 | 0 | 0 | 15125575 | 95.6625 |
| 5 | title_principals | job | 102738762 | 0 | 82869755 | 0 | 0 | 0 | 82869755 | 80.6607 |

#### Data quality report

##### Parameters

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

##### Violations per rule and table

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

#### Data quality report - sample rows

##### Parameters

| parameter | value |
| --- | --- |
| sample_size | 10 |
| text_truncated_at | 60 |

##### DQ01 - name_basics

_deathYear earlier than birthYear. Showing 10 of 28 violating row(s)._

| nconst | primaryName | birthYear | deathYear | primaryProfession | knownForTitles | _cast_errors | _corrupt_record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nm0012634 | Aeschylus | 525 | 456 | writer | tt0070453, tt5524714, tt33145207, tt0076871 |  |  |
| nm0012635 | Aesop | 620 | 560 | writer | tt0079466, tt0386936, tt32139270, tt12026942 |  |  |
| nm0034922 | Aristophanes | 450 | 388 | writer, soundtrack | tt4594834, tt29474378, tt0060028, tt0201742 |  |  |
| nm0174595 | Confucius | 551 | 479 | writer | tt0136776, tt0092322 |  |  |
| nm0202552 | C. Daveillans | 1962 | 1936 | writer | tt0183025, tt14793342 |  |  |
| nm0262381 | Euripides | 484 | 406 | writer, composer | tt0054650, tt29474378, tt0257740, tt0258203 |  |  |
| nm0392955 | Homer | 850 | 800 | writer, miscellaneous | tt33764258, tt0332452, tt0190590, tt35148005 |  |  |
| nm0515385 | Titus Livius | 59 | 17 | writer | tt0003740 |  |  |
| nm0541940 | A. Maneck | 1899 | 1867 | miscellaneous | tt0046416, tt0043466 |  |  |
| nm0549460 | Publius Vergilius Maro | 70 | 19 | writer | tt3373410, tt0172319, tt0159876, tt0112225 |  |  |

##### DQ02 - name_basics

_Age at death above max_age_years, or birthYear / deathYear after the reference year. Showing 2 of 2 violating row(s)._

| nconst | primaryName | birthYear | deathYear | primaryProfession | knownForTitles | _cast_errors | _corrupt_record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nm0130625 | Jeanne Louise Calment | 1875 | 1997 | soundtrack, archive_footage | tt2433670, tt0128058, tt0081721, tt10875582 |  |  |
| nm0243164 | Tatzumbia Dupea | 1849 | 1970 | actress |  |  |  |

##### DQ03 - title_principals

_Principal credited on a title released more than posthumous_grace_years after their death (archive material and exempt categories excluded). Showing 10 of 23742 violating row(s)._

| tconst | ordering | nconst | category | job | characters | _cast_errors | _corrupt_record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tt0000929 | 1 | nm0066941 | actor |  |  |  |  |
| tt0000929 | 2 | nm0170183 | actor |  |  |  |  |
| tt0000929 | 4 | nm0093361 | director |  |  |  |  |
| tt0003599 | 4 | nm1286798 | self |  | Self |  |  |
| tt0011801 | 1 | nm0681726 | actor |  | Musiker Erik Paulsen |  |  |
| tt0011801 | 2 | nm0692612 | actress |  | Karin, Tochter Brückner |  |  |
| tt0011801 | 3 | nm0726256 | actor |  | Sebald, Sohn Brückner |  |  |
| tt0011801 | 4 | nm0776458 | actor |  | Eriks Sohn |  |  |
| tt0011801 | 5 | nm0666006 | actor |  | Staatsanwalt Brückner |  |  |
| tt0011801 | 6 | nm0745073 | actor |  | Jurist Landt |  |  |

##### DQ04 - title_principals

_Principal credited on a title that was released (or, for a series, ended) before their birth year. Showing 10 of 1159 violating row(s)._

| tconst | ordering | nconst | category | job | characters | _cast_errors | _corrupt_record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tt0000229 | 4 | nm0595213 | composer | composer |  |  |  |
| tt0000417 | 15 | nm0242155 | composer | composer |  |  |  |
| tt0000417 | 16 | nm0324073 | composer | composer |  |  |  |
| tt0000417 | 17 | nm9991717 | composer | composer |  |  |  |
| tt0001223 | 9 | nm1529472 | composer |  |  |  |  |
| tt0001452 | 11 | nm0628190 | composer | composer |  |  |  |
| tt0002208 | 13 | nm1311785 | composer | composer |  |  |  |
| tt0002646 | 16 | nm0004592 | composer | composer |  |  |  |
| tt0004060 | 11 | nm0595213 | composer | composer |  |  |  |
| tt0004099 | 17 | nm0236373 | composer | composer |  |  |  |

##### DQ05:directors - title_crew

_Orphan foreign key: at least one value of title_crew.directors has no parent row in name_basics.nconst. Showing 10 of 419 violating row(s)._

| tconst | directors | writers | _cast_errors | _corrupt_record |
| --- | --- | --- | --- | --- |
| tt0850260 | nm17757903 |  |  |  |
| tt10568254 | nm17761498, nm2600814 | nm11075310, nm2288763 |  |  |
| tt1111863 | nm1011308, nm1367823, nm3741162, nm2637096, nm0256430, nm2843789, nm2806063, nm3812585, nm3750795, nm1000287, nm1011881, nm0341896, nm4650538, nm0227460, nm0757157, nm0857523, nm0901146, nm2783538, nm0581775, nm3741368, nm1026579, nm0591615, nm1022063, nm0407821, nm0716721, nm1058822, nm3741948, nm0039350, nm3292701, nm5857806, nm0813447, nm0130471, nm0465169, nm0667728, nm0288192, nm0323321, nm1688236, nm2764756, nm0465352, nm0998289, nm2613492, nm2535622, nm0510988, nm7220715, nm0631798, nm0804476, nm2590958, nm0048165, nm3765931, nm0468111, nm0510100, nm3372616, nm1105195, nm0083002, nm0277095, nm2789823, nm0584260, nm18615226, nm2818119, nm2558824, nm0660309, nm0955938, nm10464476, nm8527778, nm2567080, nm2187535, nm0901330, nm3188480, nm0363760, nm0468059, nm0804772, nm1176761, nm3382918, nm7731334, nm0874753, nm2549598, nm0903837, nm0028393, nm0299561, nm4621014, nm2597218, nm0803794, nm1008323, nm0468089, nm3765455, nm2821600, nm0859784, nm0369116, nm2922129, nm9127362, nm0608130, nm2552509, nm0802578, nm0224570, nm3016043, nm13416034, nm2580860, nm15815218, nm0128050, nm2637820, nm0660363, nm17023314 | nm1266781, nm0757157, nm0953554, nm0699622, nm0309738, nm0155009, nm0034922, nm1239212, nm0685063, nm0316328, nm0596942, nm0012634, nm1795633, nm0275492, nm0814668, nm0262381, nm0642156, nm0856167, nm3802297, nm0406585, nm5004532, nm0813447, nm0130471, nm2527146, nm3758773, nm0027355, nm0691602, nm0931783, nm0901339, nm0324690, nm0325958, nm0288192, nm10097138, nm0002005, nm2540989, nm2262327, nm0787323, nm0407821, nm2206842, nm11107248, nm2549598, nm0746090, nm3740554, nm0789737, nm0928642, nm10225746, nm12996167, nm0407651, nm0030478, nm0079348, nm1241805, nm1927610, nm1221649, nm0331003, nm0056217, nm0035422, nm1369998, nm0316067, nm0696538, nm0305030, nm0746097, nm8311879, nm0043697, nm0238610, nm0303335, nm2475716, nm12805875, nm2509335, nm2538774, nm2761554, nm0128050, nm0295835, nm0320824, nm0001294, nm2902914, nm0544114, nm3810229, nm0621783, nm0656528, nm0697362, nm0741627, nm0765490, nm0786219, nm7193419, nm1022998, nm0020022, nm3745520, nm0054667, nm0066848, nm0130913, nm0142622, nm11577452, nm0222164, nm0280234, nm0316225, nm0341896, nm0344899, nm0532032, nm0825705, nm0846712, nm12589386, nm0178785, nm0377223, nm3756977, nm0711905, nm3760592, nm0891558, nm1113541, nm0002021, nm14315657, nm0369458, nm0443611, nm0560857, nm0007186, nm2514969, nm0675810, nm14576241, nm1022063, nm0780962, nm3761581, nm12823796, nm0921722, nm0093664, nm3933700, nm0143810, nm10288822, nm0216340, nm0311155, nm3893609, nm0441502, nm2651175, nm0536249, nm1031882, nm1077993, nm0894579, nm0928492, nm0032002, nm0127253, nm0234502, nm0314561, nm0358096, nm0450279, nm13476030, nm1407152, nm2187535, nm2613492, nm1391726, nm1088321, nm12298192, nm2009323, nm0804772, nm1196850, nm0315418, nm14315871, nm0843708, nm0874753, nm0874997, nm0033469, nm10297032, nm2517965, nm2643156, nm0824026, nm2497672, nm0375484, nm0479514, nm0843423, nm4621014, nm14347237, nm2597218, nm4842725, nm0068847, nm0224570, nm0283700, nm0369524, nm12935818, nm3543298, nm0177774, nm0236244, nm0468089, nm1007829, nm0689225, nm3741368, nm1000287, nm0133411, nm1680352, nm0375789, nm2719466, nm1474612, nm1324103, nm0834529, nm0884952, nm17740250, nm0227460, nm0434019, nm1114447, nm0774217, nm3206364, nm0355239, nm1007185, nm1330846, nm0210114, nm0765683, nm0800319, nm0804770, nm2827798, nm2948487, nm0268711, nm1025065, nm0919815, nm0167994, nm2808172, nm0888937, nm0859436, nm2553818, nm1310399 |  |  |
| tt11404322 | nm17761498, nm6207727 | nm9504599, nm11212386, nm17833636 |  |  |
| tt12380288 | nm18618876 |  |  |  |
| tt15017986 | nm10273156, nm17762072 | nm7466077, nm16269167, nm16325580, nm10273156 |  |  |
| tt2130249 | nm4802745, nm18593495 |  |  |  |
| tt2289131 | nm17626952, nm9417033, nm0528381, nm5319124, nm9292847, nm11061032, nm2686865, nm3382694, nm6289192, nm17694282, nm4254378, nm2386041, nm3091467, nm4970436, nm8288691, nm6121912, nm2460433, nm0940657, nm8483469, nm4439198, nm3625807, nm8287602, nm12062608, nm11964084, nm8177348, nm14793765, nm17662185, nm3850757, nm9813766, nm5155109, nm11619610, nm1749539, nm6056434, nm6834295, nm9770218, nm4390649, nm5260166, nm4681656, nm5934321, nm2346983, nm4746742, nm0400529, nm8307713, nm4506394, nm0172736, nm4848801, nm4167299, nm3282137, nm7468135, nm4278352, nm8962050, nm9495951, nm17691683, nm17626951, nm1837183, nm8837305, nm16823605, nm3484507, nm14636930, nm3493263, nm3494426, nm6187588, nm9181068, nm4117635, nm17669548, nm17694280, nm6950393, nm9243047, nm8574969, nm8309886, nm8722988, nm6150785, nm9827825, nm9498156, nm15104066, nm10078737, nm7173579, nm8034112, nm7201851, nm17607421, nm10300335, nm7384368, nm11410889, nm6815184, nm3501272, nm17811166, nm2701005, nm1990517, nm9272749, nm4824489, nm17743273, nm9953658, nm8914821, nm4065690, nm8010827, nm17705924, nm3811943, nm3997068, nm8010828, nm7657146, nm17743276, nm6856224, nm2419195, nm8754975, nm1396934, nm0004342, nm11401789, nm0888231, nm1119798, nm10773919, nm2370588, nm17743271, nm10961186, nm2611753, nm6365977, nm8468608, nm4906045, nm17865137, nm3820289, nm1839358, nm2259283, nm17685508, nm17867025, nm5558984, nm5563957, nm17865135, nm3453283, nm3249937, nm3238220, nm0526325, nm2301412, nm0733941, nm3958872, nm3215397, nm17865131, nm4383739, nm17685507, nm17685505, nm0860973, nm5353054, nm3695750, nm12875340, nm4888030, nm17749929, nm17749928, nm4618012, nm17760255, nm4947837, nm17760252, nm8946100, nm5618638, nm17749927, nm1203846, nm4119661, nm17749924, nm8946099, nm3687471, nm5058837, nm4301160, nm7429292, nm5190169, nm2972759, nm2564355, nm2561414, nm0003789, nm10480618, nm17854223, nm17850650, nm3459234, nm17854222, nm0253320, nm17683191, nm2289516, nm17743958, nm17750906, nm1897814, nm17658415, nm7150055, nm6402138, nm17658409, nm3674899, nm17849813, nm17660077, nm17854230, nm5892508, nm17658028, nm17658027, nm1769088, nm1988856, nm0891315, nm2042850, nm17658413, nm1340293, nm3383114, nm4476748, nm4497617, nm5193093, nm5097596, nm17857070, nm17766192, nm16840428, nm4813087, nm17766193, nm17848385, nm4245387, nm17857335, nm1968580, nm0381116, nm17727319, nm7347709, nm3717153, nm13337255, nm1796302, nm1834967, nm11950745, nm2591451, nm0516858, nm1885310, nm17691685, nm17691690, nm6963154, nm17857071, nm1048392, nm4870743, nm9546093, nm3517154, nm17766194, nm5479260, nm17857069, nm17691688, nm10819467, nm5360866, nm17626949, nm0878047, nm13708845, nm17626950, nm14510548, nm4150219, nm17727110, nm8179161, nm17749103, nm3430130, nm5794645, nm6507716, nm17749096, nm17727108, nm4615452, nm7145549, nm2153943, nm6005406, nm1328045, nm5880602, nm12962212, nm6692017, nm10097073, nm17764793, nm2627751, nm13524692, nm5475120, nm1580272, nm13148874, nm7372348, nm17763228, nm9505739, nm2296717, nm8388590, nm10097078, nm17694281, nm3778729, nm4155746, nm11855722, nm4139956, nm9841018, nm3672668, nm5040728, nm10951970, nm5690810, nm8474868, nm12804527, nm7971657, nm3318144, nm13848327, nm6685995, nm17584019, nm4799896, nm7403409, nm17651756, nm17651757, nm7467985, nm8611713, nm1692204, nm3959525, nm3513250, nm6241292, nm3321827, nm3212274, nm17869008, nm1640481, nm2893786, nm17520070, nm1513476, nm17869009, nm6081046, nm6825438, nm9865570, nm6449714, nm5203383, nm17750763, nm6069578, nm5649411, nm17750766, nm9277206, nm10937889, nm11217406, nm3880161, nm3304743, nm17723236, nm11729375, nm8753192, nm3478796, nm6260319, nm10429350, nm2007236, nm8140693, nm17744704, nm0910539, nm12794188, nm17750762, nm17853743, nm17732113, nm5152278, nm6413110, nm11089571, nm17651211, nm5669325, nm14465096, nm8229931, nm17651212, nm11177195, nm6595795, nm12843597, nm8878602, nm17697200, nm15208225, nm17697201, nm4202666, nm17697199, nm3709883, nm17651208, nm11664641, nm6157905, nm17651209, nm4531489, nm2424543, nm0630277, nm11930774, nm5355576, nm17732114, nm5318218, nm3129506, nm17732117, nm7977941, nm17732115, nm8546639, nm9613575, nm7027976, nm16891768, nm5274109, nm17728500, nm4888265, nm17671161, nm17674402, nm8483774, nm1357028, nm10214831, nm17674292, nm7771127, nm6998458, nm4551666, nm3161917, nm13825092, nm2099597, nm17674291, nm17728505, nm17658080, nm4737626, nm5423916, nm17674400, nm11373267, nm17674404, nm8388459, nm17658081, nm17671160, nm17677900, nm17671159, nm0037867, nm7832615, nm13547508, nm3490121, nm3422121, nm10297327, nm5959833, nm13217155, nm6162262, nm5923960, nm17643312, nm17643311, nm3439470, nm10335329, nm13157373, nm11255666, nm16765619, nm2161382, nm9187287, nm10224720, nm9720075, nm9505979, nm7842953, nm17607420, nm17860249, nm6718420, nm11255665, nm17607423, nm6266711, nm4588730, nm17860254, nm17860250, nm1044110, nm6822215, nm17860251, nm3488663, nm14774943, nm7832253, nm3680976, nm17595818, nm4276126, nm17860248, nm17738413, nm17813202, nm17738415, nm11168968, nm7383352, nm17540002, nm5260214, nm17738416, nm1909266, nm8779963, nm11130409, nm17738414, nm1676581, nm6124629, nm1911741, nm17662184, nm5829631, nm17738408, nm0510576, nm17738409, nm14012050, nm17662320, nm17662321, nm2015221, nm5557665, nm5471372, nm5964951, nm5030072, nm17738412, nm6515132, nm1466688, nm3539983, nm12102993, nm11806088, nm17584536, nm11619894, nm3967702, nm17667980, nm12521500, nm11067068, nm2568309, nm17667976, nm13894297, nm14524952, nm17667975, nm6679213, nm17667979, nm12554037, nm15589672, nm17895352, nm11273908, nm10295783, nm11619297, nm13358814, nm4860666, nm6269453, nm2781317, nm17712705, nm3338081, nm4860365, nm4469320, nm9543277, nm18077943, nm17895895, nm2754096, nm5800302, nm3004893, nm2172048, nm5046582, nm16185484, nm18077835, nm10733939, nm16968523, nm6480539, nm7254602, nm4879351, nm1570721, nm10521524, nm11366943 | nm0400529, nm3247266, nm3707658, nm9865570, nm0238668, nm0755981, nm1581663, nm2301412, nm9814364, nm6081046, nm6069578, nm5649411, nm5356135, nm5669325, nm5406043, nm12843597, nm15470775, nm11930774, nm5355576, nm5116722, nm9498156, nm17607422, nm3422121, nm13217155, nm1749539, nm5923960, nm11255666, nm11255665, nm8962050, nm6822215, nm1990517, nm3501272, nm0154074, nm4860666, nm18077839, nm4860365, nm17202057, nm9813766, nm2754096, nm10573914 |  |  |
| tt30625284 | nm18605094 |  |  |  |
| tt31963046 | nm13142592, nm16524953, nm16524941, nm16088956, nm15995756, nm15992670, nm15992710, nm15995748, nm6702150, nm16848795, nm17465994, nm18624770, nm16848779, nm16863758, nm16766446, nm16867073, nm16766432, nm7757259, nm16863764, nm14956934, nm16895533, nm18606110, nm18483310, nm16763027, nm15989168, nm15989350, nm18572192, nm18617508, nm18486632, nm18467532, nm18356891, nm18419934, nm11775247, nm18512892, nm16878820, nm16880263, nm18357230, nm13714823, nm11173642, nm18404555 |  |  |  |

##### DQ05:knownForTitles - name_basics

_Orphan foreign key: at least one value of name_basics.knownForTitles has no parent row in title_basics.tconst. Showing 6 of 6 violating row(s)._

| nconst | primaryName | birthYear | deathYear | primaryProfession | knownForTitles | _cast_errors | _corrupt_record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nm16010739 | Jack Gray |  |  | actor, composer, music_department | tt33299234, tt33078672, tt32028906, tt33039259 |  |  |
| nm16077811 | Stanford Payne |  |  | casting_department, producer, director | tt37847945, tt41362328, tt37425713, tt41055466 |  |  |
| nm18694082 | Flaminio Bertoni |  |  |  | tt43667328 |  |  |
| nm18858818 | Abdul Rauf Rofi | 2011 |  | actor, producer, writer | tt44899441, tt44899307 |  |  |
| nm5410397 | Cagan Kayi |  |  | writer, producer, director | tt15435104, tt3111336, tt11775236, tt43004576 |  |  |
| nm6380170 | Edwin van der Walt |  |  | actor, director, producer | tt37847945, tt23061236, tt7385530, tt5185042 |  |  |

##### DQ05:nconst - title_principals

_Orphan foreign key: title_principals.nconst has no parent row in name_basics.nconst. Showing 10 of 8263 violating row(s)._

| tconst | ordering | nconst | category | job | characters | _cast_errors | _corrupt_record |
| --- | --- | --- | --- | --- | --- | --- | --- |
| tt0022647 | 10 | nm17757978 | actor |  | Hansel |  |  |
| tt0027126 | 5 | nm17757976 | actor |  | Stork |  |  |
| tt0027126 | 14 | nm17757973 | actress |  | Mrs. Skunk |  |  |
| tt0027126 | 15 | nm17757974 | actor |  | Snail |  |  |
| tt0027126 | 16 | nm17757977 | actor |  | Mr. Skunk |  |  |
| tt0029339 | 13 | nm17757980 | actress |  | Mice |  |  |
| tt0096014 | 2 | nm18615990 | actress |  |  |  |  |
| tt0117917 | 3 | nm17757689 | self |  | Self |  |  |
| tt0117917 | 4 | nm17757691 | self |  | Self |  |  |
| tt0117917 | 11 | nm17757708 | actor |  | Specialist |  |  |

##### DQ05:parentTconst - title_episode

_Orphan foreign key: title_episode.parentTconst has no parent row in title_basics.tconst. Showing 5 of 5 violating row(s)._

| tconst | parentTconst | seasonNumber | episodeNumber | _cast_errors | _corrupt_record |
| --- | --- | --- | --- | --- | --- |
| tt28611150 | tt28606619 |  |  |  |  |
| tt28638568 | tt28606619 |  |  |  |  |
| tt29195389 | tt28606619 |  |  |  |  |
| tt33366211 | tt28606619 |  |  |  |  |
| tt34954661 | tt28606619 |  |  |  |  |

##### DQ05:writers - title_crew

_Orphan foreign key: at least one value of title_crew.writers has no parent row in name_basics.nconst. Showing 10 of 812 violating row(s)._

| tconst | directors | writers | _cast_errors | _corrupt_record |
| --- | --- | --- | --- | --- |
| tt0041061 | nm0828720, nm0612322, nm0679013, nm0666777, nm0842611 | nm2731572, nm3367627, nm0027355, nm0035158, nm0035655, nm1664770, nm0049903, nm5483999, nm12085570, nm0057921, nm0062299, nm12085574, nm0063243, nm2764459, nm0068666, nm0071864, nm12085651, nm2467942, nm3754776, nm1089163, nm0088662, nm2759794, nm0001969, nm0104572, nm2753929, nm19112617, nm1503327, nm1563042, nm0121885, nm1709261, nm0130154, nm0139757, nm2762571, nm0146896, nm0002005, nm2759784, nm0167664, nm0168356, nm0169665, nm0171924, nm0172741, nm2418726, nm0236279, nm0177336, nm7065162, nm0001094, nm0204514, nm0205024, nm0205235, nm0208342, nm0219068, nm0002042, nm16848179, nm0234758, nm12085550, nm0238898, nm0241416, nm0243004, nm0245943, nm0089286, nm0251375, nm0254124, nm0254641, nm12085654, nm0254700, nm1910739, nm2725450, nm0262412, nm0266274, nm0001203, nm0269879, nm0277563, nm0277643, nm0280234, nm2479603, nm1499103, nm0295053, nm0300366, nm0311261, nm0313975, nm3297478, nm0325267, nm0330003, nm4768462, nm0344246, nm0357824, nm0369617, nm0370152, nm0370252, nm0371088, nm0371092, nm0371193, nm0371614, nm0371907, nm0374352, nm0376937, nm0381280, nm0384509, nm0385264, nm0396716, nm0408979, nm2664087, nm0414669, nm1097476, nm1709308, nm5087074, nm0437320, nm0439268, nm1713424, nm0456017, nm0457173, nm2837657, nm0492982, nm2753776, nm0497458, nm0500494, nm0504520, nm0507574, nm7954668, nm0972416, nm1038850, nm0523269, nm1195400, nm0531878, nm2759390, nm1713431, nm12085622, nm0569423, nm3477624, nm2723647, nm2715066, nm2720012, nm0597574, nm0606510, nm12085579, nm0612322, nm0616730, nm0626981, nm0628305, nm0632873, nm0640993, nm4716212, nm0650581, nm0666377, nm0670019, nm0681052, nm3570187, nm0000590, nm0689679, nm12085685, nm12085581, nm0701090, nm1190774, nm2499095, nm0721913, nm0722425, nm0723385, nm0731409, nm0732456, nm2764476, nm12085555, nm1494087, nm0738222, nm0741269, nm0750357, nm1709358, nm0764588, nm0768465, nm0776068, nm1914989, nm0783913, nm0785245, nm0789947, nm2760048, nm0795080, nm0795229, nm0799442, nm12085621, nm10678624, nm10673738, nm12085580, nm12346043, nm0823551, nm0824699, nm0828720, nm0829044, nm12346079, nm2420636, nm18371105, nm0848194, nm3379143, nm3379677, nm0871604, nm0000683, nm0899225, nm0908683, nm0909408, nm12085728, nm0909884, nm0919925, nm0920465, nm14150498, nm3381248, nm0930082, nm0938445, nm2950647, nm0940397, nm0409997, nm0957652 |  |  |
| tt0090442 | nm0384987, nm0651369, nm0277467 | nm1521750, nm1318225, nm18610673, nm1491922, nm2660866, nm0040720, nm9516340, nm2095561, nm3420197, nm0971746, nm2084549, nm6159910, nm18607060, nm7474229, nm5854064, nm2953057, nm18613146, nm6329680, nm1511409, nm8086450, nm0147700, nm17427821, nm3896381, nm1113275, nm18621928, nm3454882, nm0176781, nm7987602, nm1462941, nm2123957, nm6461162, nm18614523, nm18610909, nm3454559, nm0213017, nm1733297, nm6811657, nm1497217, nm12330109, nm9498197, nm1788125, nm18670041, nm0298279, nm6811658, nm18617880, nm2820957, nm0330911, nm2992620, nm0996106, nm3454654, nm0338425, nm0354907, nm18140130, nm0368188, nm0368977, nm3822716, nm7459550, nm12515372, nm3670216, nm0417141, nm0420746, nm18617829, nm8086538, nm1498331, nm9094069, nm18621331, nm1546012, nm9496356, nm1140275, nm1546014, nm0485712, nm0494812, nm1230595, nm1230596, nm18613831, nm0507612, nm2333332, nm8658232, nm12111517, nm3456043, nm4323518, nm1497233, nm18613145, nm18614207, nm6811659, nm3448273, nm0607328, nm1813311, nm18607142, nm1434273, nm0623279, nm12515413, nm0629298, nm7399310, nm0635712, nm0655154, nm18617943, nm0662571, nm0663773, nm7660411, nm18614524, nm18607059, nm0972432, nm0712390, nm6812851, nm7059350, nm0726978, nm9496357, nm0746816, nm18611267, nm1648401, nm18607042, nm3569081, nm0807364, nm1537763, nm10809131, nm0972447, nm0828962, nm0832329, nm0846422, nm1498281, nm2539521, nm8086461, nm0877805, nm18607058, nm0908148, nm3445384, nm10568014, nm6138781, nm3420471, nm3454606, nm18617482, nm1140125, nm18617483, nm18621447, nm0950034, nm1563984 |  |  |
| tt0445107 | nm1203430 | nm18597160, nm18643569, nm18643567, nm4765440, nm4102812, nm0419494, nm18597161, nm18643571, nm18643568 |  |  |
| tt0713891 | nm0828720 | nm19112617, nm0919925 |  |  |
| tt0863054 | nm3862710 | nm17846022, nm18076341, nm17796255, nm18052775, nm6210880, nm17861483, nm16959366, nm3115028, nm17897312, nm17783443, nm17796258, nm18136463, nm17809909, nm17804731, nm17755437, nm18140959, nm17755430, nm17937261, nm17922878, nm17880738, nm17809903, nm17770302, nm2217509, nm18048367, nm11918632, nm10386166, nm17981309, nm10383270, nm17754404, nm17908311, nm8023109, nm17944983, nm7610274, nm7517072, nm12614514, nm8813216, nm9043709, nm18148161, nm6503890, nm17925528, nm17864251, nm4315731, nm17835262, nm17784303, nm5414365, nm17780361, nm17798492, nm17754327, nm17756212, nm17996235, nm12337338, nm17850145, nm17754311, nm17932003, nm17898350, nm17754323, nm17922873, nm17788193, nm17935764, nm11192179, nm9429291, nm10576149, nm17825797, nm17835941, nm17796050, nm18028706, nm3655728, nm18156631, nm17782652, nm4104745, nm17754237, nm17932125, nm18028394, nm18118351, nm17749300, nm18052777, nm17738399, nm17756214, nm17756217, nm17756099, nm10355256, nm17818242, nm18088281, nm17824501, nm10383587, nm17754315, nm0389277, nm17754500, nm8606365, nm17910788, nm18169312, nm7838578, nm17770417, nm17931993, nm17881445, nm17754321, nm17848036, nm17754312, nm17821297, nm17754319, nm15433508, nm12248727, nm18084694, nm17796259, nm9392680, nm17846939, nm17755368, nm18226296, nm17790589, nm17756216, nm10047648, nm17796051, nm15410689, nm12372603, nm17794772, nm10383289, nm17775527, nm17842161, nm12248716, nm7982471, nm17754231, nm17812491, nm2091077, nm17777979, nm13502734, nm12485867, nm17749302, nm17908318, nm17754496, nm17778360, nm5201761, nm11966661, nm5053897, nm16424894, nm17904407, nm17932122, nm17802252, nm17816842, nm16973673, nm17864253, nm17926676, nm17755436, nm17749301, nm5258055, nm11818590, nm12248720, nm6265018, nm10385782, nm18023495, nm17770303, nm17754402, nm18129344, nm10224716, nm15961259, nm17796257, nm17770301, nm17784301, nm18124136, nm17770296, nm17822975, nm17977296, nm17854513, nm17794270, nm17919849, nm18104018, nm17754328, nm17738403, nm17804473, nm18105493, nm10798439, nm5074698, nm10072752, nm12230157, nm14951994, nm17792460, nm18003973, nm17788192, nm17856875, nm10383348, nm17770770, nm17938443, nm10352686, nm17969291, nm6837184, nm14805981, nm4699079, nm17754408, nm17754236, nm17788190, nm17903219, nm18012922, nm17756221, nm2815423, nm18060181, nm17908477, nm17754238, nm18119205, nm9952641, nm17988547, nm17784300, nm18004020, nm14312456, nm15754908, nm17947224, nm17754498, nm10729375, nm14101458, nm18267530, nm12614971, nm5194996, nm10911176, nm15336077, nm5032347, nm17832645, nm18070092, nm1351812, nm4401627, nm17790590, nm18122106, nm4011710, nm6660359, nm17900197, nm17861450, nm17832074, nm17818237, nm17794271, nm10489464, nm17771494, nm11979318, nm17792458, nm17804730, nm17846025, nm17754492, nm7156615, nm18028477, nm10381696, nm17931988, nm11026094, nm17794773, nm2507333, nm18052781, nm18028396, nm2354073, nm17954008, nm17809902, nm18122214, nm17755369, nm10383273, nm18023777, nm17749295, nm11073273, nm9108898, nm18026550, nm14271704, nm11493925, nm12256976, nm5371008, nm17770769, nm17867868, nm7074343, nm17797931, nm17809650, nm10362668, nm5558473, nm9103282, nm7662161, nm17794769, nm12264814, nm16973807, nm16013663, nm17832644, nm17138948, nm10362385, nm17796256, nm16525595, nm17932959, nm18088282, nm17771262, nm9975450, nm18228436, nm11726194, nm17920766, nm7544423 |  |  |
| tt10074050 | nm3250782, nm10570224, nm3385561 | nm16133104, nm16156984, nm15346629, nm11258509, nm0989197, nm9198297, nm17760645, nm10894311, nm2394938, nm16133105, nm10570224, nm14094839 |  |  |
| tt10474506 | nm8261855, nm10048334 | nm17755041 |  |  |
| tt1051724 | nm0706350 | nm18618911, nm1334208 |  |  |
| tt10706900 | nm10868136 | nm17758103 |  |  |
| tt1173239 | nm0651369 | nm0354907, nm0655154, nm0368188, nm18617482, nm18617483 |  |  |

##### DQ07 - title_basics

_startYear later than the reference year + max_future_years. Showing 3 of 3 violating row(s)._

| tconst | titleType | primaryTitle | originalTitle | isAdult | startYear | endYear | runtimeMinutes | genres | _cast_errors | _corrupt_record |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tt37368526 | tvMiniSeries | UEFA Euro 2032 | UEFA Euro 2032 | false | 2032 | 2032 |  | Sport |  |  |
| tt43255463 | movie | The Last Mourning: End of the Cycle | The Last Mourning: End of the Cycle | false | 2032 |  |  | Horror |  |  |
| tt5174640 | short | 100 Years | 100 Years | false | 2115 |  |  | Drama, Short |  |  |

##### DQ08 - title_basics

_runtimeMinutes <= 0 or above max_runtime_minutes. Showing 10 of 446 violating row(s)._

| tconst | titleType | primaryTitle | originalTitle | isAdult | startYear | endYear | runtimeMinutes | genres | _cast_errors | _corrupt_record |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tt0004052 | movie | The Hazards of Helen | The Hazards of Helen | false | 1914 |  | 1428 | Action |  |  |
| tt0096679 | tvSeries | Press Gang | Press Gang | false | 1989 | 1993 | 1290 | Comedy, Drama, Family |  |  |
| tt0140739 | tvSeries | Grafinya de Monsoro | Grafinya de Monsoro | false | 1997 |  | 1352 | Drama, History, Romance |  |  |
| tt0144722 | tvSeries | De kleine waarheid | De kleine waarheid | false | 1970 | 1972 | 1320 | Drama |  |  |
| tt0165127 | movie | Burning of the Red Lotus Temple | Huo shao hong lian si | false | 1928 |  | 1620 | Action, Drama, Fantasy |  |  |
| tt0179184 | movie | **** | **** | false | 1967 |  | 1500 | Drama |  |  |
| tt0188360 | tvSeries | Show of Hearts | Show of Hearts | false | 2015 |  | 1320 | Comedy |  |  |
| tt0190204 | tvSeries | Tokugawa Buraichô | Tokugawa Buraichô | false | 1992 |  | 1080 |  |  |  |
| tt0209734 | tvSeries | Capital Sin | Pecado Capital | false | 1975 | 1976 | 1800 | Drama, Romance |  |  |
| tt0228639 | tvMiniSeries | Nickellennium | Nickellennium | false | 1999 |  | 1440 | Documentary |  |  |

##### DQ14 - title_episode

_seasonNumber or episodeNumber <= 0 or non-numeric. Showing 10 of 7125 violating row(s)._

| tconst | parentTconst | seasonNumber | episodeNumber | _cast_errors | _corrupt_record |
| --- | --- | --- | --- | --- | --- |
| tt0056578 | tt0055663 | 1 | 0 |  |  |
| tt0059753 | tt0060028 | 1 | 0 |  |  |
| tt0063046 | tt0062568 | 1 | 0 |  |  |
| tt0064214 | tt0063875 | 1 | 0 |  |  |
| tt0064475 | tt0065303 | 1 | 0 |  |  |
| tt0064636 | tt0063927 | 1 | 0 |  |  |
| tt0064648 | tt0065317 | 1 | 0 |  |  |
| tt0064725 | tt0065327 | 1 | 0 |  |  |
| tt0065087 | tt0063955 | 1 | 0 |  |  |
| tt0065141 | tt0063928 | 1 | 0 |  |  |

#### Cleaning summary (bronze to silver)

##### Parameters

| parameter | value |
| --- | --- |
| reference_year | 2026 |
| quarantine_rules | DQ05:nconst, DQ05:parentTconst, DQ05:tconst, DQ05:titleId, DQ10, DQ15, DQ16 |
| duplicate_handling | identical rows sharing a primary key: one copy kept, others quarantined; conflicting rows: all quarantined |
| foreign_keys_checked_against | silver parent tables |
| silver_path | data/silver |
| quarantine_path | data/quarantine |

##### Rows before and after cleaning

| table | bronze_rows | silver_rows | quarantined_rows | pct_quarantined | silver_rows_with_flags | pct_silver_rows_with_flags |
| --- | --- | --- | --- | --- | --- | --- |
| name_basics | 15811387 | 15811387 | 0 | 0.0000 | 36 | 0.0002 |
| title_akas | 60385482 | 60385482 | 0 | 0.0000 | 0 | 0.0000 |
| title_basics | 12958477 | 12958477 | 0 | 0.0000 | 449 | 0.0035 |
| title_crew | 12958477 | 12958477 | 0 | 0.0000 | 1033 | 0.0080 |
| title_episode | 10030795 | 10030790 | 5 | 0.0000 | 7125 | 0.0710 |
| title_principals | 102738762 | 102730499 | 8263 | 0.0080 | 24901 | 0.0242 |
| title_ratings | 1731756 | 1731756 | 0 | 0.0000 | 0 | 0.0000 |

##### Quarantined rows per reason

| table | dq_reason | rows |
| --- | --- | --- |
| title_episode | DQ05:parentTconst | 5 |
| title_principals | DQ05:nconst | 8263 |

##### Silver rows per quality flag

| table | dq_flag | rows |
| --- | --- | --- |
| name_basics | DQ01 | 28 |
| name_basics | DQ02 | 2 |
| name_basics | DQ05:knownForTitles | 6 |
| title_basics | DQ07 | 3 |
| title_basics | DQ08 | 446 |
| title_crew | DQ05:directors | 419 |
| title_crew | DQ05:writers | 812 |
| title_episode | DQ14 | 7125 |
| title_principals | DQ03 | 23742 |
| title_principals | DQ04 | 1159 |

##### Deterministic corrections

| table | column | correction | values_set_to_null |
| --- | --- | --- | --- |
| name_basics | birthYear | birthYear after the reference year set to null | 0 |
| name_basics | deathYear | deathYear after the reference year set to null | 0 |
| title_basics | runtimeMinutes | runtimeMinutes <= 0 set to null | 4 |
| title_episode | episodeNumber | negative episodeNumber set to null | 0 |
| title_episode | seasonNumber | negative seasonNumber set to null | 0 |
| title_ratings | averageRating | averageRating outside [rating_min, rating_max] set to null | 0 |
| title_ratings | numVotes | numVotes <= 0 set to null | 0 |

<!-- AUTO:preparation:end -->

### Methodological Explanation

#### Methodology and why it was chosen

The pipeline is split into layers (`raw` → `bronze` → `silver`, plus a `quarantine` area). Each layer can be re-run and checked on its own.

- **Bronze ingestion.** We read the seven TSV files with an explicit schema in which every column is a string. Quoting is disabled and `\N` is left as it is. The result is written once to Parquet. Reading everything as text means nothing is converted silently before we have looked at it. A value that fails to cast would otherwise become a null, and we could not tell it apart from a value that is really missing. Quoting is disabled because some IMDb titles contain unbalanced `"` characters, which would merge lines together. We also count malformed lines (lines with the wrong number of fields). There were none in 216.6 M rows.
- **Missing-value profile.** For each of the 39 columns, we count Spark nulls, `\N`, empty strings, whitespace-only strings and empty arrays separately, in a single pass per table. Keeping the forms apart shows where the missing values come from. In this snapshot, every missing value is an IMDb `\N`: no column contains Spark nulls, empty strings, whitespace-only values or empty arrays.
- **Standardisation.** `\N`, empty and blank values become null. Columns are cast to their real types, and multi-valued columns (`genres`, `directors`, `knownForTitles`, `characters`, …) become `array<string>`. Values that cannot be cast are recorded in a `_cast_errors` column instead of being dropped. We use only native Spark functions, with no Python UDFs, so the job stays fast on 100 M+ rows.
- **Quality rules.** Each check is a declarative rule `(rule_id, table, description, condition)`, from DQ01 to DQ16. One generic engine evaluates them and returns the number of violations, the share of the table and a sample of 10 rows. Adding a rule is a one-line change. Foreign keys are checked with anti-joins.
- **Handling.** We treat two kinds of problems differently:
  - Rows that are *structurally* broken go to `data/quarantine/<table>/`, with a `dq_reason` column. This means a duplicate or missing primary key, or a fact row that points to a person or series that does not exist. These rows cannot be joined correctly. If we kept them in silver, they would cause silent losses or wrong counts later.
  - Rows that are *probably wrong but still usable* stay in silver. This covers cases such as death before birth, a credit after death, an extreme runtime or season 0. Each of these rows gets a `dq_flags` array that lists the rules it breaks, and each analysis decides whether to exclude it.

  The only value we change is a runtime ≤ 0, which we set to null (4 values), because such a duration has no meaning. We never impute.

The three layers reconcile exactly: 216,606,868 silver rows + 8,268 quarantined rows = 216,615,136 bronze rows.

Everything had to run on a 16 GB laptop, with about 10 GB available to Docker. Converting to Parquet once means later jobs read only the columns they need, in compressed form, instead of parsing gzipped TSV again. Our first cleaning run on `title_principals` (102 M rows) ran out of native memory. We then lowered the settings to `local[4]` with a 4 GB driver and 64 shuffle partitions (with AQE), and used smaller Parquet batches.

#### Alternatives considered and trade-offs

- **Schema inference** (`inferSchema`): simpler, but it costs an extra full pass over the data, and `\N` would push numeric columns to strings anyway. We chose explicit schemas, defined once in `common/schemas.py`.
- **Dropping invalid rows**: silver would look cleaner, but we would lose information and the row counts would no longer reconcile. Quarantine keeps every rejected row together with its reason.
- **Imputation** (e.g. median runtime per genre, estimated birth years): this fills gaps by inventing values, and those values would then feed the exploration (outliers in Q1, career lengths in Q7). The missing values are concentrated in columns we barely use, so we would have gained little and risked a lot.
- **Correcting rows by hand** (e.g. the 28 cases of death before birth): not reproducible, and we cannot know which of the two years is wrong. The sample also shows that most of these rows are not real errors: they are ancient authors such as Aeschylus, Homer or Virgil, whose BC dates are stored as positive years.
- **pandas**: not realistic for `title_principals` and `title_akas` with 16 GB of RAM.

The cost of flagging rather than deleting is that downstream queries must remember to filter on `dq_flags` when it matters.

### Key takeaways

- IMDb is structurally clean: no malformed lines, no duplicate keys, and only 8,268 rows (0.004 %) had to be quarantined. Almost all of them (8,263) are principals pointing to a person who is missing from `name.basics`.
- Missing values are concentrated in a few columns: `title_akas.attributes` (99.5 %), `endYear` (98.7 %), `deathYear` (98.3 %), `birthYear` (95.7 %) and `principals.job` (80.7 %). `endYear` and `deathYear` are mostly empty for normal reasons (ongoing series, living people). However, `birthYear` is missing for 96 % of people, which limits any age-based analysis.
- Logical errors are rare but real: 23,742 credits more than 5 years after death (archive footage, writers and composers excluded), 1,159 credits before birth (all composers on silent films in the sample), 446 extreme runtimes and 7,125 episodes with a season or episode number ≤ 0. These are small numbers compared with the table sizes, so flagging them is enough.
- A flag is not a verdict. DQ02 flags Jeanne Calment, who really lived to 122, and DQ01 mostly flags ancient authors with BC dates. Deleting these rows would have removed correct data.

## 2. Data Exploration

### Q1. Runtime outliers by genre

#### Results

<!-- AUTO:q1:start -->

##### Q1 - Feature films with a runtime notably different from their genre

###### Parameters

| parameter | value |
| --- | --- |
| feature_film.title_types | movie |
| feature_film.min_runtime_minutes | 40 |
| feature_film.include_adult | false |
| z_threshold | 2 |
| iqr_multiplier | 1.5 |
| min_films_per_genre | 30 |
| top_per_genre | 20 |
| outlier_rule | abs(z_score) > z_threshold OR runtime outside the IQR fences |
| feature_films | 456414 |
| outlier_film_genre_pairs | 35557 |
| outlier_distinct_films | 24177 |

###### Runtime distribution and outliers per genre

| genre | n_films | analysed | mean_runtime | std_runtime | q1 | median | q3 | lower_fence | upper_fence | n_outliers | pct_outliers | n_longer | n_shorter | n_zscore_and_iqr | n_zscore_only | n_iqr_only |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Action | 40364 | true | 101.21 | 33.75 | 85.00 | 94.00 | 113.00 | 43.00 | 155.00 | 1892 | 4.69 | 1884 | 8 | 841 | 0 | 1051 |
| Adventure | 24024 | true | 93.01 | 30.58 | 79.00 | 90.00 | 101.00 | 46.00 | 134.00 | 1466 | 6.10 | 1311 | 155 | 632 | 0 | 834 |
| Animation | 8331 | true | 82.68 | 26.79 | 68.00 | 81.00 | 93.00 | 30.50 | 130.50 | 221 | 2.65 | 221 | 0 | 175 | 0 | 46 |
| Biography | 16107 | true | 89.22 | 29.38 | 69.00 | 88.00 | 104.00 | 16.50 | 156.50 | 469 | 2.91 | 469 | 0 | 324 | 145 | 0 |
| Comedy | 95772 | true | 93.30 | 28.74 | 82.00 | 91.00 | 102.00 | 52.00 | 132.00 | 7237 | 7.56 | 4620 | 2617 | 1613 | 0 | 5624 |
| Crime | 34410 | true | 95.70 | 25.60 | 83.00 | 93.00 | 105.00 | 50.00 | 138.00 | 2101 | 6.11 | 1767 | 334 | 1188 | 0 | 913 |
| Documentary | 116181 | true | 78.04 | 223.43 | 57.00 | 74.00 | 90.00 | 7.50 | 139.50 | 2079 | 1.79 | 2079 | 0 | 58 | 0 | 2021 |
| Drama | 196130 | true | 96.10 | 37.00 | 82.00 | 93.00 | 107.00 | 44.50 | 144.50 | 8707 | 4.44 | 8656 | 51 | 1964 | 0 | 6743 |
| Family | 15956 | true | 92.26 | 31.42 | 77.00 | 90.00 | 102.00 | 39.50 | 139.50 | 885 | 5.55 | 885 | 0 | 329 | 0 | 556 |
| Fantasy | 12594 | true | 94.06 | 31.90 | 80.00 | 91.00 | 104.00 | 44.00 | 140.00 | 514 | 4.08 | 511 | 3 | 237 | 0 | 277 |
| Film-Noir | 878 | true | 81.87 | 13.76 | 71.00 | 81.50 | 91.00 | 41.00 | 121.00 | 31 | 3.53 | 28 | 3 | 3 | 28 | 0 |
| Game-Show | 7 | false | 79.57 | 35.36 | 56.00 | 67.00 | 88.50 | 7.25 | 137.25 | 0 | 0.00 | 0 | 0 | 0 | 0 | 0 |
| History | 13637 | true | 94.28 | 52.86 | 72.00 | 90.00 | 108.00 | 18.00 | 162.00 | 419 | 3.07 | 419 | 0 | 143 | 0 | 276 |
| Horror | 30559 | true | 88.66 | 22.27 | 79.00 | 88.00 | 97.00 | 52.00 | 124.00 | 2064 | 6.75 | 1152 | 912 | 707 | 0 | 1357 |
| Music | 13979 | true | 88.43 | 57.66 | 68.00 | 87.00 | 100.00 | 20.00 | 148.00 | 385 | 2.75 | 385 | 0 | 97 | 0 | 288 |
| Musical | 8499 | true | 100.03 | 33.32 | 82.00 | 94.00 | 111.00 | 38.50 | 154.50 | 489 | 5.75 | 489 | 0 | 240 | 0 | 249 |
| Mystery | 16427 | true | 94.39 | 50.44 | 81.00 | 92.00 | 105.00 | 45.00 | 141.00 | 496 | 3.02 | 492 | 4 | 52 | 0 | 444 |
| News | 1409 | true | 77.62 | 32.19 | 60.00 | 75.00 | 88.00 | 18.00 | 130.00 | 28 | 1.99 | 28 | 0 | 27 | 0 | 1 |
| Reality-TV | 297 | true | 92.07 | 85.20 | 64.00 | 90.00 | 96.00 | 16.00 | 144.00 | 13 | 4.38 | 13 | 0 | 2 | 0 | 11 |
| Romance | 42197 | true | 99.16 | 25.05 | 85.00 | 96.00 | 110.00 | 47.50 | 147.50 | 2252 | 5.34 | 1984 | 268 | 1987 | 82 | 183 |
| Sci-Fi | 9777 | true | 91.23 | 30.47 | 79.00 | 90.00 | 100.00 | 47.50 | 131.50 | 588 | 6.01 | 415 | 173 | 146 | 0 | 442 |
| Sport | 6812 | true | 88.90 | 37.39 | 71.00 | 90.00 | 100.00 | 27.50 | 143.50 | 184 | 2.70 | 184 | 0 | 98 | 0 | 86 |
| Talk-Show | 102 | true | 88.08 | 33.71 | 60.00 | 81.50 | 116.50 | -24.75 | 201.25 | 5 | 4.90 | 5 | 0 | 0 | 5 | 0 |
| Thriller | 34052 | true | 96.11 | 21.75 | 85.00 | 93.00 | 105.00 | 55.00 | 135.00 | 2526 | 7.42 | 1732 | 794 | 2092 | 0 | 434 |
| War | 8050 | true | 94.75 | 31.25 | 80.00 | 92.00 | 105.00 | 42.50 | 142.50 | 358 | 4.45 | 357 | 1 | 217 | 0 | 141 |
| Western | 6353 | true | 76.55 | 28.74 | 57.00 | 70.00 | 90.00 | 7.50 | 139.50 | 148 | 2.33 | 148 | 0 | 133 | 15 | 0 |

###### Top 20 outliers per genre (by absolute z-score)

_Showing 478 of 35557 rows_

| genre | tconst | primaryTitle | startYear | runtimeMinutes | genre_mean_runtime | z_score | method | direction | rank_in_genre |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Action | tt7321476 | h36: | 2017 | 2160 | 101.21 | 61.00 | zscore+iqr | longer | 1 |
| Action | tt0165127 | Burning of the Red Lotus Temple | 1928 | 1620 | 101.21 | 45.00 | zscore+iqr | longer | 2 |
| Action | tt45643419 | Ooio Aifujairea: Lifedesign | 2025 | 1440 | 101.21 | 39.66 | zscore+iqr | longer | 3 |
| Action | tt0004052 | The Hazards of Helen | 1914 | 1428 | 101.21 | 39.31 | zscore+iqr | longer | 4 |
| Action | tt0131597 | Split | 2004 | 700 | 101.21 | 17.74 | zscore+iqr | longer | 5 |
| Action | tt12669540 | Marathon Wars |  | 600 | 101.21 | 14.78 | zscore+iqr | longer | 6 |
| Action | tt39392193 | The Longest Movie on Earth!?: The Narwallus Movie! | 2016 | 600 | 101.21 | 14.78 | zscore+iqr | longer | 7 |
| Action | tt37937538 | Pedazo del Alma | 2024 | 540 | 101.21 | 13.00 | zscore+iqr | longer | 8 |
| Action | tt42728310 | Cinematic Carnage: The Movie | 2026 | 486 | 101.21 | 11.40 | zscore+iqr | longer | 9 |
| Action | tt0006206 | Les Vampires | 1915 | 421 | 101.21 | 9.47 | zscore+iqr | longer | 10 |
| Action | tt0009204 | The House of Hate | 1918 | 410 | 101.21 | 9.15 | zscore+iqr | longer | 11 |
| Action | tt0006917 | Liberty | 1916 | 400 | 101.21 | 8.85 | zscore+iqr | longer | 12 |
| Action | tt0007932 | The Fatal Ring | 1917 | 400 | 101.21 | 8.85 | zscore+iqr | longer | 13 |
| Action | tt36375509 | Los Monjes Guerreros De Zardak | 2025 | 397 | 101.21 | 8.76 | zscore+iqr | longer | 14 |
| Action | tt0337998 | Ek Hindustani | 2003 | 370 | 101.21 | 7.96 | zscore+iqr | longer | 15 |
| Action | tt0045382 | Commando Cody: Sky Marshal of the Universe | 1953 | 361 | 101.21 | 7.70 | zscore+iqr | longer | 16 |
| Action | tt0008353 | The Mystery Ship | 1917 | 360 | 101.21 | 7.67 | zscore+iqr | longer | 17 |
| Action | tt0009304 | The Lion's Claws | 1918 | 360 | 101.21 | 7.67 | zscore+iqr | longer | 18 |
| Action | tt0010361 | The Lion Man | 1919 | 360 | 101.21 | 7.67 | zscore+iqr | longer | 19 |
| Action | tt0011367 | King of the Circus | 1920 | 360 | 101.21 | 7.67 | zscore+iqr | longer | 20 |
| Adventure | tt45643419 | Ooio Aifujairea: Lifedesign | 2025 | 1440 | 93.01 | 44.05 | zscore+iqr | longer | 1 |
| Adventure | tt39392193 | The Longest Movie on Earth!?: The Narwallus Movie! | 2016 | 600 | 93.01 | 16.58 | zscore+iqr | longer | 2 |
| Adventure | tt21638058 | Fireside Reading of Dracula | 2022 | 565 | 93.01 | 15.43 | zscore+iqr | longer | 3 |
| Adventure | tt5452954 | In Course of the Miraculous | 2016 | 540 | 93.01 | 14.62 | zscore+iqr | longer | 4 |
| Adventure | tt42728310 | Cinematic Carnage: The Movie | 2026 | 486 | 93.01 | 12.85 | zscore+iqr | longer | 5 |
| Adventure | tt4842296 | A Lullaby to the Sorrowful Mystery | 2016 | 485 | 93.01 | 12.82 | zscore+iqr | longer | 6 |
| Adventure | tt0003675 | The Beloved Adventurer | 1914 | 450 | 93.01 | 11.67 | zscore+iqr | longer | 7 |
| Adventure | tt21636390 | Fireside Reading of Black Beauty | 2022 | 447 | 93.01 | 11.58 | zscore+iqr | longer | 8 |
| Adventure | tt0005005 | The Broken Coin | 1915 | 440 | 93.01 | 11.35 | zscore+iqr | longer | 9 |
| Adventure | tt21637774 | Fireside Reading of Peter Pan | 2022 | 425 | 93.01 | 10.86 | zscore+iqr | longer | 10 |
| Adventure | tt0006206 | Les Vampires | 1915 | 421 | 93.01 | 10.73 | zscore+iqr | longer | 11 |
| Adventure | tt0009701 | Tih Minh | 1918 | 418 | 93.01 | 10.63 | zscore+iqr | longer | 12 |
| Adventure | tt0281305 | Tsigni pitsisa | 1983 | 406 | 93.01 | 10.24 | zscore+iqr | longer | 13 |
| Adventure | tt0006917 | Liberty | 1916 | 400 | 93.01 | 10.04 | zscore+iqr | longer | 14 |
| Adventure | tt21285620 | Fireside Reading of My Man Jeeves | 2022 | 393 | 93.01 | 9.81 | zscore+iqr | longer | 15 |
| Adventure | tt0008371 | The New Mission of Judex | 1917 | 374 | 93.01 | 9.19 | zscore+iqr | longer | 16 |
| Adventure | tt0045382 | Commando Cody: Sky Marshal of the Universe | 1953 | 361 | 93.01 | 8.76 | zscore+iqr | longer | 17 |
| Adventure | tt0008353 | The Mystery Ship | 1917 | 360 | 93.01 | 8.73 | zscore+iqr | longer | 18 |
| Adventure | tt0009304 | The Lion's Claws | 1918 | 360 | 93.01 | 8.73 | zscore+iqr | longer | 19 |
| Adventure | tt0010361 | The Lion Man | 1919 | 360 | 93.01 | 8.73 | zscore+iqr | longer | 20 |
| Animation | tt39246012 | Tom and Jerry: The Golden Era Anthology | 1958 | 817 | 82.68 | 27.41 | zscore+iqr | longer | 1 |
| Animation | tt20721834 | Disappeared Quipu | 2018 | 490 | 82.68 | 15.21 | zscore+iqr | longer | 2 |
| Animation | tt38809606 | The Long Walk to Nowhere | 2025 | 420 | 82.68 | 12.59 | zscore+iqr | longer | 3 |
| Animation | tt40593286 | The Crown | 2024 | 381 | 82.68 | 11.14 | zscore+iqr | longer | 4 |
| Animation | tt39484983 | Turning Zone | 2025 | 360 | 82.68 | 10.35 | zscore+iqr | longer | 5 |
| Animation | tt6709832 | Painting | 2017 | 360 | 82.68 | 10.35 | zscore+iqr | longer | 6 |
| Animation | tt6541996 | Dream Big - The Boovie | 2015 | 346 | 82.68 | 9.83 | zscore+iqr | longer | 7 |
| Animation | tt20870494 | Glitchtale the Movie (Season 2 Compilation) | 2022 | 338 | 82.68 | 9.53 | zscore+iqr | longer | 8 |
| Animation | tt32378695 | The Seagull on the Sims 4 | 2020 | 318 | 82.68 | 8.78 | zscore+iqr | longer | 9 |
| Animation | tt33095704 | Snow White's Storytime: The Wishing-Stone Stories | 2024 | 296 | 82.68 | 7.96 | zscore+iqr | longer | 10 |
| Animation | tt15505056 | The Clouts EP5 - That Little Itch | 2020 | 294 | 82.68 | 7.89 | zscore+iqr | longer | 11 |
| Animation | tt37340747 | Buddha - Thus Have I Heard | 2012 | 288 | 82.68 | 7.66 | zscore+iqr | longer | 12 |
| Animation | tt9909938 | Xenosaga Episode 1: Der Wille Zur Macht | 2005 | 288 | 82.68 | 7.66 | zscore+iqr | longer | 13 |
| Animation | tt13334482 | Distracted Blueberry | 2019 | 273 | 82.68 | 7.10 | zscore+iqr | longer | 14 |
| Animation | tt26628514 | Epletreet | 2013 | 265 | 82.68 | 6.81 | zscore+iqr | longer | 15 |
| Animation | tt10462138 | A Certain Magical Pimpdex: Extended Edition | 2019 | 263 | 82.68 | 6.73 | zscore+iqr | longer | 16 |
| Animation | tt28950991 | Ah My Goddess: Marller Gets a Spinoff Sailor Moon vs Jigsaw | 2021 | 257 | 82.68 | 6.51 | zscore+iqr | longer | 17 |
| Animation | tt7328912 | Star Trek III: Redemption | 2013 | 252 | 82.68 | 6.32 | zscore+iqr | longer | 18 |
| Animation | tt39049541 | Kamen Rider Super King's Knight Legend Movie Third | 2026 | 248 | 82.68 | 6.17 | zscore+iqr | longer | 19 |
| Animation | tt9591836 | The Greatest Adventure: The Book of Dragons | 2018 | 244 | 82.68 | 6.02 | zscore+iqr | longer | 20 |
| Biography | tt47723346 | The Steps: A Memoir | 2026 | 542 | 89.22 | 15.41 | zscore+iqr | longer | 1 |
| Biography | tt5275892 | O.J.: Made in America | 2016 | 467 | 89.22 | 12.86 | zscore+iqr | longer | 2 |
| Biography | tt30576841 | Et barns liv | 1999 | 445 | 89.22 | 12.11 | zscore+iqr | longer | 3 |
| Biography | tt21867090 | AA Signature: Aquirax. Ongaku hihyôka Aida Akira | 2006 | 443 | 89.22 | 12.04 | zscore+iqr | longer | 4 |
| Biography | tt0076147 | Hitler: A Film from Germany | 1977 | 442 | 89.22 | 12.01 | zscore+iqr | longer | 5 |
| Biography | tt43704232 | Joie de vivre | 2026 | 435 | 89.22 | 11.77 | zscore+iqr | longer | 6 |
| Biography | tt7516648 | Nation and Destiny 1-4: Choe Hyon Dok | 1992 | 378 | 89.22 | 9.83 | zscore+iqr | longer | 7 |
| Biography | tt31613235 | Interviews with Abdelkrim Baba Aïssa | 2024 | 374 | 89.22 | 9.69 | zscore+iqr | longer | 8 |
| Biography | tt35887598 | Why We Can't Wait | 1964 | 365 | 89.22 | 9.39 | zscore+iqr | longer | 9 |
| Biography | tt0498915 | Life of St. Paul Series | 1949 | 360 | 89.22 | 9.22 | zscore+iqr | longer | 10 |
| Biography | tt3526810 | Adolf Hitler: The Greatest Story Never Told | 2013 | 350 | 89.22 | 8.88 | zscore+iqr | longer | 11 |
| Biography | tt6541996 | Dream Big - The Boovie | 2015 | 346 | 89.22 | 8.74 | zscore+iqr | longer | 12 |
| Biography | tt0018192 | Napoleon | 1927 | 330 | 89.22 | 8.20 | zscore+iqr | longer | 13 |
| Biography | tt0318415 | Mahatma: Life of Gandhi, 1869-1948 | 1968 | 330 | 89.22 | 8.20 | zscore+iqr | longer | 14 |
| Biography | tt30783313 | Eksperimentet |  | 330 | 89.22 | 8.20 | zscore+iqr | longer | 15 |
| Biography | tt43704443 | Life of Jorge Luis Borges | 2026 | 330 | 89.22 | 8.20 | zscore+iqr | longer | 16 |
| Biography | tt0056937 | Cleopatra | 1963 | 320 | 89.22 | 7.85 | zscore+iqr | longer | 17 |
| Biography | tt8372544 | Name Dropping |  | 300 | 89.22 | 7.17 | zscore+iqr | longer | 18 |
| Biography | tt8696742 | The Orson Bean Show |  | 300 | 89.22 | 7.17 | zscore+iqr | longer | 19 |
| Biography | tt46062820 | Remember Me | 2026 | 299 | 89.22 | 7.14 | zscore+iqr | longer | 20 |
| Comedy | tt5136218 | London EC1 | 2015 | 5460 | 93.30 | 186.73 | zscore+iqr | longer | 1 |
| Comedy | tt1885195 | Azgrab: The Documentary | 2011 | 1669 | 93.30 | 54.82 | zscore+iqr | longer | 2 |
| Comedy | tt45643419 | Ooio Aifujairea: Lifedesign | 2025 | 1440 | 93.30 | 46.86 | zscore+iqr | longer | 3 |
| Comedy | tt8677246 | Bullfighting Memories | 2017 | 1100 | 93.30 | 35.03 | zscore+iqr | longer | 4 |
| Comedy | tt19711676 | Kahrlton Heights North | 2022 | 900 | 93.30 | 28.07 | zscore+iqr | longer | 5 |
| Comedy | tt33336291 | Phonetag | 2023 | 659 | 93.30 | 19.68 | zscore+iqr | longer | 6 |
| Comedy | tt42728310 | Cinematic Carnage: The Movie | 2026 | 486 | 93.30 | 13.66 | zscore+iqr | longer | 7 |
| Comedy | tt7017462 | Till We Age | 2016 | 480 | 93.30 | 13.45 | zscore+iqr | longer | 8 |
| Comedy | tt45800099 | The Big Tent | 2026 | 475 | 93.30 | 13.28 | zscore+iqr | longer | 9 |
| Comedy | tt0270523 | The Movie Orgy | 1968 | 420 | 93.30 | 11.37 | zscore+iqr | longer | 10 |
| Comedy | tt0499428 | The Cloth Peddler | 1917 | 420 | 93.30 | 11.37 | zscore+iqr | longer | 11 |
| Comedy | tt37539046 | Schmuck Amuck | 2024 | 420 | 93.30 | 11.37 | zscore+iqr | longer | 12 |
| Comedy | tt39718781 | Rotate | 2026 | 420 | 93.30 | 11.37 | zscore+iqr | longer | 13 |
| Comedy | tt27696461 | Videobook: A Clockwork Orange | 2023 | 396 | 93.30 | 10.53 | zscore+iqr | longer | 14 |
| Comedy | tt0231586 | De filosoof van Haeghem | 1967 | 385 | 93.30 | 10.15 | zscore+iqr | longer | 15 |
| Comedy | tt7740334 | Hogwash | 2023 | 382 | 93.30 | 10.05 | zscore+iqr | longer | 16 |
| Comedy | tt0257420 | Babel - lettre à mes amis restés en Belgique | 1991 | 380 | 93.30 | 9.98 | zscore+iqr | longer | 17 |
| Comedy | tt0346596 | Berserk in the Antarctic | 2000 | 360 | 93.30 | 9.28 | zscore+iqr | longer | 18 |
| Comedy | tt10524318 | Make Love! The Bruce Campbell Way | 2005 | 360 | 93.30 | 9.28 | zscore+iqr | longer | 19 |
| Comedy | tt2769354 | Ringsend |  | 360 | 93.30 | 9.28 | zscore+iqr | longer | 20 |
| Crime | tt9900018 | His Last Stand |  | 990 | 95.70 | 34.93 | zscore+iqr | longer | 1 |
| Crime | tt39327389 | Lemons | 2026 | 751 | 95.70 | 25.60 | zscore+iqr | longer | 2 |
| Crime | tt0131597 | Split | 2004 | 700 | 95.70 | 23.61 | zscore+iqr | longer | 3 |
| Crime | tt3201284 | Are We Famous Yet??? |  | 625 | 95.70 | 20.68 | zscore+iqr | longer | 4 |
| Crime | tt38895289 | Steal my heart | 2023 | 530 | 95.70 | 16.97 | zscore+iqr | longer | 5 |
| Crime | tt0843515 | Heremias, Book One: The Legend of the Lizard Princess | 2006 | 519 | 95.70 | 16.54 | zscore+iqr | longer | 6 |
| Crime | tt0009905 | Barrabas | 1919 | 489 | 95.70 | 15.36 | zscore+iqr | longer | 7 |
| Crime | tt5275892 | O.J.: Made in America | 2016 | 467 | 95.70 | 14.50 | zscore+iqr | longer | 8 |
| Crime | tt0006206 | Les Vampires | 1915 | 421 | 95.70 | 12.71 | zscore+iqr | longer | 9 |
| Crime | tt32514957 | Maximum Pain - a Max Payne Memoir | 2022 | 416 | 95.70 | 12.51 | zscore+iqr | longer | 10 |
| Crime | tt27696461 | Videobook: A Clockwork Orange | 2023 | 396 | 95.70 | 11.73 | zscore+iqr | longer | 11 |
| Crime | tt10407026 | Serious Serial Killers | 2012 | 388 | 95.70 | 11.42 | zscore+iqr | longer | 12 |
| Crime | tt0209123 | La maison du mystère | 1923 | 382 | 95.70 | 11.18 | zscore+iqr | longer | 13 |
| Crime | tt2194569 | Florentina Hubaldo, CTE | 2012 | 360 | 95.70 | 10.32 | zscore+iqr | longer | 14 |
| Crime | tt2769354 | Ringsend |  | 360 | 95.70 | 10.32 | zscore+iqr | longer | 15 |
| Crime | tt41542814 | Digital Arrest | 2026 | 327 | 95.70 | 9.04 | zscore+iqr | longer | 16 |
| Crime | tt0027365 | The Black Coin | 1936 | 323 | 95.70 | 8.88 | zscore+iqr | longer | 17 |
| Crime | tt1954470 | Gangs of Wasseypur | 2012 | 321 | 95.70 | 8.80 | zscore+iqr | longer | 18 |
| Crime | tt0193571 | I topi grigi | 1918 | 320 | 95.70 | 8.76 | zscore+iqr | longer | 19 |
| Crime | tt0303720 | Batang West Side | 2001 | 315 | 95.70 | 8.57 | zscore+iqr | longer | 20 |
| Documentary | tt8273150 | Logistics | 2012 | 51420 | 78.04 | 229.79 | zscore+iqr | longer | 1 |
| Documentary | tt3854496 | Ambiancé | 2020 | 43200 | 78.04 | 193.00 | zscore+iqr | longer | 2 |
| Documentary | tt12277054 | Carnets Filmés (Liste Complète) | 2019 | 28643 | 78.04 | 127.85 | zscore+iqr | longer | 3 |
| Documentary | tt2659636 | Modern Times Forever | 2011 | 14400 | 78.04 | 64.10 | zscore+iqr | longer | 4 |
| Documentary | tt2355497 | Beijing 2003 | 2004 | 9000 | 78.04 | 39.93 | zscore+iqr | longer | 5 |
| Documentary | tt5068890 | Hunger! | 2015 | 6000 | 78.04 | 26.50 | zscore+iqr | longer | 6 |
| Documentary | tt0284020 | The Cure for Insomnia | 1987 | 5220 | 78.04 | 23.01 | zscore+iqr | longer | 7 |
| Documentary | tt5135246 | Saynatakuna: Masks | 2013 | 2905 | 78.04 | 12.65 | zscore+iqr | longer | 8 |
| Documentary | tt0342707 | The Longest Most Meaningless Movie in the World | 1970 | 2880 | 78.04 | 12.54 | zscore+iqr | longer | 9 |
| Documentary | tt1866307 | World Peace & Prayer Day | 2011 | 2400 | 78.04 | 10.39 | zscore+iqr | longer | 10 |
| Documentary | tt10958742 | Five-Year Diary | 1982 | 2160 | 78.04 | 9.32 | zscore+iqr | longer | 11 |
| Documentary | tt38066726 | The Freedom of Uselessness | 2025 | 2000 | 78.04 | 8.60 | zscore+iqr | longer | 12 |
| Documentary | tt1823692 | Hollywood East | 2010 | 1800 | 78.04 | 7.71 | zscore+iqr | longer | 13 |
| Documentary | tt32187732 | 24 | 2024 | 1464 | 78.04 | 6.20 | zscore+iqr | longer | 14 |
| Documentary | tt1447786 | Grandmother Martha | 1996 | 1452 | 78.04 | 6.15 | zscore+iqr | longer | 15 |
| Documentary | tt16385264 | Gondwana | 2022 | 1440 | 78.04 | 6.10 | zscore+iqr | longer | 16 |
| Documentary | tt38146238 | Sky TV | 1966 | 1440 | 78.04 | 6.10 | zscore+iqr | longer | 17 |
| Documentary | tt32701008 | L'Afrique aux Portes de Paris | 2024 | 1400 | 78.04 | 5.92 | zscore+iqr | longer | 18 |
| Documentary | tt1277455 | A Time to Stir | 2018 | 1320 | 78.04 | 5.56 | zscore+iqr | longer | 19 |
| Documentary | tt7529390 | Pakistan: Education and Women | 2016 | 1184 | 78.04 | 4.95 | zscore+iqr | longer | 20 |
| Drama | tt5068890 | Hunger! | 2015 | 6000 | 96.10 | 159.57 | zscore+iqr | longer | 1 |
| Drama | tt1806963 | Matrjoschka | 2006 | 5700 | 96.10 | 151.46 | zscore+iqr | longer | 2 |
| Drama | tt5136218 | London EC1 | 2015 | 5460 | 96.10 | 144.97 | zscore+iqr | longer | 3 |
| Drama | tt3837350 | A 2nd generation film | 2013 | 3077 | 96.10 | 80.57 | zscore+iqr | longer | 4 |
| Drama | tt0342707 | The Longest Most Meaningless Movie in the World | 1970 | 2880 | 96.10 | 75.24 | zscore+iqr | longer | 5 |
| Drama | tt0387271 | A Twist of Fate | 1970 | 1970 | 96.10 | 50.65 | zscore+iqr | longer | 6 |
| Drama | tt0165127 | Burning of the Red Lotus Temple | 1928 | 1620 | 96.10 | 41.19 | zscore+iqr | longer | 7 |
| Drama | tt5942280 | The Nothing Movie | 2016 | 1559 | 96.10 | 39.54 | zscore+iqr | longer | 8 |
| Drama | tt0179184 | **** | 1967 | 1500 | 96.10 | 37.94 | zscore+iqr | longer | 9 |
| Drama | tt2008009 | The Clock | 2010 | 1440 | 96.10 | 36.32 | zscore+iqr | longer | 10 |
| Drama | tt35509411 | Our First Day | 2025 | 1311 | 96.10 | 32.84 | zscore+iqr | longer | 11 |
| Drama | tt7156814 | The Innocence | 2019 | 1260 | 96.10 | 31.46 | zscore+iqr | longer | 12 |
| Drama | tt7549254 | Sakhi |  | 1179 | 96.10 | 29.27 | zscore+iqr | longer | 13 |
| Drama | tt4567170 | Breaking Yop | 2015 | 1151 | 96.10 | 28.51 | zscore+iqr | longer | 14 |
| Drama | tt0821950 | A Mosca cieca | 1921 | 1035 | 96.10 | 25.38 | zscore+iqr | longer | 15 |
| Drama | tt2330754 | My Reflected Death | 2012 | 842 | 96.10 | 20.16 | zscore+iqr | longer | 16 |
| Drama | tt1910611 | Saving Julian | 2012 | 840 | 96.10 | 20.11 | zscore+iqr | longer | 17 |
| Drama | tt9047474 | La Flor | 2018 | 808 | 96.10 | 19.24 | zscore+iqr | longer | 18 |
| Drama | tt32186666 | Tendrils | 2024 | 799 | 96.10 | 19.00 | zscore+iqr | longer | 19 |
| Drama | tt3615052 | Empired | 2013 | 780 | 96.10 | 18.48 | zscore+iqr | longer | 20 |
| Family | tt1866307 | World Peace & Prayer Day | 2011 | 2400 | 92.26 | 73.45 | zscore+iqr | longer | 1 |
| Family | tt0231586 | De filosoof van Haeghem | 1967 | 385 | 92.26 | 9.32 | zscore+iqr | longer | 2 |
| Family | tt2654746 | Living Neverland | 2013 | 317 | 92.26 | 7.15 | zscore+iqr | longer | 3 |
| Family | tt0030138 | Flash Gordon's Trip to Mars | 1938 | 299 | 92.26 | 6.58 | zscore+iqr | longer | 4 |
| Family | tt33095704 | Snow White's Storytime: The Wishing-Stone Stories | 2024 | 296 | 92.26 | 6.49 | zscore+iqr | longer | 5 |
| Family | tt0033776 | Jungle Girl | 1941 | 267 | 92.26 | 5.56 | zscore+iqr | longer | 6 |
| Family | tt0031796 | The Phantom Creeps | 1939 | 265 | 92.26 | 5.50 | zscore+iqr | longer | 7 |
| Family | tt0030382 | The Lone Ranger | 1938 | 264 | 92.26 | 5.47 | zscore+iqr | longer | 8 |
| Family | tt0041162 | Batman and Robin | 1949 | 263 | 92.26 | 5.43 | zscore+iqr | longer | 9 |
| Family | tt0035665 | Batman | 1943 | 260 | 92.26 | 5.34 | zscore+iqr | longer | 10 |
| Family | tt0042846 | Pirates of the High Seas | 1950 | 260 | 92.26 | 5.34 | zscore+iqr | longer | 11 |
| Family | tt4294646 | Behavioral Family Therapy for Serious Psychiatric Disorders | 2013 | 260 | 92.26 | 5.34 | zscore+iqr | longer | 12 |
| Family | tt0031394 | The Green Hornet | 1940 | 258 | 92.26 | 5.28 | zscore+iqr | longer | 13 |
| Family | tt0027254 | Ace Drummond | 1936 | 255 | 92.26 | 5.18 | zscore+iqr | longer | 14 |
| Family | tt0042211 | Atom Man vs. Superman | 1950 | 252 | 92.26 | 5.08 | zscore+iqr | longer | 15 |
| Family | tt0043831 | Mysterious Island | 1951 | 252 | 92.26 | 5.08 | zscore+iqr | longer | 16 |
| Family | tt0022078 | The Lightning Warrior | 1931 | 250 | 92.26 | 5.02 | zscore+iqr | longer | 17 |
| Family | tt0049612 | Perils of the Wilderness | 1956 | 248 | 92.26 | 4.96 | zscore+iqr | longer | 18 |
| Family | tt0046012 | The Lost Planet | 1953 | 246 | 92.26 | 4.89 | zscore+iqr | longer | 19 |
| Family | tt0026867 | The Phantom Empire | 1935 | 245 | 92.26 | 4.86 | zscore+iqr | longer | 20 |
| Fantasy | tt0165127 | Burning of the Red Lotus Temple | 1928 | 1620 | 94.06 | 47.83 | zscore+iqr | longer | 1 |
| Fantasy | tt6127010 | Funusion | 2016 | 1440 | 94.06 | 42.19 | zscore+iqr | longer | 2 |
| Fantasy | tt9047474 | La Flor | 2018 | 808 | 94.06 | 22.38 | zscore+iqr | longer | 3 |
| Fantasy | tt11617492 | Orbius | 2020 | 570 | 94.06 | 14.92 | zscore+iqr | longer | 4 |
| Fantasy | tt5452954 | In Course of the Miraculous | 2016 | 540 | 94.06 | 13.98 | zscore+iqr | longer | 5 |
| Fantasy | tt4842296 | A Lullaby to the Sorrowful Mystery | 2016 | 485 | 94.06 | 12.25 | zscore+iqr | longer | 6 |
| Fantasy | tt1992236 | The Cremaster Cycle | 2003 | 398 | 94.06 | 9.53 | zscore+iqr | longer | 7 |
| Fantasy | tt10002034 | The Scowling Dusk Trilogy |  | 360 | 94.06 | 8.34 | zscore+iqr | longer | 8 |
| Fantasy | tt18547058 | Fireside Reading of A Study in Scarlet | 2022 | 360 | 94.06 | 8.34 | zscore+iqr | longer | 9 |
| Fantasy | tt9485592 | Girl Blood Sport | 2019 | 354 | 94.06 | 8.15 | zscore+iqr | longer | 10 |
| Fantasy | tt20870494 | Glitchtale the Movie (Season 2 Compilation) | 2022 | 338 | 94.06 | 7.65 | zscore+iqr | longer | 11 |
| Fantasy | tt0193571 | I topi grigi | 1918 | 320 | 94.06 | 7.08 | zscore+iqr | longer | 12 |
| Fantasy | tt0007107 | The Mysteries of Myra | 1916 | 310 | 94.06 | 6.77 | zscore+iqr | longer | 13 |
| Fantasy | tt42783932 | Critical Role: Live from Radio City Music Hall | 2025 | 300 | 94.06 | 6.46 | zscore+iqr | longer | 14 |
| Fantasy | tt1954491 | Battle of Demons | 2010 | 270 | 94.06 | 5.52 | zscore+iqr | longer | 15 |
| Fantasy | tt30526735 | Dragen og de 5 elementer | 2024 | 260 | 94.06 | 5.20 | zscore+iqr | longer | 16 |
| Fantasy | tt0221015 | Belphégor | 1927 | 255 | 94.06 | 5.04 | zscore+iqr | longer | 17 |
| Fantasy | tt12987702 | Bezumnyy angel Pinokkio | 2024 | 255 | 94.06 | 5.04 | zscore+iqr | longer | 18 |
| Fantasy | tt23708860 | Holy Fools | 2019 | 250 | 94.06 | 4.89 | zscore+iqr | longer | 19 |
| Fantasy | tt11452490 | The Wars of Darkness | 2005 | 245 | 94.06 | 4.73 | zscore+iqr | longer | 20 |
| Film-Noir | tt0048432 | Not as a Stranger | 1955 | 135 | 81.87 | 3.86 | zscore+iqr | longer | 1 |
| Film-Noir | tt0035966 | Hangmen Also Die! | 1943 | 134 | 81.87 | 3.79 | zscore+iqr | longer | 2 |
| Film-Noir | tt0038622 | Humoresque | 1946 | 125 | 81.87 | 3.13 | zscore+iqr | longer | 3 |
| Film-Noir | tt0043643 | His Kind of Woman | 1951 | 120 | 81.87 | 2.77 | zscore | longer | 4 |
| Film-Noir | tt0049130 | Death of a Scoundrel | 1956 | 119 | 81.87 | 2.70 | zscore | longer | 5 |
| Film-Noir | tt0038988 | The Strange Love of Martha Ivers | 1946 | 116 | 81.87 | 2.48 | zscore | longer | 6 |
| Film-Noir | tt0039066 | Undercurrent | 1946 | 116 | 81.87 | 2.48 | zscore | longer | 7 |
| Film-Noir | tt0039677 | Odd Man Out | 1947 | 116 | 81.87 | 2.48 | zscore | longer | 8 |
| Film-Noir | tt0038355 | The Big Sleep | 1946 | 114 | 81.87 | 2.33 | zscore | longer | 9 |
| Film-Noir | tt0038854 | The Postman Always Rings Twice | 1946 | 113 | 81.87 | 2.26 | zscore | longer | 10 |
| Film-Noir | tt0036790 | End of the Road | 1944 | 51 | 81.87 | -2.24 | zscore | shorter | 11 |
| Film-Noir | tt0037263 | The Seventh Cross | 1944 | 112 | 81.87 | 2.19 | zscore | longer | 12 |
| Film-Noir | tt0040202 | Call Northside 777 | 1948 | 112 | 81.87 | 2.19 | zscore | longer | 13 |
| Film-Noir | tt0042208 | The Asphalt Jungle | 1950 | 112 | 81.87 | 2.19 | zscore | longer | 14 |
| Film-Noir | tt0047985 | The Desperate Hours | 1955 | 112 | 81.87 | 2.19 | zscore | longer | 15 |
| Film-Noir | tt0035090 | Mr. District Attorney in the Carter Case | 1941 | 52 | 81.87 | -2.17 | zscore | shorter | 16 |
| Film-Noir | tt0037913 | Mildred Pierce | 1945 | 111 | 81.87 | 2.12 | zscore | longer | 17 |
| Film-Noir | tt0038109 | Spellbound | 1945 | 111 | 81.87 | 2.12 | zscore | longer | 18 |
| Film-Noir | tt0039666 | Nora Prentiss | 1947 | 111 | 81.87 | 2.12 | zscore | longer | 19 |
| Film-Noir | tt0041503 | Impact | 1949 | 111 | 81.87 | 2.12 | zscore | longer | 20 |
| History | tt5135246 | Saynatakuna: Masks | 2013 | 2905 | 94.28 | 53.17 | zscore+iqr | longer | 1 |
| History | tt0342707 | The Longest Most Meaningless Movie in the World | 1970 | 2880 | 94.28 | 52.70 | zscore+iqr | longer | 2 |
| History | tt1823692 | Hollywood East | 2010 | 1800 | 94.28 | 32.27 | zscore+iqr | longer | 3 |
| History | tt8677246 | Bullfighting Memories | 2017 | 1100 | 94.28 | 19.03 | zscore+iqr | longer | 4 |
| History | tt2330754 | My Reflected Death | 2012 | 842 | 94.28 | 14.14 | zscore+iqr | longer | 5 |
| History | tt0074334 | Comment Yukong déplaça les montagnes | 1976 | 763 | 94.28 | 12.65 | zscore+iqr | longer | 6 |
| History | tt7528992 | Europa: The Last Battle | 2017 | 746 | 94.28 | 12.33 | zscore+iqr | longer | 7 |
| History | tt0174864 | A Retrospection of Leningrad (1957-1990) | 1990 | 659 | 94.28 | 10.68 | zscore+iqr | longer | 8 |
| History | tt0270784 | Khleb - imya sushchestvitelnoe | 1988 | 580 | 94.28 | 9.19 | zscore+iqr | longer | 9 |
| History | tt0090015 | Shoah | 1985 | 566 | 94.28 | 8.92 | zscore+iqr | longer | 10 |
| History | tt2334994 | What Is Love? | 2012 | 545 | 94.28 | 8.53 | zscore+iqr | longer | 11 |
| History | tt4833186 | Freedom & Unity: The Vermont Movie | 2013 | 520 | 94.28 | 8.05 | zscore+iqr | longer | 12 |
| History | tt8296608 | Dead Souls | 2018 | 495 | 94.28 | 7.58 | zscore+iqr | longer | 13 |
| History | tt0162536 | The Photo-Drama of Creation | 1914 | 480 | 94.28 | 7.30 | zscore+iqr | longer | 14 |
| History | tt43493699 | F321 - Aussagen von KZ-Häftlingen kurz nach ihrer Befreiung | 2025 | 472 | 94.28 | 7.15 | zscore+iqr | longer | 15 |
| History | tt0178472 | Français si vous saviez | 1973 | 465 | 94.28 | 7.01 | zscore+iqr | longer | 16 |
| History | tt27722639 | The Lincoln Highway: Across America on the First Transcontinental Motor Route | 2023 | 451 | 94.28 | 6.75 | zscore+iqr | longer | 17 |
| History | tt42749576 | Mirror of Greed | 2026 | 450 | 94.28 | 6.73 | zscore+iqr | longer | 18 |
| History | tt0089458 | Lamentations a Monument for the Dead World | 1985 | 437 | 94.28 | 6.48 | zscore+iqr | longer | 19 |
| History | tt0270523 | The Movie Orgy | 1968 | 420 | 94.28 | 6.16 | zscore+iqr | longer | 20 |
| Horror | tt7521772 | 24 Hour Psycho | 1993 | 1440 | 88.66 | 60.68 | zscore+iqr | longer | 1 |
| Horror | tt1433078 | Amy's Night Out | 2007 | 675 | 88.66 | 26.33 | zscore+iqr | longer | 2 |
| Horror | tt7442346 | Fan | 2017 | 623 | 88.66 | 23.99 | zscore+iqr | longer | 3 |
| Horror | tt40792136 | Growth | 2026 | 587 | 88.66 | 22.38 | zscore+iqr | longer | 4 |
| Horror | tt3096442 | The Soulless | 2014 | 450 | 88.66 | 16.22 | zscore+iqr | longer | 5 |
| Horror | tt8492848 | Three Mirrors Creature's Flashes of Flesh | 2023 | 442 | 88.66 | 15.86 | zscore+iqr | longer | 6 |
| Horror | tt1992236 | The Cremaster Cycle | 2003 | 398 | 88.66 | 13.89 | zscore+iqr | longer | 7 |
| Horror | tt35657687 | In Search of Darkness 1995-1999: Journey Back Into Iconic '90s Horror | 2025 | 383 | 88.66 | 13.22 | zscore+iqr | longer | 8 |
| Horror | tt11777298 | DAU. Degeneratsiya | 2020 | 369 | 88.66 | 12.59 | zscore+iqr | longer | 9 |
| Horror | tt29476448 | In Search of Darkness 1990-1994: A Journey Into Iconic '90s Horror | 2024 | 363 | 88.66 | 12.32 | zscore+iqr | longer | 10 |
| Horror | tt10002034 | The Scowling Dusk Trilogy |  | 360 | 88.66 | 12.18 | zscore+iqr | longer | 11 |
| Horror | tt2802610 | Zombie Horror Fright Fest! | 2012 | 360 | 88.66 | 12.18 | zscore+iqr | longer | 12 |
| Horror | tt5505320 | Homunculus | 1916 | 360 | 88.66 | 12.18 | zscore+iqr | longer | 13 |
| Horror | tt0006554 | The Crimson Stain Mystery | 1916 | 355 | 88.66 | 11.96 | zscore+iqr | longer | 14 |
| Horror | tt48311633 | Mimic | 2025 | 355 | 88.66 | 11.96 | zscore+iqr | longer | 15 |
| Horror | tt15768444 | In Search of Darkness Part III: The Final Journey Into '80s Horror | 2022 | 341 | 88.66 | 11.33 | zscore+iqr | longer | 16 |
| Horror | tt37540837 | The Reflex | 2025 | 329 | 88.66 | 10.79 | zscore+iqr | longer | 17 |
| Horror | tt8241148 | Dagko na Tawo | 2018 | 320 | 88.66 | 10.39 | zscore+iqr | longer | 18 |
| Horror | tt0007107 | The Mysteries of Myra | 1916 | 310 | 88.66 | 9.94 | zscore+iqr | longer | 19 |
| Horror | tt0010356 | Lightning Bryce | 1919 | 300 | 88.66 | 9.49 | zscore+iqr | longer | 20 |
| Music | tt0284020 | The Cure for Insomnia | 1987 | 5220 | 88.43 | 88.99 | zscore+iqr | longer | 1 |
| Music | tt32350999 | Rock Milestones: Metallica - The Halcyon Years | 2007 | 2007 | 88.43 | 33.27 | zscore+iqr | longer | 2 |
| Music | tt32350897 | Madonna: Live | 2005 | 2005 | 88.43 | 33.24 | zscore+iqr | longer | 3 |
| Music | tt38952788 | The Schoenberg Effect: The Untold Story of Arnold Schoenberg's Musical Legacy | 2025 | 742 | 88.43 | 11.33 | zscore+iqr | longer | 4 |
| Music | tt17513128 | Deskpop x Funny Rave Presents: Ridge Raver | 2022 | 720 | 88.43 | 10.95 | zscore+iqr | longer | 5 |
| Music | tt12176756 | Die Meistersinger von Nürnberg | 2017 | 495 | 88.43 | 7.05 | zscore+iqr | longer | 6 |
| Music | tt12176912 | Lohengrin Bayreuth 2018 | 2018 | 460 | 88.43 | 6.44 | zscore+iqr | longer | 7 |
| Music | tt21867090 | AA Signature: Aquirax. Ongaku hihyôka Aida Akira | 2006 | 443 | 88.43 | 6.15 | zscore+iqr | longer | 8 |
| Music | tt0889237 | 100 Greatest Songs of the Past 25 Years | 2003 | 420 | 88.43 | 5.75 | zscore+iqr | longer | 9 |
| Music | tt35522738 | 13 Lentes De Um Final Feliz (Documentário Completo) | 2024 | 410 | 88.43 | 5.58 | zscore+iqr | longer | 10 |
| Music | tt7821060 | Depeche Mode: Video Singles Collection | 2016 | 383 | 88.43 | 5.11 | zscore+iqr | longer | 11 |
| Music | tt23897372 | Meris Kanispol | 2022 | 365 | 88.43 | 4.80 | zscore+iqr | longer | 12 |
| Music | tt7683692 | Fra X Til Døden | 2006 | 365 | 88.43 | 4.80 | zscore+iqr | longer | 13 |
| Music | tt1792588 | The Big 4: Live from Sofia, Bulgaria | 2010 | 364 | 88.43 | 4.78 | zscore+iqr | longer | 14 |
| Music | tt19656034 | Narthex making the album | 2022 | 360 | 88.43 | 4.71 | zscore+iqr | longer | 15 |
| Music | tt2486976 | Song | 2010 | 360 | 88.43 | 4.71 | zscore+iqr | longer | 16 |
| Music | tt39734226 | Ensaios da Anitta | 2026 | 360 | 88.43 | 4.71 | zscore+iqr | longer | 17 |
| Music | tt8232682 | Freddie Mercury: Lover of Life, Singer of Songs | 2006 | 360 | 88.43 | 4.71 | zscore+iqr | longer | 18 |
| Music | tt36553094 | Armageddon Over Wacken - Live 2004 | 2005 | 357 | 88.43 | 4.66 | zscore+iqr | longer | 19 |
| Music | tt35710276 | Royal Opera House: Die Walkure | 2025 | 356 | 88.43 | 4.64 | zscore+iqr | longer | 20 |
| Musical | tt22445582 | Sigur rós: Route One | 2016 | 1440 | 100.03 | 40.22 | zscore+iqr | longer | 1 |
| Musical | tt9047474 | La Flor | 2018 | 808 | 100.03 | 21.25 | zscore+iqr | longer | 2 |
| Musical | tt10037452 | Der fliegende Holländer | 2007 | 429 | 100.03 | 9.87 | zscore+iqr | longer | 3 |
| Musical | tt0240606 | L'idole des jeunes | 1976 | 338 | 100.03 | 7.14 | zscore+iqr | longer | 4 |
| Musical | tt11945356 | Ermitazh | 2020 | 319 | 100.03 | 6.57 | zscore+iqr | longer | 5 |
| Musical | tt43376331 | DCI 2026: Big, Loud & Live | 2026 | 315 | 100.03 | 6.45 | zscore+iqr | longer | 6 |
| Musical | tt5547792 | Still Swingin' | 1994 | 303 | 100.03 | 6.09 | zscore+iqr | longer | 7 |
| Musical | tt29780616 | BTS Japan Official Fanmeeting Vol.5: Magic Shop | 2020 | 260 | 100.03 | 4.80 | zscore+iqr | longer | 8 |
| Musical | tt9602094 | A Smartphone User's Guide to Etiquette | 2018 | 250 | 100.03 | 4.50 | zscore+iqr | longer | 9 |
| Musical | tt0317751 | Janwar | 1965 | 247 | 100.03 | 4.41 | zscore+iqr | longer | 10 |
| Musical | tt0246925 | Shirley Temple Story | 1976 | 240 | 100.03 | 4.20 | zscore+iqr | longer | 11 |
| Musical | tt0058547 | Sangam | 1964 | 238 | 100.03 | 4.14 | zscore+iqr | longer | 12 |
| Musical | tt7200370 | Season of the Devil | 2018 | 234 | 100.03 | 4.02 | zscore+iqr | longer | 13 |
| Musical | tt3785116 | Abraham & Sarah, the Film Musical | 2014 | 231 | 100.03 | 3.93 | zscore+iqr | longer | 14 |
| Musical | tt9624486 | Urban Tea Ceremony | 2009 | 227 | 100.03 | 3.81 | zscore+iqr | longer | 15 |
| Musical | tt9847236 | Just Some Kids | 2019 | 226 | 100.03 | 3.78 | zscore+iqr | longer | 16 |
| Musical | tt0066070 | My Name Is Joker | 1970 | 224 | 100.03 | 3.72 | zscore+iqr | longer | 17 |
| Musical | tt0169102 | Lagaan: Once Upon a Time in India | 2001 | 224 | 100.03 | 3.72 | zscore+iqr | longer | 18 |
| Musical | tt12088786 | Le Nozze di Figaro - Wiener Staatsoper | 2014 | 223 | 100.03 | 3.69 | zscore+iqr | longer | 19 |
| Musical | tt13224844 | Ballads of the Exodus | 2021 | 223 | 100.03 | 3.69 | zscore+iqr | longer | 20 |
| Mystery | tt5136218 | London EC1 | 2015 | 5460 | 94.39 | 106.38 | zscore+iqr | longer | 1 |
| Mystery | tt1745901 | How Does David Lynch Do It? | 2010 | 1800 | 94.39 | 33.82 | zscore+iqr | longer | 2 |
| Mystery | tt0246135 | Out 1 | 1971 | 776 | 94.39 | 13.51 | zscore+iqr | longer | 3 |
| Mystery | tt3201284 | Are We Famous Yet??? |  | 625 | 94.39 | 10.52 | zscore+iqr | longer | 4 |
| Mystery | tt0005005 | The Broken Coin | 1915 | 440 | 94.39 | 6.85 | zscore+iqr | longer | 5 |
| Mystery | tt0089458 | Lamentations a Monument for the Dead World | 1985 | 437 | 94.39 | 6.79 | zscore+iqr | longer | 6 |
| Mystery | tt0009701 | Tih Minh | 1918 | 418 | 94.39 | 6.42 | zscore+iqr | longer | 7 |
| Mystery | tt7740334 | Hogwash | 2023 | 382 | 94.39 | 5.70 | zscore+iqr | longer | 8 |
| Mystery | tt32189237 | She Found a Moviola | 2022 | 364 | 94.39 | 5.35 | zscore+iqr | longer | 9 |
| Mystery | tt0006554 | The Crimson Stain Mystery | 1916 | 355 | 94.39 | 5.17 | zscore+iqr | longer | 10 |
| Mystery | tt11347306 | First Last Man | 2022 | 326 | 94.39 | 4.59 | zscore+iqr | longer | 11 |
| Mystery | tt8241148 | Dagko na Tawo | 2018 | 320 | 94.39 | 4.47 | zscore+iqr | longer | 12 |
| Mystery | tt0010189 | The Great Gamble | 1919 | 310 | 94.39 | 4.27 | zscore+iqr | longer | 13 |
| Mystery | tt0027452 | The Amazing Exploits of the Clutching Hand | 1936 | 305 | 94.39 | 4.18 | zscore+iqr | longer | 14 |
| Mystery | tt0031230 | Dick Tracy's G-Men | 1939 | 302 | 94.39 | 4.12 | zscore+iqr | longer | 15 |
| Mystery | tt0008767 | Who Is Number One? | 1917 | 300 | 94.39 | 4.08 | zscore+iqr | longer | 16 |
| Mystery | tt0010795 | The Trail of the Octopus | 1919 | 300 | 94.39 | 4.08 | zscore+iqr | longer | 17 |
| Mystery | tt0012293 | The Hope Diamond Mystery | 1921 | 300 | 94.39 | 4.08 | zscore+iqr | longer | 18 |
| Mystery | tt0013864 | Beasts of Paradise | 1923 | 300 | 94.39 | 4.08 | zscore+iqr | longer | 19 |
| Mystery | tt0029287 | The Mysterious Pilot | 1937 | 300 | 94.39 | 4.08 | zscore+iqr | longer | 20 |
| News | tt38551781 | Australia Votes 2022 | 2022 | 387 | 77.62 | 9.61 | zscore+iqr | longer | 1 |
| News | tt38552314 | Australia Votes 2019 | 2019 | 387 | 77.62 | 9.61 | zscore+iqr | longer | 2 |
| News | tt38552441 | Australia Votes 2016 | 2016 | 373 | 77.62 | 9.18 | zscore+iqr | longer | 3 |
| News | tt3195318 | Glorious Things Are Sung of Zion | 2013 | 364 | 77.62 | 8.90 | zscore+iqr | longer | 4 |
| News | tt31196978 | The Stoke-on-Trent Sustainability Summit | 2023 | 360 | 77.62 | 8.77 | zscore+iqr | longer | 5 |
| News | tt38594596 | Queensland Votes | 2017 | 339 | 77.62 | 8.12 | zscore+iqr | longer | 6 |
| News | tt38594090 | Queensland Votes | 2024 | 329 | 77.62 | 7.81 | zscore+iqr | longer | 7 |
| News | tt22021004 | Inside a Cult - Gender Critical | 2022 | 320 | 77.62 | 7.53 | zscore+iqr | longer | 8 |
| News | tt38534186 | Tasmania Votes | 2025 | 305 | 77.62 | 7.06 | zscore+iqr | longer | 9 |
| News | tt38594704 | Queensland Votes | 2015 | 300 | 77.62 | 6.91 | zscore+iqr | longer | 10 |
| News | tt38594254 | Queensland Votes | 2020 | 289 | 77.62 | 6.57 | zscore+iqr | longer | 11 |
| News | tt38593942 | SA Votes | 2010 | 259 | 77.62 | 5.63 | zscore+iqr | longer | 12 |
| News | tt38551570 | WA Votes | 2017 | 255 | 77.62 | 5.51 | zscore+iqr | longer | 13 |
| News | tt38534245 | WA Votes | 2025 | 246 | 77.62 | 5.23 | zscore+iqr | longer | 14 |
| News | tt4086408 | RED by James Hogan | 2016 | 240 | 77.62 | 5.04 | zscore+iqr | longer | 15 |
| News | tt2925992 | Standing on Sacred Ground | 2013 | 228 | 77.62 | 4.67 | zscore+iqr | longer | 16 |
| News | tt2973582 | Sideroads | 2012 | 213 | 77.62 | 4.21 | zscore+iqr | longer | 17 |
| News | tt32842886 | UK General Election 2024 | 2024 | 180 | 77.62 | 3.18 | zscore+iqr | longer | 18 |
| News | tt6350750 | The Pillars of Heaven | 2017 | 179 | 77.62 | 3.15 | zscore+iqr | longer | 19 |
| News | tt3058116 | Single in Seattle | 2013 | 167 | 77.62 | 2.78 | zscore+iqr | longer | 20 |
| Reality-TV | tt38146238 | Sky TV | 1966 | 1440 | 92.07 | 15.82 | zscore+iqr | longer | 1 |
| Reality-TV | tt14437180 | Craziest Vacation Ever | 2020 | 317 | 92.07 | 2.64 | zscore+iqr | longer | 2 |
| Reality-TV | tt30616272 | Mit liv og min familie i julen | 2023 | 250 | 92.07 | 1.85 | iqr | longer | 3 |
| Reality-TV | tt3086504 | United Grand Lodge of Queensland Grand Installation | 2013 | 240 | 92.07 | 1.74 | iqr | longer | 4 |
| Reality-TV | tt14058376 | ALAF Fair & Fiesta | 2016 | 215 | 92.07 | 1.44 | iqr | longer | 5 |
| Reality-TV | tt32565918 | Beta Squad vs AMP Charity Match 2024 | 2024 | 210 | 92.07 | 1.38 | iqr | longer | 6 |
| Reality-TV | tt6860638 | Shotgun Boogie | 2017 | 200 | 92.07 | 1.27 | iqr | longer | 7 |
| Reality-TV | tt5275236 | 4K Fireplace | 2015 | 181 | 92.07 | 1.04 | iqr | longer | 8 |
| Reality-TV | tt50360286 | Engineering Paradise: On the Road |  | 180 | 92.07 | 1.03 | iqr | longer | 9 |
| Reality-TV | tt0383386 | Guru | 2003 | 162 | 92.07 | 0.82 | iqr | longer | 10 |
| Reality-TV | tt31849609 | The Loneliest Boy on Earth | 2024 | 158 | 92.07 | 0.77 | iqr | longer | 11 |
| Reality-TV | tt30413143 | The Netflix Slam | 2024 | 150 | 92.07 | 0.68 | iqr | longer | 12 |
| Reality-TV | tt25394952 | $100 vs. $10,000: Hotel Europe Edition | 2022 | 145 | 92.07 | 0.62 | iqr | longer | 13 |
| Romance | tt30249764 | The Man of Her Dreams | 2023 | 750 | 99.16 | 25.98 | zscore+iqr | longer | 1 |
| Romance | tt39392193 | The Longest Movie on Earth!?: The Narwallus Movie! | 2016 | 600 | 99.16 | 19.99 | zscore+iqr | longer | 2 |
| Romance | tt0270784 | Khleb - imya sushchestvitelnoe | 1988 | 580 | 99.16 | 19.20 | zscore+iqr | longer | 3 |
| Romance | tt7017462 | Till We Age | 2016 | 480 | 99.16 | 15.20 | zscore+iqr | longer | 4 |
| Romance | tt0346336 | The Best of Youth | 2003 | 374 | 99.16 | 10.97 | zscore+iqr | longer | 5 |
| Romance | tt0063794 | War and Peace | 1965 | 373 | 99.16 | 10.93 | zscore+iqr | longer | 6 |
| Romance | tt31645581 | I Wish I Were a Camera | 2025 | 369 | 99.16 | 10.77 | zscore+iqr | longer | 7 |
| Romance | tt0095530 | Little Dorrit | 1987 | 357 | 99.16 | 10.29 | zscore+iqr | longer | 8 |
| Romance | tt8056150 | What Love Feels Like | 2018 | 340 | 99.16 | 9.61 | zscore+iqr | longer | 9 |
| Romance | tt2360250 | The Break Ups | 2012 | 333 | 99.16 | 9.34 | zscore+iqr | longer | 10 |
| Romance | tt0051082 | Quiet Flows the Don | 1957 | 330 | 99.16 | 9.22 | zscore+iqr | longer | 11 |
| Romance | tt40486548 | Before We Grow Up | 2025 | 330 | 99.16 | 9.22 | zscore+iqr | longer | 12 |
| Romance | tt38778076 | A Heart's Shutter | 2025 | 314 | 99.16 | 8.58 | zscore+iqr | longer | 13 |
| Romance | tt0005400 | The Goddess | 1915 | 310 | 99.16 | 8.42 | zscore+iqr | longer | 14 |
| Romance | tt0008366 | The Neglected Wife | 1917 | 300 | 99.16 | 8.02 | zscore+iqr | longer | 15 |
| Romance | tt0011939 | The Avenging Arrow | 1921 | 300 | 99.16 | 8.02 | zscore+iqr | longer | 16 |
| Romance | tt43398485 | Two Rooms | 2026 | 299 | 99.16 | 7.98 | zscore+iqr | longer | 17 |
| Romance | tt1864584 | Spin | 2011 | 294 | 99.16 | 7.78 | zscore+iqr | longer | 18 |
| Romance | tt10094362 | The Blood Will Murder Roses | 2014 | 288 | 99.16 | 7.54 | zscore+iqr | longer | 19 |
| Romance | tt0204321 | The Sons of the Sun | 1924 | 284 | 99.16 | 7.38 | zscore+iqr | longer | 20 |
| Sci-Fi | tt6127010 | Funusion | 2016 | 1440 | 91.23 | 44.26 | zscore+iqr | longer | 1 |
| Sci-Fi | tt0131597 | Split | 2004 | 700 | 91.23 | 19.98 | zscore+iqr | longer | 2 |
| Sci-Fi | tt8997670 | Wholy | 2018 | 660 | 91.23 | 18.67 | zscore+iqr | longer | 3 |
| Sci-Fi | tt40792136 | Growth | 2026 | 587 | 91.23 | 16.27 | zscore+iqr | longer | 4 |
| Sci-Fi | tt35112545 | Planetagatik | 2024 | 579 | 91.23 | 16.01 | zscore+iqr | longer | 5 |
| Sci-Fi | tt38673358 | The Last Phantom: The Phantom Chronicles, Book 1 (Audiobook) | 2021 | 492 | 91.23 | 13.15 | zscore+iqr | longer | 6 |
| Sci-Fi | tt3096442 | The Soulless | 2014 | 450 | 91.23 | 11.77 | zscore+iqr | longer | 7 |
| Sci-Fi | tt8492848 | Three Mirrors Creature's Flashes of Flesh | 2023 | 442 | 91.23 | 11.51 | zscore+iqr | longer | 8 |
| Sci-Fi | tt12617172 | The Dominion War Chronicles | 2020 | 435 | 91.23 | 11.28 | zscore+iqr | longer | 9 |
| Sci-Fi | tt25811204 | FOMO: The Best Show That Never Was and Ever Is! | 2023 | 417 | 91.23 | 10.69 | zscore+iqr | longer | 10 |
| Sci-Fi | tt14426348 | Be Useful | 2019 | 397 | 91.23 | 10.03 | zscore+iqr | longer | 11 |
| Sci-Fi | tt0045382 | Commando Cody: Sky Marshal of the Universe | 1953 | 361 | 91.23 | 8.85 | zscore+iqr | longer | 12 |
| Sci-Fi | tt5505320 | Homunculus | 1916 | 360 | 91.23 | 8.82 | zscore+iqr | longer | 13 |
| Sci-Fi | tt26850159 | Space Force 9 & The Lord of the JohnnyBuddhas | 2022 | 347 | 91.23 | 8.39 | zscore+iqr | longer | 14 |
| Sci-Fi | tt2813024 | Black Sabbath | 2012 | 330 | 91.23 | 7.84 | zscore+iqr | longer | 15 |
| Sci-Fi | tt36374829 | Ferria: El despertar de un mundo (Audiolibro) | 2025 | 317 | 91.23 | 7.41 | zscore+iqr | longer | 16 |
| Sci-Fi | tt11341742 | In Search of Tomorrow | 2022 | 305 | 91.23 | 7.02 | zscore+iqr | longer | 17 |
| Sci-Fi | tt0028637 | Blake of Scotland Yard | 1937 | 303 | 91.23 | 6.95 | zscore+iqr | longer | 18 |
| Sci-Fi | tt0016237 | The Power God | 1925 | 300 | 91.23 | 6.85 | zscore+iqr | longer | 19 |
| Sci-Fi | tt16760450 | Inquisition - Avik Sarkar | 2022 | 300 | 91.23 | 6.85 | zscore+iqr | longer | 20 |
| Sport | tt1885195 | Azgrab: The Documentary | 2011 | 1669 | 88.90 | 42.26 | zscore+iqr | longer | 1 |
| Sport | tt3963450 | NHL: Washington Capitals 10 Greatest Games | 2010 | 1200 | 88.90 | 29.72 | zscore+iqr | longer | 2 |
| Sport | tt2000421 | The New York Yankees: Fall Classic Collector's Edition 1996-2001 | 2005 | 865 | 88.90 | 20.76 | zscore+iqr | longer | 3 |
| Sport | tt34798645 | 3 Games to Glory IV | 2015 | 398 | 88.90 | 8.27 | zscore+iqr | longer | 4 |
| Sport | tt11753240 | Girl on Tower | 2019 | 384 | 88.90 | 7.89 | zscore+iqr | longer | 5 |
| Sport | tt11265668 | KSI vs. Logan Paul II | 2019 | 368 | 88.90 | 7.46 | zscore+iqr | longer | 6 |
| Sport | tt34790129 | 3 Games to Glory III | 2005 | 360 | 88.90 | 7.25 | zscore+iqr | longer | 7 |
| Sport | tt41777960 | Best of NXT TakeOver 2018 | 2019 | 360 | 88.90 | 7.25 | zscore+iqr | longer | 8 |
| Sport | tt9534772 | Kid Fights from Around the World | 2018 | 360 | 88.90 | 7.25 | zscore+iqr | longer | 9 |
| Sport | tt10366986 | 3 Games to Glory VI | 2019 | 350 | 88.90 | 6.98 | zscore+iqr | longer | 10 |
| Sport | tt42040824 | The Ashes 2015 - Record Breaking Series | 2015 | 345 | 88.90 | 6.85 | zscore+iqr | longer | 11 |
| Sport | tt3117260 | Tottenham Hotspur Rivalries Collection | 2012 | 340 | 88.90 | 6.72 | zscore+iqr | longer | 12 |
| Sport | tt13851728 | Champions: Liverpool Football Club Season Review 2019-20 | 2020 | 316 | 88.90 | 6.07 | zscore+iqr | longer | 13 |
| Sport | tt34772921 | 3 Games to Glory II | 2004 | 300 | 88.90 | 5.65 | zscore+iqr | longer | 14 |
| Sport | tt9037316 | 2009 Nabba Britain Finals | 2009 | 295 | 88.90 | 5.51 | zscore+iqr | longer | 15 |
| Sport | tt0090559 | 16 Days of Glory | 1985 | 284 | 88.90 | 5.22 | zscore+iqr | longer | 16 |
| Sport | tt11100434 | Wilder vs. Ortiz | 2019 | 270 | 88.90 | 4.84 | zscore+iqr | longer | 17 |
| Sport | tt34800622 | 3 Games to Glory V | 2017 | 266 | 88.90 | 4.74 | zscore+iqr | longer | 18 |
| Sport | tt7266936 | The IX Olympiad in Amsterdam | 1928 | 251 | 88.90 | 4.34 | zscore+iqr | longer | 19 |
| Sport | tt1602608 | The IX Olympiad in Amsterdam | 1928 | 250 | 88.90 | 4.31 | zscore+iqr | longer | 20 |
| Talk-Show | tt4931176 | The Conciousnous Paradigm | 2015 | 190 | 88.08 | 3.02 | zscore | longer | 1 |
| Talk-Show | tt40109537 | Quo Vadis Austria III - Jetzt... und was wäre wenn? | 2025 | 185 | 88.08 | 2.87 | zscore | longer | 2 |
| Talk-Show | tt18521078 | Po stranitsam «Vokrug smekha». 1978-1980 | 2006 | 180 | 88.08 | 2.73 | zscore | longer | 3 |
| Talk-Show | tt12564502 | O'Brien's Extremely Pale Ale | 2013 | 165 | 88.08 | 2.28 | zscore | longer | 4 |
| Talk-Show | tt34872198 | Att vara två | 1972 | 160 | 88.08 | 2.13 | zscore | longer | 5 |
| Thriller | tt13990786 | Final Call | 2018 | 619 | 96.11 | 24.04 | zscore+iqr | longer | 1 |
| Thriller | tt0009905 | Barrabas | 1919 | 489 | 96.11 | 18.07 | zscore+iqr | longer | 2 |
| Thriller | tt0008284 | Mefisto | 1917 | 460 | 96.11 | 16.73 | zscore+iqr | longer | 3 |
| Thriller | tt28713219 | Christmas Mourning | 2023 | 420 | 96.11 | 14.89 | zscore+iqr | longer | 4 |
| Thriller | tt11777298 | DAU. Degeneratsiya | 2020 | 369 | 96.11 | 12.55 | zscore+iqr | longer | 5 |
| Thriller | tt19785522 | The Steward | 2021 | 338 | 96.11 | 11.12 | zscore+iqr | longer | 6 |
| Thriller | tt0098238 | The French Revolution | 1989 | 335 | 96.11 | 10.98 | zscore+iqr | longer | 7 |
| Thriller | tt14317746 | The Gallery | 2022 | 318 | 96.11 | 10.20 | zscore+iqr | longer | 8 |
| Thriller | tt0010795 | The Trail of the Octopus | 1919 | 300 | 96.11 | 9.37 | zscore+iqr | longer | 9 |
| Thriller | tt0011773 | The Tiger Band | 1920 | 300 | 96.11 | 9.37 | zscore+iqr | longer | 10 |
| Thriller | tt21378968 | Trenque Lauquen | 2022 | 262 | 96.11 | 7.63 | zscore+iqr | longer | 11 |
| Thriller | tt0066192 | Out 1: Spectre | 1972 | 253 | 96.11 | 7.21 | zscore+iqr | longer | 12 |
| Thriller | tt6019206 | Kill Bill: The Whole Bloody Affair | 2004 | 253 | 96.11 | 7.21 | zscore+iqr | longer | 13 |
| Thriller | tt1666348 | Vixen Highway 2006: It Came from Uranus! | 2010 | 250 | 96.11 | 7.08 | zscore+iqr | longer | 14 |
| Thriller | tt32516299 | Tanha Dar Mazrae | 2024 | 250 | 96.11 | 7.08 | zscore+iqr | longer | 15 |
| Thriller | tt0025940 | The Vanishing Shadow | 1934 | 242 | 96.11 | 6.71 | zscore+iqr | longer | 16 |
| Thriller | tt5765358 | The Way of Thorns |  | 240 | 96.11 | 6.62 | zscore+iqr | longer | 17 |
| Thriller | tt10952902 | Athaha | 2019 | 235 | 96.11 | 6.39 | zscore+iqr | longer | 18 |
| Thriller | tt39139925 | Dhurandhar: The Revenge | 2026 | 235 | 96.11 | 6.39 | zscore+iqr | longer | 19 |
| Thriller | tt0021895 | The Galloping Ghost | 1931 | 226 | 96.11 | 5.97 | zscore+iqr | longer | 20 |
| War | tt0095979 | The Journey | 1987 | 873 | 94.75 | 24.90 | zscore+iqr | longer | 1 |
| War | tt7528992 | Europa: The Last Battle | 2017 | 746 | 94.75 | 20.84 | zscore+iqr | longer | 2 |
| War | tt15765564 | 48 War Movies | 2019 | 720 | 94.75 | 20.01 | zscore+iqr | longer | 3 |
| War | tt0090015 | Shoah | 1985 | 566 | 94.75 | 15.08 | zscore+iqr | longer | 4 |
| War | tt0178472 | Français si vous saviez | 1973 | 465 | 94.75 | 11.85 | zscore+iqr | longer | 5 |
| War | tt1841612 | George Stevens' World War II Footage | 1946 | 420 | 94.75 | 10.41 | zscore+iqr | longer | 6 |
| War | tt0063794 | War and Peace | 1965 | 373 | 94.75 | 8.90 | zscore+iqr | longer | 7 |
| War | tt5503368 | Combat Trains | 2015 | 360 | 94.75 | 8.49 | zscore+iqr | longer | 8 |
| War | tt0257497 | La Commune (Paris, 1871) | 2000 | 345 | 94.75 | 8.01 | zscore+iqr | longer | 9 |
| War | tt0027488 | Custer's Last Stand | 1936 | 328 | 94.75 | 7.46 | zscore+iqr | longer | 10 |
| War | tt0275942 | Aszparuh | 1981 | 323 | 94.75 | 7.30 | zscore+iqr | longer | 11 |
| War | tt0074891 | The Memory of Justice | 1976 | 278 | 94.75 | 5.86 | zscore+iqr | longer | 12 |
| War | tt0406551 | The Gate of Sun | 2004 | 278 | 94.75 | 5.86 | zscore+iqr | longer | 13 |
| War | tt0124169 | Tokyo Trial | 1983 | 277 | 94.75 | 5.83 | zscore+iqr | longer | 14 |
| War | tt3493902 | Posledny reis Albatrosa | 1971 | 268 | 94.75 | 5.54 | zscore+iqr | longer | 15 |
| War | tt9573150 | Occupied City | 2023 | 266 | 94.75 | 5.48 | zscore+iqr | longer | 16 |
| War | tt0035611 | The Adventures of Smilin' Jack | 1943 | 265 | 94.75 | 5.45 | zscore+iqr | longer | 17 |
| War | tt2186805 | History of the National Security State | 2008 | 261 | 94.75 | 5.32 | zscore+iqr | longer | 18 |
| War | tt0063084 | The Hour of the Furnaces | 1968 | 260 | 94.75 | 5.29 | zscore+iqr | longer | 19 |
| War | tt2226515 | Sea of Blood | 1969 | 260 | 94.75 | 5.29 | zscore+iqr | longer | 20 |
| Western | tt0019196 | The Mystery Rider | 1928 | 380 | 76.55 | 10.56 | zscore+iqr | longer | 1 |
| Western | tt0011478 | The Moon Riders | 1920 | 360 | 76.55 | 9.86 | zscore+iqr | longer | 2 |
| Western | tt0027488 | Custer's Last Stand | 1936 | 328 | 76.55 | 8.75 | zscore+iqr | longer | 3 |
| Western | tt0031764 | The Oregon Trail | 1939 | 320 | 76.55 | 8.47 | zscore+iqr | longer | 4 |
| Western | tt0011335 | The Invisible Hand | 1920 | 310 | 76.55 | 8.12 | zscore+iqr | longer | 5 |
| Western | tt0015277 | Riders of the Plains | 1924 | 310 | 76.55 | 8.12 | zscore+iqr | longer | 6 |
| Western | tt0025706 | The Red Rider | 1934 | 310 | 76.55 | 8.12 | zscore+iqr | longer | 7 |
| Western | tt0026940 | The Roaring West | 1935 | 310 | 76.55 | 8.12 | zscore+iqr | longer | 8 |
| Western | tt0026720 | The Miracle Rider | 1935 | 306 | 76.55 | 7.98 | zscore+iqr | longer | 9 |
| Western | tt0011650 | Ruth of the Rockies | 1920 | 300 | 76.55 | 7.77 | zscore+iqr | longer | 10 |
| Western | tt0011784 | Trailed by Three | 1920 | 300 | 76.55 | 7.77 | zscore+iqr | longer | 11 |
| Western | tt0011815 | The Veiled Mystery | 1920 | 300 | 76.55 | 7.77 | zscore+iqr | longer | 12 |
| Western | tt0011997 | Breaking Through | 1921 | 300 | 76.55 | 7.77 | zscore+iqr | longer | 13 |
| Western | tt0012598 | The Purple Riders | 1922 | 300 | 76.55 | 7.77 | zscore+iqr | longer | 14 |
| Western | tt0013759 | White Eagle | 1922 | 300 | 76.55 | 7.77 | zscore+iqr | longer | 15 |
| Western | tt0031773 | Overland with Kit Carson | 1939 | 300 | 76.55 | 7.77 | zscore+iqr | longer | 16 |
| Western | tt0030137 | Flaming Frontiers | 1938 | 298 | 76.55 | 7.70 | zscore+iqr | longer | 17 |
| Western | tt0034390 | White Eagle | 1941 | 290 | 76.55 | 7.43 | zscore+iqr | longer | 18 |
| Western | tt0032386 | Deadwood Dick | 1940 | 285 | 76.55 | 7.25 | zscore+iqr | longer | 19 |
| Western | tt0034102 | Riders of Death Valley | 1941 | 283 | 76.55 | 7.18 | zscore+iqr | longer | 20 |

###### CSV exports

| file | total_rows | exported_rows | truncated | gold_directory |
| --- | --- | --- | --- | --- |
| q1_runtime_outliers_summary.csv | 26 | 26 | false | data/gold/exploration |
| q1_runtime_outliers.csv | 35557 | 35557 | false | data/gold/exploration |

<!-- AUTO:q1:end -->

### Q2. Most popular genres by year

#### Results

<!-- AUTO:q2:start -->

##### Q2 - Top 3 most popular movie genres per year

###### Parameters

| parameter | value |
| --- | --- |
| feature_film.title_types | movie |
| feature_film.min_runtime_minutes | 40 |
| feature_film.include_adult | false |
| min_votes | 1000 |
| year_min | 1980 |
| year_max | 2025 |
| top_n | 3 |
| popularity | sum of numVotes of the films of the genre released in the year |
| vote_share_pct | genre votes / votes of all genres of the year (film-genre pairs) |
| ranking | dense_rank by total_votes desc within the year |

###### Top 3 genres per year (share of the votes)

| year | rank_1 | rank_2 | rank_3 |
| --- | --- | --- | --- |
| 1980 | Drama (17.8%) | Adventure (14.5%) | Horror (12.1%) |
| 1981 | Adventure (20.6%) | Drama (14.7%) | Horror (11.6%) |
| 1982 | Drama (17.9%) | Sci-Fi (14.9%) | Action (11.1%) |
| 1983 | Drama (19.0%) | Action (13.6%) | Adventure (13.4%) |
| 1984 | Action (17.0%) | Adventure (13.7%) | Drama (13.6%) |
| 1985 | Comedy (21.4%) | Adventure (16.2%) | Drama (14.0%) |
| 1986 | Drama (18.8%) | Adventure (14.3%) | Comedy (13.1%) |
| 1987 | Drama (17.1%) | Comedy (15.4%) | Action (9.9%) |
| 1988 | Comedy (17.9%) | Drama (17.9%) | Action (11.0%) |
| 1989 | Comedy (20.9%) | Drama (16.2%) | Adventure (12.4%) |
| 1990 | Drama (20.6%) | Comedy (13.1%) | Crime (11.8%) |
| 1991 | Drama (19.6%) | Crime (13.2%) | Comedy (11.2%) |
| 1992 | Drama (20.4%) | Comedy (13.6%) | Crime (12.2%) |
| 1993 | Drama (24.3%) | Comedy (12.1%) | Crime (8.2%) |
| 1994 | Drama (32.9%) | Crime (13.6%) | Comedy (11.8%) |
| 1995 | Drama (23.2%) | Crime (14.5%) | Comedy (11.3%) |
| 1996 | Drama (20.6%) | Comedy (12.5%) | Crime (11.8%) |
| 1997 | Drama (22.2%) | Action (12.0%) | Comedy (9.8%) |
| 1998 | Drama (21.7%) | Comedy (18.2%) | Crime (11.5%) |
| 1999 | Drama (21.8%) | Comedy (11.5%) | Crime (10.2%) |
| 2000 | Drama (20.6%) | Comedy (13.2%) | Adventure (11.2%) |
| 2001 | Drama (18.5%) | Comedy (12.0%) | Adventure (11.8%) |
| 2002 | Drama (21.1%) | Adventure (10.9%) | Action (10.5%) |
| 2003 | Drama (16.8%) | Action (15.0%) | Comedy (13.6%) |
| 2004 | Drama (17.4%) | Action (12.3%) | Comedy (11.6%) |
| 2005 | Drama (16.6%) | Comedy (12.4%) | Action (11.2%) |
| 2006 | Drama (21.5%) | Comedy (12.1%) | Adventure (9.0%) |
| 2007 | Drama (18.0%) | Comedy (11.4%) | Adventure (8.8%) |
| 2008 | Drama (16.6%) | Action (12.9%) | Comedy (10.7%) |
| 2009 | Drama (16.7%) | Comedy (12.9%) | Action (11.7%) |
| 2010 | Drama (15.8%) | Action (12.2%) | Adventure (12.1%) |
| 2011 | Drama (18.3%) | Action (15.4%) | Comedy (12.4%) |
| 2012 | Drama (18.0%) | Action (13.5%) | Comedy (11.2%) |
| 2013 | Drama (16.8%) | Action (13.3%) | Comedy (11.4%) |
| 2014 | Drama (18.2%) | Action (15.8%) | Adventure (13.4%) |
| 2015 | Drama (18.9%) | Action (14.6%) | Adventure (13.4%) |
| 2016 | Drama (18.1%) | Action (15.2%) | Adventure (11.0%) |
| 2017 | Drama (19.1%) | Action (15.6%) | Adventure (10.5%) |
| 2018 | Drama (16.6%) | Action (14.8%) | Adventure (13.1%) |
| 2019 | Drama (20.5%) | Action (11.7%) | Comedy (11.4%) |
| 2020 | Drama (20.1%) | Comedy (12.6%) | Action (12.1%) |
| 2021 | Drama (17.7%) | Action (16.2%) | Adventure (12.9%) |
| 2022 | Drama (18.6%) | Action (16.0%) | Comedy (11.9%) |
| 2023 | Drama (18.7%) | Action (13.8%) | Comedy (12.4%) |
| 2024 | Drama (18.1%) | Action (13.8%) | Comedy (11.0%) |
| 2025 | Drama (15.0%) | Action (13.8%) | Comedy (10.3%) |

###### Detail per year and rank

| year | rank | genre | total_votes | vote_share_pct | n_films | weighted_rating |
| --- | --- | --- | --- | --- | --- | --- |
| 1980 | 1 | Drama | 3027804 | 17.83 | 131 | 7.81 |
| 1980 | 2 | Adventure | 2468725 | 14.54 | 43 | 7.95 |
| 1980 | 3 | Horror | 2052854 | 12.09 | 68 | 7.50 |
| 1981 | 1 | Adventure | 2237367 | 20.63 | 43 | 7.73 |
| 1981 | 2 | Drama | 1590505 | 14.66 | 139 | 7.28 |
| 1981 | 3 | Horror | 1256785 | 11.59 | 80 | 6.49 |
| 1982 | 1 | Drama | 2946433 | 17.89 | 151 | 7.55 |
| 1982 | 2 | Sci-Fi | 2454706 | 14.90 | 30 | 7.70 |
| 1982 | 3 | Action | 1835683 | 11.15 | 55 | 7.54 |
| 1983 | 1 | Drama | 2788336 | 19.04 | 156 | 7.43 |
| 1983 | 2 | Action | 1989654 | 13.59 | 58 | 7.48 |
| 1983 | 3 | Adventure | 1963073 | 13.41 | 44 | 7.52 |
| 1984 | 1 | Action | 3632498 | 17.03 | 65 | 7.34 |
| 1984 | 2 | Adventure | 2915630 | 13.67 | 41 | 7.37 |
| 1984 | 3 | Drama | 2890609 | 13.55 | 158 | 7.45 |
| 1985 | 1 | Comedy | 4485386 | 21.38 | 145 | 7.49 |
| 1985 | 2 | Adventure | 3398066 | 16.20 | 61 | 7.44 |
| 1985 | 3 | Drama | 2945153 | 14.04 | 144 | 7.28 |
| 1986 | 1 | Drama | 3866854 | 18.77 | 167 | 7.33 |
| 1986 | 2 | Adventure | 2945784 | 14.30 | 53 | 7.55 |
| 1986 | 3 | Comedy | 2697518 | 13.10 | 145 | 6.74 |
| 1987 | 1 | Drama | 3996016 | 17.11 | 185 | 7.41 |
| 1987 | 2 | Comedy | 3600960 | 15.42 | 160 | 6.93 |
| 1987 | 3 | Action | 2304287 | 9.87 | 76 | 6.95 |
| 1988 | 1 | Comedy | 4349471 | 17.95 | 166 | 6.92 |
| 1988 | 2 | Drama | 4328292 | 17.86 | 192 | 7.43 |
| 1988 | 3 | Action | 2654911 | 10.96 | 82 | 7.28 |
| 1989 | 1 | Comedy | 4921105 | 20.90 | 158 | 7.12 |
| 1989 | 2 | Drama | 3821159 | 16.23 | 195 | 7.29 |
| 1989 | 3 | Adventure | 2926012 | 12.43 | 50 | 7.43 |
| 1990 | 1 | Drama | 6193035 | 20.59 | 192 | 7.50 |
| 1990 | 2 | Comedy | 3940455 | 13.10 | 160 | 6.87 |
| 1990 | 3 | Crime | 3549117 | 11.80 | 88 | 7.53 |
| 1991 | 1 | Drama | 5436752 | 19.64 | 212 | 7.53 |
| 1991 | 2 | Crime | 3646018 | 13.17 | 73 | 7.80 |
| 1991 | 3 | Comedy | 3110786 | 11.24 | 170 | 6.67 |
| 1992 | 1 | Drama | 5969071 | 20.38 | 200 | 7.41 |
| 1992 | 2 | Comedy | 3991176 | 13.63 | 153 | 6.94 |
| 1992 | 3 | Crime | 3575993 | 12.21 | 82 | 7.35 |
| 1993 | 1 | Drama | 8869574 | 24.29 | 239 | 7.62 |
| 1993 | 2 | Comedy | 4431620 | 12.13 | 158 | 6.85 |
| 1993 | 3 | Crime | 3012451 | 8.25 | 87 | 7.20 |
| 1994 | 1 | Drama | 15599152 | 32.90 | 229 | 8.32 |
| 1994 | 2 | Crime | 6470001 | 13.65 | 78 | 7.92 |
| 1994 | 3 | Comedy | 5598176 | 11.81 | 192 | 6.68 |
| 1995 | 1 | Drama | 12369774 | 23.19 | 262 | 7.71 |
| 1995 | 2 | Crime | 7738737 | 14.51 | 84 | 7.85 |
| 1995 | 3 | Comedy | 6010547 | 11.27 | 172 | 7.09 |
| 1996 | 1 | Drama | 7718394 | 20.56 | 274 | 7.14 |
| 1996 | 2 | Comedy | 4700903 | 12.52 | 201 | 6.47 |
| 1996 | 3 | Crime | 4420055 | 11.78 | 86 | 7.31 |
| 1997 | 1 | Drama | 12457545 | 22.20 | 294 | 7.53 |
| 1997 | 2 | Action | 6717251 | 11.97 | 108 | 6.51 |
| 1997 | 3 | Comedy | 5504117 | 9.81 | 208 | 6.90 |
| 1998 | 1 | Drama | 11598188 | 21.70 | 305 | 7.53 |
| 1998 | 2 | Comedy | 9745216 | 18.23 | 229 | 7.23 |
| 1998 | 3 | Crime | 6172820 | 11.55 | 117 | 7.53 |
| 1999 | 1 | Drama | 15300056 | 21.84 | 343 | 7.73 |
| 1999 | 2 | Comedy | 8081188 | 11.53 | 240 | 6.87 |
| 1999 | 3 | Crime | 7133677 | 10.18 | 94 | 7.98 |
| 2000 | 1 | Drama | 12808766 | 20.56 | 355 | 7.45 |
| 2000 | 2 | Comedy | 8223657 | 13.20 | 249 | 6.81 |
| 2000 | 3 | Adventure | 6968865 | 11.19 | 47 | 7.33 |
| 2001 | 1 | Drama | 14503615 | 18.53 | 381 | 7.48 |
| 2001 | 2 | Comedy | 9378910 | 11.98 | 262 | 6.91 |
| 2001 | 3 | Adventure | 9233515 | 11.80 | 59 | 7.69 |
| 2002 | 1 | Drama | 16834985 | 21.11 | 433 | 7.47 |
| 2002 | 2 | Adventure | 8677010 | 10.88 | 68 | 7.27 |
| 2002 | 3 | Action | 8347807 | 10.47 | 143 | 6.74 |
| 2003 | 1 | Drama | 13019663 | 16.76 | 402 | 7.53 |
| 2003 | 2 | Action | 11660422 | 15.01 | 129 | 7.02 |
| 2003 | 3 | Comedy | 10597137 | 13.64 | 293 | 6.76 |
| 2004 | 1 | Drama | 16229606 | 17.38 | 484 | 7.30 |
| 2004 | 2 | Action | 11465354 | 12.28 | 162 | 7.01 |
| 2004 | 3 | Comedy | 10794723 | 11.56 | 320 | 6.67 |
| 2005 | 1 | Drama | 13398997 | 16.62 | 512 | 7.09 |
| 2005 | 2 | Comedy | 10016380 | 12.43 | 340 | 6.48 |
| 2005 | 3 | Action | 9004826 | 11.17 | 142 | 6.76 |
| 2006 | 1 | Drama | 20559813 | 21.49 | 557 | 7.44 |
| 2006 | 2 | Comedy | 11584521 | 12.11 | 374 | 6.55 |
| 2006 | 3 | Adventure | 8631378 | 9.02 | 108 | 6.90 |
| 2007 | 1 | Drama | 18207380 | 17.99 | 569 | 7.27 |
| 2007 | 2 | Comedy | 11512456 | 11.37 | 371 | 6.73 |
| 2007 | 3 | Adventure | 8952736 | 8.84 | 85 | 6.90 |
| 2008 | 1 | Drama | 17222935 | 16.64 | 581 | 7.00 |
| 2008 | 2 | Action | 13335951 | 12.89 | 178 | 6.77 |
| 2008 | 3 | Comedy | 11114053 | 10.74 | 354 | 6.41 |
| 2009 | 1 | Drama | 17216360 | 16.70 | 607 | 7.18 |
| 2009 | 2 | Comedy | 13253430 | 12.86 | 390 | 6.89 |
| 2009 | 3 | Action | 12036959 | 11.68 | 200 | 6.87 |
| 2010 | 1 | Drama | 17167536 | 15.78 | 621 | 6.96 |
| 2010 | 2 | Action | 13241158 | 12.17 | 224 | 6.68 |
| 2010 | 3 | Adventure | 13149083 | 12.08 | 101 | 7.34 |
| 2011 | 1 | Drama | 20332684 | 18.32 | 651 | 7.07 |
| 2011 | 2 | Action | 17057362 | 15.37 | 225 | 6.78 |
| 2011 | 3 | Comedy | 13748337 | 12.39 | 418 | 6.66 |
| 2012 | 1 | Drama | 19694709 | 17.99 | 686 | 7.12 |
| 2012 | 2 | Action | 14813382 | 13.53 | 234 | 6.85 |
| 2012 | 3 | Comedy | 12234527 | 11.17 | 414 | 6.68 |
| 2013 | 1 | Drama | 21525648 | 16.76 | 742 | 7.06 |
| 2013 | 2 | Action | 17089064 | 13.30 | 264 | 6.67 |
| 2013 | 3 | Comedy | 14649903 | 11.41 | 423 | 6.80 |
| 2014 | 1 | Drama | 24032745 | 18.16 | 809 | 7.12 |
| 2014 | 2 | Action | 20847132 | 15.75 | 277 | 6.93 |
| 2014 | 3 | Adventure | 17682928 | 13.36 | 155 | 7.29 |
| 2015 | 1 | Drama | 19970874 | 18.92 | 804 | 7.04 |
| 2015 | 2 | Action | 15446331 | 14.63 | 279 | 6.92 |
| 2015 | 3 | Adventure | 14102441 | 13.36 | 161 | 7.03 |
| 2016 | 1 | Drama | 20353952 | 18.14 | 879 | 7.10 |
| 2016 | 2 | Action | 17085217 | 15.23 | 317 | 6.82 |
| 2016 | 3 | Adventure | 12298078 | 10.96 | 161 | 6.72 |
| 2017 | 1 | Drama | 20226252 | 19.07 | 892 | 7.04 |
| 2017 | 2 | Action | 16596640 | 15.65 | 340 | 7.00 |
| 2017 | 3 | Adventure | 11132491 | 10.50 | 175 | 6.95 |
| 2018 | 1 | Drama | 16818313 | 16.64 | 944 | 6.93 |
| 2018 | 2 | Action | 14961587 | 14.80 | 319 | 6.91 |
| 2018 | 3 | Adventure | 13280109 | 13.14 | 173 | 7.05 |
| 2019 | 1 | Drama | 21406240 | 20.47 | 974 | 7.24 |
| 2019 | 2 | Action | 12246649 | 11.71 | 326 | 6.84 |
| 2019 | 3 | Comedy | 11929978 | 11.41 | 515 | 6.84 |
| 2020 | 1 | Drama | 10054756 | 20.12 | 706 | 6.60 |
| 2020 | 2 | Comedy | 6282107 | 12.57 | 388 | 6.48 |
| 2020 | 3 | Action | 6060642 | 12.13 | 203 | 6.18 |
| 2021 | 1 | Drama | 13905357 | 17.67 | 820 | 6.80 |
| 2021 | 2 | Action | 12778870 | 16.24 | 305 | 6.64 |
| 2021 | 3 | Adventure | 10148574 | 12.89 | 145 | 7.02 |
| 2022 | 1 | Drama | 15385106 | 18.56 | 952 | 6.89 |
| 2022 | 2 | Action | 13250749 | 15.98 | 364 | 6.77 |
| 2022 | 3 | Comedy | 9874991 | 11.91 | 556 | 6.61 |
| 2023 | 1 | Drama | 14140550 | 18.67 | 897 | 6.89 |
| 2023 | 2 | Action | 10454227 | 13.81 | 387 | 6.53 |
| 2023 | 3 | Comedy | 9425697 | 12.45 | 505 | 6.60 |
| 2024 | 1 | Drama | 11152615 | 18.08 | 765 | 6.71 |
| 2024 | 2 | Action | 8525327 | 13.82 | 343 | 6.56 |
| 2024 | 3 | Comedy | 6769705 | 10.98 | 450 | 6.47 |
| 2025 | 1 | Drama | 8225477 | 15.00 | 645 | 6.68 |
| 2025 | 2 | Action | 7589233 | 13.84 | 312 | 6.44 |
| 2025 | 3 | Comedy | 5645232 | 10.29 | 357 | 6.46 |

###### CSV exports

| file | total_rows | exported_rows | truncated | gold_directory |
| --- | --- | --- | --- | --- |
| q2_top_genres.csv | 138 | 138 | false | data/gold/exploration |
| q2_top_genres_all_genres.csv | 975 | 975 | false | data/gold/exploration |

<!-- AUTO:q2:end -->

### Q3. Top genres versus the rest

#### Results

<!-- AUTO:q3:start -->

##### Q3 - Top 3 genres versus the other genres

###### Parameters

| parameter | value |
| --- | --- |
| feature_film.title_types | movie |
| feature_film.min_runtime_minutes | 40 |
| feature_film.include_adult | false |
| min_votes | 1000 |
| year_min | 1980 |
| year_max | 2025 |
| top_n | 3 |
| top | genres ranked <= top_n in the year (Q2 ranking) |
| rest | all the other genres of the year |
| films | (film, genre) pairs: a film counts once in each of its genres |
| weighted_rating | sum(averageRating * numVotes) / sum(numVotes) |

###### Comparison per decade

| decade | top_vote_share_pct | votes_ratio_top_rest | top_films | rest_films | top_votes_per_film | rest_votes_per_film | votes_per_film_ratio_top_rest | top_weighted_rating | rest_weighted_rating | weighted_rating_diff_top_rest | rest_genres_per_year |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1980 | 46.27 | 0.86 | 3241 | 4663 | 27550.64 | 22236.51 | 1.24 | 7.35 | 7.11 | 0.24 | 17.90 |
| 1990 | 47.35 | 0.90 | 5330 | 5207 | 39223.61 | 44639.57 | 0.88 | 7.43 | 7.18 | 0.25 | 17.90 |
| 2000 | 41.67 | 0.71 | 9155 | 10731 | 39846.23 | 47584.58 | 0.84 | 7.06 | 7.03 | 0.02 | 18.20 |
| 2010 | 44.22 | 0.79 | 13503 | 20086 | 36667.51 | 31088.76 | 1.18 | 6.97 | 6.90 | 0.07 | 18.70 |
| 2020 | 44.49 | 0.80 | 9100 | 11657 | 19743.87 | 19230.94 | 1.03 | 6.67 | 6.57 | 0.11 | 18.33 |

###### Comparison per year

| year | top_vote_share_pct | votes_ratio_top_rest | top_films | rest_films | top_votes_per_film | rest_votes_per_film | votes_per_film_ratio_top_rest | top_weighted_rating | rest_weighted_rating | weighted_rating_diff_top_rest | rest_genres_per_year |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1980 | 44.45 | 0.80 | 242 | 439 | 31195.80 | 21491.67 | 1.45 | 7.77 | 7.54 | 0.22 | 18.00 |
| 1981 | 46.88 | 0.88 | 262 | 456 | 19407.09 | 12634.05 | 1.54 | 7.28 | 6.90 | 0.38 | 18.00 |
| 1982 | 43.94 | 0.78 | 236 | 442 | 30664.50 | 20891.14 | 1.47 | 7.60 | 7.19 | 0.41 | 17.00 |
| 1983 | 46.04 | 0.85 | 258 | 442 | 26128.15 | 17874.62 | 1.46 | 7.47 | 7.15 | 0.32 | 18.00 |
| 1984 | 44.25 | 0.79 | 264 | 472 | 35752.79 | 25195.10 | 1.42 | 7.38 | 7.22 | 0.16 | 18.00 |
| 1985 | 51.62 | 1.07 | 350 | 399 | 30938.87 | 25439.60 | 1.22 | 7.42 | 7.05 | 0.37 | 18.00 |
| 1986 | 46.17 | 0.86 | 365 | 452 | 26055.22 | 24532.06 | 1.06 | 7.23 | 7.09 | 0.14 | 18.00 |
| 1987 | 42.40 | 0.74 | 421 | 476 | 23518.44 | 28258.49 | 0.83 | 7.13 | 7.09 | 0.04 | 18.00 |
| 1988 | 46.77 | 0.88 | 440 | 536 | 25756.08 | 24067.94 | 1.07 | 7.20 | 7.10 | 0.10 | 18.00 |
| 1989 | 49.56 | 0.98 | 403 | 549 | 28953.54 | 21632.03 | 1.34 | 7.25 | 6.81 | 0.44 | 18.00 |
| 1990 | 45.50 | 0.83 | 440 | 471 | 31096.83 | 34799.96 | 0.89 | 7.33 | 7.09 | 0.24 | 18.00 |
| 1991 | 44.04 | 0.79 | 455 | 463 | 26799.02 | 33462.18 | 0.80 | 7.39 | 7.53 | -0.14 | 18.00 |
| 1992 | 46.22 | 0.86 | 435 | 451 | 31117.79 | 34924.83 | 0.89 | 7.26 | 7.02 | 0.24 | 18.00 |
| 1993 | 44.67 | 0.81 | 484 | 522 | 33705.88 | 38713.27 | 0.87 | 7.34 | 7.41 | -0.08 | 18.00 |
| 1994 | 58.36 | 1.40 | 499 | 475 | 55445.55 | 41564.21 | 1.33 | 7.89 | 7.34 | 0.55 | 18.00 |
| 1995 | 48.97 | 0.96 | 518 | 536 | 50422.89 | 50779.12 | 0.99 | 7.61 | 7.29 | 0.32 | 18.00 |
| 1996 | 44.86 | 0.81 | 561 | 518 | 30016.67 | 39954.76 | 0.75 | 7.00 | 6.80 | 0.20 | 18.00 |
| 1997 | 43.97 | 0.78 | 610 | 562 | 40457.23 | 55949.99 | 0.72 | 7.11 | 7.14 | -0.03 | 17.00 |
| 1998 | 51.47 | 1.06 | 651 | 599 | 42267.63 | 43307.87 | 0.98 | 7.43 | 6.82 | 0.61 | 18.00 |
| 1999 | 43.55 | 0.77 | 677 | 610 | 45073.74 | 64840.28 | 0.70 | 7.56 | 7.34 | 0.22 | 18.00 |
| 2000 | 44.95 | 0.82 | 651 | 770 | 43012.73 | 44545.16 | 0.97 | 7.23 | 7.00 | 0.24 | 18.00 |
| 2001 | 42.31 | 0.73 | 702 | 826 | 47173.85 | 54664.30 | 0.86 | 7.38 | 7.18 | 0.20 | 18.00 |
| 2002 | 42.45 | 0.74 | 644 | 1028 | 52577.33 | 44657.43 | 1.18 | 7.24 | 7.06 | 0.18 | 18.00 |
| 2003 | 45.41 | 0.83 | 824 | 830 | 42812.16 | 51105.08 | 0.84 | 7.13 | 7.24 | -0.11 | 18.00 |
| 2004 | 41.23 | 0.70 | 966 | 976 | 39844.39 | 56217.84 | 0.71 | 7.04 | 7.12 | -0.08 | 19.00 |
| 2005 | 40.22 | 0.67 | 994 | 1051 | 32615.90 | 45845.57 | 0.71 | 6.81 | 6.88 | -0.07 | 18.00 |
| 2006 | 42.63 | 0.74 | 1039 | 1286 | 39245.15 | 42674.26 | 0.92 | 7.08 | 7.02 | 0.06 | 18.00 |
| 2007 | 38.20 | 0.62 | 1025 | 1347 | 37729.34 | 46437.79 | 0.81 | 7.02 | 6.90 | 0.12 | 18.00 |
| 2008 | 40.27 | 0.67 | 1113 | 1232 | 37441.99 | 50172.73 | 0.75 | 6.77 | 7.11 | -0.34 | 18.00 |
| 2009 | 41.24 | 0.70 | 1197 | 1385 | 35511.07 | 43723.22 | 0.81 | 7.00 | 6.89 | 0.10 | 19.00 |
| 2010 | 40.03 | 0.67 | 946 | 1621 | 46044.16 | 40251.59 | 1.14 | 6.99 | 7.04 | -0.05 | 19.00 |
| 2011 | 46.08 | 0.85 | 1294 | 1389 | 39519.62 | 43074.53 | 0.92 | 6.86 | 6.77 | 0.09 | 18.00 |
| 2012 | 42.69 | 0.74 | 1334 | 1585 | 35039.44 | 39597.18 | 0.88 | 6.92 | 6.97 | -0.05 | 19.00 |
| 2013 | 41.47 | 0.71 | 1429 | 1725 | 37274.05 | 43583.71 | 0.86 | 6.87 | 6.97 | -0.10 | 19.00 |
| 2014 | 47.27 | 0.90 | 1241 | 2219 | 50413.22 | 31449.87 | 1.60 | 7.11 | 6.98 | 0.12 | 19.00 |
| 2015 | 46.91 | 0.88 | 1244 | 2179 | 39806.79 | 25718.23 | 1.55 | 7.00 | 6.80 | 0.20 | 19.00 |
| 2016 | 44.32 | 0.80 | 1357 | 2284 | 36652.36 | 27353.72 | 1.34 | 6.91 | 6.93 | -0.02 | 19.00 |
| 2017 | 45.21 | 0.83 | 1407 | 2426 | 34083.43 | 23954.53 | 1.42 | 7.00 | 6.79 | 0.21 | 18.00 |
| 2018 | 44.57 | 0.80 | 1436 | 2469 | 31378.84 | 22693.21 | 1.38 | 6.96 | 6.78 | 0.18 | 18.00 |
| 2019 | 43.59 | 0.77 | 1815 | 2189 | 25114.53 | 26944.15 | 0.93 | 7.03 | 6.88 | 0.15 | 19.00 |
| 2020 | 44.81 | 0.81 | 1297 | 1689 | 17268.70 | 16331.87 | 1.06 | 6.45 | 6.45 | 0.01 | 18.00 |
| 2021 | 46.80 | 0.88 | 1270 | 2138 | 29002.21 | 19586.04 | 1.48 | 6.80 | 6.58 | 0.23 | 18.00 |
| 2022 | 46.45 | 0.87 | 1872 | 2243 | 20572.03 | 19796.93 | 1.04 | 6.78 | 6.58 | 0.19 | 19.00 |
| 2023 | 44.93 | 0.82 | 1789 | 2110 | 19016.48 | 19763.14 | 0.96 | 6.70 | 6.69 | 0.01 | 18.00 |
| 2024 | 42.88 | 0.75 | 1558 | 1867 | 16975.38 | 18871.08 | 0.90 | 6.60 | 6.55 | 0.05 | 18.00 |
| 2025 | 39.13 | 0.64 | 1314 | 1610 | 16331.77 | 20732.01 | 0.79 | 6.54 | 6.48 | 0.06 | 19.00 |

###### Stability of the top 3 (years spent in it)

| genre | years_in_top | years_ranked_first | first_year_in_top | last_year_in_top | average_rank | average_vote_share_pct | pct_years_in_top |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Drama | 46 | 41 | 1980 | 2025 | 1.15 | 18.83 | 100.00 |
| Comedy | 33 | 3 | 1985 | 2025 | 2.98 | 12.13 | 71.74 |
| Action | 28 | 1 | 1982 | 2025 | 3.26 | 11.56 | 60.87 |
| Adventure | 19 | 1 | 1980 | 2021 | 3.87 | 10.50 | 41.30 |
| Crime | 9 | 0 | 1990 | 1999 | 5.54 | 7.80 | 19.57 |
| Horror | 2 | 0 | 1980 | 1981 | 9.02 | 4.61 | 4.35 |
| Sci-Fi | 1 | 0 | 1982 | 1982 | 8.46 | 5.06 | 2.17 |

###### CSV exports

| file | total_rows | exported_rows | truncated | gold_directory |
| --- | --- | --- | --- | --- |
| q3_top_vs_rest_yearly.csv | 46 | 46 | false | data/gold/exploration |
| q3_top_vs_rest_by_decade.csv | 5 | 5 | false | data/gold/exploration |
| q3_top_vs_rest_stability.csv | 7 | 7 | false | data/gold/exploration |

<!-- AUTO:q3:end -->

### Q4. Directors with one highly rated film

#### Results

<!-- AUTO:q4:start -->

##### Q4 - Directors with exactly one highly rated film and low-rated other films

###### Parameters

| parameter | value |
| --- | --- |
| feature_film.title_types | movie |
| feature_film.min_runtime_minutes | 40 |
| feature_film.include_adult | false |
| min_votes | 1000 |
| high_rating | 8 |
| low_average | 6 |
| min_other_films | 2 |
| director_sources | title.crew.directors UNION title.principals (category = director) |
| rated_feature_films | 49434 |
| directors_found | 47 |
| sorted_by | hit_rating desc, hit_votes desc |

###### Directors

| nconst | primaryName | hit_title | hit_year | hit_rating | hit_votes | n_other_films | avg_other_rating | min_other_rating | max_other_rating |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nm6252943 | Harish Vyas | Om Ka Hari | 2026 | 9.80 | 5026 | 2 | 5.75 | 4.80 | 6.70 |
| nm2735803 | Saurabh Varma | The Great Punjab Robbery | 2026 | 9.30 | 1760 | 2 | 5.90 | 5.70 | 6.10 |
| nm0449984 | Irvin Kershner | Star Wars: Episode V - The Empire Strikes Back | 1980 | 8.70 | 1533117 | 9 | 5.94 | 4.50 | 6.80 |
| nm0500896 | David Leland | Concert for George | 2003 | 8.60 | 2330 | 4 | 5.85 | 4.70 | 6.80 |
| nm0062614 | Harry Baweja | Chaar Sahibzaade 2: Rise of Banda Singh Bahadur | 2016 | 8.60 | 1051 | 6 | 5.30 | 2.70 | 7.80 |
| nm2259353 | Christopher Ashley | Come from Away | 2021 | 8.50 | 5015 | 2 | 5.60 | 4.40 | 6.80 |
| nm0846092 | Kamal Tabrizi | The Lizard | 2004 | 8.40 | 24813 | 4 | 5.53 | 4.10 | 7.50 |
| nm1703622 | R. Madhesh | Mudhalvan | 1999 | 8.40 | 9594 | 3 | 5.87 | 5.10 | 6.50 |
| nm0803350 | Sangeeth Sivan | Yoddha | 1992 | 8.40 | 5499 | 4 | 5.25 | 3.50 | 6.10 |
| nm16275551 | Sateesh Paramveda | Seetha Kalyana Vaibhogame | 2024 | 8.40 | 2362 | 2 | 5.80 | 3.80 | 7.80 |
| nm9511013 | Satish Paramvedha | Seetha Kalyana Vaibhogame | 2024 | 8.40 | 2362 | 2 | 5.80 | 3.80 | 7.80 |
| nm1318819 | Ezhil | Thulladha Manamum Thullum | 1999 | 8.30 | 7363 | 2 | 4.55 | 2.80 | 6.30 |
| nm0092632 | Carlos Bolado | Promises | 2001 | 8.30 | 2796 | 2 | 5.85 | 4.40 | 7.30 |
| nm0796117 | M. Night Shyamalan | The Sixth Sense | 1999 | 8.20 | 1177469 | 15 | 5.87 | 3.90 | 7.30 |
| nm1359360 | Dharani | Ghilli | 2004 | 8.20 | 19436 | 5 | 5.44 | 3.90 | 7.20 |
| nm5650589 | Nalan Kumarasamy | Soodhu Kavvum | 2013 | 8.20 | 13775 | 2 | 5.95 | 4.40 | 7.50 |
| nm0890864 | P. Vasu | Aapthamitra | 2004 | 8.20 | 1464 | 5 | 5.24 | 2.60 | 7.20 |
| nm0574625 | James McTeigue | V for Vendetta | 2005 | 8.10 | 1261778 | 4 | 5.98 | 5.50 | 6.40 |
| nm0853238 | Tate Taylor | The Help | 2011 | 8.10 | 535066 | 6 | 5.88 | 5.00 | 6.90 |
| nm1084488 | Umesh Shukla | OMG: Oh My God! | 2012 | 8.10 | 72471 | 6 | 5.60 | 3.60 | 7.40 |
| nm2134474 | Vikas Bahl | Queen | 2013 | 8.10 | 72021 | 6 | 5.83 | 2.60 | 7.90 |
| nm1729063 | Mert Baykal | Pardon | 2005 | 8.10 | 24941 | 3 | 5.90 | 4.50 | 7.40 |
| nm8678191 | Karthick Naren | Dhuruvangal Pathinaaru | 2016 | 8.10 | 19417 | 2 | 5.15 | 4.40 | 5.90 |
| nm6044360 | Ravikanth Perepu | Kshanam | 2016 | 8.10 | 6712 | 2 | 5.95 | 5.90 | 6.00 |
| nm0536705 | Ananth Mahadevan | Phule | 2025 | 8.10 | 3248 | 4 | 5.15 | 3.50 | 6.90 |
| nm1434372 | Johny Antony | C.I.D. Moosa | 2003 | 8.10 | 2817 | 2 | 5.80 | 5.10 | 6.50 |
| nm0446819 | Richard Kelly | Donnie Darko | 2001 | 8.00 | 925354 | 2 | 5.45 | 5.30 | 5.60 |
| nm0001675 | Robert Rodriguez | Sin City | 2005 | 8.00 | 825724 | 22 | 5.94 | 3.60 | 7.50 |
| nm0588340 | Frank Miller | Sin City | 2005 | 8.00 | 825724 | 2 | 5.65 | 4.80 | 6.50 |
| nm0132709 | Martin Campbell | Casino Royale | 2006 | 8.00 | 758789 | 16 | 5.92 | 4.20 | 7.20 |
| nm0204628 | Garth Davis | Lion | 2016 | 8.00 | 270305 | 2 | 5.65 | 5.40 | 5.90 |
| nm0490487 | Wai Keung Lau | Infernal Affairs | 2002 | 8.00 | 139912 | 21 | 6.00 | 2.70 | 7.40 |
| nm1749112 | Vincent Paronnaud | Persepolis | 2007 | 8.00 | 107510 | 3 | 5.70 | 4.80 | 7.00 |
| nm0000671 | Billy Bob Thornton | Sling Blade | 1996 | 8.00 | 105234 | 3 | 5.93 | 5.70 | 6.30 |
| nm0031342 | Predrag Antonijevic | Dara of Jasenovac | 2020 | 8.00 | 82508 | 5 | 5.70 | 4.30 | 7.40 |
| nm5120912 | Ajay Bahl | Section 375 | 2019 | 8.00 | 21947 | 3 | 4.63 | 1.80 | 6.30 |
| nm0244892 | J.P. Dutta | Border | 1997 | 8.00 | 20780 | 4 | 5.33 | 5.20 | 5.50 |
| nm0700872 | Puri Jagannadh | Pokiri | 2006 | 8.00 | 17308 | 18 | 5.80 | 2.60 | 7.40 |
| nm0149134 | Sinan Çetin | Abbas in Flower | 1982 | 8.00 | 12168 | 7 | 4.84 | 1.80 | 7.10 |
| nm0348015 | Gunasekhar | Okkadu | 2003 | 8.00 | 11854 | 6 | 5.38 | 3.60 | 7.20 |
| nm0761522 | Denis Sanders | Elvis: That's the Way It Is | 1970 | 8.00 | 3536 | 2 | 5.60 | 4.90 | 6.30 |
| nm0002239 | Prince | Sign 'o' the Times | 1987 | 8.00 | 3058 | 2 | 4.90 | 4.70 | 5.10 |
| nm0389514 | David Hogan | Sign 'o' the Times | 1987 | 8.00 | 3058 | 2 | 4.60 | 3.60 | 5.60 |
| nm0536299 | Albert Magnoli | Sign 'o' the Times | 1987 | 8.00 | 3058 | 4 | 5.80 | 5.00 | 6.50 |
| nm3607398 | Suseenthiran | Jeeva | 2014 | 8.00 | 2448 | 5 | 5.96 | 4.30 | 7.20 |
| nm1048560 | Marcus Raboy | Conan O'Brien: The Kennedy Center Mark Twain Prize for American Humor | 2025 | 8.00 | 1584 | 2 | 5.45 | 5.10 | 5.80 |
| nm0735879 | Ismael Rodríguez | Two Careful Fellows | 1953 | 8.00 | 1141 | 2 | 5.95 | 4.10 | 7.80 |

###### CSV exports

| file | total_rows | exported_rows | truncated | gold_directory |
| --- | --- | --- | --- | --- |
| q4_one_hit_directors.csv | 47 | 47 | false | data/gold/exploration |

<!-- AUTO:q4:end -->

### Q5. Series with a decline in their final season

#### Results

<!-- AUTO:q5:start -->

##### Q5 - Series with the best episode in the first seasons and the worst in the last

###### Parameters

| parameter | value |
| --- | --- |
| series_types | tvSeries, tvMiniSeries |
| min_seasons | 3 |
| min_episodes_per_season | 10 |
| min_votes_episode | 50 |
| first_seasons | 2 |
| tie_policy | all |
| last_season | highest positive season number before rating and vote filtering |
| series_with_enough_eligible_seasons | 1364 |
| series_selected | 171 |
| sorted_by | n_rated_episodes desc |

###### Series

_Showing 50 of 171 rows_

| series_title | start_year | end_year | n_seasons | n_eligible_seasons | n_rated_episodes | best_rating | best_season | best_episode | best_episode_title | n_best_episodes | worst_rating | worst_season | worst_episode | worst_episode_title | n_worst_episodes | last_season |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| The Beverly Hillbillies | 1962 | 1971 | 9 | 9 | 274 | 8.80 | 2 | 25 | Granny Versus the Weather Bureau | 1 | 5.80 | 9 | 18 | The Palace of Clampett-San | 2 | 9 |
| Coach | 1989 | 1997 | 9 | 9 | 199 | 9.10 | 2 | 15 | Homewreckers | 1 | 6.70 | 9 | 4 | Isn't It Romantic? | 1 | 9 |
| The Cosby Show | 1984 | 1992 | 8 | 8 | 197 | 8.50 | 2 | 22 | Theo's Holiday | 1 | 5.40 | 8 | 22 | You Can't Stop the Music | 1 | 8 |
| 24 | 2001 | 2010 | 8 | 8 | 192 | 9.30 | 1 | 24 | 11:00 p.m.-12:00 a.m. | 1 | 7.60 | 8 | 9 | Day 8: 12:00 a.m.-1:00 a.m. | 1 | 8 |
| The Flash | 2014 | 2023 | 9 | 9 | 184 | 9.60 | 1 | 15 | Out of Time | 1 | 3.80 | 9 | 6 | The Good, the Bad and the Lucky | 1 | 9 |
| Wings | 1990 | 1997 | 8 | 7 | 172 | 8.60 | 2 | 21 | Murder, She Roast | 1 | 6.40 | 8 | 22 | Raging Bull*&@! | 1 | 8 |
| Soy Luna | 2016 | 2026 | 4 | 3 | 160 | 9.10 | 2 | 80 | La final de la Rodafest en México, sobre ruedas (Parte 2) | 1 | 2.80 | 4 | 12 | Alas en los pies y un corazón expectante | 1 | 4 |
| Talking Tom & Friends | 2014 | 2021 | 5 | 5 | 158 | 9.20 | 1 | 51 | A Secret Worth Keeping: Part 3 | 1 | 5.40 | 5 | 16 | Tom the Guru | 1 | 5 |
| NCIS: New Orleans | 2014 | 2021 | 7 | 7 | 155 | 8.40 | 2 | 24 | Sleeping with the Enemy | 1 | 6.50 | 7 | 5 | Operation Drano: Part 1 | 1 | 7 |
| The Outer Limits | 1995 | 2002 | 7 | 7 | 152 | 8.40 | 2 | 1 | A Stitch in Time | 1 | 5.20 | 7 | 22 | Human Trials | 1 | 7 |
| Gomer Pyle: USMC | 1964 | 1969 | 5 | 5 | 150 | 8.80 | 2 | 13 | Gomer Minds His Sergeant's Car | 1 | 6.10 | 5 | 12 | The Wild Bull Returns | 1 | 5 |
| We Bare Bears | 2014 | 2019 | 4 | 4 | 139 | 9.60 | 2 | 16 | Yuri and the Bear | 1 | 6.30 | 4 | 34 | Ranger Norm | 1 | 4 |
| Get Smart | 1965 | 1970 | 5 | 5 | 138 | 8.80 | 2 | 3 | A Spy for a Spy | 1 | 6.40 | 5 | 13 | Ice Station Siegfried | 1 | 5 |
| 30 for 30 | 2009 |  | 5 | 4 | 135 | 8.50 | 1 | 25 | Once Brothers | 2 | 5.20 | 5 | 5 | No Scope: The Story of FaZe Clan | 1 | 5 |
| Emergency! | 1972 | 1979 | 7 | 6 | 131 | 9.00 | 2 | 4 | Virus | 1 | 6.50 | 7 | 3 | Survival on Charter #220 | 1 | 7 |
| In Treatment | 2008 | 2021 | 4 | 4 | 130 | 9.10 | 1 | 41 | Sophie: Week Nine | 1 | 5.60 | 4 | 24 | Brooke - Week 6 | 2 | 4 |
| Avengers Assemble | 2013 | 2019 | 5 | 5 | 127 | 8.30 | 2 | 12 | Widow's Run | 1 | 5.90 | 5 | 7 | T'Challa Royale | 1 | 5 |
| All American | 2018 | 2026 | 8 | 7 | 127 | 9.00 | 2 | 7 | Coming Home | 1 | 6.10 | 8 | 6 | Rebel Without a Pause | 1 | 8 |
| Bull | 2016 | 2022 | 6 | 6 | 125 | 8.60 | 2 | 22 | Death Sentence | 1 | 5.90 | 6 | 20 | The Envelope, Please | 1 | 6 |
| Batman | 1966 | 1968 | 3 | 3 | 120 | 8.40 | 2 | 40 | That Darn Catwoman | 2 | 5.70 | 3 | 19 | Nora Clavicle and the Ladies' Crime Club | 1 | 3 |
| Beyblade: Metal Fusion | 2009 | 2013 | 3 | 3 | 119 | 9.80 | 2 | 42 | The Dragon Emperor Descends | 1 | 7.70 | 3 | 40 | Diablo Nemesis: Part 2 | 1 | 3 |
| The Untouchables | 1959 | 1963 | 4 | 4 | 118 | 8.50 | 2 | 1 | The Rusty Heller Story | 3 | 7.00 | 4 | 9 | Come and Kill Me | 1 | 4 |
| Petticoat Junction | 1963 | 1970 | 7 | 4 | 118 | 8.00 | 1 | 4 | Is There a Doctor in the Roundhouse? | 2 | 5.80 | 7 | 20 | Susan B. Anthony, I Love You | 1 | 7 |
| Route 66 | 1960 | 1964 | 4 | 4 | 116 | 9.00 | 2 | 3 | Goodnight Sweet Blues | 1 | 5.50 | 4 | 11 | Come Home Greta Inger Gruenschaffen | 1 | 4 |
| Peter Gunn | 1958 | 1961 | 3 | 3 | 114 | 8.30 | 1 | 31 | Love Me to Death | 1 | 6.60 | 3 | 36 | Voodoo | 1 | 3 |
| The Kids in the Hall | 1988 | 2021 | 5 | 5 | 111 | 8.30 | 2 | 9 | Episode #2.9 | 1 | 6.80 | 5 | 3 | Episode #5.3 | 1 | 5 |
| Dynasty | 2017 | 2022 | 5 | 5 | 108 | 9.30 | 1 | 22 | Dead Scratch | 1 | 6.80 | 5 | 18 | A Writer of Dubious Talent | 1 | 5 |
| The Resident | 2018 | 2023 | 6 | 6 | 107 | 9.10 | 2 | 20 | If Not Now, When? | 1 | 6.90 | 6 | 2 | Peek and Shriek | 1 | 6 |
| Alias | 2001 | 2006 | 5 | 5 | 105 | 9.00 | 2 | 13 | Phase One | 1 | 7.10 | 5 | 5 | Out of the Box | 2 | 5 |
| Station 19 | 2018 | 2024 | 7 | 7 | 105 | 9.20 | 2 | 15 | Always Ready | 1 | 6.50 | 7 | 3 | True Colors | 1 | 7 |
| Weeds | 2005 | 2012 | 8 | 8 | 102 | 8.90 | 2 | 12 | Pittsburgh | 1 | 6.90 | 8 | 10 | Threshold | 2 | 8 |
| Nip/Tuck | 2003 | 2010 | 6 | 6 | 100 | 8.90 | 2 | 16 | Joan Rivers | 1 | 6.70 | 6 | 17 | Christian Troy II | 1 | 6 |
| Young Justice | 2010 | 2022 | 4 | 4 | 98 | 9.70 | 2 | 19 | Summit | 1 | 6.80 | 4 | 14 | Nautical Twilight | 1 | 4 |
| The High Chaparral | 1967 | 1971 | 4 | 4 | 97 | 8.80 | 2 | 2 | Ten Little Indians | 1 | 6.80 | 4 | 13 | The Badge | 1 | 4 |
| The Valley of the Wolves | 2003 | 2005 | 4 | 4 | 97 | 9.00 | 2 | 45 | 45. Bölüm | 1 | 6.80 | 4 | 87 | 87. Bölüm | 1 | 4 |
| Welcome Back, Kotter | 1975 | 1979 | 4 | 4 | 95 | 7.80 | 1 | 20 | The Telethon | 1 | 5.70 | 4 | 10 | Washington's Clone | 2 | 4 |
| My Favorite Martian | 1963 | 1966 | 3 | 3 | 94 | 8.20 | 2 | 26 | We Love You, Miss Pringle | 1 | 6.40 | 3 | 8 | Bottled Martian | 1 | 3 |
| Golden Boy | 2022 | 2025 | 3 | 3 | 93 | 8.70 | 2 | 31 | Episode #2.31 | 1 | 4.10 | 3 | 16 | Episode #3.16 | 2 | 3 |
| Scorpion | 2014 | 2018 | 4 | 4 | 93 | 8.60 | 2 | 10 | Arrivals and Departures | 1 | 6.20 | 4 | 22 | A Lie in the Sand | 1 | 4 |
| No One Could Live Here | 2003 | 2006 | 5 | 5 | 91 | 8.80 | 1 | 9 | Érase una de miedo | 1 | 6.30 | 5 | 5 | Érase un anuncio | 1 | 5 |
| Chuck | 2007 | 2012 | 5 | 5 | 91 | 9.50 | 2 | 22 | Chuck Versus the Ring | 1 | 7.40 | 5 | 2 | Chuck Versus the Bearded Bandit | 1 | 5 |
| The Commish | 1991 | 1996 | 5 | 4 | 88 | 8.40 | 2 | 5 | The Witches of Eastbridge | 1 | 7.10 | 5 | 1 | In the Shadows of the Gallows | 1 | 5 |
| Picket Fences | 1992 | 1996 | 4 | 4 | 87 | 8.60 | 1 | 14 | Bad Moons Rising | 1 | 6.80 | 4 | 15 | Bottled | 1 | 4 |
| Sliders | 1995 | 2000 | 5 | 4 | 87 | 8.30 | 2 | 8 | Post Traumatic Slide Syndrome | 1 | 4.80 | 5 | 1 | The Unstuck Man | 1 | 5 |
| The Suite Life of Zack & Cody | 2005 | 2008 | 3 | 3 | 87 | 8.20 | 1 | 19 | The Ghost of Suite 613 | 1 | 6.60 | 3 | 17 | Foiled Again | 2 | 3 |
| Saved by the Bell | 1989 | 1992 | 4 | 4 | 86 | 8.20 | 2 | 9 | Jessie's Song | 1 | 6.40 | 4 | 22 | Best Summer of My Life | 1 | 4 |
| Cybill | 1995 | 1998 | 4 | 4 | 86 | 8.40 | 2 | 4 | Cybill with an 'S' | 1 | 6.80 | 4 | 11 | The Golden Years | 1 | 4 |
| Timon & Pumbaa | 1995 | 1999 | 3 | 3 | 85 | 7.60 | 1 | 22 | Let's Serengeti Out of Here/Congo on Like This | 1 | 6.20 | 3 | 35 | Stay Away from my Honey!/Sitting Pretty Awful | 5 | 3 |
| For My Son | 2015 | 2017 | 3 | 3 | 82 | 9.40 | 1 | 23 | Episode #1.23 | 1 | 6.60 | 3 | 18 | Episode #3.18 | 1 | 3 |
| True Blood | 2008 | 2014 | 7 | 7 | 81 | 8.80 | 2 | 8 | Timebomb | 1 | 5.40 | 7 | 10 | Thank You | 1 | 7 |

###### CSV exports

| file | total_rows | exported_rows | truncated | gold_directory |
| --- | --- | --- | --- | --- |
| q5_series_decline.csv | 171 | 171 | false | data/gold/exploration |

<!-- AUTO:q5:end -->

### Q6. Actors successful across languages

#### Results

<!-- AUTO:q6:start -->

##### Q6 - Actors and actresses successful in several original languages

###### Parameters

| parameter | value |
| --- | --- |
| feature_film.title_types | movie |
| feature_film.min_runtime_minutes | 40 |
| feature_film.include_adult | false |
| min_rating | 7 |
| min_votes | 10000 |
| categories | actor, actress |
| multilingual_films | exclude |
| language_aliases | cmn->zh, nb->no, nn->no |
| language_sources | wikidata_P364, akas_original_language, akas_region |
| successful_films | 4974 |
| films_used_in_the_analysis | 4311 |
| people_with_2_or_more_languages | 650 |
| people_with_3_or_more_languages | 74 |

###### Original language coverage of the successful films

| language_source | films | films_with_several_languages | pct_of_successful_films |
| --- | --- | --- | --- |
| wikidata_P364 | 4896 | 593 | 98.43 |
| unknown | 70 | 0 | 1.41 |
| akas_region | 8 | 0 | 0.16 |

###### Most frequent original languages

| language | language_label | films |
| --- | --- | --- |
| en | English | 2802 |
| hi | Hindi | 271 |
| fr | French | 202 |
| ja | Japanese | 185 |
| tr | Turkish | 86 |
| it | Italian | 80 |
| ta | Tamil | 79 |
| es | Spanish | 78 |
| de | German | 65 |
| ko | Korean | 59 |
| ml | Malayalam | 40 |
| te | Telugu | 36 |
| sv | Swedish | 34 |
| ru | Russian | 31 |
| zh | Mandarin | 31 |

###### People per number of languages

| n_languages | people |
| --- | --- |
| 2 | 576 |
| 3 | 68 |
| 4 | 6 |

###### Successful in 3 or more languages

_Showing 50 of 74 rows_

| primaryName | n_languages | languages | n_successful_films | examples |
| --- | --- | --- | --- | --- |
| Prakash Raj | 4 | Hindi, Kannada, Tamil, Telugu | 24 | Hindi: Khakee (2004); Kannada: K.G.F: Chapter 2 (2022); Tamil: Jai Bhim (2021); Telugu: Rangasthalam (2018) |
| Jackie Chan | 4 | Cantonese, English, Mandarin, Yue Chinese | 17 | Cantonese: Drunken Master II (1994); English: Kung Fu Panda (2008); Mandarin: The Shadow's Edge (2025); Yue Chinese: Drunken Master (1978) |
| Ashish Vidyarthi | 4 | Hindi, Malayalam, Tamil, Telugu | 7 | Hindi: Barfi! (2012); Malayalam: Aavesham (2024); Tamil: Ghilli (2004); Telugu: Pokiri (2006) |
| Bruno Ganz | 4 | English, German, Italian, Modern Greek | 6 | English: A Hidden Life (2019); German: Downfall (2004); Italian: Bread and Tulips (2000); Modern Greek: Eternity and a Day (1998) |
| Sobhita Dhulipala | 4 | Hindi, Malayalam, Tamil, Telugu | 5 | Hindi: Psycho Raman (2016); Malayalam: Kurup (2021); Tamil: Ponniyin Selvan: Part I (2022); Telugu: Goodachari (2018) |
| Franco Nero | 4 | English, German, Italian, Spanish | 4 | English: Die Hard 2 (1990); German: The Collini Case (2019); Italian: Django (1966); Spanish: Tristana (1970) |
| Amitabh Bachchan | 3 | English, Hindi, Telugu | 26 | English: The Great Gatsby (2013); Hindi: Veer Zaara (2004); Telugu: Manam (2014) |
| Nassar | 3 | Hindi, Tamil, Telugu | 21 | Hindi: Article 15 (2019); Tamil: Master (2021); Telugu: Baahubali 2: The Conclusion (2017) |
| Max von Sydow | 3 | English, French, Swedish | 13 | English: Shutter Island (2010); French: The Diving Bell and the Butterfly (2007); Swedish: Winter Light (1963) |
| Catherine Deneuve | 3 | English, French, Spanish | 11 | English: Dancer in the Dark (2000); French: Persepolis (2007); Spanish: Tristana (1970) |
| Sanjay Dutt | 3 | Hindi, Kannada, Tamil | 11 | Hindi: Dhurandhar (2025); Kannada: K.G.F: Chapter 2 (2022); Tamil: Leo (2023) |
| Ron Perlman | 3 | English, French, artistic language | 10 | English: Drive (2011); French: The City of Lost Children (1995); artistic language: Quest for Fire (1981) |
| Madhavan | 3 | English, Hindi, Tamil | 10 | English: Rocketry: The Nambi Effect (2022); Hindi: 3 Idiots (2009); Tamil: Vikram Vedha (2017) |
| Fahadh Faasil | 3 | Malayalam, Tamil, Telugu | 10 | Malayalam: Aavesham (2024); Tamil: Vikram (2022); Telugu: Pushpa: The Rise - Part 1 (2021) |
| Maggie Cheung | 3 | Cantonese, Mandarin, Yue Chinese | 9 | Cantonese: In the Mood for Love (2000); Mandarin: Hero (2002); Yue Chinese: Police Story (1985) |
| Mohanlal | 3 | Hindi, Malayalam, Tamil | 9 | Hindi: Company (2002); Malayalam: Drishyam (2013); Tamil: Jailer (2023) |
| Tony Leung Chiu-wai | 3 | Cantonese, German, Mandarin | 9 | Cantonese: In the Mood for Love (2000); German: Red Cliff II (2009); Mandarin: Hero (2002) |
| Jeanne Moreau | 3 | English, French, Italian | 9 | English: The Trial (1962); French: Elevator to the Gallows (1958); Italian: La Notte (1961) |
| Amrish Puri | 3 | English, Hindi, Tamil | 9 | English: Indiana Jones and the Temple of Doom (1984); Hindi: Dilwale Dulhania Le Jayenge (1995); Tamil: Thalapathi (1991) |
| Yun-Fat Chow | 3 | Cantonese, English, Mandarin | 8 | Cantonese: Hard Boiled (1992); English: A Better Tomorrow II (1987); Mandarin: Crouching Tiger, Hidden Dragon (2000) |
| Jean Reno | 3 | English, French, Italian | 8 | English: Léon: The Professional (1994); French: The Big Blue (1988); Italian: The Tiger and the Snow (2005) |
| Michelle Yeoh | 3 | Cantonese, English, Mandarin | 8 | Cantonese: Police Story 3: Supercop (1992); English: Kung Fu Panda 2 (2011); Mandarin: Crouching Tiger, Hidden Dragon (2000) |
| Richard Harris | 3 | English, Italian, Russian | 8 | English: Gladiator (2000); Italian: Red Desert (1964); Russian: The Barber of Siberia (1998) |
| Donnie Yen | 3 | Cantonese, English, Mandarin | 8 | Cantonese: Ip Man (2008); English: Rogue One: A Star Wars Story (2016); Mandarin: Hero (2002) |
| Valeria Golino | 3 | English, French, Italian | 7 | English: Rain Man (1988); French: Portrait of a Lady on Fire (2019); Italian: Human Capital (2013) |
| Kishore Kumar G. | 3 | Kannada, Malayalam, Tamil | 7 | Kannada: Kantara (2022); Malayalam: Kannur Squad (2023); Tamil: Vada Chennai (2018) |
| Isabelle Adjani | 3 | English, French, German | 6 | English: Possession (1981); French: The Tenant (1976); German: Nosferatu the Vampyre (1979) |
| Julie Delpy | 3 | English, French, German | 6 | English: Before Sunrise (1995); French: Three Colors: Blue (1993); German: Europa Europa (1990) |
| Rutger Hauer | 3 | Dutch, English, German | 6 | Dutch: Soldier of Orange (1977); English: Batman Begins (2005); German: Knockin' on Heaven's Door (1997) |
| Jet Li | 3 | Cantonese, English, Mandarin | 6 | Cantonese: Once Upon a Time in China (1991); English: Unleashed (2005); Mandarin: Hero (2002) |
| Leslie Cheung | 3 | Cantonese, English, Mandarin | 6 | Cantonese: A Better Tomorrow (1986); English: A Better Tomorrow II (1987); Mandarin: Farewell My Concubine (1993) |
| Takeshi Kaneshiro | 3 | Cantonese, German, Mandarin | 6 | Cantonese: Chungking Express (1994); German: Red Cliff II (2009); Mandarin: House of Flying Daggers (2004) |
| Sachin Khedekar | 3 | Hindi, Tamil, Telugu | 6 | Hindi: Rustom (2016); Tamil: 13B: Fear Has a New Address (2009); Telugu: Sita Ramam (2022) |
| Diane Kruger | 3 | English, French, German | 6 | English: Mr. Nobody (2009); French: Anything for Her (2008); German: In the Fade (2017) |
| Murli Sharma | 3 | Hindi, Tamil, Telugu | 6 | Hindi: OMG: Oh My God! (2012); Tamil: 13B: Fear Has a New Address (2009); Telugu: Shyam Singha Roy (2021) |
| Kajal Aggarwal | 3 | Hindi, Tamil, Telugu | 6 | Hindi: Special 26 (2013); Tamil: Mersal (2017); Telugu: Magadheera (2009) |
| Rao Ramesh | 3 | Kannada, Tamil, Telugu | 6 | Kannada: K.G.F: Chapter 2 (2022); Tamil: Jai Bhim (2021); Telugu: Pushpa: The Rise - Part 1 (2021) |
| Sammo Kam-Bo Hung | 3 | Cantonese, English, Yue Chinese | 5 | Cantonese: The Legend Is Born: Ip Man (2010); English: Ip Man 2 (2010); Yue Chinese: Project A (1983) |
| Tinnu Anand | 3 | Hindi, Tamil, Telugu | 5 | Hindi: Ghajini (2008); Tamil: Nayakan (1987); Telugu: Lucky Baskhar (2024) |
| Féodor Atkine | 3 | English, French, Spanish | 5 | English: Love and Death (1975); French: Ernest & Celestine (2012); Spanish: High Heels (1991) |
| Kim Bodnia | 3 | Danish, English, Hindi | 5 | Danish: Pusher (1996); English: F1: The Movie (2025); Hindi: Delhi Belly (2011) |
| Golshifteh Farahani | 3 | English, French, Persian | 5 | English: Body of Lies (2008); French: Chicken with Plums (2011); Persian: The Music Man (2007) |
| Pierfrancesco Favino | 3 | English, French, Italian | 5 | English: Rush (2013); French: The Count of Monte Cristo (2024); Italian: The Unknown Woman (2006) |
| Jun Hu | 3 | Cantonese, German, Mandarin | 5 | Cantonese: Infernal Affairs II (2003); German: Red Cliff II (2009); Mandarin: Red Cliff (2008) |
| Kishore Kadam | 3 | Hindi, Marathi, Tamil | 5 | Hindi: Special 26 (2013); Marathi: Gondhal (2025); Tamil: Theeran Adhigaram Ondru (2017) |
| Carina Lau | 3 | Cantonese, Mandarin, Yue Chinese | 5 | Cantonese: Days of Being Wild (1990); Mandarin: Let the Bullets Fly (2010); Yue Chinese: Project A 2 (1987) |
| R. Sarathkumar | 3 | Kannada, Tamil, Telugu | 5 | Kannada: Raajakumara (2017); Tamil: Ponniyin Selvan: Part I (2022); Telugu: Bharath Ane Nenu (2018) |
| Matthias Schoenaerts | 3 | Dutch, English, French | 5 | Dutch: Loft (2008); English: The Drop (2014); French: Rust and Bone (2012) |
| Pradeep Singh Rawat | 3 | Hindi, Tamil, Telugu | 5 | Hindi: Ghajini (2008); Tamil: Ghajini (2005); Telugu: 1: Nenokkadine (2014) |
| Roman Polanski | 3 | English, French, Polish | 4 | English: Chinatown (1974); French: The Tenant (1976); Polish: Knife in the Water (1962) |

###### Successful in 2 or more languages

_Showing 50 of 650 rows_

| primaryName | n_languages | languages | n_successful_films | examples |
| --- | --- | --- | --- | --- |
| Prakash Raj | 4 | Hindi, Kannada, Tamil, Telugu | 24 | Hindi: Khakee (2004); Kannada: K.G.F: Chapter 2 (2022); Tamil: Jai Bhim (2021); Telugu: Rangasthalam (2018) |
| Jackie Chan | 4 | Cantonese, English, Mandarin, Yue Chinese | 17 | Cantonese: Drunken Master II (1994); English: Kung Fu Panda (2008); Mandarin: The Shadow's Edge (2025); Yue Chinese: Drunken Master (1978) |
| Ashish Vidyarthi | 4 | Hindi, Malayalam, Tamil, Telugu | 7 | Hindi: Barfi! (2012); Malayalam: Aavesham (2024); Tamil: Ghilli (2004); Telugu: Pokiri (2006) |
| Bruno Ganz | 4 | English, German, Italian, Modern Greek | 6 | English: A Hidden Life (2019); German: Downfall (2004); Italian: Bread and Tulips (2000); Modern Greek: Eternity and a Day (1998) |
| Sobhita Dhulipala | 4 | Hindi, Malayalam, Tamil, Telugu | 5 | Hindi: Psycho Raman (2016); Malayalam: Kurup (2021); Tamil: Ponniyin Selvan: Part I (2022); Telugu: Goodachari (2018) |
| Franco Nero | 4 | English, German, Italian, Spanish | 4 | English: Die Hard 2 (1990); German: The Collini Case (2019); Italian: Django (1966); Spanish: Tristana (1970) |
| Amitabh Bachchan | 3 | English, Hindi, Telugu | 26 | English: The Great Gatsby (2013); Hindi: Veer Zaara (2004); Telugu: Manam (2014) |
| Nassar | 3 | Hindi, Tamil, Telugu | 21 | Hindi: Article 15 (2019); Tamil: Master (2021); Telugu: Baahubali 2: The Conclusion (2017) |
| Max von Sydow | 3 | English, French, Swedish | 13 | English: Shutter Island (2010); French: The Diving Bell and the Butterfly (2007); Swedish: Winter Light (1963) |
| Catherine Deneuve | 3 | English, French, Spanish | 11 | English: Dancer in the Dark (2000); French: Persepolis (2007); Spanish: Tristana (1970) |
| Sanjay Dutt | 3 | Hindi, Kannada, Tamil | 11 | Hindi: Dhurandhar (2025); Kannada: K.G.F: Chapter 2 (2022); Tamil: Leo (2023) |
| Ron Perlman | 3 | English, French, artistic language | 10 | English: Drive (2011); French: The City of Lost Children (1995); artistic language: Quest for Fire (1981) |
| Madhavan | 3 | English, Hindi, Tamil | 10 | English: Rocketry: The Nambi Effect (2022); Hindi: 3 Idiots (2009); Tamil: Vikram Vedha (2017) |
| Fahadh Faasil | 3 | Malayalam, Tamil, Telugu | 10 | Malayalam: Aavesham (2024); Tamil: Vikram (2022); Telugu: Pushpa: The Rise - Part 1 (2021) |
| Maggie Cheung | 3 | Cantonese, Mandarin, Yue Chinese | 9 | Cantonese: In the Mood for Love (2000); Mandarin: Hero (2002); Yue Chinese: Police Story (1985) |
| Mohanlal | 3 | Hindi, Malayalam, Tamil | 9 | Hindi: Company (2002); Malayalam: Drishyam (2013); Tamil: Jailer (2023) |
| Tony Leung Chiu-wai | 3 | Cantonese, German, Mandarin | 9 | Cantonese: In the Mood for Love (2000); German: Red Cliff II (2009); Mandarin: Hero (2002) |
| Jeanne Moreau | 3 | English, French, Italian | 9 | English: The Trial (1962); French: Elevator to the Gallows (1958); Italian: La Notte (1961) |
| Amrish Puri | 3 | English, Hindi, Tamil | 9 | English: Indiana Jones and the Temple of Doom (1984); Hindi: Dilwale Dulhania Le Jayenge (1995); Tamil: Thalapathi (1991) |
| Yun-Fat Chow | 3 | Cantonese, English, Mandarin | 8 | Cantonese: Hard Boiled (1992); English: A Better Tomorrow II (1987); Mandarin: Crouching Tiger, Hidden Dragon (2000) |
| Jean Reno | 3 | English, French, Italian | 8 | English: Léon: The Professional (1994); French: The Big Blue (1988); Italian: The Tiger and the Snow (2005) |
| Michelle Yeoh | 3 | Cantonese, English, Mandarin | 8 | Cantonese: Police Story 3: Supercop (1992); English: Kung Fu Panda 2 (2011); Mandarin: Crouching Tiger, Hidden Dragon (2000) |
| Richard Harris | 3 | English, Italian, Russian | 8 | English: Gladiator (2000); Italian: Red Desert (1964); Russian: The Barber of Siberia (1998) |
| Donnie Yen | 3 | Cantonese, English, Mandarin | 8 | Cantonese: Ip Man (2008); English: Rogue One: A Star Wars Story (2016); Mandarin: Hero (2002) |
| Valeria Golino | 3 | English, French, Italian | 7 | English: Rain Man (1988); French: Portrait of a Lady on Fire (2019); Italian: Human Capital (2013) |
| Kishore Kumar G. | 3 | Kannada, Malayalam, Tamil | 7 | Kannada: Kantara (2022); Malayalam: Kannur Squad (2023); Tamil: Vada Chennai (2018) |
| Isabelle Adjani | 3 | English, French, German | 6 | English: Possession (1981); French: The Tenant (1976); German: Nosferatu the Vampyre (1979) |
| Julie Delpy | 3 | English, French, German | 6 | English: Before Sunrise (1995); French: Three Colors: Blue (1993); German: Europa Europa (1990) |
| Rutger Hauer | 3 | Dutch, English, German | 6 | Dutch: Soldier of Orange (1977); English: Batman Begins (2005); German: Knockin' on Heaven's Door (1997) |
| Jet Li | 3 | Cantonese, English, Mandarin | 6 | Cantonese: Once Upon a Time in China (1991); English: Unleashed (2005); Mandarin: Hero (2002) |
| Leslie Cheung | 3 | Cantonese, English, Mandarin | 6 | Cantonese: A Better Tomorrow (1986); English: A Better Tomorrow II (1987); Mandarin: Farewell My Concubine (1993) |
| Takeshi Kaneshiro | 3 | Cantonese, German, Mandarin | 6 | Cantonese: Chungking Express (1994); German: Red Cliff II (2009); Mandarin: House of Flying Daggers (2004) |
| Sachin Khedekar | 3 | Hindi, Tamil, Telugu | 6 | Hindi: Rustom (2016); Tamil: 13B: Fear Has a New Address (2009); Telugu: Sita Ramam (2022) |
| Diane Kruger | 3 | English, French, German | 6 | English: Mr. Nobody (2009); French: Anything for Her (2008); German: In the Fade (2017) |
| Murli Sharma | 3 | Hindi, Tamil, Telugu | 6 | Hindi: OMG: Oh My God! (2012); Tamil: 13B: Fear Has a New Address (2009); Telugu: Shyam Singha Roy (2021) |
| Kajal Aggarwal | 3 | Hindi, Tamil, Telugu | 6 | Hindi: Special 26 (2013); Tamil: Mersal (2017); Telugu: Magadheera (2009) |
| Rao Ramesh | 3 | Kannada, Tamil, Telugu | 6 | Kannada: K.G.F: Chapter 2 (2022); Tamil: Jai Bhim (2021); Telugu: Pushpa: The Rise - Part 1 (2021) |
| Sammo Kam-Bo Hung | 3 | Cantonese, English, Yue Chinese | 5 | Cantonese: The Legend Is Born: Ip Man (2010); English: Ip Man 2 (2010); Yue Chinese: Project A (1983) |
| Tinnu Anand | 3 | Hindi, Tamil, Telugu | 5 | Hindi: Ghajini (2008); Tamil: Nayakan (1987); Telugu: Lucky Baskhar (2024) |
| Féodor Atkine | 3 | English, French, Spanish | 5 | English: Love and Death (1975); French: Ernest & Celestine (2012); Spanish: High Heels (1991) |
| Kim Bodnia | 3 | Danish, English, Hindi | 5 | Danish: Pusher (1996); English: F1: The Movie (2025); Hindi: Delhi Belly (2011) |
| Golshifteh Farahani | 3 | English, French, Persian | 5 | English: Body of Lies (2008); French: Chicken with Plums (2011); Persian: The Music Man (2007) |
| Pierfrancesco Favino | 3 | English, French, Italian | 5 | English: Rush (2013); French: The Count of Monte Cristo (2024); Italian: The Unknown Woman (2006) |
| Jun Hu | 3 | Cantonese, German, Mandarin | 5 | Cantonese: Infernal Affairs II (2003); German: Red Cliff II (2009); Mandarin: Red Cliff (2008) |
| Kishore Kadam | 3 | Hindi, Marathi, Tamil | 5 | Hindi: Special 26 (2013); Marathi: Gondhal (2025); Tamil: Theeran Adhigaram Ondru (2017) |
| Carina Lau | 3 | Cantonese, Mandarin, Yue Chinese | 5 | Cantonese: Days of Being Wild (1990); Mandarin: Let the Bullets Fly (2010); Yue Chinese: Project A 2 (1987) |
| R. Sarathkumar | 3 | Kannada, Tamil, Telugu | 5 | Kannada: Raajakumara (2017); Tamil: Ponniyin Selvan: Part I (2022); Telugu: Bharath Ane Nenu (2018) |
| Matthias Schoenaerts | 3 | Dutch, English, French | 5 | Dutch: Loft (2008); English: The Drop (2014); French: Rust and Bone (2012) |
| Pradeep Singh Rawat | 3 | Hindi, Tamil, Telugu | 5 | Hindi: Ghajini (2008); Tamil: Ghajini (2005); Telugu: 1: Nenokkadine (2014) |
| Roman Polanski | 3 | English, French, Polish | 4 | English: Chinatown (1974); French: The Tenant (1976); Polish: Knife in the Water (1962) |

###### CSV exports

| file | total_rows | exported_rows | truncated | gold_directory |
| --- | --- | --- | --- | --- |
| q6_multilingual_actors.csv | 650 | 650 | false | data/gold/exploration |
| q6_multilingual_actors_three_or_more.csv | 74 | 74 | false | data/gold/exploration |
| q6_multilingual_actors_coverage.csv | 3 | 3 | false | data/gold/exploration |

<!-- AUTO:q6:end -->

### Q7. Actors with an early career peak

#### Results

<!-- AUTO:q7:start -->

##### Q7 - Long-career actors and actresses whose ratings peaked early

###### Parameters

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

###### Population summary (early peak versus others)

| early_peak | people | avg_career_years | avg_films | avg_peak_position | avg_top_k_mean_position | avg_first_minus_second_half | avg_rating_slope | pct_negative_slope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| true | 1557 | 35.18 | 27.24 | 0.14 | 0.27 | 0.66 | -0.04 | 96.85 |
| false | 1971 | 33.74 | 28.35 | 0.57 | 0.48 | 0.18 | -0.01 | 67.38 |

###### Actors and actresses with an early peak

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

###### CSV exports

| file | total_rows | exported_rows | truncated | gold_directory |
| --- | --- | --- | --- | --- |
| q7_early_peak_actors.csv | 1557 | 1557 | false | data/gold/exploration |
| q7_early_peak_actors_summary.csv | 2 | 2 | false | data/gold/exploration |

<!-- AUTO:q7:end -->

### Q8. Professionals with multiple roles

#### Results

<!-- AUTO:q8:start -->

##### Q8 - Multi-talented professionals: multi-role films versus single-role films

###### Parameters

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

###### Multi-talented people per set of career roles

| career_roles | people |
| --- | --- |
| actor+director | 152 |
| actor+director+writer | 440 |
| actor+writer | 392 |
| director+writer | 2669 |

###### Paired comparison per role combination on the same film

| combination | people | multi_role_films | mean_rating_multi_role | mean_rating_single_role | mean_diff | median_diff | std_diff | pct_people_better_multi_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| any combination | 2734 | 14226 | 6.29 | 6.17 | 0.11 | 0.12 | 0.78 | 57.57 |
| actor+director | 169 | 332 | 6.15 | 6.21 | -0.06 | 0.06 | 0.86 | 55.03 |
| actor+director+writer | 540 | 1299 | 6.20 | 6.13 | 0.07 | 0.10 | 0.97 | 53.89 |
| actor+writer | 468 | 1323 | 6.16 | 6.05 | 0.11 | 0.13 | 0.94 | 57.26 |
| director+writer | 2296 | 11272 | 6.31 | 6.20 | 0.12 | 0.12 | 0.79 | 57.45 |

###### People with the most multi-role films

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

###### CSV exports

| file | total_rows | exported_rows | truncated | gold_directory |
| --- | --- | --- | --- | --- |
| q8_multi_talented_summary.csv | 5 | 5 | false | data/gold/exploration |
| q8_multi_talented_career_roles.csv | 4 | 4 | false | data/gold/exploration |
| q8_multi_talented.csv | 6207 | 6207 | false | data/gold/exploration |

<!-- AUTO:q8:end -->

### Methodological Explanation

#### Methodology and why it was chosen

All eight questions read the silver tables and share the same conventions, defined in `conf/settings.yaml` and `exploration/base.py`:

- A **feature-length movie** is a title with `titleType = movie` and a runtime of at least 40 minutes, adult titles excluded. 40 minutes is the usual threshold for a feature film.
- Any analysis based on ratings keeps only movies with **at least 1,000 votes**, which leaves 49,434 movies. With fewer votes, a handful of users can give a movie almost any score.
- Genres are **exploded**: a movie tagged `Drama,Romance` counts in both genres.
- **Popularity** means the number of votes.

Each question writes a Markdown summary, with its parameters at the top, and a CSV containing the full results. This way, the thresholds always appear next to the numbers.

**Q1.** For each genre with at least 30 movies, we compute the mean, the standard deviation and the quartiles of the runtime. A movie is an outlier when |z| > 2 **or** when it falls outside the fences [Q1 − 1.5·IQR, Q3 + 1.5·IQR]. We use two methods because runtimes are very skewed. A few extremely long documentaries push the standard deviation of Documentary to 223 minutes, which makes the z-score threshold so wide that it catches almost nothing. The IQR fences rely on quartiles and are not affected by those extremes. In practice, most outliers are found by the IQR alone (for Drama: 6,743 by IQR only, 1,964 by both, 0 by z-score only). We keep the union and record which method fired.

**Q2.** We sum `numVotes` per (year, genre) for 1980–2025 and rank genres with `dense_rank`, so that ties share a rank. We also keep the number of movies and the vote-weighted rating, to see whether a genre is popular because it has many movies or a few very-watched ones. Votes measure audience. A count of movies would measure production, and an average rating says nothing about how many people watched.

**Q3.** For each year, we compare the top 3 genres with all other genres combined: share of votes, vote-weighted rating and ratio between the two groups. We then aggregate by decade and count how many years each genre appears in the top 3.

**Q4.** Directors come from the union of `title.crew.directors` and the `director` category of `title.principals`, deduplicated, because each source misses some credits. We keep directors with exactly one movie rated ≥ 8.0 and at least two other movies whose average rating is ≤ 6.0. We read "multiple" as "at least two".

**Q5.** We keep series with at least 3 seasons that each have ≥ 10 rated episodes (≥ 50 votes per episode). The last season is identified *before* the vote filter. Otherwise, a recent season with few votes would disappear, and the season before it would wrongly be treated as the last one. Ties are handled in `all` mode: when several episodes share the worst or best rating, all of them must sit in the expected seasons.

**Q6.** A movie is a success if it is rated ≥ 7.0 with ≥ 10,000 votes. Its original language comes from Wikidata (property P364, found through the IMDb ID, P345), with `title.akas` as a fallback. `title.akas` lists release titles by *region*, and a region is not a language. An Indian film has region `IN` whether it is in Hindi, Tamil or Telugu, which matters for actors like Prakash Raj. Movies with several original languages are excluded, so that a single film cannot add two languages to an actor's count. Together with the 70 movies whose language is unknown, this leaves 4,311 of the 4,974 successful movies.

**Q7.** We keep actors and actresses whose career lasts at least 20 years (from their first to their last rated movie) and who have at least 15 rated movies. A career has an *early peak* when the best movie falls in the first third of the career **and** the average rating of the first half is higher than that of the second half. Requiring both conditions avoids calling a career "early peak" because of one lucky early hit. We also compute the slope of rating against year (`covar_samp / var_samp`) as a continuous measure.

**Q8.** A person is multi-talented if they hold at least two of the roles {director, writer, actor}, with at least 3 movies in each. For each person, we compare the average rating of the movies where they combine roles with the movies where they hold a single role. The comparison is done *per person*, so each person is their own control. Comparing all multi-role movies with all single-role movies would mostly compare different people.

#### Alternatives considered and trade-offs

- **Thresholds.** `min_votes = 1,000` trades coverage for reliability. A threshold of 10,000 would remove most older and non-English movies. With 100, obscure titles rated 9+ would dominate, and even at 1,000 this still happens in Q4 with very recent films. We considered a Bayesian weighted rating, which pulls low-vote ratings toward the mean, but it adds a parameter and makes the results harder to explain.
- **Q1.** We could have used only the z-score (simple, but unreliable on skewed genres), only the IQR, or a robust z-score based on the median absolute deviation. We kept the two standard methods side by side.
- **Q2/Q3.** We could have measured popularity by number of movies or by average rating. Votes favour recent movies, because IMDb users vote more for what they watch now. We accepted this bias because the question is about popularity.
- **Q6.** Using `title.akas` alone would have avoided an external source, but it confuses region and language. Wikidata adds a dependency and gives the language of 98.4 % of the movies.
- **Q7.** We could have used only one of the two measures. The slope is affected by the general decline of ratings over careers. The halves-and-third rule is closer to the wording of the question.
- **Q8.** A regression with one fixed effect per person would test the same idea and give a confidence interval. We kept the simpler paired comparison.

### Key takeaways

- **Drama dominates.** It ranks first in 41 of the 46 years and appears in the top 3 every year, with 15–33 % of the votes (peak in 1994). Part of this is mechanical: Drama is the most common tag (196,130 of the 456,414 feature films), and with exploded genres, every "drama + something" movie adds its votes to Drama.
- **The top 3 genres take 42–47 % of all votes** and are slightly better rated than the rest (+0.02 to +0.25 points depending on the decade). This means more than half of the audience goes to the ~18 other genres.
- **The lead of the top 3 comes partly from volume.** In the 1990s and 2000s, top-3 films actually get fewer votes per film than the rest (ratio 0.88 and 0.84): these genres win because they have more films. The rating gap is not stable either; in some years the rest is better rated (−0.34 in 2008).
- **Runtime outliers are mostly long movies** (30,234 longer than normal against 5,323 shorter), and the count depends heavily on the method used. The most extreme cases are experimental works (*Logistics*, 2012, listed at 51,420 minutes) and silent-era serials (*Les Vampires*, 421 minutes), not mainstream films.
- **Rating-based results are sensitive to vote counts.** The first two directors in Q4 owe their place to 2026 films rated 9.8 and 9.3 with only 5,026 and 1,760 votes. Ratings from early, enthusiastic voters like these will probably drop. Irvin Kershner is the textbook case: *The Empire Strikes Back* is rated 8.7 with 1.5 M votes, while his 9 other movies average 5.94. M. Night Shyamalan (*The Sixth Sense*, 15 other movies averaging 5.87) and James McTeigue (*V for Vendetta*) are also on the list of 47. Two rows (Sateesh Paramveda and Satish Paramvedha) look like the same person under two IMDb IDs, a duplicate that our key checks cannot detect.
- **171 of 1,364 eligible series (12.5 %)** have their worst episode in the last season and their best in the first two (e.g. *The Flash*: 9.6 in season 1, 3.8 in season 9).
- **650 people succeeded in ≥ 2 languages and 74 in ≥ 3.** English dominates the successful movies (2,802), followed by Hindi, French and Japanese. Indian cinema produces many multilingual careers (Prakash Raj: 4 languages). One limit is that the language labels are noisy. Wikidata separates Cantonese and Yue Chinese (Jackie Chan, Maggie Cheung, Carina Lau), tags *Red Cliff II* as German and *Quest for Fire* as an "artistic language". A few counts are therefore one language too high.
- **44 % of long careers (1,557 of 3,528) peak early** (e.g. Edward Furlong with *Terminator 2*, Shelley Duvall with *The Shining*), but even among the others, two thirds have a negative slope. Ratings tend to decline over a career in general. The likely reasons are that old movies still rated today are the ones remembered for being good, and that actors take smaller roles later in their career.
- **Combining roles goes with a small gain**: +0.12 points in median, and 57.6 % of people are rated higher when they combine roles. The effect is small next to the spread between people (standard deviation 0.78), but with 2,734 people the mean difference is about 7 standard errors above zero, so it is unlikely to be noise. Individual cases go both ways: Woody Allen gains +1.02 when he combines roles, Tyler Perry loses −1.07. The gain probably reflects selection: people write and direct their personal projects. Actor + director is the only combination with a negative mean difference (−0.06).

## 3. Data Enrichment

### Results

<!-- AUTO:enrichment:start -->

#### Enrichment scope

##### Parameters

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

##### Scope size

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

##### Films per decade

| decade | films |
| --- | --- |
| 1980 | 1403 |
| 1990 | 1433 |
| 2000 | 1443 |
| 2010 | 1595 |
| 2020 | 947 |

#### Enrichment coverage

##### Parameters

| parameter | value |
| --- | --- |
| text_source | Wikipedia (en) |
| identifier_and_statement_source | Wikidata |
| plot_section_titles | Plot, Synopsis, Plot summary, Plot synopsis, Premise, Summary, Storyline, Story |
| min_synopsis_chars | 200 |
| min_biography_chars | 100 |
| text_license | CC BY-SA 4.0 |
| facts_license | CC0 1.0 |
| films | 6821 |
| people | 9759 |

##### Films per enrichment status

| enrichment_status | records | pct |
| --- | --- | --- |
| ok | 5908 | 86.61 |
| not_found | 492 | 7.21 |
| no_plot_section | 365 | 5.35 |
| partial | 56 | 0.82 |

##### Films per decade and status

| decade | films | ok | partial | no_plot_section | not_found | pct_with_synopsis |
| --- | --- | --- | --- | --- | --- | --- |
| 1980 | 1403 | 1187 | 18 | 97 | 101 | 92.80 |
| 1990 | 1433 | 1263 | 9 | 88 | 73 | 94.91 |
| 2000 | 1443 | 1300 | 5 | 67 | 71 | 95.08 |
| 2010 | 1595 | 1367 | 11 | 77 | 140 | 91.22 |
| 2020 | 947 | 791 | 13 | 36 | 107 | 88.70 |

##### Synopsis length (characters)

| synopsis_type | films | avg_chars | median_chars | min_chars | max_chars |
| --- | --- | --- | --- | --- | --- |
| plot_section | 5964 | 3330.94 | 3605.00 | 29 | 13578 |
| lead_section | 365 | 603.87 | 483.00 | 61 | 2817 |

##### Section heading used for the synopsis

| synopsis_section | films |
| --- | --- |
| Plot | 5570 |
| Synopsis | 263 |
| Summary | 57 |
| Premise | 43 |
| Plot summary | 24 |
| Plot synopsis | 3 |
| Storyline | 3 |
| Story | 1 |

##### People per enrichment status

| enrichment_status | records | pct |
| --- | --- | --- |
| ok | 7184 | 73.61 |
| not_found | 1485 | 15.22 |
| partial | 1090 | 11.17 |

##### People: available information

| people | with_biography | with_birth_date | with_death_date | with_birth_place | with_citizenship |
| --- | --- | --- | --- | --- | --- |
| 9759 | 7525 | 8084 | 1427 | 7826 | 8066 |

##### Films per number of principals with a biography

| principals_selected | principals_with_biography | films |
| --- | --- | --- |
| 1 | 0 | 84 |
| 1 | 1 | 208 |
| 2 | 0 | 45 |
| 2 | 1 | 73 |
| 2 | 2 | 80 |
| 3 | 0 | 217 |
| 3 | 1 | 337 |
| 3 | 2 | 716 |
| 3 | 3 | 5049 |

#### Collection statistics

##### Parameters

| parameter | value |
| --- | --- |
| user_agent_product | ECE-BigData-IMDb-Project/1.0 |
| max_requests_per_second | 1 |
| maxlag_seconds | 5 |
| max_retries | 6 |
| robots.policy | report |
| requests | sequential, network requests only (cache hits are not requests) |

##### Collection statistics per step (all runs)

| step | runs | requests | retries | http_429 | http_5xx | maxlag_waits | network_errors | failed | cache_hits | cache_misses | seconds_waited | duration_seconds | ids_requested |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| enrichment:film_pages | 1 | 6334 | 4 | 0 | 0 | 0 | 4 | 0 | 0 | 6330 | 3906.42 | 6602.20 | 6330 |
| enrichment:film_sitelinks | 2 | 35 | 0 | 0 | 0 | 0 | 0 | 0 | 35 | 35 | 2.97 | 130.70 | 6821 |
| enrichment:person_facts | 1 | 51 | 2 | 1 | 0 | 0 | 1 | 0 | 0 | 49 | 124.39 | 334.30 | 9759 |
| enrichment:person_intros | 1 | 377 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 377 | 191.75 | 391.50 | 7525 |
| enrichment:person_sitelinks | 1 | 53 | 4 | 2 | 1 | 0 | 1 | 0 | 0 | 49 | 247.67 | 372.70 | 9759 |

##### robots.txt verdict per endpoint

| endpoint | robots_txt_verdict | robots_policy |
| --- | --- | --- |
| en.wikipedia.org/w/api.php | disallowed | report |
| query.wikidata.org/sparql | disallowed | report |

#### Enrichment sample

##### Parameters

| parameter | value |
| --- | --- |
| sample_rows | 10 |
| text_truncated_at | 300 |

##### Films (most voted first)

| tconst | primaryTitle | startYear | enrichment_status | synopsis_type | synopsis | source_permalink | retrieved_at | license | enrichment_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tt0111161 | The Shawshank Redemption | 1994 | ok | plot_section | In 1947, Portland, Maine, banker Andy Dufresne arrives at Shawshank State Prison to serve two consecutive life sentences for murdering his wife and her lover. He is befriended by Ellis Boyd "Red" Redding, a contraband smuggler serving a life sentence, who procures for him a rock hammer and a large p… | https://en.wikipedia.org/w/index.php?oldid=1384720571 | 2026-11-13T16:54:04Z | CC BY-SA 4.0 |  |
| tt0468569 | The Dark Knight | 2008 | ok | plot_section | A gang of masked criminals rob a mafia-owned bank in Gotham City, betraying and killing each other until the sole survivor, the Joker, reveals himself as the mastermind and escapes with the money. The vigilante Batman, district attorney Harvey Dent, and police lieutenant Jim Gordon ally to eliminate… | https://en.wikipedia.org/w/index.php?oldid=1384066085 | 2026-11-13T17:24:53Z | CC BY-SA 4.0 |  |
| tt1375666 | Inception | 2010 | ok | plot_section | Dom Cobb and Arthur are professional thieves who perform corporate espionage using experimental dream-sharing technology to infiltrate their targets' subconscious and extract information. Their latest target Saito is impressed with Cobb's ability to layer multiple dreams within each other. He offers… | https://en.wikipedia.org/w/index.php?oldid=1385346213 | 2026-11-14T13:32:17Z | CC BY-SA 4.0 |  |
| tt0137523 | Fight Club | 1999 | ok | plot_section | The unnamed Narrator works an office job as an insurance claims adjuster. He sees a doctor for his disordered sleep, complaining that he falls asleep unexpectedly and wakes up in unfamiliar places. The doctor suggests he attend a testicular cancer support group to see what actual pain looks like. Th… | https://en.wikipedia.org/w/index.php?oldid=1385277614 | 2026-11-13T17:03:44Z | CC BY-SA 4.0 |  |
| tt0816692 | Interstellar | 2014 | ok | plot_section | In the near future, humanity faces extinction due to dust storms and widespread crop blights. Joseph Cooper, a widowed former NASA test pilot, works as a farmer and raises his children, Murphy "Murph" and Tom, with his father-in-law Donald. Following a dust storm, Cooper and Murph discover that dust… | https://en.wikipedia.org/w/index.php?oldid=1384598366 | 2026-11-13T17:27:21Z | CC BY-SA 4.0 |  |
| tt0109830 | Forrest Gump | 1994 | ok | plot_section | In 1981, a feather lands at a bus stop in Savannah, Georgia; Forrest Gump collects it, then recounts his life story to strangers on a bus bench. In the fictional city of Greenbow, Alabama during the 1950s, Forrest is fitted with leg braces to correct a curved spine. His mother runs a boarding house … | https://en.wikipedia.org/w/index.php?oldid=1384754400 | 2026-11-13T16:52:58Z | CC BY-SA 4.0 |  |
| tt0110912 | Pulp Fiction | 1994 | ok | plot_section | A young Butch Coolidge is visited by Captain Koons, an Air Force pilot. Koons reveals a gold watch to Butch and explains that the watch is a family heirloom and belonged to Butch's father, who served with Koons and died in a POW camp in the Vietnam War. Koons continues the tradition by giving the wa… | https://en.wikipedia.org/w/index.php?oldid=1385190039 | 2026-11-13T16:53:53Z | CC BY-SA 4.0 |  |
| tt0133093 | The Matrix | 1999 | ok | plot_section | In an unnamed city in 1999, Thomas Anderson, a computer programmer known as "Neo" in hacking circles, investigates the mystery of the "Matrix", bringing him to the attention of hacker Trinity. She tells him that Morpheus can answer Neo's questions. At his workplace, Neo is pursued by Agents led by A… | https://en.wikipedia.org/w/index.php?oldid=1384970784 | 2026-11-13T17:03:22Z | CC BY-SA 4.0 |  |
| tt0120737 | The Lord of the Rings: The Fellowship of the Ring | 2001 | ok | plot_section | In the Second Age of Middle-earth, the lords of Elves, Dwarves, and Men each receive Rings of Power. Unbeknownst to them, the Dark Lord Sauron forges the One Ring, imbuing it with his power to control the other Rings and conquer Middle-earth. An alliance of Men and Elves battles Sauron's forces in M… | https://en.wikipedia.org/w/index.php?oldid=1385099037 | 2026-11-13T17:01:38Z | CC BY-SA 4.0 |  |
| tt0167260 | The Lord of the Rings: The Return of the King | 2003 | ok | plot_section | The hobbit Déagol discovers the One Ring in a river while fishing with his cousin Sméagol. The Ring immediately ensnares Sméagol's mind, and he kills his cousin for it. Physically and mentally corrupted, he retreats into caves below the Misty Mountains and becomes known as Gollum. Centuries later, d… | https://en.wikipedia.org/w/index.php?oldid=1385136677 | 2026-11-13T17:06:20Z | CC BY-SA 4.0 |  |

##### Films without a plot section (most voted first)

| tconst | primaryTitle | startYear | enrichment_status | source_url | enrichment_note |
| --- | --- | --- | --- | --- | --- |
| tt14992922 | The Tinder Swindler | 2022 | no_plot_section | https://en.wikipedia.org/wiki/The_Tinder_Swindler | No section among (Plot, Synopsis, Plot summary, Plot synopsis, Premise, Summary, Storyline, Story) in Wikipedia page 'The Tinder Swindler'; lead section used instead |
| tt2125608 | Searching for Sugar Man | 2012 | no_plot_section | https://en.wikipedia.org/wiki/Searching_for_Sugar_Man | No section among (Plot, Synopsis, Plot summary, Plot synopsis, Premise, Summary, Storyline, Story) in Wikipedia page 'Searching for Sugar Man'; lead section used instead |
| tt0379217 | Coffee and Cigarettes | 2003 | no_plot_section | https://en.wikipedia.org/wiki/Coffee_and_Cigarettes | No section among (Plot, Synopsis, Plot summary, Plot synopsis, Premise, Summary, Storyline, Story) in Wikipedia page 'Coffee and Cigarettes'; lead section used instead |
| tt0428803 | March of the Penguins | 2005 | no_plot_section | https://en.wikipedia.org/wiki/March_of_the_Penguins | No section among (Plot, Synopsis, Plot summary, Plot synopsis, Premise, Summary, Storyline, Story) in Wikipedia page 'March of the Penguins'; lead section used instead |
| tt1155592 | Man on Wire | 2008 | no_plot_section | https://en.wikipedia.org/wiki/Man_on_Wire | No section among (Plot, Synopsis, Plot summary, Plot synopsis, Premise, Summary, Storyline, Story) in Wikipedia page 'Man on Wire'; lead section used instead |
| tt9412098 | Fyre | 2019 | no_plot_section | https://en.wikipedia.org/wiki/Fyre_(film) | No section among (Plot, Synopsis, Plot summary, Plot synopsis, Premise, Summary, Storyline, Story) in Wikipedia page 'Fyre (film)'; lead section used instead |
| tt0892255 | Che: Part One | 2008 | not_found | https://www.wikidata.org/wiki/Q860425 | No enwiki sitelink for Q860425 (P345=tt0892255) |
| tt1754700 | The Prototype | 2022 | not_found | https://www.wikidata.org/wiki/Q136542673 | No enwiki sitelink for Q136542673 (P345=tt1754700) |
| tt17505010 | Horizon: An American Saga - Chapter 1 | 2024 | no_plot_section | https://en.wikipedia.org/wiki/Horizon:_An_American_Saga | No section among (Plot, Synopsis, Plot summary, Plot synopsis, Premise, Summary, Storyline, Story) in Wikipedia page 'Horizon: An American Saga'; lead section used instead |
| tt0120910 | Fantasia 2000 | 1999 | no_plot_section | https://en.wikipedia.org/wiki/Fantasia_2000 | No section among (Plot, Synopsis, Plot summary, Plot synopsis, Premise, Summary, Storyline, Story) in Wikipedia page 'Fantasia 2000'; lead section used instead |

##### People (most scope films first)

| nconst | primaryName | enrichment_status | biography | birth_date | death_date | birth_place | citizenships | source_permalink | license |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nm0000158 | Tom Hanks | ok | Thomas Jeffrey Hanks (born July 9, 1956) is an American actor and filmmaker. Known for both his comedic and dramatic roles, he is one of the most popular and recognizable film stars worldwide, and is regarded as an American cultural icon. In 2020, Hanks was ranked as the fourth-highest-grossing Amer… | 1956-07-09 |  | Concord | Greece, United States | https://en.wikipedia.org/w/index.php?oldid=1384593094 | CC BY-SA 4.0 |
| nm0000115 | Nicolas Cage | ok | Nicolas Cage (born Nicolas Kim Coppola; January 7, 1964) is an American actor and film producer known for his versatility as an actor across diverse film genres, which has gained him a significant cult following. The recipient of various accolades, he was inducted into the Hollywood Walk of Fame in … | 1964-01-07 |  | Long Beach | United States | https://en.wikipedia.org/w/index.php?oldid=1385354136 | CC BY-SA 4.0 |
| nm0000134 | Robert De Niro | ok | Robert Anthony De Niro ( də NEER-roh; Italian: [de ˈniːro]; born August 17, 1943) is an American actor and producer. Widely regarded as one of the greatest and most influential actors of his generation, he has received various accolades, including two Academy Awards and a Golden Globe Award as well … | 1943-08-17 |  | New York City | Italy, United States | https://en.wikipedia.org/w/index.php?oldid=1385624854 | CC BY-SA 4.0 |
| nm0000129 | Tom Cruise | ok | Thomas Cruise Mapother IV ( ; born July 3, 1962), known professionally as Tom Cruise, is an American actor and film producer. His accolades include an Honorary Palme d'Or, an Academy Honorary Award, and three Golden Globe Awards, as well as nominations for four competitive Academy Awards. Considered… | 1962-07-03 |  | Syracuse | United States | https://en.wikipedia.org/w/index.php?oldid=1382360435 | CC BY-SA 4.0 |
| nm0000136 | Johnny Depp | ok | John Christopher Depp II (born June 9, 1963) is an American actor, musician, and filmmaker. He is the recipient of multiple accolades, including an Actor Award and a Golden Globe Award as well as nominations for three Academy Awards and two British Academy Film Awards. His films, in which he has oft… | 1963-06-09 |  | Owensboro | United States | https://en.wikipedia.org/w/index.php?oldid=1384898752 | CC BY-SA 4.0 |
| nm0000168 | Samuel L. Jackson | ok | Samuel Leroy Jackson (born December 21, 1948) is an American actor and film producer. He is one of the most widely recognized actors of his generation. The films in which he has appeared have collectively grossed more than $27 billion worldwide, making him the highest-grossing actor of all time. Jac… | 1948-12-21 |  | Washington, D.C. | Gabon, United States | https://en.wikipedia.org/w/index.php?oldid=1385099910 | CC BY-SA 4.0 |
| nm0000093 | Brad Pitt | ok | William Bradley Pitt (born December 18, 1963) is an American actor and film producer. In a film career spanning more than thirty-five years, Pitt has received numerous accolades, including two Academy Awards, two British Academy Film Awards, two Golden Globe Awards, two Primetime Emmy Awards, and on… | 1963-12-18 |  | Shawnee | United States | https://en.wikipedia.org/w/index.php?oldid=1385271082 | CC BY-SA 4.0 |
| nm0000598 | Dennis Quaid | ok | Dennis William Quaid (born April 9, 1954) is an American actor. He is known for his starring roles in many successful films, including Breaking Away (1979), Jaws 3-D (1983), Innerspace (1987), Great Balls of Fire! (1989), Dragonheart (1996), The Parent Trap (1998), Frequency (2000), The Rookie (2002… | 1954-04-09 |  | Houston | United States | https://en.wikipedia.org/w/index.php?oldid=1384750440 | CC BY-SA 4.0 |
| nm0000243 | Denzel Washington | ok | Denzel Hayes Washington Jr. (born December 28, 1954) is an American actor and film producer. Known for his dramatic roles on stage and screen, he has received numerous accolades including two Academy Awards, an Actor Award, two Golden Globes, two Silver Bears and a Tony Award, as well as nominations… | 1954-12-28 |  | Mount Vernon | United States | https://en.wikipedia.org/w/index.php?oldid=1384381898 | CC BY-SA 4.0 |
| nm0000354 | Matt Damon | ok | Matthew Paige Damon ( DAY-mən; born October 8, 1970) is an American actor, film producer, and screenwriter. He was ranked among Forbes's most bankable stars in 2007, and in 2010 was one of the highest-grossing actors of all time. He has received various awards and nominations, including an Academy A… | 1970-10-08 |  | Cambridge | United States | https://en.wikipedia.org/w/index.php?oldid=1383989129 | CC BY-SA 4.0 |

<!-- AUTO:enrichment:end -->

### Methodological Explanation

#### Methodology and why it was chosen

- **Scope (Spark).** We take feature films from 1980–2025 and keep the top 10 per (genre, year), ranked by votes then by rating. This gives 9,832 selections and 6,821 distinct films. For each film, we take the first 3 principals among actor, actress, director and writer, in IMDb `ordering`, which gives 9,759 people. The scope depends only on parameters: with `top_n: null` and `year_min: null`, the same code processes the whole dataset. The HTTP layer works in batches and resumes from its cache, so a larger scope changes the run time, not the code.
- **Source.** We use English Wikipedia for text (CC BY-SA 4.0). Wikidata (CC0) serves only to map IMDb IDs (P345) to Wikipedia pages and to retrieve structured facts about people: birth date and place, death date and nationality. We use a single source, as the instructions allow, because Wikipedia covers these films well and its text is written by people.
- **Matching by ID, not by title.** We run Wikidata SPARQL queries in batches (`VALUES ?imdb {…}` on P345). An exact ID match avoids homonyms such as *Crash* or *It*, which a title search would confuse.
- **Text.** We use the MediaWiki API. For films, we take the Plot section (or Synopsis, Premise, Summary, …). If no such section exists, we take the lead section and set the status to `no_plot_section`. For people, we take the introduction (`exintro`, `explaintext`), in batches of 20. We also store the `revid`, so each record links to the exact revision we read.
- **Collection (Python, outside Spark, as allowed).** A single-threaded client sends at most 1 request per second, with `maxlag=5`. It honours `Retry-After` on 429/503 responses, with exponential backoff and at most 6 attempts. It identifies itself with a User-Agent that includes a contact email. Every raw response is cached on disk, so an interrupted run resumes without sending any request twice.
- **Everything else in Spark.** Spark reads the JSON cache with an enforced schema and cleans the text: trimming, collapsing whitespace, removing `[1]`-style reference markers, and applying a minimum length of 200 characters for a synopsis and 100 for a biography. It then joins the result to silver and writes `data/gold/enriched_films/` and `enriched_people/`.
- **Lineage.** Every record carries `source_name`, `source_url`, `source_revision_id`, `source_permalink`, `retrieved_at`, `license`, `enrichment_status` and `enrichment_note`. When information is missing, the note is built by code from a fixed template (for example, "no English Wikipedia page"). It states the status and contains no generated content about the film.

**No machine-generated text.** Every text we keep was written by Wikipedia editors. We deliberately ignore Wikidata descriptions. They are very short ("2010 film by …"), and many were created by bots, so we cannot guarantee that a person wrote them.

**Rate limits and `robots.txt`.** Before collecting, the client reads the `robots.txt` of each domain. For generic user agents, both endpoints we call (`en.wikipedia.org/w/api.php` and `query.wikidata.org/sparql`) come out as disallowed. Our policy is set to `report`: this is logged in the output, but it does not block the run. Our view is that `robots.txt` targets crawlers that follow links across a site. Wikimedia publishes separate rules for API clients (User-Agent policy and API etiquette: serial requests, `maxlag`, identification), and those are the rules we followed. We also fetch a fixed list of pages instead of crawling. We prefer to state this openly rather than hide it.

#### Alternatives considered and trade-offs

- **Scraping the HTML pages**: more fragile (it breaks when the layout changes), heavier on Wikimedia's servers, and closer to what `robots.txt` forbids. The API returns clean text and revision IDs.
- **Wikipedia dumps**: no rate-limit concerns, and the best option for the full IMDb scale. However, downloading and parsing tens of GB for about 16,000 pages was out of proportion for our scope.
- **TMDb / OMDb**: good synopsis coverage, but they need API keys, their terms restrict reuse, and their text is not under an open licence.
- **Other Wikipedia languages as a fallback**: better coverage for non-English films, but the output would mix languages, and the instructions do not require a second source.
- **Parallel requests**: much faster than our ~2 h 10 min of collection, but incompatible with the 1 request per second etiquette. We accepted the slower run.

### Key takeaways

- **86.6 % of films got a full synopsis** from a plot-like section, 5.4 % fell back to the introduction, 7.2 % have no English page and 0.8 % are partial. A plot section is far richer than an introduction (median of 3,605 characters against 483), so the introduction is a fallback, not an equivalent. Films without a plot section are mostly documentaries (*Man on Wire*, *March of the Penguins*), whose articles naturally have no Plot heading.
- **People are harder to cover**: 73.6 % `ok`, 15.2 % `not_found` and 11.2 % `partial`. Less-known principals often have no article.
- **Coverage depends on the decade**: 92.8 % (1980s), 94.9 % (1990s), 95.1 % (2000s), 91.2 % (2010s) and 88.7 % (2020s). Recent films are less likely to have a page or a written plot yet.
- **The polite collection worked**: 6,850 requests and 0 failures. The client retried 10 times (3 HTTP 429, 1 HTTP 5xx, 6 network errors), and every retry succeeded. Thanks to the cache, the interruption when the machine went to sleep overnight had no effect.
- **3 principals per film is not always reachable**: 6,319 films have 3 selected principals, and 5,049 have a biography for all three.

## 4. Streaming

### Results

<!-- AUTO:streaming:start -->

#### Streaming lookup table (Wikipedia pages linked to IMDb identifiers)

##### Parameters

| parameter | value |
| --- | --- |
| wikis | enwiki, frwiki |
| lookup.titles | 30000 |
| lookup.title_types | movie->film, tvMovie->film, tvSeries->tv_series, tvMiniSeries->tv_series |
| lookup.people | 20000 |
| lookup.principal_categories | actor, actress, director, writer |
| identifier_mapping | Wikidata P345 and sitelinks |
| pages | 88273 |

##### IMDb identifiers of the lookup scope

| entity_type | identifiers | identifiers_with_a_page | pct_with_a_page |
| --- | --- | --- | --- |
| film | 25450 | 24326 | 95.58 |
| person | 25192 | 19622 | 77.89 |
| tv_series | 5973 | 5437 | 91.03 |

##### Pages per wiki and entity type

| wiki | entity_type | pages |
| --- | --- | --- |
| enwiki | film | 24198 |
| enwiki | person | 19217 |
| enwiki | tv_series | 5410 |
| frwiki | film | 20012 |
| frwiki | person | 15327 |
| frwiki | tv_series | 4109 |

#### Streaming summary

##### Parameters

| parameter | value |
| --- | --- |
| application_run_id | f10bdae5cc954d749056961a2a8ee769 |
| status | completed |
| duration_seconds | 1236.99 |
| watermark_delay | 10 minutes |
| tumbling | {"duration": "5 minutes", "slide": "5 minutes"} |
| sliding | {"duration": "10 minutes", "slide": "5 minutes"} |
| late_injection | injected |
| aggregate_output | append; finalized windows only |
| window_scope | finalized in this run; resumed state can contain prior-run edits |
| checkpoint_policy | resume; independent checkpoints per query |
| matched_events | 72 |

##### Totals per query (independent Kafka reads)

| query | batches | input_rows | rows_dropped_by_watermark |
| --- | --- | --- | --- |
| matched_events | 117 | 2113 | 5 |
| sliding | 120 | 2055 | 5 |
| tumbling | 120 | 2055 | 5 |

##### Latest batches

| query | batch_id | input_rows | input_rows_per_second | processed_rows_per_second | trigger_ms | rows_dropped_by_watermark | watermark |
| --- | --- | --- | --- | --- | --- | --- | --- |
| matched_events | 99 | 22 | 2.20 | 2.10 | 10564 | 0 | 2026-11-14T14:57:48.569Z |
| sliding | 99 | 22 | 2.20 | 4.50 | 4909 | 0 | 2026-11-14T14:57:48.569Z |
| tumbling | 99 | 22 | 2.20 | 4.00 | 5471 | 0 | 2026-11-14T14:57:48.569Z |
| sliding | 100 | 21 | 2.10 | 4.50 | 4697 | 0 | 2026-11-14T14:57:58.175Z |
| tumbling | 100 | 21 | 2.10 | 4.00 | 5244 | 0 | 2026-11-14T14:57:58.175Z |
| matched_events | 100 | 22 | 2.10 | 2.20 | 10013 | 0 | 2026-11-14T14:57:58.175Z |
| tumbling | 101 | 20 | 2.00 | 3.90 | 5139 | 0 | 2026-11-14T14:58:08.677Z |
| sliding | 101 | 20 | 2.00 | 3.70 | 5362 | 0 | 2026-11-14T14:58:08.677Z |
| matched_events | 101 | 20 | 2.00 | 2.00 | 9995 | 0 | 2026-11-14T14:58:09.851Z |
| sliding | 102 | 17 | 1.70 | 2.80 | 6112 | 0 | 2026-11-14T14:58:18.796Z |
| tumbling | 102 | 17 | 1.70 | 3.20 | 5310 | 0 | 2026-11-14T14:58:18.796Z |
| matched_events | 102 | 17 | 1.70 | 1.70 | 10217 | 0 | 2026-11-14T14:58:19.721Z |
| sliding | 103 | 18 | 1.80 | 3.00 | 6017 | 0 | 2026-11-14T14:58:29.296Z |
| tumbling | 103 | 18 | 1.80 | 3.70 | 4892 | 0 | 2026-11-14T14:58:29.296Z |
| matched_events | 103 | 18 | 1.80 | 1.70 | 10342 | 0 | 2026-11-14T14:58:29.935Z |
| tumbling | 104 | 23 | 2.30 | 3.90 | 5885 | 0 | 2026-11-14T14:58:39.133Z |
| sliding | 104 | 23 | 2.30 | 4.40 | 5261 | 0 | 2026-11-14T14:58:39.133Z |
| matched_events | 104 | 25 | 2.40 | 2.50 | 9989 | 0 | 2026-11-14T14:58:39.931Z |
| sliding | 105 | 18 | 1.80 | 3.40 | 5334 | 0 | 2026-11-14T14:58:49.566Z |
| tumbling | 105 | 18 | 1.80 | 3.00 | 6048 | 0 | 2026-11-14T14:58:49.566Z |
| matched_events | 105 | 18 | 1.80 | 1.70 | 10417 | 0 | 2026-11-14T14:58:50.457Z |
| tumbling | 106 | 26 | 2.60 | 5.00 | 5249 | 0 | 2026-11-14T14:58:58.880Z |
| sliding | 106 | 26 | 2.60 | 5.60 | 4657 | 0 | 2026-11-14T14:58:58.880Z |
| matched_events | 106 | 26 | 2.50 | 2.40 | 10957 | 0 | 2026-11-14T14:59:00.286Z |
| sliding | 107 | 14 | 1.40 | 2.70 | 5141 | 0 | 2026-11-14T14:59:09.182Z |
| tumbling | 107 | 14 | 1.40 | 2.40 | 5800 | 0 | 2026-11-14T14:59:09.182Z |
| matched_events | 107 | 19 | 1.70 | 1.70 | 11129 | 0 | 2026-11-14T14:59:10.595Z |
| sliding | 108 | 22 | 2.20 | 3.90 | 5643 | 0 | 2026-11-14T14:59:18.164Z |
| tumbling | 108 | 22 | 2.20 | 3.50 | 6335 | 0 | 2026-11-14T14:59:18.164Z |
| matched_events | 108 | 20 | 1.80 | 2.00 | 9876 | 0 | 2026-11-14T14:59:21.529Z |
| sliding | 109 | 23 | 2.30 | 3.80 | 6091 | 0 | 2026-11-14T14:59:29.691Z |
| tumbling | 109 | 23 | 2.30 | 4.20 | 5452 | 0 | 2026-11-14T14:59:29.691Z |
| matched_events | 109 | 22 | 2.20 | 1.00 | 21517 | 0 | 2026-11-14T14:59:32.335Z |
| sliding | 110 | 19 | 1.90 | 3.40 | 5596 | 0 | 2026-11-14T14:59:39.283Z |
| tumbling | 110 | 19 | 1.90 | 3.70 | 5188 | 0 | 2026-11-14T14:59:39.283Z |
| sliding | 111 | 11 | 1.10 | 1.90 | 5662 | 0 | 2026-11-14T14:59:49.039Z |
| tumbling | 111 | 11 | 1.10 | 1.70 | 6434 | 0 | 2026-11-14T14:59:49.039Z |
| matched_events | 110 | 40 | 1.90 | 2.30 | 17026 | 0 | 2026-11-14T14:59:41.235Z |
| sliding | 112 | 25 | 2.50 | 5.00 | 5008 | 0 | 2026-11-14T14:59:55.338Z |
| tumbling | 112 | 25 | 2.50 | 4.70 | 5314 | 0 | 2026-11-14T14:59:55.338Z |
| sliding | 113 | 25 | 2.50 | 4.00 | 6280 | 0 | 2026-11-14T15:00:08.312Z |
| tumbling | 113 | 25 | 2.50 | 3.60 | 6922 | 0 | 2026-11-14T15:00:08.312Z |
| matched_events | 111 | 38 | 2.20 | 2.10 | 18248 | 0 | 2026-11-14T15:00:03.938Z |
| sliding | 114 | 18 | 1.80 | 3.50 | 5213 | 0 | 2026-11-14T15:00:19.097Z |
| tumbling | 114 | 18 | 1.80 | 3.70 | 4889 | 0 | 2026-11-14T15:00:19.097Z |
| sliding | 115 | 19 | 1.90 | 3.40 | 5620 | 0 | 2026-11-14T15:00:29.086Z |
| tumbling | 115 | 19 | 1.90 | 3.00 | 6347 | 0 | 2026-11-14T15:00:29.086Z |
| matched_events | 112 | 36 | 2.00 | 2.00 | 18386 | 0 | 2026-11-14T15:00:21.190Z |
| tumbling | 116 | 15 | 1.50 | 2.70 | 5637 | 0 | 2026-11-14T15:00:38.945Z |
| sliding | 116 | 15 | 1.50 | 2.80 | 5307 | 0 | 2026-11-14T15:00:38.945Z |
| matched_events | 113 | 32 | 1.70 | 1.60 | 19597 | 0 | 2026-11-14T15:00:39.664Z |
| sliding | 117 | 19 | 1.90 | 3.50 | 5402 | 0 | 2026-11-14T15:00:49.121Z |
| tumbling | 117 | 19 | 1.90 | 3.80 | 4949 | 0 | 2026-11-14T15:00:49.121Z |
| sliding | 118 | 11 | 1.10 | 1.60 | 6851 | 0 | 2026-11-14T15:00:58.010Z |
| tumbling | 118 | 11 | 1.10 | 1.70 | 6386 | 0 | 2026-11-14T15:00:58.010Z |
| matched_events | 114 | 20 | 1.00 | 1.20 | 16905 | 0 | 2026-11-14T15:00:58.010Z |
| sliding | 119 | 14 | 1.40 | 2.40 | 5939 | 0 | 2026-11-14T15:01:09.358Z |
| tumbling | 119 | 14 | 1.40 | 2.60 | 5329 | 0 | 2026-11-14T15:01:09.358Z |
| matched_events | 115 | 36 | 2.10 | 2.30 | 15611 | 0 | 2026-11-14T15:01:17.027Z |
| matched_events | 116 | 27 | 1.70 | 1.70 | 15454 | 0 | 2026-11-14T15:01:33.798Z |

##### Matched sink

| counter | value |
| --- | --- |
| matched_events | 72 |

##### Relevant edits by wiki, entity type and bot flag

| wiki | entity_type | bot | match_reason | count |
| --- | --- | --- | --- | --- |
| frwiki | person | false | lookup | 10 |
| enwiki | film | false | lookup | 7 |
| enwiki | film | false | lookup+title_pattern | 7 |
| enwiki | person | false | lookup | 7 |
| enwiki | film | true | title_pattern | 6 |
| frwiki | film | false | title_pattern | 6 |
| enwiki | tv_series | false | lookup | 5 |
| enwiki | film | false | title_pattern | 4 |
| enwiki | tv_series | true | title_pattern | 4 |
| enwiki | tv_series | false | title_pattern | 3 |
| enwiki | person | false | title_pattern | 2 |
| enwiki | tv_series | true | lookup+title_pattern | 2 |
| enwiki | tv_series | false | lookup+title_pattern | 2 |
| frwiki | tv_series | false | lookup | 2 |
| enwiki | tv_series | true | lookup | 1 |
| frwiki | film | true | lookup | 1 |
| frwiki | film | false | lookup | 1 |
| frwiki | person | false | title_pattern | 1 |
| frwiki | tv_series | false | lookup+title_pattern | 1 |

##### Top pages (matched events)

| wiki | page_title_normalized | count |
| --- | --- | --- |
| frwiki | Christophe Colomb (film, 1949) | 4 |
| enwiki | Slow Horses | 3 |
| enwiki | Beautiful Boy (2018 film) | 2 |
| enwiki | Kudrat (1998 film) | 2 |
| enwiki | La bola negra | 2 |
| enwiki | Tangled: Before Ever After | 2 |
| enwiki | Ti West | 2 |
| frwiki | Drew Barrymore | 2 |
| frwiki | Jacqueline Bisset | 2 |
| frwiki | Ma meilleure amie (film, 2014) | 2 |

##### Match examples

| event_time | wiki | title | imdb_id | entity_type | match_reason |
| --- | --- | --- | --- | --- | --- |
| 2026-11-14T15:11:31.345000 | enwiki | Catalyst (TV program) |  | tv_series | title_pattern |
| 2026-11-14T15:11:27.506000 | enwiki | John Steinbeck | nm0825705 | person | lookup |
| 2026-11-14T15:11:18.592000 | frwiki | Le Laboratoire de Dexter | tt0115157 | tv_series | lookup |
| 2026-11-14T15:10:54.393000 | frwiki | Laetitia Casta | nm0144377 | person | lookup |
| 2026-11-14T15:10:25.390000 | enwiki | Buddy (2026 film) | tt37281055 | film | lookup+title_pattern |
| 2026-11-14T15:09:47.673000 | enwiki | Al Hilal (film) |  | film | title_pattern |
| 2026-11-14T15:09:27.134000 | enwiki | Breakfast (Australian TV program) |  | tv_series | title_pattern |
| 2026-11-14T15:09:23.631000 | enwiki | Beautiful Boy (2018 film) | tt1226837 | film | lookup+title_pattern |
| 2026-11-14T15:09:05.714000 | enwiki | Bra Boys (film) |  | film | title_pattern |
| 2026-11-14T15:08:39.931000 | enwiki | Jack Lowden | nm4110963 | person | lookup |

##### Finalized tumbling windows

| window_start | window_end | wiki | entity_type | bot | edits | avg_size_delta |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | enwiki | film | false | 5 | -85.80 |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | enwiki | person | false | 2 | -965.00 |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | enwiki | tv_series | false | 3 | 2.33 |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | frwiki | film | false | 1 | 4.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | film | false | 8 | 95.88 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | film | true | 1 | 57.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | person | false | 1 | 22.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | tv_series | false | 6 | -65.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | tv_series | true | 1 | 4.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | frwiki | film | false | 1 | 802.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | frwiki | person | false | 4 | 211.50 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | frwiki | tv_series | false | 1 | 2.00 |

##### Finalized tumbling page windows

| window_start | window_end | wiki | entity_type | bot | page_title_normalized | edits | avg_size_delta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | enwiki | person | false | Anthony Clark (actor) | 1 | 15.00 |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | enwiki | film | false | Coma (1978 film) | 1 | -31.00 |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | enwiki | film | false | Ebenezer (2026 film) | 1 | 0.00 |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | enwiki | tv_series | false | Georgie & Mandy's First Marriage | 1 | 11.00 |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | enwiki | film | false | Idiocracy | 1 | -1.00 |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | enwiki | person | false | Inde Navarrette | 1 | -1945.00 |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | enwiki | tv_series | false | India's Got Latent | 1 | 0.00 |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | enwiki | film | false | Kesari (2020 film) | 1 | -350.00 |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | enwiki | film | false | Tell It to the Marines (1926 film) | 1 | -47.00 |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | enwiki | tv_series | false | Trigger Point (TV series) | 1 | -4.00 |
| 2026-11-14T14:50:00 | 2026-11-14T14:55:00 | frwiki | film | false | Les Pleins Pouvoirs | 1 | 4.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | tv_series | false | Slow Horses | 3 | 66.67 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | film | false | La bola negra | 2 | 285.50 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | tv_series | true | 24 (TV series) | 1 | 4.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | tv_series | false | Anna Karenina (2013 TV series) | 1 | 193.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | film | false | Beautiful Boy (2018 film) | 1 | 260.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | person | false | Dennis Miller (Australian actor) | 1 | 22.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | film | false | Ela Veezha Poonchira | 1 | -481.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | film | false | Fritz the Cat (film) | 1 | -80.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | film | true | Kudrat (1998 film) | 1 | 57.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | tv_series | false | Marshals (TV series) | 1 | -553.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | film | false | Tangled: Before Ever After | 1 | 1.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | film | false | Teen Murti (film) | 1 | 492.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | tv_series | false | Trinayani (Telugu TV series) | 1 | -230.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | enwiki | film | false | Wild Horse Nine | 1 | 4.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | frwiki | film | false | Christophe Colomb (film, 1949) | 1 | 802.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | frwiki | person | false | Drew Barrymore | 1 | 30.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | frwiki | person | false | Fredric March | 1 | 810.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | frwiki | person | false | Jacqueline Bisset | 1 | 6.00 |
| 2026-11-14T14:55:00 | 2026-11-14T15:00:00 | frwiki | tv_series | false | Marco Polo (série télévisée, 2014) | 1 | 2.00 |

##### Finalized sliding windows

| window_start | window_end | wiki | entity_type | bot | edits | avg_size_delta |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | enwiki | film | false | 5 | -85.80 |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | enwiki | person | false | 2 | -965.00 |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | enwiki | tv_series | false | 3 | 2.33 |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | frwiki | film | false | 1 | 4.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | film | false | 13 | 26.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | film | true | 1 | 57.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | person | false | 3 | -636.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | tv_series | false | 9 | -42.56 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | tv_series | true | 1 | 4.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | frwiki | film | false | 2 | 403.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | frwiki | person | false | 4 | 211.50 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | frwiki | tv_series | false | 1 | 2.00 |

##### Finalized sliding page windows

| window_start | window_end | wiki | entity_type | bot | page_title_normalized | edits | avg_size_delta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | enwiki | person | false | Anthony Clark (actor) | 1 | 15.00 |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | enwiki | film | false | Coma (1978 film) | 1 | -31.00 |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | enwiki | film | false | Ebenezer (2026 film) | 1 | 0.00 |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | enwiki | tv_series | false | Georgie & Mandy's First Marriage | 1 | 11.00 |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | enwiki | film | false | Idiocracy | 1 | -1.00 |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | enwiki | person | false | Inde Navarrette | 1 | -1945.00 |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | enwiki | tv_series | false | India's Got Latent | 1 | 0.00 |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | enwiki | film | false | Kesari (2020 film) | 1 | -350.00 |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | enwiki | film | false | Tell It to the Marines (1926 film) | 1 | -47.00 |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | enwiki | tv_series | false | Trigger Point (TV series) | 1 | -4.00 |
| 2026-11-14T14:45:00 | 2026-11-14T14:55:00 | frwiki | film | false | Les Pleins Pouvoirs | 1 | 4.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | tv_series | false | Slow Horses | 3 | 66.67 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | film | false | La bola negra | 2 | 285.50 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | tv_series | true | 24 (TV series) | 1 | 4.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | tv_series | false | Anna Karenina (2013 TV series) | 1 | 193.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | person | false | Anthony Clark (actor) | 1 | 15.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | film | false | Beautiful Boy (2018 film) | 1 | 260.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | film | false | Coma (1978 film) | 1 | -31.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | person | false | Dennis Miller (Australian actor) | 1 | 22.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | film | false | Ebenezer (2026 film) | 1 | 0.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | film | false | Ela Veezha Poonchira | 1 | -481.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | film | false | Fritz the Cat (film) | 1 | -80.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | tv_series | false | Georgie & Mandy's First Marriage | 1 | 11.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | film | false | Idiocracy | 1 | -1.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | person | false | Inde Navarrette | 1 | -1945.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | tv_series | false | India's Got Latent | 1 | 0.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | film | false | Kesari (2020 film) | 1 | -350.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | film | true | Kudrat (1998 film) | 1 | 57.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | tv_series | false | Marshals (TV series) | 1 | -553.00 |
| 2026-11-14T14:50:00 | 2026-11-14T15:00:00 | enwiki | film | false | Tangled: Before Ever After | 1 | 1.00 |

##### Injected event observations

| event_id | offset_minutes | event_time | present_in_matched_sink |
| --- | --- | --- | --- |
| 1fea66cf-494b-4298-ad05-f3e77f14b5b5-late-c17d6e3d90244594aaf3aec723c13da8 | 30.00 | 2026-11-14T14:33:19.636000Z | false |
| 1fea66cf-494b-4298-ad05-f3e77f14b5b5-late-812625e76d164928aa6849076548a0c9 | 5.00 | 2026-11-14T14:58:19.636000Z | true |
| c9607284-a0aa-4ad0-9c8f-66bfe04b5016-late-ff24a54793234b2ba7accab3621c2bd5 | 30.00 | 2026-11-14T14:33:19.636000Z | false |
| c9607284-a0aa-4ad0-9c8f-66bfe04b5016-late-4656ca6caad34b05be29e0c2f4794ad2 | 5.00 | 2026-11-14T14:58:19.636000Z | true |
| f0a313e8-f25d-4f29-b050-ca1796f83d26-late-f8b61795ac0a4643b36b1cf281c0c522 | 30.00 | 2026-11-14T14:33:19.636000Z | false |
| f0a313e8-f25d-4f29-b050-ca1796f83d26-late-8f355476b32e496b967885c7addf10d7 | 5.00 | 2026-11-14T14:58:19.636000Z | true |
| 3d22f1cc-c006-4707-b617-1343a71dd326-late-0c0d20307a27467bad85f763b1dcfda9 | 30.00 | 2026-11-14T14:33:19.636000Z | false |
| 3d22f1cc-c006-4707-b617-1343a71dd326-late-14529f5fc3eb4469a216e77e67faee54 | 5.00 | 2026-11-14T14:58:19.636000Z | true |
| 523daf65-2593-46f6-80f2-61bf8d02d320-late-eccf785acb9d49cd901dcd4cc71889a2 | 30.00 | 2026-11-14T14:33:19.636000Z | false |
| 523daf65-2593-46f6-80f2-61bf8d02d320-late-64f23c2e5bfb4b5cbcb7dca7f959c32d | 5.00 | 2026-11-14T14:58:19.636000Z | true |

<!-- AUTO:streaming:end -->

### Methodological Explanation

#### Methodology and why it was chosen

The pipeline is: Wikimedia EventStreams (`recentchange`, SSE) → Python producer → Kafka topic `wikistreams` → Spark Structured Streaming → Parquet + console.

- **Producer.** It reads the SSE stream and keeps only `enwiki`/`frwiki` events of type `edit`/`new` in namespace 0 (articles). It publishes the raw JSON to Kafka, with `meta.id` as the key. After a disconnection, it resumes with `Last-Event-ID`, so no events are skipped. The cost is that a few events may be sent twice, which the dedup step handles downstream.
- **Lookup table.** Before the stream starts, a Spark batch job builds `data/gold/wiki_lookup/`. It maps the 30,000 most-voted titles and 20,000 people to their enwiki/frwiki pages through Wikidata, which gives 88,273 pages with a normalised title, the IMDb ID and the entity type. The table is small enough to be broadcast.
- **Relevance.** An event is relevant if its (wiki, normalised title) is in the lookup **or** if its title matches a pattern such as "(film)", "(TV series)", "(actor)" or "(série télévisée)". The `match_reason` column records which rule fired. The lookup links an edit to an exact IMDb ID. The patterns catch pages outside the lookup, such as less-voted titles or new pages. Together, they ensure that several events match within the test window: we got 72 in 20 minutes.
- **Streaming job.** Spark reads Kafka with an explicit JSON schema and uses `meta.dt` (the time of the edit on Wikipedia) as event time. It applies a 10-minute watermark and `dropDuplicatesWithinWatermark(event_id)`. Three independent queries run, each with its own checkpoint:
  1. relevant events → Parquet (append);
  2. 5-minute tumbling windows;
  3. 10-minute sliding windows with a 5-minute slide.

  The window queries count events per wiki, entity type, bot/human and page, and compute the average size change. They write in append mode through `foreachBatch`, to Parquet and to the console.
- **Metrics.** A `StreamingQueryListener` writes every progress event to `outputs/streaming/progress.jsonl`: input rows, rates, durations, watermark and rows dropped by the watermark.
- The job stops cleanly after the configured duration.

**Why Kafka.** Kafka decouples the source from Spark. Spark has no native SSE source and cannot replay the Wikimedia stream itself. With Kafka in between, events wait in the topic if Spark restarts, and Spark resumes from the offsets saved in its checkpoint. Several queries can also read the same topic independently.

**Why two window types.** Tumbling windows do not overlap, so their counts add up to the total, which is convenient for reporting. Sliding windows count each event twice and give a smoother trend, which shows bursts that straddle a window boundary.

#### Alternatives considered and trade-offs

- **Reading the SSE stream directly from Spark** (custom source or socket): no replay and no buffer, and Spark would depend on the availability of the source.
- **Patterns only**: no lookup to build (about 17 minutes on the first run), but they miss pages whose title gives no hint, such as *Slow Horses* or *John Steinbeck*. **Lookup only** misses films outside the top 30,000. Each rule found events the other missed: 34 by the lookup only, 26 by the patterns only, 12 by both.
- **Matching against the full IMDb title list**: far larger, and full of false positives, because common words ("Home", "Love") are also IMDb titles.
- **`update` or `complete` output mode**: earlier results, but windows get rewritten, which does not fit an append-only Parquet sink, and `complete` keeps all the state forever.
- **Processing-time windows**: no late-data problem, but the counts would reflect when Spark processed events, not when the edits happened.

### Late-arriving data

Events can arrive late for several reasons: a reconnection of the producer, lag in Kafka, or Spark restarting and reading a backlog. We work in **event time** (`meta.dt`) and use a **10-minute watermark**. Spark tracks the latest event time it has seen and assumes that no event older than that time minus 10 minutes will still arrive. In practice:

- an event up to 10 minutes late is still counted in its correct window;
- an older event is dropped by the stateful operators (window aggregation and dedup) and counted in `numRowsDroppedByWatermark`;
- in append mode, a window is written only once the watermark has passed its end. A 5-minute window is therefore final about 10 minutes after it closes, and it is never rewritten;
- state older than the watermark (old windows, seen IDs) is purged, so memory stays bounded however long the stream runs.

**Why 10 minutes.** The `recentchange` stream is close to real time, and normal delays are a few seconds. Ten minutes covers a producer reconnection or a short Spark restart, while keeping the delay before results acceptable in a 20-minute run and the state small. The trade-off is simple: a larger watermark gives more complete counts, but later results and more state; a smaller one gives faster results, but drops more events.

**Deduplication.** `dropDuplicatesWithinWatermark(event_id)` removes duplicates caused by the `Last-Event-ID` replay or by producer retries (Kafka is at-least-once here). Because it is bounded by the watermark, the set of seen IDs does not grow forever. A plain `dropDuplicates` on `event_id` would have to remember every ID.

**Experiment.** After 12 minutes, an injector republished 10 real events with new IDs, so that the dedup would not remove them: 5 with `meta.dt` moved back by 5 minutes, and 5 moved back by 30 minutes.

| Injected delay | Expected | Observed |
|---|---|---|
| 5 min (< watermark) | accepted | accepted, present in the sink |
| 30 min (> watermark) | dropped | dropped: 5 rows in `numRowsDroppedByWatermark` for each query |

The behaviour matches the theory. The 5-minute-late events carried an event time of 14:58:19 UTC, which was still above the watermark; the 30-minute-late ones (14:33:19 UTC) were below it.

The cost of the watermark is visible in the window outputs too. When the job stopped, the watermark was about 10 minutes behind the latest event, so only the windows ending at 14:55 and 15:00 UTC were finalized and written. Edits from the last ten minutes of the run were still sitting in open windows.

The limit is that dropped events are lost from the aggregates and only counted. If they mattered, we could compare their event time with the current watermark in `foreachBatch`, send them to a separate sink, and reconcile them later in batch.

### Key takeaways

- In 20 minutes, the matched-events query read **2,113 events** (each window query read 2,055, since every query reads Kafka on its own), at about 1 to 2.6 events per second after the producer filter. **72 were relevant** (67 real + 5 injected), or about 3.4 %. This is well above "multiple matches" for the test window.
- enwiki accounts for 50 of the relevant events and frwiki for 22. By type: 32 films, 20 people and 20 series. 14 edits (19 %) came from bots, 13 of them on enwiki, which do a visible share of maintenance even on film pages. The bot flag is kept so they can be filtered out.
- The lookup and the patterns are complementary (34 / 26 / 12): neither would have been enough alone. People are found almost only through the lookup (17 of 20), because their page titles rarely carry a hint like "(actor)". Bot edits, in contrast, were mostly caught by the patterns (10 of 14).
- A trigger takes about 5–7 seconds for the window queries and 10–20 seconds for the matched-events query, and the input rate is low. The bottleneck is the source, not Spark, so a single local container is enough.
- The injection experiment confirms that the watermark accepts events that are slightly late and drops events that are too late, as designed.

## 5. Open Question

### Question and motivation

**Do repeated director–actor collaborations produce better-rated films than the first one?**

Many directors work with the same actors again and again: Kurosawa with Toshirō Mifune and Takashi Shimura, Ozu with Chishū Ryū, Bergman with Gunnar Björnstrand. Two stories are possible. Either familiarity improves the work, or a director brings an actor back after a success and the following films do not live up to it. IMDb lets us test this on tens of thousands of pairs. The question needs joins between four tables and window functions per pair, which makes it a non-trivial Spark problem.

### Data

IMDb only, with no external data:

- `title.basics` (type, year, runtime) and `title.ratings`: the same 49,434 rated feature films as the exploration (≥ 1,000 votes);
- `title.crew` and `title.principals` for directors, using the same union as Q4;
- `title.principals` for actors and actresses;
- `name.basics` for names.

Films where the director also acts are excluded from the pairs, because directing yourself is not a collaboration.

### Results

<!-- AUTO:open_question:start -->

#### Open question - Recurring director-actor collaborations

##### Parameters

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

##### Overall

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

##### Recurring pairs by collaboration rank

| collab_rank | films | avg_rating | avg_diff_vs_first | avg_votes |
| --- | --- | --- | --- | --- |
| 1 | 26630 | 6.61 | 0.00 | 48622.84 |
| 2 | 26630 | 6.36 | -0.24 | 36250.71 |
| 3 | 6587 | 6.40 | -0.35 | 40428.08 |
| 4 | 2431 | 6.44 | -0.37 | 35037.10 |
| 5+ | 2771 | 6.42 | -0.40 | 19510.01 |

##### Recurring pairs by number of collaborations

| collaborations | pairs | avg_first_rating | avg_repeat_rating | avg_delta | share_higher | avg_excess_vs_director |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 20043 | 6.56 | 6.28 | -0.28 | 0.34 | 0.10 |
| 3 | 4156 | 6.71 | 6.43 | -0.28 | 0.30 | 0.15 |
| 4-5 | 1850 | 6.79 | 6.48 | -0.31 | 0.29 | 0.17 |
| 6+ | 581 | 6.85 | 6.60 | -0.25 | 0.30 | 0.22 |

##### Most frequent recurring pairs

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

##### CSV exports

| file | total_rows | exported_rows | truncated |
| --- | --- | --- | --- |
| collaborations_pairs.csv | 26630 | 26630 | false |
| collaborations_by_rank.csv | 5 | 5 | false |
| collaborations_by_count.csv | 4 | 4 | false |

<!-- AUTO:open_question:end -->

### Key takeaways

- **Collaborations rarely repeat**: only 26,630 of the 469,141 pairs (5.7 %) worked together on at least two films.
- **The first film of a recurring pair is already rated well above average**: 6.61 against 6.13 for one-off pairs. A success makes a new collaboration more likely.
- **Follow-up films are rated lower than the first**: −0.28 on average (median −0.20, t = −53.7), and 60.8 % of pairs decline. The gap stays between −0.24 and −0.40 at every collaboration rank.
- **However, the pair still does better than the director's other work**: the follow-ups are rated +0.12 above the films the same director made, over the same period, without that actor, and 57.1 % of pairs are above this baseline. This excess grows with the number of collaborations (+0.10 for pairs with 2 films, +0.22 for pairs with 6 or more), while the delta stays around −0.28.
- **Kartal Tibet and Kemal Sunal show both effects at once.** Their first film, *Tosun Pasha* (8.8), was never matched (delta −1.97), but their 25 other films are still rated 1.43 points above Tibet's work without Sunal.
- **How we read it.** The decline relative to the first film looks like regression to the mean. Pairs are selected on a good first film, so the next films can only be expected to fall back toward the director's usual level. The general decline of ratings over careers, seen in Q7, adds to this effect. The positive excess suggests that working again with the same actor goes with slightly better films than the director's other work. Familiarity seems to help a little, but it does not repeat the first success.
- **This is correlation, not causation.** Directors may cast their regular actors in their more personal or better-funded projects.

### Methodological Explanation

#### Methodology and why it was chosen

- **Pairs.** We join director credits and actor credits on the same `tconst`, excluding cases where the director and the actor are the same person.
- **Order.** A Spark window partitioned by pair and ordered by year (then `tconst` for ties) numbers the films of each pair.
- **Delta.** For each recurring pair, the delta is the average rating of the follow-up films minus the rating of the first film. Averaging the follow-ups gives each pair exactly one value, so a pair with 26 films does not weigh more than a pair with two.
- **Excess.** The excess is the average rating of the follow-ups minus the average rating of the director's films *without* that actor, released after the pair's first film. This baseline controls for the director's general level and for the period. 21,573 pairs have such a baseline.
- **Statistics.** We compute a paired t statistic on the delta, and use a tolerance of 0.05 to classify each pair as better, equal or worse. We also build profiles by collaboration rank and by number of collaborations, and list the most frequent pairs.

We chose this design because it is simple to explain and each pair serves as its own control. We added the director baseline after seeing that the negative delta could be explained by selection alone.

#### Alternatives considered and trade-offs

- **Comparing all films of recurring pairs with all films of one-off pairs**: easy, but it mixes first films and follow-ups, and selection drives the result (6.61 against 6.13 before any follow-up is made).
- **A regression with director, actor and year effects**: it would separate the effects better and give proper confidence intervals, but it is heavier to build in Spark and harder to explain. We kept paired comparisons.
- **Matching each follow-up with a film the same director made in the same year**: a closer control, but many directors do not make a film every year, so far fewer pairs would remain.
- **Weighting by number of votes**: famous pairs would dominate the result. We gave every pair the same weight.
- **External data (budgets, box office)**: would help control for the size of the project, but we found no open, human-written source with good coverage, and budgets in Wikipedia infoboxes are patchy.

One limit of our approach is that the t statistic assumes the pairs are independent. Pairs that share a director or an actor are not independent, so t = −53.7 overstates how certain the result is. The sign and the size of the effect remain informative.
