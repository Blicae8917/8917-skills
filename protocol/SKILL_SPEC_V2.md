# 8917 Skill Spec v2

> 这是 `8917-skills` 当前现行的技能规范。
> 旧版规范见：`../specs/skill-spec-v1.md`（历史版本，仅供迁移参考）。

---

## 一、目标

本规范用于定义：
- `8917-skills` 仓库中 skill 的推荐目录结构
- `SKILL.md` 的最小必要字段
- 类型层与模式层
- external / wrapper / native 的基本判断思路

本规范优先服务于：
- 可执行 skill 资产
- 对外可发布 skill
- 8917 主权技能资产

---

## 二、推荐目录结构

```text
skill-name/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

### 说明
- `SKILL.md`：技能入口与核心流程
- `scripts/`：确定性执行脚本
- `references/`：按需读取的说明、规则、API 信息
- `assets/`：模板、静态资源、示例素材

### 默认不建议
以下内容不是 skill 的长期主结构标配：
- `README.md`
- `CHANGELOG.md`
- `INSTALLATION_GUIDE.md`
- `src/`
- `tests/`

如确有必要，应在仓库级别统一管理，而不是默认塞进每个 skill 目录。

---

## 三、SKILL.md frontmatter

### 必填字段
```yaml
---
name: skill-name
description: 一句话说明 skill 做什么，以及何时触发
---
```

### 可选字段
```yaml
metadata:
```

### 默认不建议字段
除非有特别明确的发布理由，默认不建议在 `SKILL.md` frontmatter 中加入：
- `version`
- `author`
- `license`
- `compatibility`

---

## 四、类型层（治理层）

每个 skill 都应明确自己属于以下哪一类：

### 1. 规范型
回答“怎么做才对”
- 规则
- 标准
- 方法论
- 守门与判断框架

### 2. 工具型
回答“具体怎么干”
- 明确输入输出
- 依赖脚本或 API
- 解决单一能力问题

### 3. 编排型
回答“多个能力如何串起来”
- 调度多个子能力
- 控制步骤顺序
- 设置确认点与断点恢复

---

## 五、模式层（设计层）

每个 skill 还应明确主设计模式：

### 1. Tool Wrapper
给工具或外部能力包一层可执行包装。

### 2. Generator
根据模板、规则或结构生成稳定产物。

### 3. Reviewer
根据 checklist / rubric 审查和判断。

### 4. Inversion
先提问、澄清、收集条件，再执行。

### 5. Pipeline
严格按步骤推进，控制确认点和上下游关系。

---

## 六、归属判断

处理一个 skill 时，默认按以下顺序判断：

1. 现有 native 是否已覆盖
2. 现有 external 是否已覆盖
3. 是否只需要在 external 外包一层 wrapper
4. 只有 wrapper 不足且已形成明确主权价值时，才进入 native

---

## 七、命名规则

### 主权技能
默认使用：
- `8917-xxx`

### 外部技能
尽量保留原名，放在 external 层；若需要本地治理，优先新增 wrapper，而不是直接改外部 skill 本体。

---

## 八、一句话原则

**`8917-skills` 只收可执行资产；skill 要轻、要清楚、要可复用，不要把理论全文和仓库杂项塞进 skill 目录。**
