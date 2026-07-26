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

所有请求使用 Header `X-API-Key: arkvol-sk-...` 并显式请求 `view=summary`。`summary` 是当期结论，`page_text` 是数据语义和计算口径，`metrics` 和 `items` 提供最新摘要明细。

Skill 不直接转发上述原始响应。`scripts/query.py` 只输出本地白名单中的日期、0-100 聚合分数、聚合数量和本地指标定义；不会输出上游自由文本、个股清单、排名、目标价或交易动作字段。`low-52w-leverage` 仅返回阈值、扫描数、命中数和过期样本数。

## Skill 版本检查

- 端点：`GET /api/data/skill-version`
- 请求头：`X-Arkvol-Skill-Version: <VERSION 文件内容>`
- 响应字段：`current_version`、`latest_version`、`minimum_supported_version`、`update_available`、`update_required`、`repository_url`
- 响应头：`X-Arkvol-Skill-Latest-Version`、`X-Arkvol-Skill-Update-Available`、`X-Arkvol-Skill-Update-Url`

正常数据端点也返回相同的 `data.skill_update`。缺少版本头时，服务端按 0.2.0 兼容客户端处理，并把升级提示写入 `summary` 和 `page_text.notes[0]`。0.3.0 及后续版本必须先检查版本；`update_required` 为 `true` 时停止查询并先升级。
