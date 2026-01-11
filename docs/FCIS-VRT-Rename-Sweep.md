# FCIS-VRT Rename Sweep — Org Schedule

**Status:** Proposed  
**Owner:** FCIS compliance + repo maintainers  
**Goal:** Replace legacy "PB-VRT" naming with FCIS-VRT modes (VRT-Render, VRT-Protocol) while preserving compatibility.

---

## Scope

Repositories and surfaces currently using PB-VRT or its aliases:
- **FountainKit** (VRT-Render): `pb-vrt` HTTP paths, PBVRT* symbols, `pbvrt-*` tooling, artifacts under `.fountain/artifacts/pb-vrt/`.
- **midi2** (VRT-Protocol): fixture docs and JS tests (mostly renamed).
- **midi2-gpu-fabric** (VRT-Render): Stage Native snapshot tests (already aligned).
- **composer-studio** (VRT-Render legacy references in AGENTS/fixtures).
- **Org docs/sites**: `.github/docs/*`, `style-src/`, `org-site/`.

---

## Non-Negotiables

- **Compatibility first:** Legacy aliases remain supported during the sweep (PB-VRT, `pb-vrt` routes, `pbvrt-*` tooling).
- **No IDL changes:** The MIDI backplane IDL remains the sole contract.
- **FCIS naming only in new docs:** New documentation must use FCIS-VRT terms.
- **Explicit repo declaration:** Each repo declares its VRT mode, baseline location, and gate policy.

---

## Phased Schedule

### Phase 0 — Inventory + Mapping (Week 0–1)
- Complete org-wide `rg` audit and classify references as VRT-Render or VRT-Protocol.
- Update mapping table in `docs/FCIS-VRT-Standard.md` if new aliases are found.
- Deliverable: inventory log + updated mapping table.

### Phase 1 — Docs + Policy Alignment (Week 1–2)
- Update org docs and websites to FCIS-VRT naming.
- Ensure AGENTS/PLANS references use FCIS-VRT terminology only.
- Deliverable: org docs/site clean of PB-VRT except legacy alias notes.

### Phase 2 — VRT-Render Code Rename (Week 2–4)
- FountainKit: rename PBVRT symbols and tooling to FCIS-VRT Render equivalents.
- Keep a compatibility layer: legacy paths/env vars/aliases remain supported.
- Update tests and scripts to prefer new names.
- Deliverable: dual-name compatibility with FCIS-VRT Render as primary.

### Phase 3 — VRT-Protocol Completion (Week 3–4)
- midi2: ensure all docs, fixtures, and CI references are VRT-Protocol.
- Verify required checks and baseline fixtures align with the new names.
- Deliverable: no PB-VRT references in midi2.

### Phase 4 — CI/Gate Normalization (Week 4–5)
- Align required check names and gating docs to FCIS-VRT modes.
- Make "Quiet Frame alignment test" references explicit per repo.
- Deliverable: consistent gate naming across repos.

### Phase 5 — Deprecation Window (2 releases)
- Keep legacy aliases in place with deprecation notes.
- Track removal target dates per repo; only remove after two stable releases.
- Deliverable: removal plan per repo (tracked in release notes).

---

## Acceptance Criteria

- No new PB-VRT references in docs or code.
- Each repo declares VRT mode(s), baseline path, and gate policy.
- Legacy aliases are documented and functional where required.
- CI and status checks use FCIS-VRT naming.

---

## Open Questions

- Do we preserve `pb-vrt` HTTP routes indefinitely or introduce a new canonical `vrt-render` path?
- Should artifacts remain under `.fountain/artifacts/pb-vrt/` or migrate with shims?
- Are there third-party integrations that require a longer alias window?

