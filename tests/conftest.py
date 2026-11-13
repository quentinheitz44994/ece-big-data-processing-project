"""Shared pytest fixtures: a small local Spark session and a base configuration."""

from __future__ import annotations

from pathlib import Path

import pytest
from pyspark.sql import SparkSession

from imdb_project.common.config import Config, load_config

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def spark() -> SparkSession:
    session = (
        SparkSession.builder.master("local[2]")
        .appName("imdb-project-tests")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.default.parallelism", "2")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.driver.memory", "1g")
        .getOrCreate()
    )
    session.sparkContext.setLogLevel("ERROR")
    yield session
    session.stop()


@pytest.fixture(scope="session")
def settings() -> Config:
    """The real settings file of the repository."""
    return load_config(REPO_ROOT / "conf" / "settings.yaml")


@pytest.fixture()
def cfg(settings: Config, tmp_path: Path) -> Config:
    """Settings with every data/output path redirected to a temporary folder."""
    overrides = {f"paths.{name}": str(tmp_path / name) for name in settings.get("paths", Config())}
    return settings.with_overrides(overrides)
