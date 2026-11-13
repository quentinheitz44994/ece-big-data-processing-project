"""Builders of small silver tables for the exploration and enrichment tests."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from pyspark.sql import DataFrame, SparkSession

from imdb_project.common import io
from imdb_project.common.config import Config
from imdb_project.common.schemas import TABLES


def silver_df(spark: SparkSession, table: str, rows: Iterable[Mapping[str, Any]]) -> DataFrame:
    """Create a DataFrame with the silver schema of ``table`` from partial rows."""
    schema = TABLES[table].silver_schema
    values = [
        tuple(row.get(f.name, [] if f.name == "dq_flags" else None) for f in schema.fields)
        for row in rows
    ]
    return spark.createDataFrame(values, schema)


def write_silver(
    spark: SparkSession, cfg: Config, table: str, rows: Iterable[Mapping[str, Any]]
) -> None:
    """Write a small silver table to the (temporary) silver layer of ``cfg``."""
    spec = TABLES[table]
    io.write_parquet(
        silver_df(spark, table, rows),
        io.layer_path(cfg, "silver", table),
        partition_by=spec.partition_by or None,
    )


def movie(
    tconst: str,
    year: int | None,
    runtime: int | None,
    genres: list[str] | None,
    title: str | None = None,
    title_type: str = "movie",
    is_adult: bool = False,
    end_year: int | None = None,
) -> dict[str, Any]:
    """Return a ``title_basics`` row."""
    return {
        "tconst": tconst,
        "titleType": title_type,
        "primaryTitle": title or f"Title {tconst}",
        "originalTitle": title or f"Title {tconst}",
        "isAdult": is_adult,
        "startYear": year,
        "endYear": end_year,
        "runtimeMinutes": runtime,
        "genres": genres,
    }


def rating(tconst: str, average: float, votes: int) -> dict[str, Any]:
    """Return a ``title_ratings`` row."""
    return {"tconst": tconst, "averageRating": average, "numVotes": votes}


def person(
    nconst: str, name: str | None = None, birth: int | None = None, death: int | None = None
) -> dict[str, Any]:
    """Return a ``name_basics`` row."""
    return {
        "nconst": nconst,
        "primaryName": name or f"Person {nconst}",
        "birthYear": birth,
        "deathYear": death,
    }


def principal(tconst: str, ordering: int, nconst: str, category: str) -> dict[str, Any]:
    """Return a ``title_principals`` row."""
    return {"tconst": tconst, "ordering": ordering, "nconst": nconst, "category": category}


def crew(
    tconst: str, directors: list[str] | None = None, writers: list[str] | None = None
) -> dict[str, Any]:
    """Return a ``title_crew`` row."""
    return {"tconst": tconst, "directors": directors, "writers": writers}


def episode(tconst: str, parent: str, season: int | None, number: int | None) -> dict[str, Any]:
    """Return a ``title_episode`` row."""
    return {
        "tconst": tconst,
        "parentTconst": parent,
        "seasonNumber": season,
        "episodeNumber": number,
    }
