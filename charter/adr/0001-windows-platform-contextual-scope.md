# ADR 0001 — Windows platform is contextual scope

- **Status**: Accepted
- **Date**: 2026-08-02 (recording a decision already in effect)
- **Supersedes**: none

## Context

The originating project charter lists Windows as a scope area and names eight
subsystems under it: NT Kernel, Win32, Console, ConPTY, Filesystem, Registry,
Security, and Networking. Read plainly, that asks for a Windows platform
volume comparable in depth to the MSYS runtime or toolchain volumes.

`charter/PROJECT-CHARTER.md` narrowed it. Under "Contextual scope" it states:

> Windows internals are documented to the depth necessary to explain
> observable MSYS2 behavior.

That narrowing was never recorded as a decision. `charter/adr/` contained
only a README and a template, and a 2026-08-02 audit found Volume 2 at one
page of 485 words with "NT Kernel" appearing once in the whole repository —
inside a pasted transcript. The audit could not distinguish "deliberately
narrowed" from "not done", because nothing said which it was.

This ADR is written after ADR 0002 and records a decision that predates both.
The numbering reflects subject order, not chronology.

## Decision

Windows platform coverage is **contextual scope**, as `PROJECT-CHARTER.md`
already states. Volume 2 documents the *boundary* — what MSYS2 requires from
each Windows subsystem, where this knowledge base's claims stop, and what
evidence an exact claim would need — and does not document Windows
implementation.

Concretely, for each of the charter's eight named subsystems, Volume 2
answers:

1. What does MSYS2 depend on from this subsystem?
2. Where does the boundary sit — what is a Windows fact rather than an MSYS2
   fact?
3. What evidence would be required to make an exact claim, and does this
   knowledge base hold it?

It does **not** answer how Windows implements any of them. Microsoft's own
documentation is the reference for that, and is cited where a boundary needs
a definition.

## Consequences

**Accepted:**

- Volume 2 is a boundary reference, not a Windows internals reference, and
  says so on every page.
- The eight named subsystems are each addressable, so a reader following the
  charter's scope list arrives somewhere rather than nowhere.
- Effort stays on the ecosystem this knowledge base is actually about.

**Costs:**

- Volume 2 will remain thinner than volumes covering MSYS2's own components,
  permanently and by design. A future reader comparing page counts will see
  an imbalance; this ADR is the explanation.
- Questions that genuinely require Windows internals — loader search order
  under specific conditions, filesystem behavior by volume type — cannot be
  answered from this knowledge base and are referred out.

**Revisit if:** an MSYS2 behavior cannot be explained without deeper Windows
detail, in which case that specific detail is in scope by the charter's own
wording ("to the depth necessary"). The narrowing is a default, not a
prohibition.

## Notes

The distinction this preserves matters more than the page count. An MSYS
process can present POSIX paths and mounts while executing on a Windows host;
a native PE program is not an MSYS program merely because it was installed by
pacman or launched from Git Bash. Volume 2's job is to keep those separable,
which is a boundary task rather than an internals task.
