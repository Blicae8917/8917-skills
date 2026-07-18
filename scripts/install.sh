#!/usr/bin/env bash
# 8917-skills 一键安装(macOS / Linux):把 skills/ 下全部 skill 以 symlink 链接进本机 Agent 宿主。
# 幂等:已正确链接的跳过;同名路径被占用且不是指向本仓的链接时只警告,不覆盖。
# 用法:./scripts/install.sh
set -euo pipefail

case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*)
    echo "Windows 环境请用 scripts/install.ps1(Git Bash 的 ln -s 默认是复制,不是链接)。"
    exit 1
    ;;
esac

repo_skills="$(cd "$(dirname "$0")/../skills" && pwd)"
linked=0
found_host=0

for host_root in "$HOME/.claude" "$HOME/.codex" "$HOME/.agents"; do
  [ -d "$host_root" ] || continue
  found_host=1
  host_dir="$host_root/skills"
  echo "宿主: $host_dir"
  mkdir -p "$host_dir"
  for skill in "$repo_skills"/*/; do
    skill="${skill%/}"
    name="$(basename "$skill")"
    link="$host_dir/$name"
    if [ -L "$link" ]; then
      if [ "$(readlink "$link")" = "$skill" ]; then
        echo "  已装(跳过): $name"
      else
        echo "  冲突(未覆盖): $link 是指向别处的链接"
      fi
      continue
    elif [ -e "$link" ]; then
      echo "  冲突(未覆盖): $link 已存在且不是链接"
      continue
    fi
    ln -s "$skill" "$link"
    echo "  已链接: $name -> $skill"
    linked=$((linked + 1))
  done
done

if [ "$found_host" -eq 0 ]; then
  echo "未发现 ~/.claude、~/.codex 或 ~/.agents,本机没有可安装的 Agent 宿主。"
  exit 1
fi
echo "完成:新装 $linked 个链接。新 skill 在下个 Agent 会话生效。"
