#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOP_README = ROOT / "README.md"
SKIP_DIRS = {".git", ".agent", "scripts", "__pycache__", ".github"}
SKILLS_START = "<!-- skills:start -->"
SKILLS_END = "<!-- skills:end -->"


def iter_skill_dirs() -> list[Path]:
    skills: list[Path] = []
    for child in sorted(ROOT.iterdir()):
        if not child.is_dir() or child.name.startswith(".") or child.name in SKIP_DIRS:
            continue
        if (child / "SKILL.md").exists():
            skills.append(child)
    return skills


def extract_frontmatter(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    return match.group(1) if match else ""


def extract_field(frontmatter: str, field_name: str) -> str:
    lines = frontmatter.splitlines()
    for idx, line in enumerate(lines):
        if not line.startswith(f"{field_name}:"):
            continue
        _, value = line.split(":", 1)
        value = value.strip()
        if value and value not in {"|", ">"}:
            return value.strip().strip('"')
        block: list[str] = []
        for next_line in lines[idx + 1 :]:
            if next_line.startswith("  ") or not next_line.strip():
                if next_line.startswith("  "):
                    block.append(next_line.strip())
                continue
            break
        return " ".join(part for part in block if part).strip().strip('"')
    return ""


def extract_summary(description: str) -> str:
    summary = re.split(r"\bUse when\b", description, maxsplit=1, flags=re.IGNORECASE)[0].strip()
    summary = summary.rstrip()
    if not summary.endswith("."):
        summary = f"{summary}."
    return summary


def render_skill_section(skills: list[dict[str, str]]) -> str:
    blocks: list[str] = []
    for skill in skills:
        blocks.append(
            "\n".join(
                [
                    f"### {skill['name']}",
                    "",
                    skill["summary"],
                    "",
                    f"[Documentation](./{skill['name']}/README.md)",
                ]
            )
        )
    return f"{SKILLS_START}\n\n" + "\n\n".join(blocks) + f"\n\n{SKILLS_END}"


def replace_skill_section(readme_text: str, section_text: str) -> str:
    pattern = rf"{re.escape(SKILLS_START)}.*?{re.escape(SKILLS_END)}"
    return re.sub(pattern, section_text, readme_text, flags=re.DOTALL)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate tumf/skills metadata and top-level README index.")
    parser.add_argument("--write", action="store_true", help="Rewrite the generated skill index section in README.md")
    args = parser.parse_args()

    top_readme = TOP_README.read_text()
    errors: list[str] = []
    warnings: list[str] = []
    skills = iter_skill_dirs()
    skill_rows: list[dict[str, str]] = []

    if SKILLS_START not in top_readme or SKILLS_END not in top_readme:
        errors.append("top-level README is missing skills:start / skills:end markers")

    for skill_dir in skills:
        name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        readme_md = skill_dir / "README.md"
        text = skill_md.read_text()
        frontmatter = extract_frontmatter(text)
        skill_name = extract_field(frontmatter, "name")
        description = extract_field(frontmatter, "description")

        if not readme_md.exists():
            errors.append(f"missing README.md: {name}")
        if not skill_name:
            errors.append(f"missing frontmatter name: {name}")
        elif skill_name != name:
            errors.append(f"frontmatter name mismatch: {name} != {skill_name}")
        if not description:
            errors.append(f"missing frontmatter description: {name}")
            continue
        if "use when" not in description.lower() and "use this skill when" not in description.lower():
            warnings.append(f"description lacks explicit trigger guidance: {name}")

        skill_rows.append({
            "name": name,
            "summary": extract_summary(description),
        })

    generated_section = render_skill_section(skill_rows)
    if not errors and SKILLS_START in top_readme and SKILLS_END in top_readme:
        rewritten = replace_skill_section(top_readme, generated_section)
        if args.write:
            TOP_README.write_text(rewritten)
            top_readme = rewritten
        elif rewritten != top_readme:
            errors.append("top-level README Available Skills section is out of date; run: python3 scripts/validate_skills.py --write")

    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"- {warning}")
        print()

    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK: validated {len(skills)} skills")
    if args.write:
        print("README skill index refreshed")
    if warnings:
        print(f"Warnings: {len(warnings)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
