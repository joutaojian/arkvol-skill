# Arkvol 数据参考

脚本接收 Arkvol 聚合接口响应后，只对外输出以下合规字段白名单：

- `source`、`page`、`title`、`as_of`
- `sentiment_score`、由分数确定的 `sentiment_label`
- 根据合规字段在本地生成的中性 `metric_definitions`
- 固定的 `limitations` 和 `notice`

脚本不输出任何上游自由文本。不要绕过脚本读取、展示或转述上游原始 `summary`、`page_text`、`notes`、`metrics` 或 `items`；这些字段可能包含不适合对外输出的策略、信号、排名、预测或操作性文字。

端点映射：

| 页面 | 端点 |
|---|---|
| `alla` | `/api/data/alla` |
| `alla-tech` | `/api/data/alla-tech` |
| `funds-greed` | `/api/data/funds-greed` |
| `gll` | `/api/data/gll` |
| `greed-mid-term` | `/api/data/greed/mid-term` |
| `us7-rotation` | `/api/data/us7-rotation` |

所有请求使用 Header `X-API-Key: arkvol-sk-...` 并显式请求 `view=summary`。不得在回答、日志或错误信息中输出完整 Key。
