# Skill 规范 v1.0

## 文件结构

```
skill-name/
├── README.md          # Skill 说明（用户视角）
├── SKILL.md           # 协议定义（Agent 视角）
├── src/               # 代码实现（可选）
│   ├── core/
│   ├── templates/
│   └── utils/
└── tests/             # 测试用例
```

## SKILL.md 头部格式

```yaml
---
name: skill-name
version: x.y.z
description: "一句话描述"
author: "作者名"
---
```

## 最佳实践

1. **单一职责** — 一个 Skill 解决一类问题
2. **自包含** — 不依赖外部文件（除非明确声明）
3. **可验证** — 提供使用示例和预期输出
4. **渐进增强** — 基础功能可用，高级功能可选

---

_待完善_
