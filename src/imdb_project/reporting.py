"""Insert generated Markdown tables into AUTO blocks without changing author text."""

from __future__ import annotations

import argparse
import os
import re
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path

from imdb_project.common.config import CONFIG_ENV_VAR, Config, add_config_argument, load_config

MARKER = re.compile(rb"<!--[ \t]*AUTO:([A-Za-z][A-Za-z0-9_-]*):(start|end)[ \t]*-->")
HEADING = re.compile(rb"^( {0,3})(#{1,6})([ \t]+)")
FENCE = re.compile(rb"^ {0,3}(`{3,}|~{3,})")


class ReportError(ValueError):
    """An unsafe or incomplete report configuration or marker layout."""


def block_spans(content: bytes) -> dict[str, tuple[int, int]]:
    """Locate paired, non-nested, unique AUTO blocks by byte offsets."""
    spans: dict[str, tuple[int, int]] = {}
    active: tuple[str, int] | None = None
    for marker in MARKER.finditer(content):
        name, kind = (part.decode("ascii") for part in marker.groups())
        if kind == "start":
            if active is not None:
                raise ReportError(f"Nested AUTO block: {name}")
            if name in spans:
                raise ReportError(f"Duplicate AUTO block: {name}")
            active = (name, marker.end())
        else:
            if active is None or active[0] != name:
                raise ReportError(f"Mismatched or orphan AUTO end marker: {name}")
            spans[name] = (active[1], marker.start())
            active = None
    if active is not None:
        raise ReportError(f"Unclosed AUTO block: {active[0]}")
    return spans


def prepare_source(content: bytes, heading_offset: int) -> bytes:
    """Nest generated headings while preserving fenced code and table cells."""
    content.decode("utf-8")
    if MARKER.search(content):
        raise ReportError("A generated source contains AUTO markers")
    lines = []
    active_fence: bytes | None = None
    for line in content.replace(b"\r\n", b"\n").split(b"\n"):
        fence = FENCE.match(line)
        if active_fence is not None:
            if (
                fence
                and fence[1][:1] == active_fence[:1]
                and len(fence[1]) >= len(active_fence)
                and not line[fence.end() :].strip()
            ):
                active_fence = None
        elif fence:
            active_fence = fence[1]
        else:
            heading = HEADING.match(line)
            if heading:
                line = (
                    heading[1]
                    + b"#" * min(6, len(heading[2]) + heading_offset)
                    + line[heading.end(2) :]
                )
        lines.append(line)
    return b"\n".join(lines).strip(b"\n")


def render(content: bytes, replacements: Mapping[str, bytes]) -> bytes:
    """Replace only the bytes strictly inside selected AUTO marker pairs."""
    spans = block_spans(content)
    unknown = set(replacements) - set(spans)
    if unknown:
        raise ReportError(f"Missing AUTO blocks: {', '.join(sorted(unknown))}")
    pieces = []
    previous = 0
    for name, (start, end) in sorted(spans.items(), key=lambda item: item[1][0]):
        if name in replacements:
            pieces.extend([content[previous:start], replacements[name]])
            previous = end
    pieces.append(content[previous:])
    return b"".join(pieces)


def inside(root: Path, path: str, description: str) -> Path:
    """Resolve a configured path and reject paths escaping its declared root."""
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ReportError(f"{description} escapes {root}: {path}")
    return resolved


def run(
    cfg: Config,
    project_root: Path,
    *,
    selected: Sequence[str] | None = None,
    check: bool = False,
) -> bool:
    """Render selected blocks atomically, or check freshness without writing.

    Returns:
        Whether the report was already up to date before this call.
    """
    root = project_root.resolve()
    report = inside(root, str(cfg.require("report.path")), "Report path")
    original = report.read_bytes()
    spans = block_spans(original)
    blocks = cfg.require("report.blocks")
    if not isinstance(blocks, Mapping) or not blocks:
        raise ReportError("report.blocks must be a non-empty mapping")
    if set(blocks) != set(spans):
        raise ReportError("Configured block names must match the report AUTO blocks exactly")
    names = list(blocks) if selected is None else list(dict.fromkeys(selected))
    unknown = set(names) - set(blocks)
    if unknown:
        raise ReportError(f"Unknown selected blocks: {', '.join(sorted(unknown))}")
    outputs = (root / str(cfg.require("paths.outputs"))).resolve()
    newline = b"\r\n" if b"\r\n" in original else b"\n"
    replacements = {}
    for name in names:
        settings = blocks[name]
        if not isinstance(settings, Mapping):
            raise ReportError(f"Block {name} must define files and heading_offset")
        files = settings.get("files")
        offset = settings.get("heading_offset")
        if not isinstance(files, list) or not files or not all(isinstance(p, str) for p in files):
            raise ReportError(f"Block {name}: files must be a non-empty list of paths")
        if type(offset) is not int or not 0 <= offset <= 5:
            raise ReportError(f"Block {name}: heading_offset must be an integer from 0 to 5")
        sources = []
        for filename in files:
            path = inside(outputs, filename, f"Source for {name}")
            if not path.is_file():
                raise ReportError(f"Missing source for block {name}: {path}")
            sources.append(prepare_source(path.read_bytes(), offset))
        body = b"\n\n" + b"\n\n".join(sources) + b"\n\n"
        replacements[name] = body.replace(b"\n", newline)
    updated = render(original, replacements)
    current = updated == original
    if check or current:
        return current
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=report.parent, prefix=f".{report.name}.", delete=False
        ) as f:
            temporary = Path(f.name)
            f.write(updated)
        os.chmod(temporary, report.stat().st_mode)
        if report.read_bytes() != original:
            raise ReportError("The report changed during rendering; no update was written")
        os.replace(temporary, report)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return False


def main(project_root: Path | None = None) -> int:
    """CLI: exit 0 on success, 1 for a stale check, and 2 for invalid inputs."""
    parser = add_config_argument(argparse.ArgumentParser(description=__doc__))
    parser.add_argument("--check", action="store_true", help="Check freshness without writing.")
    parser.add_argument(
        "--block", action="append", help="Render/check one block; repeat to select several."
    )
    args = parser.parse_args()
    root = Path.cwd() if project_root is None else project_root
    config_path = args.config or os.environ.get(CONFIG_ENV_VAR) or root / "conf/settings.yaml"
    try:
        current = run(load_config(config_path), root, selected=args.block, check=args.check)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"Report error: {exc}\n")
    if args.check:
        print("Report is up to date." if current else "Report is out of date.")
        return 0 if current else 1
    print("Report is already up to date." if current else "Report updated.")
    return 0
