#!/usr/bin/env python3
"""Bundle each skill's SKILL.md and references into one Markdown file.

For AI tools that don't read skill folders (ChatGPT, Gemini, any API):
paste the file as a system prompt or upload it as a knowledge file.
Writes dist/<skill>-prompt.md for every folder in skills/.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"

ROLES = {
    "humanizer-th": "คุณคือผู้ช่วยเกลาภาษาไทย",
    "localize-th": "คุณคือผู้ช่วยแปลภาษาอังกฤษเป็นภาษาไทย สำหรับซับไตเติล แอป เว็บไซต์ และเกม",
    "script-th": "คุณคือผู้ช่วยเขียนและเกลาบทพูดภาษาไทย สำหรับละครสั้นที่สร้างด้วย AI และเสียงพากย์ AI",
}

HEADER = """\
# {name}

{role} ทำงานตามคำสั่งในเอกสารนี้ทุกข้อ

เอกสารนี้รวมทุกไฟล์ของ skill {name} ไว้ในไฟล์เดียว ส่วนแรกคือคำสั่งหลัก (SKILL.md) ส่วนที่เหลือคือไฟล์อ้างอิงที่คำสั่งหลักพูดถึง ได้แก่ {refs} ทุกไฟล์อยู่ในเอกสารนี้แล้ว ไม่ต้องหาหรือโหลดเพิ่ม และเมื่อเขียนคำตอบให้ผู้ใช้ ห้ามพูดถึงเอกสารนี้หรือชื่อไฟล์
{extra}
"""

NO_SCRIPTS = (
    "\nสคริปต์ในโฟลเดอร์ `scripts/` ของ skill นี้ไม่ได้รวมอยู่ในเอกสาร "
    "ถ้าคำสั่งหลักให้รันสคริปต์ ให้ทำตามทางเลือกสำหรับกรณีที่รันไม่ได้แทน\n"
)


def strip_frontmatter(text):
    return re.sub(r"\A---\n.*?\n---\n+", "", text, flags=re.S)


def demote(text):
    # Push every heading down one level so the bundle has one H1.
    # Lines inside code fences are left alone.
    out, fenced = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced and re.match(r"#{1,5} ", line):
            line = "#" + line
        out.append(line)
    return "\n".join(out)


def build(skill_dir):
    name = skill_dir.name
    skill = strip_frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    # References in the order SKILL.md lists them.
    refs = list(dict.fromkeys(re.findall(r"\]\(references/([^)#]+)\)", skill)))
    skill = re.sub(rf"^# {re.escape(name)}\n+", "", skill)
    # Links to reference files point at sections of this bundle instead.
    skill = re.sub(r"\[references/([^\]]+)\]\(references/[^)]+\)", r"`\1` (อยู่ท้ายเอกสาร)", skill)
    extra = NO_SCRIPTS if (skill_dir / "scripts").is_dir() else ""
    parts = [HEADER.format(
        name=name,
        role=ROLES.get(name, "คุณคือผู้ช่วยด้านภาษาไทย"),
        refs=" ".join(f"`{r}`" for r in refs),
        extra=extra,
    )]
    parts.append("## คำสั่งหลัก (SKILL.md)\n\n" + demote(skill).strip() + "\n")
    for ref in refs:
        body = strip_frontmatter((skill_dir / "references" / ref).read_text(encoding="utf-8"))
        parts.append(f"## ไฟล์อ้างอิง: {ref}\n\n" + demote(demote(body)).strip() + "\n")
    out = DIST / f"{name}-prompt.md"
    out.write_text("\n".join(parts), encoding="utf-8")
    print(f"Built {out.relative_to(ROOT)} ({len(out.read_text(encoding='utf-8'))} chars)")


def main():
    DIST.mkdir(exist_ok=True)
    for skill_dir in sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file()):
        build(skill_dir)


if __name__ == "__main__":
    sys.exit(main())
