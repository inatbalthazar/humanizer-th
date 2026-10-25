#!/usr/bin/env bash
# Build release files into dist/:
#   humanizer-th.zip        skill folder for Claude.ai upload (one top-level folder with SKILL.md)
#   humanizer-th-prompt.md  every skill file in one Markdown file, for tools that don't read skill folders
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
out="$root/dist/humanizer-th.zip"

python3 "$root/scripts/validate_skill.py"

mkdir -p "$root/dist"
rm -f "$out"
(cd "$root/skills" && zip -rq "$out" humanizer-th -x '*.DS_Store' -x '*__pycache__*')
echo "Built dist/humanizer-th.zip"
unzip -l "$out"

python3 "$root/scripts/build_prompt.py"
