"""Tests for skills/localize-th/scripts/check_translation.py. Run: python3 -m unittest discover tests"""
import contextlib
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures" / "check_translation"
sys.path.insert(0, str(ROOT / "skills" / "localize-th" / "scripts"))

import check_translation  # noqa: E402


def run(*names):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = check_translation.main([str(FIXTURES / n) for n in names])
    return code, out.getvalue()


class VisibleLength(unittest.TestCase):
    def test_thai_marks_not_counted(self):
        self.assertEqual(check_translation.visible_len("ไม่เป็นไรหรอก"), 11)
        self.assertEqual(check_translation.visible_len("น้ำ"), 2)


class Subtitles(unittest.TestCase):
    def test_good(self):
        code, out = run("en.srt", "th.srt")
        self.assertEqual(code, 0, out)
        self.assertIn("0 error(s), 0 warning(s)", out)

    def test_bad(self):
        code, out = run("en.srt", "th_bad.srt")
        self.assertEqual(code, 1)
        self.assertIn("timing changed", out)
        self.assertIn("missing </i>, <i>", out)
        self.assertIn('contains "!"', out)
        self.assertIn("characters per second", out)

    def test_vtt(self):
        code, out = run("en.vtt", "th.vtt")
        self.assertEqual(code, 0, out)

    def test_ass_tags(self):
        self.assertEqual(run("en.ass", "th.ass")[0], 0)
        code, out = run("en.ass", "th_bad.ass")
        self.assertEqual(code, 1)
        self.assertIn("missing {\\i0}, {\\i1}", out)


class KeyValue(unittest.TestCase):
    def test_json_good(self):
        code, out = run("en.json", "th.json")
        self.assertEqual(code, 0, out)

    def test_json_bad(self):
        code, out = run("en.json", "th_bad.json")
        self.assertEqual(code, 1)
        self.assertIn("missing {{count}}", out)
        self.assertIn("cart.greeting: missing in translation", out)

    def test_strings(self):
        self.assertEqual(run("en.strings", "th.strings")[0], 0)

    def test_android_plurals_other_only(self):
        code, out = run("en.xml", "th.xml")
        self.assertEqual(code, 0, out)


class SingleFile(unittest.TestCase):
    def test_po(self):
        code, out = run("th.po")
        self.assertEqual(code, 1)
        self.assertIn("missing %d", out)
        self.assertIn("not translated", out)

    def test_csv_warns_only(self):
        code, out = run("th.csv")
        self.assertEqual(code, 0, out)
        self.assertIn("(max 10)", out)

    def test_xliff(self):
        code, out = run("th.xlf")
        self.assertEqual(code, 1)
        self.assertIn("unit hello: missing {name}", out)


if __name__ == "__main__":
    unittest.main()
