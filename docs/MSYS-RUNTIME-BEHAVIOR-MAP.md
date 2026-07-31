---
id: doc:volume-3:msys-runtime-behavior-map
title: MSYS Runtime Behavior Architecture Map
volume: 3
status: partial
model_refs:
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:msys-runtime:git-for-windows-comparative-observation-2026-07-30
last_verified: 2026-07-30
---

# MSYS Runtime Behavior Architecture Map

The [Level 3 runtime-boundary diagram](../diagrams/level-3-msys-runtime-boundary.svg)
is the navigation companion to this map. It distinguishes MSYS-dependent
execution from native environment execution before drilling into individual
adaptation concerns.

| Concern | MSYS runtime responsibility | Windows-facing boundary | Required deep evidence |
| --- | --- | --- | --- |
| Process creation | Present POSIX process semantics where supported | Windows process creation and handles | Runtime source and controlled probes |
| `fork()` / `exec()` | Adapt POSIX lifecycle expectations | Process image, inheritance, loader | Version-qualified implementation analysis |
| Signals | Map POSIX signal behavior to available host mechanisms | Threads, processes, console control | Behavioral test matrix |
| Paths and mounts | Translate MSYS paths and virtual mount rules | Drive/UNC/filesystem namespaces | Mount table and path-conversion observations |
| Filesystem and symlinks | Present POSIX-like file operations | NTFS/ReFS/Win32 semantics | Filesystem probes by host/version |
| PTY and console | Provide terminal-facing abstractions | Console, ConPTY, pipes | Terminal integration tests |

## Boundary Rule

These services apply to MSYS-dependent processes. Native UCRT64, CLANG64, and
MinGW programs use Windows-facing runtime behavior directly unless they
explicitly load the MSYS runtime.

## Evidence Gaps

This is a responsibility map, not a claim of exact implementation ordering or
feature parity. Each row requires source revision, Windows version, and
reproducible observation evidence before being elevated beyond `partial`.

## Controlled local observation

On 2026-07-30, the bounded `--behavior` collector ran through the isolated
MSYS x86_64 shell (MSYS runtime reported by `uname` as `3.6.10`). Its raw
output is retained locally rather than committed. The following are exact
command outcomes, not general compatibility claims:

| Probe | Observed outcome | Boundary |
| --- | --- | --- |
| Process lifecycle | Background child existed and exited with status 0 | A shell child/process-management observation only |
| Shell `exec` | Replaced shell emitted `exec-ok` with status 0 | Does not characterize loader behavior |
| Signal delivery | A shell `USR1` trap emitted `signal=USR1` with status 0 | Does not establish the complete signal mapping |
| Filesystem symlink | `ln -s` succeeded and the target was readable, but `test -L` returned non-zero | The collector preserves this classification discrepancy; it does not claim POSIX symlink parity |
| Terminal-device namespace | `/dev` and `/dev/tty` existed | This is not a PTY allocation or ConPTY integration test |

The collector has a five-second bound per probe and creates/removes only a
fresh temporary directory for the symlink check. See the
[runtime observation contract](RUNTIME-OBSERVATION-CONTRACT.md) for the
command and retention boundary.

## Comparative observation: Git for Windows' bundled MSYS runtime

On 2026-07-30, the same probe battery was run manually against a second,
distinct MSYS distribution on the same host: Git for Windows' own bundled
`msys-2.0.dll` (`C:\Program Files\Git\usr\bin\msys-2.0.dll`, 3,368,543
bytes). `uname -a` reported runtime `3.6.9-b4195d69.x86_64` — a different
version from the isolated MSYS2 installation's `3.6.10` above, confirming
these are genuinely separate MSYS runtime deployments, not the same
binary observed twice.

| Probe | Observed outcome | Compared to the isolated installation above |
| --- | --- | --- |
| Process lifecycle | Background child ran; `wait` exit status 0 | Same outcome |
| Shell `exec` | Replaced shell emitted `exec-ok`, status 0 | Same outcome |
| Signal delivery | A `USR1` trap fired, status 0 | Same outcome |
| Filesystem symlink | `ln -s` exited 0, but `stat` reported a **regular file** containing a full copy of the target's bytes, not a symlink; confirmed at the Windows API level (`Attributes=Archive`, no `ReparsePoint` flag, no `LinkType`) | **Diverges**: a full-content-copy fallback, not merely the isolated installation's narrower "`test -L` false while still readable through it" discrepancy |

Both `MSYS` and `CYGWIN` environment variables were unset (default) for
this probe. The symlink divergence is a concrete instance of this page's
own Evidence Gaps caveat: MSYS symlink fallback behavior is
installation/configuration-dependent (see the `winsymlinks` mode family),
so neither observation generalizes to "MSYS symlinks behave as X" without
naming the specific distribution, version, and environment configuration.
This is also consistent with
[Windows platform boundaries](WINDOWS-PLATFORM-BOUNDARIES.md#controlled-local-host-observation)'s
finding that native symlink creation requires elevation in this same
non-elevated session — the runtime's fallback path, not a defect.

## Related Views

- [Runtime initialization](MSYS-RUNTIME-INITIALIZATION.md)
- [Runtime environments](RUNTIME-ENVIRONMENTS.md)
