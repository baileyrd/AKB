---
id: doc:volume-5:gnu-ed
title: GNU Ed
volume: 5
status: partial
model_refs:
  - component:gnu:ed
  - package:msys2:ed
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:gnu:ed-manual-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# GNU Ed

## Purpose

Ed is the original Unix line-oriented text editor and the POSIX-mandated
baseline editor that every conforming system is expected to provide. This
page documents its architectural role as the minimal, scriptable end of
this volume's editor spectrum; see the
[official GNU Ed project page](https://www.gnu.org/software/ed/ed.html) for
the command reference.

## Architectural Classification

`component:gnu:ed` is a GNU-userland component packaged as
`package:msys2:ed` (version `1.22.4-1` in the current catalog snapshot,
license `GPL`), belonging to the MSYS environment. It sits at the opposite
end of this volume's editor spectrum from [GNU Emacs](GNU-EMACS.md): a
minimal, line-at-a-time, script-friendly editor with no screen-drawing
dependency at all, notably the only editor in this batch with no
[ncurses](NCURSES.md) dependency.

## Responsibilities

- Line-oriented, non-interactive-friendly text editing: addressing,
  displaying, and modifying a buffer by line number or regex match, driven
  by short commands rather than a full-screen display.
- Serving as the historical ancestor of `ex`/`vi`'s command-mode syntax,
  which [Vim](VIM.md) still descends from.

## Boundaries

Ed does not draw a screen or maintain a persistent visual buffer view; it
prints only what a command explicitly requests. This is a deliberate,
minimal design, not a missing feature relative to the screen editors in
this batch.

## Interfaces

- Line-addressing syntax (line numbers, `.` current line, `$` last line,
  regex addresses) paired with single-letter commands (`p` print, `d`
  delete, `s` substitute, `w` write), per the manual.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:ed` beyond its membership in the `msys` repository and the
MSYS environment. Its declared dependencies also list `sh`, a virtual
capability provided by `package:msys2:bash` rather than an actual package
name; it does not resolve to a `runtime-depends-on` edge and is instead
retained in `generated/unresolved-dependencies.json`, per the same
explanation given for [GNU Grep](GNU-GREP.md#dependencies).

## Reverse Dependencies

The snapshot records 1 relationship targeting `package:msys2:ed`, the
lowest reverse-dependency count of any editor in this batch. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Ed has no persistent configuration file; behavior is controlled entirely
through command-line flags and in-session commands.

## Initialization and Execution Flow

Ed is an invoke-run-exit process for a single editing session (interactive
or scripted via stdin), adapted from POSIX semantics onto Windows process
primitives by `msys-2.0.dll` per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md). Because it
requires no terminal screen-control library, it is the only editor
documented in this volume usable identically over a plain, non-interactive
stdin/stdout pipe.

## Runtime Behavior

Ed prints nothing by default after most commands succeed, a deliberately
terse design suited to scripted use; this differs from the always-visible
buffer view of the screen editors in this batch.

## Compatibility and Variants

Ed's command language is the historical basis for `ex` mode commands still
present in [Vim](VIM.md) (`:s///`, line-range addressing); users familiar
with Vim's command-line mode will recognize much of ed's syntax directly.

## Security Considerations

Scripting ed from untrusted input carries the same general
command-injection-adjacent risk as any line-oriented editor accepting
attacker-influenced commands; see
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture. No ed-specific CVE review has been
performed for the recorded `1.22.4-1` version.

## Failure Modes and Diagnostics

Ed's terseness (printing `?` on error rather than a descriptive message by
default) is a common source of new-user confusion rather than an actual
defect; the manual documents verbose-mode (`-v`) as the way to get
descriptive error messages.

## Evidence, Assumptions, and Open Questions

Command language and design are backed by the official GNU Ed project page
(`evidence:gnu:ed-manual-2026-07-30`), matching the `project_url` already
recorded for `package:msys2:ed` in the catalog. Package identity, version,
and license are backed by the pacman catalog snapshot
(`evidence:catalog:current`). The unresolved `sh` dependency is explained
by `generated/unresolved-dependencies.json`, not merely asserted.

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["GNU Ed"]
    d0["msys-2.0.dll"]
    subject -->|uses-runtime| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `component:gnu:ed` in the composed graph: 0 dependents and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->

## Related Objects

- [GNU Userland Role Model](GNU-USERLAND-ROLE-MODEL.md)
- [Vim](VIM.md)
- [GNU Nano](GNU-NANO.md)
- [GNU Emacs](GNU-EMACS.md)
