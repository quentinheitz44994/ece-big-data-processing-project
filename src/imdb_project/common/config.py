"""Configuration loading (``conf/settings.yaml``).

Every tunable of the project (thresholds, years, top-N, paths, rate limits...)
lives in one YAML file. :class:`Config` gives read-only, attribute-style and
dotted-path access to it.
"""

from __future__ import annotations

import argparse
import os
import re
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG_PATH = "conf/settings.yaml"
CONFIG_ENV_VAR = "IMDB_PROJECT_CONFIG"

# ${NAME} or ${NAME:-default}
_ENV_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}")
_MISSING = object()


class ConfigError(KeyError):
    """Raised when a required configuration key is missing."""


class Config(Mapping[str, Any]):
    """Read-only view over a nested configuration dictionary.

    Nested dictionaries are returned as :class:`Config` objects, so both
    ``cfg.exploration.min_votes`` and ``cfg.get("exploration.min_votes")`` work.

    Args:
        data: The underlying (nested) dictionary.
        prefix: Dotted path of this node, used in error messages.
    """

    def __init__(self, data: Mapping[str, Any] | None = None, prefix: str = "") -> None:
        self._data: dict[str, Any] = dict(data or {})
        self._prefix = prefix

    def _wrap(self, key: str, value: Any) -> Any:
        if isinstance(value, Mapping):
            child_prefix = f"{self._prefix}.{key}" if self._prefix else key
            return Config(value, child_prefix)
        return value

    def __getitem__(self, key: str) -> Any:
        if key not in self._data:
            path = f"{self._prefix}.{key}" if self._prefix else key
            raise ConfigError(f"Missing configuration key: {path}")
        return self._wrap(key, self._data[key])

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        try:
            return self[name]
        except ConfigError as exc:
            raise AttributeError(str(exc)) from exc

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Config({self._data!r})"

    def get(self, path: str, default: Any = None) -> Any:
        """Return the value at a dotted ``path`` or ``default`` when absent.

        Args:
            path: Key or dotted path such as ``"exploration.q1.z_threshold"``.
            default: Value returned when any segment of the path is missing.

        Returns:
            The value (nested mappings wrapped in :class:`Config`).
        """
        node: Any = self
        for part in path.split("."):
            if not isinstance(node, Config) or part not in node._data:
                return default
            node = node[part]
        return node

    def require(self, path: str) -> Any:
        """Return the value at a dotted ``path`` or raise :class:`ConfigError`."""
        value = self.get(path, _MISSING)
        if value is _MISSING:
            full = f"{self._prefix}.{path}" if self._prefix else path
            raise ConfigError(f"Missing configuration key: {full}")
        return value

    def to_dict(self) -> dict[str, Any]:
        """Return a deep copy of the underlying dictionary."""
        return _deep_copy(self._data)

    def with_overrides(self, overrides: Mapping[str, Any]) -> Config:
        """Return a new :class:`Config` with dotted-path ``overrides`` applied.

        Args:
            overrides: Mapping of dotted path to new value,
                e.g. ``{"enrichment.scope.top_n": None}``.

        Returns:
            A new configuration object; the current one is left untouched.
        """
        data = self.to_dict()
        for path, value in overrides.items():
            node = data
            parts = path.split(".")
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            node[parts[-1]] = value
        return Config(data, self._prefix)


def _deep_copy(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _deep_copy(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_deep_copy(item) for item in value]
    return value


def expand_env(value: Any, env: Mapping[str, str] | None = None) -> Any:
    """Recursively expand ``${VAR}`` / ``${VAR:-default}`` in string values.

    Args:
        value: A scalar, list or mapping loaded from YAML.
        env: Environment mapping (defaults to ``os.environ``).

    Returns:
        The same structure with environment references substituted. A reference
        to an unset variable without default expands to an empty string.
    """
    environment = os.environ if env is None else env

    def substitute(match: re.Match[str]) -> str:
        name, default = match.group(1), match.group(2)
        resolved = environment.get(name)
        if resolved is None or resolved == "":
            return default if default is not None else ""
        return resolved

    if isinstance(value, str):
        return _ENV_PATTERN.sub(substitute, value)
    if isinstance(value, Mapping):
        return {key: expand_env(item, environment) for key, item in value.items()}
    if isinstance(value, list):
        return [expand_env(item, environment) for item in value]
    return value


def load_config(path: str | os.PathLike[str] | None = None) -> Config:
    """Load the YAML configuration file.

    Args:
        path: Path of the YAML file. Defaults to ``$IMDB_PROJECT_CONFIG`` or
            ``conf/settings.yaml`` relative to the working directory.

    Returns:
        The parsed configuration with environment variables expanded.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    resolved = Path(path or os.environ.get(CONFIG_ENV_VAR) or DEFAULT_CONFIG_PATH)
    if not resolved.is_file():
        raise FileNotFoundError(f"Configuration file not found: {resolved}")
    with resolved.open(encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    return Config(expand_env(raw))


def add_config_argument(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Add the standard ``--config`` option to a job argument parser."""
    parser.add_argument(
        "--config",
        default=None,
        help=f"YAML settings file (default: ${CONFIG_ENV_VAR} or {DEFAULT_CONFIG_PATH}).",
    )
    return parser
