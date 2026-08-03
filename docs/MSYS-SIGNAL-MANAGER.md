---
id: doc:volume-3:signal-manager
title: MSYS Signal Manager
volume: 3
status: partial
model_refs:
  - subsystem:msys2:signal-manager
  - runtime:msys2:msys-2.0.dll
  - environment:msys2:msys
evidence_refs:
  - evidence:cygwin:user-guide-2026-08-02
  - evidence:msys2:runtime-behavior-probes-2026-07-30
last_verified: 2026-08-02
---

# MSYS Signal Manager

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `subsystem:msys2:signal-manager` |
| Kind | `subsystem` |
| Status | `partial` |
| Confidence | `medium` |
| Authority | MSYS2 |
| Environments | `msys` |

**Evidence on this object**

- `evidence:cygwin:user-guide-2026-08-02` — Cygwin User's Guide (`primary`, retrieved 2026-08-02)

Generated from the composed model by `tools/build_object_facts.py`. Observed values come from the catalog snapshot and change when it is refreshed.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED object-facts -->


## Purpose

The signal manager maps POSIX signal generation, delivery, and disposition
onto Windows primitives that have no signal concept. Windows offers thread
APIs, events, and console control handlers; POSIX programs expect
asynchronous delivery with per-signal dispositions and masking.

## Architectural Classification

`subsystem:msys2:signal-manager`, contained by
[`msys-2.0.dll`](MSYS-2-0-DLL.md). Derived from Cygwin's signal
implementation.

## Responsibilities

- Generating signals from both program requests (`kill`, `raise`) and host
  events such as console control notifications.
- Delivering signals asynchronously to the target process or thread and
  running the installed disposition — default action, ignore, or handler.
- Maintaining per-process signal masks and pending sets across `fork` and
  `exec`.

## Boundaries

Signal semantics apply to MSYS-linked processes. A signal sent to a native
Windows process from an MSYS process does not carry POSIX meaning, and
Ctrl+C handling at a console shared between MSYS and native programs is a
boundary this knowledge base has not characterized.

## Interfaces

`kill`, `raise`, `signal`, `sigaction`, `sigprocmask`, and the related POSIX
families, via [the POSIX API surface](MSYS-POSIX-API.md).

## Dependencies

Windows thread primitives, console control handling, and inter-process
notification. Named in
[Windows platform boundaries](WINDOWS-PLATFORM-BOUNDARIES.md).

## Reverse Dependencies

Every MSYS process. Interactive shells and long-running tools depend on it
most visibly, through Ctrl+C and job control.

## Configuration

No documented configuration surface; dispositions are set by the program at
runtime.

## Initialization and Execution Flow

Signal machinery is established during runtime initialization, before
`main`; see [MSYS runtime initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

One bounded probe touches this subsystem. On 2026-07-30 a shell `USR1` trap
emitted `signal=USR1` and exited with status 0.

That establishes exactly one thing: a shell-level trap for one signal fired
once. It does not establish the complete signal mapping, delivery under
load, behavior across `fork`, mask correctness, or any real-time signal
support. The behavior map states this boundary explicitly and this page
does not widen it.

## Compatibility and Variants

MSYS-only. Native environments use Windows structured exception handling and
console control handlers directly, with no POSIX signal layer.

## Security Considerations

No subsystem-specific vulnerability review has been performed. See
[Threat model and supply chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general posture; the runtime version observed was `3.6.10`.

## Failure Modes and Diagnostics

A handler that does not fire, or fires late, is the characteristic symptom
and is difficult to distinguish from a program defect without a controlled
test. This knowledge base has no signal test matrix, which the behavior map
identifies as required deep evidence for this row.

## Evidence, Assumptions, and Open Questions

Signal-model design is attributed to the
[Cygwin User's Guide](https://cygwin.com/cygwin-ug-net/cygwin-ug-net.html)
(`evidence:cygwin:user-guide-2026-08-02`). The single probe outcome is from
the bounded collector
(`evidence:msys2:runtime-behavior-probes-2026-07-30`).

Open: the behavioral test matrix the behavior map requires for this row does
not exist. Mixed MSYS/native console signal behavior is uncharacterized.

## Related Objects

- [msys-2.0.dll](MSYS-2-0-DLL.md)
- [Process Manager](MSYS-PROCESS-MANAGER.md)
- [PTY and Console](MSYS-PTY-AND-CONSOLE.md)
