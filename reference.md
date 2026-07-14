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

所有请求使用 Header `X-API-Key: arkvol-sk-...` 并显式请求 `view=summary`。`summary` 是当期结论，`page_text` 是数据语义和计算口径，`metrics` 和 `items` 提供最新摘要明细。
