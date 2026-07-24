# FCIS-AX Standard (Accessibility)

**Status:** Adopted
**Category:** Standards Track
**Applies to:** Fountain Coach org repositories that ship, render, or drive a user-facing interface (native or web)
**Version:** 1.0

---

## 1. Purpose

FCIS-AX defines a single, org-wide standard for **accessibility** as the machine-readable semantic layer of every user interface.

Accessibility is not treated here only as an assistive-technology feature for humans (though it is that, and that alone would suffice to require it). In the Fountain Coach architecture it is **load-bearing infrastructure** for three parties at once:

1. **The human** — perceives and operates the interface, including with assistive technology (VoiceOver, Switch Control, Voice Control, screen readers).
2. **The agent** — a conversational copilot may only speak truthfully about a surface it can *introspect*. The accessibility tree is that surface. A copilot that claims "64 beats" must be claiming about elements that exist, and are queryable, in the accessibility tree.
3. **The verifier** — automated UI testing and AI-driven verification resolve elements through the accessibility tree (roles, labels, values, actions), not through pixels. On Apple platforms this is literal: XCUITest and UI automation drive the accessibility tree; assistive technology reads the same tree. An interface with no accessibility is opaque to automation and cannot be honestly verified except by eyeballing pixels.

A view that paints pixels but exposes nothing to the accessibility tree is therefore **not finished**, regardless of how it looks. It is unusable to a human with assistive technology, unspeakable-about by an agent, and unverifiable by a driver.

This standard is compliance-critical.

---

## 2. Terminology

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as described in RFC 2119.

- **Accessibility tree (AX tree):** The platform's semantic representation of the interface — the structure assistive technology and UI automation traverse.
- **Accessible element:** A node in the AX tree carrying, at minimum, a **role**; where it names something, a **label**; where it holds or changes state, a **value**; and where it can be operated, the **actions** that operate it.
- **Custom-drawn view:** Any view whose content is produced by drawing code rather than standard platform controls — CALayer/Core Animation layers, Core Graphics/`draw(_:)`, `Canvas`, sprite/scene graphs, WebGL/canvas on web. These expose **nothing** to the AX tree by default.
- **Pixel parity failure:** A state that is visible in the rendered pixels but absent from (or contradicted by) the AX tree.
- **AX-driven verification:** Asserting the presence, count, and state of interface content by querying the AX tree, as opposed to reading it off a screenshot or clicking measured pixel coordinates.

---

## 3. Compliance Requirements

### FCIS-AX-01: Every view exposes its content
Every user-facing view **MUST** expose its meaningful content through the platform accessibility API — standard controls and custom-drawn views alike. "Meaningful content" is anything the interface communicates to or accepts from the user: labels, values, structure, counts, status, and every operable affordance.

### FCIS-AX-02: Custom-drawn views MUST be made accessible
A custom-drawn view **MUST** implement platform accessibility for each meaningful element it paints. Each such element **MUST** carry a role and a label; a **value** where it holds or changes state; and the **actions** that change that state where it is operable. Painting alone does not satisfy this requirement. (Implementation is platform-specific — e.g. `NSAccessibility`/`accessibilityElements`/`NSAccessibilityElement` on macOS, `UIAccessibilityElement`/`accessibilityElements` on iOS, ARIA roles/attributes on web — and belongs in a repo's Skills layer, not here.)

### FCIS-AX-03: Pixel parity
The AX tree **MUST** present the same structure and state the pixels present. If the surface shows N items, N items **MUST** be queryable in the AX tree; if an item is in a state (selected, kept, cut, running), that state **MUST** be reflected on its accessible element. A pixel parity failure is a defect of the same severity as a wrong render.

### FCIS-AX-04: Agent honesty is bounded by the AX tree
An agent, copilot, or other automated conversational surface **MUST NOT** claim, offer, report, or act upon interface state that is not present as an accessible element on the surface it refers to. The accessibility tree is the shared truth between the human, the agent, and the verifier. (This is the mechanical enforcement of the "situated" agent principle: an agent may not offer what the arrangement does not show.)

### FCIS-AX-05: Verification is AX-driven, not pixel-driven
GUI behaviour **MUST** be driven and verified through the accessibility tree — query by role/label/identifier, read value, invoke action. The presence, count, and state of content **MUST NOT** be asserted from screenshot-only inspection, and interaction **MUST NOT** depend on measured pixel coordinates where an accessible element exists to target. Visual checks (see FCIS-VRT) remain **complementary**: FCIS-VRT proves the pixels look right; FCIS-AX proves the content is there, correct, and operable. Neither substitutes for the other.

### FCIS-AX-06: Stable targeting identifiers
Interactive and stateful accessible elements **SHOULD** carry a stable accessibility identifier (e.g. `accessibilityIdentifier`, `data-testid`/`aria-*` on web) so that AX-driven tests and drivers can target them without depending on localized labels.

### FCIS-AX-07: Definition of done
A UI change is **not complete** until (a) its content is exposed to the accessibility tree per FCIS-AX-01–03, and (b) it is covered by at least one AX-driven check per FCIS-AX-05. "It renders" is not "it is done."

---

## 4. Repository Declaration Template

Repositories that ship or drive a UI **MUST** add a short declaration to their docs making AX status explicit:

```
FCIS-AX Declaration
- Surfaces: <list of user-facing views/screens covered>
- Custom-drawn views: <list, each MUST be accessible per FCIS-AX-02>
- AX identifiers: <where stable identifiers are defined>
- AX-driven verification: <where the AX tests/drivers live; manual or CI-gated>
- Known gaps: <any surface not yet compliant, with a tracking reference>
```

---

## 5. Relationship to other FCIS standards

- **FCIS-VRT (Visual Regression Testing):** VRT governs *visual fidelity* (does it look right); FCIS-AX governs *semantic truth and operability* (is the content there, correct, stateful, and operable, and can it be introspected). A surface is fully verified only under both. Reading state off a VRT screenshot to stand in for AX assertion is a FCIS-AX-05 violation.
- **FCIS RFC 0001 (repo layering):** This standard is declarative. Platform-specific *how-to* (the accessibility APIs, the driver harness, the test patterns) belongs in each repo's `.codex/skills/*` runbooks, not in AGENTS.md and not here.

---

## 6. Rationale (non-normative)

The rule was adopted after a concrete failure: an AI agent verifying a native app could only click measured pixel coordinates and read screenshots, because the app's core visual surfaces were custom CALayer-drawn views that exposed nothing to accessibility. The agent reported content ("beats") that a human could not see on screen, and had no accessible way to detect the discrepancy — the exact class of dishonest, unverifiable interface this standard exists to prohibit. Accessibility is how software becomes introspectable; introspectability is the precondition for both human trust and automated verification. Apple's own platform makes this the same tree for assistive technology and for UI automation, which is why "make it accessible" and "make it verifiable by an agent" are one requirement, not two.
