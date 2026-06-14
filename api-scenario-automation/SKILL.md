---
name: api-scenario-automation
description: 根据需求文档、测试用例、OpenAPI、Postman、Apipost、Swagger、Markdown 接口文档、后端文档或后端路由生成场景化接口自动化。适用于生成接口流程编排、scenarios.yaml/scenarios.json 场景文件、unittest/pytest 兼容的接口自动化测试，以及带数据依赖的端到端接口测试；不用于生成单元测试。
---

# 场景化接口自动化

使用本 skill 将接口资料和测试用例转换成场景化接口自动化。目标不是生成单接口冒烟用例，而是生成可执行的业务流程：包含请求顺序、变量提取、跨步骤数据依赖、业务断言和清晰的失败反馈。

## 工作流程

1. 收集源材料：
   - 接口资料：OpenAPI、Swagger、Postman 集合、Apipost 导出、Markdown 接口文档、后端路由文件。
   - 可选上游测试用例，例如 `test-case-xmind` 生成的 `cases.json`。
   - 环境信息：`base_url`、测试账号、鉴权方式、必要测试数据、数据清理要求。
2. 编写场景 DSL 前，阅读 `references/scenario_schema.md`。
3. 导出测试代码前，阅读 `references/pytest_export.md`。
4. 如果接口资料是 Markdown，可以先运行 `scripts/extract_api_inventory.py` 提取接口清单。
5. 生成 `scenarios.yaml`。除非用户明确要求其他格式，否则保持 JSON 兼容 YAML。
6. 运行 `scripts/validate_scenarios.py scenarios.yaml` 校验场景文件，并修复所有错误。
7. 运行 `scripts/export_pytest.py scenarios.yaml --output <项目目录>/api-automation` 导出接口自动化测试代码。
8. 如果目标应用可以在本地运行，执行生成的测试套件；如果无法运行，交付生成文件并说明未执行的原因。

## 场景设计规则

- 优先生成 3-8 条有价值的业务场景，而不是大量浅层接口检查。
- 使用 `extract` 和 `{{ variable }}` 模板串联步骤之间的数据。
- 同时断言传输结果和业务结果：
  - HTTP 状态码。
  - 响应字段。
  - 创建后的资源能被查询。
  - 数量、状态、归属关系或业务流转符合预期。
  - 禁止访问路径返回正确失败结果。
- 在有价值的地方加入反向场景：缺少必填字段、非法 ID、错误鉴权、过期状态、重复提交、可注入的服务错误。
- 保持测试确定性。避免真实支付、真实邮件、真实 AI 调用或不可逆的生产操作。
- 如果没有清理接口，生成唯一测试数据，并避免依赖持久化全局状态。

## 输出结构

默认输出目录：

```text
api-automation/
├── scenarios.yaml
├── tests/
│   └── test_api_scenarios.py
└── README.generated.md
```

`scenarios.yaml` 是接口自动化的源文件。生成的测试文件会内嵌场景定义，因此运行时不需要额外 YAML 解析依赖。导出的测试基于 `unittest`，也可以被 pytest 收集执行。

## 脚本

可在任意工作目录运行：

```bash
python3 <skill>/scripts/extract_api_inventory.py docs/接口文档.md --output api-inventory.json
python3 <skill>/scripts/validate_scenarios.py scenarios.yaml
python3 <skill>/scripts/export_pytest.py scenarios.yaml --output api-automation
```

脚本只使用 Python 标准库。生成的接口自动化测试也只使用 Python 标准库，可以通过 `python3 -m unittest` 运行；如果项目安装了 pytest，也可以被 pytest 收集执行。
