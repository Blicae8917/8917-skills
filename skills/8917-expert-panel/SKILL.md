---
name: 8917-expert-panel
description: 动态组建临时专家团，对议题做讨论、评论或规划。用于“组个专家团”“多视角看看”“找几个专家评一下”“让专家们讨论/规划”等请求；按当前宿主分别使用 Claude Code 或 Codex 原生专家库，语义不匹配时生成 persona，经用户确认名单后反锚定派遣，并透明报告失败、降级、共识与分歧。
---

# 8917-expert-panel

## 定位

编排型 + Pipeline skill。固定执行链：

`识别宿主 → 发现并筛选专家 → 确认名单 → 反锚定派遣 → barrier 收集 → 主 Agent 综合`

支持三种模式：

- **讨论**：展示立场光谱、共识与分歧。
- **评论**：对抗式评审，必须有至少一位唱反调专家。
- **规划**：分领域产出步骤、依赖、负责人和风险。

方法来源：council/ECC 的反锚定与综合护栏、agency-agents 的角色卡思想。详细运行时契约、schema、prompt 和验证矩阵见 [references/runtime-contract.md](references/runtime-contract.md)。

## 运行时铁律

1. **先识别当前宿主，不用目录存在性猜宿主。** 一台机器可以同时安装两套专家库。
2. **只走当前宿主原生库。** Claude Code 不默认借 Codex 卡，Codex 不默认借 Claude Code 卡。
3. **分开判断发现、解析、调用。** 找到卡片不等于派遣 API 能按卡片原生实例化。
4. **Workflow 或其他执行器只负责可靠派遣与 barrier；综合永远由主 Agent 完成。**
5. **能力不足时不伪装。** 用户要求留痕、可复现或多轮交锋，而环境无法满足时，说明缺失能力并暂停重型档；不要静默降级后声称已满足。

## 宿主原生专家库

| 当前宿主 | 原生路径 | 格式 |
|---|---|---|
| Claude Code | `~/.claude/agents/*.md` | YAML frontmatter + Markdown |
| Codex | `~/.codex/agents/*.toml` | TOML |

从当前 Skill 目录运行注册表脚本，只读取紧凑元数据：

```bash
python scripts/expert_registry.py list --host codex --query "multi agent"
python scripts/expert_registry.py list --host claude-code --query "security"
```

确定选角后再解析单张卡；不要把整个专家库的正文全部塞进上下文：

```bash
python scripts/expert_registry.py resolve \
  --host codex \
  --name "Multi-Agent Systems Architect" \
  --include-instructions
```

使用卡片内部 `name` 生成统一 `canonical_id`，保留宿主自己的 `native_id`、路径和 SHA-256。`native_id` 只表示宿主文件 stem，用于来源对账，不自动等于派遣 API 的调用键。

## 派遣能力探测

选档前检查当前工具实际支持什么：

- 是否支持指定 typed agent / subagent type。
- 是否只有 generic spawn。
- 可用并发槽位（扣除主 Agent）。
- 是否支持隔离上下文、结构化 schema、timeout/cancel、重试和 trace。
- 是否存在 Workflow 或具备等价能力的可靠执行器。

把“工具存在”和“本轮获准调用”分开判断。若 Workflow 或等价编排器要求用户显式 opt-in，而用户本轮没有明确要求 workflow/多 Agent 编排，则 `workflow_or_equivalent` 必须按 `false` 处理。

`typed_agent=true` 也不表示磁盘上每张卡都已被运行时注册。以派遣工具本轮暴露的可用 subagent 类型为最终真相源；如果 Claude Code 因 Agent 描述总量上限没有暴露某张卡，即使文件可解析，也只能走 `persona-injected`，不得尝试伪原生调用。

重型档把能力表写成临时 JSON 后先跑 gate。可审计重型档省略 `--require-reproducible`；需要安全快照复跑时才增加该参数。只有用户明确同意时才加 `--allow-downgrade`：

```bash
python scripts/run_contract.py gate \
  --capabilities <capabilities.json> \
  --requested-tier heavy

# 可复现重型档额外增加：--require-reproducible
```

调用分三档：

1. **原生调用**：派遣 API 支持 typed agent，使用该宿主 API 真实要求的 `dispatch_key`。Claude Code 2.1.209 的 `subagent_type` 按卡片 frontmatter `name`（即 `display_name`）匹配，不按文件 stem 匹配；其他宿主必须先从实际工具 schema 确认，不能把 `native_id` 当成通用调用键。
2. **角色注入**：只有 generic spawn，注入选定卡片的角色投影，并明确标注 `persona-injected`。
3. **现场生成**：无合适原生卡，生成角色名、单一 lens、立场偏置和是否唱反调。

本地有卡也不能硬选。语义贴合度不足时，生成 persona 比无关的长卡更可靠。

## 双档执行

| | 轻型档（默认） | 重型档 |
|---|---|---|
| 适用 | 即时、小规模、单轮 | 留痕、可复现、多轮、较大规模 |
| 逻辑专家数 | 3–5，够用就停 | 通常 6+，但由议题和能力决定 |
| 并发 | 按可用槽位并发，必要时分波 | 可靠执行器限流调度 |
| barrier | 主 Agent 维护 ledger | 执行器维护 ledger，主 Agent 复核 |
| trace | 会话内摘要 | 版本化运行 manifest |

专家数量不决定真实并发数。例如宿主共 4 个槽且主 Agent 占 1 个时，每波最多派 3 位。

命中任一条件时尝试重型档：用户明确要求留痕/可复现/重大决策、多轮交锋、或规模超过当前轻型并发能力。若缺少重型能力，给出缺失项和可选方案：减少范围走轻型、分波但不承诺持久 trace、或暂停等待合适执行器。

## 七步流程

1. **抽议题**：一句话锁定决定、评审或规划什么，以及成功标准。
2. **定模式与选档**：按用户要求或议题推断，并说明依据和环境能力。
3. **选专家**：从当前宿主原生库筛选；不足时生成 persona。互补优先，评论模式必须含唱反调角色。
4. **确认名单**：列出专家、来源、调用方式、lens 和理由，等待用户增删拍板。不得跳过。
5. **反锚定派遣**：派遣前写下主 Agent 初判；每位专家只拿议题、必要上下文、单一角色和输出 schema。不得传完整对话历史。
6. **Barrier 收集**：声明派出 N 位、分几波；收集后声明成功 M 位以及 failed/timed_out/cancelled 明细。主 Agent 校验 schema，必要时最多重试一次。
7. **综合**：先展示各专家原始立场，再给共识、分歧、最强反对意见和主 Agent 判断。说明哪些观点改变了初判。

## 角色投影

generic spawn 时不要默认注入整张长卡。只投影：

- 专家显示名与卡片 SHA-256。
- 与议题直接相关的职责和 2–4 条关键约束。
- 一个互斥的单一目标 lens。
- 本轮禁止动作和结构化输出要求。

若完整卡片中存在与本轮无关的工具命令、行业模板或输出格式，排除它们。不得静默截断本轮必需约束。

## 不可违反的边界

- **评审专家只产判断，不执行修改。** 若运行时支持工具权限，强制只读或禁用工具；不支持时明确告知这只是软约束。
- **fan-in 不静默。** 任一分支失败都要在报告顶部说明，禁止把残缺结果伪装为完整专家团结论。
- **隔离上下文。** Codex 派生线程显式使用无历史继承的方式；其他宿主采用等价设置。
- **不派攻击性安全角色做真实探测、抓取或改动。** 只输出风险描述和缓解建议。
- **敏感信息白名单化。** 不向专家传 `.env`、凭据、客户原始数据或无关私密路径。
- **不自动 push、发布、改生产或替用户做不可逆决策。**
- **不伪造专家来源。** 报告中区分 `native`、`persona-injected`、`generated`。

## 完成标准

一次合格的专家团执行必须同时满足：名单已确认、来源和调用方式可见、派回数量对账、失败原因可见、分歧未隐藏、主 Agent 给出独立判断。

重型档还必须用下列命令验证 manifest：

```bash
python scripts/run_contract.py validate --manifest <run-manifest.json>
```

只有审计字段完整时才称“可审计”；只有输入/上下文安全快照引用、模型参数和执行器版本都可重建时才称“可复现”。缺一项就不能声称“可复现专家评审完成”。
