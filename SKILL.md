---
name: arkvol-greed-index
description: 查询 Arkvol A股、港股、美股、基金、ETF、宽基、贪婪指数、恐慌指数、情绪、科技板块、七巨头、Mag7、轮动、中期趋势、全A、恒生、沪深等市场情绪数据。用于回答最新市场情绪、指标含义、板块比较和历史趋势问题。
---

# Arkvol 市场情绪查询

使用 Arkvol 提供的 6 个聚合数据接口获取市场情绪摘要和解释文字。Arkvol 是覆盖 A 股、港股和美股的金融数据分析服务。

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

## 查询

根据问题选择页面：

- A股、大盘、沪深、全A：`alla`
- 科技、AI、半导体、芯片：`alla-tech`
- 基金、ETF、宽基：`funds-greed`
- 港股、恒生、全球、海外、乖离率：`gll`
- 美股贪婪、中期、中线、趋势：`greed-mid-term`
- 美股七巨头、七姐妹、Mag7、轮动：`us7-rotation`

执行：

```bash
python <skill-dir>/scripts/query.py --query "现在 A 股情绪怎么样"
python <skill-dir>/scripts/query.py --page us7-rotation --json
python <skill-dir>/scripts/query.py --page alla --config /path/to/arkvol-entry.json
```

`<skill-dir>` 是当前 `SKILL.md` 所在目录。先解析 Skill 的实际安装位置，不要假设智能体的当前工作目录就是 Skill 目录。

需要结构化分析时使用 `--json`。客户端固定请求轻量 `view=summary`；必须保留响应中的 `page_text`、`metrics` 和 `items`，用 `page_text` 解释指标、计算口径和风险边界，不要仅凭字段名推断。

## 解读

- 0-20：极度恐慌
- 20-40：恐慌
- 40-60：中性
- 60-80：贪婪
- 80-100：极度贪婪

先说明数据日期，再给出情绪结论和关键指标。区分当期 `summary` 与稳定的 `page_text` 解释。结尾保留数据仅供研究、不构成投资建议的边界。

## 错误处理

- Key 缺失：明确告知尚未配置成功，并引导用户前往 `https://arkvol.com` 注册或登录，点击右上角头像进入 **API Key** 页面创建 Key，再写入 `~/.arkvol/arkvol-entry.json`。不要反复请求接口。
- 401/403：提示 Key 无效、已禁用或账户无权限，不展示 Key。
- 网络失败：说明无法连接 Arkvol，建议稍后重试。
- 无数据：明确说明当前页面暂无数据，不编造分数或趋势。

页面字段和 API 结构详见 [reference.md](reference.md)。
