"""skill 清单一致性门:skills/ 目录、双语 README 清单、SKILL.md name 字段三方对齐。

背景:8917-session-restore v1.0 入仓时漏登 CHANGELOG 与 README 清单,靠人工发现;
本测试把"新 skill 必须登记双语 README"固化为机制。
"""
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
READMES = (REPO_ROOT / "README.md", REPO_ROOT / "README_CN.md")


def skill_names():
    return sorted(p.name for p in SKILLS_DIR.iterdir() if p.is_dir())


class SkillRosterTests(unittest.TestCase):
    def test_every_skill_listed_in_both_readmes(self) -> None:
        names = skill_names()
        self.assertTrue(names, "skills/ 下没有任何 skill 目录")
        for readme in READMES:
            text = readme.read_text(encoding="utf-8")
            for name in names:
                self.assertIn(
                    f"`{name}`",
                    text,
                    f"{readme.name} 缺少 skill 登记: {name}(新 skill 入仓须同步双语 README 清单)",
                )

    def test_skill_md_name_matches_directory(self) -> None:
        for name in skill_names():
            skill_md = SKILLS_DIR / name / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"{name} 缺少 SKILL.md")
            match = re.search(
                r"^name:\s*(\S+)",
                skill_md.read_text(encoding="utf-8"),
                re.MULTILINE,
            )
            self.assertIsNotNone(match, f"{name}/SKILL.md 缺少 name: 字段")
            self.assertEqual(
                name, match.group(1), f"{name}/SKILL.md 的 name 字段与目录名不一致"
            )


if __name__ == "__main__":
    unittest.main()
