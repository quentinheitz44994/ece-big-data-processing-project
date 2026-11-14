from pathlib import Path

import pytest
import yaml

from imdb_project import reporting
from imdb_project.common.config import Config, load_config


@pytest.fixture()
def report_project(tmp_path):
    prefix = b"\xef\xbb\xbf# Report\r\nAuthor: \xc3\x89lodie\r\n<!-- AUTO:preparation:start -->"
    middle = b"<!-- AUTO:preparation:end -->\r\nKeep  two spaces.\r\n<!-- AUTO:q1:start -->"
    suffix = b"<!-- AUTO:q1:end -->\r\n<!-- TODO(authors): human reasoning -->\r\n"
    original = prefix + b"old preparation" + middle + b"old exploration" + suffix
    (tmp_path / "REPORT.md").write_bytes(original)
    outputs = tmp_path / "outputs"
    outputs.mkdir()
    (outputs / "preparation.md").write_bytes(b"# Counts\n\n| rows |\n| --- |\n| 42 |\n")
    (outputs / "exploration.md").write_bytes(b"# Q1\n\n| value |\n| --- |\n| 7 |\n")
    cfg = Config(
        {
            "paths": {"outputs": "outputs"},
            "report": {
                "path": "REPORT.md",
                "blocks": {
                    "preparation": {"files": ["preparation.md"], "heading_offset": 3},
                    "q1": {"files": ["exploration.md"], "heading_offset": 4},
                },
            },
        }
    )
    return cfg, tmp_path, original, prefix, middle, suffix


def test_author_bytes_markers_crlf_and_utf8_are_preserved(report_project):
    cfg, root, original, prefix, middle, suffix = report_project
    assert not reporting.run(cfg, root)
    preparation = b"\r\n\r\n#### Counts\r\n\r\n| rows |\r\n| --- |\r\n| 42 |\r\n\r\n"
    exploration = b"\r\n\r\n##### Q1\r\n\r\n| value |\r\n| --- |\r\n| 7 |\r\n\r\n"
    assert (root / "REPORT.md").read_bytes() == prefix + preparation + middle + exploration + suffix
    assert (root / "REPORT.md").read_bytes() != original


def test_rerender_is_idempotent_without_rewriting_the_file(report_project):
    cfg, root, *_ = report_project
    reporting.run(cfg, root)
    report = root / "REPORT.md"
    content, modified = report.read_bytes(), report.stat().st_mtime_ns
    assert reporting.run(cfg, root)
    assert report.read_bytes() == content
    assert report.stat().st_mtime_ns == modified


def test_check_is_read_only_for_both_stale_and_current_reports(report_project):
    cfg, root, original, *_ = report_project
    assert not reporting.run(cfg, root, check=True)
    assert (root / "REPORT.md").read_bytes() == original
    reporting.run(cfg, root)
    modified = (root / "REPORT.md").stat().st_mtime_ns
    assert reporting.run(cfg, root, check=True)
    assert (root / "REPORT.md").stat().st_mtime_ns == modified


def test_missing_source_never_partially_updates_the_report(report_project):
    cfg, root, original, *_ = report_project
    (root / "outputs/exploration.md").unlink()
    with pytest.raises(reporting.ReportError, match="Missing source for block q1"):
        reporting.run(cfg, root)
    assert (root / "REPORT.md").read_bytes() == original


def test_selected_block_does_not_require_unselected_outputs(report_project):
    cfg, root, original, *_ = report_project
    (root / "outputs/exploration.md").unlink()
    reporting.run(cfg, root, selected=["preparation"])
    rendered = (root / "REPORT.md").read_bytes()
    assert b"#### Counts" in rendered
    assert (
        rendered.split(b"<!-- AUTO:q1:start -->")[1] == original.split(b"<!-- AUTO:q1:start -->")[1]
    )
    assert reporting.run(cfg, root, selected=["preparation"], check=True)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        (b"<!-- AUTO:a:start -->", "Unclosed"),
        (b"<!-- AUTO:a:end -->", "orphan"),
        (b"<!-- AUTO:a:start --><!-- AUTO:b:end -->", "Mismatched"),
        (b"<!-- AUTO:a:start --><!-- AUTO:b:start -->", "Nested"),
        (
            b"<!-- AUTO:a:start --><!-- AUTO:a:end -->" b"<!-- AUTO:a:start --><!-- AUTO:a:end -->",
            "Duplicate",
        ),
    ],
)
def test_invalid_marker_layout_is_rejected(content, message):
    with pytest.raises(reporting.ReportError, match=message):
        reporting.block_spans(content)


def test_unknown_block_and_config_marker_mismatch_are_rejected(report_project):
    cfg, root, original, *_ = report_project
    with pytest.raises(reporting.ReportError, match="Unknown selected blocks"):
        reporting.run(cfg, root, selected=["unknown"])
    wrong = cfg.with_overrides({"report.blocks.extra": {"files": ["unused"], "heading_offset": 1}})
    with pytest.raises(reporting.ReportError, match="match the report AUTO blocks"):
        reporting.run(wrong, root)
    assert (root / "REPORT.md").read_bytes() == original


def test_configured_file_order_and_heading_offsets_are_used(report_project):
    cfg, root, *_ = report_project
    cfg = cfg.with_overrides(
        {
            "report.blocks.preparation.files": ["exploration.md", "preparation.md"],
            "report.blocks.preparation.heading_offset": 1,
        }
    )
    reporting.run(cfg, root, selected=["preparation"])
    content = (root / "REPORT.md").read_bytes()
    assert content.index(b"## Q1") < content.index(b"## Counts")


def test_headings_are_nested_without_modifying_fenced_code_or_tables():
    source = (
        b"# Table\n| value |\n| --- |\n| # literal |\n"
        b"````python\n# code comment\n```\n# still code\n````\n"
        b"~~~text\n## also code\n~~~\n## Details\n"
    )
    rendered = reporting.prepare_source(source, 3)
    assert rendered.startswith(b"#### Table\n") and rendered.endswith(b"##### Details")
    assert b"| # literal |" in rendered
    assert b"# code comment\n```\n# still code" in rendered
    assert b"## also code" in rendered


@pytest.mark.parametrize("offset", [-1, 6, True, "3"])
def test_invalid_heading_offset_is_rejected(report_project, offset):
    cfg, root, original, *_ = report_project
    with pytest.raises(reporting.ReportError, match="heading_offset"):
        reporting.run(
            cfg.with_overrides({"report.blocks.preparation.heading_offset": offset}), root
        )
    assert (root / "REPORT.md").read_bytes() == original


def test_source_escape_and_embedded_markers_cannot_change_the_report(report_project):
    cfg, root, original, *_ = report_project
    (root / "private.md").write_text("Not an output.")
    escaped = cfg.with_overrides({"report.blocks.preparation.files": ["../private.md"]})
    with pytest.raises(reporting.ReportError, match="escapes"):
        reporting.run(escaped, root)
    (root / "outputs/preparation.md").write_bytes(b"<!-- AUTO:injected:start -->")
    with pytest.raises(reporting.ReportError, match="source contains AUTO markers"):
        reporting.run(cfg, root)
    assert (root / "REPORT.md").read_bytes() == original


def test_author_edit_during_rendering_is_preserved(report_project, monkeypatch):
    cfg, root, original, *_ = report_project
    prepare = reporting.prepare_source
    edited = b"Author edit\r\n" + original

    def edit_during_read(content, offset):
        (root / "REPORT.md").write_bytes(edited)
        return prepare(content, offset)

    monkeypatch.setattr(reporting, "prepare_source", edit_during_read)
    with pytest.raises(reporting.ReportError, match="changed during rendering"):
        reporting.run(cfg, root)
    assert (root / "REPORT.md").read_bytes() == edited
    assert not list(root.glob(".REPORT.md.*"))


def test_cli_exit_codes_for_stale_current_and_missing_source(report_project, monkeypatch):
    cfg, root, original, *_ = report_project
    settings = root / "settings.yaml"
    settings.write_text(yaml.safe_dump(cfg.to_dict()))
    command = ["render_report.py", "--config", str(settings), "--check"]
    monkeypatch.setattr("sys.argv", command)
    assert reporting.main(root) == 1
    assert (root / "REPORT.md").read_bytes() == original
    reporting.run(cfg, root)
    assert reporting.main(root) == 0
    (root / "outputs/exploration.md").unlink()
    with pytest.raises(SystemExit) as error:
        reporting.main(root)
    assert error.value.code == 2


def test_repository_config_matches_the_delivered_skeleton():
    root = Path(__file__).resolve().parents[1]
    cfg = load_config(root / "conf/settings.yaml")
    assert set(reporting.block_spans((root / "REPORT.md").read_bytes())) == set(cfg.report.blocks)
