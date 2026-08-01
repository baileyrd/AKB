# Vendored dependencies

## d3.v7.min.js

- Source: `https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js`
- Version: 7.9.0
- Retrieved: 2026-07-31
- SHA-256: `f2094bbf6141b359722c4fe454eb6c4b0f0e42cc10cc7af921fc158fceb86539`
- License: ISC (https://github.com/d3/d3/blob/main/LICENSE)

Vendored (not CDN-loaded) so the generated explorer stays fully
self-contained and works offline, matching every other generated
artifact in this repository. `tools/build_explorer.py` copies this file
into `generated/explorer/d3.v7.min.js` on every build; do not edit the
generated copy directly.
