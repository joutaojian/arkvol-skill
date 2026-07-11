# Arkvol Skill 升级指南

## 查看版本

版本号记录在 Skill 目录的 [`VERSION`](VERSION) 文件中。没有该文件的旧版本可直接升级。

升级不会覆盖用户目录中的 `~/.arkvol/arkvol-entry.json`。如果 Key 保存在 Skill 内的 `shared/arkvol-entry.json`，请先备份该文件。

## 让 Agent 升级（推荐）

如果最初是让 Agent 安装的，直接告诉它：

```text
帮我把 Arkvol Skill 升级到最新版本：https://github.com/joutaojian/arkvol-skill
```

升级后重新打开会话，并查询一次市场数据进行验证。

## 使用 CLI 升级

通过 `npx skills add` 安装的用户，执行：

```bash
npx skills update arkvol-greed-index
```

如果提示找不到 Skill，重新安装：

```bash
npx skills add joutaojian/arkvol-skill -a codex
```

完整参数见 [`skills` CLI 官方文档](https://github.com/vercel-labs/skills#skills-update)。

## WorkBuddy

WorkBuddy 手动导入的 Skill 按以下步骤升级：

1. 从 [GitHub Releases](https://github.com/joutaojian/arkvol-skill/releases) 下载并解压新版本。
2. 备份旧版 `shared/arkvol-entry.json`（如有）。
3. 在技能管理中删除、替换或停用旧版，然后导入新版完整目录，不要只替换 `SKILL.md`。
4. 必要时恢复包内 Key，重新打开会话并查询一次市场数据。

## 版本发布

项目使用语义化版本。仓库中的 `VERSION`、Git tag `vX.Y.Z` 和 GitHub Release 必须一致，不在 `SKILL.md` 中添加版本字段。

维护者发布新版本时：

1. 更新 `VERSION` 和相关文档，并完成测试。
2. 提交变更，创建并推送同版本 tag，例如 `v0.2.0`。
3. 创建同名 GitHub Release，说明主要变化和不兼容项。
4. 分别验证 Codex 安装和 WorkBuddy 完整目录导入。

已发布的 tag 不应移动或重写；修复问题时发布新的版本。
