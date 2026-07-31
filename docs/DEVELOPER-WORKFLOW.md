---
id: doc:volume-18:developer-workflow
title: AKB Developer Change Workflow
volume: 18
status: partial
model_refs: []
evidence_refs:
  - evidence:akb-process:developer-workflow-observed-run-2026-07-31
last_verified: 2026-07-31
---

# AKB Developer Change Workflow

## Developer Change Workflow

1. Start from synchronized `main` on a scoped `agent/` branch.
2. Make authored-model, importer, generator, test, or documentation changes
   without editing generated views by hand.
3. Run `py -3 -m unittest discover -s tests -q`, `py -3 tools/akb.py all`,
   `py -3 tools/build_explorer.py`, and `git diff --check`.
4. Stage only the intentional source and regenerated artifacts; commit a
   concise description; push; and open a draft PR.
5. Address CI failures from logs and rerun the relevant validation. When CI is
   green, merge and fast-forward local `main`.

## Observed run

On 2026-07-31, PR #123 (`observe-console-terminal-device`,
[Runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md) console-observation
change) exercised this workflow end to end and is cited here as this
row's first genuinely observed run, not merely documented steps:

| Step | What actually happened | Deviation from the documented steps above |
| --- | --- | --- |
| 1. Start from synced `main` on a scoped branch | Branched from `main` at `2da50e0` as `observe-console-terminal-device` | Branch name was not `agent/`-prefixed |
| 2. Author changes only | Edited two `docs/` pages and `model/graph.json`; no generated file was hand-edited | None |
| 3. Validate/test/generate | In a disposable `git worktree` (matching CI's clean-checkout behavior): `python tools/akb.py validate` (16,430 entities/77,233 relationships/39 claims/109 evidence, the clean-checkout baseline), `python tools/akb.py generate`, `python tools/build_explorer.py`, `python tools/build_catalog_views.py`, then `python -m unittest discover -s tests -v` (65 tests, all passed) | Ran the generator/explorer/catalog steps individually rather than via a single `tools/akb.py all` invocation; did not run `git diff --check` |
| 4. Stage, commit, push, open PR | Staged exactly the 3 intentionally-changed files, committed, pushed, opened PR #123 via `gh pr create` | The PR was opened directly rather than as a draft |
| 5. CI, merge, fast-forward | `gh pr checks --watch` showed the `validate` check go `pending` -> `pass`; merged with `gh pr merge --squash --delete-branch`; local `main` fast-forwarded via `git fetch` + `git merge --ff-only` to `998bbf6` | Used squash merge rather than an unspecified merge strategy |

This is single-run, single-operator evidence for one small documentation
change; it does not exercise a build/generator-code change, a failing-CI
recovery path, or a multi-committer PR review cycle.

## Related Views

- [Self-updating knowledge base](SELF-UPDATING-KNOWLEDGE-BASE.md)
- [Operator refresh workflow](OPERATOR-REFRESH-WORKFLOW.md)
- [Threat model and supply-chain analysis](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
