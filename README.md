<div align="center">

**English** | [简体中文](README.zh-CN.md)

# Arkvol Skill

**Query and interpret multi-market financial data with natural language in AI agents**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-blue)](https://skills.sh)
[![Multi-Runtime](https://img.shields.io/badge/Runtime-Claude%20Code%20%20Codex%20%20Cursor%20%20OpenClaw%20%20Hermes-blueviolet)](#2-install-the-skill)

[Arkvol.com](https://arkvol.com) · [Install](#2-install-the-skill) · [Update](#3-update-the-skill) · [Security](#security)

<p align="center">
  <img src="shared/arkvol-hero-16x9.gif" alt="Arkvol Skill Hero" />
  <br/>
</p>

</div>

## Overview

[arkvol.com](https://arkvol.com) is a financial data analysis service covering mainland China A-shares, Hong Kong stocks, and US stocks. It helps users observe market conditions and trends through market sentiment, fear and greed indexes, sector rotation, and related indicators.

Arkvol Skill brings the data querying and interpretation capabilities of [arkvol.com](https://arkvol.com) to AI agents compatible with the Agent Skills standard. Once installed, users can query A-shares and technology sectors, Hong Kong stocks, funds and ETFs, US medium-term trends, the Magnificent Seven, global capital flows, China government bond temperature, and 52-week-low aggregate statistics using natural language. Results include the data date, key indicators, and clear risk boundaries.

See [`VERSION`](VERSION) for the current source version.

## API Key Skill Reference Implementation

This Skill natively supports API key configuration and has been tested in practice by more than 100 users. It is a strong reference implementation for other projects that need to build an API-key-enabled Skill.

Reusable design patterns include storing user credentials outside the Skill repository, defining an explicit priority order for command-line options, configuration files, and environment variables, supporting automated upgrades, providing example configuration without committing real secrets, handling authentication errors consistently, and preventing complete keys from appearing in responses or logs. Other Skill projects can directly adopt these configuration and security boundaries.

## 1. Get an API Key

Register or sign in at [arkvol.com](https://arkvol.com), open **API Key** from the avatar menu in the upper-right corner, and create a key. The complete key is displayed only once.

<img src="shared/p1.png" alt="Arkvol API Key creation page" />

## 2. Install the Skill

Arkvol Skill follows the open [Agent Skills](https://agentskills.io) standard and runs in AI agents that support Agent Skills.

> Installation notice: This Skill provides market data and indicator interpretation only. It does not recommend securities and does not constitute investment advice. Users are responsible for their own investment decisions and risks.

Open the agent you use, such as Claude Code, Codex, Cursor, OpenClaw, or WorkBuddy, and tell it:

```text
Install this Skill: https://github.com/joutaojian/arkvol-skill
Help me configure the Arkvol Skill API key.
My API key is: [replace with your API key]
```

After installation, you can ask questions such as:

```text
What is the current sentiment in the A-share market?
Is the global capital flow indicator currently expanding or contracting?
What is the current temperature of China's 30-year government bond market?
How many valid samples are currently in the 52-week-low model?
```

## 3. Update the Skill

Starting with version 0.3.0, every data query checks Arkvol for the latest Skill version first. You can also ask your AI agent directly:

> Update notice: This Skill provides market data and indicator interpretation only. It does not recommend securities and does not constitute investment advice. Users are responsible for their own investment decisions and risks.

```text
Upgrade Arkvol Skill to the latest version: https://github.com/joutaojian/arkvol-skill
```

## Security

If the API key is missing, the script directs the user to create one at Arkvol and add it to the configuration file.

- Do not ask or use this Skill to recommend, screen, or rank financial products, or to generate trading signals.
- Provide the key only in a trusted local or private agent session. Never expose it in a README, public chat, command history, or logs.
- Do not share or upload a Skill installation that contains a key to GitHub.
- If a key is exposed, regenerate or disable it in Arkvol immediately.
