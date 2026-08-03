---
id: doc:volume-3:path-conversion
title: MSYS Path Conversion
volume: 3
status: partial
model_refs:
  - subsystem:msys2:path-conversion
  - subsystem:msys2:mount-manager
  - runtime:msys2:msys-2.0.dll
  - environment:msys2:msys
evidence_refs:
  - evidence:cygwin:user-guide-2026-08-02
  - evidence:msys2:runtime-behavior-probes-2026-07-30
last_verified: 2026-08-02
---

# MSYS Path Conversion

<!-- BEGIN GENERATED object-facts -->

| Model fact | Value |
| --- | --- |
| Object | `subsystem:msys2:path-conversion` |
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

Path conversion translates between POSIX path forms (`/usr/bin`, `/c/Users`)
and Win32 forms (`C:\\msys64\\usr\\bin`, `C:\\Users`) at the boundary where an
MSYS process hands a path to something that does not share its worldview.
It is the subsystem where MSYS2 diverges most from its Cygwin ancestry, and
the one most likely to surprise.

## Architectural Classification

`subsystem:msys2:path-conversion`, contained by
[`msys-2.0.dll`](MSYS-2-0-DLL.md). Works in concert with the
[mount manager](MSYS-MOUNT-MANAGER.md), which supplies the prefix mapping
conversion applies.

## Responsibilities

- Converting POSIX paths to Win32 paths when an MSYS process invokes a
  native program, so the native program receives a path it can open.
- Converting arguments that look like paths, which is the behavior that makes
  this subsystem both useful and hazardous: it acts on things that resemble
  paths whether or not they are.
- Honoring `MSYS2_ARG_CONV_EXCL` to exclude arguments from conversion.

## Boundaries

Conversion happens at the process boundary, not inside a running program.
Native-to-native invocation involves no conversion at all. The rules are
MSYS2-specific: Cygwin documentation describes the derived design, but
argument conversion is precisely where MSYS2 differs, so Cygwin behavior
must not be assumed here.

## Interfaces

- `MSYS2_ARG_CONV_EXCL`, which excludes matching arguments from conversion.
- `MSYS`, which influences related runtime behavior.
- `cygpath`, the documented user-facing conversion tool.

## Dependencies

The [mount manager](MSYS-MOUNT-MANAGER.md) for prefix mappings, and the
Windows filesystem namespace for the target forms.

## Reverse Dependencies

Every MSYS process that invokes a native program — which includes most
build systems, since compilers in UCRT64 and CLANG64 are native while `make`
and the shell driving them are MSYS.

## Configuration

`MSYS2_ARG_CONV_EXCL` is the documented control. No controlled observation
of its effect exists in this knowledge base.

## Initialization and Execution Flow

Conversion rules depend on the mount table, which is read during runtime
initialization; see
[MSYS runtime initialization](MSYS-RUNTIME-INITIALIZATION.md).

## Runtime Behavior

No bounded probe in the 2026-07-30 collection exercised path conversion. The
behavior map lists "mount table and path-conversion observations" as the
required deep evidence for this row, and that evidence does not exist.

Everything on this page is documented design rather than observed behavior,
and that gap is wider here than for the process or signal subsystems, which
at least have one probe each.

## Compatibility and Variants

MSYS-only, and MSYS2-specific rather than Cygwin-inherited in its argument
handling.

## Security Considerations

No subsystem-specific vulnerability review has been performed. See
[Threat model and supply chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general posture; the runtime version observed was `3.6.10`.

## Failure Modes and Diagnostics

The characteristic failure is silent: an argument that merely resembled a
path is rewritten, and the receiving program gets plausible but wrong input
with no error anywhere. A flag value beginning with `/` is the common
trigger. `MSYS2_ARG_CONV_EXCL` is the documented remedy; `cygpath` is the
tool for inspecting what a path converts to.

## Evidence, Assumptions, and Open Questions

Design is attributed to the
[Cygwin User's Guide](https://cygwin.com/cygwin-ug-net/cygwin-ug-net.html)
(`evidence:cygwin:user-guide-2026-08-02`) with the explicit caveat that
argument conversion is where MSYS2 diverges from it.

Open, and the largest gap in Volume 3: no path-conversion observation of any
kind. No MSYS2-specific upstream documentation is registered as a source.

## Related Objects

- [msys-2.0.dll](MSYS-2-0-DLL.md)
- [Mount Manager](MSYS-MOUNT-MANAGER.md)
- [Environment Manager](MSYS-ENVIRONMENT-MANAGER.md)
