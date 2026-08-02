---
id: doc:volume-3:posix-api
title: MSYS POSIX API Surface
volume: 3
status: partial
model_refs:
  - subsystem:msys2:posix-api
  - runtime:msys2:msys-2.0.dll
  - environment:msys2:msys
  - layer:msys2:3-msys-posix-runtime
evidence_refs:
  - evidence:cygwin:user-guide-2026-08-02
  - evidence:msys2:runtime-behavior-probes-2026-07-30
last_verified: 2026-08-02
---

# MSYS POSIX API Surface

## Purpose

The POSIX API surface is what `msys-2.0.dll` exports to programs that link
it, and the boundary at which a POSIX call becomes one or more Win32 calls.
It is the interface every other runtime subsystem is reached through.

## Architectural Classification

`subsystem:msys2:posix-api`, contained by
[`msys-2.0.dll`](MSYS-2-0-DLL.md). It is a surface rather than a mechanism:
the behavior behind each call belongs to the subsystem that implements it.

## Responsibilities

- Exporting the POSIX C API — process, signal, file, terminal, and
  environment families — to MSYS-linked programs.
- Translating each call into the Win32 operations that approximate it.
- Presenting POSIX error semantics, including `errno` values, for conditions
  Windows reports differently.

## Boundaries

This is where the emulation boundary actually sits. Above it a program sees
POSIX; below it, Win32. Where the two disagree the runtime approximates, and
the approximation — not the POSIX specification — is what a program
observes.

Which POSIX interfaces are present, absent, or partial in MSYS 3.6.10 is
**not** established by this knowledge base. No header-level or symbol-level
inventory of the runtime has been performed, which makes this page a
structural description rather than a conformance statement.

## Interfaces

The exported symbol set of `msys-2.0.dll`. Not enumerated here — see
Evidence.

## Dependencies

The Win32 API, and every other runtime subsystem, each of which implements
part of the surface.

## Reverse Dependencies

Every MSYS-linked binary. 173 pages in this knowledge base record a
`uses-runtime` relationship to `msys-2.0.dll`, and this surface is what that
relationship means in practice.

## Configuration

None. The exported surface is a property of the runtime build.

## Initialization and Execution Flow

Available from image load, after the runtime completes initialization and
before `main`; see
[MSYS runtime initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

Four of the five 2026-07-30 probes exercised this surface indirectly — via
shell builtins for process, exec, signal, and filesystem operations. None
called the API directly, so the observations characterize shell behavior
over the surface rather than the surface itself.

## Compatibility and Variants

MSYS-only. Native environments link the UCRT or MSVCRT and expose no POSIX
surface; this is the concrete reason MSYS objects cannot be linked into
native output.

## Security Considerations

No subsystem-specific vulnerability review has been performed. See
[Threat model and supply chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general posture; the runtime version observed was `3.6.10`.

## Failure Modes and Diagnostics

A program failing to build against MSYS headers for a missing POSIX
interface is the characteristic case. Whether that interface is genuinely
absent or present-but-partial cannot be answered from this knowledge base
today, which is itself the finding.

## Evidence, Assumptions, and Open Questions

Design is attributed to the
[Cygwin User's Guide](https://cygwin.com/cygwin-ug-net/cygwin-ug-net.html)
(`evidence:cygwin:user-guide-2026-08-02`), documenting the runtime MSYS2's
is derived from. Probe context is from the bounded collector
(`evidence:msys2:runtime-behavior-probes-2026-07-30`).

Open, and the largest gap on this page: no exported-symbol inventory, no
header inventory, and no conformance matrix. The deep-inventory pipeline
that could produce the first two exists and has been run against 2 of 15,711
packages — the MSYS runtime package is not among them.

## Related Objects

- [msys-2.0.dll](MSYS-2-0-DLL.md)
- [Process Manager](MSYS-PROCESS-MANAGER.md)
- [Filesystem Layer](MSYS-FILESYSTEM-LAYER.md)
- [Binary-to-DLL dependency graph](BINARY-DLL-DEPENDENCY-GRAPH.md)
