# 8917-expert-panel · 运行时契约

本文件提供 `SKILL.md` 执行到选角、派遣、barrier、综合或验证时所需的细节。

## 目录

1. [统一专家卡模型](#1-统一专家卡模型)
2. [能力探测与降级](#2-能力探测与降级)
3. [选角与角色投影](#3-选角与角色投影)
4. [三模式输出契约](#4-三模式输出契约)
5. [派遣 prompt](#5-派遣-prompt)
6. [Barrier ledger 与重型执行](#6-barrier-ledger-与重型执行)
7. [综合护栏与输出](#7-综合护栏与输出)
8. [验证矩阵与增益指标](#8-验证矩阵与增益指标)

## 1. 统一专家卡模型

注册表脚本把宿主不同格式归一为：

```json
{
  "canonical_id": "multi-agent-systems-architect",
  "native_id": "multi-agent-systems-architect",
  "display_name": "Multi-Agent Systems Architect",
  "description": "...",
  "host": "codex",
  "card_path": "...",
  "sha256": "..."
}
```

`canonical_id` 来自卡片内部 `name`，只用于选角和对账；`native_id` 是当前宿主文件 stem，只表示卡片来源。真正派遣时另行记录 `dispatch_key`：Claude Code 2.1.209 的 `Agent.subagent_type` 使用 frontmatter `name`（即 `display_name`）原样值，不使用文件 stem；其他宿主必须按本轮工具 schema 确认调用键。当前 Codex 只有 generic spawn 时，不得把 TOML 文件 stem 宣称为 typed 调用键。

注册表只枚举当前宿主的用户级专家库。Claude Code 运行时暴露列表还可能包含插件命名空间 agent（如 `feature-dev:code-reviewer`）和内置类型（如 `general-purpose`），因此注册表集合与运行时暴露集合双向不相等：选角来自注册表，可派遣性只认本轮运行时列表。

### 注册表命令

```bash
# 紧凑检索；默认不返回长 instructions
python scripts/expert_registry.py list --host codex --query "workflow"

# 精确解析选中的卡
python scripts/expert_registry.py resolve \
  --host claude-code \
  --name "Workflow Architect" \
  --include-instructions
```

如果 `invalid` 非空，报告坏卡数量和路径，不把坏卡当作“无匹配专家”。如果同名解析得到多张卡，停止并让用户或主 Agent 消歧。

## 2. 能力探测与降级

选档前构造会话内能力表：

```json
{
  "host": "codex",
  "typed_agent": false,
  "generic_spawn": true,
  "free_slots": 3,
  "isolated_context": true,
  "schema_enforced": false,
  "timeout_cancel": true,
  "trace_persistence": false,
  "snapshot_persistence": false,
  "workflow_or_equivalent": false,
  "orchestration_opt_in": false
}
```

判断规则：

- `typed_agent=false`：不得声称“原生激活专家”；使用 `persona-injected`。
- 卡片文件存在但其 `dispatch_key` 不在本轮派遣工具暴露的 subagent 类型列表中：视为不可原生调用，改用 `persona-injected`。Claude Code 的 Agent 描述 token 上限可能让“磁盘发现数”大于“运行时注册数”。
- `isolated_context=false`：不得声称满足反锚定；先解决上下文继承。
- `workflow_or_equivalent=true` 但本轮用户没有满足该执行器要求的显式 opt-in：按 `false` 处理。工具存在不等于本轮有权调用。
- Claude Code 原生 Agent 没有逐次调用的硬 timeout 参数；除非外层执行器能强制超时并可靠取消，否则 `timeout_cancel=false`。`run_in_background` 加人工 `TaskStop` 只能标记为软约束，不能当成重型档的硬保证。
- `trace_persistence=false`：任何重型档都必须阻断；没有持久 manifest 就不能称为可审计重型档。
- `snapshot_persistence=false`：最多称为可审计，不能称为可复现。
- `free_slots<N`：分波执行并在名单确认时说明波次。
- `schema_enforced=false`：主 Agent 在 barrier 后手动校验，格式错视为 partial，可定向重试一次。

Claude Code 可选探针：用一个已知无效的 `subagent_type` 发起一次最小派遣。`Agent type not found` 错误会枚举本轮真实注册的完整 agent 类型列表，可作为 `typed_agent` 暴露集合的权威探测。该探针消耗一次报错往返，轻型档可省略；省略时只能把派遣工具明确暴露的类型视为可调用，不得从磁盘注册表反推。

把能力表保存为临时 JSON 后执行：

```bash
python scripts/run_contract.py gate \
  --capabilities <capabilities.json> \
  --requested-tier heavy

# 可复现重型档额外增加：--require-reproducible
```

返回 `blocked` 时停止；只有用户明确接受会话内降级后，才重新运行并增加 `--allow-downgrade`。

## 3. 选角与角色投影

### 选角原则

- 互补大于数量；3 个互斥 lens 胜过 5 个“全面均衡”。
- 评论模式强制至少一个唱反调角色。
- 规划模式覆盖每个任务领域，但不要让专家承担最终总计划综合。
- 专家卡语义不贴合时生成 persona，不因“本地库优先”硬凑。

### 推荐名单格式

```text
建议召集：
1. Multi-Agent Systems Architect
   来源：Codex 原生卡
   调用：persona-injected（当前 API 无 typed agent）
   lens：失败恢复与可观测性
   理由：覆盖 fan-in 和 trace 风险
```

### 角色投影格式

```text
ROLE: <display_name>
CARD_SHA256: <sha256>
SOURCE: <native|persona-injected|generated>
LENS: <单一目标>

RELEVANT ROLE RULES:
- <从卡中提取的相关职责>
- <从卡中提取的关键约束，最多 4 条>

NOT RESPONSIBLE FOR:
- 综合其他专家
- 修改文件、调用外部系统或执行生产动作
```

不要复制与议题无关的长代码示例、行业模板和工具命令。

## 4. 三模式输出契约

### 讨论

```json
{
  "stance": "立场",
  "reasons": ["理由1", "理由2", "理由3"],
  "assumptions": ["关键假设"],
  "risk": "最大风险"
}
```

### 评论

```json
{
  "verdict": "pass|needs-work|no-go",
  "reasons": ["理由1", "理由2", "理由3"],
  "risk": "最大风险",
  "findings": [
    {
      "severity": "high|medium|low",
      "issue": "问题",
      "evidence": "证据",
      "fix": "建议"
    }
  ]
}
```

### 规划

```json
{
  "goal": "本领域目标",
  "steps": [
    {
      "step": "动作",
      "owner_domain": "负责领域",
      "depends_on": ["前置依赖"],
      "verification": "验证方式"
    }
  ],
  "risk": "最大风险",
  "prerequisites": ["前置条件"]
}
```

所有模式的结构化内容只是专家原料；最终 verdict 仍由主 Agent 给出。

## 5. 派遣 prompt

```text
你是 <专家角色>，是本轮多视角<讨论|评论|规划>的一员。

议题：
<一句话议题与成功标准>

必要上下文：
<只给相关事实和约束，不含完整对话历史或敏感路径>

角色投影：
<按 §3 注入>

你只为【<单一 lens>】负责。不要尝试全面平衡，也不要综合其他专家。

<评论模式且为唱反调角色时追加>
主 Agent 初判是：【<初判>】。假设它是错的，找出最强反例，不要附和。

边界：
- 只读分析；不修改文件，不调用外部系统，不派发其他 Agent。
- 输出必须符合本模式 schema。
- 控制在 700 字内，直接给判断。
```

若运行时无法强制只读，派遣前向用户披露“工具限制为软约束”。

## 6. Barrier ledger 与重型执行

每次运行维护一个版本化 manifest。下面仅展示关键形状；完整字段由 `scripts/run_contract.py` 校验：

```json
{
  "schema_version": "1.0",
  "output_schema_version": "review-1.0",
  "run_id": "uuid",
  "host": "codex",
  "mode": "review",
  "tier": "heavy",
  "trace_level": "audit|reproducible",
  "skill_sha256": "...",
  "input_sha256": "...",
  "context_sha256": "...",
  "input_snapshot_ref": "secure://...",
  "context_snapshot_ref": "secure://...",
  "model": {"id": "...", "parameters": {}},
  "executor": {"name": "...", "version": "..."},
  "persistence": {"location": "secure://..."},
  "requested": 3,
  "waves": 1,
  "degraded_reasons": [],
  "roster": [
    {
      "canonical_id": "reality-checker",
      "native_id": "reality-checker",
      "dispatch_key": "general-purpose",
      "source": "persona-injected",
      "card_sha256": "...",
      "role_projection_sha256": "..."
    }
  ],
  "branches": [
    {
      "branch_id": "branch-1",
      "expert": "Reality Checker",
      "source": "persona-injected",
      "native_id": "reality-checker",
      "dispatch_key": "general-purpose",
      "card_sha256": "...",
      "role_projection_sha256": "...",
      "attempts": [
        {
          "attempt": 1,
          "prompt_sha256": "...",
          "status": "partial",
          "latency_ms": 1200,
          "error": "schema validation failed",
          "output": {}
        },
        {
          "attempt": 2,
          "prompt_sha256": "...",
          "status": "success",
          "latency_ms": 900,
          "error": null,
          "output": {}
        }
      ],
      "final_status": "success"
    }
  ],
  "final_status": "complete|partial|degraded|failed|cancelled"
}
```

### 执行状态机

```text
detect → resolve → confirm → dispatch waves → collect → validate
                                            ├─ retry once
                                            └─ terminal status
terminal branches → barrier → synthesize
```

执行器要求：

1. 每个分支有稳定 `branch_id` 和明确 timeout；永久挂起不能阻塞整团。
2. 使用 settled 结果，保留错误类型；不要 `.catch(() => null)` 吞错。
3. 每次尝试追加到 `attempts[]`，不得覆盖失败历史；schema 失败记 `partial`，最多定向重试一次。
4. 用户中止或新请求覆盖当前任务时，记录 `cancelled`。
5. barrier 返回所有分支终态，而不只返回 `missing` 名单。

运行级状态按下表推导：

| 分支结果 | 运行级 `final_status` |
|---|---|
| 全部 success，且无降级原因 | `complete` |
| 有 success，也有其他终态 | `partial` |
| 有 success，且记录了能力降级 | `degraded` |
| 全部分支 cancelled | `cancelled` |
| 无 success，且不全是 cancelled | `failed` |

用以下命令验证字段、attempt 历史和状态真值：

```bash
python scripts/run_contract.py validate --manifest <run-manifest.json>
```

`trace_level=audit` 只承诺可审计：保存输入/上下文 hash、名单、卡片与角色投影 hash、schema 版本、模型参数和执行器版本。`trace_level=reproducible` 还必须提供经过授权的输入与上下文安全快照引用。敏感上下文无法安全持久化时，应降为“可审计”，不得声称“可复现”。

## 7. 综合护栏与输出

主 Agent 既是参与者又是综合者，因此：

- 派遣前先写下初判、最强理由和最大风险。
- verdict 前展示每位成功专家的原始立场。
- 不无理由否定专家；若专家改变初判，明确指出。
- 始终保留最强反对意见，即使不采纳。
- 两位以上专家一致反对初判时，视为真实信号并重新审视。
- `final_status != complete` 时，在报告顶部写明派 N、成功 M、其余终态和影响。

评论模式紧凑输出：

```markdown
## 专家团评审：<议题>
运行状态：派 N / 成功 M / partial P / failed F / timeout T

### 各方立场
- <专家与来源>：<立场>

### 问题清单
| 严重度 | 专家 | 问题 | 证据 | 建议 |

### 最强反对意见
<唱反调专家最有力的一击>

### 我的判断
<必须改 / 可接受 / go-no-go；说明是否改变初判>
```

## 8. 验证矩阵与增益指标

### 最小 smoke

Claude Code 与 Codex 各验证：

1. 原生目录可解析，内部 `name` 与宿主 `native_id` 同时保留。
2. 3 人评论模式完整返回。
3. 1 人失败或超时，ledger 和顶部告警准确。
4. 无本地卡时生成 persona，并正确标注来源。
5. 请求重型但环境无 trace 时明确阻断或降级征得用户同意。
6. 专家不继承完整对话历史。

### A/B 盲测

用至少 6 个固定议题比较：

- 单 Agent 直接列多视角。
- 现场生成 persona panel。
- 完整专家卡 panel。
- 角色投影 panel。

核心指标：

- 经人工验证的独立新发现数 / 1000 output tokens。
- 高严重度发现准确率。
- 分歧多样性，而非同义改写数量。
- 完整返回率、P95 延迟和总 token。

建议门槛：相对单 Agent，独立有效发现/千 token 提升至少 25%，且高严重度准确率不下降，才把专家库 panel 视为有证据的增强。
