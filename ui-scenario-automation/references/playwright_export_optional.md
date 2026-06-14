# 可选 Playwright 导出

只有当用户明确要求导出可复用 UI 自动化代码、CI 可运行测试或 Playwright 脚本时，才阅读本文件。

## 策略

- 默认浏览器执行不要求安装 Playwright。
- 尽量在 Codex 浏览器中执行或确认过场景后，再导出 Playwright。
- 生成的测试应保持可读，方便初学者理解和维护。
- 如果目标项目已经使用 TypeScript，优先导出 TypeScript；否则可以导出 JavaScript。

## 建议输出结构

```text
ui-automation/
├── ui-scenarios.json
├── playwright.config.ts
├── tests/
│   └── ui-scenarios.spec.ts
└── README.generated.md
```

## 生成规则

- 在测试标题中保留场景名和步骤名。
- 使用 `test.step` 提升报告可读性。
- 优先使用 `getByRole`、`getByLabel`、`getByPlaceholder`、`getByText` 和 `getByTestId`，再考虑 CSS 选择器。
- 如果框架配置支持，失败时保留截图。
- 从环境变量 `BASE_URL` 读取目标地址，并回退到 `ui-scenarios.json` 中的 `base_url`。
- 除非用户同意安装依赖，或项目本身已经有 Playwright，不要主动添加项目依赖。

## 示例请求

```text
使用 $ui-scenario-automation，将已验证的 ui-scenarios.json 导出为 Playwright 测试，输出到 ui-automation。
```
