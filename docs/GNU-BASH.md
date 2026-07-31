---
id: doc:volume-5:gnu-bash
title: GNU Bash
volume: 5
status: partial
model_refs:
  - component:gnu:bash
  - package:msys2:bash
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:gnu:bash-manual-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# GNU Bash

## Purpose

Bash is the shell that fronts every MSYS2 session. This page documents its
architectural role, startup behavior, configuration surface, and dependency
footprint as packaged for MSYS. It is a component reference, not a Bash
scripting tutorial; see the
[official GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
for language and builtin semantics.

## Architectural Classification

`component:gnu:bash` is a GNU-userland component packaged as
`package:msys2:bash` (version `5.3.015-1` in the current catalog snapshot,
license `GPL-3.0-or-later`). It belongs to the MSYS environment only: MSYS2
does not ship a separate native-environment bash. Launching a UCRT64,
CLANG64, CLANGARM64, MINGW64, or MINGW32 session (for example through
`msys2_shell.cmd`) starts this same MSYS-dependent bash with the
environment-selection variables described in
[Runtime Environments](RUNTIME-ENVIRONMENTS.md) set for that session; the
shell process itself is not duplicated per native environment.

## Responsibilities

- Interactive command interpretation and line editing for MSYS2 sessions.
- Non-interactive script execution, including pacman hooks, `makepkg`-style
  build scripts, and CI entry points that assume a POSIX-oriented shell.
- Process and job control (foreground/background jobs, signal-driven job
  state transitions) for programs launched from the shell.
- Acting as the `sh` implementation in the MSYS environment: the package
  catalog records `bash` as the package that `provides: sh`
  (`claim:component:bash:provides-sh`).

## Boundaries

Bash hosts scripts; it is not a build system or package manager and performs
no dependency resolution itself. A program bash launches does not inherit
MSYS-runtime dependence merely because it was started from bash: native
UCRT64/CLANG64/MINGW builds run against Windows-facing runtime behavior
directly, per the
[MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md). Only
processes that themselves load `msys-2.0.dll` are MSYS-dependent.

## Interfaces

- Invocation modes: interactive login, interactive non-login, non-interactive
  (script), and POSIX mode (`--posix`, or invocation as `sh`), each selecting
  a distinct startup-file set per the GNU Bash manual's "Bash Startup Files"
  chapter.
- Standard streams, process exit status, and POSIX signal delivery as the
  external contract with child processes and the calling environment.
- `$0`/`argv[0]` dispatch: because the package provides `sh`, behavior can
  differ meaningfully depending on which name invoked the binary.

## Dependencies

The current catalog snapshot (`evidence:catalog:current`) records no
`runtime-depends-on` edges for `package:msys2:bash` beyond its membership in
the `msys` repository and the MSYS environment
(`belongs-to-environment -> environment:msys2:msys`). This reflects the
snapshot's declared package metadata, not a verified absence of shared-library
dependencies; PE import analysis (`docs/DEEP-INVENTORY-CONTRACT.md`) is the
correct evidence source to confirm the linked C runtime and any GNU
readline/termcap-family libraries, and remains open work for this object.

## Reverse Dependencies

The same snapshot records 46 relationships targeting `package:msys2:bash`,
reflecting its centrality as a base system package. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
and generated `reverse-dependency-impact.md` for the full, current list; this
page does not restate it to avoid duplicating canonical Volume 13 data.

## Configuration

Startup-file selection follows upstream Bash semantics: a login shell reads
`/etc/profile` then the first of `~/.bash_profile`, `~/.bash_login`, or
`~/.profile`; a non-login interactive shell reads `~/.bashrc` (MSYS2, like
several GNU/Linux distributions, patches Bash to also source
`/etc/bash.bashrc` and files under `/etc/profile.d/` for non-login
interactive shells — this is a distribution-level patch, not vanilla
upstream Bash behavior, so it is recorded here at `medium` confidence pending
a controlled observation against the installed package). Environment
selection itself (`MSYSTEM` and the resulting `PATH`/prefix) is modeled in
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md) and is not
restated here.

## Initialization and Execution Flow

Process creation for bash and its children is adapted from POSIX
`fork()`/`exec()` semantics onto Windows process primitives by
`msys-2.0.dll`; the exact adaptation mechanics belong to
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md) and the
[MSYS runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md) and are referenced,
not duplicated, here.

## Runtime Behavior

The controlled local observation recorded in the
[MSYS runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md#controlled-local-observation)
on 2026-07-30 was performed through an MSYS bash shell and is directly
relevant to this object: a background child process existed and exited with
status 0, a shell `exec` replaced the shell process and reported success, and
a `USR1` trap correctly received the delivered signal. These are exact,
narrowly scoped command outcomes, not a general claim of POSIX process or
signal parity; see that page for the full boundary statement.

## Compatibility and Variants

Bash's POSIX mode (`--posix` or invocation as `sh`) changes startup-file
selection and several builtin behaviors relative to native Bash mode, per the
GNU Bash manual. Because the MSYS package provides `sh`, scripts invoked
with a `#!/bin/sh` shebang in this environment run under Bash's POSIX-mode
emulation rather than a distinct minimal shell implementation; this is a
compatibility-relevant distinction from environments where `/bin/sh` is a
different implementation (e.g., dash).

## Security Considerations

Bash is a script-execution engine for hooks and build recipes documented
elsewhere in this knowledge base as a supply-chain concern; see
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md), which
notes that package recipes are parsed statically and never executed by this
project's own tooling specifically to avoid arbitrary shell execution during
ingestion. This page does not separately assert bash-specific CVE history,
which would require a dedicated, version-qualified vulnerability review.

## Failure Modes and Diagnostics

Startup-file misconfiguration (an unexpected `~/.bash_profile`/`~/.bashrc`
interaction, or an inherited `BASH_ENV` in non-interactive scripts) is the
most common source of environment-selection confusion reported against MSYS2
sessions. Capturing effective startup files and environment variables as a
controlled observation, per the existing guidance in
[GNU Userland Role Model](GNU-USERLAND-ROLE-MODEL.md), is the recommended
diagnostic step before escalating to a runtime-level investigation.

## Evidence, Assumptions, and Open Questions

Shell grammar, startup-file, and invocation-mode claims are backed by the
official GNU Bash Reference Manual (`evidence:gnu:bash-manual-2026-07-30`).
Package identity, version, license, and the `provides: sh` fact are backed by
the pacman catalog snapshot (`evidence:catalog:current`). The MSYS-runtime
dependency relationship is backed by the official MSYS2 environments
documentation (`evidence:msys2:environments-2026-07-28`), which establishes
that MSYS-environment tools use the Cygwin-derived compatibility runtime.
Open: the distribution-patched `/etc/bash.bashrc` startup-file claim above
is recorded at `medium` confidence and needs a controlled observation against
an installed package to raise to `verified`; PE import analysis to confirm
bash's linked runtime libraries is likewise open.

## Related Objects

- [GNU Userland Role Model](GNU-USERLAND-ROLE-MODEL.md)
- [GNU Coreutils](GNU-COREUTILS.md)
- [GNU Grep](GNU-GREP.md)
- [GNU Sed](GNU-SED.md)
- [GNU Awk (gawk)](GNU-AWK.md)
- [GNU Findutils](GNU-FINDUTILS.md)
- [MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md)
- [MSYS Runtime Behavior Map](MSYS-RUNTIME-BEHAVIOR-MAP.md)
- [MSYS2 and MinGW-w64 Role Model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md)
