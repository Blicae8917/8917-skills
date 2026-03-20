# 8917-minimax-toolkit Smoke Test

日期：2026-03-21
状态：最小级别 smoke test 已完成

## 已验证内容

### 1. 代码层可编译
以下脚本已通过 `python3 -m py_compile`：
- `scripts/minimax_client.py`
- `scripts/mm_image.py`
- `scripts/mm_video.py`
- `scripts/mm_speech.py`
- `scripts/mm_music.py`
- `scripts/mm_i2i.py`
- `scripts/mm_async_speech.py`
- `scripts/mm_video_template.py`
- `scripts/mm_voice_clone.py`
- `scripts/mm_voice_design.py`

### 2. 结构层已验证
- 目录结构符合 `SKILL.md + scripts/ + references/` 规范
- 未检测到私有绝对路径残留（如 `/Users/blicae/.../8917Studio/00-Output/`）
- 已统一支持通用输出目录逻辑

### 3. 发布版关键能力已确认
- 使用 MiniMax Token Plan API Key
- 输出 request 次数与 5 小时滚动窗口提示
- 默认输出到 workspace 或通用输出目录
- 支持 `--project` 和 `--output-dir`

## 尚未完成的更高阶验证
以下属于下一步可选验证，不在本次最小 smoke test 范围内：
- 真实 API 调用级图片生成
- 真实 API 调用级语音生成
- 视频模板接口返回字段验证
- Voice clone / voice design 的真实在线测试

## 结论

当前 `8917-minimax-toolkit` 已通过最小级别发布前 smoke test，达到仓内样板与下一步公开发布准备状态。
