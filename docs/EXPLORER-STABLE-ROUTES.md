---
id: doc:volume-10:explorer-stable-routes
title: Explorer Stable Object Routes
volume: 10
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-07-28
---

# Explorer Stable Object Routes

`tools/build_explorer.py` builds `generated/explorer/index.html` from the
validated composed graph. Every object uses the canonical URL-safe hash route
`#/object/<percent-encoded-id>`. IDs are immutable model identities, so links
remain stable when an object's display name or metadata changes.

The initial explorer renders an object detail view with incoming and outgoing
relationships and retains a complete textual index in the HTML for accessible
fallback navigation.
