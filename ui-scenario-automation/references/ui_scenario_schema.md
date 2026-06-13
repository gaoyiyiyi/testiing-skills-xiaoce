# UI Scenario Schema

Write `ui-scenarios.json` as a JSON document. JSON keeps the format dependency-free and easy for beginners to inspect.

## Root Object

Required:

- `title`: string.
- `base_url`: string. Can be a local URL such as `http://127.0.0.1:4273`.
- `scenarios`: non-empty array of scenario objects.

Optional:

- `source_cases`: path to source `cases.json`.
- `variables`: object of global values, such as test username or generated names.
- `output_dir`: default `ui-check-report`.

## Scenario Object

Required:

- `name`: string.
- `steps`: non-empty array of step objects.

Optional:

- `source_case`: source case title or ID.
- `description`: string.
- `preconditions`: array of strings.
- `priority`: `P0`, `P1`, `P2`, or `P3`.
- `variables`: object merged over root variables.

## Step Object

Required:

- `id`: stable identifier, letters/digits/underscore/hyphen only.
- `name`: human-readable step name.
- `action`: one of `goto`, `click`, `fill`, `select`, `check`, `uncheck`, `press`, `wait_for`, `assert`, `screenshot`, `scroll`.

Action fields:

- `goto.path`: path appended to `base_url`, for example `/login`.
- `target`: object describing the element to act on.
- `value`: string/number/boolean for fill, select, press, or variable assertions.
- `assertions`: array of assertion objects.
- `screenshot`: optional file name hint for evidence.

## Target Object

Prefer stable, user-facing locators:

```json
{"role": "button", "name": "提交答案"}
{"label": "用户名"}
{"placeholder": "请输入手机号"}
{"text": "小测晓测点评"}
{"test_id": "submit-answer"}
{"css": ".submit-button"}
```

Locator priority:

1. `role` + `name`
2. `label`
3. `placeholder`
4. `text`
5. `test_id`
6. `css`

Avoid XPath unless there is no practical alternative.

## Assertions

Supported assertion types:

```json
{"type": "text_visible", "text": "提交成功"}
{"type": "text_not_visible", "text": "加载中"}
{"type": "url_contains", "expected": "/result"}
{"type": "element_visible", "target": {"role": "button", "name": "提交"}}
{"type": "element_hidden", "target": {"text": "错误提示"}}
{"type": "element_enabled", "target": {"role": "button", "name": "下一题"}}
{"type": "element_disabled", "target": {"role": "button", "name": "提交"}}
{"type": "input_value", "target": {"label": "用户名"}, "expected": "demo"}
{"type": "count", "target": {"css": ".question-card"}, "expected": 5}
```

## Minimal Example

```json
{
  "title": "AI Interviewer Lite UI scenarios",
  "base_url": "http://127.0.0.1:4273",
  "source_cases": "test-cases/cases.json",
  "scenarios": [
    {
      "name": "提交答案后展示点评",
      "priority": "P0",
      "steps": [
        {
          "id": "open_home",
          "name": "打开首页",
          "action": "goto",
          "path": "/",
          "assertions": [
            {"type": "text_visible", "text": "小测晓测"}
          ],
          "screenshot": "01-home.png"
        },
        {
          "id": "choose_demo_answer",
          "name": "一键选择正确答案",
          "action": "click",
          "target": {"text": "一键选正确答案"}
        },
        {
          "id": "submit_answer",
          "name": "提交答案",
          "action": "click",
          "target": {"role": "button", "name": "提交答案"}
        },
        {
          "id": "assert_feedback",
          "name": "校验点评展示",
          "action": "assert",
          "assertions": [
            {"type": "text_visible", "text": "小测晓测点评"}
          ],
          "screenshot": "02-result.png"
        }
      ]
    }
  ]
}
```
