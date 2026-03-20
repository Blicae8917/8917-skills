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

- 用 MiniMax 生成图片、视频、语音和音乐
- 把 Markdown 或已有内容转换为正式格式 `.docx` 文档
- 提取网页、X 帖子和媒体链接的可读正文
- 在高风险任务中执行 DCE（Discuss → Confirm → Execute）协议

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
4. 如果 skill 还没发布，再回退到 `skills/native/` 下的本地仓路径
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
- 否则再使用 `skills/native/` 下的本地路径
- 不要把 skill 资产和 `8917-organization-mastery` 的理论文档混为一谈

---

## 已包含的 skill

### 第一批

| Skill | 作用 | 状态 |
|:---|:---|:---|
| `8917-minimax-toolkit` | MiniMax 多模态生成工具集（图片 / 视频 / 语音 / 音乐） | 已发布到 ClawHub |
| `8917-docx-official` | 将 Markdown 或已有内容转换为公文 / 正式格式 docx 的 skill | 已发布到 ClawHub |
| `8917-content-ingest` | 提取 URL / 网页 / X / 视频链接正文的抓取层 skill | 已入库 |

### 第二批（整理中）

| Skill | 作用 | 状态 |
|:---|:---|:---|
| `8917-dce-protocol` | DCE 的 skill 化执行版本，负责 Discuss → Confirm → Execute 行为协议 | 整理中 |

---

## 安装方式

### 方式 1：安装已发布的 skill

当前已发布：

```bash
clawhub install 8917-minimax-toolkit
clawhub install 8917-docx-official
```

### 方式 2：直接使用仓库

你也可以先 clone 整个仓库，然后从 `skills/native/` 中引用需要的 skill：

```bash
git clone git@github.com:Blicae8917/8917-skills.git
cd 8917-skills
```

### 当前发布策略

本仓中的 skill 采用：
- **按成熟度逐个发布**
- 而不是整仓打包统一发布

---

## 快速使用示例

### `8917-minimax-toolkit`
使用 MiniMax 统一生成多模态内容：

```bash
clawhub install 8917-minimax-toolkit
```

### `8917-docx-official`
安装正式文档转换 skill：

```bash
clawhub install 8917-docx-official
```

### `8917-content-ingest`
用于先从链接中提取干净正文，再交给总结、归档或分析流程。

路径：

```text
skills/native/8917-content-ingest/
```

### `8917-dce-protocol`
用于高风险任务中的 DCE 行为协议控制。

路径：

```text
skills/native/8917-dce-protocol/
```

---

## 仓库结构

```text
8917-skills/
├── skills/
│   └── native/
├── protocol/
├── references/
├── pending/
├── packages/   # 迁移期 legacy 内容
└── specs/      # 历史规范文件
```

### 说明
- `skills/native/` 是当前 skill 资产的主目录
- `packages/` 和 `specs/` 是迁移期保留内容，不是长期主结构

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
