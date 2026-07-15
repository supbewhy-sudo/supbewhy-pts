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

    def test_gpt_5_6_positioning_is_visible_and_official_basis_is_clear(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        opening = readme.split("## 为什么需要 PTS", 1)[0]
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("面向 GPT-5.6", opening)
        self.assertIn("GPT-5.6", skill.split("---", 2)[1])
        self.assertIn(
            "https://developers.openai.com/api/docs/guides/latest-model",
            readme,
        )
        self.assertIn("非 OpenAI 官方", opening)

    def test_readme_documents_only_the_two_compact_pts_forms(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cases = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))
        inputs = [case["input"] for case in cases]

        self.assertIn("pts:你", readme)
        self.assertIn("pts 把", readme)
        self.assertNotIn("pts: ", readme.lower())
        self.assertTrue(any(value.startswith("pts:") for value in inputs))
        self.assertTrue(any(value.startswith("pts ") for value in inputs))

        unrelated = next(case for case in cases if case["id"] == "unrelated-pts-acronym")
        self.assertTrue(unrelated["input"].startswith("PTS "))
        self.assertFalse(unrelated["should_trigger"])

    def test_readme_uses_clean_xiaohongshu_profile_link(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        canonical = (
            "https://www.xiaohongshu.com/user/profile/"
            "5a04313511be1005cafea0f9"
        )

        self.assertLess(readme.index("## 关于作者"), readme.index("## 为什么需要 PTS"))
        self.assertIn(canonical, readme)
        for tracking_key in ("xsec_token", "xhsshare", "appuid", "share_id", "wechatWid"):
            self.assertNotIn(tracking_key, readme)

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
