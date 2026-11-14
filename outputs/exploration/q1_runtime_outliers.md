# Q1 - Feature films with a runtime notably different from their genre

## Parameters

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

## Runtime distribution and outliers per genre

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

## Top 20 outliers per genre (by absolute z-score)

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

## CSV exports

| file | total_rows | exported_rows | truncated | gold_directory |
| --- | --- | --- | --- | --- |
| q1_runtime_outliers_summary.csv | 26 | 26 | false | data/gold/exploration |
| q1_runtime_outliers.csv | 35557 | 35557 | false | data/gold/exploration |
