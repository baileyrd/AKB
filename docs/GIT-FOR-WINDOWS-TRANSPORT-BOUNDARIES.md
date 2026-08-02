---
id: doc:volume-9:git-for-windows-transport-boundaries
title: Git for Windows Transport, Credentials, and DLL Boundaries
volume: 9
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-28
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

## Mechanism pages

[HTTP transport](GIT-FOR-WINDOWS-HTTP-TRANSPORT.md) documents the cURL and
TLS-backend mechanism behind the HTTPS row;
[credential manager](GIT-FOR-WINDOWS-CREDENTIAL-MANAGER.md) documents the
helper protocol behind the credential row.

## Related Views

- [Git for Windows boundary](GIT-FOR-WINDOWS-BOUNDARY.md)
- [Git for Windows launcher and shell startup](GIT-FOR-WINDOWS-LAUNCHER-STARTUP.md)
- [MSYS runtime behavior map](MSYS-RUNTIME-BEHAVIOR-MAP.md)
