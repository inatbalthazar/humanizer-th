#!/usr/bin/env python3
"""Bundle SKILL.md and its references into one Markdown file.

For AI tools that don't read skill folders (ChatGPT, Gemini, any API):
paste the file as a system prompt or upload it as a knowledge file.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "humanizer-th"
OUT = ROOT / "dist" / "humanizer-th-prompt.md"
REFERENCES = ["patterns.md", "registers.md", "word-swaps.md"]

HEADER = """\
# humanizer-th

คุณคือผู้ช่วยเกลาภาษาไทย ทำงานตามคำสั่งในเอกสารนี้ทุกข้อ

เอกสารนี้รวมทุกไฟล์ของ skill humanizer-th ไว้ในไฟล์เดียว ส่วนแรกคือคำสั่งหลัก (SKILL.md) ส่วนที่เหลือคือไฟล์อ้างอิงที่คำสั่งหลักพูดถึง ได้แก่ {refs} ทุกไฟล์อยู่ในเอกสารนี้แล้ว ไม่ต้องหาหรือโหลดเพิ่ม และเมื่อเขียนคำตอบให้ผู้ใช้ ห้ามพูดถึงเอกสารนี้หรือชื่อไฟล์

"""


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


def main():
    skill = strip_frontmatter((SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"))
    skill = re.sub(r"^# humanizer-th\n+", "", skill)
    # Links to reference files point at sections of this bundle instead.
    skill = re.sub(r"\[references/([^\]]+)\]\(references/[^)]+\)", r"`\1` (อยู่ท้ายเอกสาร)", skill)
    parts = [HEADER.format(refs=" ".join(f"`{r}`" for r in REFERENCES))]
    parts.append("## คำสั่งหลัก (SKILL.md)\n\n" + demote(skill).strip() + "\n")
    for name in REFERENCES:
        body = strip_frontmatter((SKILL_DIR / "references" / name).read_text(encoding="utf-8"))
        parts.append(f"## ไฟล์อ้างอิง: {name}\n\n" + demote(demote(body)).strip() + "\n")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Built {OUT.relative_to(ROOT)} ({len(OUT.read_text(encoding='utf-8'))} chars)")


if __name__ == "__main__":
    sys.exit(main())
