# Streaming summary

## Parameters

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

## Totals per query (independent Kafka reads)

| query | batches | input_rows | rows_dropped_by_watermark |
| --- | --- | --- | --- |
| matched_events | 117 | 2113 | 5 |
| sliding | 120 | 2055 | 5 |
| tumbling | 120 | 2055 | 5 |

## Latest batches

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

## Matched sink

| counter | value |
| --- | --- |
| matched_events | 72 |

## Relevant edits by wiki, entity type and bot flag

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

## Top pages (matched events)

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

## Match examples

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

## Finalized tumbling windows

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

## Finalized tumbling page windows

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

## Finalized sliding windows

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

## Finalized sliding page windows

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

## Injected event observations

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
