# Pytest Export Guidance

The exporter creates a self-contained `tests/test_api_scenarios.py` file with:

- embedded scenario definitions
- a tiny JSON path reader
- `{{ variable }}` template rendering
- ordered step execution
- standard-library HTTP calls
- `unittest` dynamic test methods, which pytest can also collect

## Runtime Environment

Generated tests read:

- `API_BASE_URL`: overrides root `base_url`.
- `API_TIMEOUT`: request timeout in seconds, default `10`.

Example:

```bash
API_BASE_URL=http://127.0.0.1:4273 python3 -m unittest discover api-automation/tests
```

## Dependency Policy

The generated test suite uses Python standard library only. It can be run with `python3 -m unittest` or collected by pytest if pytest is available. Do not add project-specific dependencies unless the user asks.

## Assertion Strategy

For each step, assert:

1. status code
2. required response fields
3. cross-step business outcome when possible

When docs do not define exact error status codes, prefer assertions that match observable contract from the docs. For example, if docs show an error JSON with `message`, assert status is one of `[400, 422]` only when implementation is unknown; if the actual app is available, inspect and pin the observed status.

## Data Strategy

For apps with persistence:

- generate unique names with a timestamp or UUID variable
- create data through public APIs
- clean up through public APIs when supported
- avoid direct database writes unless the user explicitly asks

For stateless demo apps:

- keep scenarios independent
- avoid assumptions about order unless the API contract states it
