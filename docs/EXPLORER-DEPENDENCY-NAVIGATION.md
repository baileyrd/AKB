---
id: doc:volume-18:explorer-dependency-navigation
title: Explorer Dependency Navigation
volume: 18
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-28
---

# Explorer Dependency Navigation

Each object page derives a forward **Dependencies** list and reverse
**Dependents** list from canonical graph edges. The explorer treats
`*-depends-on`, `requires`, and `imports-dll` as dependency-navigation edges,
while retaining the complete incoming/outgoing relationship lists below them.
This makes dependency impact navigable without conflating package declarations,
binary imports, and non-dependency architectural relationships.
