---
id: doc:volume-18:developer-workflow
title: AKB Developer Change Workflow
volume: 18
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-30
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

## Related Views

- [Self-updating knowledge base](SELF-UPDATING-KNOWLEDGE-BASE.md)
- [Operator refresh workflow](OPERATOR-REFRESH-WORKFLOW.md)
- [Threat model and supply-chain analysis](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
