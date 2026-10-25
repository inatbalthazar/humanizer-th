#!/usr/bin/env bash
# Build humanizer-th.zip for upload to Claude.ai.
# The zip holds a single top-level folder, humanizer-th/, with SKILL.md inside.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
out="$root/humanizer-th.zip"

python3 "$root/scripts/validate_skill.py"

rm -f "$out"
cd "$root/skills"
zip -rq "$out" humanizer-th -x '*.DS_Store' -x '*__pycache__*'
echo "Built $out"
unzip -l "$out"
