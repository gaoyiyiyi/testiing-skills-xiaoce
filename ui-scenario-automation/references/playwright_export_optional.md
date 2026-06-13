# Optional Playwright Export

Read this only when the user explicitly asks to export reusable UI automation code, CI-ready tests, or Playwright scripts.

## Policy

- Do not require Playwright for default browser execution.
- Export Playwright only after scenarios have been reviewed or executed in the Codex browser when possible.
- Keep generated tests readable for beginners.
- Prefer TypeScript if the target project already uses TypeScript; otherwise use JavaScript.

## Suggested Output Layout

```text
ui-automation/
├── ui-scenarios.json
├── playwright.config.ts
├── tests/
│   └── ui-scenarios.spec.ts
└── README.generated.md
```

## Generation Rules

- Preserve scenario and step names in test titles.
- Use `test.step` for readable reports.
- Use `getByRole`, `getByLabel`, `getByPlaceholder`, `getByText`, and `getByTestId` before CSS selectors.
- Add screenshots on failure if the framework configuration supports it.
- Read `BASE_URL` from the environment and fall back to `ui-scenarios.json.base_url`.
- Do not add project dependencies unless the user approves installation or the project already has Playwright.

## Example Prompt

```text
Use $ui-scenario-automation to export the validated ui-scenarios.json to Playwright tests under ui-automation.
```
