---
id: doc:volume-7:pacman-transactions
title: Pacman Transaction Model
volume: 7
status: partial
model_refs:
  - package-manager:archlinux:pacman
  - layer:msys2:5-packages-and-repositories
evidence_refs:
  - evidence:pacman:pacman-8-2026-08-02
  - evidence:pacman:pacman-conf-5-2026-08-02
last_verified: 2026-08-02
---

# Pacman Transaction Model

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `package-manager:archlinux:pacman` |
| Kind | `package-manager` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Arch Linux |
| Environments | `msys` |
| Upstream | <https://www.archlinux.org/pacman/> |
| Packaged as | `package:msys2:pacman` |
| Version (observed) | 6.1.0-25 |
| License (observed) | spdx:GPL-2.0-or-later |
| Architecture (observed) | x86_64 |
| Installed size (observed) | 35.4 MB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:pacman:pacman-8-2026-08-02` — pacman(8) manual page (`primary`, retrieved 2026-08-02)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

A pacman transaction is the unit in which package state changes: targets are
selected, dependencies resolved, conflicts detected, and the whole set either
applied or not. This page documents the operations and the resolution
behavior between them.

## Architectural Classification

Pacman exposes operations as top-level flags. Three of them —
`-S` (sync), `-R` (remove), and `-U` (upgrade or install from a file) — are
the ones that mutate state, and pacman(8) groups the transaction options
under exactly those three. `-Q` (query) and `-D` (database) read or adjust
metadata without a package transaction.

## Responsibilities

- Selecting targets from the sync databases, a package file, or the local
  database, according to the operation.
- Resolving dependencies. Pacman checks a package's dependency fields to
  ensure dependencies are installed; `-d`/`--nodeps` skips the version
  checks, and package names are still checked even then.
- Comparing versions to decide what is out of date on `-Su`.
- Applying the resulting set of installs, upgrades, and removals.

## Boundaries

A transaction operates on the package universe the enabled sync databases
describe; it cannot install what no enabled repository provides. It changes
package state, not the payload behavior of what it installs.

Dependency resolution is over declared metadata. A package whose declared
dependencies are wrong resolves cleanly and still fails at runtime — which
is the gap this knowledge base's own catalog-derived dependency graph exists
to make visible.

## Interfaces

`-S`, `-R`, `-U`, `-Q`, `-D`, plus the transaction options that apply to the
first three.

## Dependencies

The [sync and local databases](PACMAN-DATABASE-MODEL.md) for the package
universe and installed state, and the
[repository configuration](PACMAN-REPOSITORY-LAYOUT.md) for which
repositories are in scope.

## Reverse Dependencies

Every package in every environment reaches an MSYS2 installation through a
transaction. The [MSYS environment](ENVIRONMENT-MSYS.md) hosts the pacman
that runs them.

## Configuration

Transaction behavior is influenced by `pacman.conf` and by per-invocation
options. Neither is captured for MSYS2 in this knowledge base.

## Initialization and Execution Flow

Target selection, then dependency resolution and conflict detection, then
application, with [hooks](PACMAN-HOOKS-AND-CACHE.md) running before and
after per their configuration.

## Runtime Behavior

Version comparison is documented with an explicit ordering:

```
1.0a < 1.0b < 1.0beta < 1.0p < 1.0pre < 1.0rc < 1.0 < 1.0.a < 1.0.1
```

That ordering is worth stating precisely because it is not lexicographic and
not intuitive: `1.0rc` sorts *before* `1.0`, and a suffixed `1.0.a` sorts
*after* bare `1.0`. Reasoning about whether a catalog snapshot's version is
newer than another cannot be done by string comparison.

## Compatibility and Variants

Pacman is the package manager for all six MSYS2 environments; the
environments differ in repository, not in transaction mechanism.

## Security Considerations

Signature verification happens against the policy documented on
[package signing](PACMAN-PACKAGE-SIGNING.md), and a transaction that
succeeds says nothing about repository trust beyond that policy. See
[Threat model and supply chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md).

## Failure Modes and Diagnostics

Unresolvable dependencies and file conflicts are the two characteristic
transaction failures. `--nodeps` suppresses the first by skipping version
checks rather than by satisfying them, which converts a build-time failure
into a runtime one.

## Evidence, Assumptions, and Open Questions

Mechanism is backed by the pacman manual pages
(`evidence:pacman:pacman-8-2026-08-02`,
`evidence:pacman:pacman-conf-5-2026-08-02`), which are authoritative for the
tool.

The standing caveat for all of Volume 7: those are the **Arch Linux** pages.
MSYS2 ships pacman but places its root, database, and cache under the MSYS2
installation rather than at the Arch defaults, and enables its own six
repositories. Documented behavior therefore establishes the mechanism, not
MSYS2's effective paths or configuration.

Open: no controlled observation of an MSYS2 pacman transaction, no captured
`pacman.conf`, and no recorded effective path for any of the locations named
here. The [repository trust model](PACMAN-REPOSITORY-TRUST-MODEL.md) states
the collection rules that would close this; they have not been executed.

## Related Objects

- [Pacman architecture](PACMAN-ARCHITECTURE.md)
- [Database model](PACMAN-DATABASE-MODEL.md)
- [Repository layout](PACMAN-REPOSITORY-LAYOUT.md)
- [Hooks and cache](PACMAN-HOOKS-AND-CACHE.md)
