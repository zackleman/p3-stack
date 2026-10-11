#!/usr/bin/env python3
"""Import the reviewed, portable subset of a pinned pstack revision."""

import argparse
from pathlib import Path
import re
import subprocess

REVISION = "4bf3e083c6dec126e254f96181b84a105b6e3e70"
NAMES = {name: f"p3-{name}" for name in (
    "arena", "blast-radius", "bro", "tdd", "teach", "unslop"
)}
FILES = [
    "skills/principle-build-the-lever/SKILL.md",
    "skills/principle-encode-lessons-in-structure/SKILL.md",
    "skills/principle-explain-the-number/SKILL.md",
    "skills/principle-minimize-reader-load/SKILL.md",
    "skills/principle-model-the-domain/SKILL.md",
    "skills/principle-never-block-on-the-human/SKILL.md",
    "skills/principle-redesign-from-first-principles/SKILL.md",
    "skills/principle-subtract-before-you-add/SKILL.md",
    "skills/principle-test-behavior-not-implementation/SKILL.md",
    "skills/principle-type-system-discipline/SKILL.md",
    "skills/benchmark-checklist/SKILL.md",
    "skills/technical-writing/SKILL.md",
    "skills/unslop/SKILL.md",
    "skills/why/references/epistemics.md",
    "skills/why/references/sources/code-archaeology.md",
    "skills/why/references/sources/datadog.md",
    "skills/why/references/sources/sentry.md",
    "skills/ketchup/SKILL.md",
    "skills/poteto-help/references/prompting.md",
    "skills/poteto-help/references/recipes.md",
]


def adapt(text):
    text = text.replace("poteto-mode", "p3-mode")
    text = text.replace("/loop until done", "schedule checks until done")
    text = text.replace("give `/loop` that predicate", "give `schedule_task` that predicate")
    for old, new in NAMES.items():
        text = re.sub(
            rf"(/|\*\*|`|\bname: ){old}(?![\w-])",
            lambda match: match[1] + new,
            text,
        )
    for role in ("arena runners", "arena cross-judge pool"):
        text = text.replace("p3-" + role, role)
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, help="local cursor/plugins checkout")
    parser.add_argument("--check", action="store_true", help="compare without writing")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    mismatches = []
    for relative in FILES:
        source = subprocess.check_output(
            ["git", "show", f"{REVISION}:pstack/{relative}"],
            cwd=args.checkout, text=True,
        )
        target = root / adapt(relative).replace("poteto-help", "p3-help")
        content = adapt(source)
        if args.check:
            if not target.exists() or target.read_text() != content:
                mismatches.append(str(target.relative_to(root)))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
    if mismatches:
        parser.exit(1, "Imported files differ:\n" + "\n".join(mismatches) + "\n")
    print(f"{'Verified' if args.check else 'Imported'} {len(FILES)} files from {REVISION}")


if __name__ == "__main__":
    main()
