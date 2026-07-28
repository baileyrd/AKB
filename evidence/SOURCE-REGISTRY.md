# Source Registry

This registry defines source classes and ingestion targets. Concrete retrieval
records belong in the machine-readable evidence collection.

| Source family | Intended evidence | Refresh strategy |
| --- | --- | --- |
| MSYS2 website and documentation | Environment, package-management, filesystem, and operational intent | Scheduled content snapshot |
| MSYS2 package databases | Package metadata and repository membership | Per repository snapshot |
| MSYS2 package recipes | Build dependencies, patches, flags, sources, and outputs | Commit-addressed ingestion |
| MSYS2 runtime source | POSIX emulation implementation and behavior | Tag/commit-addressed analysis |
| MinGW-w64 source and documentation | CRT, headers, import libraries, and ABI support | Release/commit snapshot |
| GNU upstream projects | Userland architecture, configuration, and source organization | Release/tag snapshot |
| LLVM project | Clang, LLD, LLDB, runtime, and source architecture | Release/tag snapshot |
| Microsoft documentation | Win32, NT, console, ConPTY, filesystem, security, networking, and UCRT | Date-qualified snapshot |
| Git for Windows sources and docs | Distribution, launcher, shell, native Git, transport, and integrations | Release/commit snapshot |
| Binary package contents | Files, PE metadata, DLL imports/exports, archives, headers, and configuration | Reproducible extraction |
| Controlled runtime observations | Startup, environment, mounts, processes, path conversion, and performance | Scripted experiment |
| Local pacman synchronization databases | Enabled repository package metadata, installation state, dependencies, groups, conflicts, replacements, and sizes | On-demand or scheduled `catalog-msys2-packages.ps1` snapshot |

## Acceptance rules

1. Prefer primary sources.
2. Record retrieval timestamp, source version, commit, package version, or
   repository database checksum as applicable.
3. Preserve exact locators without copying excessive source content.
4. Hash downloaded machine inputs.
5. Treat scripts and observations as derived or observed evidence.
6. Record failed or contradictory observations rather than discarding them.
7. Never infer package or runtime behavior solely from a filename.
