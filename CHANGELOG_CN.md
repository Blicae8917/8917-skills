# 更新日志

本项目的所有重要变更都会记录在本文件中。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，版本遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增
- `8917-write` v0.1：叶澄风公开长文写作 skill——选题双重质检（HKR + 资产判据）、内置证据链（依据块 + 核源 SOP）、四种文章原型、标题候选、证据核验置首的四层自检（adapted from khazix-writer + 自有方法论）
- `8917-wenzhen` v2.2：问诊·复盘双档（五问轻量收尾 / 指挥官十问对抗式会诊，含第十人异议、事前验尸、可证伪性检查）；v2.2 接线 `.8917/` 工作区落盘约定，执行债台账定位可移植化（有全局台账用全局，否则工作区局部 `.8917/execution-debt.md`）
- `8917-skills`：新增双语 changelog 支持（`CHANGELOG_CN.md`）

### 变更
- `8917-expert-panel` v2.2：运行时感知改造——Claude Code 与 Codex 分别使用各自原生专家库；新增统一专家卡注册表脚本、调用能力探测、动态并发分波、模式化 schema、失败 ledger 与可复现性门槛；重型能力缺失时不再静默伪降级
- `8917-expert-panel` v2.1：专家来源双源自适应——本机装有专家库（`~/.claude/agents/`，如 agency-agents）则优先选用，未装则现场生成专家 persona、零外部依赖独立运行；移除本机私有路径引用，保证开源可移植性
- 仓库结构：skill 直接住 `skills/` 层（移除冗余的 `native/` 中间层）

### 移除
- `8917-minimax-toolkit`、`8917-docx-official`、`8917-content-ingest`、`8917-dce-protocol`：自 2026-03 起停止维护或已被更强的通用工具取代；全部版本可在 git 历史中找到，已通过 ClawHub 安装的用户不受影响。公文写作 skill 将以升级版回归。
- 迁移期目录 `packages/`、`pending/`、`specs/`、`references/`：按当初迁移计划完成 legacy 清理

### 文档
- `protocol/SKILL_SPEC_V2.md`：保留为当前仓库级 Skill 规范参考
- README（中英）与 CONTRIBUTING 已更新为新结构与新 skill 清单

## [0.1.0] - 2026-03-14

### 新增
- 初始仓库结构
- DCE Protocol Skill 早期原型
- 早期 Skill 规范草案

[未发布]: https://github.com/Blicae8917/8917-skills/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Blicae8917/8917-skills/releases/tag/v0.1.0
