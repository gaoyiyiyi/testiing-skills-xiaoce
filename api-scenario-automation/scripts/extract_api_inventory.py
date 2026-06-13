#!/usr/bin/env python3
"""Extract a lightweight endpoint inventory from Markdown interface docs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HTTP_RE = re.compile(r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/[^\s`]+)", re.IGNORECASE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def extract(markdown: str) -> dict:
    endpoints = []
    heading_stack: list[tuple[int, str]] = []
    for line_no, line in enumerate(markdown.splitlines(), start=1):
        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2)
            heading_stack = [item for item in heading_stack if item[0] < level]
            heading_stack.append((level, title))
        for match in HTTP_RE.finditer(line):
            endpoints.append(
                {
                    "method": match.group(1).upper(),
                    "path": match.group(2),
                    "section": " > ".join(title for _, title in heading_stack),
                    "line": line_no,
                }
            )
    return {"endpoints": endpoints}


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract endpoints from Markdown.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", "-o", type=Path)
    args = parser.parse_args()
    inventory = extract(args.input.read_text(encoding="utf-8"))
    text = json.dumps(inventory, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
