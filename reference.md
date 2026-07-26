# Arkvol 数据参考

每个接口返回 `{ "code": 0, "data": ..., "msg": "" }`。`data` 包含：

- `page`、`route`、`title`、`as_of`
- `sentiment_score`、`sentiment_label`、`summary`
- `page_text`：页面简介、区块文字、指标定义、解释规则和提示
- `metrics`、`items`：便于快速读取的统一摘要索引
- `source_page_apis`：原页面只读数据来源
- `cache`：快照版本、构建时间、数据日期和响应视图

端点映射：

| 页面 | 端点 |
|---|---|
| `alla` | `/api/data/alla` |
| `alla-tech` | `/api/data/alla-tech` |
| `funds-greed` | `/api/data/funds-greed` |
| `gll` | `/api/data/gll` |
| `greed-mid-term` | `/api/data/greed/mid-term` |
| `us7-rotation` | `/api/data/us7-rotation` |
| `global-capital-flow` | `/api/data/global-capital-flow` |
| `debt` | `/api/data/debt` |
| `low-52w-leverage` | `/api/data/low-52w-leverage` |

所有请求使用 Header `X-API-Key: arkvol-sk-...`。客户端默认请求 `view=full`；`--view summary` 可用于轻量查询。`summary` 是当期结论，`page_text` 是数据语义和计算口径，`metrics` 和 `items` 提供最新明细，`series` 和 `original_page_data` 提供完整分析上下文。

`scripts/query.py --json` 直接输出完整接口响应，不再使用本地字段白名单。智能体可以使用完整数据做筛选、排名、预测、估值、目标价和策略分析，但不得输出具体证券买入/卖出推荐或荐股名单。

## Skill 版本检查

- 端点：`GET /api/data/skill-version`
- 请求头：`X-Arkvol-Skill-Version: <VERSION 文件内容>`
- 响应字段：`current_version`、`latest_version`、`minimum_supported_version`、`update_available`、`update_required`、`repository_url`
- 响应头：`X-Arkvol-Skill-Latest-Version`、`X-Arkvol-Skill-Update-Available`、`X-Arkvol-Skill-Update-Url`

版本检查端点返回结构化状态。正常数据端点发现 `update_required: true` 时返回 HTTP `426`，响应 `msg` 以 `ARKVOL_SKILL_UPDATE_REQUIRED` 开头，并在 `data.skill_update` 中提供版本和仓库地址。缺少版本头时按旧版处理；0.3.0 以前的客户端会被标记为不受支持，任何低于最新版本的客户端都无法继续获取行情数据。
