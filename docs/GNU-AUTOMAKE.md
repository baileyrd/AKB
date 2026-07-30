---
id: doc:volume-8:gnu-automake
title: GNU Automake
volume: 8
status: partial
model_refs:
  - component:gnu:automake
  - package:msys2:automake-wrapper
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:gnu:automake-manual-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# GNU Automake

## Purpose

Automake generates portable `Makefile.in` files from higher-level
`Makefile.am` descriptions, commonly used alongside
[Autoconf](GNU-AUTOCONF.md). This page documents its architectural role and
a genuinely distinguishing MSYS2 packaging pattern: multiple Automake
versions installed side by side, dispatched by a wrapper script; see the
[official GNU Automake project page](https://www.gnu.org/software/automake/)
for the full `Makefile.am` syntax reference.

## Architectural Classification

`component:gnu:automake` is a GNU-userland component. It is **not**
packaged as a single `automake` package in this environment: it is
packaged as `package:msys2:automake-wrapper` (version `20260320-1`, license
`GPL-2.0-only`) plus eight separate versioned packages,
`automake1.11` through `automake1.18`, installed side by side
(`claim:component:automake:versioned-dispatch`). It belongs to the MSYS
environment.

## Responsibilities

- Generating `Makefile.in` (consumed by [Autoconf](GNU-AUTOCONF.md)'s
  `configure` substitution mechanism) from a project's `Makefile.am`.
- Dispatching `automake`/`aclocal` invocations to the correct installed
  version for a given project, since different projects can require
  different Automake major.minor versions.

## Boundaries

Automake generates `Makefile.in`; it does not itself run `configure` or
build anything (those are [Autoconf](GNU-AUTOCONF.md)'s and
[GNU Make](GNU-MAKE.md)'s roles respectively). This catalog snapshot
records no direct package-level dependency between `automake-wrapper` and
`autoconf2.71` — the two are used together at the project level by
Autotools convention, not linked by a declared MSYS2 package dependency.

## Interfaces

- `automake` (generate `Makefile.in` from `Makefile.am`), `aclocal`
  (collect m4 macros into `aclocal.m4` for [Autoconf](GNU-AUTOCONF.md) to
  consume), both dispatched through the version-selection mechanism
  described below.

## Dependencies

The catalog snapshot records ten `runtime-depends-on` edges for
`package:msys2:automake-wrapper`:

| Dependency | Package(s) | Architectural reason |
| --- | --- | --- |
| Versioned Automake releases | `automake1.11` through `automake1.18` (eight packages) | The actual Automake implementations the wrapper dispatches between, letting projects pinned to an older Automake version (via `AM_INIT_AUTOMAKE` or an explicit version request) still build in this environment (`claim:component:automake:versioned-dispatch`). |
| Wrapper script interpreter | `package:msys2:bash` | The dispatch wrapper itself is a shell script. |
| Version-detection helper | `package:msys2:gawk` | Plausibly used by the wrapper to parse a project's requested Automake version from its build files, consistent with the wrapper's Gentoo `autotools-wrappers` origin; this specific mechanism is recorded at medium confidence pending direct inspection of the wrapper script's source. |

The `automake-wrapper` package `provides` and `conflicts` with a generic
`automake` capability, meaning it — not any single versioned
`automakeN.NN` package — is what other packages depend on when they
declare a generic `automake` build requirement.

## Reverse Dependencies

The snapshot records 6 relationships targeting
`package:msys2:automake-wrapper`. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

`Makefile.am` is the project's Automake input; `AM_INIT_AUTOMAKE` in
`configure.ac` commonly declares required options and, implicitly by
project convention, the Automake version a project was authored against —
the version-selection input the wrapper's dispatch mechanism is designed
around.

## Initialization and Execution Flow

Invoking `automake` runs the wrapper script, which selects and execs the
appropriate versioned `automakeN.NN` binary as a child process — an extra
indirection layer not present in any other tool documented in this volume.
As an MSYS-dependent process, this is adapted from POSIX semantics onto
Windows process primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

Which versioned Automake actually runs for a given invocation depends on
the wrapper's version-detection logic succeeding; a project without a
clear version declaration may resolve to a default version that does not
match what the project was actually authored against, a documented general
risk of version-dispatch wrapper designs.

## Compatibility and Variants

The eight side-by-side versions (1.11 through 1.18) reflect real behavioral
differences across Automake releases that this packaging approach
accommodates directly, rather than forcing every project in the ecosystem
onto a single Automake version.

## Security Considerations

`Makefile.am`/generated `Makefile.in` processing from an untrusted source
carries the same general risk class already noted for
[GNU Autoconf](GNU-AUTOCONF.md#security-considerations) and
[GNU Make](GNU-MAKE.md#security-considerations). See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review has
been performed for the recorded `20260320-1` wrapper version or the
individual `automake1.11`–`automake1.18` versions.

## Failure Modes and Diagnostics

An `automake`/`aclocal` invocation behaving unexpectedly should first be
checked against which versioned Automake the wrapper actually dispatched
to, per Runtime Behavior above, before assuming a defect in Automake
itself.

## Evidence, Assumptions, and Open Questions

Automake's own generation model is backed by the official GNU Automake
project page (`evidence:gnu:automake-manual-2026-07-30`); the wrapper
mechanism itself is attributable to the Gentoo `autotools-wrappers`
project recorded as `automake-wrapper`'s own `project_url` in the catalog.
Package identity, version, and the versioned-dispatch architecture are
backed by the pacman catalog snapshot (`evidence:catalog:current`) via
`claim:component:automake:versioned-dispatch`. Open: the exact mechanism
the wrapper uses to select a version (and `gawk`'s precise role in it) is
a medium-confidence inference pending direct inspection of the wrapper
script's source.

## Related Objects

- [MSYS2 Toolchain Role Model](TOOLCHAIN-ROLE-MODEL.md)
- [MSYS2 Build System Role Model](BUILD-SYSTEM-ROLE-MODEL.md)
- [GNU Autoconf](GNU-AUTOCONF.md)
- [GNU Libtool](GNU-LIBTOOL.md)
- [GNU Make](GNU-MAKE.md)
