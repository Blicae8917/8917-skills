#!/usr/bin/env python3
"""恢复 Claude Code Desktop 会话列表(切换账号后)。

机制:Desktop 会话列表按账号分区存储,macOS / Windows 目录结构同构:
  macOS   ~/Library/Application Support/Claude/claude-code-sessions/<账号UUID>/<组织UUID>/local_*.json
  Windows %APPDATA%/Claude/claude-code-sessions/<账号UUID>/<组织UUID>/local_*.json
切换账号后新分区为空,旧分区记录仍在磁盘。本脚本把旧分区的会话元数据
迁入当前分区(按 cliSessionId 去重,自动备份,可回滚),重启 Desktop 后列表恢复。
迁入时清空 bridgeSessionIds / remoteMcpServersConfig 两个旧账号关联字段
(云端桥接句柄与连接器配置,恢复的记录声明为纯本地转录入口),其余内容原样保留。

当前分区判定:包含全局最新活动 local_*.json 的账号目录(运行本脚本的会话
本身就在当前账号下持续写入,故该判定成立;若判定可疑用 --target 指定)。

用法(Windows 下 python3 换成 python):
  restore_desktop_sessions.py [--days 7] [--dry-run] [--all] [--target UUID前缀]
                              [--from 旧分区UUID前缀] [--cwd 路径子串]
"""
import argparse
import json
import os
import sys
import tarfile
import time
from datetime import datetime
from pathlib import Path

BACKUP_DIR = Path.home() / ".claude/backups"

# 迁入时清空的旧账号关联字段:云端桥接句柄 / 连接器配置
SANITIZED_FIELDS = ("bridgeSessionIds", "remoteMcpServersConfig")


def sessions_root(platform=None, env=None):
    """按平台返回 Desktop 会话列表存储根;不支持的平台返回 None。"""
    platform = platform or sys.platform
    env = os.environ if env is None else env
    if platform == "darwin":
        return Path.home() / "Library/Application Support/Claude/claude-code-sessions"
    if platform == "win32":
        appdata = env.get("APPDATA")
        base = Path(appdata) if appdata else Path.home() / "AppData/Roaming"
        return base / "Claude/claude-code-sessions"
    return None


def sanitize_meta(meta):
    """返回清洗副本:清空旧账号关联字段,其余原样;不改动入参。"""
    clean = dict(meta)
    for field in SANITIZED_FIELDS:
        if field in clean:
            clean[field] = []
    return clean


def load_meta(path):
    """读会话元数据;损坏文件返回 None(跳过,不中断)。"""
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(d, dict) or "cliSessionId" not in d:
            return None
        return d
    except (json.JSONDecodeError, OSError):
        return None


def activity_ts(path, meta):
    """会话最后活动时间(秒)。优先元数据 lastActivityAt(毫秒),缺失用文件 mtime。"""
    ts = meta.get("lastActivityAt")
    if isinstance(ts, (int, float)) and ts > 0:
        return ts / 1000
    return path.stat().st_mtime


def scan_partitions(root):
    """返回 {账号UUID: [(文件路径, 元数据, 活动时间秒), ...]}。"""
    partitions = {}
    if not root.is_dir():
        sys.exit(f"未找到会话存储目录: {root}")
    for acct_dir in root.iterdir():
        if not acct_dir.is_dir():
            continue
        records = []
        for f in acct_dir.glob("*/local_*.json"):
            meta = load_meta(f)
            if meta is None:
                continue
            records.append((f, meta, activity_ts(f, meta)))
        partitions[acct_dir.name] = records
    return partitions


def pick_current(partitions, target_prefix):
    """定位当前账号分区;返回 (账号UUID, 目标org目录)。"""
    if target_prefix:
        matches = [a for a in partitions if a.startswith(target_prefix)]
        if len(matches) != 1:
            sys.exit(f"--target '{target_prefix}' 匹配到 {len(matches)} 个分区,需唯一前缀")
        acct = matches[0]
    else:
        candidates = [(max(ts for _, _, ts in recs), a)
                      for a, recs in partitions.items() if recs]
        if not candidates:
            sys.exit("所有分区均为空,无法判定当前账号;请用 --target 指定")
        acct = max(candidates)[1]
    # 目标 org 子目录 = 当前分区下含最新记录的那个
    recs = partitions[acct]
    if not recs:
        sys.exit(f"当前分区 {acct[:8]} 无任何记录,无法定位目标 org 目录")
    latest_file = max(recs, key=lambda r: r[2])[0]
    return acct, latest_file.parent


def main():
    ap = argparse.ArgumentParser(description="恢复 Desktop 会话列表(账号切换后)")
    ap.add_argument("--days", type=int, default=7, help="恢复最近 N 天(默认 7)")
    ap.add_argument("--all", action="store_true", help="不限天数,恢复全部")
    ap.add_argument("--dry-run", action="store_true", help="只报告,不备份不写入")
    ap.add_argument("--target", default=None, help="手动指定当前账号分区 UUID 前缀")
    ap.add_argument("--from", dest="from_prefix", default=None,
                    help="只从匹配该 UUID 前缀的旧分区迁入(多旧账号时筛源)")
    ap.add_argument("--cwd", default=None, help="只迁入 cwd 包含该子串的记录")
    args = ap.parse_args()

    root = sessions_root()
    if root is None:
        sys.exit(f"暂不支持当前平台: {sys.platform}(本 skill 面向 macOS / Windows 的 Claude Code Desktop)")
    partitions = scan_partitions(root)
    current_acct, dest_dir = pick_current(partitions, args.target)
    cutoff = 0 if args.all else time.time() - args.days * 86400

    print(f"存储根: {root}")
    print(f"当前账号分区: {current_acct[:8]}...  目标目录: .../{dest_dir.parent.name[:8]}.../{dest_dir.name[:8]}...")
    filters = []
    if args.from_prefix:
        filters.append(f"源分区前缀={args.from_prefix}")
    if args.cwd:
        filters.append(f"cwd 含「{args.cwd}」")
    print(f"范围: {'全部历史' if args.all else f'最近 {args.days} 天'}"
          f"{('  ' + ' / '.join(filters)) if filters else ''}"
          f"{'  [dry-run 只读]' if args.dry_run else ''}\n")

    existing_ids = {m["cliSessionId"] for _, m, _ in partitions[current_acct]}
    existing_titles = {m.get("title") for _, m, _ in partitions[current_acct]}

    # 收集候选:其余分区中时间窗内的记录;同 cliSessionId 多份时取最新
    candidates = {}
    for acct, recs in partitions.items():
        if acct == current_acct:
            continue
        if args.from_prefix and not acct.startswith(args.from_prefix):
            continue
        in_window = [r for r in recs if r[2] >= cutoff
                     and (not args.cwd or args.cwd in r[1].get("cwd", ""))]
        latest = max((ts for _, _, ts in recs), default=None)
        latest_h = datetime.fromtimestamp(latest).strftime("%m-%d %H:%M") if latest else "-"
        print(f"  旧分区 {acct[:8]}...  共 {len(recs)} 条,窗口内 {len(in_window)} 条,最近活动 {latest_h}")
        for f, meta, ts in in_window:
            cid = meta["cliSessionId"]
            if cid not in candidates or ts > candidates[cid][2]:
                candidates[cid] = (f, meta, ts)

    to_copy = [(f, m, ts) for cid, (f, m, ts) in candidates.items()
               if cid not in existing_ids]
    skipped = len(candidates) - len(to_copy)
    print(f"\n候选 {len(candidates)} 条(跨分区已按 cliSessionId 去重),"
          f"目标分区已存在跳过 {skipped} 条,待迁入 {len(to_copy)} 条")

    if not to_copy:
        print("无需迁移。")
        return
    for _, meta, ts in sorted(to_copy, key=lambda r: -r[2])[:10]:
        t = datetime.fromtimestamp(ts).strftime("%m-%d %H:%M")
        hint = "  ←同名已存在,疑似 fork" if meta.get("title") in existing_titles else ""
        print(f"    {t}  {meta.get('title', '<无标题>')[:50]}  ({meta.get('cwd', '?')}){hint}")
    if len(to_copy) > 10:
        print(f"    ... 及另外 {len(to_copy) - 10} 条")

    if args.dry_run:
        print("\n[dry-run] 未做任何修改。去掉 --dry-run 执行迁移。")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = BACKUP_DIR / f"claude-code-sessions-backup-{stamp}.tar.gz"
    with tarfile.open(backup, "w:gz") as tf:
        tf.add(root, arcname=root.name)
    print(f"\n已备份: {backup}")

    copied = 0
    for f, meta, _ in to_copy:
        dest = dest_dir / f.name
        if dest.exists():  # 文件名撞车(极小概率),不覆盖
            continue
        clean = sanitize_meta(meta)
        dest.write_text(json.dumps(clean, ensure_ascii=False, separators=(",", ":")),
                        encoding="utf-8")
        if load_meta(dest) is None:  # 写入后校验
            dest.unlink()
            print(f"  校验失败已移除: {f.name}")
            continue
        st = f.stat()
        os.utime(dest, (st.st_atime, st.st_mtime))  # 保留原文件时间线(mtime 兜底排序)
        copied += 1

    print(f"迁入完成: {copied}/{len(to_copy)} 条")
    print("\n下一步: 重启 Claude Code Desktop 应用,会话列表即可见。")
    print(f"回滚: tar xzf {backup} -C '{root.parent}'")


if __name__ == "__main__":
    main()
