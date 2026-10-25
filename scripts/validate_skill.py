#!/usr/bin/env python3
"""Validate every skill in skills/: frontmatter, reference links, codes, shared copies, versions."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
EXAMPLES_DIR = ROOT / "examples"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Pattern code prefix -> the file that defines its codes.
CODE_FILES = {
    "TH": ROOT / "shared" / "patterns.md",
    "LT": SKILLS_DIR / "localize-th" / "references" / "translation.md",
    "SC": SKILLS_DIR / "script-th" / "references" / "dialogue.md",
}
CODE_RE = re.compile(r"\b(" + "|".join(CODE_FILES) + r")\d{2}\b")

errors = []


def read(path):
    return path.read_text(encoding="utf-8")


def rel(path):
    return path.relative_to(ROOT)


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


def skill_dirs():
    return sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())


def check_skill(skill):
    skill_md = skill / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"missing {rel(skill_md)}")
        return
    text = read(skill_md)
    fm = parse_frontmatter(text)
    if fm is None:
        errors.append(f"{rel(skill_md)} has no frontmatter (--- block at top)")
        return
    name = fm.get("name", "")
    if not NAME_RE.match(name):
        errors.append(f"{rel(skill_md)}: name {name!r} must be lowercase letters, digits and hyphens")
    elif name != skill.name:
        errors.append(f"{rel(skill_md)}: name {name!r} does not match folder {skill.name!r}")
    desc = fm.get("description", "")
    if not desc:
        errors.append(f"{rel(skill_md)}: description is empty")
    elif len(desc) > 1024:
        errors.append(f"{rel(skill_md)}: description is {len(desc)} chars (max 1024)")
    for target in re.findall(r"\]\((references/[^)#]+)", text):
        if not (skill / target).is_file():
            errors.append(f"{rel(skill_md)} links to missing file {target}")


def defined_codes():
    defined = {}
    for prefix, path in CODE_FILES.items():
        if not path.is_file():
            errors.append(f"missing {rel(path)} (defines {prefix} codes)")
            defined[prefix] = set()
            continue
        text = read(path)
        sections = set(re.findall(rf"^### ({prefix}\d{{2}}) ", text, re.M))
        indexed = set(re.findall(rf"^\| ({prefix}\d{{2}}) \|", text, re.M))
        if not sections:
            errors.append(f"{rel(path)} defines no {prefix} codes (### {prefix}xx headings)")
        for code in sorted(sections - indexed):
            errors.append(f"{rel(path)}: {code} has a section but is missing from the index")
        for code in sorted(indexed - sections):
            errors.append(f"{rel(path)}: {code} is in the index but has no section")
        defined[prefix] = sections
    return defined


def check_code_usage(defined):
    files = sorted(SKILLS_DIR.glob("*/SKILL.md")) + sorted(SKILLS_DIR.glob("*/references/*.md"))
    files += sorted(ROOT.glob("shared/*.md")) + sorted(EXAMPLES_DIR.glob("**/*.md"))
    defining_names = {prefix: path.name for prefix, path in CODE_FILES.items()}
    for f in files:
        for code in sorted({m.group(0) for m in CODE_RE.finditer(read(f))}):
            prefix = code[:2]
            if f.name == defining_names[prefix]:
                continue  # the defining file and its copies are checked by defined_codes()
            if code not in defined[prefix]:
                errors.append(f"{rel(f)} uses {code}, not defined in {rel(CODE_FILES[prefix])}")


def check_shared_copies():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sync_shared.py"), "--check"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        errors.append(result.stdout.strip())


def check_versions():
    m = re.search(r"^## \[(\d+\.\d+\.\d+)\]", read(ROOT / "CHANGELOG.md"), re.M)
    if not m:
        errors.append("CHANGELOG.md has no version heading (## [x.y.z])")
        return
    for manifest in (".claude-plugin/plugin.json", ".cursor-plugin/plugin.json"):
        version = json.loads(read(ROOT / manifest)).get("version")
        if version != m.group(1):
            errors.append(f"{manifest} version {version!r} does not match CHANGELOG {m.group(1)!r}")


for skill in skill_dirs():
    check_skill(skill)
check_code_usage(defined_codes())
check_shared_copies()
check_versions()

if errors:
    print("FAILED")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
names = ", ".join(p.name for p in skill_dirs())
print(f"OK: {names}: frontmatter, reference links, pattern codes, shared copies and versions are valid")
