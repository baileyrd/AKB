---
id: doc:volume-8:gnu-autoconf
title: GNU Autoconf
volume: 8
status: partial
model_refs:
  - component:gnu:autoconf
  - package:msys2:autoconf2.71
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:gnu:autoconf-manual-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# GNU Autoconf

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `component:gnu:autoconf` |
| Kind | `component` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Free Software Foundation |
| Environments | `msys` |
| Upstream | <https://www.gnu.org/software/autoconf> |
| Packaged as | `package:msys2:autoconf2.71` |
| Version (observed) | 2.71-4 |
| License (observed) | spdx:GPL-2.0-or-later;spdx:GPL-3.0-or-later;spdx:Autoconf-exception-3.0 |
| Architecture (observed) | any |
| Installed size (observed) | 1955.78 KiB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-08-05)
- `evidence:gnu:autoconf-manual-2026-07-30` — GNU Autoconf (official project page) (`primary`, retrieved 2026-07-30)

**Claims about this object**

- `claim:component:autoconf:m4-macro-processor` (`fact`, `verified`) — Autoconf is fundamentally an m4 macro-processing framework: autoconf/autoheader/autoreconf expand m4 macros to generate a portable configure script, which explains its dependency on m4.

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

Autoconf generates a portable `configure` shell script from a higher-level
`configure.ac` description, testing for platform features and quirks so
projects don't have to hardcode them. This page documents its architectural
role as an m4-macro framework; see the
[official GNU Autoconf project page](https://www.gnu.org/software/autoconf)
for the full macro reference.

## Architectural Classification

`component:gnu:autoconf` is a GNU-userland component packaged as
`package:msys2:autoconf2.71` (version `2.71-4` in the current catalog
snapshot, license
`GPL-2.0-or-later;GPL-3.0-or-later;Autoconf-exception-3.0` — the additional
Autoconf-specific license exception permits generated `configure` scripts
to be distributed without themselves being bound by the GPL, a detail
worth noting since it directly affects every project that ships an
Autoconf-generated `configure`). It belongs to the MSYS environment.

## Responsibilities

- Expanding m4 macros in `configure.ac` to generate a portable `configure`
  shell script (`claim:component:autoconf:m4-macro-processor`), which tests
  for compiler, library, and platform features at build-configuration time.

## Boundaries

Autoconf generates the `configure` script; it does not generate Makefiles
from that configuration (that is commonly [Automake](GNU-AUTOMAKE.md)'s
role, working alongside Autoconf though not linked to it by a direct
package dependency in this catalog snapshot — see Dependencies) and does
not itself build anything (that is [GNU Make](GNU-MAKE.md)'s role once
`configure` has run).

## Interfaces

- `autoconf` (generate `configure` from `configure.ac`), `autoheader`
  (generate a template config header), `autoreconf` (re-run the full
  Autotools chain as needed), per the manual.

## Dependencies

The catalog snapshot records five `runtime-depends-on` edges for
`package:msys2:autoconf2.71`, each mapping to a specific part of Autoconf's
own implementation:

| Dependency | Package | Architectural reason |
| --- | --- | --- |
| Macro processing | `package:msys2:m4` | Backs Autoconf's core mechanism: `configure.ac` is expanded by the m4 macro processor to produce `configure` (`claim:component:autoconf:m4-macro-processor`). |
| Driver scripts | `package:msys2:perl` | Autoconf's own driver commands (`autoconf`, `autoheader`, `autoreconf`, `autoscan`, `autoupdate`) have been implemented in Perl since Autoconf 2.62. |
| Generated-script interpreter | `package:msys2:bash` | The `configure` scripts Autoconf generates are POSIX-style shell scripts, executed via a shell at a project's configuration time. |
| Text substitution | `package:msys2:sed` | Backs the `@VAR@` substitution mechanism (`AC_SUBST`/`config.status`) that turns `Makefile.in`-style templates into their final generated form. |
| Change detection | `package:msys2:diffutils` | Backs internal comparison operations, such as detecting whether `config.status` needs regeneration. |
| Text processing helper | (declared as `awk`, unresolved) | Autoconf's own tooling and generated scripts commonly rely on `awk` for text processing; this dependency is declared by name but not resolved to a specific MSYS2 package edge in this snapshot (see below). |

The `awk` dependency listed in the package's declared requirements is not a
package name matching any entity in this catalog snapshot by exact string
match, so — like the `sh` dependency pattern documented for
[GNU Grep](GNU-GREP.md#dependencies) — it is retained in
`generated/unresolved-dependencies.json` rather than resolved to a
`runtime-depends-on` edge; [GNU Awk (gawk)](GNU-AWK.md) is the MSYS2
package that provides `awk` in this environment.

## Reverse Dependencies

The snapshot records 1 relationship targeting `package:msys2:autoconf2.71`.
See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

`configure.ac` (or the older `configure.in`) is the project's Autoconf
input; `aclocal.m4` and the `m4/` macro directory (commonly populated by
[Automake](GNU-AUTOMAKE.md)'s `aclocal`) supply additional macros beyond
Autoconf's built-in set.

## Initialization and Execution Flow

`autoconf`/`autoreconf` are invoke-run-exit processes that themselves spawn
`m4` as a subprocess to perform macro expansion. As an MSYS-dependent
process, this is adapted from POSIX semantics onto Windows process
primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md). The
generated `configure` script is a separate artifact, run later (and
possibly on a different machine) as its own shell-script process.

## Runtime Behavior

Autoconf itself runs only at a project maintainer's macro-expansion step;
the generated `configure` script is what end users and build systems
actually execute, and its runtime behavior (feature tests, generated
output files) is determined by the macros that were expanded into it, not
by Autoconf being present on the end user's machine at all.

## Compatibility and Variants

Autoconf 2.71 is the version recorded in this snapshot; `configure.ac`
files requiring macros only available in older or newer Autoconf releases
may not process identically, a version-sensitivity the manual documents
directly.

## Security Considerations

A `configure.ac`/generated `configure` script from an untrusted source can
run arbitrary shell commands during feature detection, the same general
risk class already noted for [GNU Make](GNU-MAKE.md#security-considerations)'s
Makefile execution. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review has
been performed for the recorded `2.71-4` version.

## Failure Modes and Diagnostics

A `configure` script failing a feature test that "should" pass is
frequently a macro-ordering or caching issue (`autom4te.cache`); clearing
the cache and re-running `autoreconf` is the manual's documented first
diagnostic step before assuming a genuine platform incompatibility.

## Evidence, Assumptions, and Open Questions

The m4-macro-expansion model and driver-script implementation are backed
by the official GNU Autoconf project page
(`evidence:gnu:autoconf-manual-2026-07-30`), matching the `project_url`
already recorded for `package:msys2:autoconf2.71` in the catalog. Package
identity, version, license, and dependency edges are backed by the pacman
catalog snapshot (`evidence:catalog:current`) via
`claim:component:autoconf:m4-macro-processor`. The unresolved `awk`
dependency is explained by `generated/unresolved-dependencies.json`, not
merely asserted.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["GNU Autoconf"]
    d0["msys-2.0.dll"]
    subject -->|uses-runtime| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `component:gnu:autoconf` in the composed graph: 0 dependents and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Toolchain Role Model](TOOLCHAIN-ROLE-MODEL.md)
- [MSYS2 Build System Role Model](BUILD-SYSTEM-ROLE-MODEL.md)
- [GNU Automake](GNU-AUTOMAKE.md)
- [GNU Libtool](GNU-LIBTOOL.md)
- [GNU Make](GNU-MAKE.md)
- [GNU Awk (gawk)](GNU-AWK.md)
