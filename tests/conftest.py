"""Shared pytest fixtures: a small local Spark session and test configurations."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pyspark.sql import SparkSession

from imdb_project.common.config import Config, load_config

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import factory  # noqa: E402  (tests/factory.py, importable once tests/ is on sys.path)


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


def _redirect_paths(settings: Config, root: Path) -> Config:
    overrides = {f"paths.{name}": str(root / name) for name in settings.get("paths", Config())}
    return settings.with_overrides(overrides)


@pytest.fixture()
def cfg(settings: Config, tmp_path: Path) -> Config:
    """Settings with every data/output path redirected to a temporary folder."""
    return _redirect_paths(settings, tmp_path)


@pytest.fixture(scope="session")
def raw_cfg(settings: Config, tmp_path_factory: pytest.TempPathFactory) -> Config:
    """Session-wide settings whose raw layer holds the synthetic mini dataset."""
    cfg = _redirect_paths(settings, tmp_path_factory.mktemp("pipeline"))
    factory.write_raw_dataset(Path(cfg.paths.raw))
    return cfg


@pytest.fixture(scope="session")
def bronze_cfg(spark: SparkSession, raw_cfg: Config) -> Config:
    """Settings whose bronze layer has been built from the mini dataset."""
    from imdb_project.preparation import ingest

    ingest.run(spark, raw_cfg)
    return raw_cfg
