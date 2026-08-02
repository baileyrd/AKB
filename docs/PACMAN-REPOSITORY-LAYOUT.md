---
id: doc:volume-7:pacman-repository-layout
title: Pacman Repository Layout
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

# Pacman Repository Layout

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

Repository layout is how pacman learns what repositories exist, where their
databases and packages live, and which one wins when two offer the same
package. In MSYS2 this is what makes six environments addressable from one
control plane.

## Architectural Classification

`pacman.conf(5)` defines **repository sections**: each section is a name in
square brackets plus at least one location where packages can be found. The
six MSYS2 repositories — `msys`, `ucrt64`, `clang64`, `clangarm64`,
`mingw64`, `mingw32` — are such sections.

Directives are CamelCase and are not recognized otherwise: `noupgrade` and
`NOUPGRADE` both fail where `NoUpgrade` works. That is a documented
foot-gun, not a stylistic preference.

## Responsibilities

- Naming each repository and giving it at least one location, via `Server`
  or via `Include` of a mirrorlist file.
- Establishing precedence. The order of repositories in the configuration
  matters: repositories listed **first take precedence** when two provide
  the same package.
- Supplying the variables that expand into mirror URLs, notably `$repo` and
  `$arch`, so one mirrorlist line serves every repository and architecture.

## Boundaries

Repository configuration determines availability, not trust. A repository
being listed says nothing about whether its content verifies — that is
[signature policy](PACMAN-PACKAGE-SIGNING.md), configured separately and
per-repository.

Mirror reachability is likewise separate: successful download from a mirror
is not evidence of repository authority, a distinction the
[trust model](PACMAN-REPOSITORY-TRUST-MODEL.md) states as a collection rule.

## Interfaces

`[section]` headers, `Server = <url>`, `Include = <path>`, and the `$repo`
and `$arch` substitutions.

## Dependencies

Mirrors deliver the [sync databases](PACMAN-DATABASE-MODEL.md) and package
archives that repository sections point at.

## Reverse Dependencies

Every [transaction](PACMAN-TRANSACTIONS.md) resolves within the repositories
this configuration enables. This knowledge base's six
`repository:msys2:*` entities correspond to these sections.

## Configuration

`pacman.conf` plus whatever it includes. The MSYS2 file is not captured
here, so which repositories are enabled in a given installation, and in what
order, is not recorded.

## Runtime Behavior

Precedence has a practical consequence worth stating: because first-listed
wins, reordering repository sections silently changes which package a name
resolves to. Nothing about the package name changes, so the effect is
invisible in a transaction log that records only names and versions.

## Initialization and Execution Flow

Configuration is read at pacman start; `Include` files are read at the point
they appear, which is why include order participates in precedence.

## Compatibility and Variants

MSYS2's six repositories map one-to-one onto its six environments, which is
why environment selection and repository selection are the same decision
made in two places.

## Security Considerations

Per-repository `SigLevel` means trust policy can differ between sections of
the same file. See [package signing](PACMAN-PACKAGE-SIGNING.md).

## Failure Modes and Diagnostics

A package resolving to an unexpected environment's build is the
characteristic symptom of precedence, not of a packaging error. Check
section order before suspecting the repository.

## Evidence, Assumptions, and Open Questions

Mechanism is backed by the pacman manual pages
(`evidence:pacman:pacman-8-2026-08-02`,
`evidence:pacman:pacman-conf-5-2026-08-02`).

The standing caveat for all of Volume 7: those are the **Arch Linux** pages.
MSYS2 ships pacman but places its root, database, and cache under the MSYS2
installation rather than at the Arch defaults, and enables its own six
repositories. Documented behavior establishes the mechanism, not MSYS2's
effective paths or configuration.

Open: no captured MSYS2 `pacman.conf`, no recorded effective path, and no
controlled observation of a transaction. The
[repository trust model](PACMAN-REPOSITORY-TRUST-MODEL.md) states the
collection rules that would close this; they have not been executed.

## Related Objects

- [Pacman architecture](PACMAN-ARCHITECTURE.md)
- [Repository trust model](PACMAN-REPOSITORY-TRUST-MODEL.md)
- [Database model](PACMAN-DATABASE-MODEL.md)
- [Runtime environments](RUNTIME-ENVIRONMENTS.md)
