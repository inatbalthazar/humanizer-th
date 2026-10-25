#!/usr/bin/env bash
# Build release files into dist/, one pair per skill:
#   <skill>.zip        skill folder for Claude.ai upload (one top-level folder with SKILL.md)
#   <skill>-prompt.md  every skill file in one Markdown file, for tools that don't read skill folders
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$root/scripts/validate_skill.py"

mkdir -p "$root/dist"
for dir in "$root"/skills/*/; do
  name="$(basename "$dir")"
  out="$root/dist/$name.zip"
  rm -f "$out"
  (cd "$root/skills" && zip -rq "$out" "$name" -x '*.DS_Store' -x '*__pycache__*')
  echo "Built dist/$name.zip ($(unzip -Z1 "$out" | wc -l | tr -d ' ') files)"
done

python3 "$root/scripts/build_prompt.py"
