---
id: doc:volume-4:environment-ucrt64
title: UCRT64 Environment
volume: 4
status: partial
model_refs:
  - environment:msys2:ucrt64
  - repository:msys2:ucrt64
  - layer:msys2:4-runtime-environments
evidence_refs:
  - evidence:msys2:environments-2026-07-28
  - evidence:catalog:current
last_verified: 2026-08-02
---

# UCRT64 Environment

## Purpose

UCRT64 is MSYS2's default recommendation for new native x86_64 work: GCC
targeting Microsoft's Universal CRT. It is the migration destination for
[MINGW64](ENVIRONMENT-MINGW64.md), and the environment most of this
knowledge base's toolchain and library pages document.

## Architectural Classification

| Attribute | Value |
| --- | --- |
| Prefix | `/ucrt64` |
| ABI | MinGW-w64 x86_64, UCRT-facing |
| Architecture | x86_64 |
| Compiler | GCC |
| C runtime | Universal CRT (UCRT) |
| C++ library | libstdc++ |
| Linker | GNU ld, from [GNU Binutils](GNU-BINUTILS.md) |
| Executable format | PE32+, native Windows, no `msys-2.0.dll` import |
| Package repository | `repository:msys2:ucrt64` — 3,898 packages in the current snapshot |
| Lifecycle | Active, default recommendation |

UCRT64 carries the largest package count of the six repositories, which is
the clearest catalog-level signal of its default status.

## Responsibilities

- Providing a GCC toolchain and library ecosystem that targets the UCRT,
  the C runtime Microsoft currently supports.
- Serving as the default target for new native x86_64 development and the
  recommended destination for MINGW64 migration.

## Boundaries

UCRT64 produces native Windows binaries with no dependency on
`msys-2.0.dll`; it is not a POSIX environment and does not provide the
process semantics [MSYS](ENVIRONMENT-MSYS.md) does.

It shares the UCRT with [CLANG64](ENVIRONMENT-CLANG64.md) and
[CLANGARM64](ENVIRONMENT-CLANGARM64.md) but not the C++ standard library:
UCRT64 uses libstdc++ where the Clang environments use libc++. C++ objects
are therefore not interchangeable across that boundary even though the C
runtime matches.

## Interfaces

- The Win32 and UCRT API surfaces, reached directly rather than through a
  POSIX translation layer.
- MinGW-w64 headers and import libraries supplying the Windows API to GCC.

## Dependencies

The environment itself is modeled as a target rather than a consumer; the
dependency structure that matters is per-package, and is documented on the
individual library and toolchain pages that carry
`applicability.environment_ids` of `environment:msys2:ucrt64`.

## Reverse Dependencies

The bulk of this knowledge base's Volume 6 library pages and Volume 8
toolchain pages document UCRT64-packaged artifacts, including
[GCC](GNU-GCC.md), [GDB](GNU-GDB.md), [CMake](CMAKE.md), and the
`mingw-w64-ucrt-x86_64-*` library set.

## Configuration

Environment selection is by launcher and `MSYSTEM`; the prefix `/ucrt64` is
prepended to `PATH` ahead of `/usr`. Per-package configuration belongs to
the individual package pages.

## Initialization and Execution Flow

A UCRT64 binary is loaded directly by the Windows image loader with no
intermediate runtime. There is no equivalent of MSYS's
`msys-2.0.dll` initialization sequence.

## Runtime Behavior

Behavior is native Windows behavior. Programs see Windows path forms,
Windows process semantics, and Windows signal approximations rather than
the POSIX equivalents MSYS provides.

## Compatibility and Variants

Strengths: current Microsoft-supported CRT; better C99/C11 conformance than
MSVCRT; the largest package selection; GCC familiarity for projects moving
from Linux; the documented default, so it receives the most upstream
packaging attention.

Weaknesses: libstdc++ C++ ABI does not interoperate with the libc++ used by
the Clang environments; UCRT requires a redistributable on older Windows
versions where MSVCRT was always present; and x86_64 only, so ARM64 targets
need [CLANGARM64](ENVIRONMENT-CLANGARM64.md).

## Security Considerations

No environment-specific vulnerability review has been performed. See
[Threat model and supply chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general posture.

## Failure Modes and Diagnostics

A link failure mixing UCRT64 and MINGW64 objects most commonly presents as
duplicate or missing CRT symbols rather than an explicit ABI error; the
first diagnostic is to confirm every object and static library in the link
came from the same prefix.

## Migration Strategy

From MINGW64: rebuild every object and static library; audit third-party
binary dependencies for MSVCRT assumptions; check any interface that
exchanges CRT-owned objects such as `FILE*` across a DLL boundary.

From MINGW32: treat as a port rather than a rebuild — pointer-width
assumptions need review.

To CLANG64: rebuild; C++ code additionally changes standard library, which
is a larger change than the CRT match suggests.

## Evidence, Assumptions, and Open Questions

Prefix, architecture, CRT, compiler family, and default-recommendation
status are backed by the
[official MSYS2 environment documentation](https://www.msys2.org/docs/environments/)
(`evidence:msys2:environments-2026-07-28`). The 3,898-package count is from
the pacman catalog snapshot (`evidence:catalog:current`). Open: the UCRT
redistributable claim is from Microsoft's platform documentation rather than
a controlled observation on this project's hosts.

## Related Objects

- [Runtime environment comparison](RUNTIME-ENVIRONMENTS.md)
- [MSYS](ENVIRONMENT-MSYS.md)
- [CLANG64](ENVIRONMENT-CLANG64.md)
- [MINGW64](ENVIRONMENT-MINGW64.md)
- [MSYS2 and MinGW-w64 role model](MSYS2-AND-MINGW-W64-ROLE-MODEL.md)
