# ADR 0002 — Dependency-free schema checking

- **Status**: Accepted
- **Date**: 2026-08-02
- **Supersedes**: none

## Context

`model/schema/*.schema.json` has held three JSON Schema documents since the
first commit. None was ever executed: `jsonschema` is imported nowhere in the
repository, so the constraints they express were documentation rather than
enforcement. A charter audit recorded this as a live defect — a typo in an
identifier-valued property would pass CI in silence.

Closing it means running the schemas. The obvious way is the `jsonschema`
package. That conflicts with a property this repository currently holds:

- there is no `requirements.txt`, `pyproject.toml`, `setup.py`, or
  `setup.cfg`;
- `.github/workflows/validate.yml` has no install step — it sets up Python
  and runs `unittest`, `akb.py`, and the generators directly;
- `tools/build_explorer.py` describes its own output as a "no-dependency
  static explorer", so the property is deliberate at least there.

The property was never written down as a decision, which is why this ADR
exists at all: `charter/adr/` contained only a README and a template despite
the governance section stating that ADRs govern cross-cutting choices.

## Decision

Implement the closed subset of JSON Schema that these three schemas actually
use, in `tools/schema_check.py`, rather than adding a runtime dependency.

The subset was measured, not guessed. Across all three schemas the keywords
in use are: `type`, `properties`, `required`, `additionalProperties`,
`items`, `$ref`, `enum`, `const`, `pattern`, `minLength`, `minimum`,
`minItems`, `uniqueItems`, `format`. Every `$ref` is an internal
`#/$defs/` reference and the only `format` is `date-time`. The constructs
that make a general implementation hard — `oneOf`, `allOf`, `anyOf`, `not`,
`patternProperties`, external references — do not appear.

`assert_supported()` rejects any keyword outside that list, so a schema that
grows past the subset fails the build rather than quietly becoming
unenforced again. That failure mode is the whole reason this ADR is
acceptable: the risk of a partial implementation is silent under-checking,
and this makes it loud instead.

## Consequences

**Accepted:**

- The repository stays installable and runnable with a bare Python 3.11 and
  no network, which is what CI currently assumes.
- The schemas become enforced on every push, against `model/graph.json`,
  `model/catalog/current.json`, and `model/inventory/current.json`.
- Running them immediately found a real inconsistency: 30 claim identifiers
  use a four-segment form and 9 use three, while entities, relationships,
  and evidence are uniformly three-segment.

**Costs:**

- `tools/schema_check.py` is a partial JSON Schema implementation and must
  be maintained as the schemas evolve. This is a real ongoing cost, bounded
  by `assert_supported()` making the boundary explicit.
- It is not a conformance-tested implementation. Its correctness is
  established by `tests/test_schema_conformance.py` rather than by the JSON
  Schema test suite.

**Revisit if:** the schemas need constructs outside the subset, another part
of the project needs a dependency anyway, or the maintenance cost of the
checker exceeds the value of the zero-dependency property. Adding
`jsonschema` and deleting `tools/schema_check.py` is a small, contained
change if that day comes.

## Notes

The claim-identifier inconsistency this surfaced is **not** resolved by this
decision. `$defs/claimId` accepts both forms and documents which is
preferred, because 33 claim identifiers are cited by name in documentation
prose and renaming them would break those citations. Normalising the nine
outliers is recorded as open work rather than silently blessed.
