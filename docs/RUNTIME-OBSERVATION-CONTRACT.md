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

The collector also records bounded, read-only observations of `uname`, MSYS
`cygpath` conversion in both directions, and the MSYS mount table. Output is
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

`Update-Akb.ps1` invokes this stage by default. Use `-SkipRuntimeObservation`
when collecting package state alone.
