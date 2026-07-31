---
id: doc:volume-6:gnu-termcap
title: GNU termcap
volume: 6
status: partial
model_refs:
  - library:gnu:termcap
  - package:msys2:mingw-w64-ucrt-x86_64-termcap
  - library:gnu:readline
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:gnu:termcap-manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# GNU termcap

## Purpose

GNU termcap is a terminal feature (capability) database library, providing
programs with the cursor-movement and editing escape sequences appropriate
for the terminal actually in use. This page documents its architectural
role as the sole directly-declared dependency of
[GNU Readline](GNU-READLINE.md); see the
[official GNU termutils project page](https://www.gnu.org/software/termutils/)
for the full reference.

## Architectural Classification

`library:gnu:termcap` is packaged per native environment: this page
cites the UCRT64 build,
`package:msys2:mingw-w64-ucrt-x86_64-termcap` (version `1.3.1-7` in the
current catalog snapshot). It belongs to the UCRT64 environment and, like
[GNU Readline](GNU-READLINE.md#architectural-classification) itself,
does not depend on `msys-2.0.dll`, per the
[MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md).
termcap is a narrower, older sibling of the terminfo-based
[ncurses](NCURSES.md) library documented in Volume 5: both solve the
"which escape sequences does this terminal support" problem, but termcap
uses a simpler, flat capability database while ncurses/terminfo use a
richer, compiled database format — the two are not interchangeable
implementations of the same file format.

## Responsibilities

- Providing terminal capability lookups (cursor movement, screen clearing,
  and other control sequences), consumed by
  [GNU Readline](GNU-READLINE.md) to determine the correct escape
  sequences for the active terminal during interactive line editing.

## Boundaries

termcap provides terminal capability lookup specifically, a narrower
scope than [ncurses](NCURSES.md)'s fuller terminal-handling library
(window/pad management, input handling, and more) — already noted on
[GNU Readline's own page](GNU-READLINE.md#dependencies) as reflecting
Readline's narrower line-editing-only scope compared to full-screen
terminal programs that depend on ncurses instead.

## Interfaces

- A C API (`tgetent`, `tgetstr`, `tgetnum`, `tputs`) for looking up and
  emitting terminal capability strings, per the documentation.

## Dependencies

The UCRT64 `package:msys2:mingw-w64-ucrt-x86_64-termcap` declares a
dependency on `mingw-w64-ucrt-x86_64-gcc-libs` only — the GCC runtime
support libraries, not a library-family dependency distinct enough to
warrant its own page in this volume.

## Reverse Dependencies

The catalog snapshot records 1 relationship targeting
`package:msys2:mingw-w64-ucrt-x86_64-termcap`:
`package:msys2:mingw-w64-ucrt-x86_64-readline`
(`relationship:foundation-libraries:readline-requires-termcap` in this
knowledge base's graph) — its sole recorded dependent in this snapshot.

## Configuration

termcap reads a terminal-capability database (conventionally identified
by the `TERM` environment variable) to determine which capability set
applies to the active terminal; this database is not user-authored
configuration in the usual sense.

## Initialization and Execution Flow

As a library, termcap has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — [GNU Readline](GNU-READLINE.md) in this dependency chain,
at line-editing-session start when the terminal's capabilities are first
queried. As a native MinGW-w64 library, this process model is
Windows-facing directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Which escape sequences termcap actually returns for a given operation
(cursor movement, screen clear) depends on the `TERM` environment
variable's value at the time of the lookup, not a single fixed sequence
set across every terminal.

## Compatibility and Variants

Whether other native environments (CLANG64, i686) in this catalog package
termcap separately was not confirmed while writing this page; this is
recorded as an open item rather than assumed either way.

## Security Considerations

termcap is not itself a security-sensitive component; its role in
[GNU Readline](GNU-READLINE.md) is limited to terminal capability lookup,
not authentication, cryptography, or network exposure. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `1.3.1-7` version.

## Failure Modes and Diagnostics

Garbled or incorrect cursor-movement behavior in a Readline-based program
should first be checked against the `TERM` environment variable's value
and the corresponding terminal-capability entry before being treated as a
Readline defect.

## Evidence, Assumptions, and Open Questions

Terminal capability database scope is backed by the official GNU
termutils project page (`evidence:gnu:termcap-manual-2026-07-30`),
matching the `project_url` already recorded for
`package:msys2:mingw-w64-ucrt-x86_64-termcap` in the catalog. Package
identity, version, and the recorded dependency/dependent edges are backed
by the pacman catalog snapshot (`evidence:catalog:current`). Open:
whether other native environments package termcap separately was not
confirmed. Also explicitly out of scope for this page: header-level API
surface and PE import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [GNU Readline](GNU-READLINE.md)
- [ncurses](NCURSES.md)
