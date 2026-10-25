#!/usr/bin/env python3
"""Check a Thai translation against its English source.

Errors are things that break the file: changed timings, missing keys,
missing or changed placeholders and tags, invalid JSON or XML.
Warnings are style limits: subtitle line length, line count, reading speed,
"!" in the text, and untranslated entries.

  python3 check_translation.py SOURCE TRANSLATION
  python3 check_translation.py FILE            (PO, XLIFF, CSV hold both)

Options:
  --max-line N     max characters per subtitle line (default 35)
  --max-lines N    max lines per subtitle block (default 2)
  --max-cps N      max characters per second (default 20)
  --source-col C   CSV source column (default: English, en, source)
  --target-col C   CSV target column (default: Thai, th, target)
  --strict         exit 1 on warnings too

Thai characters are counted without tone marks and upper or lower vowels,
which take no horizontal space. Exit code is 1 when there is an error.
"""
import argparse
import csv
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

PLACEHOLDER_RE = re.compile(
    r"\{\{[^{}]+\}\}"                              # {{count}} i18next
    r"|\{[A-Za-z0-9_.]+\}"                         # {name} {0}
    r"|\{[A-Za-z0-9_]+,"                           # {count, plural, ... ICU argument
    r"|%(?:\d+\$)?[-+0#]*\d*(?:\.\d+)?[sdifuxXc@]"  # %s %1$d %.2f %@
    r"|%\([A-Za-z_]+\)[sd]"                        # %(name)s
    r"|\[[A-Za-z][A-Za-z0-9_]*\]"                  # [PlayerName]
    r"|\$[A-Za-z_][A-Za-z0-9_]*\$"                 # $gold$
    r"|\\n"                                        # literal \n
)
HTML_TAG_RE = re.compile(r"</?[A-Za-z][^<>]*>")
ASS_TAG_RE = re.compile(r"\{\\[^{}]*\}|\\[Nnh]")
TIME_SRT = re.compile(r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})")
TIME_VTT = re.compile(r"(?:(\d{2,}):)?(\d{2}):(\d{2})\.(\d{3})")


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")


def visible_len(text):
    """Characters that take horizontal space; Thai combining marks are not counted."""
    return sum(1 for ch in text if unicodedata.category(ch) != "Mn")


def tokens(text, subtitle=False, ass=False):
    # Subtitles have no placeholders; [laughs] and the like are translated.
    found = HTML_TAG_RE.findall(text)
    if not subtitle:
        found += PLACEHOLDER_RE.findall(text)
    if ass:
        found += ASS_TAG_RE.findall(text)
    return Counter(found)


def compare_tokens(report, where, src, dst, subtitle=False, ass=False):
    a, b = tokens(src, subtitle, ass), tokens(dst, subtitle, ass)
    if a == b:
        return
    missing = a - b
    extra = b - a
    if missing:
        report.error(where, "missing " + ", ".join(sorted(missing.elements())))
    if extra:
        report.error(where, "unexpected " + ", ".join(sorted(extra.elements())))


def check_style(report, where, text):
    if "!" in strip_markup(text):
        report.warn(where, 'contains "!"')


def strip_markup(text):
    return ASS_TAG_RE.sub(" ", HTML_TAG_RE.sub("", text))


# ---------- subtitles ----------

def srt_seconds(stamp):
    h, m, s, ms = (int(x) for x in TIME_SRT.match(stamp).groups())
    return h * 3600 + m * 60 + s + ms / 1000


def parse_srt(text):
    cues = []
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n").strip()):
        lines = block.split("\n")
        if len(lines) < 2 or "-->" not in lines[1]:
            if lines and lines[0].strip():
                cues.append({"id": lines[0].strip(), "time": None, "lines": lines[1:]})
            continue
        start, _, end = lines[1].partition("-->")
        cues.append({
            "id": lines[0].strip(),
            "time": lines[1].strip(),
            "start": srt_seconds(start.strip()),
            "end": srt_seconds(end.strip().split()[0]),
            "lines": lines[2:],
        })
    return cues


def vtt_seconds(stamp):
    h, m, s, ms = TIME_VTT.match(stamp).groups()
    return int(h or 0) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def parse_vtt(text):
    cues = []
    blocks = re.split(r"\n\s*\n", text.replace("\r\n", "\n").strip())
    for block in blocks[1:]:  # first block is the WEBVTT header
        lines = block.split("\n")
        if lines[0].startswith(("NOTE", "STYLE", "REGION")):
            continue
        idx = 0 if "-->" in lines[0] else 1
        if idx >= len(lines) or "-->" not in lines[idx]:
            continue
        start, _, rest = lines[idx].partition("-->")
        cues.append({
            "id": lines[0].strip() if idx else "",
            "time": lines[idx].strip(),
            "start": vtt_seconds(start.strip()),
            "end": vtt_seconds(rest.strip().split()[0]),
            "lines": lines[idx + 1:],
        })
    return cues


def ass_seconds(stamp):
    h, m, s = stamp.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def parse_ass(text):
    cues = []
    for n, line in enumerate(text.replace("\r\n", "\n").split("\n"), 1):
        if not line.startswith("Dialogue:"):
            continue
        fields = line[len("Dialogue:"):].split(",", 9)
        if len(fields) < 10:
            continue
        cues.append({
            "id": f"line {n}",
            "time": ",".join(f.strip() for f in fields[:9]),
            "start": ass_seconds(fields[1].strip()),
            "end": ass_seconds(fields[2].strip()),
            "lines": fields[9].split("\\N"),
        })
    return cues


def check_subtitles(report, src_cues, dst_cues, opts, ass=False):
    if len(src_cues) != len(dst_cues):
        report.error("file", f"{len(src_cues)} blocks in source, {len(dst_cues)} in translation")
    for i, (s, d) in enumerate(zip(src_cues, dst_cues), 1):
        where = f"block {d['id'] or i}"
        if s["time"] != d["time"]:
            report.error(where, f"timing changed: {s['time']!r} -> {d['time']!r}")
        if s["id"] != d["id"] and not ass:
            report.error(where, f"block id changed: {s['id']!r} -> {d['id']!r}")
        src_text = "\n".join(s["lines"])
        dst_text = "\n".join(d["lines"])
        compare_tokens(report, where, src_text, dst_text, subtitle=True, ass=ass)
        lines = [strip_markup(l).strip() for l in d["lines"] if strip_markup(l).strip()]
        if not lines:
            if strip_markup(src_text).strip():
                report.warn(where, "empty")
            continue
        if len(lines) > opts.max_lines:
            report.warn(where, f"{len(lines)} lines (max {opts.max_lines})")
        for line in lines:
            n = visible_len(line)
            if n > opts.max_line:
                report.warn(where, f"line is {n} characters (max {opts.max_line}): {line}")
        duration = d.get("end", 0) - d.get("start", 0) if d.get("time") else 0
        if duration > 0:
            cps = sum(visible_len(l) for l in lines) / duration
            if cps > opts.max_cps:
                report.warn(where, f"{cps:.1f} characters per second (max {opts.max_cps})")
        if any(l.endswith(".") and not l.endswith("...") for l in lines):
            report.warn(where, "line ends with a period")
        check_style(report, where, dst_text)


# ---------- key-value formats ----------

def flatten_json(data, prefix=""):
    out = {}
    if isinstance(data, dict):
        for k, v in data.items():
            out.update(flatten_json(v, f"{prefix}{k}."))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            out.update(flatten_json(v, f"{prefix}{i}."))
    else:
        out[prefix[:-1]] = data
    return out


def load_json(report, path, label):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as e:
        report.error(label, f"invalid JSON: {e}")
        return None


def strings_pairs(text):
    pair = re.compile(r'"((?:[^"\\]|\\.)*)"\s*=\s*"((?:[^"\\]|\\.)*)"\s*;')
    return dict(pair.findall(text))


def android_strings(report, path, label):
    raw = Path(path).read_text(encoding="utf-8")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        report.error(label, f"invalid XML: {e}")
        return None
    out = {}
    for el in root:
        name = el.get("name")
        if not name or el.get("translatable") == "false":
            continue
        if el.tag == "string":
            out[name] = inner_xml(el)
        elif el.tag in ("plurals", "string-array"):
            for i, item in enumerate(el.findall("item")):
                key = item.get("quantity") or str(i)
                out[f"{name}[{key}]"] = inner_xml(item)
    return out


def inner_xml(el):
    parts = [el.text or ""]
    for child in el:
        parts.append(ET.tostring(child, encoding="unicode"))
    return "".join(parts)


def compare_maps(report, src, dst, skip=lambda k: False):
    for key in src:
        if skip(key):
            continue
        if key not in dst:
            plural = re.match(r"(.+)\[(zero|one|two|few|many)\]$", key)
            if plural and f"{plural.group(1)}[other]" in dst:
                continue  # Thai only needs the "other" plural form
            report.error(f"key {key}", "missing in translation")
            continue
        s, d = src[key], dst[key]
        if not isinstance(s, str) or not isinstance(d, str):
            if s != d:
                report.error(f"key {key}", f"non-text value changed: {s!r} -> {d!r}")
            continue
        compare_tokens(report, f"key {key}", s, d)
        if s.strip() and s == d and re.search(r"[A-Za-z]{3}", s):
            report.warn(f"key {key}", "same as source (untranslated?)")
        check_style(report, f"key {key}", d)
    for key in dst:
        if key not in src and not skip(key) and not re.search(r"\[other\]$", key):
            report.error(f"key {key}", "not in source")
    if list(k for k in src if k in dst) != list(k for k in dst if k in src):
        report.warn("file", "keys are in a different order from the source")


# ---------- single-file formats ----------

def po_entries(text):
    entries, cur, field = [], {}, None
    for line in text.replace("\r\n", "\n").split("\n") + [""]:
        line = line.strip()
        if not line:
            if cur:
                entries.append(cur)
            cur, field = {}, None
            continue
        if line.startswith("#"):
            if line.startswith("#,"):
                cur["flags"] = line
            continue
        m = re.match(r'^(msgctxt|msgid_plural|msgid|msgstr(?:\[\d+\])?)\s+"(.*)"$', line)
        if m:
            field = m.group(1)
            cur[field] = unescape_po(m.group(2))
        elif line.startswith('"') and field:
            cur[field] += unescape_po(line[1:-1])
    return entries


def unescape_po(s):
    return s.replace('\\"', '"').replace("\\\\", "\\")


def check_po(report, path):
    for e in po_entries(Path(path).read_text(encoding="utf-8")):
        msgid = e.get("msgid", "")
        if not msgid:
            continue  # header
        where = f"msgid {msgid[:40]!r}"
        if "msgid_plural" in e:
            targets = [v for k, v in e.items() if k.startswith("msgstr[")]
            source = e["msgid_plural"]
        else:
            targets = [e.get("msgstr", "")]
            source = msgid
        for t in targets:
            if not t:
                report.warn(where, "not translated")
                continue
            compare_tokens(report, where, source, t)
            check_style(report, where, t)
        if "fuzzy" in e.get("flags", ""):
            report.warn(where, "still marked fuzzy")


def element_text(el):
    """Text plus inline elements, so tags like <x id="1"/> are compared too."""
    if el is None:
        return ""
    parts = [el.text or ""]
    for child in el:
        tag = child.tag.split("}")[-1]
        parts.append(f"<{tag} id={child.get('id', '')}>")
        parts.append(element_text(child))
        parts.append(child.tail or "")
    return "".join(parts)


def check_xliff(report, path):
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        report.error("file", f"invalid XML: {e}")
        return
    def local(el):
        return el.tag.split("}")[-1]
    for el in root.iter():
        if local(el) not in ("trans-unit", "segment"):
            continue
        uid = el.get("id") or "?"
        source = next((c for c in el if local(c) == "source"), None)
        target = next((c for c in el if local(c) == "target"), None)
        where = f"unit {uid}"
        if target is None or not element_text(target).strip():
            report.warn(where, "no target")
            continue
        s, t = element_text(source), element_text(target)
        compare_tokens(report, where, s, t)
        inline_s = Counter(re.findall(r"<\w+ id=[^>]*>", s))
        inline_t = Counter(re.findall(r"<\w+ id=[^>]*>", t))
        if inline_s != inline_t:
            report.error(where, "inline tags differ between source and target")
        check_style(report, where, t)


def check_csv(report, path, opts):
    with open(path, encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        rows = list(csv.DictReader(f, dialect=dialect))
    if not rows:
        report.error("file", "no rows")
        return
    cols = {c.lower(): c for c in rows[0].keys() if c}
    src_col = pick_col(cols, opts.source_col, ["english", "en", "source", "en-us"])
    dst_col = pick_col(cols, opts.target_col, ["thai", "th", "target", "th-th"])
    if not src_col or not dst_col:
        report.error("file", f"cannot find source/target columns in {list(rows[0].keys())}")
        return
    max_col = pick_col(cols, None, ["maxlength", "max length", "max_length", "limit"])
    id_col = pick_col(cols, None, ["id", "key", "string id"]) or src_col
    for n, row in enumerate(rows, 2):
        where = f"row {n} ({row.get(id_col, '')})"
        s, d = row.get(src_col) or "", row.get(dst_col) or ""
        if not d.strip():
            if s.strip():
                report.warn(where, "not translated")
            continue
        compare_tokens(report, where, s, d)
        if max_col and (row.get(max_col) or "").strip().isdigit():
            limit = int(row[max_col])
            if visible_len(d) > limit:
                report.warn(where, f"{visible_len(d)} characters (max {limit})")
        check_style(report, where, d)


def pick_col(cols, wanted, defaults):
    if wanted:
        return cols.get(wanted.lower())
    for name in defaults:
        if name in cols:
            return cols[name]
    return None


# ---------- main ----------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--max-line", type=int, default=35)
    ap.add_argument("--max-lines", type=int, default=2)
    ap.add_argument("--max-cps", type=float, default=20)
    ap.add_argument("--source-col")
    ap.add_argument("--target-col")
    ap.add_argument("--strict", action="store_true")
    opts = ap.parse_args(argv)

    report = Report()
    ext = Path(opts.files[-1]).suffix.lower()
    single = {".po": check_po, ".xlf": check_xliff, ".xliff": check_xliff}
    if len(opts.files) == 1:
        path = opts.files[0]
        if ext in single:
            single[ext](report, path)
        elif ext in (".csv", ".tsv"):
            check_csv(report, path, opts)
        else:
            ap.error(f"{ext} needs two files: SOURCE TRANSLATION")
    elif len(opts.files) == 2:
        src_path, dst_path = opts.files
        read = lambda p: Path(p).read_text(encoding="utf-8-sig")
        if ext == ".srt":
            check_subtitles(report, parse_srt(read(src_path)), parse_srt(read(dst_path)), opts)
        elif ext == ".vtt":
            check_subtitles(report, parse_vtt(read(src_path)), parse_vtt(read(dst_path)), opts)
        elif ext in (".ass", ".ssa"):
            check_subtitles(report, parse_ass(read(src_path)), parse_ass(read(dst_path)), opts, ass=True)
        elif ext in (".json", ".arb"):
            src, dst = load_json(report, src_path, "source"), load_json(report, dst_path, "translation")
            if src is not None and dst is not None:
                skip = (lambda k: k.split(".")[0].startswith("@")) if ext == ".arb" else (lambda k: False)
                compare_maps(report, flatten_json(src), flatten_json(dst), skip)
        elif ext == ".strings":
            compare_maps(report, strings_pairs(read(src_path)), strings_pairs(read(dst_path)))
        elif ext == ".xml":
            src = android_strings(report, src_path, "source")
            dst = android_strings(report, dst_path, "translation")
            if src is not None and dst is not None:
                compare_maps(report, src, dst)
        elif ext in single:
            single[ext](report, dst_path)
        else:
            ap.error(f"unsupported file type: {ext}")
    else:
        ap.error("give one or two files")

    for e in report.errors:
        print(f"ERROR  {e}")
    for w in report.warnings:
        print(f"WARN   {w}")
    print(f"{len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    if report.errors or (opts.strict and report.warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
