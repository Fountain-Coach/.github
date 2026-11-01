# Reader navigation and Teatro Score composition — Fountain Press

**Status: writer-accepted interactive organigram (design rule), not live-reader acceptance.** Apply when the requested work concerns a reader opening, Bookshelf, collection contents, chapter navigation, Teatro Score, responsive illustration, or mixed-media folio. Pair with [page-is-the-frame.md](page-is-the-frame.md), current Fountain Press source and the applicable FCIS/authoring authority. Do not turn this reference into a new renderer, page identity, unpublished book, or publication right.

## 1. One book, four movement geometries

Keep the entire experience inside **one persistent reader frame**. Its branches have different movement rules; do not flatten them into web link lists, nested apps, or decorative card grids.

| Surface | Navigation | What stays fixed |
| --- | --- | --- |
| **On Continuity editorial** | Authored, **paginated** opening; advancing enters Bookshelf | Reader bottom bar |
| **Bookshelf** | **Horizontal** left/right scroll or swipe between only admitted books; keep it typographic | Reader bottom bar |
| **Collection contents** | **Vertical** continuously scrollable index, even when work pages are paginated; no page numbers or hyperlink underlines | Reader bottom bar, heading and reader frame |
| **Work (essay/reading)** | **Paginated** source-bound leaves; advance across authored work/chapter boundaries | Reader bottom bar |

Preserve the semantic path **On Continuity → Bookshelf (complete collection contents facing its gallery) → work**; legacy standalone contents routes are optional deep links, never an obligatory extra step. A collection may have its own authoritative title and source membership; do not invent empty titles, new collections or numbered readings to fill a layout.

Make each navigation action reversible, with clear Back/Breadcrumb semantics. Save *separate* horizontal Bookshelf position, vertical contents scroll position, selected work and source-based reading position. Returning restores the previous branch and its position. On viewport change, preserve semantic source and recompute geometry rather than use old page numbers.

Allow a long collection contents list to scroll inside its **bounded page area**. Keep bottom controls outside that scroll container, fixed and reachable at every position; do **not** allow list scrolling to move the reader footer. Use stable accessible names, focus order, keyboard arrows/Tab/Enter, touch swipe and appropriate wheel handling. A visual index entry may be clickable without looking like a blue underlined hyperlink; **retain visible keyboard focus** and true semantics.


### Bookshelf collection-gallery alternation

For every **admitted collection**, arrange a horizontally scrollable sequence of **collection editorial text → its square-thumbnail gallery**, then the next collection's text → gallery. This is the existing Bookshelf's left/right movement, not a vertical web landing, a card mosaic or another app. The gallery **itself scrolls vertically** in its bounded page region; the Bookshelf's horizontal position and each gallery's vertical position are independent, preserved when entering a work and returning. The fixed bottom reader navigation never participates in either scroll.

- The **text surface is the complete scrolling table of contents** — show a typographic collection title and a brief source-grounded ordering line, followed immediately by **every admitted source-ordered entry** in its own bounded vertical scroll area. Never replace the visible list with a collection description or a redundant **"Read Essays"** button that requires another click to see the contents. A short collection heading does not stand in for the list.
- Derive the gallery **one item per admitted published text**, in the collection's source order. Each item carries source work ID, accessible text title and original image address/provenance; do not synthesize or misattribute artwork. For works with multiple images, choose their first authenticated narrative image, retaining every original figure in the work itself.
- Render each thumbnail inside an **equal square frame (1:1)** with `object-fit: contain` / equivalent proportional fitting and calm unpainted margins. **Square is the gallery presentation cell, not an instruction to crop or deform the original illustration.** Deliberate light/dark image rendering still applies; transparency or auto-inversion is not a dark artwork.
- Selecting a **contents title or thumbnail** opens that exact work **within the same reader**, with the parent control returning **directly to the facing Bookshelf**, retaining the horizontal shelf and independent vertical contents/gallery positions. A separately addressable collection contents route may remain for old links, but never becomes an obligatory intermediate page from this Bookshelf.
- Keep **both contents and gallery** scrollable **top-down**, each with its own independently remembered position, keyboard, touch and pointer interaction and reliable focus; wheel/touch inside either must not accidentally advance the horizontal shelf. Keep heading, reader chrome, and footer fixed while the index or art items move.

**Acceptance:** independently count and compare the complete visible table of contents with admitted source membership (including introductory pieces that have no gallery image); require **no extra collection-opening click**, direct work selection and return to the facing Bookshelf, distinct restored index/gallery offsets, then count source work IDs and thumbnails in each collection; require *exactly one* image per admitted text, no broken/missing assets or substitute covers, source-ordered titles, 1:1 cell boxes with whole-image fitting, accessible names/focus, bounded vertical gallery motion, horizontal alternation, fixed footer, and restored scroll offsets after navigating to an image's work and back. Verify landscape spread, portrait, narrow phone, light/dark presentation; do not infer physical iPad/VoiceOver acceptance from desktop WebKit.

## 2. Proof before changing the page

Identify the source-authorized **On Continuity editorial** and capture **that actual opening spread** at the selected revision, route, theme and viewport. Never substitute an essay, another book, a generated impression or a convenient screenshot. Label exploratory organigrams as **design prototypes**; they prove the author-approved interaction model, not live staging behavior.

For each navigation mode, verify:
- Editorial first spread shows actual On Continuity text, not an essay or an empty title leaf.
- Page advance enters the Bookshelf; Bookshelf moves **horizontally** without shifting the whole reader.
- Opening a collection shows its **complete** contents ordered from the admitted source, vertically scrollable with **no page numbers**.
- Contents scrolls while bottom reader navigation stays fixed; position survives entering a work and returning.
- A work opens in the same reader, has intact text and associated media, turns pages and returns to the same branch.
- Accessibility tree exposes the correct landmarks, roles, labels, scroll containers and focus; screenshot witnesses readable geometry in landscape, portrait and narrow phone, plus enlarged text.
- No source paragraph, figure or media object is dropped, repeated, clipped or attributed to the wrong work. Treat source/DOM, AX and settled pixels as separate proof authorities.

A successful organigram cannot upgrade an untested physical iPad/Safari/VoiceOver reader to accepted. Record each authority separately.

## 3. Largest Balanced Fit — Teatro Score

A **Teatro Score is a narrative reference**, not a thumbnail, logo or detached hypertext destination. Compose its *complete* image **at the largest balanced size within one folio** so the reader can see what the following prose describes.

- Obtain the source-owned Score, its intended aspect ratio, resolution, alt text and associated source passage. Do not crop, auto-invert, replace with stock imagery or invent a second rendition.
- Measure the available folio content rectangle **after** safe areas, typographic margins, fixed reader chrome and any caption/necessary prose allowance. For source dimensions `(w,h)` and available figure bounds `(W,H)`, choose `scale = min(W/w, H/h)` and place at `(scale*w, scale*h)`. Allow upscaling only while source quality remains legible. **Recompute for each aspect ratio**, not a single desktop percentage.
- Maximize **legible displayed area**, not an arbitrary thumbnail width. Balance figure and prose: keep a meaningful opening passage on the same page when it remains readable; otherwise grant the Score its own dominant folio and begin its interpretation on the immediately following folio. Do not break the narrative reference by inserting unrelated controls, large gutters or an intervening gallery.
- A wide landscape Score, a portrait Score and a square Score all use their **own intrinsic aspect ratio**. Do not stretch, crop or shrink a Score to match a decorative grid. No overlay or caption may hide the source.
- The author-approved **light and dark artwork** must each have a deliberate palette/rendition when required; transparent pixels alone are **not** responsive dark-mode artwork. A missing dark variant is an open editorial issue, not a reason to apply automatic inversion and call it accepted.
- Preserve source digest and ordering so that repagination still binds the Score to the passage it anchors; the page index is not source identity.

**Acceptance:** At a minimum inspect square, wide and tall Score fixtures in landscape spread, portrait single-leaf and narrow phone formats. For each measure image vs allowed bounds, whole-image visibility, legibility, safe margins, caption/prose relationship, page transitions and accessible names. Verify no thumbnail-like suppression. Retain an actual source-owned Score screenshot and the matching textual witness; do not use generic substitute imagery.

## 4. Mixed media remains on the page

When the authored work includes audiovisual material, use the **existing SatzfunkPlayer** as Fountain Press's AV representation at its source-bound location. Do **not** replace the experience with “open elsewhere”, an external player page, a fake button or a second player engine. Preserve transport, source identity, track/time binding, release rights and secure origin requirements. A link can cite an external source, but it cannot substitute for authored playback. Distinguish operational media evidence from an illustration.

## 5. Minimum final evidence

Report **(a)** writer-accepted model/spec, **(b)** source code/revision and authored work identity, **(c)** measured reader tests, **(d)** browser accessibility and visual proof, and **(e)** stage/public deployment readback *only when actually performed*. If only the interactive organigram has been accepted, say **design accepted; live behavior unverified**. Do not introduce a new runtime capability, Skill, landing service, public release, or test instrument merely to restate this design.
