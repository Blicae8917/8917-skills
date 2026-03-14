# DCE Protocol Skill

> Discuss → Confirm → Execute

让 AI Agent 从被动执行者变成主动协作者。

---

## 安装

```bash
# 通过 ClawHub
clawhub install dce-protocol

# 或手动安装
cp SKILL.md ~/.agents/skills/dce-protocol/
cp -r templates/* ~/your-agent/
```

---

## 使用

在 AGENTS.md 中添加：

```markdown
## DCE Protocol

所有关键任务遵循 DCE：
- [D]iscuss: 给 2-3 个方案，主动挖掘信息
- [C]onfirm: 等"执行"指令，不猜不蒙
- [E]xecute: 确认后行动，记录复盘
```

---

## 模板文件

复制到 Agent 工作区：

| 模板 | 用途 |
|:---|:---|
| [SESSION-STATE.md](templates/SESSION-STATE.md) | 当前任务状态追踪 |
| [DCE-REVIEW.md](templates/DCE-REVIEW.md) | 任务复盘记录 |

---

## 理论基础

- [DCE 设计原则](../../organization-mastery/docs/DESIGN.md)
- [信息挖掘机制](../../organization-mastery/docs/DESIGN.md#主动信息挖掘机制)
- [开源战略](../../organization-mastery/docs/ROADMAP.md)

---

## 触发条件

必须使用 DCE 的场景：
- 配置修改（openclaw.json, Gateway）
- 外部通信（邮件、社交媒体）
- 数据删除、权限变更
- 安全相关操作
- 不可逆操作（发布、部署）
- 高资源消耗任务
- 首次任务

---

_由 8917OpenClaw 维护_
