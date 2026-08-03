---
id: doc:volume-7:pacman-database-model
title: Pacman Database Model
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

# Pacman Database Model

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

Pacman keeps two kinds of database: **sync** databases describing what each
enabled repository offers, and a **local** database recording what is
actually installed. Nearly every pacman question resolves to one or the
other, and conflating them is the common error.

## Architectural Classification

Both live under the database directory, which pacman(8) documents as
`/var/lib/pacman` by default and `pacman.conf(5)` allows to be overridden
with `DBPath`. In an MSYS2 installation this sits under the MSYS2 root
rather than at the Arch default; the effective path is not recorded here.

## Responsibilities

- **Sync databases** provide the package universe dependency resolution
  works against — the set of packages, versions, and declared dependencies
  each enabled repository offers. `-F`/file search operates only over
  packages that are part of the sync databases.
- **The local database** records installed packages: their files, ownership
  metadata, dependencies, conflicts, and install date. `-Q` queries it, and
  `-Qk` checks that files it claims are present actually are.

## Boundaries

A sync database describes availability, not installation. The local database
describes installation, not availability. A package can be in one and not
the other in both directions — installed but no longer offered, or offered
but not installed.

This knowledge base's `model/catalog/current.json` is derived from sync
database content, which is why it describes 15,711 packages while the
[deep inventory](DEEP-INVENTORY-CONTRACT.md) — which needs installed
payloads — covers 2.

## Interfaces

`-S` refreshes and consumes sync databases; `-Q` reads the local database;
`-D` operates on the databases directly and can check them for internal
consistency.

## Dependencies

The [repository configuration](PACMAN-REPOSITORY-LAYOUT.md) determines which
sync databases exist. Their bytes arrive from mirrors.

## Reverse Dependencies

[Transactions](PACMAN-TRANSACTIONS.md) resolve against both. This knowledge
base's entire package catalog derives from sync database content.

## Configuration

`DBPath` in `pacman.conf`, or `-b`/`--dbpath` per invocation. Both are
absolute paths to which the root path is not prepended.

## Initialization and Execution Flow

Sync databases are refreshed on demand rather than continuously; the local
database is updated as part of each transaction.

## Runtime Behavior

A stale sync database yields resolution against a stale universe. This is
the mechanism behind the snapshot discipline this knowledge base already
applies: a catalog snapshot is a point-in-time copy of sync database
content, which is why every catalog-derived claim here is
snapshot-qualified.

## Compatibility and Variants

Six repositories mean six sync databases in an MSYS2 installation, one local
database shared across all environments — the reason
[MSYS](ENVIRONMENT-MSYS.md) is the control plane for every environment.

## Security Considerations

Database signature policy is separate from package signature policy; see
[package signing](PACMAN-PACKAGE-SIGNING.md).

## Failure Modes and Diagnostics

A package that "should exist" but does not resolve usually means a stale or
unsynced database rather than a missing package. `-Qk` is the documented
check for local database claims that no longer match the filesystem.

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

- [Transaction model](PACMAN-TRANSACTIONS.md)
- [Repository layout](PACMAN-REPOSITORY-LAYOUT.md)
- [Repository package inventory](REPOSITORY-PACKAGE-INVENTORY.md)
