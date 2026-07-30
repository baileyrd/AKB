---
id: doc:volume-19:upgrade-rollback-repair-migration
title: Upgrade, Rollback, Repair, and Migration Guides
volume: 19
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-28
---

# Upgrade, Rollback, Repair, and Migration Guides

These are controlled operational guides, not a substitute for current upstream
release notes or local backup policy. Capture the environment, effective
configuration, package state, and AKB snapshot before making a material change.

## Upgrade

MSYS2 is a rolling release that supports full system upgrades. Run `pacman
-Suy` from the intended MSYS2 environment. When pacman requests that MSYS2
processes close for a core update, allow it, open a new terminal, and repeat
`pacman -Suy` to complete remaining packages. Review `.pacnew` and `.pacsave`
files with `pacdiff`; do not overwrite local configuration blindly.

Before and after the transaction, retain catalog/inventory snapshots and run
the AKB refresh. Compare package versions, owned files, imports, and unresolved
records before treating changed behavior as an architecture regression.

## Repair

1. Stop automated refresh/promotion after a failed package or evidence import.
2. Preserve the failure output, selected mirror, sync-database/archive hashes,
   effective configuration, and previous current projection.
3. For stale signature-key trust failures, follow the official recovery path:
   refresh existing keys with `pacman-key --refresh-keys`; if a new key remains
   required, update `msys2-keyring` with `pacman -Sy msys2-keyring`, then run
   the full `pacman -Suy` upgrade.
4. Re-run collection and promote a snapshot only after hash/count/schema
   validation succeeds. A repair must not convert missing or ambiguous data
   into inferred graph facts.

## Rollback

Treat rollback as a version-qualified restoration procedure, not a generic
`pacman` command. Identify the prior package/archive, its checksum, repository
and keyring context, dependent package constraints, local configuration, and
the target environment. Test restoration in a controlled copy where practical;
then refresh AKB evidence and record the resulting difference report. Retained
cache bytes are evidence of a prior download, not proof that a rollback remains
safe or compatible.

## Environment Migration

Moving from deprecated MINGW64 or MINGW32 to UCRT64/CLANG64 is a port. Select
the target environment deliberately, rebuild all objects/static libraries,
reinstall target-qualified dependencies, and validate APIs, ABI/CRT crossings,
DLL imports, and runtime behavior. Do not mix object files or static libraries
between MSVCRT and UCRT targets. Keep the old and new inventories separate
until comparison and acceptance testing are complete.

## Operational Checkpoints

| Checkpoint | Evidence to retain |
| --- | --- |
| Pre-change | Environment, package list, configuration origin, snapshot ID, backup/restore decision |
| Transaction | Command, pacman output, mirror/keyring outcome, changed config markers |
| Post-change | New snapshot ID, version/artifact/DLL differences, unresolved records, validation result |
| Acceptance | Build/runtime tests and explicit decision to retain, migrate, or restore |

The current official update procedure is documented by [MSYS2](https://www.msys2.org/docs/updating/);
environment selection and CRT migration constraints are documented in its
[environment guide](https://www.msys2.org/docs/environments/).

## Related Views

- [Pacman repository and trust model](PACMAN-REPOSITORY-TRUST-MODEL.md)
- [Runtime environments](RUNTIME-ENVIRONMENTS.md)
- [Self-updating knowledge base](SELF-UPDATING-KNOWLEDGE-BASE.md)
