# Architecture Model

The canonical model is a typed property graph serialized as JSON. It may later
be projected into SQLite, DuckDB, a graph database, JSON-LD, RDF, or other
stores without changing object identity.

## Core records

- `entity`: an architecture object with identity and properties;
- `relationship`: a typed, directional edge between two entities;
- `evidence`: a source or observation supporting objects or claims;
- `claim`: a fact, observation, or inference with evidence and confidence;
- `snapshot`: a time- and version-bounded view of mutable upstream state;
- `view`: a reproducible selection and projection used by a document, diagram,
  index, matrix, or explorer route.

## Modeling distinctions

The model deliberately separates:

- upstream project from distribution package;
- package recipe from built package artifact;
- package artifact from installed file;
- logical library from DLL, import library, static archive, and headers;
- build dependency from runtime dependency;
- package dependency from binary DLL import;
- environment membership from ABI compatibility;
- filesystem containment from architectural composition;
- implementation from deployment;
- current truth from snapshot-bound observation.

## Relationship semantics

Relationships are directional. Reverse navigation is generated rather than
stored as duplicate edges. Each relationship can include scope, conditions,
version constraints, discovery method, confidence, and evidence.

