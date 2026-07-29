---
id: doc:volume-10:diagram-hierarchy
title: Linked Diagram Hierarchy
volume: 10
status: partial
model_refs: [ecosystem:msys2:msys2]
evidence_refs: []
last_verified: 2026-07-29
---

# Linked Diagram Hierarchy

The Level 0 ecosystem diagram is a stable entry point into the Explorer. It
uses direct links for canonical objects and routes to the generated runtime,
package, and toolchain views. Higher levels must preserve this contract: each
node links to a stable object route or an explicitly snapshot-qualified view.

![MSYS2 Level 0 architecture](../diagrams/level-0-ecosystem.svg)

![MSYS2 Level 1 eight layers](../diagrams/level-1-eight-layers.svg)

![MSYS2 Level 2 runtime and package flow](../diagrams/level-2-runtime-package-flow.svg)

![MSYS2 Level 3 MSYS runtime boundary](../diagrams/level-3-msys-runtime-boundary.svg)

![MSYS2 Level 4 environment matrix](../diagrams/level-4-environment-matrix.svg)

![MSYS2 Level 5 package-to-artifact evidence](../diagrams/level-5-package-artifact-evidence.svg)

![MSYS2 Level 6 toolchain and build-output flow](../diagrams/level-6-toolchain-build-flow.svg)

The diagram is conceptual. Package and dependency counts are not encoded in
the diagram itself; consult the generated catalog views for snapshot evidence.
