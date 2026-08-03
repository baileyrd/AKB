---
id: doc:volume-7:pacman-hooks-and-cache
title: Pacman Hooks and Cache
volume: 7
status: partial
model_refs:
  - package-manager:archlinux:pacman
  - layer:msys2:5-packages-and-repositories
evidence_refs:
  - evidence:pacman:pacman-8-2026-08-02
  - evidence:pacman:pacman-conf-5-2026-08-02
  - evidence:pacman:alpm-hooks-5-2026-08-02
last_verified: 2026-08-02
---

# Pacman Hooks and Cache

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

Two pieces of transaction machinery that sit either side of the install
itself: **hooks**, which run configured actions around a transaction, and
the **package cache**, which retains fetched archives locally.

## Architectural Classification

`alpm-hooks(5)` defines the hook file format. Hooks live in a hook directory
— documented default `/etc/pacman.d/hooks`, with additional directories
configurable — must end in `.hook`, and **run in alphabetical order of file
name, ignoring the suffix**.

The cache directory is documented as `/var/cache/pacman/pkg` by default,
overridable with `CacheDir` or `--cachedir`. Multiple cache directories may
be given and are tried in the order specified.

## Responsibilities

**Hooks** declare a `[Trigger]` and an `[Action]`:

| Section | Key | Required | Values |
| --- | --- | --- | --- |
| Trigger | `Operation` | yes, repeatable | `Install`, `Upgrade`, `Remove` |
| Trigger | `Type` | yes | `Path`, `Package` |
| Trigger | `Target` | yes, repeatable | path or package name |
| Action | `When` | yes | `PreTransaction`, `PostTransaction` |
| Action | `Exec` | yes | command |
| Action | `Depends` | no | package name |
| Action | `AbortOnFail` | no | PreTransaction only |
| Action | `NeedsTargets` | no | — |

`AbortOnFail` being PreTransaction-only is the structurally important
detail: a pre-transaction hook can stop the transaction, a post-transaction
hook cannot. Failure after the fact is reported, not prevented.

**The cache** retains fetched package archives so a reinstall or downgrade
need not re-download.

## Boundaries

Hooks run around a transaction, not inside package payloads — they are
distribution-level automation, distinct from a package's own install
scriptlets.

A cached archive is retained bytes, not an available package: presence in
the cache is not evidence the package is still offered upstream, a
distinction the [trust model](PACMAN-REPOSITORY-TRUST-MODEL.md) records as
a collection rule.

## Interfaces

`.hook` files in the hook directories; `CacheDir` in `pacman.conf` and
`--cachedir` per invocation.

## Dependencies

[Transactions](PACMAN-TRANSACTIONS.md), which hooks bracket and the cache
serves.

## Reverse Dependencies

Any distribution-level automation. MSYS2's own post-install automation is
not enumerated here.

## Configuration

Hook directories and `CacheDir`. Neither captured for MSYS2, so which hooks
an MSYS2 installation actually runs is unrecorded — a meaningful gap, since
hooks execute arbitrary commands during every transaction.

## Initialization and Execution Flow

Pre-transaction hooks whose triggers match run first and may abort; the
transaction applies; post-transaction hooks run.

## Runtime Behavior

Alphabetical ordering ignoring the suffix means hook file names are
load-bearing: renaming a hook changes when it runs relative to others, with
no other signal that ordering changed.

## Compatibility and Variants

The mechanism is pacman's and is the same across environments; the hook set
is installation-specific.

## Security Considerations

Hooks execute commands during transactions, so the hook set is part of the
installation's trust surface and this knowledge base has not inventoried it.
See [Threat model and supply chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md).

## Failure Modes and Diagnostics

A post-transaction hook failure leaves the transaction applied — the system
changed and the follow-up did not complete. A pre-transaction hook with
`AbortOnFail` is the only configuration that prevents rather than reports.

## Evidence, Assumptions, and Open Questions

Hook format is backed by `evidence:pacman:alpm-hooks-5-2026-08-02`; cache
behavior by `evidence:pacman:pacman-8-2026-08-02` and
`evidence:pacman:pacman-conf-5-2026-08-02`.

Standing Volume 7 caveat: these are the **Arch Linux** manual pages. MSYS2
places its hook and cache directories under the MSYS2 installation rather
than at the Arch defaults.

Open: no inventory of MSYS2's installed hooks, no captured `pacman.conf`, no
recorded cache path or contents.

## Related Objects

- [Transaction model](PACMAN-TRANSACTIONS.md)
- [Repository trust model](PACMAN-REPOSITORY-TRUST-MODEL.md)
- [Pacman architecture](PACMAN-ARCHITECTURE.md)
