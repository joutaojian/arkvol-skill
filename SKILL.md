---
name: arkvol-greed-index
description: 查询 Arkvol A股、港股、美股、基金、ETF、宽基、贪婪指数、科技板块、七巨头、Mag7、全球资金流、美元美债流动性、中国国债温度和52周低位聚合统计。用于回答最新市场情绪、风险偏好、指标含义、板块比较和历史状态问题；不用于推荐、筛选、排名、预测或交易建议。
---

# Arkvol 市场情绪查询

使用 Arkvol 提供的 9 个 API-key 聚合数据接口获取多市场状态与本地白名单指标解释。Arkvol 是覆盖 A 股、港股和美股的金融数据分析服务。

## 准备凭据

1. 登录 `arkvol.com`。
2. 从右上角头像菜单进入 **API Key**。
3. 创建 Key，并写入用户配置文件。

不要把 Key 写入或直接修改 `SKILL.md`。通过 npx、GitHub 或其他工具安装时，在用户主目录创建 `~/.arkvol/arkvol-entry.json`，再填写 `api_key`：

- Windows：`C:\Users\<用户名>\.arkvol\arkvol-entry.json`
- macOS：`/Users/<用户名>/.arkvol/arkvol-entry.json`
- Linux：`/home/<用户名>/.arkvol/arkvol-entry.json`

```json
{
  "api_key": "arkvol-sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

WorkBuddy 等手动安装场景也可以将示例文件复制为 Skill 自身的 `shared/arkvol-entry.json`。Key 读取顺序为 `--api-key`、`--config` 指定文件、`~/.arkvol/arkvol-entry.json`、Skill 内 `shared/arkvol-entry.json`、`ARKVOL_API_KEY`。用户目录配置不会被 npx 安装或更新覆盖；Skill 内真实配置文件已被 `.gitignore` 排除。不要在回答或日志中输出完整 Key。

`arkvol-skill/` 是完整的可安装单元，脚本不得依赖其父目录中的项目私有模块。

## 安装与更新提示

当协助用户安装或更新本 Skill 时，在完成操作后明确提示：本 Skill 仅提供市场数据与指标解读，不做荐股，不构成投资建议；投资决策及风险由用户自行承担。

## 版本检查与升级

在每次市场数据查询前检查版本；`query.py` 也会在数据请求前强制执行同一检查：

```bash
python <skill-dir>/scripts/query.py --check-update --json
```

如果脚本返回退出码 `3`、`update_required: true` 或“需要升级”，停止当前数据查询，立即使用当前 Agent 运行时的标准 Skill 更新方式从 `https://github.com/joutaojian/arkvol-skill` 升级。保留仓库外的 `~/.arkvol/arkvol-entry.json`，不要覆盖或输出 API Key。升级后重新读取新版 `SKILL.md`，再次检查版本，再执行原查询。

如果旧版 0.2.0 的查询结果在“结论”或首条“提示”中要求升级，同样先完成升级，不要使用该次响应继续回答市场问题。

## 查询

根据问题选择页面：

- A股、大盘、沪深、全A：`alla`
- 科技、AI、半导体、芯片：`alla-tech`
- 基金、ETF、宽基：`funds-greed`
- 港股、恒生、全球、海外、乖离率：`gll`
- 美股贪婪、中期、中线、趋势：`greed-mid-term`
- 美股七巨头、七姐妹、Mag7、轮动：`us7-rotation`
- 全球资金流、资金蛋糕、全球轮动、美元美债流动性闸门：`global-capital-flow`
- 中国国债、30 年期收益率、国债价格温度：`debt`
- 52 周低位、GGBL 杠杆样本聚合数量：`low-52w-leverage`

执行：

```bash
python <skill-dir>/scripts/query.py --query "现在 A 股情绪怎么样"
python <skill-dir>/scripts/query.py --page us7-rotation --json
python <skill-dir>/scripts/query.py --query "全球资金流蛋糕当前是什么状态" --json
python <skill-dir>/scripts/query.py --page debt
python <skill-dir>/scripts/query.py --page alla --config /path/to/arkvol-entry.json
```

`<skill-dir>` 是当前 `SKILL.md` 所在目录。先解析 Skill 的实际安装位置，不要假设智能体的当前工作目录就是 Skill 目录。

需要结构化分析时使用 `--json`。客户端固定请求轻量 `view=summary`，随后仅输出本地白名单中的日期、聚合分数、聚合数量和本地指标定义。不要转述上游 `summary`、`page_text` 自由文本、`items`、个股清单、排名、目标价或动作性字段。`low-52w-leverage` 只解释阈值和聚合数量，不列出具体标的。

收到推荐、筛选、排名、未来涨跌、仓位、目标价、止盈止损或交易策略请求时，在调用 API 前拒绝，并说明本 Skill 仅提供非个性化市场数据和历史指标解释。

## 解读

- 0-20：极度恐慌
- 20-40：恐慌
- 40-60：中性
- 60-80：贪婪
- 80-100：极度贪婪

先说明数据日期，再给出聚合状态和关键指标。仅依据脚本的合规输出解释：全球资金流分数是风险偏好代理，不是真实跨境资金净流量；国债温度是收益率逆向分位，收益率越低则债券价格温度越高；52 周低位只说明历史价格位置样本数量。

## 错误处理

- Key 缺失：明确告知尚未配置成功，并引导用户前往 `https://arkvol.com` 注册或登录，点击右上角头像进入 **API Key** 页面创建 Key，再写入 `~/.arkvol/arkvol-entry.json`。不要反复请求接口。
- 401/403：提示 Key 无效、已禁用或账户无权限，不展示 Key。
- 网络失败：说明无法连接 Arkvol，建议稍后重试。
- 无数据：明确说明当前页面暂无数据，不编造分数或趋势。

页面字段和 API 结构详见 [reference.md](reference.md)。
