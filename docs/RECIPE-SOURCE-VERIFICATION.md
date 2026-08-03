---
id: doc:volume-12:recipe-source-verification
title: Recipe Source Verification
volume: 12
status: partial
model_refs: []
evidence_refs: []
last_verified: 2026-08-02
---

# Recipe Source Verification

`tools/verify_recipe_sources.py` reads `recipes.jsonl` from the static deep
inventory collector, downloads only explicitly declared HTTP(S) `source`
entries, and compares each payload with its positionally aligned `sha256sums`
value. It never sources a PKGBUILD, executes a package script, or extracts the
downloaded payload.

```powershell
py -3 tools/verify_recipe_sources.py work\inventory\recipes.jsonl `
    --output work\recipe-source-verification
```

Each record retains the recipe path, declared source, requested URL,
expected and actual hashes, payload size, retrieval time, and outcome.
`SKIP`, missing checksums, unsupported checksum formats, download failures, and
mismatches remain explicit rather than being treated as verified. Downloads
are bounded to one GiB per source and carry no credentials or ambient package
manager state.
