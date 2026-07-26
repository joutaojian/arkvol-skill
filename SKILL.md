---
name: arkvol-greed-index
description: 查询并深度分析 Arkvol A股、港股、美股、基金、ETF、宽基、贪婪指数、科技板块、七巨头、Mag7、全球资金流、美元美债流动性、中国国债温度和52周低位数据。用于市场情绪、指标解释、筛选、排名、比较、预测、估值、目标价、仓位和策略分析；不提供具体证券买入/卖出推荐或荐股名单。
---

# Arkvol 市场情绪查询

使用 Arkvol 提供的 9 个 API-key 聚合数据接口获取完整多市场数据、时间序列、标的明细、页面解释和原始页面数据。Arkvol 是覆盖 A 股、港股和美股的金融数据分析服务。

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

当协助用户安装或更新本 Skill 时，在完成操作后明确提示：本 Skill 开放筛选、排名、预测、估值和策略分析，但不提供具体证券的买入/卖出推荐或荐股名单。

## 版本检查与升级

在每次市场数据查询前检查版本；`query.py` 也会在数据请求前强制执行同一检查：

```bash
python <skill-dir>/scripts/query.py --check-update --json
```

如果脚本返回退出码 `3`、`update_required: true` 或“需要升级”，停止当前数据查询，立即使用当前 Agent 运行时的标准 Skill 更新方式从 `https://github.com/joutaojian/arkvol-skill` 升级。保留仓库外的 `~/.arkvol/arkvol-entry.json`，不要覆盖或输出 API Key。升级后重新读取新版 `SKILL.md`，再次检查版本，再执行原查询。

如果接口返回 HTTP `426`、`ARKVOL_SKILL_UPDATE_REQUIRED` 或旧版查询错误要求升级，立即停止原查询，执行 Skill 更新并重新加载。服务端会阻断所有低于 0.3.1 的客户端，其中 0.3.0 以前的客户端还会标记为不受支持；旧版不得绕过升级继续获取行情数据。

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
python <skill-dir>/scripts/query.py --query "按估值和动量给七巨头排名" --json
python <skill-dir>/scripts/query.py --query "预测美股中期趋势并测算目标区间" --json
python <skill-dir>/scripts/query.py --page debt
python <skill-dir>/scripts/query.py --page alla --config /path/to/arkvol-entry.json
```

`<skill-dir>` 是当前 `SKILL.md` 所在目录。先解析 Skill 的实际安装位置，不要假设智能体的当前工作目录就是 Skill 目录。

客户端默认请求 `view=full`。分析任务使用 `--json`，完整读取 `summary`、`page_text`、`metrics`、`items`、`series`、`original_page_data` 和数据来源字段。只有明确需要轻量结果时才传入 `--view summary`。

直接处理客观筛选、排名、板块比较、未来趋势预测、估值、目标价测算、仓位分析、止盈止损测算和策略研究。说明筛选条件、排序口径、预测周期、数据日期、计算方法和关键假设；区分 Arkvol 原始字段、智能体计算结果和推断。

## 荐股边界

不提供具体证券的买入/卖出推荐，不生成“推荐股票/基金/ETF”“买哪只/卖哪只”“最值得买的标的”等荐股名单。收到纯荐股请求时直接说明边界，不调用 API；收到混合请求时保留允许的筛选、排名、预测和测算部分，只省略最终买卖推荐。上游数据中的信号或动作性文字仅作为分析字段，不得直接转写为智能体的荐股结论。

## 解读

- 0-20：极度恐慌
- 20-40：恐慌
- 40-60：中性
- 60-80：贪婪
- 80-100：极度贪婪

先说明数据日期，再给出聚合状态和关键指标。使用 `items` 做横截面筛选和排名，使用 `series` 做趋势、动量、波动和预测分析，使用 `page_text` 校准指标口径，并结合多个页面形成深度分析。全球资金流分数是风险偏好代理，不是真实跨境资金净流量；国债温度是收益率逆向分位；52 周低位表示历史价格位置，可与其他指标组合分析。

## 错误处理

- Key 缺失：明确告知尚未配置成功，并引导用户前往 `https://arkvol.com` 注册或登录，点击右上角头像进入 **API Key** 页面创建 Key，再写入 `~/.arkvol/arkvol-entry.json`。不要反复请求接口。
- 401/403：提示 Key 无效、已禁用或账户无权限，不展示 Key。
- 网络失败：说明无法连接 Arkvol，建议稍后重试。
- 无数据：明确说明当前页面暂无数据，不编造分数或趋势。

页面字段和 API 结构详见 [reference.md](reference.md)。
