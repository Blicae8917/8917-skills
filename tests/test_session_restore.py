import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from importlib import util as importlib_util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    REPO_ROOT
    / "skills"
    / "8917-session-restore"
    / "scripts"
    / "restore_desktop_sessions.py"
)


def load_module():
    spec = importlib_util.spec_from_file_location("restore_desktop_sessions", SCRIPT)
    module = importlib_util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MOD = load_module()


class SessionsRootTests(unittest.TestCase):
    def test_darwin_root_under_application_support(self) -> None:
        root = MOD.sessions_root(platform="darwin", env={})
        self.assertEqual(
            Path.home() / "Library/Application Support/Claude/claude-code-sessions",
            root,
        )

    def test_win32_root_follows_appdata_env(self) -> None:
        root = MOD.sessions_root(
            platform="win32", env={"APPDATA": r"C:\Users\x\AppData\Roaming"}
        )
        self.assertEqual(
            Path(r"C:\Users\x\AppData\Roaming") / "Claude/claude-code-sessions",
            root,
        )

    def test_unsupported_platform_returns_none(self) -> None:
        self.assertIsNone(MOD.sessions_root(platform="linux", env={}))


class SanitizeMetaTests(unittest.TestCase):
    def test_strips_account_bound_fields_and_keeps_rest(self) -> None:
        meta = {
            "sessionId": "local_x",
            "cliSessionId": "abc",
            "title": "码道调度 session",
            "bridgeSessionIds": ["session_01X"],
            "remoteMcpServersConfig": [{"name": "Figma"}],
        }
        clean = MOD.sanitize_meta(meta)
        self.assertEqual([], clean["bridgeSessionIds"])
        self.assertEqual([], clean["remoteMcpServersConfig"])
        self.assertEqual("abc", clean["cliSessionId"])
        self.assertEqual("码道调度 session", clean["title"])
        # 入参不被改动
        self.assertEqual(["session_01X"], meta["bridgeSessionIds"])

    def test_fields_absent_stay_absent(self) -> None:
        clean = MOD.sanitize_meta({"cliSessionId": "abc"})
        self.assertNotIn("bridgeSessionIds", clean)


@unittest.skipUnless(
    sys.platform in ("darwin", "win32"), "Desktop 会话存储仅存在于 macOS/Windows"
)
class DryRunCliTests(unittest.TestCase):
    def _write_record(self, org_dir: Path, name: str, cli_id: str, ts_ms: int) -> None:
        org_dir.mkdir(parents=True, exist_ok=True)
        (org_dir / f"local_{name}.json").write_text(
            json.dumps(
                {
                    "sessionId": f"local_{name}",
                    "cliSessionId": cli_id,
                    "title": f"t-{name}",
                    "cwd": "/tmp/p",
                    "lastActivityAt": ts_ms,
                }
            ),
            encoding="utf-8",
        )

    def test_dry_run_reports_candidates_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            env = dict(os.environ)
            env.update(
                {
                    "HOME": str(temp),
                    "USERPROFILE": str(temp),
                    "APPDATA": str(temp / "AppData" / "Roaming"),
                    "PYTHONUTF8": "1",
                }
            )
            # 与脚本的 sessions_root 同步:子进程 Path.home() 也随上面的 env 指向 temp
            if sys.platform == "win32":
                root = Path(env["APPDATA"]) / "Claude/claude-code-sessions"
            else:
                root = temp / "Library/Application Support/Claude/claude-code-sessions"
            now_ms = int(time.time() * 1000)
            cur_org = root / "acct-new-uuid" / "org-a"
            old_org = root / "acct-old-uuid" / "org-b"
            self._write_record(cur_org, "cur", "cli-cur", now_ms)
            self._write_record(old_org, "old1", "cli-old1", now_ms - 1000)
            # 与当前分区同 cliSessionId → 去重跳过
            self._write_record(old_org, "dup", "cli-cur", now_ms - 2000)

            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--dry-run"],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env,
            )
            self.assertEqual(0, proc.returncode, proc.stderr)
            self.assertIn("待迁入 1 条", proc.stdout)
            self.assertIn("[dry-run]", proc.stdout)
            # dry-run 未写入任何文件
            self.assertEqual(1, len(list(cur_org.glob("local_*.json"))))


if __name__ == "__main__":
    unittest.main()
