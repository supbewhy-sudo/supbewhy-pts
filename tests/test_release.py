import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "supbewhy-pts"


class ReleaseContractTests(unittest.TestCase):
    def test_visible_skill_runtime_files_exist(self):
        required = {
            SKILL / "SKILL.md",
            SKILL / "agents" / "openai.yaml",
            SKILL / "references" / "rulebook.md",
            SKILL / "references" / "examples.md",
            SKILL / "references" / "gpt-5-6-basis.md",
        }
        missing = sorted(str(path.relative_to(ROOT)) for path in required if not path.is_file())
        self.assertEqual(missing, [], f"missing runtime files: {missing}")

    def test_skill_frontmatter_and_core_contract(self):
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        self.assertIn("name: supbewhy-pts", content)
        self.assertRegex(content, r"(?m)^description: .+")
        for phrase in (
            "Task immutable; prompt mutable",
            "Scope Fidelity",
            "supɃewhY",
            "supBewhY",
            "supbewhy",
            "PST",
            "Do not execute",
        ):
            self.assertIn(phrase, content)

    def test_skill_has_no_transform_and_execute_mode(self):
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertNotIn("transform and execute", content)
        self.assertNotIn("pts 后直接执行", content)

    def test_skill_reference_paths_resolve(self):
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        refs = re.findall(r"`(references/[^`]+\.md)`", content)
        self.assertGreaterEqual(len(refs), 3)
        missing = [ref for ref in refs if not (SKILL / ref).is_file()]
        self.assertEqual(missing, [])

    def test_behavior_corpus_has_exactly_15_cases_and_required_coverage(self):
        cases = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))
        self.assertEqual(len(cases), 15)
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        categories = {case["category"] for case in cases}
        expected = {
            "scope_fidelity",
            "noise_removal",
            "missing_information",
            "from_scratch",
            "brand_boundary",
            "trigger_boundary",
            "target_preservation",
            "constraint_preservation",
            "output_mode",
            "mvp_boundary",
        }
        self.assertTrue(expected.issubset(categories))
        for case in cases:
            for key in (
                "id",
                "category",
                "name",
                "input",
                "should_trigger",
                "expected_mode",
                "required",
                "forbidden",
                "rationale",
            ):
                self.assertIn(key, case)
            self.assertIsInstance(case["required"], list)
            self.assertIsInstance(case["forbidden"], list)


if __name__ == "__main__":
    unittest.main()
