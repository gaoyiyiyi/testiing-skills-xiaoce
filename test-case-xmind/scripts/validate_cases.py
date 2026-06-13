#!/usr/bin/env python3
"""Validate test-case JSON for the test-case-xmind skill."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def fail(errors: list[str], path: str, message: str) -> None:
    errors.append(f"{path}: {message}")


def validate(data: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["$: root must be an object"]

    if not is_nonempty_string(data.get("title")):
        fail(errors, "$.title", "required non-empty string")

    modules = data.get("modules")
    if not isinstance(modules, list) or not modules:
        fail(errors, "$.modules", "required non-empty array")
        return errors

    for module_index, module in enumerate(modules):
        module_path = f"$.modules[{module_index}]"
        if not isinstance(module, dict):
            fail(errors, module_path, "module must be an object")
            continue

        if not is_nonempty_string(module.get("name")):
            fail(errors, f"{module_path}.name", "required non-empty string")

        cases = module.get("cases")
        if not isinstance(cases, list) or not cases:
            fail(errors, f"{module_path}.cases", "required non-empty array")
            continue

        for case_index, case in enumerate(cases):
            case_path = f"{module_path}.cases[{case_index}]"
            if not isinstance(case, dict):
                fail(errors, case_path, "case must be an object")
                continue

            if not is_nonempty_string(case.get("title")):
                fail(errors, f"{case_path}.title", "required non-empty string")

            if not is_nonempty_string(case.get("precondition")):
                fail(errors, f"{case_path}.precondition", "required non-empty string")

            steps = case.get("steps")
            if not isinstance(steps, list) or not steps:
                fail(errors, f"{case_path}.steps", "required non-empty array")
                continue

            for step_index, step in enumerate(steps):
                step_path = f"{case_path}.steps[{step_index}]"
                if not isinstance(step, dict):
                    fail(errors, step_path, "step must be an object")
                    continue

                if not is_nonempty_string(step.get("action")):
                    fail(errors, f"{step_path}.action", "required non-empty string")

                if not is_nonempty_string(step.get("expected")):
                    fail(errors, f"{step_path}.expected", "required non-empty string")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate test-case JSON.")
    parser.add_argument("input", type=Path, help="Path to cases.json")
    args = parser.parse_args()

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: file not found: {args.input}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate(data)
    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    module_count = len(data["modules"])
    case_count = sum(len(module["cases"]) for module in data["modules"])
    step_count = sum(
        len(case["steps"])
        for module in data["modules"]
        for case in module["cases"]
    )
    print(f"OK: {module_count} module(s), {case_count} case(s), {step_count} step(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
