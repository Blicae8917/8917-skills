---
name: 8917-session-restore
description: 切换 Claude 账号后恢复 Desktop 会话列表——自动识别当前账号分区与最近使用的旧账号分区,把旧分区会话记录迁入当前分区(去重/备份/可回滚),并给出账号切换完整影响面检查清单。触发词:"切换账号"、"恢复 session"、"会话列表空了"、"session 记录不见了"、"找回会话记录"、"restore sessions"。适用 macOS 与 Windows 的 Claude Code Desktop;会话转录正本(~/.claude/projects/)不绑账号,本 skill 恢复的是 Desktop 列表入口层。
---

# 8917-session-restore — 账号切换后恢复 Desktop 会话列表

## 机制(为什么会"丢")

Claude Code 的会话分两层存储,**转录正本永远不丢,丢的只是列表入口**:

| 层 | 位置 | 账号影响 |
|---|---|---|
| 转录正本(完整对话) | `~/.claude/projects/<项目路径编码>/*.jsonl` | 不绑账号,切换后完好 |
| Desktop 会话列表 | macOS `~/Library/Application Support/Claude/claude-code-sessions/`、Windows `%APPDATA%\Claude\claude-code-sessions\`,其下同构:`<账号UUID>/<组织UUID>/local_*.json` | 按账号分区,新账号分区为空 |

列表元数据文件为纯 JSON(title/cwd/cliSessionId/时间戳),**文件内不含账号字段,归属完全由目录路径决定**——所以跨分区复制即可恢复;迁入时仅清空 `bridgeSessionIds` / `remoteMcpServersConfig` 两个旧账号关联字段(云端桥接句柄与连接器配置,恢复的记录声明为纯本地转录入口),其余内容原样保留。

## 执行步骤

1. **先 dry-run 看统计**(只读,零风险):

   ```bash
   python3 scripts/restore_desktop_sessions.py --dry-run
   ```

   脚本自动判定:当前分区 = 含全局最新活动文件的账号目录(当前会话本身在新账号下持续写入,该信号必然指向当前账号;不要依赖 `~/.claude.json` 的 oauthAccount——CLI 与 Desktop 登录态独立,该字段可能滞后)。判定可疑时用 `--target <UUID前缀>` 手动指定。Windows 下 `python3` 换成 `python`,下同。

2. **执行迁移**(自动备份,可逆):

   ```bash
   python3 scripts/restore_desktop_sessions.py            # 默认最近 7 天
   python3 scripts/restore_desktop_sessions.py --days 30  # 或指定范围
   python3 scripts/restore_desktop_sessions.py --all      # 或全部历史
   python3 scripts/restore_desktop_sessions.py --from <UUID前缀>  # 多旧账号时只迁指定旧分区
   python3 scripts/restore_desktop_sessions.py --cwd <路径子串>   # 只迁指定项目的会话
   ```

   脚本行为:先 tar 备份整个存储目录到 `~/.claude/backups/` → 跨旧分区收集候选、按 `cliSessionId` 去重(目标分区已有的跳过) → 复制进当前分区的组织目录 → 逐文件校验可解析。

3. **重启 Claude Code Desktop 应用**——列表在应用启动时加载进内存,不重启看不到。Windows 端注意从托盘图标完全退出再启动,只关窗口不算退出。

4. **向指挥官报告**:迁入条数、备份路径、最近几条会话标题,并附下方影响面清单中其余需检查的项。

## 回滚

macOS:

```bash
tar xzf ~/.claude/backups/claude-code-sessions-backup-<时间戳>.tar.gz \
  -C ~/Library/Application\ Support/Claude/
```

Windows(PowerShell,`tar` 为 Win10+ 系统自带):

```powershell
tar xzf "$env:USERPROFILE\.claude\backups\claude-code-sessions-backup-<时间戳>.tar.gz" -C "$env:APPDATA\Claude"
```

## 账号切换完整影响面清单

恢复会话列表只是第一步。切换账号后逐项检查:

**受影响(绑账号)**:

| 项 | 说明 | 处置 |
|---|---|---|
| Desktop 会话列表 | 本 skill 恢复 | 迁移 + 重启应用 |
| CLI 登录态 | **CLI 与 Desktop 登录互相独立**:CLI 凭据在 macOS Keychain(service=`Claude Code-credentials`),Windows 在 `~/.claude/.credentials.json`;账号信息在 `~/.claude.json` 的 `oauthAccount`/`userID` 字段。Desktop 切了账号,CLI 仍是旧账号 | 终端里 `claude /login` 单独切换 |
| claude.ai 云端资源 | 云端会话(web/移动端发起)、Artifacts、claude.ai Projects 全部跟账号走,本地无法迁移 | 需要保留的内容在旧账号导出 |
| MCP connectors 授权 | claude.ai 连接器(Notion/GitLab/Slack 等)的 OAuth 授权绑账号 | 新账号在 claude.ai 连接器设置里重新授权 |
| 订阅与额度 | Plan 档位、用量、rate limit 状态跟账号走 | 无需操作,知悉即可 |

**不受影响(纯本机文件,任何账号登录都加载同一份)**:

- 全局记忆与规则:`~/.claude/CLAUDE.md`、`~/.claude/rules/`
- 能力层:`~/.claude/skills/`、`agents/`、`commands/`、hooks、plugins
- 配置:`settings.json`、`keybindings.json`、`~/.claude.json` 中除 oauthAccount 外的 projects/mcpServers 配置
- 数据:`~/.claude/projects/`(转录正本)、`~/.claude-mem/`、各项目 `.remember/`、todos、file-history

## 边界与注意

- 当前分区必须已有至少 1 条记录(即已在新账号下开过会话)——正常总成立,跑本 skill 的会话就是。
- 元数据里 `bridgeSessionIds`(云端桥接)绑旧账号,恢复的是**本地转录入口**;点开恢复的会话是从本地 jsonl 续接,云端桥接功能不迁移。
- 同一会话在 Desktop 端继续使用后 `cliSessionId` 可能更新(fork),旧新记录同名不同 id——迁入预览对同名会话标注「疑似 fork」;去重只按 cliSessionId,同名双入口无害,按需手动归档其一。
- 绕过 Desktop 的备用路径:`cd <项目目录> && claude --resume`(CLI 直接扫描本地转录,不认账号)。
