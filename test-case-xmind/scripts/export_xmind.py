#!/usr/bin/env python3
"""Export structured test cases to a simple XMind workbook."""

from __future__ import annotations

import argparse
import json
import time
import uuid
import zipfile
from pathlib import Path
from typing import Any

from validate_cases import validate


def topic(title: str, children: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    node: dict[str, Any] = {"id": uuid.uuid4().hex, "title": title}
    if children:
        node["children"] = {"attached": children}
    return node


def case_topic(case: dict[str, Any]) -> dict[str, Any]:
    step_children = []
    for index, step in enumerate(case["steps"], start=1):
        label = f"步骤 {index}：{step['action']}"
        expected = topic(f"预期结果：{step['expected']}")
        step_children.append(topic(label, [expected]))

    precondition = topic(f"前置条件：{case['precondition']}", step_children)
    return topic(case["title"], [precondition])


def build_workbook(data: dict[str, Any]) -> list[dict[str, Any]]:
    module_topics = []
    for module in data["modules"]:
        cases = [case_topic(case) for case in module["cases"]]
        module_topics.append(topic(module["name"], cases))

    return [
        {
            "id": uuid.uuid4().hex,
            "class": "sheet",
            "title": data["title"],
            "rootTopic": topic(data["title"], module_topics),
        }
    ]


def write_xmind(data: dict[str, Any], output: Path) -> None:
    content = build_workbook(data)
    now_ms = int(time.time() * 1000)
    metadata = {
        "creator": {"name": "test-case-xmind", "version": "1.0.0"},
        "activeSheetId": content[0]["id"],
    }
    manifest = {
        "file-entries": {
            "content.json": {},
            "metadata.json": {},
        }
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("content.json", json.dumps(content, ensure_ascii=False, indent=2))
        zf.writestr("metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2))
        zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        zf.writestr("Thumbnails/thumbnail.png", b"")
        zf.writestr(
            "comments.json",
            json.dumps({"comments": [], "created": now_ms}, ensure_ascii=False),
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Export cases.json to .xmind.")
    parser.add_argument("input", type=Path, help="Path to cases.json")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Output .xmind path")
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"error: {error}")
        return 1

    write_xmind(data, args.output)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
