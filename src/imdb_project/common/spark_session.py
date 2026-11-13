"""Spark session factory driven by ``conf/settings.yaml``."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pyspark.sql import SparkSession

from imdb_project.common.config import Config


def build_spark(
    cfg: Config,
    app_name: str | None = None,
    extra_conf: Mapping[str, Any] | None = None,
) -> SparkSession:
    """Create (or reuse) the Spark session of a job.

    The driver memory is not set here: with ``spark-submit`` the JVM is already
    running when this code executes, so it comes from ``SPARK_DRIVER_MEMORY``
    (see ``compose.yaml`` and ``scripts/_common.sh``).

    Args:
        cfg: Project configuration (section ``spark``).
        app_name: Application name suffix shown in the Spark UI.
        extra_conf: Job-specific Spark configuration overriding the settings file.

    Returns:
        The active :class:`pyspark.sql.SparkSession`.
    """
    spark_cfg = cfg.get("spark", Config())
    name = spark_cfg.get("app_name", "imdb-project")
    if app_name:
        name = f"{name}:{app_name}"

    builder = (
        SparkSession.builder.appName(name)
        .config("spark.sql.shuffle.partitions", str(spark_cfg.get("shuffle_partitions", 64)))
        .config("spark.sql.adaptive.enabled", str(spark_cfg.get("adaptive_enabled", True)).lower())
        .config("spark.sql.session.timeZone", spark_cfg.get("session_timezone", "UTC"))
        .config("spark.ui.showConsoleProgress", "false")
        # Parquet written by the project is read back by the project only.
        .config("spark.sql.parquet.compression.codec", "snappy")
        .config("spark.sql.sources.partitionOverwriteMode", "static")
    )
    master = spark_cfg.get("master")
    if master:
        builder = builder.master(master)

    merged: dict[str, Any] = {}
    merged.update(spark_cfg.get("extra_conf", Config()) or {})
    merged.update(extra_conf or {})
    for key, value in merged.items():
        builder = builder.config(key, str(value))

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel(spark_cfg.get("log_level", "WARN"))
    return spark
