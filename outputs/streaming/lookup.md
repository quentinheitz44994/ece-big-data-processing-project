# Streaming lookup table (Wikipedia pages linked to IMDb identifiers)

## Parameters

| parameter | value |
| --- | --- |
| wikis | enwiki, frwiki |
| lookup.titles | 30000 |
| lookup.title_types | movie->film, tvMovie->film, tvSeries->tv_series, tvMiniSeries->tv_series |
| lookup.people | 20000 |
| lookup.principal_categories | actor, actress, director, writer |
| identifier_mapping | Wikidata P345 and sitelinks |
| pages | 88273 |

## IMDb identifiers of the lookup scope

| entity_type | identifiers | identifiers_with_a_page | pct_with_a_page |
| --- | --- | --- | --- |
| film | 25450 | 24326 | 95.58 |
| person | 25192 | 19622 | 77.89 |
| tv_series | 5973 | 5437 | 91.03 |

## Pages per wiki and entity type

| wiki | entity_type | pages |
| --- | --- | --- |
| enwiki | film | 24198 |
| enwiki | person | 19217 |
| enwiki | tv_series | 5410 |
| frwiki | film | 20012 |
| frwiki | person | 15327 |
| frwiki | tv_series | 4109 |
