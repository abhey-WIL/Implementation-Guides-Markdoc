#!/usr/bin/env python3
"""Expand custom Markdoc-style section tags in a .mdoc file into plain Markdown.

Supported tags in the source file:

  {% remote-section src="<url-or-path>" id="<anchor-id>" %}
  {% /remote-section %}

  {% local-section file="<relative-path>" id="<anchor-id>" %}
  {% /local-section %}

- remote-section:
    * src: HTTP(S) URL or local filesystem path, interpreted relative to
      this script's directory.
    * id: anchor id from the target document's Table of Contents.

- local-section:
    * file: local markdown path, interpreted relative to the .mdoc file's
    * id: anchor id for the section root. The script first looks for a
      `<span id="...">` and, if not found, falls back to TOC-based lookup.

Usage (from the Markdoc directory):

    python build_markdoc_sections.py guides/new-guide.mdoc -o docs/new-guide.md

This script is generic: it reads src/file/id from the tags and does not
hardcode any standard-specific URLs or paths.
"""

from __future__ import annotations

import argparse
import re
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

try:
    import requests  # type: ignore
except ImportError:  # pragma: no cover
    requests = None


TAG_REMOTE_RE = re.compile(
    r"\{%\s*remote-section(?P<attrs>.*?)%\}\s*\{%\s*/remote-section\s*%\}",
    re.DOTALL,
)

TAG_LOCAL_RE = re.compile(
    r"\{%\s*local-section(?P<attrs>.*?)%\}\s*\{%\s*/local-section\s*%\}",
    re.DOTALL,
)

ATTR_RE = re.compile(r"(\w+)\s*=\s*\"([^\"]*)\"")

TOC_LINK_RE = re.compile(r"^- \[(?P<title>.+?)\]\(#(?P<id>[^)]+)\)")
HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*$")


@dataclass
class SourceCache:
    """Simple in-memory cache for text loaded from URLs or local paths."""

    text_by_src: Dict[str, str]

    def get(self, src: str, base_dir: Path) -> str:
        if src in self.text_by_src:
            return self.text_by_src[src]

        if src.startswith("http://") or src.startswith("https://"):
            if requests is None:
                raise RuntimeError(
                    "'requests' is required to fetch remote URLs; install via `pip install requests`.",
                )
            response = requests.get(src, timeout=30)
            response.raise_for_status()
            text = response.text
        else:
            path = (base_dir / src).resolve()
            text = path.read_text(encoding="utf-8")

        self.text_by_src[src] = text
        return text


def parse_attrs(block: str) -> Dict[str, str]:
    """Parse key="value" attributes from a tag block."""

    return {key: value for key, value in ATTR_RE.findall(block)}


def build_toc_map(text: str) -> Dict[str, Tuple[str, int, int]]:
    """Map anchor id -> (heading title, heading level, line index) using the doc's TOC.

    Expects a TOC with entries like:
        - [Title](#anchor-id)
    """

    lines = text.splitlines()
    id_to_title: Dict[str, str] = {}
    seen_toc = False

    for line in lines:
        match = TOC_LINK_RE.match(line.strip())
        if match:
            seen_toc = True
            title = match.group("title").strip()
            anchor_id = match.group("id").strip()
            id_to_title[anchor_id] = title
        else:
            if seen_toc and line.strip() and not line.strip().startswith("- "):
                break

    id_map: Dict[str, Tuple[str, int, int]] = {}

    for index, line in enumerate(lines):
        heading_match = HEADING_RE.match(line)
        if not heading_match:
            continue
        level = len(heading_match.group("hashes"))
        title = heading_match.group("title").strip()
        for anchor_id, toc_title in id_to_title.items():
            if title.startswith(toc_title):
                id_map[anchor_id] = (title, level, index)

    return id_map


def extract_section_by_toc(text: str, anchor_id: str) -> str:
    """Extract a section by anchor id using TOC + heading levels."""

    lines = text.splitlines()
    toc_map = build_toc_map(text)
    info = toc_map.get(anchor_id)
    if not info:
        return f"<!-- section {anchor_id} not found via TOC -->\n"

    _title, level, start_index = info

    end_index = len(lines)
    for i in range(start_index + 1, len(lines)):
        heading_match = HEADING_RE.match(lines[i])
        if heading_match and len(heading_match.group("hashes")) <= level:
            end_index = i
            break

    return "\n".join(lines[start_index:end_index]).rstrip() + "\n"


def extract_section_by_span(text: str, anchor_id: str) -> str:
    """Extract section using a <span id="..."> marker in the body."""

    lines = text.splitlines()

    span_index = None
    for i, line in enumerate(lines):
        if f'id="{anchor_id}"' in line:
            span_index = i
            break

    if span_index is None:
        return f"<!-- section {anchor_id} not found via span id -->\n"

    start_index = span_index
    current_level = 6

    for i in range(span_index, -1, -1):
        heading_match = HEADING_RE.match(lines[i])
        if heading_match:
            start_index = i
            current_level = len(heading_match.group("hashes"))
            break

    end_index = len(lines)
    for i in range(span_index + 1, len(lines)):
        heading_match = HEADING_RE.match(lines[i])
        if heading_match and len(heading_match.group("hashes")) <= current_level:
            end_index = i
            break

    return "\n".join(lines[start_index:end_index]).rstrip() + "\n"


def extract_remote_section(text: str, anchor_id: str) -> str:
    """Extract a section from a remote document (TOC-based)."""

    return extract_section_by_toc(text, anchor_id)


def extract_local_section(text: str, anchor_id: str) -> str:
    """Extract a section from a local document (span-first, then TOC)."""

    if f'id="{anchor_id}"' in text:
        return extract_section_by_span(text, anchor_id)
    return extract_section_by_toc(text, anchor_id)


def expand_remote_sections(content: str, base_dir: Path, cache: SourceCache) -> str:
    """Replace all remote-section blocks with extracted content."""

    def repl(match: re.Match) -> str:
        attrs = parse_attrs(match.group("attrs"))
        src = attrs.get("src")
        anchor_id = attrs.get("id")
        if not src or not anchor_id:
            return f"<!-- invalid remote-section attrs: {attrs} -->\n"
        try:
            text = cache.get(src, base_dir)
            return extract_remote_section(text, anchor_id)
        except Exception as exc:  # noqa: BLE001
            return textwrap.dedent(
                f"""\
                <!-- error expanding remote-section src={src!r} id={anchor_id!r}:
                {exc}
                -->
                """,
            )

    return TAG_REMOTE_RE.sub(repl, content)


def expand_local_sections(content: str, repo_root: Path, mdoc_dir: Path) -> str:
    """Replace all local-section blocks with extracted content."""

    def repl(match: re.Match) -> str:
        attrs = parse_attrs(match.group("attrs"))
        file_attr = attrs.get("file")
        anchor_id = attrs.get("id")
        if not file_attr or not anchor_id:
            return f"<!-- invalid local-section attrs: {attrs} -->\n"

        search_paths = [mdoc_dir / file_attr, repo_root / file_attr]
        last_error: Exception | None = None

        for path in search_paths:
            try:
                text = path.read_text(encoding="utf-8")
                return extract_local_section(text, anchor_id)
            except Exception as exc:  # noqa: BLE001
                last_error = exc

        return textwrap.dedent(
            f"""\
            <!-- error expanding local-section file={file_attr!r} id={anchor_id!r}:
            {last_error}
            -->
            """,
        )

    return TAG_LOCAL_RE.sub(repl, content)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Expand remote/local section tags in a .mdoc file into plain Markdown.",
    )
    parser.add_argument("input")
    parser.add_argument(
        "-o",
        "--output",
    )

    args = parser.parse_args(argv)

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    repo_root = Path(__file__).resolve().parent
    mdoc_dir = input_path.parent

    raw = input_path.read_text(encoding="utf-8")
    cache = SourceCache(text_by_src={})

    expanded = expand_remote_sections(raw, repo_root, cache)
    expanded = expand_local_sections(expanded, repo_root, mdoc_dir)

    if args.output:
        out_path = (repo_root / args.output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(expanded, encoding="utf-8")
        print(f"Wrote {out_path}")
    else:
        sys.stdout.write(expanded)


if __name__ == "__main__":  # pragma: no cover
    main()
