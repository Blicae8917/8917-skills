# 8917-skills 一键安装(Windows):把 skills/ 下全部 skill 以 Junction 链接进本机 Agent 宿主。
# 幂等:已正确链接的跳过;同名路径被占用且不是指向本仓的链接时只警告,不覆盖。
# 用法:.\scripts\install.ps1
$ErrorActionPreference = "Stop"
$repoSkills = (Resolve-Path (Join-Path $PSScriptRoot "..\skills")).Path

$hostDirs = @()
if (Test-Path (Join-Path $HOME ".claude")) { $hostDirs += (Join-Path $HOME ".claude\skills") }
if (Test-Path (Join-Path $HOME ".codex"))  { $hostDirs += (Join-Path $HOME ".codex\skills") }
if (Test-Path (Join-Path $HOME ".agents")) { $hostDirs += (Join-Path $HOME ".agents\skills") }
if (-not $hostDirs) {
    Write-Host "未发现 ~/.claude、~/.codex 或 ~/.agents,本机没有可安装的 Agent 宿主。"
    exit 1
}

$linked = 0
foreach ($hostDir in $hostDirs) {
    Write-Host "宿主: $hostDir"
    New-Item -ItemType Directory -Force $hostDir | Out-Null
    foreach ($skill in (Get-ChildItem $repoSkills -Directory)) {
        $link = Join-Path $hostDir $skill.Name
        if (Test-Path $link) {
            $item = Get-Item $link
            if ($item.LinkType -and ([string]$item.Target -eq $skill.FullName)) {
                Write-Host "  已装(跳过): $($skill.Name)"
            } else {
                Write-Host "  冲突(未覆盖): $link 已存在且不是指向本仓的链接"
            }
            continue
        }
        New-Item -ItemType Junction -Path $link -Target $skill.FullName | Out-Null
        Write-Host "  已链接: $($skill.Name) -> $($skill.FullName)"
        $linked++
    }
}
Write-Host "完成:新装 $linked 个链接。新 skill 在下个 Agent 会话生效。"
