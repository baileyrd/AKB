---
id: doc:volume-4:runtime-observation-contract
title: Runtime Observation Contract
volume: 4
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-08-02
---

# Runtime Observation Contract

Bootstrap 0.4 records bounded, local observations for one active MSYS2
environment. It complements package and artifact inventory; it does not infer
runtime behavior that was not observed.

## Trust boundary

The collector records only an explicit allow-list of environment variables:
`MSYSTEM`, `MSYSTEM_PREFIX`, `MSYS2_PATH_TYPE`, `CHERE_INVOKING`, and `OSTYPE`.
It deliberately excludes `PATH`, credentials, tokens, home-directory state,
and arbitrary process environment values.

Tool identity is captured by resolving a fixed list of commands and, when
possible, reading their first `--version` output line. Tool execution is
bounded by a three-second timeout and does not perform package installation,
network activity, or configuration changes.

When a resolved tool cannot execute, the observation records `executed: false`
and a sanitized exception class. This is particularly relevant when inspecting
a target-architecture environment from a host that cannot execute its native
binaries; discovery is not evidence of successful execution.

The collector also records bounded, read-only observations of `uname`, MSYS
`cygpath` conversion in both directions, the MSYS mount table, and the
executing process's `/proc/self/exe` link. Output is
limited to 8,000 characters per probe. These probes describe the MSYS
shell/runtime executing the collector even when its selected `MSYSTEM` is a
native environment; they are not evidence of native UCRT64/MinGW runtime
semantics.

## Lifecycle

```text
active MSYS2 environment
  -> bounded runtime observation
  -> schema and field validation
  -> generated configuration projection
  -> environment report and composed graph
```

The projection creates one generated `configuration` entity per observed
environment, linked to its authored `environment` entity. It never changes
authored environment facts. A new import replaces the current observation for
that environment while retaining current observations for other environments.
Historical raw observations can be retained by the caller alongside other
evidence snapshots.

## Use

Run from the target environment so executable lookup reflects that environment:

```powershell
python tools/collect_runtime_observation.py --environment ucrt64 `
  --output work/runtime-observation.json
python tools/import_runtime_observation.py work/runtime-observation.json
python tools/akb.py all
```

For a controlled MSYS-shell behavior observation, add `--behavior`. This
opt-in suite records the outcome of bounded process-lifecycle, shell `exec`,
signal-delivery, filesystem-symlink, and terminal-device-namespace probes.
It does not claim general process, loader, filesystem, or PTY behavior beyond
the exact command result. The symlink probe uses a newly-created temporary
directory and removes it before the shell exits.

`Update-Akb.ps1` invokes this stage by default. Use `-SkipRuntimeObservation`
when collecting package state alone.
