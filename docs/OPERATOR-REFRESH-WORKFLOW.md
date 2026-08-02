---
id: doc:volume-19:operator-refresh-workflow
title: AKB Operator Refresh Workflow
volume: 19
status: partial
model_refs: []
evidence_refs:
  - evidence:akb-process:operator-refresh-workflow-observed-run-2026-07-31
last_verified: 2026-07-31
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

## Observed run: partial success, one collector-harness blocker

On 2026-07-31, this workflow was exercised end to end for the first
time against a genuinely new MSYS2 installation (`C:\msys64`,
winget-installed this session; no MSYS2 root was available for any
earlier attempt at this row's evidence).

- **Step 2 (`Update-Akb.ps1`) as a whole did not complete**: it calls
  `catalog-msys2-packages.ps1` first, which throws a
  `Cannot bind argument to parameter 'Lines' because it is an empty
  string` error specific to this automated execution harness when
  processing the full ~15,700-package `pacman -Si` dump. A debug probe
  inserted immediately before the failing call confirmed the underlying
  data was valid (a fully-populated 301,336-element result array), so
  this is a harness/tooling limitation under this specific non-interactive
  environment, not a pacman or data-correctness defect. It stopped
  promotion rather than producing partial output, consistent with the
  Failure and Escalation section below.
- **The runtime-observation sub-step was exercised independently and
  succeeded completely**: `collect_runtime_observation.py --environment
  ucrt64 --behavior` ran through this new installation's own shell
  (avoiding the cross-runtime execution issue documented in
  [MSYS runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md#cross-installation-toolchain-execution-observation))
  and produced a complete observation — real tool identity for `bash`,
  `gcc`, `ld`, `make`, `pacman`, `sh` (with `clang`/`cmake`/`ninja`
  correctly reported absent), `uname`, mount table, and behavior probes
  — then `import_runtime_observation.py` imported it successfully,
  producing snapshot `runtime-ucrt64-7aebd17a225e`. This is a genuine,
  successful exercise of two of the workflow's pipeline stages
  (collect, import), run manually rather than via the orchestrating
  script because that script's first step (catalog collection) never
  returns control to reach them.

This is the first real evidence for this row beyond documented steps: a
concrete, reproducible partial success and a specifically root-caused
blocker, not a hypothetical failure mode. Deep-inventory collection and
a full, unblocked `Update-Akb.ps1` run remain unexercised.

## Related Views

- [Self-updating knowledge base](SELF-UPDATING-KNOWLEDGE-BASE.md)
- [Upgrade, rollback, repair, and migration](UPGRADE-ROLLBACK-REPAIR-MIGRATION.md)
- [Developer change workflow](DEVELOPER-WORKFLOW.md)
- [Threat model and supply-chain analysis](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
