#!/usr/bin/env bash
# Install the Thai skills (humanizer-th, localize-th, script-th) into every
# AI tool found on this machine.
#
#   curl -fsSL https://raw.githubusercontent.com/inatbalthazar/humanizer-th/main/install.sh | bash
#
# Options (after "bash -s --" when piping):
#   --skill NAME   install or remove only this skill (repeatable)
#   --target DIR   install into DIR only (DIR/<skill>)
#   --uninstall    remove the skills from every location below
#
# Environment:
#   HUMANIZER_TH_REF   branch or tag to install (default: main)
#   HUMANIZER_TH_SRC   local skills/ folder to copy instead of downloading
set -euo pipefail

repo="inatbalthazar/humanizer-th"
ref="${HUMANIZER_TH_REF:-main}"
all_skills=(humanizer-th localize-th script-th)
skills=()
target=""
uninstall=0

while [ $# -gt 0 ]; do
  case "$1" in
    --skill) skills+=("${2:?--skill needs a name}"); shift 2 ;;
    --target) target="${2:?--target needs a folder}"; shift 2 ;;
    --uninstall) uninstall=1; shift ;;
    -h|--help) sed -n '2,15p' "$0" 2>/dev/null || true; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done
[ ${#skills[@]} -eq 0 ] && skills=("${all_skills[@]}")
for s in "${skills[@]}"; do
  case " ${all_skills[*]} " in
    *" $s "*) ;;
    *) echo "Unknown skill: $s (choose from ${all_skills[*]})" >&2; exit 1 ;;
  esac
done

# Skill folders to install into. ~/.agents/skills is shared by Codex and
# other tools that follow the Agent Skills standard, so it is always used.
# The rest are used only when the tool's config folder already exists.
dests=()
if [ -n "$target" ]; then
  dests+=("$target")
else
  dests+=("$HOME/.agents/skills")
  [ -d "$HOME/.claude" ] && dests+=("$HOME/.claude/skills")
  [ -d "$HOME/.gemini" ] && dests+=("$HOME/.gemini/skills")
  [ -d "$HOME/.copilot" ] && dests+=("$HOME/.copilot/skills")
fi

if [ "$uninstall" -eq 1 ]; then
  for d in "${dests[@]}"; do
    for s in "${skills[@]}"; do
      if [ -d "$d/$s" ]; then
        rm -rf "${d:?}/$s"
        echo "Removed $d/$s"
      fi
    done
  done
  exit 0
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

if [ -n "${HUMANIZER_TH_SRC:-}" ]; then
  src="$HUMANIZER_TH_SRC"
else
  url="https://codeload.github.com/$repo/tar.gz/$ref"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$url" -o "$tmp/src.tar.gz"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "$tmp/src.tar.gz" "$url"
  else
    echo "Need curl or wget to download $repo" >&2
    exit 1
  fi
  tar -xzf "$tmp/src.tar.gz" -C "$tmp"
  src="$(find "$tmp" -mindepth 2 -maxdepth 2 -type d -name skills | head -n 1)"
fi

for s in "${skills[@]}"; do
  if [ ! -f "$src/$s/SKILL.md" ]; then
    echo "$s/SKILL.md not found in the download" >&2
    exit 1
  fi
done

for d in "${dests[@]}"; do
  mkdir -p "$d"
  for s in "${skills[@]}"; do
    rm -rf "${d:?}/$s"
    cp -R "$src/$s" "$d/$s"
    echo "Installed $d/$s"
  done
done

echo
echo "เสร็จแล้ว ถ้าเครื่องมือเปิดอยู่ ให้ปิดแล้วเปิดใหม่ก่อน แล้วลองพิมพ์"
echo "  \"เกลาให้หน่อย\" ตามด้วยข้อความภาษาไทย"
echo "  \"แปลซับนี้เป็นไทย\" ตามด้วยไฟล์ซับ"
echo "  \"เขียนบทละครสั้นเรื่อง...\""
