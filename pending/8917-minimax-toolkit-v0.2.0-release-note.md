# 8917-minimax-toolkit v0.2.0 Release Note

## 概述

`8917-minimax-toolkit` 是 8917 的多模态生成工具集，统一封装 MiniMax 的图片、图生图、视频、视频模板、语音合成、声音克隆、声音设计、长文本 TTS 和音乐生成能力。

本次 `v0.2.0` 是它进入 `8917-skills` 仓库后的首个仓内发布候选版本，重点不是新增更多能力，而是把它从本地工具脚本收敛为更适合公开复用的技能资产。

---

## 本次版本的关键改进

### 1. 主权化命名完成
- 技能名统一为 `8917-minimax-toolkit`
- 与 `8917-skills` 仓库的主权命名体系一致

### 2. 输出目录通用化
不再依赖个人绝对路径。

输出根目录优先级统一为：
1. `--output-dir`
2. `MINIMAX_OUTPUT_DIR`
3. `workspace/03-Resources/minimax-output/`
4. `./outputs/minimax/`

### 3. Token Plan 逻辑明确化
- 默认使用 **MiniMax Token Plan API Key**
- 支持 `MINIMAX_API_KEY`
- 若运行在 OpenClaw 环境中，可从 `~/.openclaw/openclaw.json` 兜底读取
- 根据官方文档提示 request 消耗与 **5 小时滚动窗口** 风险

### 4. 多脚本统一收口
已统一关键脚本的：
- 输出目录逻辑
- 保存结果提示
- request 次数提示
- 项目子目录支持

### 5. 最小 smoke test 已完成
- 核心脚本已通过编译校验
- 未检测到个人绝对路径残留
- 结构符合当前 `8917-skills` 的 skill 规范

---

## 当前能力范围

- Image Generation
- Image-to-Image
- Video Generation
- Video Agent Templates
- Speech Synthesis
- Voice Clone
- Voice Design
- Async Long-text TTS
- Music Generation

---

## 当前定位

- 类型：**工具型**
- 模式：**Tool Wrapper**
- 状态：**仓内旗舰样板候选**

---

## 仍未纳入本版本的内容

以下更高阶验证与发布动作，不属于本次 `v0.2.0` 的必需项：
- 全量真实 API 调用级 smoke test
- ClawHub 正式发布
- 更完整的公开示例集

---

## 一句话总结

`v0.2.0` 的意义不是把 `8917-minimax-toolkit` 做得更花，而是把它做得更通用、更清楚、更像一个可以公开复用的 8917 能力资产。
