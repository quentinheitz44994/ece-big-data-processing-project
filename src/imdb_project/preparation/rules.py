"""Declarative data quality rules (DQ01 to DQ16).

Two kinds of rules, both evaluated on the standardised tables of
:mod:`imdb_project.preparation.standardize`:

* :class:`RowRule`: a Spark condition on the columns of one row;
* :class:`KeyRule`: a rule that needs other rows or other tables (foreign keys,
  duplicates, cross-table consistency). It returns the *keys* of the violating
  rows, which are then matched against the table.

The same definitions drive the quality report (``quality_checks.py``) and the
flags / quarantine of the silver layer (``cleaning.py``). Rules marked
``quarantine=True`` identify structurally invalid rows.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass

from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F

from imdb_project.common.config import Config
from imdb_project.common.schemas import CORRUPT_RECORD_COLUMN, TABLES
from imdb_project.preparation.standardize import CAST_ERRORS_COLUMN

Tables = Mapping[str, DataFrame]


@dataclass(frozen=True)
class RowRule:
    """Rule expressed as a condition on a single row.

    Attributes:
        rule_id: Identifier written in ``dq_flags``.
        table: Table the rule applies to.
        description: Short description used in the reports.
        condition: Builds the violation condition from the configuration.
        quarantine: Whether violating rows are excluded from silver.
    """

    rule_id: str
    table: str
    description: str
    condition: Callable[[Config], Column]
    quarantine: bool = False


@dataclass(frozen=True)
class KeyRule:
    """Rule whose violations are identified by a set of keys.

    Attributes:
        rule_id: Identifier written in ``dq_flags``.
        table: Table the rule applies to.
        description: Short description used in the reports.
        key_columns: Columns of ``table`` matched against the violating keys.
        keys: Builds the distinct violating keys (columns ``key_columns``).
        quarantine: Whether violating rows are excluded from silver.
    """

    rule_id: str
    table: str
    description: str
    key_columns: tuple[str, ...]
    keys: Callable[[Tables, Config], DataFrame]
    quarantine: bool = False


Rule = RowRule | KeyRule


# ------------------------------------------------------------------ parameters


def quality_settings(cfg: Config) -> Config:
    """Return the ``preparation.quality`` section of the settings."""
    return cfg.require("preparation.quality")


def reference_year(cfg: Config) -> int:
    """Year used by the "in the future" rules (current year unless configured)."""
    configured = quality_settings(cfg).get("reference_year")
    return int(configured) if configured else dt.datetime.now(dt.UTC).year


# ------------------------------------------------------------- key set builders


def orphan_keys(child: DataFrame, fk: str, parent: DataFrame, pk: str) -> DataFrame:
    """Return the distinct non-null values of ``child.fk`` absent from ``parent.pk``.

    Args:
        child: Table holding the foreign key.
        fk: Foreign key column of ``child``.
        parent: Referenced table.
        pk: Referenced column of ``parent``.

    Returns:
        A DataFrame with the single column ``fk``.
    """
    values = child.select(F.col(fk)).where(F.col(fk).isNotNull()).distinct()
    parents = parent.select(F.col(pk).alias(fk)).where(F.col(fk).isNotNull()).distinct()
    return values.join(parents, fk, "left_anti")


def orphan_array_owner_keys(
    child: DataFrame,
    array_column: str,
    owner_keys: Sequence[str],
    parent: DataFrame,
    pk: str,
) -> DataFrame:
    """Return the keys of the rows whose array holds at least one orphan value.

    Args:
        child: Table holding the array of foreign keys.
        array_column: ``array<string>`` column of ``child``.
        owner_keys: Key columns of ``child`` identifying the row.
        parent: Referenced table.
        pk: Referenced column of ``parent``.

    Returns:
        The distinct ``owner_keys`` of the violating rows.
    """
    exploded = child.select(*owner_keys, F.explode(array_column).alias("_element"))
    orphans = orphan_keys(exploded, "_element", parent, pk)
    # Orphan values are few: broadcasting them avoids shuffling the exploded table.
    return (
        exploded.join(F.broadcast(orphans), "_element", "left_semi").select(*owner_keys).distinct()
    )


def duplicate_keys(df: DataFrame, key_columns: Sequence[str]) -> DataFrame:
    """Return the primary key values carried by more than one row."""
    not_null = df
    for column in key_columns:
        not_null = not_null.where(F.col(column).isNotNull())
    return not_null.groupBy(*key_columns).count().where(F.col("count") > 1).select(*key_columns)


def _people_with(tables: Tables, year_column: str) -> DataFrame:
    """People whose ``year_column`` is known: a few hundred thousand rows."""
    return (
        tables["name_basics"]
        .select("nconst", year_column)
        .where(F.col(year_column).isNotNull())
        .dropDuplicates(["nconst"])
    )


def _dated_titles(tables: Tables) -> DataFrame:
    return (
        tables["title_basics"]
        .select("tconst", "titleType", "startYear", "endYear")
        .where(F.col("startYear").isNotNull())
        .dropDuplicates(["tconst"])
    )


def posthumous_credit_keys(tables: Tables, cfg: Config) -> DataFrame:
    """Keys of principals credited on a title released long after their death.

    A credit is reported when ``startYear > deathYear + posthumous_grace_years``,
    unless its category is exempt (archive material, or roles such as writer for
    which posthumous credits are ordinary) or its job / characters mention archive
    material.

    The year comparison only reads the light columns of ``title_principals``; the
    ``job`` and ``characters`` columns (the latter is a parsed JSON array) are
    read for the few candidate rows only.
    """
    quality = quality_settings(cfg)
    archive = quality.get("archive_pattern", "(?i)archive")
    exempt = list(quality.get("posthumous_exempt_categories", []))
    grace = int(quality.posthumous_grace_years)
    principals = tables["title_principals"]

    credits = principals.select("tconst", "ordering", "nconst", "category").where(
        ~F.col("category").isin(exempt)
    )
    candidates = (
        credits.join(F.broadcast(_people_with(tables, "deathYear")), "nconst")
        .join(_dated_titles(tables).select("tconst", "startYear"), "tconst")
        .where(F.col("startYear") > F.col("deathYear") + grace)
        .select("tconst", "ordering")
        .distinct()
    )
    mentions_archive = F.coalesce(F.col("job"), F.lit("")).rlike(archive) | F.coalesce(
        F.array_join(F.col("characters"), " "), F.lit("")
    ).rlike(archive)
    return (
        principals.select("tconst", "ordering", "job", "characters")
        .join(F.broadcast(candidates), ["tconst", "ordering"], "left_semi")
        .where(~mentions_archive)
        .select("tconst", "ordering")
        .distinct()
    )


def credit_before_birth_keys(tables: Tables, cfg: Config) -> DataFrame:
    """Keys of principals credited on a title that was over before they were born.

    The last year of a title is ``endYear`` when known, otherwise ``startYear``.
    A series without ``endYear`` may still be running, so it is never reported.
    """
    series_types = list(quality_settings(cfg).episode_parent_types)
    last_year = F.coalesce(
        F.col("endYear"),
        F.when(~F.col("titleType").isin(series_types), F.col("startYear")),
    )
    finished = (
        _dated_titles(tables)
        .select("tconst", last_year.alias("last_year"))
        .where(F.col("last_year").isNotNull())
    )
    return (
        tables["title_principals"]
        .select("tconst", "ordering", "nconst")
        .join(F.broadcast(_people_with(tables, "birthYear")), "nconst")
        .join(finished, "tconst")
        .where(F.col("last_year") < F.col("birthYear"))
        .select("tconst", "ordering")
        .distinct()
    )


def episode_parent_type_keys(tables: Tables, cfg: Config) -> DataFrame:
    """Keys of the episodes whose existing parent title is not a series."""
    valid_types = list(quality_settings(cfg).episode_parent_types)
    parents = (
        tables["title_basics"]
        .select(F.col("tconst").alias("parentTconst"), "titleType")
        .dropDuplicates(["parentTconst"])
    )
    return (
        tables["title_episode"]
        .select("tconst", "parentTconst")
        .join(parents, "parentTconst")
        .where(F.col("titleType").isNull() | ~F.col("titleType").isin(valid_types))
        .select("tconst")
        .distinct()
    )


# ------------------------------------------------------------------ rule list


def _scalar_fk_rule(table: str, fk: str, parent: str, pk: str) -> KeyRule:
    return KeyRule(
        rule_id=f"DQ05:{fk}",
        table=table,
        description=f"Orphan foreign key: {table}.{fk} has no parent row in {parent}.{pk}",
        key_columns=(fk,),
        keys=lambda tables, cfg: orphan_keys(tables[table], fk, tables[parent], pk),
        quarantine=True,
    )


def _array_fk_rule(table: str, array_column: str, parent: str, pk: str) -> KeyRule:
    owner_keys = TABLES[table].primary_key
    return KeyRule(
        rule_id=f"DQ05:{array_column}",
        table=table,
        description=(
            f"Orphan foreign key: at least one value of {table}.{array_column} "
            f"has no parent row in {parent}.{pk}"
        ),
        key_columns=owner_keys,
        keys=lambda tables, cfg: orphan_array_owner_keys(
            tables[table], array_column, owner_keys, tables[parent], pk
        ),
    )


def _duplicate_rule(table: str) -> KeyRule:
    key_columns = TABLES[table].primary_key
    return KeyRule(
        rule_id="DQ10",
        table=table,
        description=f"Duplicated primary key ({', '.join(key_columns)})",
        key_columns=key_columns,
        keys=lambda tables, cfg: duplicate_keys(tables[table], key_columns),
        quarantine=True,
    )


def _cast_rule(table: str) -> RowRule:
    converted = sorted({*TABLES[table].casts, *TABLES[table].arrays})
    return RowRule(
        rule_id="DQ09",
        table=table,
        description=(
            "Value that cannot be converted to its expected type "
            f"({', '.join(converted)}), e.g. non-numeric number or flag not in {{0,1}}"
        ),
        condition=lambda cfg: F.size(F.col(CAST_ERRORS_COLUMN)) > 0,
    )


def _malformed_rule(table: str) -> RowRule:
    return RowRule(
        rule_id="DQ15",
        table=table,
        description="Malformed line: number of fields different from the header",
        condition=lambda cfg: F.col(CORRUPT_RECORD_COLUMN).isNotNull(),
        quarantine=True,
    )


def _missing_key_rule(table: str) -> RowRule:
    keys = TABLES[table].primary_key
    return RowRule(
        rule_id="DQ16",
        table=table,
        description=f"Missing primary key component ({', '.join(keys)})",
        condition=lambda cfg: F.greatest(
            F.lit(False), *[F.col(column).isNull() for column in keys]
        ),
        quarantine=True,
    )


def _unknown_genre(cfg: Config) -> Column:
    known = list(quality_settings(cfg).known_genres)
    return F.exists(F.col("genres"), lambda genre: ~genre.isin(known))


def _episode_numbers(cfg: Config) -> Column:
    non_numeric = F.arrays_overlap(
        F.col(CAST_ERRORS_COLUMN), F.array(F.lit("seasonNumber"), F.lit("episodeNumber"))
    )
    return (F.col("seasonNumber") <= 0) | (F.col("episodeNumber") <= 0) | non_numeric


def build_rules() -> list[Rule]:
    """Return every quality rule of the project, ordered by rule id and table."""
    rules: list[Rule] = [
        RowRule(
            "DQ01",
            "name_basics",
            "deathYear earlier than birthYear",
            lambda cfg: F.col("deathYear") < F.col("birthYear"),
        ),
        RowRule(
            "DQ02",
            "name_basics",
            "Age at death above max_age_years, or birthYear / deathYear after the reference year",
            lambda cfg: (
                (F.col("deathYear") - F.col("birthYear") > int(quality_settings(cfg).max_age_years))
                | (F.col("birthYear") > reference_year(cfg))
                | (F.col("deathYear") > reference_year(cfg))
            ),
        ),
        KeyRule(
            "DQ03",
            "title_principals",
            "Principal credited on a title released more than posthumous_grace_years "
            "after their death (archive material and exempt categories excluded)",
            ("tconst", "ordering"),
            posthumous_credit_keys,
        ),
        KeyRule(
            "DQ04",
            "title_principals",
            "Principal credited on a title that was released (or, for a series, ended) "
            "before their birth year",
            ("tconst", "ordering"),
            credit_before_birth_keys,
        ),
        _scalar_fk_rule("title_principals", "tconst", "title_basics", "tconst"),
        _scalar_fk_rule("title_principals", "nconst", "name_basics", "nconst"),
        _scalar_fk_rule("title_ratings", "tconst", "title_basics", "tconst"),
        _scalar_fk_rule("title_crew", "tconst", "title_basics", "tconst"),
        _array_fk_rule("title_crew", "directors", "name_basics", "nconst"),
        _array_fk_rule("title_crew", "writers", "name_basics", "nconst"),
        _scalar_fk_rule("title_episode", "tconst", "title_basics", "tconst"),
        _scalar_fk_rule("title_episode", "parentTconst", "title_basics", "tconst"),
        _scalar_fk_rule("title_akas", "titleId", "title_basics", "tconst"),
        _array_fk_rule("name_basics", "knownForTitles", "title_basics", "tconst"),
        RowRule(
            "DQ06",
            "title_basics",
            "endYear earlier than startYear",
            lambda cfg: F.col("endYear") < F.col("startYear"),
        ),
        RowRule(
            "DQ07",
            "title_basics",
            "startYear later than the reference year + max_future_years",
            lambda cfg: (
                F.col("startYear")
                > reference_year(cfg) + int(quality_settings(cfg).max_future_years)
            ),
        ),
        RowRule(
            "DQ08",
            "title_basics",
            "runtimeMinutes <= 0 or above max_runtime_minutes",
            lambda cfg: (
                (F.col("runtimeMinutes") <= 0)
                | (F.col("runtimeMinutes") > int(quality_settings(cfg).max_runtime_minutes))
            ),
        ),
        *[
            _cast_rule(table)
            for table in (
                "name_basics",
                "title_akas",
                "title_basics",
                "title_principals",
                "title_ratings",
            )
        ],
        *[_duplicate_rule(table) for table in sorted(TABLES)],
        KeyRule(
            "DQ11",
            "title_episode",
            "Episode whose parent title is not of an episode_parent_types type",
            ("tconst",),
            episode_parent_type_keys,
        ),
        RowRule(
            "DQ12",
            "title_ratings",
            "averageRating outside [rating_min, rating_max] or numVotes <= 0",
            lambda cfg: (
                (F.col("averageRating") < float(quality_settings(cfg).rating_min))
                | (F.col("averageRating") > float(quality_settings(cfg).rating_max))
                | (F.col("numVotes") <= 0)
            ),
        ),
        RowRule(
            "DQ13",
            "title_basics",
            "Genre outside the known_genres list",
            _unknown_genre,
        ),
        RowRule(
            "DQ14",
            "title_episode",
            "seasonNumber or episodeNumber <= 0 or non-numeric",
            _episode_numbers,
        ),
        *[_malformed_rule(table) for table in sorted(TABLES)],
        *[_missing_key_rule(table) for table in sorted(TABLES)],
    ]
    return sorted(rules, key=lambda rule: (rule.rule_id, rule.table))


def rules_for_table(rules: Sequence[Rule], table: str) -> list[Rule]:
    """Return the rules applying to ``table``."""
    return [rule for rule in rules if rule.table == table]
