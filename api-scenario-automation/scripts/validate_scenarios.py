#!/usr/bin/env python3
"""Validate API scenario DSL for api-scenario-automation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}
ASSERT_TYPES = {
    "status",
    "json_path_exists",
    "json_path_not_exists",
    "json_equals",
    "json_not_equals",
    "json_contains",
    "json_length",
    "var_equals",
}
ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def add(errors: list[str], path: str, message: str) -> None:
    errors.append(f"{path}: {message}")


def load_json_compatible(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON-compatible YAML: {exc}. "
            "Write scenarios.yaml as JSON-compatible YAML or convert it to JSON."
        ) from exc


def validate_assertion(assertion: Any, path: str, errors: list[str]) -> None:
    if not isinstance(assertion, dict):
        add(errors, path, "assertion must be an object")
        return
    atype = assertion.get("type")
    if atype not in ASSERT_TYPES:
        add(errors, f"{path}.type", f"must be one of {sorted(ASSERT_TYPES)}")
        return
    if atype == "status":
        expected = assertion.get("expected")
        if not isinstance(expected, int) and not (
            isinstance(expected, list) and expected and all(isinstance(x, int) for x in expected)
        ):
            add(errors, f"{path}.expected", "status assertion expects an int or non-empty int array")
    elif atype in {"json_path_exists", "json_path_not_exists", "json_equals", "json_not_equals", "json_contains", "json_length"}:
        if not nonempty_str(assertion.get("path")):
            add(errors, f"{path}.path", "required JSON path string")
        if atype not in {"json_path_exists", "json_path_not_exists"} and "expected" not in assertion:
            add(errors, f"{path}.expected", "required")
    elif atype == "var_equals":
        if not nonempty_str(assertion.get("name")):
            add(errors, f"{path}.name", "required variable name")
        if "expected" not in assertion:
            add(errors, f"{path}.expected", "required")


def validate(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["$: root must be an object"]
    if not nonempty_str(data.get("title")):
        add(errors, "$.title", "required non-empty string")
    if "base_url" in data and not nonempty_str(data.get("base_url")):
        add(errors, "$.base_url", "must be a non-empty string when present")
    if "variables" in data and not isinstance(data["variables"], dict):
        add(errors, "$.variables", "must be an object when present")

    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        add(errors, "$.scenarios", "required non-empty array")
        return errors

    for si, scenario in enumerate(scenarios):
        sp = f"$.scenarios[{si}]"
        if not isinstance(scenario, dict):
            add(errors, sp, "scenario must be an object")
            continue
        if not nonempty_str(scenario.get("name")):
            add(errors, f"{sp}.name", "required non-empty string")
        if "variables" in scenario and not isinstance(scenario["variables"], dict):
            add(errors, f"{sp}.variables", "must be an object when present")
        steps = scenario.get("steps")
        if not isinstance(steps, list) or not steps:
            add(errors, f"{sp}.steps", "required non-empty array")
            continue
        seen_ids: set[str] = set()
        for ti, step in enumerate(steps):
            tp = f"{sp}.steps[{ti}]"
            if not isinstance(step, dict):
                add(errors, tp, "step must be an object")
                continue
            step_id = step.get("id")
            if not nonempty_str(step_id) or not ID_RE.match(step_id):
                add(errors, f"{tp}.id", "required stable id with letters, digits, underscore, or hyphen")
            elif step_id in seen_ids:
                add(errors, f"{tp}.id", "duplicate step id in scenario")
            else:
                seen_ids.add(step_id)
            if not nonempty_str(step.get("name")):
                add(errors, f"{tp}.name", "required non-empty string")
            req = step.get("request")
            if not isinstance(req, dict):
                add(errors, f"{tp}.request", "required object")
                continue
            method = req.get("method")
            if not nonempty_str(method) or method.upper() not in METHODS:
                add(errors, f"{tp}.request.method", f"must be one of {sorted(METHODS)}")
            if not nonempty_str(req.get("path")):
                add(errors, f"{tp}.request.path", "required non-empty string")
            for key in ("query", "headers"):
                if key in req and not isinstance(req[key], dict):
                    add(errors, f"{tp}.request.{key}", "must be an object when present")
            if "extract" in step:
                if not isinstance(step["extract"], dict):
                    add(errors, f"{tp}.extract", "must be an object")
                else:
                    for name, jpath in step["extract"].items():
                        if not nonempty_str(name) or not ID_RE.match(name):
                            add(errors, f"{tp}.extract.{name}", "variable name must be identifier-like")
                        if not nonempty_str(jpath):
                            add(errors, f"{tp}.extract.{name}", "JSON path must be non-empty string")
            assertions = step.get("assert", [])
            if not isinstance(assertions, list):
                add(errors, f"{tp}.assert", "must be an array when present")
            elif not any(isinstance(a, dict) and a.get("type") == "status" for a in assertions):
                add(errors, f"{tp}.assert", "include at least one status assertion")
            else:
                for ai, assertion in enumerate(assertions):
                    validate_assertion(assertion, f"{tp}.assert[{ai}]", errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate API scenario DSL.")
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        data = load_json_compatible(args.input)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    scenario_count = len(data["scenarios"])
    step_count = sum(len(s["steps"]) for s in data["scenarios"])
    print(f"OK: {scenario_count} scenario(s), {step_count} step(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
