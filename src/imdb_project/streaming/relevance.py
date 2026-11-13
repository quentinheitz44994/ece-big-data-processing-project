"""Relevance of a Wikipedia change for the IMDb dataset.

Shared by the lookup builder, the streaming job and the late event injector, so
that they all use the same title normalisation and the same title patterns.

A change is relevant when its page is in the lookup table of pages linked to an
IMDb identifier (stream-static join) **or** when its title carries a
disambiguation suffix typical of films, series or film professionals
(``title_patterns`` of the settings). ``match_reason`` records which.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass

from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F

from imdb_project.common.config import Config

REASON_LOOKUP = "lookup"
REASON_PATTERN = "title_pattern"
REASON_BOTH = "lookup+title_pattern"


@dataclass(frozen=True)
class TitlePattern:
    """A title pattern and the entity type it designates."""

    entity_type: str
    pattern: str


def title_patterns(cfg: Config) -> list[TitlePattern]:
    """Return the configured title patterns, in order of precedence."""
    return [
        TitlePattern(str(item["entity_type"]), str(item["pattern"]))
        for item in cfg.streaming.title_patterns
    ]


def normalize_title(title: Column) -> Column:
    """Normalise a page title: underscores to spaces, single spaces, trimmed."""
    return F.trim(F.regexp_replace(F.regexp_replace(title, "_", " "), " +", " "))


def normalize_title_text(title: str) -> str:
    """Python counterpart of :func:`normalize_title`."""
    return re.sub(" +", " ", title.replace("_", " ")).strip()


def pattern_entity_type(title: Column, patterns: Sequence[TitlePattern]) -> Column:
    """Return the entity type of the first pattern matching ``title`` (else null)."""
    result: Column | None = None
    for item in patterns:
        matched = title.rlike(item.pattern)
        result = (
            F.when(matched, F.lit(item.entity_type))
            if result is None
            else result.when(matched, F.lit(item.entity_type))
        )
    return result if result is not None else F.lit(None).cast("string")


def matches_any_pattern(title: str, patterns: Sequence[TitlePattern]) -> bool:
    """Python counterpart of :func:`pattern_entity_type` (any pattern matches)."""
    return any(re.search(item.pattern, title) for item in patterns)


def flag_relevant(
    events: DataFrame, lookup: DataFrame, patterns: Sequence[TitlePattern]
) -> DataFrame:
    """Keep the relevant changes and explain why they are relevant.

    Args:
        events: Parsed changes with ``wiki`` and ``title`` (batch or streaming).
        lookup: Static lookup table with one row per (``wiki``,
            ``page_title_normalized``) and the columns ``imdb_id``,
            ``entity_type`` and ``source_url``.
        patterns: Title patterns.

    Returns:
        The relevant changes with ``page_title_normalized``, ``imdb_id``,
        ``entity_type``, ``lookup_source_url`` and ``match_reason``.
    """
    static = F.broadcast(
        lookup.select(
            "wiki",
            "page_title_normalized",
            "imdb_id",
            F.col("entity_type").alias("lookup_entity_type"),
            F.col("source_url").alias("lookup_source_url"),
        )
    )
    keyed = events.withColumn("page_title_normalized", normalize_title(F.col("title")))
    joined = keyed.join(static, ["wiki", "page_title_normalized"], "left")
    by_pattern = pattern_entity_type(F.col("page_title_normalized"), patterns)
    in_lookup = F.col("imdb_id").isNotNull()
    reason = (
        F.when(in_lookup & by_pattern.isNotNull(), F.lit(REASON_BOTH))
        .when(in_lookup, F.lit(REASON_LOOKUP))
        .when(by_pattern.isNotNull(), F.lit(REASON_PATTERN))
    )
    return (
        joined.withColumn("match_reason", reason)
        .withColumn("entity_type", F.coalesce(F.col("lookup_entity_type"), by_pattern))
        .drop("lookup_entity_type")
        .where(F.col("match_reason").isNotNull())
    )
