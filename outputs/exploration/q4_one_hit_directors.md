# Q4 - Directors with exactly one highly rated film and low-rated other films

## Parameters

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

## Directors

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

## CSV exports

| file | total_rows | exported_rows | truncated | gold_directory |
| --- | --- | --- | --- | --- |
| q4_one_hit_directors.csv | 47 | 47 | false | data/gold/exploration |
