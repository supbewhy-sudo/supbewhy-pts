#!/usr/bin/env python3
"""Validate the supbewhy-pts runtime skill and release bundle."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Iterable


REQUIRED_SKILL_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/rulebook.md",
    "references/examples.md",
    "references/gpt-5-6-basis.md",
)

REQUIRED_CASE_FIELDS = (
    "id",
    "category",
    "name",
    "input",
    "should_trigger",
    "expected_mode",
    "required",
    "forbidden",
    "rationale",
)

REQUIRED_CATEGORIES = {
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


def parse_frontmatter(content: str) -> tuple[dict[str, str], list[str]]:
    issues: list[str] = []
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", content, re.DOTALL)
    if not match:
        return {}, ["SKILL.md: missing or malformed YAML frontmatter"]

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            issues.append(f"SKILL.md: malformed frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values, issues


def validate_skill_dir(skill_dir: Path) -> list[str]:
    issues: list[str] = []
    if not skill_dir.is_dir():
        return [f"missing visible skill directory: {skill_dir}"]

    for relative in REQUIRED_SKILL_FILES:
        if not (skill_dir / relative).is_file():
            issues.append(f"missing runtime file: {relative}")

    skill_path = skill_dir / "SKILL.md"
    if not skill_path.is_file():
        return issues

    content = skill_path.read_text(encoding="utf-8")
    frontmatter, frontmatter_issues = parse_frontmatter(content)
    issues.extend(frontmatter_issues)

    if set(frontmatter) != {"name", "description"}:
        issues.append("SKILL.md: frontmatter must contain only name and description")
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        issues.append("SKILL.md: name must use 1-64 lowercase letters, digits, or hyphens")
    if name and name != skill_dir.name:
        issues.append(f"SKILL.md: name {name!r} does not match folder {skill_dir.name!r}")
    if not description:
        issues.append("SKILL.md: description is required")
    if len(description) > 1024:
        issues.append("SKILL.md: description exceeds 1024 characters")

    for phrase in (
        "Task immutable; prompt mutable",
        "Scope Fidelity",
        "supɃewhY",
        "supBewhY",
        "supbewhy",
        "PST",
        "Do not execute",
    ):
        if phrase not in content:
            issues.append(f"SKILL.md: missing required contract phrase: {phrase}")

    lowered = content.lower()
    if "transform and execute" in lowered or "pts 后直接执行" in lowered:
        issues.append("SKILL.md: obsolete transform-and-execute mode is present")

    references = re.findall(r"`(references/[^`]+\.md)`", content)
    if len(set(references)) < 3:
        issues.append("SKILL.md: expected three conditionally routed reference files")
    for relative in sorted(set(references)):
        if not (skill_dir / relative).is_file():
            issues.append(f"SKILL.md: unresolved reference {relative}")

    metadata_path = skill_dir / "agents" / "openai.yaml"
    if metadata_path.is_file():
        metadata = metadata_path.read_text(encoding="utf-8")
        for key in ("display_name", "short_description", "default_prompt", "allow_implicit_invocation"):
            if not re.search(rf"(?m)^\s*{re.escape(key)}:\s*", metadata):
                issues.append(f"agents/openai.yaml: missing {key}")
        if name and f"${name}" not in metadata:
            issues.append(f"agents/openai.yaml: default_prompt must mention ${name}")
        short_match = re.search(r'(?m)^\s*short_description:\s*"([^"]+)"\s*$', metadata)
        if short_match and not 25 <= len(short_match.group(1)) <= 64:
            issues.append("agents/openai.yaml: short_description must be 25-64 characters")

    basis_path = skill_dir / "references" / "gpt-5-6-basis.md"
    if basis_path.is_file():
        basis = basis_path.read_text(encoding="utf-8")
        if "https://developers.openai.com/api/docs/guides/latest-model" not in basis:
            issues.append("gpt-5-6-basis.md: missing official guide URL")
        if not re.search(r"Reviewed:\s*\d{4}-\d{2}-\d{2}", basis):
            issues.append("gpt-5-6-basis.md: missing review date")

    return issues


def validate_cases_file(path: Path, expected_count: int = 15) -> list[str]:
    if not path.is_file():
        return [f"missing behavior corpus: {path}"]
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid behavior corpus JSON: {exc}"]

    issues: list[str] = []
    if not isinstance(cases, list):
        return ["behavior corpus must be a JSON list"]
    if len(cases) != expected_count:
        issues.append(f"behavior corpus must contain exactly {expected_count} cases; found {len(cases)}")

    ids: list[str] = []
    categories: set[str] = set()
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            issues.append(f"case {index}: must be an object")
            continue
        for field in REQUIRED_CASE_FIELDS:
            if field not in case:
                issues.append(f"case {index}: missing field {field}")
        case_id = case.get("id")
        category = case.get("category")
        if isinstance(case_id, str):
            ids.append(case_id)
        if isinstance(category, str):
            categories.add(category)
        if "should_trigger" in case and not isinstance(case["should_trigger"], bool):
            issues.append(f"case {index}: should_trigger must be boolean")
        for field in ("required", "forbidden"):
            if field in case and not isinstance(case[field], list):
                issues.append(f"case {index}: {field} must be a list")

    if len(ids) != len(set(ids)):
        issues.append("behavior corpus contains duplicate ids")
    missing_categories = sorted(REQUIRED_CATEGORIES - categories)
    if missing_categories:
        issues.append(f"behavior corpus missing categories: {', '.join(missing_categories)}")
    return issues


def validate_archive_names(names: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    for name in names:
        if not name or name.endswith("/"):
            continue
        while name.startswith("./"):
            name = name[2:]
        normalized.append(name)
    issues: list[str] = []
    if any(name.startswith(".agents/") for name in normalized):
        issues.append("archive uses a hidden .agents root; distribute a visible supbewhy-pts/ folder")
    for required in ("README.md", "supbewhy-pts/SKILL.md"):
        if required not in normalized:
            issues.append(f"archive missing visible entry: {required}")
    return issues


def validate_release(root: Path) -> list[str]:
    issues = validate_skill_dir(root / "supbewhy-pts")
    issues.extend(validate_cases_file(root / "tests" / "cases.json"))

    for relative in (
        "README.md",
        "scripts/validate_skill.py",
        "tests/manual-eval.md",
        "dist/supbewhy-pts.zip",
    ):
        if not (root / relative).is_file():
            issues.append(f"missing release file: {relative}")

    archive_path = root / "dist" / "supbewhy-pts.zip"
    if archive_path.is_file():
        try:
            with zipfile.ZipFile(archive_path) as archive:
                issues.extend(validate_archive_names(archive.namelist()))
                bad_file = archive.testzip()
                if bad_file:
                    issues.append(f"archive CRC failure: {bad_file}")
        except zipfile.BadZipFile as exc:
            issues.append(f"invalid release archive: {exc}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="project release root")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    issues = validate_release(root)
    if issues:
        print(f"Validation failed with {len(issues)} issue(s):")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Validation passed: runtime skill, 15-case corpus, metadata, references, and visible release archive are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
