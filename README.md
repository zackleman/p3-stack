# p3-stack

p3-stack is [pstack](https://github.com/cursor/plugins/tree/main/pstack) rebuilt for T3 Code. Same engineering discipline, native T3 orchestration.

pstack is poteto's answer to AI slop code. It turns an agent into an engineering team: one mode skill that routes to playbooks, principles that ground every decision, and verification strict enough that you can parallelize with confidence. p3-stack keeps that system and rewires the mechanics to T3 Code's primitives:

- **Delegation.** `delegate_task` child agents replace Cursor's Task tool, with per-role providers and models resolved from `orchestrator_capabilities`. Cross-model panels are native.
- **Worktrees.** `t3_thread_launch` binds a worker to its own worktree and branch. One writer per worktree, enforced by the app instead of by advice.
- **Watching.** `watch_pull_request` wakes the thread when checks finish, someone comments, or the branch conflicts. No polling loops.
- **Scheduling.** `schedule_task` runs audits and overnight cadences even when no turn is active. No `/loop`.
- **Memory.** `t3_thread_read` and `t3_thread_search` replace mining Cursor transcript files.
- **Proof.** `preview_*` browser tools and `device_*` simulators replace external control skills. Screenshots and recordings land in the thread.

## Install

```bash
git clone https://github.com/zackleman/p3-stack.git
cd p3-stack
./install.sh
```

This fork is maintained at [zackleman/p3-stack](https://github.com/zackleman/p3-stack). Clone that repository to use these updates.

`install.sh` links every `skills/*` directory into `~/.agents/skills/`, where T3 Code reads skills. Use `./install.sh --project /path/to/repo` to install into a project's `.agents/skills/` instead. Existing files and links from other installations are preserved. Running the installer again leaves matching links intact.

Four skills use a prefix to coexist with the existing personal skill library: `/p3-arena`, `/p3-blast-radius`, `/p3-tdd`, and `/p3-teach`. Their references inside this fork use those names too. The upstream unslop is installed as `/unslop`. `/bro` comes from the personal skill library; this fork does not install a second bro skill.

These workflows use T3 Code tools. Other clients can discover the skills, but running the orchestration workflows requires T3 Code.

## Get started

1. Run `/setup-p3`. It reads `orchestrator_capabilities` and writes `p3-models.md`, mapping each role (code, judgment, the review panels) to a provider and model you actually have.
2. Use `/p3-mode` whenever you want rigorous work. It reads the request, picks a playbook, and runs the other skills as the steps need them.
3. Stuck or unsure which skill fits? Ask `/p3-help`.

## The mode

`p3-mode` routes every task. Its playbooks: investigation, bug fix, perf issue, hillclimb, runtime forensics, trace forensics, feature, refactoring, prototype, visual parity, authoring a skill, eval, babysit, shipping, autonomous run, orchestrate, autopilot-full, autopilot-stack, session pickup, pause safely, multi-phase plan, worktree cleanup, opening a PR.

## Skills

architect, p3-arena, automate-me, benchmark-checklist, p3-blast-radius, correct, create-verification-skill, figure-it-out, how, interrogate, ketchup, maintain-verification-skill, make-bot-ui, no-comments, p3-help, recall, reflect, setup-p3, show-me-your-work, swarm, p3-tdd, p3-teach, technical-writing, typescript-best-practices, unslop, why.

The [upstream comparison](docs/upstream-comparison.md) records what this fork imported and which platform-specific updates remain separate.

## Principles

The twenty-four principle skills are indexed inside `p3-mode` and referenced by the other skills by name.

## Credit

p3-stack adapts [pstack](https://github.com/cursor/plugins/tree/main/pstack) by [poteto](https://x.com/poteto). The skills, principles, and language are hers; the T3 Code rewiring is this repo's. MIT, see [LICENSE](LICENSE).
