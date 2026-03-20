# Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-agent--skills-blue.svg)](https://github.com/Blicae8917/agent-skills)

> 实用 AI Agent Skills 集合

开箱即用的 Agent 能力增强包。

---

## Skills 列表

| Skill | 版本 | 说明 |
|:---|:---|:---|
| [dce-protocol](packages/dce-protocol/) | v2.0.0 | Discuss-Confirm-Execute 安全协议 |

---

## 快速开始

```bash
# 通过 ClawHub 安装
clawhub install dce-protocol

# 或手动安装
cp packages/dce-protocol/SKILL.md ~/.agents/skills/
cp -r packages/dce-protocol/templates/* ~/your-agent/
```

---

## 理论基础

这些 Skills 基于 [organization-mastery](https://github.com/Blicae8917/organization-mastery) 方法论：
- [DCE 设计原则](https://github.com/Blicae8917/organization-mastery/blob/main/docs/DESIGN.md)
- [信息挖掘机制](https://github.com/Blicae8917/organization-mastery/blob/main/docs/DESIGN.md)

**建议**: 先理解原理，再使用工具，效果提升 3 倍。

---

## 开发 Skills

参考 [specs/skill-spec-v1.md](specs/skill-spec-v1.md)

---

_由 [8917OpenClaw](https://github.com/Blicae8917) 维护_
