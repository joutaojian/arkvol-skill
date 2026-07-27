<div align="center">

**简体中文** | [English](#english)

# Arkvol Skill

**让 AI Agent 使用自然语言查询并解读多市场金融数据**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-blue)](https://skills.sh)
[![Multi-Runtime](https://img.shields.io/badge/Runtime-Claude%20Code%20%20Codex%20%20Cursor%20%20OpenClaw%20%20Hermes-blueviolet)](#2-安装-skill)

[Arkvol.com](https://arkvol.com) · [安装](#2-安装-skill) · [更新](#3-更新-skill) · [安全与合规](#安全与合规)

<p align="center">
  <img src="shared/arkvol-hero-16x9.gif" alt="Arkvol Skill Hero" />
  <br/>
</p>

</div>

## 简介

[arkvol.com](https://arkvol.com) 是覆盖 A 股、港股和美股的金融数据分析服务，通过市场情绪、贪婪与恐慌指数、板块轮动等指标，帮助用户观察市场状态和趋势。

Arkvol Skill 将 [arkvol.com](https://arkvol.com) 的数据查询与解读能力接入兼容 Agent Skills 的 AI Agent。安装后，可以直接用自然语言查询 A 股与科技板块、港股、基金与 ETF、美股中期趋势、七巨头、全球资金流、中国国债温度和 52 周低位数据。

> **合规声明：Arkvol Skill 遵守中国法律法规，不提供具体证券买入/卖出推荐，也不生成股票、基金或 ETF 荐股名单。**

当前源码版本见 [`VERSION`](VERSION)。

## API Key Skill 参考实例

这是一个原生支持 API Key 配置的 Skill，已经过 100+ 用户的实践测试，可作为其他项目开发 API Key Skill 的参考实例。

可复用的设计包括：将用户密钥持久化在 Skill 仓库之外、支持命令行/配置文件/环境变量的明确优先级、支持自动化升级、提供不含真实密钥的示例配置、统一处理鉴权错误，以及避免在回答和日志中输出完整 Key。其他 Skill 项目可以借鉴这套配置与安全边界设计。

## 1. 获取 API Key

前往 [arkvol.com](https://arkvol.com) 注册或登录，从右上角头像进入 **API Key** 页面创建 Key。完整 Key 仅显示一次。

<img src="shared/p1.png" alt="Arkvol API Key 创建页面" />

## 2. 安装 Skill

Arkvol Skill 基于开放的 [Agent Skills](https://agentskills.io) 协议，可在兼容 Agent Skills 的 AI Agent 中运行。

> **安装前请知悉：本 Skill 不提供具体证券买入/卖出推荐，也不生成股票、基金或 ETF 荐股名单。**

打开你正在使用的 Agent（如 Claude Code、Codex、Cursor、OpenClaw 或 WorkBuddy），告诉它：

```text
帮我安装这个 Skill：https://github.com/joutaojian/arkvol-skill，并帮我配置 Arkvol Skill 的 API Key。
我的 API Key 是：[替换成你的 API Key]
```

安装完成后可直接询问：

```text
现在 A 股情绪怎么样？
全球资金流蛋糕当前是扩张还是收缩？
中国 30 年期国债温度是多少？
```

## 3. 更新 Skill

从 0.3.0 版本起，每次数据查询都会先向 Arkvol 检查最新 Skill 版本。也可以主动告诉 AI Agent：

> 更新提示：低于服务端配置版本的 Skill 会被 API 阻断，必须升级并重新加载后才能继续查询。

```text
帮我把 Arkvol Skill 升级到最新版本：https://github.com/joutaojian/arkvol-skill
```

## 安全与合规

Arkvol Skill 以遵守中国法律法规为基本原则。

- 不要使用本 Skill 生成具体证券买入/卖出推荐名单；
- 不提供具体证券买入/卖出推荐，也不生成股票、基金或 ETF 荐股名单。
- 仅在可信的本地或私有 Agent 会话中提供 Key，不要在 README、公开聊天、命令记录或日志中公开 Key。
- 不得将包含 Key 的 Skill 分享或上传至 GitHub。
- Key 泄露后，应立即在 Arkvol 重新生成或禁用。

<a id="english"></a>

---

<div align="center">

[简体中文](#arkvol-skill) | **English**

# Arkvol Skill (English)

**Query and interpret multi-market financial data with natural language in AI agents**

</div>

## Overview

[arkvol.com](https://arkvol.com) is a financial data analysis service covering mainland China A-shares, Hong Kong stocks, and US stocks. It helps users observe market conditions and trends through market sentiment, fear and greed indexes, sector rotation, and related indicators.

Arkvol Skill brings the data querying and interpretation capabilities of [arkvol.com](https://arkvol.com) to AI agents compatible with the Agent Skills standard. Once installed, users can query A-shares and technology sectors, Hong Kong stocks, funds and ETFs, US medium-term trends, the Magnificent Seven, global capital flows, China government bond temperature, and 52-week-low data using natural language.

> **Compliance statement: Arkvol Skill complies with the laws and regulations of China. It does not provide recommendations to buy or sell specific securities and does not generate stock, fund, or ETF recommendation lists.**

See [`VERSION`](VERSION) for the current source version.

## API Key Skill Reference Implementation

This Skill natively supports API key configuration and has been tested in practice by more than 100 users. It is a strong reference implementation for other projects building API-key-enabled Skills.

Reusable design patterns include storing user credentials outside the Skill repository, defining an explicit priority order for command-line options, configuration files, and environment variables, supporting automated upgrades, providing example configuration without committing real secrets, handling authentication errors consistently, and preventing complete keys from appearing in responses or logs.

## Installation

Arkvol Skill follows the open [Agent Skills](https://agentskills.io) standard and runs in AI agents that support Agent Skills.

> **Before installation: This Skill does not provide recommendations to buy or sell specific securities and does not generate stock, fund, or ETF recommendation lists.**

Open the agent you use, such as Claude Code, Codex, Cursor, OpenClaw, or WorkBuddy, and tell it:

```text
Install this Skill: https://github.com/joutaojian/arkvol-skill
Help me configure the Arkvol Skill API key.
My API key is: [replace with your API key]
```

## Updates

Starting with version 0.3.0, every data query checks Arkvol for the latest Skill version first. Versions below the release configured by the service are blocked by the API until the Skill is upgraded and reloaded.

```text
Upgrade Arkvol Skill to the latest version: https://github.com/joutaojian/arkvol-skill
```

## Security and Compliance

Arkvol Skill treats compliance with the laws and regulations of China as a fundamental requirement.

- It does not provide recommendations to buy or sell specific securities and does not generate stock, fund, or ETF recommendation lists.
- Provide the key only in a trusted local or private agent session. Never expose it in a README, public chat, command history, or logs.
- Do not share or upload a Skill installation containing a key to GitHub.
- If a key is exposed, regenerate or disable it in Arkvol immediately.
