# LINOTYPE-FOLIO-01 — compose the argument, its figure and the next argument

**Source-owned lesson, 20 November 2026.** Apply to source-anchored illustrated Fountain Press works where a figure changes the page break or leaves an unusually large empty field. This is a reusable **agent procedure**, not a newly deployed compositor, metadata schema, FCIS instrument, publishing permission or automatic aesthetic judgment.

## The relationship that page geometry cannot tell us

Resolve three **distinct source units** before placing the illustration:

- **Argument / source passage** — the passage whose proposition the image explains. Its existing source address and original text remain authoritative.
- **Figure with its caption** — one inseparable source-anchored explanatory unit. Treat the title, ink/data, legend and caption as the *inside* of that unit.
- **Subsequent argument** — the next source passage, whose rhetorical role may be continuation, example, contrast or a new section. Its relationship to the figure is not an automatic demand to share the same leaf.

**Example — *Before We Can Work Together*.** The learning-cycle paragraph at `before-we-can-work-together.p07` is **illustrated by** Figure II (`before-we-can-work-together.plate-02`). The paragraph beginning “A concrete example comes from Fountain Press” (`before-we-can-work-together.p08`) **introduces the following example**. The illustration closes the preceding argument; p08 does not belong inside the Figure II group. These source addresses and roles are the evidence for this example, not universal positions or names.

Do not infer relationships merely from HTML siblings, pixel distances or a caption's wording. Inspect the admitted source paragraph anchor and author-declared figure/section semantics. If the intended relationship is ambiguous, preserve source order and classify the relation as **EDITORIAL_REVIEW_REQUIRED** rather than inventing an `illustrates` edge or moving artwork. Document the relationship in the existing source/composition record; do not invent a second CMS or mandatory data schema.

## Linotype's semantic composition decision

1. **Bind meaning before page breaking.** Identify the argument, figure+caption, following argument and any heading/footnote. Record `illustrates`, `continues`, `introduces-example` or the actually supported role using existing source addresses. An ordinal placement is not itself a semantic relation.
2. **Maintain the nesting contract.** Keep figure ink, title, legend and caption together, preserve exact source anchors/alt/rights and keep text measures readable. Maintain genuine widow/orphan constraints and source text order. An argument may span leaves where ordinary prose splitting is lawful; a figure may not precede its authored source anchor.
3. **Allow a figure to end a folio.** If the whole source-bound figure+caption fits after its anchoring prose at the current readable type size, it may close the leaf. Do **not** evict it just to reserve space for the following unrelated paragraph. Begin the next argument on a new leaf when needed; no one-line prose stub is required beneath a figure.
4. **When it does not fit, keep the semantic unit intact.** Move the figure+caption to the next admissible leaf. A spacious prior leaf can be legitimate: do not shorten source text, reduce ink/type, invent filler, violate the anchor, or impose a universal minimum fill percentage.
5. **Choose break candidates by relations, then measure.** Prefer a break between the completed figure+caption and the following independent argument when it preserves meaning and avoids gratuitous underfill. Check the same source on portrait and facing leaves, small screens, large text and theme changes. Do not hard-code the Figure II IDs, historical free-space measurements, special paragraph text or one viewport's pixel threshold as a general semantic rule.

## What counts as independent proof

- Record the **before** source/release, folio and last admissible source unit, measured usable area, available space and the actual reason a figure was rejected. Distinguish a genuine non-splittable image from an artificial following-prose reserve or a CSS-layout error.
- Prove the **after** layout through the existing Reader and source-owned Proof Press: argument/figure/caption order, complete image and legible caption on the intended leaf, next argument at its stable original address, all source characters exactly once, no visual overflow or single-line orphan, and no clipping under enlarged text or theme changes. Measure whitespace as evidence of the change, **not** as a quota governing all books.
- Recompose and inspect the actual iPad portrait leaf and eligible landscape spread; verify other affected viewports, original figure SHA and staged route/source parity. A WebKit viewport screenshot is **not** physical-iPad editorial approval.
- Separate the **observed one-essay repair** from a **generalized runtime capability**. The private v228 WebKit proof placed Figure II on folio 3 with 73/976 px trailing space, versus the earlier approximately 607 px gap; the preceding iPad Safari screenshot at 06:32 still displayed the older six-folio edition. This supports the design lesson but **does not establish** that every semantic relationship is implemented by the runtime, nor that the revised folio was approved on the physical iPad.

**Refusal cases:** figure before its source anchor; figure/caption split; unrelated prose forced onto the same leaf as a condition for placing a complete figure; excessive whitespace accepted solely because tests are geometrically green when a valid semantic break exists; arbitrary occupancy targets or source rewriting presented as semantic understanding; new published runtime/Skill authority inferred from this reference.

Keep [the page frame hierarchy](page-is-the-frame.md), [semantic data plates](linotype-semantic-data-plates.md) and the existing source-bound [illustration contract](illustration-and-social-card.md) binding. Use the existing `linotype-proof-press` for proof evidence and the existing EstatePublisher pathway for separately authorized staging/release.
