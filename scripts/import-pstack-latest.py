#!/usr/bin/env python3
"""Import the reviewed formal-verification and recap skills from pstack."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess


REVISION = "23ab063af02bb9b9c97936b0563879dd6bf21a05"
SKILL_FILES = (
    "create-formal-verification-skill/SKILL.md",
    "in-your-own-words/SKILL.md",
    "ketchup-video/SKILL.md",
    "maintain-formal-verification-skill/SKILL.md",
    "sharpen/SKILL.md",
)
STATECHART_PREFIX = "statechart/"


def git(checkout: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=checkout)


def adapt(path: str, content: bytes) -> bytes:
    if path == "create-formal-verification-skill/SKILL.md":
        return content.replace(b"the pstack [`/statechart`]", b"the p3-stack [`/statechart`]")
    if path == "statechart/scripts/package.json":
        return content.replace(b"@cursor-skill/statechart", b"@p3-stack/statechart")
    return content


def source_paths(checkout: Path) -> list[str]:
    output = git(checkout, "ls-tree", "-r", "--name-only", REVISION, "pstack/skills/statechart")
    return [line.removeprefix("pstack/skills/") for line in output.decode().splitlines()]


def source_mode(checkout: Path, relative: str) -> int:
    path = f"pstack/skills/{relative}"
    line = git(checkout, "ls-tree", REVISION, path).decode().split(maxsplit=1)[0]
    return int(line, 8)


def write_file(checkout: Path, root: Path, relative: str, check: bool) -> bool:
    source = f"pstack/skills/{relative}"
    target = root / "skills" / relative
    content = adapt(relative, git(checkout, "show", f"{REVISION}:{source}"))
    if check:
        return target.exists() and target.read_bytes() == content
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    target.chmod(source_mode(checkout, relative))
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, help="local cursor/plugins checkout")
    parser.add_argument("--check", action="store_true", help="compare without writing")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    files = list(SKILL_FILES) + source_paths(args.checkout)
    mismatches = [relative for relative in files if not write_file(args.checkout, root, relative, args.check)]
    if mismatches:
        parser.exit(1, "Imported files differ:\n" + "\n".join(mismatches) + "\n")
    verb = "Verified" if args.check else "Imported"
    print(f"{verb} {len(files)} files from {REVISION}")


if __name__ == "__main__":
    main()
