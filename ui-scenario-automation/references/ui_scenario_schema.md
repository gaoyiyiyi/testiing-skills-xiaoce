# UI 场景结构说明

`ui-scenarios.json` 使用 JSON 编写。JSON 便于初学者查看，也不需要额外格式解析依赖。

## 根对象

必填字段：

- `title`：字符串，表示这组 UI 场景的标题。
- `base_url`：字符串，可以是本地地址，例如 `http://127.0.0.1:8080`。
- `scenarios`：非空数组，包含一个或多个场景对象。

可选字段：

- `source_cases`：来源 `cases.json` 路径。
- `variables`：对象，存放全局变量，例如测试用户名或生成名称。
- `output_dir`：输出目录，默认 `ui-check-report`。

## 场景对象

必填字段：

- `name`：字符串，场景名称。
- `steps`：非空数组，包含一个或多个步骤对象。

可选字段：

- `source_case`：来源用例标题或 ID。
- `description`：字符串，场景说明。
- `preconditions`：字符串数组，前置条件。
- `priority`：`P0`、`P1`、`P2` 或 `P3`。
- `variables`：对象，场景级变量，会合并到根对象变量中。

## 步骤对象

必填字段：

- `id`：稳定标识，只允许字母、数字、下划线和连字符。
- `name`：可读的步骤名称。
- `action`：动作类型，可选值为 `goto`、`click`、`fill`、`select`、`check`、`uncheck`、`press`、`wait_for`、`assert`、`screenshot`、`scroll`。

动作相关字段：

- `goto.path`：追加到 `base_url` 后的路径，例如 `/login`。
- `target`：描述要操作或检查的元素。
- `value`：用于输入、选择、按键或变量断言的值。
- `assertions`：断言对象数组。
- `screenshot`：可选截图文件名。

## 目标元素对象

优先使用稳定、面向用户的定位方式：

```json
{"role": "button", "name": "提交"}
{"label": "用户名"}
{"placeholder": "请输入手机号"}
{"text": "提交成功"}
{"test_id": "submit-button"}
{"css": ".submit-button"}
```

定位方式优先级：

1. `role` + `name`
2. `label`
3. `placeholder`
4. `text`
5. `test_id`
6. `css`

除非没有其他实用方式，否则避免使用 XPath。

## 断言

支持的断言类型：

```json
{"type": "text_visible", "text": "提交成功"}
{"type": "text_not_visible", "text": "加载中"}
{"type": "url_contains", "expected": "/result"}
{"type": "element_visible", "target": {"role": "button", "name": "提交"}}
{"type": "element_hidden", "target": {"text": "错误提示"}}
{"type": "element_enabled", "target": {"role": "button", "name": "下一步"}}
{"type": "element_disabled", "target": {"role": "button", "name": "提交"}}
{"type": "input_value", "target": {"label": "用户名"}, "expected": "test_user"}
{"type": "count", "target": {"css": ".result-item"}, "expected": 5}
```

## 最小示例

```json
{
  "title": "登录功能 UI 场景",
  "base_url": "http://127.0.0.1:8080",
  "source_cases": "test-cases/cases.json",
  "scenarios": [
    {
      "name": "使用有效账号登录成功",
      "priority": "P0",
      "steps": [
        {
          "id": "open_login",
          "name": "打开登录页",
          "action": "goto",
          "path": "/login",
          "assertions": [
            {"type": "text_visible", "text": "登录"}
          ],
          "screenshot": "01-login.png"
        },
        {
          "id": "fill_username",
          "name": "输入用户名",
          "action": "fill",
          "target": {"label": "用户名"},
          "value": "test_user"
        },
        {
          "id": "fill_password",
          "name": "输入密码",
          "action": "fill",
          "target": {"label": "密码"},
          "value": "test_password"
        },
        {
          "id": "submit_login",
          "name": "提交登录表单",
          "action": "click",
          "target": {"role": "button", "name": "登录"}
        },
        {
          "id": "assert_login_success",
          "name": "校验登录成功",
          "action": "assert",
          "assertions": [
            {"type": "text_visible", "text": "欢迎"}
          ],
          "screenshot": "02-home.png"
        }
      ]
    }
  ]
}
```
