"""Synthetic miniature IMDb dataset used by the preparation tests.

Every name and title is invented. The rows are designed so that each data
quality rule of the project has at least one violation (see the trailing
comments), together with clean rows that must go through untouched.
"""

from __future__ import annotations

import gzip
from pathlib import Path

from imdb_project.common.schemas import TABLES

N = "\\N"  # the IMDb marker for a missing value

# fmt: off
NAME_BASICS = [
    ["nm0000001", "Ada Alpha", "1950", "2010", "actress,producer", "tt0000001,tt0000002"],
    ["nm0000002", "Bob Beta", "1960", N, "director,writer", "tt0000001"],
    ["nm0000003", "Cy Gamma", "1980", "1970", "actor", "tt0000002"],             # DQ01
    ["nm0000004", "Di Delta", "1800", "1950", "actor", N],                       # DQ02 (age 150)
    ["nm0000005", "Ed Epsilon", "2090", N, "writer", "tt0000003"],               # DQ02 (future)
    ["nm0000006", "Flo Zeta", "1900", "1950", "actress", "tt0000005"],           # DQ03 via principals
    ["nm0000007", "Gus Eta", "1990", N, "actor", "tt0000001,tt9999999"],         # DQ04, DQ05 (knownFor)
    ["nm0000008", "Hal Theta", N, N, N, N],
    ["nm0000009", "   ", "abc", N, "actor,", "tt0000001"],                       # whitespace, DQ09
    ["nm0000001", "Ada Alpha", "1950", "2010", "actress,producer", "tt0000001,tt0000002"],  # DQ10 exact
    ["nm0000010", "Ivy Iota", "1970", N, "actress", "tt0000004"],
    ["nm0000010", "Ivy Iota-Conflict", "1971", N, "actress", "tt0000004"],       # DQ10 conflicting
    ["nm0000011", "Jo Kappa", "", N, "actor", "tt0000001"],                      # empty raw field
    ["nm0000012", "Short Row", "1970"],                                          # malformed line
]

TITLE_BASICS = [
    ["tt0000001", "movie", 'Alpha "The Quote" Film', "Alpha Film", "0", "1985", N, "100", "Drama,Comedy"],
    ["tt0000002", "movie", "Beta", "Beta", "0", "1995", N, "0", "Drama"],                   # DQ08 (<= 0)
    ["tt0000003", "movie", "Gamma", "Gamma", "0", "2000", N, "5000", "Documentary"],        # DQ08 (> max)
    ["tt0000004", "movie", "Delta", "Delta", "2", "2001", N, "90", "Comedy"],               # DQ09 isAdult
    ["tt0000005", "movie", "Epsilon", "Epsilon", "0", "2000", N, "95", "Telepathy,Drama"],  # DQ13
    ["tt0000006", "tvSeries", "Series One", "Series One", "0", "2005", "2001", "30", "Drama"],  # DQ06
    ["tt0000007", "tvEpisode", "S1 E1", "S1 E1", "0", "2005", N, "30", "Drama"],
    ["tt0000008", "tvEpisode", "S1 E2", "S1 E2", "0", "2005", N, "30", "Drama"],
    ["tt0000009", "movie", "Future", "Future", "0", "2099", N, "90", "Sci-Fi"],             # DQ07
    ["tt0000010", "movie", "Shifted", "Shifted", "0", "1999", N, "Reality-TV", "Talk-Show"],  # DQ09
    ["tt0000011", "short", "Short", "Short", "0", "1990", N, "10", "Short"],
    ["tt0000012", "tvEpisode", "Orphan Ep", "Orphan Ep", "0", "2006", N, "30", "Comedy"],
    ["tt0000013", "movie", "No Rating", "No Rating", "0", "1990", N, N, N],
]

TITLE_RATINGS = [
    ["tt0000001", "8.5", "15000"],
    ["tt0000002", "5.0", "2000"],
    ["tt0000003", "7.0", "1200"],
    ["tt0000004", "6.1", "0"],       # DQ12 (votes <= 0)
    ["tt0000005", "11.0", "500"],    # DQ12 (rating out of range)
    ["tt0000006", "7.7", "3000"],
    ["tt0000007", "8.0", "100"],
    ["tt0000008", "6.0", "100"],
    ["tt7777777", "5.5", "10"],      # DQ05 orphan tconst
]

TITLE_CREW = [
    ["tt0000001", "nm0000002", "nm0000002,nm0000005"],
    ["tt0000002", "nm0000002", N],
    ["tt0000003", "nm8888888", "nm0000005"],   # DQ05 orphan director
    ["tt6666666", "nm0000002", N],             # DQ05 orphan tconst
    ["tt0000004", N, N],
]

TITLE_EPISODE = [
    ["tt0000007", "tt0000006", "1", "1"],
    ["tt0000008", "tt0000006", "1", "0"],      # DQ14 (episode <= 0)
    ["tt0000012", "tt0000001", "1", "1"],      # DQ11 (parent is a movie)
    ["tt0000014", "tt5555555", "2", "3"],      # DQ05 orphan tconst and parentTconst
    ["tt0000013", "tt0000006", "x", "2"],      # DQ14 (non numeric)
]

TITLE_PRINCIPALS = [
    ["tt0000001", "1", "nm0000001", "actress", N, '["Lead","Narrator"]'],
    ["tt0000001", "2", "nm0000002", "director", N, N],
    ["tt0000001", "3", "nm0000007", "actor", N, '["Kid"]'],            # DQ04 (1985 < born 1990)
    ["tt0000002", "1", "nm0000003", "actor", N, '["Hero"]'],
    ["tt0000005", "1", "nm0000006", "actress", N, '["Ghost"]'],        # DQ03 (2000 > 1950 + 5)
    ["tt0000003", "1", "nm0000006", "archive_footage", N, '["Self"]'],  # posthumous but archive
    ["tt0000003", "2", "nm4444444", "actor", N, '["X"]'],              # DQ05 orphan nconst
    ["tt3333333", "1", "nm0000001", "actress", N, '["Y"]'],            # DQ05 orphan tconst
    ["tt0000001", "1", "nm0000001", "actress", N, '["Lead","Narrator"]'],  # DQ10 exact duplicate
    ["tt0000004", "1", "nm0000010", "actress", "lead", "[not json]"],  # invalid characters array
]

TITLE_AKAS = [
    ["tt0000001", "1", "Alpha Film", N, N, "original", N, "1"],
    ["tt0000001", "2", "Film Alpha", "FR", "fr", "imdbDisplay", N, "0"],
    ["tt0000001", "3", "Alpha", "US", "en", "dvd\x02video", "short title\x02informal title", "0"],
    ["tt2222222", "1", "Ghost Title", "US", N, N, N, "0"],             # DQ05 orphan titleId
    ["tt0000002", "1", "Beta", N, N, "original", N, "7"],              # DQ09 isOriginalTitle
]
# fmt: on

DATASET: dict[str, list[list[str]]] = {
    "name_basics": NAME_BASICS,
    "title_basics": TITLE_BASICS,
    "title_ratings": TITLE_RATINGS,
    "title_crew": TITLE_CREW,
    "title_episode": TITLE_EPISODE,
    "title_principals": TITLE_PRINCIPALS,
    "title_akas": TITLE_AKAS,
}


def write_raw_dataset(raw_dir: Path) -> None:
    """Write the synthetic tables as ``*.tsv.gz`` files named like the IMDb ones."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    for table, rows in DATASET.items():
        spec = TABLES[table]
        lines = ["\t".join(spec.columns)] + ["\t".join(row) for row in rows]
        with gzip.open(raw_dir / spec.source_file, "wt", encoding="utf-8", newline="") as handle:
            handle.write("\n".join(lines) + "\n")
