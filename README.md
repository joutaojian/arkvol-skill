<div align="center">

# Arkvol Skill

**让 AI Agent 使用自然语言查询并解读多市场金融数据**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-blue)](https://skills.sh)
[![Multi-Runtime](https://img.shields.io/badge/Runtime-Claude%20Code%20%20Codex%20%20Cursor%20%20OpenClaw%20%20Hermes-blueviolet)](#安装)

[Arkvol.com](https://arkvol.com) · [安装](#安装) · [配置 API Key](#配置-Api-Key) · [安全说明](#安全说明)
<p align="center">
  <img src="shared/arkvol-hero-16x9.gif" alt="Arkvol Skill Hero" />
  <br/>
</p>

</div>



## 简介

[arkvol.com](https://arkvol.com) 是覆盖 A 股、港股和美股的金融数据分析服务，通过市场情绪、贪婪与恐慌指数、板块轮动等指标，帮助用户观察市场状态和趋势。

Arkvol Skill 将 [arkvol.com](https://arkvol.com) 的数据查询与解读能力接入兼容 Agent Skills 的 AI Agent。安装后，可以直接用自然语言查询 A 股与科技板块、港股、基金与 ETF、美股中期趋势及七巨头轮动等数据，并获得包含数据日期、关键指标和风险边界的分析结果。

> 数据仅供研究，不构成投资建议。


## 1. 获取 API Key

### 获取 Key

前往 [arkvol.com](https://arkvol.com) 注册或登录，从右上角头像进入 **API Key** 页面创建 Key。完整 Key 仅显示一次。
<img src="shared/p1.png" alt="Arkvol Skill Hero" />



## 2. 安装Skill

Arkvol Skill 基于开放的 [Agent Skills](https://agentskills.io) 协议，可在兼容 Agent Skills 的 AI Agent 中运行。

### 方式一：让 Agent 安装（推荐）

打开你正在使用的 Agent（如 Claude Code、Codex、Cursor、OpenClaw、WorkBuddy 等），告诉它：

```text
帮我安装这个 Skill：https://github.com/joutaojian/arkvol-skill
```
```text
帮我配置 Arkvol Skill 的 API Key。我的 API Key 是：arkvol-sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 方式二：使用通用 CLI

使用 [vercel-labs/skills](https://github.com/vercel-labs/skills) 安装器：

```bash
npx skills add joutaojian/arkvol-skill
```

1、安装器会自动识别当前 Runtime 并安装到对应目录。需要指定 Runtime 时，可添加 `-a claude-code`、`-a codex`、`-a cursor` 或 `-a openclaw` 等参数。
2、进入大模型，告诉它:
```text
帮我配置 Arkvol Skill 的 API Key。我的 API Key 是：arkvol-sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 方式三：WorkBuddy 手动添加

1. 下载完整的 `arkvol-skill` 目录。
2. 在 WorkBuddy 的技能管理入口选择添加或导入自定义技能。
3. 导入整个目录；根目录必须包含 `SKILL.md`、`scripts/`、`shared/`，不能只上传 `SKILL.md`。
4. 如果只能读取包内配置，将 `shared/arkvol-entry.example.json` 复制为 `shared/arkvol-entry.json` 后填写 Key。
5. 添加后提问“现在 A 股情绪怎么样？”进行验证。


## 3. 配置Key

### 通过对话配置（推荐）

无需手动创建目录或配置文件。在可信的本地或私有 Agent 会话中，直接告诉大模型：

```text
帮我配置 Arkvol Skill 的 API Key。我的 API Key 是：arkvol-sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

大模型会找到 Arkvol Skill，并将 Key 写入当前用户的 `~/.arkvol/arkvol-entry.json`。配置完成后，可以继续让它查询市场数据来验证配置是否生效。

### 手动创建配置文件

也可以手动创建用户配置文件：

| 系统 | 路径 |
| --- | --- |
| Windows | `C:\Users\<用户名>\.arkvol\arkvol-entry.json` |
| macOS | `/Users/<用户名>/.arkvol/arkvol-entry.json` |
| Linux | `/home/<用户名>/.arkvol/arkvol-entry.json` |

```json
{
  "api_key": "arkvol-sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

读取顺序：`~/.arkvol/arkvol-entry.json` → `shared/arkvol-entry.json`


## 安全说明

缺少 Key 时，脚本会提示前往 Arkvol 创建并写入配置文件。

- 仅在可信的本地或私有 Agent 会话中提供 Key，不要在 README、公开聊天、命令记录或日志中公开 Key。
- 包含 Key 的 Skill 不得分享或上传 GitHub。
- Key 泄露后，立即在 Arkvol 重新生成或禁用。
