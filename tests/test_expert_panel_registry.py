import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    REPO_ROOT
    / "skills"
    / "8917-expert-panel"
    / "scripts"
    / "expert_registry.py"
)


class ExpertRegistryCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_lists_codex_toml_cards_with_canonical_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "multi-agent-systems-architect.toml").write_text(
                'name = "Multi-Agent Systems Architect"\n'
                'description = "Designs reliable agent systems."\n'
                'developer_instructions = "Prefer explicit contracts."\n',
                encoding="utf-8",
            )

            result = self.run_cli(
                "list", "--host", "codex", "--root", str(root)
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["host"], "codex")
            self.assertEqual(payload["count"], 1)
            card = payload["experts"][0]
            self.assertEqual(card["canonical_id"], "multi-agent-systems-architect")
            self.assertEqual(card["native_id"], "multi-agent-systems-architect")
            self.assertEqual(card["display_name"], "Multi-Agent Systems Architect")
            self.assertNotIn("instructions", card)
            self.assertEqual(len(card["sha256"]), 64)

    def test_lists_claude_code_markdown_cards_using_internal_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "engineering-multi-agent-systems-architect.md").write_text(
                "---\n"
                "name: Multi-Agent Systems Architect\n"
                "description: Designs reliable agent systems.\n"
                "---\n\n"
                "# Role\n\nPrefer explicit contracts.\n",
                encoding="utf-8",
            )

            result = self.run_cli(
                "list", "--host", "claude-code", "--root", str(root)
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            card = payload["experts"][0]
            self.assertEqual(card["canonical_id"], "multi-agent-systems-architect")
            self.assertEqual(
                card["native_id"], "engineering-multi-agent-systems-architect"
            )
            self.assertEqual(card["display_name"], "Multi-Agent Systems Architect")

    def test_parses_claude_block_scalar_descriptions_without_invalid_cards(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "folded-expert.md").write_text(
                "---\n"
                "name: Folded Expert\n"
                "description: >\n"
                "  Designs reliable agent systems\n"
                "  across multiple runtimes.\n"
                "---\n\n"
                "# Role\n",
                encoding="utf-8",
            )
            (root / "literal-expert.md").write_text(
                "---\n"
                "name: Literal Expert\n"
                "description: |\n"
                "  First responsibility.\n"
                "  Second responsibility.\n"
                "---\n\n"
                "# Role\n",
                encoding="utf-8",
            )

            result = self.run_cli(
                "list", "--host", "claude-code", "--root", str(root)
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["count"], 2)
            self.assertEqual(payload["invalid"], [])
            descriptions = {
                card["display_name"]: card["description"]
                for card in payload["experts"]
            }
            self.assertEqual(
                descriptions["Folded Expert"],
                "Designs reliable agent systems across multiple runtimes.",
            )
            self.assertEqual(
                descriptions["Literal Expert"],
                "First responsibility.\nSecond responsibility.",
            )

    def test_resolve_can_return_instructions_without_listing_every_card_body(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "reality-checker.toml").write_text(
                'name = "Reality Checker"\n'
                'description = "Challenges unsupported claims."\n'
                'developer_instructions = "Trust evidence over claims."\n',
                encoding="utf-8",
            )

            result = self.run_cli(
                "resolve",
                "--host",
                "codex",
                "--root",
                str(root),
                "--name",
                "Reality Checker",
                "--include-instructions",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            card = json.loads(result.stdout)
            self.assertEqual(card["display_name"], "Reality Checker")
            self.assertEqual(card["instructions"], "Trust evidence over claims.")

    def test_query_filters_compact_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "architect.toml").write_text(
                'name = "Workflow Architect"\n'
                'description = "Designs workflow systems."\n'
                'developer_instructions = "Design workflows."\n',
                encoding="utf-8",
            )
            (root / "writer.toml").write_text(
                'name = "Technical Writer"\n'
                'description = "Writes technical documentation."\n'
                'developer_instructions = "Write clearly."\n',
                encoding="utf-8",
            )

            result = self.run_cli(
                "list",
                "--host",
                "codex",
                "--root",
                str(root),
                "--query",
                "workflow",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["count"], 1)
            self.assertEqual(payload["experts"][0]["display_name"], "Workflow Architect")

    def test_preserves_non_ascii_names_in_canonical_id(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "architecture-reviewer.toml").write_text(
                'name = "架构评审专家"\n'
                'description = "审查系统架构。"\n'
                'developer_instructions = "只产判断。"\n',
                encoding="utf-8",
            )

            result = self.run_cli(
                "list", "--host", "codex", "--root", str(root)
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            card = json.loads(result.stdout)["experts"][0]
            self.assertEqual(card["canonical_id"], "架构评审专家")

    def test_reports_invalid_cards_without_hiding_valid_cards(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "valid.toml").write_text(
                'name = "Valid Expert"\n', encoding="utf-8"
            )
            (root / "invalid.toml").write_text(
                'name = "unterminated\n', encoding="utf-8"
            )

            result = self.run_cli(
                "list", "--host", "codex", "--root", str(root)
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["count"], 1)
            self.assertEqual(len(payload["invalid"]), 1)


if __name__ == "__main__":
    unittest.main()
