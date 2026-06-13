---
name: api-scenario-automation
description: Generate scenario-based API automation from requirements, test cases, OpenAPI/Postman/Apipost/Swagger/Markdown interface docs, backend docs, or source routes. Use when Codex needs to create API workflow orchestration, scenarios.yaml/scenarios.json DSL files, unittest/pytest-compatible API automation, or data-dependent end-to-end API tests rather than unit tests.
---

# API Scenario Automation

Use this skill to turn interface assets and test cases into scenario-based API automation. The goal is not single-endpoint smoke tests; the goal is executable business flows with request ordering, variable extraction, cross-step data dependencies, business assertions, and clean failure reporting.

## Workflow

1. Collect source materials:
   - Interface docs: OpenAPI, Swagger, Postman collection, Apipost export, Markdown docs, backend route files.
   - Optional upstream test cases, such as `cases.json` from `test-case-xmind`.
   - Environment details: `base_url`, test accounts, auth style, required seed data, and cleanup expectations.
2. Read `references/scenario_schema.md` before writing scenario DSL.
3. Read `references/pytest_export.md` before exporting pytest.
4. If interface docs are Markdown, optionally run `scripts/extract_api_inventory.py` to create a quick endpoint inventory.
5. Generate `scenarios.yaml`. Keep it valid JSON-compatible YAML unless the user explicitly wants another format.
6. Run `scripts/validate_scenarios.py scenarios.yaml` and fix all errors.
7. Run `scripts/export_pytest.py scenarios.yaml --output <project>/api-automation`.
8. If the target app can run locally, start it and run the generated pytest suite. If it cannot run, still deliver the generated files and state what was not executed.

## Scenario Design Rules

- Prefer 3-8 valuable business scenarios over many shallow endpoint checks.
- Chain data between steps with `extract` and `{{ variable }}` templates.
- Assert both transport behavior and business behavior:
  - HTTP status.
  - Response fields.
  - Created resource can be queried.
  - Counts, balances, ownership, or state transitions changed as expected.
  - Forbidden paths fail for the right reason.
- Include negative paths where they matter: missing required fields, invalid IDs, wrong auth, expired state, duplicate submit, service errors if injectable.
- Keep generated tests deterministic. Avoid real payments, real emails, real AI calls, or irreversible production actions.
- If cleanup is not available, generate unique test data names and avoid depending on persistent global state.

## Output Layout

Default output directory:

```text
api-automation/
├── scenarios.yaml
├── tests/
│   └── test_api_scenarios.py
└── README.generated.md
```

The `.yaml` file is the source of truth. The generated test file embeds the scenario definitions so it can run without extra parsing dependencies. It is `unittest`-based and pytest-compatible.

## Scripts

Run from any working directory:

```bash
python3 <skill>/scripts/extract_api_inventory.py docs/05-接口文档.md --output api-inventory.json
python3 <skill>/scripts/validate_scenarios.py scenarios.yaml
python3 <skill>/scripts/export_pytest.py scenarios.yaml --output api-automation
```

The scripts use Python standard library only. The generated tests also use Python standard library only. They can run with `python3 -m unittest` and can be collected by pytest if pytest is available.
