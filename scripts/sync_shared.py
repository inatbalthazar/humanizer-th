#!/usr/bin/env python3
"""Copy shared reference files from shared/ into each skill's references/.

Each skill folder must work on its own once installed, so shared files are
committed as copies. Edit the file in shared/, then run this script.

  python3 scripts/sync_shared.py          copy files
  python3 scripts/sync_shared.py --check  fail if any copy is out of date
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "shared"

# Which shared files each skill uses.
USES = {
    "humanizer-th": ["patterns.md", "registers.md", "word-swaps.md"],
    "localize-th": ["patterns.md", "registers.md", "word-swaps.md", "characters.md"],
    "script-th": ["patterns.md", "registers.md", "characters.md"],
}


def main():
    check = "--check" in sys.argv[1:]
    stale = []
    for skill, names in USES.items():
        refs = ROOT / "skills" / skill / "references"
        for name in names:
            src = (SHARED / name).read_bytes()
            dst = refs / name
            if dst.is_file() and dst.read_bytes() == src:
                continue
            if check:
                stale.append(str(dst.relative_to(ROOT)))
            else:
                refs.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(src)
                print(f"Updated {dst.relative_to(ROOT)}")
    if stale:
        print("Out of date with shared/ (edit shared/, then run scripts/sync_shared.py):")
        for path in stale:
            print(f"  - {path}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
