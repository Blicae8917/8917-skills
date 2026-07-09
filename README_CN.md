# 8917-skills

8917 的可复用 AI Agent 技能仓。

[English](README.md)

---

## 这是什么？

`8917-skills` 是 8917 的**可执行能力资产仓**。

这里收录的是：
- 已治理过的 skill
- 可复用的 wrapper
- 可安装、可复制、可继续扩展的能力资产

如果说 `8917-organization-mastery` 负责解释 8917 的原则、治理与方法论，
那么 `8917-skills` 负责把这些原则落成可直接使用的技能资产。

---

## 你可以用这些 skill 做什么

当前仓库中的 skill 能帮助 Agent：

- 以稳定的作者声音撰写公开长文（选题双重质检 → 证据链 → 成文 → 四层自检）
- 动态组建多视角专家团，对议题做圆桌讨论 / 对抗评审 / 分工规划（无专家库也能独立运行）

---

## 给人类看的

如果你是人类用户，这个仓库主要帮你：
- 了解 8917 有哪些 skill
- 安装或复制你需要的 skill
- 快速判断每个 skill 适合做什么
- 决定优先使用已发布 skill 还是本地仓版本

如果你最关心安装和使用，直接跳到：
- [已包含的 skill](#已包含的-skill)
- [安装方式](#安装方式)
- [快速使用示例](#快速使用示例)

---

## 给 Agent 看的

如果你准备把这个仓交给 OpenClaw 或其他 Agent 处理，Agent 应该：

1. 先读这个 README
2. 判断哪个 skill 最适合当前任务
3. 优先使用已经发布的 skill
4. 如果 skill 还没发布，再回退到 `skills/` 下的本地仓路径
5. 如果需要方法论和治理背景，再去参考 `8917-organization-mastery`

### 可直接复制给 OpenClaw / Agent 的提示语

```text
请阅读 8917-skills 仓库的 README，判断哪一个 skill 最适合我的任务，然后引导我完成安装与使用。
如果该 skill 已经发布，优先给我发布后的安装方式；
如果还没发布，就根据仓库结构告诉我如何本地使用。
如果需要方法论和治理背景，请继续参考 8917-organization-mastery。
```

### Agent 的处理规则

当 Agent 帮用户处理这个仓时，应遵循：
- 优先推荐最稳定、已发布的 skill
- 否则再使用 `skills/` 下的本地路径
- 不要把 skill 资产和 `8917-organization-mastery` 的理论文档混为一谈

---

## 已包含的 skill

| Skill | 作用 | 状态 |
|:---|:---|:---|
| `8917-write` | 叶澄风公开长文写作：选题双重质检（HKR + 资产判据）→ 证据链（依据块 + 核源 SOP）→ 四种文章原型 → 标题候选 → 四层自检（证据核验置首） | v0.1，仓内可用 |
| `8917-expert-panel` | 多视角专家团：三模式（讨论 / 评论 / 规划）× 双档执行（对话内 / Workflow 引擎）；专家来源双源自适应——本机有专家库则优先选用，没有则现场生成 persona，零外部依赖 | v2.1，仓内可用 |

> 早期入库的 `8917-minimax-toolkit`、`8917-docx-official`、`8917-content-ingest`、`8917-dce-protocol` 已于 2026-07 清理出仓（停止维护或被更强的通用工具取代）。历史版本见 git 记录；已通过 ClawHub 安装的用户不受影响。公文写作 skill 将以升级版回归。

---

## 安装方式

clone 仓库后，把需要的 skill 复制到你的 Agent skill 目录：

```bash
git clone git@github.com:Blicae8917/8917-skills.git
cp -r 8917-skills/skills/8917-write ~/.claude/skills/
cp -r 8917-skills/skills/8917-expert-panel ~/.claude/skills/
```

或者直接把仓库地址丢给你的 Agent，让它帮你安装。

### 当前发布策略

本仓中的 skill 采用：
- **按成熟度逐个发布**
- 而不是整仓打包统一发布

---

## 快速使用示例

### `8917-write`
对 Agent 说「帮我把这个项目复盘写成公众号文章」即可触发。skill 会走：选题双重质检 → 证据链取材 → 按原型成文 → 出 5-8 个候选标题 → 四层自检并输出质检报告。

路径：

```text
skills/8917-write/
```

### `8917-expert-panel`
对 Agent 说「组个专家团评一下这个方案」即可触发。skill 会：判定专家来源（本机库 / 现场生成）→ 确认名单 → 并行派遣（反锚定）→ 汇总共识与分歧。

路径：

```text
skills/8917-expert-panel/
```

---

## 仓库结构

```text
8917-skills/
├── skills/          # skill 资产主目录
│   ├── 8917-write/
│   └── 8917-expert-panel/
├── protocol/        # 仓库级 Skill 规范（SKILL_SPEC_V2）
└── README / CHANGELOG / CONTRIBUTING / LICENSE
```

### 说明
- `skills/` 是 skill 资产主目录，skill 直接住在此层
- 历史上的 `packages/`、`specs/`、`pending/`、`references/` 迁移期目录已于 2026-07 清理，详见 CHANGELOG

---

## 关联仓库

### `8917-organization-mastery`
这是 8917 的组织治理与方法论主仓。

当你想了解：
- 为什么这些 skill 要这样设计
- DCE 协议的完整理论形态
- 8917 的组织原则与治理逻辑

就应该去看这个仓。

一句话：
- `8917-skills` = 可执行能力资产
- `8917-organization-mastery` = 原则、治理与方法论

仓库地址：
- https://github.com/Blicae8917/8917-organization-mastery

---

## 贡献

参见：
- `CONTRIBUTING.md`
- `protocol/SKILL_SPEC_V2.md`

---

由 8917OpenClaw 维护。
