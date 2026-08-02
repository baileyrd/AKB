---
id: doc:volume-6:gnu-readline
title: GNU Readline
volume: 6
status: partial
model_refs:
  - library:gnu:readline
  - package:msys2:mingw-w64-ucrt-x86_64-readline
  - component:gnu:gdb
  - library:gnu:termcap
  - library:gnu:readline@msys
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:gnu:readline-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# GNU Readline

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `library:gnu:readline` |
| Kind | `library` |
| Status | `partial` |
| Confidence | `high` |
| Authority | Free Software Foundation |
| Environments | `ucrt64` |
| Upstream | <https://tiswww.case.edu/php/chet/readline/rltop.html> |
| Packaged as | `package:msys2:mingw-w64-ucrt-x86_64-readline` |
| Version (observed) | 8.3.003-1 |
| License (observed) | spdx:GPL-3.0-or-later |
| Architecture (observed) | any |
| Installed size (observed) | 2.6 MB |

**Evidence on this object**

- `evidence:catalog:current` — MSYS2 pacman package catalog (`observed`, retrieved 2026-07-29)
- `evidence:gnu:readline-manual-2026-07-30` — GNU Readline (official project page) (`primary`, retrieved 2026-07-30)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

Readline provides interactive line editing, history, and tab-completion for
command-line programs, and it is the dependency behind the interactive
prompt already documented for [GDB](GNU-GDB.md#dependencies). This page
documents the **UCRT64**-packaged build specifically;
[GnuPG's](GNUPG.md) own MSYS-packaged interactive prompts depend on a
separately versioned MSYS sibling package instead, documented on
[GNU Readline (MSYS)](GNU-READLINE-MSYS.md). See the
[official GNU Readline project page](https://tiswww.case.edu/php/chet/readline/rltop.html)
for the key-binding and API reference.

## Architectural Classification

`library:gnu:readline` is a GNU-userland library, packaged per native
environment: this page cites the UCRT64 build,
`package:msys2:mingw-w64-ucrt-x86_64-readline` (version `8.3.003-1` in the
current catalog snapshot, license `GPL-3.0-or-later`), a MinGW port of the
canonical GNU Readline. This page is scoped to Volume 6's
package/dependency-level evidence; the fuller
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology has not been applied here and remains open.

## Responsibilities

- Providing line editing (cursor movement, kill/yank), persistent command
  history, and tab-completion for any program that links against it,
  rather than each program implementing its own terminal input handling.

## Boundaries

Readline provides input editing; it does not provide the broader
screen/terminal-capability handling [ncurses](NCURSES.md) does — a program
can use one, the other, or both for different purposes (Readline for its
command prompt, ncurses for a full-screen display), and several tools in
this knowledge base depend on both simultaneously (for example,
[GDB](GNU-GDB.md#dependencies)).

## Interfaces

- The `readline()` C function (returns a line of edited input) plus
  history (`add_history`) and completion (`rl_completion_matches`) APIs,
  per the documentation. This page does not enumerate the header-level
  surface; that belongs to
  [Header and Development-Metadata Indexes](HEADER-AND-METADATA-INDEXES.md).

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:mingw-w64-ucrt-x86_64-readline`:
[GNU termcap](GNU-TERMCAP.md), the terminal-capability database Readline
uses to determine cursor-movement and editing escape sequences for the
active terminal — a narrower, more specific dependency than
[ncurses](NCURSES.md)'s fuller terminal-capability library, reflecting
Readline's narrower line-editing-only scope.

## Reverse Dependencies

The snapshot records 36 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-readline`, including
[GDB's](GNU-GDB.md#dependencies) interactive-prompt dependency.
[GnuPG](GNUPG.md) is **not** among them — its own interactive prompts
depend on [GNU Readline (MSYS)](GNU-READLINE-MSYS.md#reverse-dependencies)
instead, a separate catalog entity. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

`~/.inputrc` is a genuine standing configuration file, setting key
bindings and editing-mode options (for example, `vi` versus `emacs`
editing mode) that apply to every Readline-linked program a user runs, not
just one tool.

## Initialization and Execution Flow

As a library, Readline has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it, the same model documented for
[ncurses](NCURSES.md#initialization-and-execution-flow). It reads
`~/.inputrc` once during that initialization.

## Runtime Behavior

Because `~/.inputrc` is shared across every Readline-linked program
regardless of which specific Readline package it links against, a
key-binding change a user makes affects [GDB's](GNU-GDB.md) prompt
(backed by this UCRT64 package), [GnuPG's](GNUPG.md) prompt (backed by
the separate [GNU Readline (MSYS)](GNU-READLINE-MSYS.md) package
instead), and any other Readline-based tool simultaneously — a
documented, deliberate consistency property of the Readline library
convention itself, not evidence that both programs share this specific
package.

## Compatibility and Variants

Some programs link against a Readline-compatible but not identical
library (such as `libedit`, already documented as an
[OpenSSH](OPENSSH.md#dependencies) dependency for a similar purpose); this
page does not claim interchangeability between them beyond noting that
both exist in this knowledge base for a comparable role.

## Security Considerations

No Readline-specific vulnerability review has been performed for this
volume; see [Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md)
for the project's general supply-chain posture. No version-qualified CVE
review has been performed for the recorded `8.3.003-1` version.

## Failure Modes and Diagnostics

Unexpected key-binding behavior across multiple tools should first be
checked against `~/.inputrc`, per Runtime Behavior above, before being
treated as a defect in any one dependent tool.

## Evidence, Assumptions, and Open Questions

The line-editing and configuration model are backed by the official GNU
Readline project page (`evidence:gnu:readline-manual-2026-07-30`),
matching the `project_url` already recorded for
`package:msys2:mingw-w64-ucrt-x86_64-readline` in the catalog. Package
identity, version, license, and the termcap dependency are backed by the
pacman catalog snapshot (`evidence:catalog:current`). Open, and
explicitly out of scope for this page: header-level API surface and PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["GNU Readline"]
    u0["GDB"]
    u0 -->|requires| subject
    d0["GNU termcap"]
    subject -->|requires| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `library:gnu:readline` in the composed graph: 1 dependent and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [ncurses](NCURSES.md)
- [GDB](GNU-GDB.md)
- [GNU termcap](GNU-TERMCAP.md)
- [GNU Readline (MSYS)](GNU-READLINE-MSYS.md)
