---
id: doc:volume-6:wineditline
title: WinEditLine
volume: 6
status: partial
model_refs:
  - library:mingweditline:wineditline
  - package:msys2:mingw-w64-ucrt-x86_64-wineditline
  - library:pcre:pcre2
  - environment:msys2:ucrt64
evidence_refs:
  - evidence:mingweditline:manual-2026-07-30
  - evidence:catalog:current
last_verified: 2026-07-30
---

# WinEditLine

## Purpose

WinEditLine is an implementation of the BSD EditLine API for the native
Windows Console, providing readline/libedit-style interactive line editing
to programs built for native Windows rather than a POSIX-emulated
terminal. This page documents its architectural role as a directly-declared
dependency of [PCRE2](PCRE2.md); see the
[official WinEditLine project page](https://mingweditline.sourceforge.io/)
for the full reference.

## Architectural Classification

`library:mingweditline:wineditline` is packaged per native environment:
this page cites the UCRT64 build,
`package:msys2:mingw-w64-ucrt-x86_64-wineditline` (version `2.208-1` in
the current catalog snapshot). It belongs to the UCRT64 environment and,
like [PCRE2](PCRE2.md#architectural-classification) itself, does not
depend on `msys-2.0.dll`, per the
[MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md).
WinEditLine implements the same EditLine API that
[libedit](LIBEDIT.md) (documented elsewhere in this volume as an
[OpenSSH](OPENSSH.md) dependency) also implements, but the two are
separately packaged, separately versioned catalog entities targeting
different environments — WinEditLine specifically for the native Windows
Console, libedit for the MSYS/POSIX-emulated terminal — not the same
library under two names.

## Responsibilities

- Providing interactive line editing (history, cursor movement, key
  bindings) for native Windows Console programs, consumed by
  [PCRE2](PCRE2.md)'s bundled `pcre2test` tool.

## Boundaries

WinEditLine provides the EditLine API specifically for the native Windows
Console; it is architecturally comparable to
[libedit](LIBEDIT.md) and [GNU Readline](GNU-READLINE.md) in role
(interactive line editing) but targets a different console model than
either — libedit and Readline both operate within the MSYS/POSIX-emulated
terminal environment, while WinEditLine targets the native Windows Console
API directly, already noted on
[PCRE2's own page](PCRE2.md#dependencies)
(`claim:library:pcre2-wineditline-interactive-tool`).

## Interfaces

- The BSD EditLine C API (`el_init`, `el_gets`, `el_set`), the same API
  surface [libedit](LIBEDIT.md) also implements, per the documentation.

## Dependencies

The catalog snapshot records no `runtime-depends-on` edges for
`package:msys2:mingw-w64-ucrt-x86_64-wineditline` — one of only a small
number of libraries documented in this volume with no recorded runtime
dependencies of its own, alongside [libuv](LIBUV.md) and
[libxcrypt](LIBXCRYPT.md).

## Reverse Dependencies

The catalog snapshot records 3 relationships targeting
`package:msys2:mingw-w64-ucrt-x86_64-wineditline`:
`package:msys2:mingw-w64-ucrt-x86_64-pcre2`
(`relationship:foundation-libraries:pcre2-requires-wineditline` in this
knowledge base's graph), `package:msys2:mingw-w64-ucrt-x86_64-pcre` (an
older PCRE1 package not otherwise documented in this knowledge base), and
`package:msys2:mingw-w64-ucrt-x86_64-sqlitestudio`.

## Configuration

WinEditLine has no persistent configuration file of its own; its behavior
is controlled entirely through its C API by the calling program.

## Initialization and Execution Flow

As a library, WinEditLine has no independent process lifecycle: it
initializes and executes within the process of whatever program links
against it — `pcre2test` (bundled with [PCRE2](PCRE2.md)) in this
dependency chain. As a native MinGW-w64 library, this process model is
Windows-facing directly rather than mediated by `msys-2.0.dll`.

## Runtime Behavior

Interactive line-editing behavior (history, key bindings) is exercised
only when `pcre2test` is run interactively at a native Windows Console;
it plays no role when PCRE2's library functions are called directly by
another program.

## Compatibility and Variants

Whether other native environments (CLANG64, i686) in this catalog package
WinEditLine separately was not confirmed while writing this page; this is
recorded as an open item rather than assumed either way. Code written
against the EditLine API for [libedit](LIBEDIT.md) should be portable to
WinEditLine at the API level, per both implementing the same interface,
though this page does not assert full behavioral compatibility between
the two.

## Security Considerations

WinEditLine is not itself a security-sensitive component; its role is
limited to `pcre2test`'s interactive prompt, a developer/testing tool
rather than a network-facing or authentication-relevant surface. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture; no version-qualified CVE review
has been performed for the recorded `2.208-1` version.

## Failure Modes and Diagnostics

Unexpected `pcre2test` prompt behavior (missing history, unresponsive key
bindings) should be checked against WinEditLine's own key-binding
defaults before being treated as a PCRE2 defect.

## Evidence, Assumptions, and Open Questions

EditLine API implementation scope is backed by the official WinEditLine
project page (`evidence:mingweditline:manual-2026-07-30`), matching the
`project_url` already recorded for
`package:msys2:mingw-w64-ucrt-x86_64-wineditline` in the catalog. Package
identity, version, and the recorded dependency/dependent edges are backed
by the pacman catalog snapshot (`evidence:catalog:current`). Open:
whether other native environments package WinEditLine separately was not
confirmed, and full behavioral compatibility with
[libedit](LIBEDIT.md) beyond shared API surface was not asserted. Also
explicitly out of scope for this page: header-level API surface and PE
import/export-level evidence, per the
[Library Family Classification](LIBRARY-FAMILY-CLASSIFICATION.md)
methodology.

## Related Objects

- [MSYS2 Library Architecture](LIBRARIES-ARCHITECTURE.md)
- [PCRE2](PCRE2.md)
- [libedit](LIBEDIT.md)
- [GNU Readline](GNU-READLINE.md)
- [WinEditLine (CLANG64)](WINEDITLINE-CLANG64.md)
