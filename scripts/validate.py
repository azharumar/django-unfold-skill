#!/usr/bin/env python3
"""Validate the skill: frontmatter, size budget, internal links and coverage targets.

Standard library only. Run from the repository root: python scripts/validate.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "unfold-admin"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFS = SKILL_DIR / "references"
COVERAGE = ROOT / "docs" / "coverage.md"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$", re.M)

errors: list[str] = []


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append("SKILL.md: missing YAML frontmatter")
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line and not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def slugify(heading: str) -> str:
    # GitHub-style anchor: lowercase, drop punctuation, spaces to hyphens.
    heading = re.sub(r"[`*]", "", heading).strip().lower()
    heading = re.sub(r"[^\w\- ]", "", heading)
    return heading.replace(" ", "-")


def check_frontmatter() -> None:
    fm = parse_frontmatter(SKILL_MD.read_text())
    name = fm.get("name", "")
    description = fm.get("description", "")
    if not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"SKILL.md: invalid name {name!r}")
    if name != SKILL_DIR.name:
        errors.append(f"SKILL.md: name {name!r} must match directory {SKILL_DIR.name!r}")
    if not 1 <= len(description) <= 1024:
        errors.append(f"SKILL.md: description length {len(description)} not in 1..1024")
    if len(fm.get("compatibility", "")) > 500:
        errors.append("SKILL.md: compatibility longer than 500 characters")


def check_links(path: Path) -> None:
    text = path.read_text()
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        file_part, _, anchor = target.partition("#")
        dest = (path.parent / file_part).resolve() if file_part else path
        if not dest.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken link {target}")
            continue
        if anchor and dest.suffix == ".md":
            anchors = {slugify(h) for h in HEADING_RE.findall(dest.read_text())}
            if anchor not in anchors:
                errors.append(f"{path.relative_to(ROOT)}: missing anchor {target}")


def check_coverage() -> None:
    text = COVERAGE.read_text()
    known = {p.name for p in REFS.glob("*.md")} | {"SKILL.md"}
    for row in text.splitlines():
        if not row.startswith("| [") or row.count("|") < 6:
            continue
        target = row.rstrip("|").rsplit("|", 1)[-1]
        for name in re.findall(r"[\w-]+\.md", target):
            if name not in known:
                errors.append(f"docs/coverage.md: unknown target {name}")
    referenced = set(re.findall(r"references/([\w-]+\.md)", SKILL_MD.read_text()))
    for ref in known - {"SKILL.md"}:
        if ref not in referenced:
            errors.append(f"SKILL.md: reference {ref} is not linked")


def main() -> int:
    check_frontmatter()
    lines = SKILL_MD.read_text().count("\n")
    if lines > 500:
        errors.append(f"SKILL.md: {lines} lines exceeds the 500-line spec guidance")
    for path in [SKILL_MD, *sorted(REFS.glob("*.md")), ROOT / "README.md", COVERAGE]:
        check_links(path)
    check_coverage()

    # Rough estimate: ~4 characters per token for English prose mixed with code.
    chars = len(SKILL_MD.read_text())
    print(f"SKILL.md: {lines} lines, {chars} chars (~{chars // 4} tokens)")
    for ref in sorted(REFS.glob("*.md")):
        c = len(ref.read_text())
        print(f"  {ref.name:30} {c:6} chars (~{c // 4} tokens)")
    if errors:
        print("\nFAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
