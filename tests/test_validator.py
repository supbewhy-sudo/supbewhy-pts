import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_skill import (
    validate_archive_names,
    validate_cases_file,
    validate_skill_dir,
)


ROOT = Path(__file__).resolve().parents[1]


class ValidatorTests(unittest.TestCase):
    def test_current_skill_directory_is_valid(self):
        self.assertEqual(validate_skill_dir(ROOT / "supbewhy-pts"), [])

    def test_missing_reference_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "supbewhy-pts"
            shutil.copytree(ROOT / "supbewhy-pts", skill)
            (skill / "references" / "examples.md").unlink()
            issues = validate_skill_dir(skill)
        self.assertTrue(any("references/examples.md" in issue for issue in issues))

    def test_wrong_case_count_is_reported(self):
        cases = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"
            path.write_text(json.dumps(cases[:-1], ensure_ascii=False), encoding="utf-8")
            issues = validate_cases_file(path)
        self.assertTrue(any("exactly 15" in issue for issue in issues))

    def test_hidden_install_root_is_rejected(self):
        names = [
            "README.md",
            ".agents/skills/supbewhy-pts/SKILL.md",
            "tests/cases.json",
        ]
        issues = validate_archive_names(names)
        self.assertTrue(any("hidden .agents root" in issue for issue in issues))

    def test_visible_release_root_is_accepted(self):
        names = [
            "README.md",
            "supbewhy-pts/SKILL.md",
            "supbewhy-pts/agents/openai.yaml",
            "supbewhy-pts/references/rulebook.md",
            "scripts/validate_skill.py",
            "tests/cases.json",
        ]
        self.assertEqual(validate_archive_names(names), [])


if __name__ == "__main__":
    unittest.main()
