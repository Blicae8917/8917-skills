---
name: 8917-minimax-toolkit
description: MiniMax 多模态工具集。适用于：生成图片、图生图、视频、视频模板、语音合成、声音克隆、声音设计、长文本 TTS 和音乐生成。默认将产物输出到当前工作区的 `workspace/03-Resources/minimax-output/`；若当前目录不含 `workspace/`，则退回 `./outputs/minimax/`。支持 `--project` 进入项目子目录，也支持 `--output-dir` 显式覆盖输出根目录。默认读取 MiniMax Token Plan API Key（环境变量 `MINIMAX_API_KEY` 或 `~/.openclaw/openclaw.json`）。
metadata:
  openclaw:
    requires:
      env: ["MINIMAX_API_KEY"]
---

# minimax-toolkit

## 定位

这是一个 **工具型 / Tool Wrapper** skill。

它负责调用 MiniMax 的多模态生成能力并将产物有结构地落到当前工作区或用户指定目录。

---

## 输出纪律

### 输出根目录优先级
1. `--output-dir`
2. 环境变量 `MINIMAX_OUTPUT_DIR`
3. 当前工作目录下的 `workspace/03-Resources/minimax-output/`
4. 若当前目录不存在 `workspace/`，则退回 `./outputs/minimax/`

### 项目子目录
使用 `--project <ProjectName>` 时，产物进入：
- `<output-root>/<ProjectName>/<Modality>/`

### 完成提示
每次生成完成后，都应明确提示用户：
- 文件类型
- 保存路径
- 如需长期管理，建议后续整理到项目目录

---

## Token Plan Key 规则

默认读取的是 **MiniMax Token Plan API Key**。

读取优先级：
1. `MINIMAX_API_KEY`（通用、跨环境优先）
2. `~/.openclaw/openclaw.json`（如果运行在 OpenClaw 环境中，则作为增强兜底）

注意：
- Token Plan API Key 与按量计费文本模型 API Key 不可互换
- Token Plan 额度按 **请求次数（request）** 计，不按 token 计
- 套餐按 **5 小时滚动窗口** 扣减

---

## 数据处理与隐私提示

本 skill 在以下场景中会把用户提供的内容发送到 MiniMax API：
- 图片生成 / 图生图（上传参考图或接收生成结果）
- 视频生成 / 视频模板（上传素材或下载结果）
- 语音合成 / 长文本 TTS
- 声音克隆 / 声音设计（上传音频样本）
- 音乐生成

因此：
- 不要在未确认的情况下处理高敏感媒体文件
- 若任务涉及私密图像、音频或视频，应先确认用户接受第三方 API 处理
- 本 skill 的默认行为是把必要素材发送到 MiniMax 官方接口完成任务，而不是仅在本地离线处理

## 套餐提示规则

在执行前，应根据官方 Token Plan 文档输出请求消耗提示，至少包含：
- 模型名称
- 预计消耗的 request 次数
- 5 小时滚动窗口说明
- 高消耗任务（尤其视频）风险提醒

如果用户触顶，应提醒：
- 等待 5 小时窗口恢复
- 或改用按量计费 API Key

---

## 核心能力

### 1. 图片生成
```bash
python3 scripts/mm_image.py "A cyberpunk cat" --ratio 16:9 [--project MyProject] [--output-dir ./outputs/minimax]
```

### 2. 图生图
```bash
python3 scripts/mm_i2i.py "transform to anime style" --ref ~/photo.jpg [--project MyProject] [--output-dir ./outputs/minimax]
```

### 3. 视频生成
```bash
python3 scripts/mm_video.py "Cinematic flight over ruins" [--project MyProject] [--output-dir ./outputs/minimax]
```

### 4. 视频模板
```bash
python3 scripts/mm_video_template.py labubu --media ~/me.jpg [--project MyProject]
```

### 5. 语音合成
```bash
python3 scripts/mm_speech.py "你好！(laughs)" --voice male-qn-qingse [--project MyProject] [--output-dir ./outputs/minimax]
```

### 6. 声音克隆
```bash
python3 scripts/mm_voice_clone.py ~/my_voice.wav --voice-id my-voice [--project MyProject]
```

### 7. 声音设计
```bash
python3 scripts/mm_voice_design.py "A warm, deep male voice" [--project MyProject]
```

### 8. 长文本 TTS
```bash
python3 scripts/mm_async_speech.py ~/long_script.txt --voice male-qn-qingse [--project MyProject]
```

### 9. 音乐生成
```bash
python3 scripts/mm_music.py "Upbeat lo-fi beat" --instrumental [--project MyProject] [--output-dir ./outputs/minimax]
```

---

## 关键规则

1. API Key 只能从 MiniMax Token Plan API Key 来源读取，禁止硬编码。
2. 不再使用个人绝对路径作为默认输出目录。
3. 产物默认遵守当前工作区纪律；如果没有 workspace，则使用通用输出目录。
4. 若任务需要项目隔离，优先使用 `--project`；若要显式控制输出根目录，使用 `--output-dir`。

---

## 一句话原则

**MiniMax 产物默认落当前工作区或通用输出目录，并在执行前明确提示 Token Plan 请求消耗与 5 小时窗口风险。**
