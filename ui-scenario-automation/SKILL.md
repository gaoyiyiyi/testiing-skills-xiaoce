---
name: ui-scenario-automation
description: 根据需求文档、UI 文档、截图、前端文档、已有测试用例（如 cases.json）或可访问的本地页面生成并执行浏览器 UI 场景验证。适用于驱动 Codex 内置浏览器进行点击、输入、导航、检查页面状态、截图取证、验证用户流程、生成 UI 检查报告、创建 ui-scenarios.json；也可在用户明确要求时导出 Playwright 测试。
---

# UI 场景自动化

使用本 skill 将产品资料或已有测试用例转换成可执行的 UI 场景，并通过 Codex 内置浏览器执行。默认使用 Codex 浏览器完成交互验证；除非用户明确要求可复用脚本、CI 测试或 Playwright 导出，否则不要强制要求安装 Playwright。

## 工作流程

1. 收集输入：
   - 目标 URL 或本地应用启动命令。
   - 可选的 `cases.json`，例如由 `test-case-xmind` 生成的测试用例。
   - 需求文档、UI 稿、截图、前端文档、路由说明，或用户提供的流程描述。
   - 测试账号、预置数据、权限信息，以及需要用户确认的操作。
2. 如果存在 `cases.json`，优先从中选择 UI 场景；否则从文档和当前页面推断场景。
3. 编写 `ui-scenarios.json` 前，阅读 `references/ui_scenario_schema.md`。
4. 执行场景前，阅读 `references/browser_execution.md`。
5. 选择断言和通过/失败标准时，阅读 `references/assertion_rules.md`。
6. 生成 `ui-scenarios.json`。默认生成 3-8 条有价值的用户流程，除非用户要求更窄范围。
7. 目标应用可访问时，使用 Codex 内置浏览器执行场景。
8. 为关键状态、失败点和最终结果截图取证。
9. 输出简洁报告，包含通过项、失败项、截图、缺陷和阻塞项。
10. 只有在用户明确要求时，才阅读 `references/playwright_export_optional.md` 并导出 Playwright 测试。

## 场景选择规则

- 优先选择用户可见的业务路径，而不是孤立点击检查。
- 至少包含一条正向路径，并覆盖重要的反向或校验路径。
- 未经用户明确确认，不要自动执行破坏性操作或会产生外部副作用的操作。
- 未经用户明确提供，不要输入敏感数据。
- 保持检查确定性。避免真实支付、真实邮件、真实生产数据变更或不可逆操作。
- 如果某条用例更适合接口层验证，应交给 `api-scenario-automation`，不要强行通过 UI 执行。

## 与其他 skill 的关系

当用户希望从产品资料生成测试用例时，可以先使用 `test-case-xmind`，再消费其输出的 `cases.json` 作为 UI 场景来源。

后端状态流转、数据组合、权限矩阵或 UI 执行收益较低的流程，更适合交给 `api-scenario-automation`。

本 skill 关注用户可见路径：页面导航、输入、可见状态、校验文案、禁用/启用状态、弹窗、最终页面证据。

## 输出结构

默认输出目录：

```text
ui-check-report/
├── report.md
├── ui-scenarios.json
└── screenshots/
    ├── 01-home.png
    └── 02-result.png
```

`ui-scenarios.json` 是场景源文件；`report.md` 是执行证据，不是场景定义。

## 浏览器要求

优先使用 Codex 内置浏览器。若当前环境无法使用浏览器执行，应说明交互式浏览器执行受阻，并仍然交付 `ui-scenarios.json`，同时给出手动执行或导出 Playwright 的后续方案。
