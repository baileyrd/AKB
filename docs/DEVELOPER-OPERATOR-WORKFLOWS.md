---
id: doc:volume-20:developer-operator-workflows
title: AKB Developer and Operator Workflows
volume: 20
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-28
---

# AKB Developer and Operator Workflows

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

## Operator Refresh Workflow

1. Confirm the MSYS2 root, selected runtime environment, inventory scope, and
   whether package/file databases may be synchronized.
2. Run `pwsh ./tools/Update-Akb.ps1 -Msys2Root C:\msys64` for the standard
   catalog, deep inventory, runtime observation, validation, and generation
   pipeline. Use `-SkipDatabaseRefresh`, `-SkipDeepInventory`, or
   `-SkipRuntimeObservation` only when their evidence scope is intentionally
   excluded and recorded.
3. For repository-wide file ownership, use `-InventoryScope repositories`;
   optionally supply a statically parsed recipes checkout with `-RecipeRoot`.
4. Inspect snapshot/change/unresolved records. Promote or publish only after
   all imports validate and the current views reflect the expected scope.

## Scheduled Operation

Preview registration with:

```powershell
pwsh ./tools/Register-AkbRefreshTask.ps1 -DailyAt 03:00 -Msys2Root C:\msys64 -WhatIf
```

Register only after reviewing the resolved PowerShell executable, update-script
path, account context, and MSYS2 root. The task uses `IgnoreNew` for overlapping
instances; investigate a missed/failed run before manually replacing evidence.

## Failure and Escalation

Stop promotion on collector, hash/count/schema, importer, or generation
failure. Retain the preceding current projection, capture command output and
input scope, and inspect unresolved/warning records. Do not retry by deleting
snapshots or bypassing validation. Follow the operational migration guide for
package/keyring repair and use a scoped PR for code or contract changes.

## Related Views

- [Self-updating knowledge base](SELF-UPDATING-KNOWLEDGE-BASE.md)
- [Upgrade, rollback, repair, and migration](UPGRADE-ROLLBACK-REPAIR-MIGRATION.md)
- [Threat model and supply-chain analysis](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
