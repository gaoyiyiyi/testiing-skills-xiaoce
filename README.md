# testiing-skills-xiaoce

这是一个用于 Codex 的测试用例生成 skill 仓库。

当前包含：

- `test-case-xmind`：根据需求文档、前端技术文档、后端技术文档、交互稿、接口文档等资料生成结构化测试用例，并导出 `.xmind` 文件。

## 安装

将 skill 目录复制到本机 Codex skills 目录：

```bash
cp -R test-case-xmind ~/.codex/skills/
```

重启或刷新 Codex 后，即可通过 `$test-case-xmind` 使用。

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
```

## 脚本说明

脚本是给 Codex 自动调用的稳定工具。用户通常不需要手动运行。

维护或调试时可以运行：

```bash
python3 test-case-xmind/scripts/validate_cases.py cases.json
python3 test-case-xmind/scripts/export_xmind.py cases.json --output test-cases.xmind
```

脚本只使用 Python 标准库，不需要额外安装依赖。
