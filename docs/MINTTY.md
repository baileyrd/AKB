---
id: doc:volume-5:mintty
title: mintty
volume: 5
status: partial
model_refs:
  - component:mintty:mintty
  - package:msys2:mintty
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:mintty:project-site-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# mintty

## Purpose

Mintty is the terminal emulator that provides the actual window a shell
session runs inside on Windows, presenting a native Windows look and feel
rather than emulating a specific Unix terminal type's appearance. This page
documents its architectural role as the terminal host for MSYS sessions;
see the [official mintty project site](https://mintty.github.io) for
configuration and feature details.

## Architectural Classification

`component:mintty:mintty` is packaged as `package:msys2:mintty` (version
`1~3.8.3-1` in the current catalog snapshot, license `GPL-3.0-or-later`).
It belongs to the MSYS environment. Mintty is distinct in kind from every
other tool documented in this volume's editors/pagers/terminals family: it
is the terminal itself, hosting [GNU Bash](GNU-BASH.md) and the programs
that run inside it — including [ncurses](NCURSES.md)-based editors and
pagers — rather than being a program that runs inside a terminal.

## Responsibilities

- Rendering a terminal window, translating keyboard and mouse input to the
  hosted shell process, and interpreting the escape sequences that
  ncurses-based programs emit.
- Providing native Windows integration (window controls, clipboard,
  fonts, and DPI handling) rather than emulating a specific hardware
  terminal's chrome.

## Boundaries

Mintty does not itself provide POSIX process semantics; it is the terminal
front-end for whatever shell (ordinarily [GNU Bash](GNU-BASH.md)) it
launches, which is the process that becomes MSYS-runtime-dependent.
Mintty's own dependence on `msys-2.0.dll` (see Dependencies) is a separate,
narrower question from whether the programs it hosts are MSYS-dependent.

## Interfaces

- Command-line invocation typically launches a shell inside the terminal
  window (e.g., via `msys2_shell.cmd`, which the
  [Runtime Environments](RUNTIME-ENVIRONMENTS.md) page documents as the
  entry point for every modeled environment).
- Configuration via `~/.minttyrc` and command-line options for font, theme,
  and terminal-emulation behavior, per the project documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:mintty` beyond its membership in the `msys` repository and
the MSYS environment. Its declared dependencies also list `sh`, a virtual
capability provided by `package:msys2:bash` rather than an actual package
name; it does not resolve to a `runtime-depends-on` edge and is instead
retained in `generated/unresolved-dependencies.json`, per the same
explanation given for [GNU Grep](GNU-GREP.md#dependencies).

## Reverse Dependencies

The snapshot records 2 relationships targeting `package:msys2:mintty`. See
the [reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

`~/.minttyrc` sets persistent font, color-theme, and behavior options; this
is a genuine standing configuration file, unlike most other tools in this
volume, which are configured per-invocation through command-line flags.

## Initialization and Execution Flow

Mintty is a longer-lived process for the duration of the terminal session,
distinct from the invoke-run-exit model of most other tools documented in
this volume: it starts, launches a hosted shell as a child process, and
persists until the window (or hosted shell) closes. As an MSYS-dependent
process, its own startup is adapted from POSIX semantics onto Windows
process primitives by `msys-2.0.dll`, per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

Mintty's terminfo entry (identifying it to ncurses-based programs via
`TERM`) determines whether those programs draw correctly; this is the same
open dependency flagged in [ncurses](NCURSES.md#runtime-behavior)'s own
Runtime Behavior section and is not re-derived here.

## Compatibility and Variants

Mintty presents itself under a specific `TERM` value (commonly
`xterm-256color` or a mintty-specific terminfo entry, depending on
configuration); programs assuming a different terminal's exact capability
set may render suboptimally without the correct terminfo entry installed.

## Security Considerations

As the terminal rendering escape sequences emitted by hosted programs,
mintty inherits the general class of terminal-escape-sequence risks (for
example, a program printing attacker-controlled bytes that manipulate
terminal state); no mintty-specific CVE review has been performed for the
recorded `1~3.8.3-1` version. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture.

## Failure Modes and Diagnostics

Rendering glitches in a hosted program are the most common mintty-adjacent
issue reported, and should first be checked against the terminfo/`TERM`
question noted above rather than assumed to be a defect in mintty itself or
in the hosted program.

## Evidence, Assumptions, and Open Questions

Mintty's role and configuration are backed by the official mintty project
site (`evidence:mintty:project-site-2026-07-30`), matching the
`project_url` already recorded for `package:msys2:mintty` in the catalog.
Package identity, version, and license are backed by the pacman catalog
snapshot (`evidence:catalog:current`). The unresolved `sh` dependency is
explained by `generated/unresolved-dependencies.json`, not merely asserted.
Open: the accuracy of mintty's installed terminfo entry in this environment
has not been directly observed.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["mintty"]
    d0["msys-2.0.dll"]
    subject -->|uses-runtime| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `component:mintty:mintty` in the composed graph: 0 dependents and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [GNU Userland Role Model](GNU-USERLAND-ROLE-MODEL.md)
- [GNU Bash](GNU-BASH.md)
- [ncurses](NCURSES.md)
- [MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md)
