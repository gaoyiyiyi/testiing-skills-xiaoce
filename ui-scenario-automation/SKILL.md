---
name: ui-scenario-automation
description: Generate and execute browser-based UI scenario checks from requirements, UI docs, screenshots, frontend docs, existing test cases such as cases.json, or a live local page. Use when Codex needs to drive the Codex in-app browser to click, type, navigate, inspect visible UI state, take screenshots, verify user flows, produce UI check reports, create ui-scenarios.json, or optionally export Playwright tests after scenarios are validated.
---

# UI Scenario Automation

Use this skill to turn product materials or existing test cases into executable UI scenarios, then run those scenarios in the Codex in-app browser. Default to browser execution inside Codex. Do not require Playwright unless the user explicitly asks for reusable code, CI-ready tests, or Playwright export.

## Workflow

1. Collect inputs:
   - Target URL or local app start command.
   - Optional `cases.json` from `test-case-xmind`.
   - Requirements, UI drafts, screenshots, frontend docs, routes, or user-provided flow descriptions.
   - Test accounts, seeded data, permissions, and actions that need confirmation.
2. If `cases.json` exists, prioritize it as the source of UI scenarios. Otherwise infer scenarios from docs and the live page.
3. Read `references/ui_scenario_schema.md` before writing `ui-scenarios.json`.
4. Read `references/browser_execution.md` before running scenarios in the Codex browser.
5. Read `references/assertion_rules.md` when choosing assertions and pass/fail criteria.
6. Generate `ui-scenarios.json` with 3-8 valuable user flows unless the user asks for a narrower set.
7. Execute scenarios with the Codex in-app browser when the app is reachable.
8. Capture screenshots for important states, failures, and final evidence.
9. Deliver a concise report with passed checks, failed checks, screenshots, defects, and blocked items.
10. Only if requested, read `references/playwright_export_optional.md` and export Playwright tests.

## Scenario Selection Rules

- Prefer user-visible business flows over isolated click checks.
- Include at least one happy path and important negative or validation paths.
- Do not automate destructive or external side-effect actions without explicit user approval.
- Do not enter sensitive data unless the user explicitly supplied it for this target.
- Keep checks deterministic. Avoid real payments, real emails, real production mutations, or irreversible actions.
- If a case is better suited to API checks, hand it to `api-scenario-automation` instead of forcing it through the UI.

## Relationship To Other Skills

Use `test-case-xmind` before this skill when the user wants to derive test cases from product documents. Consume its `cases.json` as the UI case pool.

Use `api-scenario-automation` for backend-heavy checks, data combinations, permission matrices, or workflows where UI execution adds little value.

This skill handles the user-facing path: page navigation, input, visible states, validation messages, disabled/enabled controls, modals, and final UI evidence.

## Output Layout

Default output directory:

```text
ui-check-report/
├── report.md
├── ui-scenarios.json
└── screenshots/
    ├── 01-home.png
    └── 02-result.png
```

`ui-scenarios.json` is the scenario source of truth. The report is execution evidence, not the source definition.

## Browser Requirement

Use the Codex in-app browser when available. If Browser is not available, state that interactive browser execution is blocked and still deliver `ui-scenarios.json` plus instructions for manual or Playwright execution.
