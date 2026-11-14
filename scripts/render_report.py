"""Run the report renderer using this checkout's code and configuration."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from imdb_project.reporting import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(PROJECT_ROOT))
