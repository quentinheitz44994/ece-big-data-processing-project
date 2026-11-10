"""Logging helper shared by every job."""

from __future__ import annotations

import logging
import sys

_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
_ROOT_NAME = "imdb_project"


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Return a logger of the project hierarchy writing to stderr.

    The handler is attached once to the ``imdb_project`` root logger, so calling
    this function from several modules never duplicates log lines.

    Args:
        name: Usually ``__name__`` of the calling module.
        level: Logging level of the project root logger.

    Returns:
        A configured :class:`logging.Logger`.
    """
    root = logging.getLogger(_ROOT_NAME)
    if not root.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(_FORMAT, _DATE_FORMAT))
        root.addHandler(handler)
        root.setLevel(level)
        root.propagate = False
    if name == "__main__" or not name.startswith(_ROOT_NAME):
        name = f"{_ROOT_NAME}.{name.strip('_') or 'main'}"
    return logging.getLogger(name)
