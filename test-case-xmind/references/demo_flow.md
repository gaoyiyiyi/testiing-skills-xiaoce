# 演示流程

当用户希望在 Codex 中做一个更丝滑的演示时，使用本流程。

## 推荐演示路径

1. 根据用户提供的需求文档、前端技术文档、后端技术文档、交互稿等资料生成 `cases.json`。
2. 校验用例结构：

   ```bash
   python3 scripts/validate_cases.py cases.json
   ```

3. 导出 XMind 文件：

   ```bash
   python3 scripts/export_xmind.py cases.json --output test-cases.xmind
   ```

4. 到此结束操作。不要生成 HTML 预览页，不要自动打开浏览器。

## 演示话术

可以这样说明：

> 我已经根据输入文档生成了结构化测试用例，校验了“一条前置条件、多个步骤、每个步骤一个预期结果”的格式，并按指定模板导出了真实 `.xmind` 文件。脑图中只保留用例标题、前置条件、步骤和预期结果。
