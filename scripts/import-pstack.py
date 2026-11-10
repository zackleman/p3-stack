#!/usr/bin/env python3
"""Import the reviewed, portable subset of a pinned pstack revision."""

import argparse
from pathlib import Path
import subprocess

REVISION = "236e5481d05cbadc315b374a5de54971858c27bb"
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
# Upstream hides these from the model, but other skills tell agents to load
# them, so they must stay invocable.
MODEL_INVOCABLE = {"skills/unslop/SKILL.md"}


def adapt(text):
    text = text.replace("poteto-mode", "p3-mode")
    text = text.replace("/loop until done", "schedule checks until done")
    text = text.replace("give `/loop` that predicate", "give `schedule_task` that predicate")
    text = text.replace("[`/bro`](../bro/SKILL.md)", "the personal `/bro` skill")
    # Cursor's /visualize skill has no p3 counterpart; T3 renders charts with html_render.
    text = text.replace("a chart or diagram from `/visualize`", "a chart or diagram shown with `html_render`")
    text = text.replace("a `/visualize` chart for numbers", "an `html_render` chart for numbers")
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
        if relative in MODEL_INVOCABLE:
            content = content.replace("disable-model-invocation: true\n", "", 1)
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
