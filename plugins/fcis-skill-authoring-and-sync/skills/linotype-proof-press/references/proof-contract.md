# Linotype Proof Press — acceptance and failure taxonomy

**Authority:** the author-approved source, admitted publication snapshot, actual existing Reader and immutable release identity. This document is a procedure; it introduces no rights, new compositor or publisher.

## Observations the machine can establish

- **Inventory:** exact published book/ordered work identities from the catalogue; actual folio total per work and viewport. All folios 1..N each observed once. A page can legitimately have a different number on another device.
- **Source continuity:** source-addressed fragments and ranges retained in order. A work may split a paragraph across leaves, but no admitted source text should disappear or duplicate. Where character ranges are exposed, independently require a continuous 0..source-length interval per source block; a missing tail, gap or overlap blocks the proof. For single un-ranged text blocks, verify exact text length. Figures and multi-fragment source nodes without offsets remain identity-only evidence and require an explicit separate image/ink check; do **not** call these character-perfect.
- **Composition geometry:** actual sheet, Satzspiegel, heading, text fragments, captions, original image boxes, baseline/line metrics, clipping and unexpected overflow. Measure inline SVG label ink independently from the enclosing `<img>` when source SVG is supplied.
- **Page relationships:** terminal headings without following passage, orphan/widow candidates, excessive open leaf before admissible prose, secondary figure pushing a sentence to its own leaf, facing verso/recto reference, broken image/caption adjacency, layout instability on orientation changes. An editorial exception may be correct.
- **Accessibility and language:** reading order, headings, alt text, text enlargement, focus/AX; browser selectors do not replace real assistive-technology acceptance.
- **Environmental identity:** browser engine/version, tested CSS viewport/DPR, loaded fonts, image digests, source revision, release identity, screenshot digest. An unpinned browser or missing image invalidates exact visual regression comparison.

## Nested composition evidence: inside versus outside

Proof text and illustration at **distinct semantic boundaries**, not as a single undifferentiated occupancy rectangle. Record (1) paragraph lineation/leading and exact source continuity; (2) each diagram label's visible ink relative to *its own intended inner frame*; (3) union of figure header, panels, annotations and key within the **outer plate**; (4) caption adjacency and the figure+caption group's separation from preceding and following prose; (5) group containment within the leaf's Satzspiegel and actual facing-page relation. Source text inside a deliberately failing **diagram specimen** is an exception for that marked negative panel only, never permission to render the outer plate outside its page or overlap the positive specimen.

A reader's request for additional breathing space is a request to clarify **external relationships among semantic units**, not a request to enlarge every line gap. Verify that the revised group spacing clarifies the ownership of ink and caption. Record machine widths/gaps to support, not replace, editorial judgment. Increase page count only when the measured readable composition requires it; report orphaned trailing prose and caption separation for review rather than scoring density automatically.

**Regression:** on *Before We Can Work Together*, reject “fixed” proofs that shift all lines apart or split semantic groups while leaving figure/caption boundaries ambiguous. Keep rejected screenshots as negative evidence, never as a passing baseline. Distinguish `PASS_MEASURED` for actual nonoverlap and `EDITORIAL_REVIEW_REQUIRED` for the author's qualitative finding of inappropriate internal/external rhythm.

## Classify defects

| State | Meaning | Release implication |
| --- | --- | --- |
| `BLOCKING` | Missing leaf, duplicate source, source overflow/clipping, broken essential image, wrong publication identity, incomplete scan | Reject acceptance |
| `EDITORIAL_REVIEW_REQUIRED` | One-line continuation, heading near foot, exceptional whitespace or a subjective image/prose relation | Must be reviewed or corrected; not automatically a defect |
| `ACCEPTED_EXCEPTION` | Author/editor approved this exact leaf/revision with justification | Retain approval evidence; do not apply to other revisions |
| `PASS_MEASURED` | All checks actually executed for a particular folio with zero blocking findings | Not an aesthetic or literary sign-off |
| `UNVERIFIED` | Unsupported platform, inaccessible source, absent native iPad witness or incomplete proof | Never upgrade to pass by inference |

## Scale and performance

Process the actual catalogue/work list; never count inert source templates as active books. Stream one record per physical folio to `pages.jsonl`; one lossless screenshot per page into a separate private tree; write resumable domain receipts and a machine-readable run summary. Batch by work/platform but account for the complete expected matrix at final acceptance. For long 1,000+ leaf runs, keep the process memory bounded by one Reader context and one page capture, avoid giant in-memory screenshots, and use the independent Python audit to catch gaps/duplicates. If interrupted, report incomplete; do not silently resume by accepting stale screenshots.

## The essay as the interpretive constraint

*What Makes a Page Modern?* states: source survives setting, measure declared, white space available, mark as evidence, position not identity, writer authorizes next composition. Therefore a low occupancy warning is a **question**, not an automatic order to make the page fuller. A source-authenticated full folio can be aesthetically poor and a nearly empty terminal page can be perfect. An authorial correction may change pagination, invalidating previous screenshots while preserving manuscript/source identity.

For proof illustrations, distinguish three kinds: (a) actual source-bound failed screenshot, labelled with release/folio; (b) independently accepted corrected screenshot; (c) original explanatory SVG schema, explicitly labelled as a diagram rather than a recorded failure. Never present a fabricated bad page as a verified product bug. The companion *Proof of the Page* may teach the reader with (c), but the proof ledger must cite (a)/(b) before claiming repairs.
