# 8917-minimax-toolkit v0.2.1 Release Note

## 概述

`v0.2.1` 是 `8917-minimax-toolkit` 的透明度与风控信息补强版本。

这次更新不改变 skill 的核心能力，而是专门补足之前在公开发布场景下容易触发风控疑虑的信息披露：
- MiniMax Token Plan API Key 的读取路径
- OpenClaw 环境下的本地配置兜底读取
- 图片 / 音频 / 视频等媒体文件会上传到 MiniMax API 的事实
- 数据处理与隐私提示

---

## 本次更新内容

### 1. 明确 API Key 读取规则
现在公开写明：
1. 优先读取 `MINIMAX_API_KEY`
2. 若运行在 OpenClaw 环境中，可从 `~/.openclaw/openclaw.json` 兜底读取 MiniMax Token Plan API Key

### 2. 明确媒体上传行为
现在公开写明：
- 图生图会上传参考图
- 视频模板会上传媒体素材
- 声音克隆会上传音频样本
- 相关能力会把必要素材发送到 MiniMax API 完成任务

### 3. 新增隐私与透明度提示
在 `SKILL.md` 中新增“数据处理与隐私提示”小节，提醒用户：
- 高敏感媒体应先确认再处理
- 该 skill 不是纯本地离线工具
- 敏感行为已明确披露

### 4. 新增透明度说明文件
新增：
- `references/8917-minimax-toolkit-trust-note.md`

用于解释为什么这类 skill 容易被安全扫描器标记为 caution / suspicious，以及如何通过充分披露来建立信任。

---

## 版本意义

`v0.2.1` 的重点不是新能力，而是：
> **让 skill 看起来和实际上都足够清白、透明、可审计。**

---

## 一句话总结

`v0.2.1` 是 `8917-minimax-toolkit` 的透明度修订版，用更完整的行为披露来降低风控误判并提升公开可用性。
