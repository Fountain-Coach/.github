# FCIS-VRT Standard (Visual Regression Testing)

**Status:** Adopted
**Category:** Standards Track
**Applies to:** Fountain Coach org repositories that publish or execute visual regression tests
**Version:** 1.0

---

## 1. Purpose

FCIS-VRT defines a single, org-wide standard for visual regression testing. It resolves the historical drift between prompt-bound GUI testing and protocol baseline testing by introducing two explicit modes under one umbrella standard.

This standard is compliance-critical. Legacy naming drift ("PB-VRT") is treated as non-compliant unless a documented legacy alias mapping is provided.

---

## 2. Terminology

- **FCIS-VRT**: The organization-wide Visual Regression Testing standard.
- **VRT-Render**: Prompt-bound visual regression for GUI rendering fidelity (formerly PB-VRT in FountainKit).
- **VRT-Protocol**: Protocol baseline regression using canonical message fixtures (formerly PB-VRT in midi2).
- **Legacy Alias**: An existing identifier (paths, endpoints, or storage keys) that must remain for compatibility but is formally mapped to FCIS-VRT.

---

## 3. Compliance Requirements

The key words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are to be interpreted as described in RFC 2119.

### FCIS-VRT-01: Mode Declaration
Repositories that implement visual regression **MUST** declare which FCIS-VRT mode(s) they support (VRT-Render, VRT-Protocol, or both), and where their baselines live.

### FCIS-VRT-02: Naming Discipline
New documentation **MUST** use FCIS-VRT naming. The legacy term "PB-VRT" **MUST NOT** be introduced in new docs.

### FCIS-VRT-03: Legacy Alias Mapping
If legacy identifiers remain, repos **MUST** document a mapping from legacy names to FCIS-VRT modes (see Section 5). Legacy aliases **MUST** be treated as temporary compatibility layers.

### FCIS-VRT-04: VRT-Render Requirements
VRT-Render implementations **MUST**:
- Bind each baseline to a prompt or deterministic test input.
- Store baselines in a documented, versioned location.
- Document how baselines are updated and reviewed.
- Declare whether execution is manual or CI-gated.

### FCIS-VRT-05: VRT-Protocol Requirements
VRT-Protocol implementations **MUST**:
- Store canonical baseline fixtures under a documented path (for example, `docs/vrt-protocol/`).
- Load fixtures in tests that fail on regression.
- Document coverage gaps and baseline completeness.

### FCIS-VRT-06: Gate Policy
The governance rule "Quiet Frame alignment test" **MUST** map to an explicit FCIS-VRT gate in repos that claim gating. If a repo is manual/opt-in, that status **MUST** be documented.

---

## 4. Repository Declaration Template

Add a short declaration in repo docs to make VRT status explicit:

```
FCIS-VRT:
  modes: [VRT-Render | VRT-Protocol]
  baselines: <path>
  gate: [manual | CI]
  legacy-aliases: <if any>
```

---

## 5. Legacy Alias Mapping (Org-Wide)

This mapping is the compatibility layer for historical naming drift. It is authoritative until the legacy identifiers are migrated.

| Legacy Identifier | FCIS-VRT Mode | Notes |
| --- | --- | --- |
| PB-VRT | VRT-Render (primary) | Historical name used in FountainKit for prompt-bound rendering tests. |
| pb-vrt (path/route) | VRT-Render | Legacy HTTP route for render testing services. |
| pbvrt-* (tools/scripts) | VRT-Render | Legacy tooling names; keep wrappers where required. |
| PB-VRT (midi2 docs/tests) | VRT-Protocol | Historical name for protocol baseline fixtures. |

---

## 6. Implementation Status

- **FountainKit**: VRT-Render (legacy pb-vrt service and tooling). Gate: manual/opt-in unless stated otherwise.
- **midi2**: VRT-Protocol baselines in docs, with JS tests loading fixtures. Gate: CI via test suite.
- **midi2-gpu-fabric**: VRT-Render snapshots for Stage Native. Gate: manual/opt-in.

---

**End of Standard**
