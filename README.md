# 8917-skills

> 8917 的开源能力兵工厂，收录已治理、可复用、可发布的主权技能与 wrapper。

---

## 第一批技能资产（已入库）

| Skill | 说明 | 状态 |
|:---|:---|:---|
| `8917-minimax-toolkit` | MiniMax 多模态生成工具集（图片 / 视频 / 语音 / 音乐） | 已入库 |
| `8917-docx-official` | 将 Markdown 或已有内容转换为公文/正式格式 docx 的技能 | 已入库 |
| `8917-content-ingest` | 提取 URL / 网页 / X / 视频链接正文的抓取层技能 | 已入库 |

---

## Related Repository

### `8917-organization-mastery`
组织管理与方法论主仓，承载：
- D.C.E. 协议
- 组织治理框架
- 方法论与理论资产

### 与 `8917-skills` 的关系
- `8917-skills` 负责 **可执行的技能资产与能力兵工厂**
- `8917-organization-mastery` 负责 **原则、治理与方法论**

一句话说：
> `8917-skills` 解决“能力怎么落地”，`8917-organization-mastery` 解决“为什么这样做、按什么原则做”。

---

## 当前仓库结构

```text
8917-skills/
├── README.md
├── skills/
│   └── native/
│       ├── 8917-minimax-toolkit/
│       ├── 8917-docx-official/
│       └── 8917-content-ingest/
├── protocol/
├── references/
├── pending/
├── packages/   # 迁移过渡期保留
└── specs/      # 迁移过渡期保留
```

---

## 迁移说明

当前仓库仍保留早期结构：
- `packages/`
- `specs/`

它们将在迁移过程中逐步整理，不作为未来长期主结构。

---

## 协议与规范

本仓库后续将逐步引入与 skill 直接相关的公开协议与规范，放入：
- `protocol/`

例如：
- Skill Governance
- Communication Shortcodes
- Skill Design Patterns

---

_由 8917OpenClaw 维护_
