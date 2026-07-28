# Documentation Standard

## Required metadata

Every authored page begins with:

```yaml
---
id: doc:<volume>:<slug>
title: Human-readable title
volume: 1
status: planned
model_refs: []
evidence_refs: []
last_verified: null
---
```

## Required object-page headings

Use headings when applicable; record `Not applicable` with a reason instead of
silently omitting an expected concern.

1. Purpose
2. Architectural Classification
3. Responsibilities
4. Boundaries
5. Interfaces
6. Dependencies
7. Reverse Dependencies
8. Configuration
9. Initialization and Execution Flow
10. Runtime Behavior
11. Build and Packaging
12. Files and Directory Structure
13. Compatibility and Variants
14. Security Considerations
15. Performance Considerations
16. Failure Modes and Diagnostics
17. Extension and Migration
18. Examples
19. Diagrams
20. Evidence, Assumptions, and Open Questions
21. Related Objects

## Evidence classes

| Class | Meaning |
| --- | --- |
| primary | Upstream source, official documentation, package database, or signed artifact |
| derived | Reproducible analysis of primary evidence |
| observed | Reproducible runtime or filesystem observation |
| secondary | Credible third-party explanation |
| inference | Architectural conclusion drawn from cited evidence |

Each evidence reference records retrieval time, upstream version or snapshot,
license constraints, integrity data when available, and the exact object or
claim it supports.

## Confidence

| Value | Meaning |
| --- | --- |
| verified | Confirmed by primary evidence and, where appropriate, observation |
| high | Strong evidence with no material conflict |
| medium | Partial evidence or version-sensitive interpretation |
| low | Preliminary evidence requiring verification |
| unknown | Explicitly unresearched |

## Diagram requirements

- Every diagram has a stable diagram ID, title, purpose, scope, depth, and
  generated textual inventory.
- Nodes link to object pages; edges use controlled relationship types.
- A diagram declares whether it is conceptual, logical, runtime, build,
  package, deployment, sequence, data, security, or dependency-oriented.
- Large graphs use clustering, filtering, progressive disclosure, and
  server- or build-time layout.
- Color is never the only carrier of meaning.
- Generated SVGs preserve stable anchors and accessible labels.

## Writing rules

- Distinguish distribution, runtime, environment, subsystem, package, project,
  library, binary, and source unit precisely.
- Qualify time-sensitive claims with the applicable version or snapshot.
- Separate fact, observation, and inference.
- Explain the reason and consequence of relationships, not only their existence.
- Avoid treating MSYS2 and MinGW-w64 as replacements for one another; model
  their distinct roles and integration.
- Use Windows paths and POSIX paths exactly as observed and state the active
  translation context.

