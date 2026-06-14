# 场景 DSL 结构说明

`scenarios.yaml` 使用 JSON 兼容 YAML 编写。也就是说，一个合法 JSON 文档保存为 `.yaml` 也可以被脚本读取。这样可以减少依赖，同时方便后续转换成其他格式。

## 根对象

必填字段：

- `title`：字符串，表示这组接口自动化场景的标题。
- `scenarios`：非空数组，包含一个或多个场景对象。

可选字段：

- `base_url`：字符串。运行时可通过环境变量 `API_BASE_URL` 覆盖。
- `variables`：对象。全局变量，可被所有场景使用。

## 场景对象

必填字段：

- `name`：字符串，场景名称。
- `steps`：非空数组，包含一个或多个步骤对象。

可选字段：

- `description`：字符串，场景说明。
- `variables`：对象，场景级变量，会覆盖或补充根对象变量。

## 步骤对象

必填字段：

- `id`：稳定标识，只允许字母、数字、下划线和连字符。
- `name`：可读的步骤名称。
- `request`：请求对象，包含：
  - `method`：GET、POST、PUT、PATCH、DELETE。
  - `path`：字符串，支持 `{{ variable }}` 变量模板。

可选字段：

- `request.query`：对象，查询参数。
- `request.headers`：对象，请求头。
- `request.body`：对象、数组、字符串、数字、布尔值或 null。
- `extract`：对象，把响应中的字段提取成变量，例如 `"item_id": "$.data.id"`。
- `assert`：数组，包含一个或多个断言对象。

## 支持的断言

每个请求至少需要一个状态码断言。

```json
{"type": "status", "expected": 200}
{"type": "json_path_exists", "path": "$.data.id"}
{"type": "json_path_not_exists", "path": "$.data.error"}
{"type": "json_equals", "path": "$.data.success", "expected": true}
{"type": "json_not_equals", "path": "$.data.id", "expected": null}
{"type": "json_contains", "path": "$.message", "expected": "成功"}
{"type": "json_length", "path": "$.data.items", "expected": 3}
{"type": "var_equals", "name": "item_id", "expected": "item_001"}
```

## JSON Path 支持范围

脚本只支持一小部分稳定、可预测的 JSON Path：

- 根节点以 `$` 开头。
- 点访问：`$.data.id`。
- 数组下标：`$.data.items[0]`。

不要使用过滤器、通配符、递归查找或复杂表达式。

## 变量模板

任意字符串字段都可以引用变量：

```json
"path": "/api/items/{{ item_id }}"
```

变量来源按优先级依次为：

1. 根对象 `variables`
2. 场景对象 `variables`
3. 前面步骤的 `extract`

## 最小示例

```json
{
  "title": "商品接口自动化场景",
  "base_url": "http://127.0.0.1:8080",
  "scenarios": [
    {
      "name": "创建商品后查询商品详情",
      "steps": [
        {
          "id": "create_item",
          "name": "创建商品",
          "request": {
            "method": "POST",
            "path": "/api/items",
            "body": {
              "name": "自动化测试商品",
              "price": 99
            }
          },
          "assert": [
            {"type": "status", "expected": 200},
            {"type": "json_path_exists", "path": "$.data.id"}
          ],
          "extract": {
            "item_id": "$.data.id"
          }
        },
        {
          "id": "get_item",
          "name": "查询商品详情",
          "request": {
            "method": "GET",
            "path": "/api/items/{{ item_id }}"
          },
          "assert": [
            {"type": "status", "expected": 200},
            {"type": "json_equals", "path": "$.data.name", "expected": "自动化测试商品"}
          ]
        }
      ]
    }
  ]
}
```
