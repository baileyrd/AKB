---
id: doc:volume-19:operator-refresh-workflow
title: AKB Operator Refresh Workflow
volume: 19
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-30
---

# AKB Operator Refresh Workflow

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
- [Developer change workflow](DEVELOPER-WORKFLOW.md)
- [Threat model and supply-chain analysis](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
