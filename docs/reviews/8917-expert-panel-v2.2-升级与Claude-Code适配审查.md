# 8917-expert-panel v2.2 升级与 Claude Code 适配审查

> 日期：2026-07-16
> 审查对象：`skills/8917-expert-panel/`
> 源码真相源：`skills/8917-expert-panel`
> 当前状态：功能改造和本地测试完成；Claude Code 适配复核进行中；尚未 commit / push / 发布。

## 1. 这次要解决什么

旧版把“本机存在某个专家库目录”近似当成“当前宿主”，并偏向 Claude Code 的路径和卡片格式。在 Claude Code 与 Codex 同机共存时，这会造成三类问题：

1. 可能从错误宿主的专家库选卡；
2. 找到卡片不等于当前派遣 API 能原生实例化该卡片；
3. 轻量讨论、可审计运行和可复现运行之间缺少真实能力门槛，容易把降级执行描述成完整成功。

v2.2 的目标不是单纯“多叫几个 Agent”，而是建立一条可解释、可对账、按宿主原生能力运行的专家团编排契约。

## 2. 路径模型

### 2.1 Skill 安装入口

同一个源码真相源，通过两个宿主专属 Junction 暴露：

| 宿主 | 安装入口 | 目标 | 2026-07-16 状态 |
|---|---|---|---|
| Claude Code | `~/.claude/skills/8917-expert-panel` | 仓内源码目录 | 已安装 |
| Codex | `~/.codex/skills/8917-expert-panel` | 仓内源码目录 | 已安装 |

两条入口的 `SKILL.md` SHA-256 均为：

```text
CEC12A529F6CDD9CBD13E92537009F6692FFA82E6EA7733DA72541E61A19FC8D
```

此前的共享入口 `~/.agents/skills/8917-expert-panel` 已迁移掉。真实 smoke test 表明，当前 Codex 能从共享入口发现 Skill，但 Claude Code 2.1.209 不会把它解析为 slash skill；因此不能把 `~/.agents/skills` 当成两个宿主都支持的安装标准。

### 2.2 专家卡来源

Skill 安装入口和专家卡来源是两个不同概念。运行时先识别当前宿主，再只读取该宿主自己的专家库：

| 当前宿主 | 专家库 | 卡片格式 |
|---|---|---|
| Claude Code | `~/.claude/agents/*.md` | YAML frontmatter + Markdown |
| Codex | `~/.codex/agents/*.toml` | TOML |

禁止通过“哪个目录存在”猜测宿主，也禁止默认跨宿主借用另一套卡片。

## 3. 升级思路

### 3.1 宿主感知路由

把宿主身份作为显式运行时输入。Claude Code 只发现 Claude 卡，Codex 只发现 Codex 卡。同机存在两套专家库是正常状态，不是路由依据。

### 3.2 拆分发现、解析和调用

将专家卡处理拆为三个阶段：

- 发现：枚举当前宿主原生目录；
- 解析：提取紧凑元数据并校验坏卡、重名；
- 调用：根据当前工具是否支持 typed agent，选择原生调用、persona 注入或现场生成。

这样避免把“文件可读”误报成“原生 Agent 可调用”。

### 3.3 统一身份但保留原生身份

卡片内部 `name` 生成跨宿主稳定的 `canonical_id`；同时保留宿主文件 stem 形成的 `native_id`、原始路径和 SHA-256。`canonical_id` 用于选角与对账，`native_id` 只用于宿主明确支持的原生派遣。

### 3.4 角色投影而非整卡灌入

generic spawn 时，只投影与本轮议题相关的职责、关键约束和单一 lens，并标记为 `persona-injected`。若本地卡语义不贴合，现场生成 persona，并标记为 `generated`。不把无关长卡、工具指令或行业模板整体塞入上下文。

### 3.5 能力协商与动态并发

派遣前探测：typed agent、generic spawn、空闲槽位、隔离上下文、schema、timeout/cancel、trace、snapshot 和可靠执行器。专家数量与真实并发数分离；例如总槽位为 4、主 Agent 占 1 时，每波最多派 3 位。

### 3.6 轻型与重型分档

- 轻型：会话内单轮讨论/评论/规划，主 Agent 维护 ledger；
- 可审计重型：必须持久化 manifest 和 trace；
- 可复现重型：在可审计基础上，还必须有授权的输入/上下文安全快照引用、hash、模型参数和执行器版本。

缺少能力时明确阻断；只有用户同意，才可以降为轻型，且不得继续宣称“可审计”或“可复现”。

### 3.7 Fan-in 与状态真值

每个分支有稳定 `branch_id`，每次尝试追加到 `attempts[]`，失败不得覆盖。barrier 汇总 success / partial / failed / timed_out / cancelled；运行级状态由分支终态和降级原因推导，禁止吞错或把残缺结果包装成完整专家团结论。

## 4. 实现落点

| 文件 | 作用 |
|---|---|
| `skills/8917-expert-panel/SKILL.md` | 主流程、宿主路由、能力门槛、七步编排、边界和完成标准 |
| `skills/8917-expert-panel/references/runtime-contract.md` | 统一卡片模型、schema、派遣 prompt、manifest、状态机和验证矩阵 |
| `skills/8917-expert-panel/scripts/expert_registry.py` | 发现/解析 Claude Markdown 与 Codex TOML 卡片，输出紧凑注册表 |
| `skills/8917-expert-panel/scripts/run_contract.py` | 重型能力 gate、manifest 字段与最终状态一致性校验 |
| `tests/test_expert_panel_registry.py` | 注册表正常、坏卡、重名、查询和 resolve 测试 |
| `tests/test_expert_panel_contract.py` | 能力 gate、attempt 历史、审计/复现字段和状态真值测试 |
| `README.md` / `README_CN.md` | 明确宿主专属 Skill 安装入口与宿主专属专家库路径 |

## 5. 已完成验证

- 初版 Python unittest：15/15 通过；Claude 审查修正后扩充为 17/17 通过；
- Claude Code 原生专家库：254 张卡可解析，invalid=0；
- Codex 原生专家库：254 张卡可解析，invalid=0；
- 两侧 duplicate `canonical_id`=0；
- `py_compile` 通过；
- frontmatter 等价校验通过；
- Skill 内相对链接检查通过；
- 旧契约/过时表述扫描通过；
- `git diff --check` 通过；
- Codex 前向 smoke：选择 Codex 卡、persona 注入、3 个空闲槽位分两波；缺少持久 trace 时正确阻断重型档；
- 独立 Codex Code Reviewer 在两个 blocker 修正后给出 APPROVE。

官方 `skill-creator` 的 `quick_validate.py` 因系统 Python 缺少 PyYAML 未直接执行；已经用等价的 frontmatter、链接、脚本、单测和真实注册表检查覆盖，但此项仍应在带 PyYAML 的发布环境补跑。

## 6. Claude Code 复核任务

请 Claude Code 以只读方式检查源码和本文件，不修改、不 commit、不 push，重点回答：

1. Claude Code 2.1.209 能否从 `~/.claude/skills/8917-expert-panel` 稳定发现并加载该 Skill？
2. `~/.claude/agents/*.md` 的发现、YAML frontmatter 解析、内部 `name`、文件 stem `native_id` 的约定是否符合当前 Claude Code？
3. Claude Code 当前原生派遣 API 是否真能按文件 stem 激活 typed subagent？准确工具名、参数名和限制是什么？
4. Skill 声明的 typed agent、上下文隔离、只读权限、并发槽位、timeout/cancel、结构化 schema、trace/snapshot 等能力，哪些是硬保证，哪些只是 prompt 软约束？
5. `Workflow 或等价执行器`、可审计 manifest、可复现安全快照在 Claude Code 当前环境是否有真实落点？若没有，重型档是否已经正确阻断？
6. Windows Junction、路径引用、Python 脚本启动方式和 UTF-8 处理是否兼容？
7. 是否存在与 Claude Code 的 Skill / Agent 发现规则、权限系统或上下文继承机制冲突的表述？
8. 给出最终 `GO / GO-WITH-FIXES / NO-GO`，并按 blocker / high / medium / low 列出证据、影响和最小修正建议。

建议至少执行以下只读场景：

- slash-skill 发现；
- Claude 专家库全量 list 与单卡 resolve；
- 3 人轻型评论模式；
- 1 个分支失败或 schema 不合格；
- 无贴合卡时 generated persona；
- 请求重型但没有 trace persistence；
- 可审计与可复现 gate 的差异。

## 7. Claude Code 审查结果

审查环境：Claude Code 2.1.209，Sonnet 5，后台只读会话 `cb580a84`。Claude 读取了 Skill、运行时契约、两个脚本和本审查文档；文件写入、commit、push 和子 Agent 派遣均未授权。

初审结论：**GO-WITH-FIXES**。

| 级别 | 发现 | 结论与处理 |
|---|---|---|
| Blocker | Claude Code 原生 typed agent 的 `subagent_type` 按 frontmatter `name` 匹配，不按文件 stem 匹配；旧契约把 `native_id` 当调用键会派遣失败，并使 manifest 记录失真 | 已修正：`native_id` 只作来源标识；新增必填 `dispatch_key` 记录真实调用值；Claude 使用 `display_name`，其他宿主必须按真实工具 schema 确认 |
| High | Workflow 工具存在用户显式 opt-in 门禁；旧能力表只判断“工具存在” | 已修正：新增 `orchestration_opt_in` 重型 gate；没有明确授权时重型档阻断或经用户同意降级 |
| Medium | Claude 本轮因执行权限受限，未独立复跑 254 卡重名检查 | 已由 Codex 主 Agent 补跑：Claude/Codex 均为 count=254、invalid=0、duplicate canonical_id=0、duplicate display_name=0 |
| Medium | Claude 原生 Agent 无逐调用硬 timeout；`TaskStop` 依赖后台任务 id，属于软约束 | 已修正：Claude 下除非外层执行器提供硬超时和可靠取消，否则 `timeout_cancel=false`，不得进入重型档 |

Claude 确认兼容的部分：

- `~/.claude/skills/8917-expert-panel` Junction 可被 Claude Code 发现；
- 254 张 `~/.claude/agents/*.md` 卡的 frontmatter 格式与解析器一致；
- Claude Agent 默认新上下文符合反锚定隔离目标；
- Claude Agent 没有原生 schema 参数，契约中的“主 Agent 手动校验、失败可重试一次”降级路径合理；
- `run_contract.py` 的状态推导、attempt 历史和 hash 校验内部一致。

另有一项真实环境观察：Claude Code 启动时提示 Agent descriptions 约 16k tokens，超过 15k 上限。因此“磁盘可解析 254 张卡”不等于“本轮 typed Agent 列表暴露 254 张卡”。契约已补充：以派遣工具本轮暴露的 subagent 类型为准；不在列表中的卡必须走 `persona-injected`。

Claude 初审未实际派遣一张 typed 卡验证调用失败/成功，也未复核 Codex 侧。前者的工具 schema 结论已落为保守规则；后者由本轮 Codex 实机注册表与 17 项测试覆盖。

### 7.1 修正后闭环复核

Claude Code 使用独立只读会话 `a0260f1a` 复核修正后的 `SKILL.md`、运行时契约、校验脚本、测试和本节记录，最终结论：**APPROVE**。

- B1：Closed。`native_id` 与 `dispatch_key` 语义已分离，roster/branch 均强制记录真实派遣键，并有缺失校验测试；
- H1：Closed。`orchestration_opt_in` 已进入重型必需能力，并有阻断测试；
- M1：本机 254 卡重名检查结果被接受为一次性环境证据；未来可把真实注册表计数/重名固化为可选环境回归门禁，不阻塞本次；
- M2：Closed。Claude 无硬 timeout 时必须把 `timeout_cancel` 视为 false，重型 gate 会阻断；
- 15k Agent 描述上限：处理合理。当前属于明确披露的 prompt/运行时软约束，没有伪装成硬保证。

### 7.2 Claude Fable 5 独立复核（2026-07-16）

Claude Fable 5 在独立只读会话中复现了发布前验证：17/17 测试通过；真实 Claude 专家库 `count=254`、`invalid=0`、`duplicate canonical_id=0`、`duplicate display_name=0`；仓内源码、Claude Code 入口和 Codex 入口三处 `SKILL.md` SHA-256 一致；两个宿主 Junction 的目标均指向仓内源码，目录树逐文件哈希一致。

本轮还用正反派遣实验闭合了 §7 中“未实际派遣 typed 卡”的缺口：

- `subagent_type="Reality Checker"`（frontmatter `name`）派遣成功；
- `subagent_type="testing-reality-checker"`（文件 stem）返回 `Agent type not found`，且错误信息枚举了本轮运行时暴露的全部 agent 类型。

因此，Claude Code 下 `dispatch_key=display_name` 已由保守规则升级为实测事实。独立复核维持 **APPROVE / GO**。

## 8. 发布判定

当前判定：**功能完成、两轮 Claude 复核（Sonnet 5 闭环 + Fable 5 独立实测）均 APPROVE、18/18 测试通过、已安装到两个宿主专属入口，但尚未 commit / push / 正式发布**。代码与本机安装已就绪；是否提交和发布由用户决定。
