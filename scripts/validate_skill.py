#!/usr/bin/env python3
"""Validate the humanizer-th skill: frontmatter, reference links, pattern codes."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "humanizer-th"
SKILL_MD = SKILL_DIR / "SKILL.md"
PATTERNS_MD = SKILL_DIR / "references" / "patterns.md"
EXAMPLES_DIR = ROOT / "examples"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
CODE_RE = re.compile(r"\bTH\d{2}\b")

errors = []


def read(path):
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields = {}
    for line in m.group(1).split("\n"):
        key, sep, value = line.partition(":")
        if sep and key.strip() and not line.startswith((" ", "\t")):
            fields[key.strip()] = value.strip()
    return fields


def check_frontmatter():
    if not SKILL_MD.is_file():
        errors.append(f"missing {SKILL_MD.relative_to(ROOT)}")
        return
    fm = parse_frontmatter(read(SKILL_MD))
    if fm is None:
        errors.append("SKILL.md has no frontmatter (--- block at top)")
        return
    name = fm.get("name", "")
    if not NAME_RE.match(name):
        errors.append(f"name {name!r} must be lowercase letters, digits and hyphens")
    elif name != SKILL_DIR.name:
        errors.append(f"name {name!r} does not match folder {SKILL_DIR.name!r}")
    desc = fm.get("description", "")
    if not desc:
        errors.append("description is empty")
    elif len(desc) > 1024:
        errors.append(f"description is {len(desc)} chars (max 1024)")


def check_reference_links():
    if not SKILL_MD.is_file():
        return
    for target in re.findall(r"\]\((references/[^)#]+)", read(SKILL_MD)):
        if not (SKILL_DIR / target).is_file():
            errors.append(f"SKILL.md links to missing file {target}")


def check_codes():
    if not PATTERNS_MD.is_file():
        errors.append(f"missing {PATTERNS_MD.relative_to(ROOT)}")
        return
    defined = set(re.findall(r"^### (TH\d{2}) ", read(PATTERNS_MD), re.M))
    if not defined:
        errors.append("patterns.md defines no TH codes (### THxx headings)")
    text = read(PATTERNS_MD)
    indexed = set(re.findall(r"^\| (TH\d{2}) \|", text, re.M))
    for code in sorted(defined - indexed):
        errors.append(f"patterns.md: {code} has a section but is missing from the index")
    for code in sorted(indexed - defined):
        errors.append(f"patterns.md: {code} is in the index but has no section")
    files = sorted(EXAMPLES_DIR.glob("*.md")) + sorted(
        p for p in (SKILL_DIR / "references").glob("*.md") if p != PATTERNS_MD
    )
    for f in files:
        for code in sorted(set(CODE_RE.findall(read(f))) - defined):
            errors.append(f"{f.relative_to(ROOT)} uses {code}, not defined in patterns.md")


check_frontmatter()
check_reference_links()
check_codes()

if errors:
    print("FAILED")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
print("OK: frontmatter, reference links and pattern codes are valid")
