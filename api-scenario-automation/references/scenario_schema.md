# Scenario DSL Schema

Write `scenarios.yaml` as JSON-compatible YAML: a JSON document saved with `.yaml` is valid. This keeps the skill dependency-free while remaining easy to transform later.

## Root Object

Required:

- `title`: string.
- `scenarios`: non-empty array of scenario objects.

Optional:

- `base_url`: string. Can be overridden at runtime by `API_BASE_URL`.
- `variables`: object of global variables.

## Scenario Object

Required:

- `name`: string.
- `steps`: non-empty array of step objects.

Optional:

- `description`: string.
- `variables`: object merged over root variables.

## Step Object

Required:

- `id`: stable identifier, letters/digits/underscore/hyphen only.
- `name`: human-readable step name.
- `request`: object with:
  - `method`: GET, POST, PUT, PATCH, DELETE.
  - `path`: string. Supports `{{ variable }}` templates.

Optional:

- `request.query`: object. Query parameters.
- `request.headers`: object. Request headers.
- `request.body`: object, array, string, number, boolean, or null.
- `extract`: object mapping variable names to JSON paths, for example `"question_id": "$.data.id"`.
- `assert`: array of assertion objects.

## Supported Assertions

Use at least one status assertion for every request.

```json
{"type": "status", "expected": 200}
{"type": "json_path_exists", "path": "$.data.id"}
{"type": "json_path_not_exists", "path": "$.data.explanation"}
{"type": "json_equals", "path": "$.data.correct", "expected": true}
{"type": "json_not_equals", "path": "$.data.id", "expected": null}
{"type": "json_contains", "path": "$.message", "expected": "请选择"}
{"type": "json_length", "path": "$.data.options", "expected": 3}
{"type": "var_equals", "name": "question_id", "expected": "q_api_failures"}
```

## JSON Path Subset

Scripts support a small, deterministic subset:

- Root starts with `$`.
- Dot access: `$.data.id`.
- Array index: `$.data.options[0]`.

Do not use filters, wildcards, recursive descent, or complex expressions.

## Templates

Any string field can reference variables:

```json
"path": "/api/items/{{ item_id }}"
```

Variable values come from:

1. root `variables`
2. scenario `variables`
3. prior step `extract`

## Minimal Example

```json
{
  "title": "AI Interviewer Lite API scenarios",
  "base_url": "http://127.0.0.1:4273",
  "scenarios": [
    {
      "name": "抽题并提交正确答案",
      "steps": [
        {
          "id": "next_question",
          "name": "抽下一题",
          "request": {"method": "POST", "path": "/api/quiz/next"},
          "assert": [
            {"type": "status", "expected": 200},
            {"type": "json_path_exists", "path": "$.data.id"}
          ],
          "extract": {
            "question_id": "$.data.id",
            "demo_option": "$.data.demoOption"
          }
        },
        {
          "id": "answer_question",
          "name": "提交正确答案",
          "request": {
            "method": "POST",
            "path": "/api/quiz/answer",
            "body": {
              "questionId": "{{ question_id }}",
              "selectedOption": "{{ demo_option }}"
            }
          },
          "assert": [
            {"type": "status", "expected": 200},
            {"type": "json_equals", "path": "$.data.correct", "expected": true}
          ]
        }
      ]
    }
  ]
}
```
