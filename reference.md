# Arkvol 数据参考

每个接口返回 `{ "code": 0, "data": ..., "msg": "" }`。`data` 包含：

- `page`、`route`、`title`、`as_of`
- `sentiment_score`、`sentiment_label`、`summary`
- `page_text`：页面简介、区块文字、指标定义、解释规则和提示
- `metrics`、`series`、`items`：便于快速读取的统一索引
- `source_page_apis`：原页面只读数据来源
- `original_page_data`：原页面完整明细，保留既有响应结构

端点映射：

| 页面 | 端点 |
|---|---|
| `alla` | `/api/data/alla` |
| `alla-tech` | `/api/data/alla-tech` |
| `funds-greed` | `/api/data/funds-greed` |
| `gll` | `/api/data/gll` |
| `greed-mid-term` | `/api/data/greed/mid-term` |
| `us7-rotation` | `/api/data/us7-rotation` |

所有请求使用 Header `X-API-Key: arkvol-sk-...`。`summary` 是当期结论，`page_text` 是数据语义和计算口径，`original_page_data` 是完整明细来源。
