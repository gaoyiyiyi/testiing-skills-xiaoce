# testiing-skills-xiaoce

这是一个用于 Codex 的软件测试技能仓库，面向测试学习者、测试工程师和测试开发练习场景。

当前包含：

- `test-case-xmind`：根据需求文档、前端技术文档、后端技术文档、交互稿、接口文档等资料生成结构化测试用例，并导出 `.xmind` 文件。
- `api-scenario-automation`：根据接口文档、测试用例、OpenAPI/Swagger/Postman/Apipost 导出、后端路由或 Markdown 接口说明，生成场景式 API 自动化测试。
- `ui-scenario-automation`：根据测试用例、需求文档、UI 稿、截图或本地页面，使用 Codex 内置浏览器执行 UI 场景验证，并输出报告和截图。

## 安装

将 skill 目录复制到本机 Codex skills 目录：

```bash
cp -R test-case-xmind ~/.codex/skills/
cp -R api-scenario-automation ~/.codex/skills/
cp -R ui-scenario-automation ~/.codex/skills/
```

重启或刷新 Codex 后，即可通过 `$test-case-xmind`、`$api-scenario-automation` 和 `$ui-scenario-automation` 使用。

## 使用方式

向 Codex 提供一个或多个项目文档，然后发起请求，例如：

```text
使用 $test-case-xmind，根据这些需求文档、前端技术文档、后端技术文档和交互稿生成测试用例，并导出 xmind 文件。
```

Codex 会执行：

1. 阅读输入文档。
2. 生成结构化 `cases.json`。
3. 校验用例格式。
4. 导出 `.xmind` 文件。
5. 结束操作。

生成接口自动化时，可以提供接口文档、后端代码、OpenAPI/Swagger/Postman/Apipost 导出或已有测试用例，然后发起请求，例如：

```text
使用 $api-scenario-automation，根据 docs/接口文档.md 和 test-cases/cases.json 生成 5 个核心业务流 API 自动化场景，base_url 是 http://127.0.0.1:8080，输出到 api-automation。
```

Codex 会执行：

1. 阅读接口资料和测试用例。
2. 生成 `scenarios.yaml` 场景文件。
3. 校验场景文件格式。
4. 导出 `unittest`/`pytest` 兼容的 API 自动化测试。
5. 在目标服务可运行时执行测试并反馈结果。

生成 UI 自动化验证时，可以提供 `cases.json`、需求文档、UI 稿、页面截图或本地页面地址，然后发起请求，例如：

```text
使用 $ui-scenario-automation，根据 test-cases/cases.json 和当前页面 http://127.0.0.1:4273 生成 UI 场景，并用 Codex 浏览器执行验证，输出报告和截图。
```

Codex 会执行：

1. 从测试用例、文档或页面中识别适合 UI 执行的用户路径。
2. 生成 `ui-scenarios.json` 场景文件。
3. 使用 Codex 内置浏览器点击、输入、导航和检查页面结果。
4. 记录通过、失败、阻塞项，并保存关键截图。
5. 只有在用户明确要求时，才进一步导出 Playwright 自动化脚本。

## 用例模板

XMind 脑图采用以下结构：

```text
模块
└── 用例标题
    └── 前置条件：...
        ├── 步骤 1：...
        │   └── 预期结果：...
        ├── 步骤 2：...
        │   └── 预期结果：...
```

模板只展示：

- 用例标题
- 前置条件
- 步骤
- 预期结果

不会在 XMind 中展示来源参考、用例属性、备注或 HTML 预览。

## 目录结构

```text
test-case-xmind/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── case_schema.md
│   ├── coverage_rules.md
│   └── demo_flow.md
└── scripts/
    ├── export_xmind.py
    └── validate_cases.py

api-scenario-automation/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── pytest_export.md
│   └── scenario_schema.md
└── scripts/
    ├── export_pytest.py
    ├── extract_api_inventory.py
    └── validate_scenarios.py

ui-scenario-automation/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── assertion_rules.md
    ├── browser_execution.md
    ├── playwright_export_optional.md
    └── ui_scenario_schema.md
```

## 脚本说明

脚本是给 Codex 自动调用的稳定工具。用户通常不需要手动运行。

维护或调试时可以运行：

```bash
python3 test-case-xmind/scripts/validate_cases.py cases.json
python3 test-case-xmind/scripts/export_xmind.py cases.json --output test-cases.xmind
python3 api-scenario-automation/scripts/extract_api_inventory.py docs/接口文档.md --output api-inventory.json
python3 api-scenario-automation/scripts/validate_scenarios.py scenarios.yaml
python3 api-scenario-automation/scripts/export_pytest.py scenarios.yaml --output api-automation
```

脚本只使用 Python 标准库，不需要额外安装依赖。生成的 API 自动化测试也只使用 Python 标准库，可通过 `python3 -m unittest` 运行；如果项目安装了 pytest，也可以被 pytest 收集执行。

`ui-scenario-automation` 默认不要求用户安装 Playwright。它优先使用 Codex 内置浏览器执行 UI 场景；只有在用户需要长期沉淀、CI 回归或团队协作脚本时，才建议导出 Playwright。
