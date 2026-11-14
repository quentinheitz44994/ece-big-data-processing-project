# Collection statistics

## Parameters

| parameter | value |
| --- | --- |
| user_agent_product | ECE-BigData-IMDb-Project/1.0 |
| max_requests_per_second | 1 |
| maxlag_seconds | 5 |
| max_retries | 6 |
| robots.policy | report |
| requests | sequential, network requests only (cache hits are not requests) |

## Collection statistics per step (all runs)

| step | runs | requests | retries | http_429 | http_5xx | maxlag_waits | network_errors | failed | cache_hits | cache_misses | seconds_waited | duration_seconds | ids_requested |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| enrichment:film_pages | 1 | 6334 | 4 | 0 | 0 | 0 | 4 | 0 | 0 | 6330 | 3906.42 | 6602.20 | 6330 |
| enrichment:film_sitelinks | 2 | 35 | 0 | 0 | 0 | 0 | 0 | 0 | 35 | 35 | 2.97 | 130.70 | 6821 |
| enrichment:person_facts | 1 | 51 | 2 | 1 | 0 | 0 | 1 | 0 | 0 | 49 | 124.39 | 334.30 | 9759 |
| enrichment:person_intros | 1 | 377 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 377 | 191.75 | 391.50 | 7525 |
| enrichment:person_sitelinks | 1 | 53 | 4 | 2 | 1 | 0 | 1 | 0 | 0 | 49 | 247.67 | 372.70 | 9759 |

## robots.txt verdict per endpoint

| endpoint | robots_txt_verdict | robots_policy |
| --- | --- | --- |
| en.wikipedia.org/w/api.php | disallowed | report |
| query.wikidata.org/sparql | disallowed | report |
