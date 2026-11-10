---
name: orchestrate
description: Run a multi-day, many-PR program as a standing coordinator that decides which agent does each piece of work and checks what each one produces.
---

### Orchestrate

**You run the program, never the code. Decide which agent does each piece of work, then check what each one produces.** For a standing project handed to one coordinator thread: multi-day, many stacked PRs, dozens to hundreds of delegated workers, few human turns. One task driven to a predicate is Autonomous run. One ambitious run that needs a bespoke workflow is figure-it-out. Work that one agent could finish inside the session's budget is not a program.

Run it with your own tools. Spawn workers with `delegate_task` (`mode: "async"`) and drain them with `task_status`. Keep the program's state in `orchestrate/<project-slug>/notes.md` in the current project and in the PRs linked to this thread. Call `link_pull_request` for every PR the moment it exists; `list_thread_pull_requests` returns the stack bottom to top. Watch each PR with `watch_pull_request`: arm it, end the turn, triage on wake. When no PR event will wake you, a `schedule_task` interval is the heartbeat. Call no scripts, run no polling loops, and never relay messages or status between agents.

#### Topology

- **One owner per PR.** The owner is the only writer of its branch and carries the PR from build to merge. Launch it with `t3_thread_launch` and `workspaceStrategy` `{"type":"worktree","baseRef":...,"branch":...}`, one writer per worktree. Only the owner pushes, rebases, or retargets it. Closing or retargeting a base PR orphans every PR above it, so the owner does that only on your call. You never author or edit code. Conflicted merges, chain rebases, and fixes go to owners.
- **A fresh worker for each independent task.** Its brief carries everything it needs, including each upstream report it depends on, pasted in full. T3 child agents get only the brief, never your context, and can't see their siblings. A worker is a `delegate_task` child unless it needs its own thread, worktree, or branch, such as a `preview_*` or `device_*` runtime check or auth that exists only in one checkout. Pick each worker's role from `p3-models.md`, per the Subagents section of `p3-mode`.
- **A sub-coordinator only when one area has many parallel workers.** It is a `t3_thread_launch` thread that owns that area's workers and briefs and sends you one rollup, never raw worker reports. Stop at three levels: you, sub-coordinators, and workers. Keep about ten workers in flight per coordinator, and start the next one as each finishes instead of waiting on a whole batch.
- **Reuse a worker's built state only when new work needs it,** such as its checkout, uncommitted changes, or a running process. Launch the new thread into that worktree with `{"type":"existing_worktree","worktreePath":...}` once the old one stops writing. Message a worker with `t3_thread_send` only for a follow-up on the same work. Never message one to check on it, because a message restarts an idle agent.
- **Each PR gets a verifier that isn't its author,** on a different model family. The owner merges only on that verifier's pass at the current head.
- **Start with one unit.** Take it through brief, owner, verifier, and merge before you fan out, so a flaw in the brief costs one agent instead of fifty. On near-identical cheap units, the first unit is that test.

#### Supervision

- **Each brief names the evidence that proves the work is done,** such as a command and its expected output, a `preview_*` or `device_*` check, or an artifact. It also names the goal, the paths the worker may and may not write, and the actions it must not take. If you can't name the evidence, the unit isn't scoped yet.
- **Read the diff or the artifact, not only the worker's summary.** Green CI is an input to a verdict, not a verdict. Behavioral work needs more than a type check. A verdict covers one head SHA, so a new push needs a new verdict. Read a sample of each sub-coordinator's briefs with `t3_thread_read` while its workers run, and fix its instructions when one fails.
- **Send back work that drifts from scope or grows past what was asked.** Keep only the fixes that block the program, and park the rest as follow-ups.
- **Check a PR's live state before you report on it,** with `gh pr view` and `gh pr checks`, not the worker's last report. Account for every worker you spawned as done, replaced, or absorbed into another worker's scope.
- **Stop or replace a worker that stalls or loops.** Judge it by its pushes and PR activity, not its status text. Stop it with `task_cancel` or `t3_thread_interrupt`. Retry by cause: a smaller scope after a context or memory limit, the same brief after a dropped connection, and a different model after a tool error. After two retries, drop the unit and replan around it. When a stopped worker returns late, check its result against the PR's current state, and hand any unique findings to a fresh worker.
- **Ask the user only for a real decision or a blocker,** such as an irreversible action, a product or preference call that no experiment settles, or a dead end that survived a replan. Rebase mechanics, retries, CI flakes, review triage, and "should I keep going" never reach the user.

**Reply:** what landed against the goal, each PR's live state and verdict with its link, what was dropped and why, and the decisions waiting on the user.
