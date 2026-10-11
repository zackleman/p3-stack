#!/usr/bin/env bash
# Install or update real p3-stack files as a Git subtree.
set -euo pipefail

TARGET_REPO="${HOME}/.agents/skills"
PREFIX="p3"
SOURCE="${P3_STACK_SOURCE:-https://github.com/zackleman/p3-stack.git}"

if [[ "${1:-}" == "--project" && "$#" == 2 ]]; then
  TARGET_REPO="$2"
  PREFIX=".agents/skills/p3"
elif [[ "$#" != 0 ]]; then
  printf 'usage: ./install.sh [--project /path/to/repo]\n' >&2
  exit 2
fi

TARGET_REPO="$(cd "$TARGET_REPO" && pwd -P)"
if [[ "$(git -C "$TARGET_REPO" rev-parse --show-toplevel)" != "$TARGET_REPO" ]]; then
  printf 'target must be the root of an existing Git repository\n' >&2
  exit 1
fi
if ! git -C "$TARGET_REPO" diff --quiet || ! git -C "$TARGET_REPO" diff --cached --quiet; then
  printf 'commit or save tracked changes before installing or updating p3-stack\n' >&2
  exit 1
fi

if [[ -e "$TARGET_REPO/$PREFIX" || -L "$TARGET_REPO/$PREFIX" ]]; then
  if [[ -L "$TARGET_REPO/$PREFIX" ]] || [[ -z "$(git -C "$TARGET_REPO" log -1 --format=%B --grep="^git-subtree-dir: $PREFIX$")" ]]; then
    printf 'existing %s is not a managed p3-stack subtree; leaving it untouched\n' "$PREFIX" >&2
    exit 1
  fi
  git -C "$TARGET_REPO" subtree pull --prefix="$PREFIX" "$SOURCE" main --squash -m 'chore: sync p3-stack subtree'
else
  git -C "$TARGET_REPO" subtree add --prefix="$PREFIX" "$SOURCE" main --squash -m 'feat: add p3-stack subtree'
fi

printf 'p3-stack files are tracked under %s/%s\n' "$TARGET_REPO" "$PREFIX"
