---
id: doc:volume-9:git-for-windows-transport-boundaries
title: Git for Windows Transport, Credentials, and DLL Boundaries
volume: 9
status: partial
model_refs:
  - ecosystem:msys2:msys2
  - library:gnu:zlib
evidence_refs:
  - evidence:git-for-windows:local-installation-observation-2026-07-30
  - evidence:git-for-windows:cmd-exe-shell-context-observation-2026-07-31
last_verified: 2026-07-31
---

# Git for Windows Transport, Credentials, and DLL Boundaries

Git for Windows connects a native Git executable to several independently
configured integration domains.  An observed command path is required before
assigning a transport, authentication, TLS, or runtime-loading behavior to a
particular installation.

| Domain | Architectural responsibility | Evidence boundary |
| --- | --- | --- |
| Native Git executable | Orchestrates Git operations and configured helper invocations | Executable path and version are invocation-specific artifacts |
| SSH | Provides remote transport using client configuration and keys | Capture configuration provenance; never capture private keys or passphrases |
| HTTP and libcurl | Transfers over HTTP(S), including proxy handling | Proxy, CA, and TLS behavior depend on effective configuration and bundled versions |
| Credential helper | Acquires or stores authentication secrets outside Git's repository data | Record helper selection only after sanitization; never ingest secrets, tokens, or store contents |
| Crypto and TLS | Verifies encrypted transport and certificate chains | Package/version and policy claims require artifact-level evidence |
| DLL loader | Resolves runtime dependencies for the launched executable | Inspect the actual executable and resolved DLL set; do not infer them from distribution branding |

## Decision Rules

1. Distinguish Git configuration that selects a credential helper from the
   credential store the helper uses. The latter is secret-bearing and outside
   AKB evidence collection.
2. When configuration provenance is needed, use a sanitized observation of
   `git config --show-origin`; redact credentials, tokens, private paths when
   sensitive, and proxy userinfo before retaining it.
3. Treat SSH and HTTP as alternative transport paths selected per remote and
   invocation. Their client, proxy, certificate, and authentication behavior
   must be observed independently.
4. Establish DLL-loading claims from a specific binary and its runtime
   dependency evidence. A Git Bash launch and a native-terminal launch can
   select different executable and DLL-resolution paths.
5. Keep certificate stores, crypto providers, and helper implementations as
   versioned deployment facts rather than permanent properties of Git for
   Windows.

## Diagnostic Sequence

1. Identify the invoked Git executable, working environment, and remote URL.
2. Classify the selected transport as SSH or HTTP(S).
3. Record only sanitized effective configuration and its origin.
4. Collect binary and DLL evidence for that executable before attributing a
   startup or transport failure to the distribution.

## Controlled local installation observation

On 2026-07-30, `ssh.exe` and `curl.exe` resolved to genuinely different
binaries depending on invoking shell context — not the same executable
observed from two vantage points. Per the launcher-path evidence in
[Launcher and Shell Startup](GIT-FOR-WINDOWS-LAUNCHER-STARTUP.md#controlled-local-installation-observation):

| Command | Git Bash session | PowerShell session |
| --- | --- | --- |
| `ssh` | `Git\usr\bin\ssh.exe`, `OpenSSH_10.3p1, OpenSSL 3.5.7` | `Windows\System32\OpenSSH\ssh.exe`, `OpenSSH_for_Windows_9.5p2, LibreSSL 3.8.2` |
| `curl` | `Git\mingw64\bin\curl.exe`, `curl 8.21.0 (x86_64-w64-mingw32) libcurl/8.21.0 Schannel zlib/1.3.2 brotli/1.2.0 zstd/1.5.7 libidn2/2.3.8 libpsl/0.21.5 libssh2/1.11.1 WinLDAP` | `Windows\System32\curl.exe`, `curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.3.2 WinIDN WinLDAP` |

Both `ssh` implementations report distinct OpenSSH releases *and* distinct
underlying TLS libraries (OpenSSL vs. LibreSSL); both `curl` builds report
the identical `8.21.0` version number yet a materially different compiled
feature set (no `brotli`/`zstd`/`libssh2`/`libidn2` in the system build).
This is directly observed, single-workstation evidence: it does not
establish which resolution order any other installation, shell, or script
invocation will use.

A third invocation context, `cmd.exe`, was observed on 2026-07-31 to
resolve identically to the PowerShell session above, not as a distinct
third behavior: `where ssh` listed `C:\Windows\System32\OpenSSH\ssh.exe`
first (matching PowerShell's resolution, `OpenSSH_for_Windows_9.5p2,
LibreSSL 3.8.2`), and `where curl`/`curl --version` resolved only to
`C:\Windows\System32\curl.exe`. Direct `PATH` inspection explains why:
`C:\Program Files\Git\mingw64\bin` (where Git for Windows' own `curl.exe`
lives) is absent from the base Windows user `PATH` entirely — only
`Git\cmd` and `Git\usr\bin` are present — while `C:\Windows\System32\OpenSSH\`
precedes `Git\usr\bin` in that same `PATH`. `cmd.exe` and PowerShell share
this base `PATH`; Git Bash's distinct resolution in the table above is not
a property of "PowerShell vs. Git Bash" as two arbitrary shells, but of
Git Bash's own shell-launch machinery augmenting `PATH` with
`Git\mingw64\bin` for its session specifically, which the base Windows
environment does not do. This remains single-workstation evidence for
this one `PATH` configuration.

**Credential helper** (sanitized, per Decision Rule 2): `git config
--show-origin --get credential.helper` reported `manager`, sourced from
`file:C:/Program Files/Git/etc/gitconfig` — Git Credential Manager,
selected at the distribution-default configuration layer on this
installation. No credential store contents were accessed.

**DLL loader**: a direct PE-import parse of `mingw64\bin\git.exe`
(4,383,048 bytes, SHA-256
`1a0043555d254618f2d56c936c3d9a1fbfb878bc878416a133c346bc7835eda9`,
`tools/deep_inventory.py`'s own `parse_pe`) recorded 10 imported DLLs:
`advapi32.dll`, `kernel32.dll`, `msvcrt.dll`, `ntdll.dll`, `user32.dll`,
and `ws2_32.dll` (Windows system DLLs), plus `libiconv-2.dll`,
`libintl-8.dll`, `libpcre2-8-0.dll`, and `zlib1.dll` — MSYS-derived
shared libraries bundled directly into the native `git.exe`, not the
Git-for-Windows-packaged [zlib (UCRT64)](ZLIB.md) or MSYS2 pacman-managed
zlib this knowledge base otherwise documents. This is the first
byte-level confirmation in this knowledge base of
[Git for Windows boundary](GIT-FOR-WINDOWS-BOUNDARY.md)'s claim that the
distribution "incorporat[es] MSYS-derived tooling"; it establishes an
import-table fact for this one binary and version only, not a general
DLL-compatibility or loader-resolution claim.

## Related Views

- [Git for Windows boundary](GIT-FOR-WINDOWS-BOUNDARY.md)
- [Git for Windows launcher and shell startup](GIT-FOR-WINDOWS-LAUNCHER-STARTUP.md)
- [MSYS runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md)

<!-- BEGIN GENERATED dependency-subgraph -->

## Dependency Diagram

```mermaid
flowchart LR
    subject["MSYS2"]
    d0["Microsoft Windows"]
    subject -->|requires| d0
    style subject stroke-width:3px
```

Dependencies and dependents of `ecosystem:msys2:msys2` in the composed graph: 0 dependents and 1 dependency.

Generated from the composed model by `tools/build_object_diagrams.py`.
Edits between the surrounding markers are overwritten on the next build.

<!-- END GENERATED dependency-subgraph -->
