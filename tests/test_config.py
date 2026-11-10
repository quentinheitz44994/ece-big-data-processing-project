from __future__ import annotations

import pytest

from imdb_project.common.config import Config, ConfigError, expand_env, load_config


def test_attribute_and_dotted_access():
    cfg = Config({"a": {"b": {"c": 3}}, "x": [1, 2]})
    assert cfg.a.b.c == 3
    assert cfg.get("a.b.c") == 3
    assert cfg["x"] == [1, 2]
    assert cfg.get("a.missing", "fallback") == "fallback"
    assert cfg.get("a.b.c.d", 7) == 7


def test_require_reports_full_path():
    cfg = Config({"a": {"b": 1}})
    assert cfg.require("a.b") == 1
    with pytest.raises(ConfigError, match="a.c"):
        cfg.require("a.c")
    with pytest.raises(AttributeError):
        _ = cfg.a.nope


def test_with_overrides_does_not_mutate_original():
    cfg = Config({"scope": {"top_n": 10, "year_min": 1980}})
    changed = cfg.with_overrides({"scope.top_n": None, "new.key": "v"})
    assert changed.scope.top_n is None
    assert changed.new.key == "v"
    assert cfg.scope.top_n == 10
    assert "new" not in cfg


def test_expand_env_defaults_and_values():
    env = {"SET": "value", "EMPTY": ""}
    data = {
        "a": "${SET}",
        "b": "${UNSET:-fallback}",
        "c": ["x-${EMPTY:-d}"],
        "d": "${UNSET}",
        "e": 5,
    }
    assert expand_env(data, env) == {"a": "value", "b": "fallback", "c": ["x-d"], "d": "", "e": 5}


def test_load_config_reads_yaml_and_expands(tmp_path, monkeypatch):
    path = tmp_path / "settings.yaml"
    path.write_text("kafka:\n  servers: ${TEST_BOOTSTRAP:-kafka:19092}\n", encoding="utf-8")
    assert load_config(path).kafka.servers == "kafka:19092"
    monkeypatch.setenv("TEST_BOOTSTRAP", "localhost:9092")
    assert load_config(path).kafka.servers == "localhost:9092"
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "missing.yaml")


def test_repository_settings_have_core_sections(settings):
    for key in ("spark.shuffle_partitions", "paths.bronze", "paths.outputs", "kafka.topic"):
        assert settings.require(key) is not None
