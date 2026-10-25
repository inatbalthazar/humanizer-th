#!/usr/bin/env bash
# Install humanizer-th into every AI tool found on this machine.
#
#   curl -fsSL https://raw.githubusercontent.com/inatbalthazar/humanizer-th/main/install.sh | bash
#
# Options (after "bash -s --" when piping):
#   --target DIR   install into DIR only (DIR/humanizer-th)
#   --uninstall    remove humanizer-th from every location below
#
# Environment:
#   HUMANIZER_TH_REF   branch or tag to install (default: main)
#   HUMANIZER_TH_SRC   local skill folder to copy instead of downloading
set -euo pipefail

repo="inatbalthazar/humanizer-th"
ref="${HUMANIZER_TH_REF:-main}"
name="humanizer-th"
target=""
uninstall=0

while [ $# -gt 0 ]; do
  case "$1" in
    --target) target="${2:?--target needs a folder}"; shift 2 ;;
    --uninstall) uninstall=1; shift ;;
    -h|--help) sed -n '2,13p' "$0" 2>/dev/null || true; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
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
    if [ -d "$d/$name" ]; then
      rm -rf "${d:?}/$name"
      echo "Removed $d/$name"
    fi
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
  src="$(find "$tmp" -mindepth 3 -maxdepth 3 -type d -path "*/skills/$name" | head -n 1)"
fi

if [ ! -f "$src/SKILL.md" ]; then
  echo "SKILL.md not found in the download" >&2
  exit 1
fi

for d in "${dests[@]}"; do
  mkdir -p "$d"
  rm -rf "${d:?}/$name"
  cp -R "$src" "$d/$name"
  echo "Installed $d/$name"
done

echo
echo "เสร็จแล้ว ลองพิมพ์ \"เกลาให้หน่อย\" แล้ววางข้อความภาษาไทย"
echo "ถ้าเครื่องมือเปิดอยู่ ให้ปิดแล้วเปิดใหม่ก่อน"
