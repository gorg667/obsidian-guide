#!/usr/bin/env python3
"""Concatenate all chapter files listed in mkdocs.yml nav into a single GUIDE.md.

- Reads nav order from mkdocs.yml (recursively), skipping index.md and GUIDE-only pages.
- Demotes nothing: each chapter already starts with a single H1, so the combined
  document is a sequence of H1 chapters. A generated table of contents is prepended.
- Rewrites relative links between chapter files (e.g. `03-links.md#anchor`) to
  in-document anchors so the single file remains navigable.
- Strips MkDocs-only syntax that plain Markdown renderers choke on is NOT done on
  purpose: GitHub renders admonitions as blockquote-ish text, which is acceptable.

Usage: python scripts/build_guide.py   (run from repo root)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "GUIDE.md"
SKIP = {"index.md", "GUIDE.md", "changelog.md"}


def flatten_nav(nav) -> list[str]:
    files: list[str] = []
    if isinstance(nav, list):
        for item in nav:
            files.extend(flatten_nav(item))
    elif isinstance(nav, dict):
        for _title, value in nav.items():
            files.extend(flatten_nav(value))
    elif isinstance(nav, str):
        files.append(nav)
    return files


def slugify(text: str) -> str:
    text = re.sub(r"[`*_~]", "", text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s]+", "-", text)


def first_h1(md: str, fallback: str) -> str:
    m = re.search(r"^# (.+)$", md, re.M)
    return m.group(1).strip() if m else fallback


def rewrite_links(md: str, known: set[str]) -> str:
    """Turn `[x](07-foo.md#bar)` into `[x](#bar)` and `[x](07-foo.md)` into `[x](#<h1 slug>)`."""
    def repl(m: re.Match) -> str:
        text, target = m.group(1), m.group(2)
        path, _, anchor = target.partition("#")
        path = path.split("/")[-1]
        if path in known:
            if anchor:
                return f"[{text}](#{anchor})"
            return f"[{text}](#{known_slugs[path]})"
        return m.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+\.md(?:#[^)\s]*)?)\)", repl, md)


known_slugs: dict[str, str] = {}


def main() -> int:
    # mkdocs.yml contains python-specific tags; use a loader that ignores them.
    class Loader(yaml.SafeLoader):
        pass

    Loader.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, suffix, node: None)
    Loader.add_constructor("!ENV", lambda loader, node: None)

    cfg = yaml.load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"), Loader=Loader)
    files = [f for f in flatten_nav(cfg.get("nav", [])) if f.endswith(".md") and f not in SKIP]

    chapters: list[tuple[str, str, str]] = []  # (filename, title, body)
    for f in files:
        p = DOCS / f
        if not p.exists():
            print(f"warning: {f} listed in nav but missing", file=sys.stderr)
            continue
        body = p.read_text(encoding="utf-8")
        title = first_h1(body, p.stem)
        known_slugs[p.name] = slugify(title)
        chapters.append((p.name, title, body))

    known = set(known_slugs)
    parts = [
        "# The Complete Obsidian Mastery Guide\n",
        "> Single-file edition. Generated automatically from the chapter files in `docs/` "
        "by `scripts/build_guide.py`. The web edition lives at "
        "<https://gorg667.github.io/obsidian-guide/>.\n",
        "## Table of contents\n",
    ]
    for i, (_f, title, _b) in enumerate(chapters, 1):
        parts.append(f"{i}. [{title}](#{slugify(title)})")
    parts.append("\n---\n")

    for _f, _title, body in chapters:
        parts.append(rewrite_links(body, known).rstrip() + "\n\n---\n")

    OUT.write_text("\n".join(parts), encoding="utf-8")
    words = len(OUT.read_text(encoding="utf-8").split())
    print(f"wrote {OUT.relative_to(ROOT)} with {len(chapters)} chapters, ~{words:,} words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
