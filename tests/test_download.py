from __future__ import annotations

import gzip
import os
import subprocess
from pathlib import Path

import pytest

from imdb_project.common.schemas import TABLES


@pytest.mark.parametrize("corrupt", [False, True])
def test_existing_downloads_are_checked_before_skipping(tmp_path, corrupt):
    raw = tmp_path / "raw"
    raw.mkdir()
    for spec in TABLES.values():
        (raw / spec.source_file).write_bytes(gzip.compress(b"header\nsynthetic row\n"))
    if corrupt:
        (raw / "name.basics.tsv.gz").write_bytes(b"incomplete archive")
    snapshot = tmp_path / "snapshot.md"
    result = subprocess.run(
        ["bash", str(Path("scripts/download_imdb.sh").resolve())],
        env={
            **os.environ,
            "IMDB_RAW_DIR": str(raw),
            "IMDB_SNAPSHOT_FILE": str(snapshot),
            "IMDB_BASE_URL": "https://unused.invalid",
        },
        capture_output=True,
        text=True,
        check=False,
    )
    if corrupt:
        assert result.returncode != 0 and "--force" in result.stderr
        assert not snapshot.exists()
    else:
        assert result.returncode == 0, result.stderr
        assert snapshot.read_text().count("already present") == 7
