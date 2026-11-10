# Upstream comparison

Compared on October 10, 2026. The starting p3-stack revision is [`09909eb`](https://github.com/uzairansaruzi/p3-stack/commit/09909eb). The Cursor repository was inspected at `4bf3e083c6dec126e254f96181b84a105b6e3e70`. Its latest pstack change is [`978ca6e`](https://github.com/cursor/plugins/commit/978ca6e), which adds `/ketchup`.

p3-stack is an independent adaptation, not a Git fork of cursor/plugins. Compare `pstack/` against the corresponding skill files rather than merging the repositories.

The October 28, 2026 review used Cursor revision [`23ab063`](https://github.com/cursor/plugins/commit/23ab063af02bb9b9c97936b0563879dd6bf21a05). It imported the formal-verification pair, `/statechart`, `/in-your-own-words`, `/sharpen`, and `/ketchup-video` as a portable bundle. Cursor-specific plugin manifests, model slugs, and harness instructions remain out of p3.

The November 9, 2026 sync brought every existing p3 file up to Cursor revision [`236e548`](https://github.com/cursor/plugins/commit/236e5481d05cbadc315b374a5de54971858c27bb); pstack has not changed since `c742dd6` (October 27). It ports the workflow distillation that the October 10 review deferred, the agentic Orchestrate rewrite (#1043, without the `orch` scripts), the effort and speed rule for delegates (#613, through `delegate_task` `target.options`), and the shorter interrogate, which drops its four reference files. The importer now pins `236e548`, keeps `/unslop` model-invocable, and maps `/visualize` to `html_render`. The original `uzairansaruzi/p3-stack` has no commits after `09909eb`.

| Upstream change | Decision in this fork |
| --- | --- |
| [Prompt distillation, #538](https://github.com/cursor/plugins/commit/00b14f1) | Import shorter versions of ten principles, benchmarking, technical writing, unslop, and four investigation references. |
| [Catch-up skill, #539](https://github.com/cursor/plugins/commit/978ca6e) | Add `/ketchup` and link it from `/p3-help`. Keep its turn read-only. |
| [Prompting references, #507](https://github.com/cursor/plugins/commit/807c031) | Add prompting guidance and recipes. Replace the mode name and recurring-check instructions with T3 equivalents. |
| [Typed help invocation, #506](https://github.com/cursor/plugins/commit/00b52d9) | Make `/p3-help` explicit and correct its guidance about invocation. |
| [Missing model setup prompt, #509](https://github.com/cursor/plugins/commit/1e56b29) | Keep the existing T3 setup check and role discovery. Users run `/setup-p3` in T3 to resolve the models available there. |
| [Model default changes, #511](https://github.com/cursor/plugins/commit/df58112) | Keep models capability-driven through `orchestrator_capabilities` and `p3-models.md`. Do not import Cursor model slugs. |
| Workflow distillation in #538 | Deferred on October 10, ported on November 9: each of architect, arena, how, interrogate, reflect, why, and the mode playbooks takes upstream's wording and structure, then the T3 delegation, worktree, watching, and model-role wiring is reapplied. |
| Cursor guide and plugin manifest changes | Leave out Cursor installation, custom modes, and plugin metadata. |

## Reproduce the import

The importer copies exactly twenty reviewed files from a pinned revision and applies the local names and T3 prompting changes. It does not import arbitrary future revisions.

```sh
python3 scripts/import-pstack.py /path/to/cursor-plugins
python3 scripts/import-pstack.py /path/to/cursor-plugins --check
```

The separate `/p3-help` edits preserve its T3 instructions. Four overlapping skill names stay plain so the fork shares the personal skills instead of creating duplicate prefixed commands. The installer imports real files as a Git subtree and leaves an existing unmanaged directory untouched.

On October 11, 2026, Zack chose to keep the personal `/bro` and remove `/p3-bro`, keep both TDD and teaching versions, and replace the personal unslop with the upstream version under `/unslop`. Bro references now resolve by name to the personal library, and the importer preserves this choice.

The personal installation now uses `p3/` as a Git subtree instead of per-skill symlinks. The skills repository records the complete contents, while subtree pull and push synchronize with the independent fork.
