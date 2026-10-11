#!/usr/bin/env bash
# Install p3-stack skills for T3 Code.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${HOME}/.agents/skills"

if [[ "${1:-}" == "--project" ]]; then
  TARGET="${2:?usage: ./install.sh --project /path/to/repo}/.agents/skills"
  [[ "$#" == 2 ]] || { printf 'usage: ./install.sh [--project /path/to/repo]\n' >&2; exit 2; }
elif [[ "$#" != 0 ]]; then
  printf 'usage: ./install.sh [--project /path/to/repo]\n' >&2
  exit 2
fi

mkdir -p "$TARGET"
installed=0
skipped=0

for skill in "$ROOT"/skills/*/; do
  name="$(basename "$skill")"
  source="${skill%/}"
  if [[ -L "$TARGET/$name" ]]; then
    if [[ "$(readlink "$TARGET/$name")" == "$source" ]]; then
      installed=$((installed + 1))
      continue
    fi
    printf 'skip %s (existing symlink belongs to another installation)\n' "$name"
    skipped=$((skipped + 1))
    continue
  elif [[ -e "$TARGET/$name" ]]; then
    printf 'skip %s (exists and is not a symlink)\n' "$name"
    skipped=$((skipped + 1))
    continue
  fi
  ln -s "$source" "$TARGET/$name"
  installed=$((installed + 1))
done

printf 'linked %d skills into %s' "$installed" "$TARGET"
if [[ "$skipped" -gt 0 ]]; then
  printf ' (%d skipped)' "$skipped"
fi
printf '\n'
