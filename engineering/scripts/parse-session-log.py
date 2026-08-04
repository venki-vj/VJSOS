#!/usr/bin/env python3
"""VJSOS — Parse session logs into structured JSON.

Turns daily session markdown files (obsidian-vault/sessions/*.md)
into queryable structured data for metrics and knowledge graph updates.

Usage:
    python engineering/scripts/parse-session-log.py --date 2026-08-05
    python engineering/scripts/parse-session-log.py --dir obsidian-vault/sessions
    python engineering/scripts/parse-session-log.py --all --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Default session directory (relative to repo root)
DEFAULT_SESSIONS = Path(__file__).resolve().parents[2] / "obsidian-vault" / "sessions"


def parse_frontmatter(text: str) -> dict:
    """Extract YAML-ish frontmatter block (title/date/version/tags)."""
    frontmatter = {}
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if match:
        for line in match.group(1).splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                key = key.strip()
                value = value.strip()
                if value.startswith("[") and value.endswith("]"):
                    value = [v.strip() for v in value[1:-1].split(",") if v.strip()]
                frontmatter[key] = value
    return frontmatter


def parse_day(text: str) -> dict:
    """Extract the Day number from the title, e.g. 'VJSOS Day 2'. Returns None if absent."""
    match = re.search(r"Day\s*(\d+)", text, re.IGNORECASE)
    return int(match.group(1)) if match else None


def extract_blocks(text: str) -> dict:
    """Extract major sections by heading (## Section)."""
    blocks = {}
    lines = text.splitlines()
    current = None
    for line in lines:
        if line.startswith("## "):
            current = line[3:].strip().lower().replace(" ", "-")
            blocks[current] = []
        elif current is not None:
            blocks[current].append(line)
    return {k: "\n".join(v) for k, v in blocks.items() if "\n".join(v).strip()}


def parse_file(path: Path) -> dict:
    """Parse a single session log into structured data."""
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    blocks = extract_blocks(text)

    record = {
        "file": path.name,
        "path": str(path),
        "frontmatter": frontmatter,
        "day": parse_day(text),
        "blocks": blocks,
        "estimated_lines": len(text.splitlines()),
        "word_count": len(text.split()),
        "parsed_at": None,  # set by wrapper; removed from deterministic output
    }
    return record


def collect_sessions(directory: Path) -> list:
    """Collect all .md session files, sorted by filename."""
    return sorted(directory.glob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse VJSOS session logs into JSON.")
    parser.add_argument("--date", help="Parse a single date's session (e.g. 2026-08-05)")
    parser.add_argument("--dir", help="Directory to scan (default: obsidian-vault/sessions)")
    parser.add_argument("--all", action="store_true", help="Parse all session files")
    parser.add_argument("--json", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    if args.date:
        target = DEFAULT_SESSIONS / f"{args.date}_Day*.md"
        files = sorted(DEFAULT_SESSIONS.glob(f"{args.date}_Day*.md"))
        if not files:
            # -DayN vs _DAYN tolerance
            files = sorted(DEFAULT_SESSIONS.glob(f"{args.date}*"))
        if not files:
            print(f"No session found for date: {args.date}", file=sys.stderr)
            return 1
    else:
        directory = Path(args.dir) if args.dir else DEFAULT_SESSIONS
        files = collect_sessions(directory)
        if not files and not args.all:
            print("No session files found.", file=sys.stderr)
            return 1

    records = []
    for f in files:
        try:
            records.append(parse_file(f))
        except Exception as exc:  # skip unreadable/invalid files
            print(f"WARN: could not parse {f.name}: {exc}", file=sys.stderr)

    output = {
        "app": "VJSOS",
        "tool": "parse-session-log",
        "parsed": len(records),
        "sessions": records,
    }

    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"\n=== VJSOS Session Log Parser ===")
        print(f"Found {len(records)} session(s).\n")
        for r in records:
            day = r["day"] or "?"
            fm = r["frontmatter"]
            title = fm.get("title", "Untitled")
            date = fm.get("date", "YYYY-MM-DD")
            tags = ", ".join(fm.get("tags", [])) if isinstance(fm.get("tags"), list) else fm.get("tags", "")
            print(f"• Day {day} — {date} — {title}")
            print(f"    {r['estimated_lines']} lines, {r['word_count']} words | tags: {tags}")
            print(f"    blocks: {list(r['blocks'].keys())}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())