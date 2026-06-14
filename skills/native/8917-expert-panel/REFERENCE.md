# 8917-expert-panel · REFERENCE

SKILL.md 的执行细节。主流程见 SKILL.md,本文件在执行到对应步骤时查。

---

## §1 选角策略(第 3 步)

从 `~/.claude/agents/`(系统每会话已注入完整列表)选:轻型档 **3-5 个**,重型档 **6+**。原则:

- **互补 > 数量**:选视角差异最大的;3 个强互补 > 5 个同质。
- **贴议题**:语义直接相关的专业角色优先。
- **够用就停**:简单议题少召,跨领域才多召(并行有 token 成本)。

**按模式调整**

| 模式 | 选角侧重 |
|---|---|
| 讨论 | 立场 / 价值取向尽量**分散**:乐观派、保守派、用户视角、商业视角都有人代言,撑开光谱。 |
| 评论 | 相关专业审查者(安全 / 性能 / 架构 / 合规),**强制塞 ≥1 个唱反调角色**(怀疑者 / 批评家 / 现实核查者 / 安全架构师),并按 §4 给它**喂靶子**。 |
| 规划 | **覆盖任务每个领域**:一领域一专家,避免盲区。 |

**对抗性选角(治"回声室")**:同模型换头衔 ≈ 采样噪声。真异质性靠**构造**——选角时就让每个专家扛一个**互斥的单一目标**(如:激进派 vs 保守派、速度派 vs 安全派),而非都选"全面均衡"的角色。

**选不到时**:如实说"库里无贴合专家",建议"我直接答"或"用 N 个近似角色",不硬凑。

---

## §2 三模式输出格式(第 6 步)

### 讨论模式
```markdown
## 专家团讨论:[议题]
**[专家A]:** [立场] · [理由]
**[专家B]:** ...
### 综合
- **共识:** [一致处]
- **主要分歧:** [最关键对立 + 双方理由]
- **我的判断:** [倾向 + 为什么]
```

### 评论模式
```markdown
## 专家团评审:[方案]   ⚠️[若 missing 非空:派 N 回 M,缺 X,以下为残缺评审]
### 问题清单(按 severity)
| 严重度 | 专家 | 问题 | 建议 |
|---|---|---|---|
| 🔴 高 | ... | ... | ... |
### 唱反调专家的核心质疑
[被喂靶子那位最有力的一击]
### 我的综合判断
[必须改 / 可接受 / go-no-go]
```

### 规划模式
```markdown
## 专家团作战计划:[任务]
### 分领域规划
**[领域A — 专家]:** [关键步骤 + 风险]
### 合成总计划(带分工 + 依赖)
1. [步骤] — 负责领域 — 前置依赖
### 关键风险 / 前置条件
```

---

## §3 综合偏见护栏(第 6 步,借 council)

我既是参与者又是综合者,所以:
- 不否定某专家观点而不解释为什么。
- 某专家**改变了我的初判** → 显式说出来。
- **始终保留最强反对意见**,即使不采纳。
- ≥2 个专家一致反对我的初判 → 当真实信号,重新审视。
- verdict 前各方立场可见,不把分歧藏进结论。

---

## §4 对抗性 subagent prompt 模板(第 5 步)

通用 + 评论模式追加"喂靶子 + 互斥单目标",逼出真分歧(治回声室):

```text
你是[专家角色]。这是多视角[讨论/评审/规划]的一员。

议题:
[一句话议题]

上下文(只给必要的,不含敏感路径):
[相关片段 / 约束 / 方案]

[评论模式追加 —— 喂靶子]
主 agent 的初判是:【[把我的初判结论放这]】。
你的任务是**假设这个结论是错的**,专门找它站不住的地方,不要附和。

[互斥单目标]
你只为【[单一目标 Y,如"安全"/"可维护性"/"上线速度"]】负责。
与 Y 冲突的可读性 / 工期 / 成本,你一律牺牲——把 Y 推到极端立场。

输出:
1. 立场/判断 — 1-2 句
2. 理由 — 3 条精简 bullet
3. 最大风险 / 盲点
[评审] 4. 问题清单 — 按严重度(high/medium/low)+ 建议
[规划] 4. 你这领域的关键步骤 + 依赖

直接,不要 hedging,400 字内。
```

**铁律**:不塞完整对话历史;单轮模式各专家互不可见。

---

## §5 轻型档:对话内派遣(第 5 步)

- 用 Agent 工具,`subagent_type` = 专家英文 ID(中文叫法→英文见速查表)。
- **一条消息内并行**发起多个 Agent 调用。
- **手动 fan-in barrier**:派遣前说"派了 N 个",收齐后数"回了 M 个";`M<N` → 综合报告**顶部告警**(派 N 回 M,缺谁),给补派 / 降级 / 中止三选一。

---

## §6 重型档:Workflow 脚本模板(第 5 步)

确认名单后,把名单 + 议题 + 模式喂给下面的脚本(动态填 `EXPERTS`/`ISSUE`/`MODE`/靶子),调用 Workflow 工具。**Workflow 只派遣 + barrier + 返回结构化产出;综合不在脚本里,拿回结果后在对话内做。**

```js
export const meta = {
  name: 'expert-panel-heavy',
  description: '专家团重型档:并行派遣 N 个专家 + barrier 收齐 + 返回结构化产出(综合由对话内主 agent 做)',
  phases: [{ title: '派遣' }],
}
// 动态填:议题 / 模式 / 专家名单(agentType + 单一目标 lens)/ 评论模式的靶子结论
const ISSUE = `<议题>`
const MODE = `<讨论|评论|规划>`
const TARGET = `<评论模式:主 agent 初判结论;其他模式留空>`
const EXPERTS = [
  { agentType: 'Security Architect', lens: '安全', devil: true },
  { agentType: 'Multi-Agent Systems Architect', lens: '架构鲁棒性', devil: false },
  // …名单
]
const SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    stance:  { type: 'string' },
    reasons: { type: 'array', items: { type: 'string' } },
    risk:    { type: 'string' },
    findings:{ type: 'array', items: {
      type: 'object', additionalProperties: false,
      properties: {
        severity: { type: 'string', enum: ['high','medium','low'] },
        issue: { type: 'string' }, fix: { type: 'string' },
      }, required: ['severity','issue','fix'] } },
  }, required: ['stance','reasons','risk'],
}
const build = (e) => `你是${e.agentType}。多视角${MODE}的一员。\n议题:\n${ISSUE}\n` +
  (MODE === '评论' ? `\n主 agent 初判:【${TARGET}】。假设它是错的,专门找它站不住的地方,不要附和。\n` : '') +
  (e.devil ? `你扛唱反调角色,任务是反驳上面的初判。\n` : '') +
  `你只为【${e.lens}】负责,与之冲突的一切一律牺牲,把立场推到极端。\n` +
  `输出:立场1-2句 / 理由3条 / 最大风险${MODE==='评论' ? ' / 问题清单(severity+建议)' : ''}。直接,不hedging,400字内。`

phase('派遣')
const results = await parallel(EXPERTS.map(e => () =>
  agent(build(e), { label: `panel:${e.agentType}`, agentType: e.agentType, schema: SCHEMA })
    .then(out => ({ expert: e.agentType, lens: e.lens, out }))
    .catch(() => ({ expert: e.agentType, lens: e.lens, out: null }))
))
const panel = results.filter(r => r && r.out)
return {
  dispatched: EXPERTS.length,
  returned: panel.length,
  missing: results.filter(r => !r.out).map(r => r.expert),  // 非空=fan-in 告警
  panel,
}
```

要点:
- `agentType` 让 Workflow 的 `agent()` 用**具体 agency 专家**(从 Agent 工具同源 registry 解析),不是默认 workflow 子 agent。
- `schema` 强制结构化产出,省去解析。
- `.catch(()=>null)` + `missing` = **代码级 fan-in barrier**,谁没回来一清二楚。
- 拿回 `{dispatched, returned, missing, panel}` 后,我在对话内按 §2 + §3 综合;`missing` 非空 → 报告顶部告警。
- 多轮交锋:把第一轮 `panel` 摘要拼进第二个 phase 的 prompt(见 §8)。

---

## §7 自举评审记录(v1 → v2)

v1 用本 skill 评论模式自评,5 专家挖出 3 个 🔴,v2 已修:

| v1 的 🔴 | v2 修法 |
|---|---|
| 回声室(同模型换头衔=采样噪声) | §1 对抗性选角 + §4 喂靶子 + 互斥单目标 |
| fan-in 静默失败 | 重型档 §6 `missing` 清单 + 边界"fan-in 不静默" |
| subagent 工具越权(All tools 软约束) | 边界:评审只产判断不执行 + 攻击性专家禁实跑 + 上下文白名单(**残留**:卡仍 All tools,非沙箱,已标注) |

未了项:**A/B 盲评**(单 agent 列 N 视角 vs panel,第三方盲评独立洞见数)——大规模依赖前应做一次,验证它真值 N 倍 token。

---

## §8 "加一轮交锋"开关(默认不做)

仅用户显式要求时:
1. 第一轮各方观点汇总成一段。
2. 重新派遣,prompt 追加"其他专家观点:[...],请反驳或补充,别重复你已说的"。
3. 再综合。
重型档下做成 Workflow 第二个 phase。成本约翻倍,非重大决策不建议。
