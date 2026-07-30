---
id: doc:volume-5:gnu-sed
title: GNU Sed
volume: 5
status: partial
model_refs:
  - component:gnu:sed
  - package:msys2:sed
  - environment:msys2:msys
  - runtime:msys2:msys-2.0.dll
evidence_refs:
  - evidence:gnu:sed-manual-2026-07-30
  - evidence:catalog:current
  - evidence:msys2:environments-2026-07-28
last_verified: 2026-07-30
---

# GNU Sed

## Purpose

Sed applies a small scripting language to transform text streams
non-interactively, one line (or addressed range of lines) at a time. This
page documents its architectural role, dependency footprint, and the
in-place editing and execute-command behaviors most relevant to safe use in
scripts; see the
[official GNU Sed manual](https://www.gnu.org/software/sed/manual/sed.html)
for the full command language.

## Architectural Classification

`component:gnu:sed` is a GNU-userland component packaged as
`package:msys2:sed` (version `4.9-1` in the current catalog snapshot,
license `GPL3`), belonging to the MSYS environment. It sits between
[GNU Grep](GNU-GREP.md) (read-only search) and [GNU Awk](GNU-AWK.md)
(general-purpose text-processing language) in capability: sed transforms
text via addressed commands but is not intended as a general programming
language.

## Responsibilities

- Line-by-line text substitution, deletion, and insertion driven by
  addressed commands (`s///`, `d`, `i`, `a`, `p`).
- In-place file editing (`-i`), optionally with a backup suffix.
- Conditional control flow via labels and branch commands (`:`, `b`, `t`),
  which the manual documents as sufficient for expressing loops and
  conditionals beyond simple per-line substitution.

## Boundaries

Sed is not a general-purpose programming language in practice: scripts
needing arrays, functions, or arithmetic are conventionally written in
[GNU Awk](GNU-AWK.md) instead. Sed's role is scoped to stream/file
transformation, not filesystem traversal (that is
[GNU Findutils](GNU-FINDUTILS.md)) or read-only search (that is
[GNU Grep](GNU-GREP.md)).

## Interfaces

- Script sources: `-e` (inline script) and `-f` (script file), composable.
- `-i[SUFFIX]` in-place editing, `-n` to suppress automatic printing,
  `-E`/`-r` for extended regular expressions.
- Addressing: line numbers, ranges, regex addresses, and step addresses
  (`first~step`), per the manual's addressing chapter.

## Dependencies

The catalog snapshot records one `runtime-depends-on` edge for
`package:msys2:sed`:

| Dependency | Package | Architectural reason |
| --- | --- | --- |
| Native-language messages | `package:msys2:libintl` | gettext-based message translation (NLS). |

A second recorded dependency, `sh`, is not explained by this snapshot alone
and is recorded as open work, consistent with the same unexplained `sh`
dependency noted for [GNU Grep](GNU-GREP.md).

## Reverse Dependencies

The snapshot records 14 relationships targeting `package:msys2:sed` — the
highest of the four tools covered in this batch, consistent with sed's
common use inside other packages' build and configuration scripts for
text substitution. See the
[reverse dependency impact analysis](REVERSE-DEPENDENCY-IMPACT-ANALYSIS.md)
for the current full list.

## Configuration

Sed has no persistent configuration file. `POSIXLY_CORRECT` disables some
GNU extensions, and `LC_ALL`/`LANG` affect locale-sensitive character-class
and collation matching in regular expressions, per the manual.

## Initialization and Execution Flow

Sed is an invoke-run-exit process with no persistent session. Process
creation for this MSYS-dependent binary is adapted from POSIX semantics onto
Windows process primitives by `msys-2.0.dll`, per
[MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md); this page does
not restate that mechanism.

## Runtime Behavior

`-i` in-place editing is documented to work by writing to a temporary file
and then replacing the original, which affects file permissions and hard
links. The exact temporary-file placement and replace mechanism as executed
on the MSYS/NTFS boundary in this environment has not been directly observed
and is recorded as open work rather than asserted.

## Compatibility and Variants

GNU sed's `-i` takes an optional backup-suffix argument, whereas BSD/macOS
sed historically requires an explicit (possibly empty) suffix argument;
scripts intended to be portable across both commonly special-case this
difference. This is background portability context rather than a claim
sourced to the GNU Sed manual itself, which documents GNU sed's own syntax
rather than other implementations.

## Security Considerations

The manual documents an `e` command (and an `s///e` flag) that executes the
pattern space, or a given command, as a shell command and substitutes its
output. This means a sed script built from untrusted input can execute
arbitrary shell commands — a materially different risk profile from grep or
find, which do not execute shell commands as part of their own scripting
language. See
[Threat Model and Supply Chain](THREAT-MODEL-AND-SUPPLY-CHAIN.md) for the
project's general supply-chain posture.

## Failure Modes and Diagnostics

Unanchored or overly greedy substitution patterns are the most common
correctness bug; the manual recommends testing with `-n` plus explicit `p`
commands before running a destructive `-i` edit. Regex-dialect confusion
between basic (default) and extended (`-E`/`-r`) mode is the most common
portability bug, mirroring the same dialect-selection issue documented for
[GNU Grep](GNU-GREP.md).

## Evidence, Assumptions, and Open Questions

Command-language, addressing, and `-i`/`e`-command semantics are backed by
the official GNU Sed manual (`evidence:gnu:sed-manual-2026-07-30`). Package
identity, version, license, and dependency edges are backed by the pacman
catalog snapshot (`evidence:catalog:current`). Open: the recorded `sh`
runtime dependency is unexplained pending file-inventory evidence, and the
exact `-i` temporary-file/replace behavior on this environment's filesystem
boundary has not been directly observed.

## Related Objects

- [GNU Userland Role Model](GNU-USERLAND-ROLE-MODEL.md)
- [GNU Grep](GNU-GREP.md)
- [GNU Awk (gawk)](GNU-AWK.md)
- [MSYS Runtime Initialization](MSYS-RUNTIME-INITIALIZATION.md)
