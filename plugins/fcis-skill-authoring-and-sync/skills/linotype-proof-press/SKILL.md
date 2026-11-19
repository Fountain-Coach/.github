---
name: linotype-proof-press
description: "Proofread every composed Fountain Press/Linotype folio across desktop, iPad portrait/landscape, and phone configurations. Use for exhaustive page-by-page print-quality acceptance, pagination, source-text completeness, white-space, orphan/widow, headings, captions, figure, font and page-break regressions, large books (1,000+ pages), page contact sheets, source-addressed defects, and before/after proof of changes. Requires code execution and authorized access to the existing Reader."
---

# Linotype Proof Press — exhaustive editorial proofing

Use the **existing** Fountain Press compositor and publication inventory. This is a read-only proofing instrument and an editorial acceptance procedure, **not** another Reader, publisher, CMS, PDF renderer, or source of manuscript authority.

## 1. Resolve the actual edition

Read the source owner's `PLANS.md`, published-catalogue snapshot, current immutable stage/public release, Reader module digest, font/assets and admission state. Read the existing `linotype-estate-template` Skill, especially `page-is-the-frame`, `model-essay-spread-proofreading-and-archive`, `semantic-illustration-ink-boundaries` and `reader-navigation-and-score-composition`. Apply the six authorial conditions from *What Makes a Page Modern?* as interpretation, not as unchangeable numeric thresholds.

## 2. Required execution host — Ubuntu Mac mini

**Writer decision, 16 November 2026:** For the current Fountain Press owner-WLAN staging estate, **all computational Proof Press execution happens on the enrolled Ubuntu Mac mini, hostname benedikt-Macmini.** The MacBook Pro may carry an SSH/remote command or source-control request, but it must **not** render page proofs, run the Playwright/WebKit matrix, capture screenshots, calculate the proof audit, or store the bulk proof evidence. Do not substitute the MacBook as a fallback. If Ubuntu is unreachable, report the proof blocked rather than silently moving execution.

Run the browser **on Ubuntu against the real owner-WLAN origin http://192.168.8.50:8200**, pin the active immutable release/source-lock and the canonical scanner/auditor SHA-256, and write append-only private evidence on Ubuntu under /home/benedikt/fountain-press-proof/runs/. Run bounded systemd --user proof jobs with CPU/memory ceilings separate from the existing staging service. A host guard must reject a non-Linux/non-benedikt-Macmini execution before launching any renderer. Physical iPad Safari remains a distinct acceptance gate; Linux WebKit emulation cannot replace the physical-device witness. **Origin parity is mandatory:** Do not substitute loopback 127.0.0.1 or localhost for the browser URL. The already-adopted Reader enables published audio players at trusted loopback origins and hides that playback path on ordinary HTTP WLAN. A real Ubuntu 16 November WebKit witness proved that the loopback audio path stalled *The Door Is a Score* at its second page, whereas the identical source and Ubuntu browser rendered all 50 pages across four layouts against the WLAN origin. This is an origin-semantic defect in the proof setup, not permission to change book content.

A real 16 November host relocation established native Ubuntu WebKit 27.2 with Node 22 and the existing source-pinned scanner. A first Ubuntu-local work captured 8/8 portrait folios; a separate Ubuntu process proved 63/63 folios for *If Only* across all four layouts. A monolithic cross-work WebKit process closed after finishing the first work, so the currently deployed Ubuntu runner uses **one isolated browser process per admitted work**, with each process measuring all four viewports, at most one retry for a failed work, and a final independently verified **66 works × 4 layouts** inventory. Isolated work success is **scoped**, not full-book acceptance. Source-addressed screenshots are hardlinked (not recopied) into the final audited inventory and stay on Ubuntu. Source digests, original failed attempts and the host identity remain in evidence.

For the exact current private host the bounded WLAN-origin entrypoint is /home/benedikt/fountain-press-proof/bin/run-isolated-catalogue-wlan-on-ubuntu.sh. It explicitly checks hostname, the live v219 source-lock and scanner/auditor source hashes before each work. A separately approved host/release would require an explicit revision of this host rule, not an automatic workstation fallback.

## 3. Run the actual Proof Press

Use the **source-owned** `Fountain-Coach/fountain.coach/scenarios/press-books/proof-press/run.mjs`, not a duplicate script here. It enumerates work IDs from the admitted `books/catalog.json`, enters each current Reader work, determines the actual composed folio count for each platform, visits **every folio**, renders one exact sheet screenshot, and writes source-addressed measurements and defects to append-only `pages.jsonl`, plus `run.json`. Example executed inside the designated Ubuntu proof host:

`PLAYWRIGHT_MODULE=<Ubuntu-playwright-core> <Ubuntu-node-22> scenarios/press-books/proof-press/run.mjs --origin http://192.168.8.50:8200 --out /home/benedikt/fountain-press-proof/runs/<unique-id>`

Default = all admitted active works × iPad portrait/landscape × desktop × phone. Work/platform filters and `--limit` are for **diagnosis only**, never publication-wide acceptance. Do not silently sample a 1,000-page book. Capture real WebKit composition; report platform/browser version and fonts. Confirm physical iPad Safari/VoiceOver independently; emulated viewports are not a physical-device proof.

Run this Skill's `scripts/audit_proof.py <proof-directory> --require-complete --write` to verify the coverage matrix, exact folio numbers, screenshot digests, source-block addresses, page errors and all unresolved findings. This is a **second** tool reading the produced proof—not the renderer certifying itself. The machine audit writes a report and HTML proof-gallery outside public Git. Read [proof contract](references/proof-contract.md) before deciding whether a finding blocks release.

## 4. Judge pages rather than filling rectangles

Every leaf must account for its source, text measure, margins, original artwork/captions, typographic units and position in the facing-page relationship. Detect omitted/duplicated source ranges, content outside the Satzspiegel, clipped glyphs/captions, missing fonts/images, unbound headings, widows/orphans, breaks introduced by an inline figure, image/text misalignment and unexplained blank leaves. White space is **not** a defect by itself: distinguish deliberate margin, end-leaf, title/opening and revision space from a compositor refusing an otherwise admissible next passage. Never impose a universal minimum occupancy or arbitrarily shrink artwork to make a numerical pass.

Where geometry, pixels or heuristics cannot decide, record **EDITORIAL_REVIEW_REQUIRED** with the work/source address, folio/platform and screenshot. A word-spacing or lineation adjustment may fix a sheet but must not rewrite the author's text or alter a source address. An approved exception must cite the writer's specific decision and edition; the machine cannot self-approve visual beauty or claim full literary proofreading.

## 4a. Inside/outside proof: grouping before whitespace

**Required for a request such as “more air,” “too dense,” or “the illustration is cramped.”** Start by identifying the exact *semantic* containers on the affected leaf: continuous prose paragraph, line/specimen frame, complete figure (including title, panel labels and any legend), attached caption, following prose, and the outer folio's Satzspiegel. Measure each layer independently. Read `linotype-estate-template/references/page-is-the-frame.md` and `linotype-semantic-data-plates.md` for the governing relationship.

- **Inner coherence:** paragraph leading and lineation should support a single thought; do not spread lines apart, insert extra paragraphs, or change author text as a shortcut to white space. A diagram's own labels and specimens need measured internal insets; a deliberate *negative specimen* may overrun its **illustrated internal frame** only, never the adjacent panel, figure, caption or page.
- **External relationship:** distinguish paragraph-to-figure separation, plate-to-caption attachment and caption-to-next-paragraph separation. Preserve the figure+caption as one unit. An attached caption must not visually drift nearer to unrelated prose than to its own figure; consider an intentional figure break before reducing readable type.
- **Print proof reality:** check the actual ink and measure at intended physical print size, including verso/recto when present. Compare the original and corrected full folios, not just crops; avoid numeric page-fill targets, blanket line-spacing increases or “we gained one more page” as success evidence.

**Negative regression case:** the author rejected two versions of *Before We Can Work Together*: a dense pre-web plate, then a global-spacing revision that made the reading more fragmented while leaving the figure's inner/outer grouping concept unresolved. A future proof that solves this only by extra leading, scattered caption/notes, isolated paragraphs or unnecessary leaves requires `EDITORIAL_REVIEW_REQUIRED` and must not be reported as “airier” or “accepted”. A geometry-only scanner may record measured group distances; only the editor accepts rhythm and modernity.

## 5. Acceptance and provenance

Separate four gates: (a) exact admitted source and complete work inventory; (b) machine folio coverage/structural geometry, with no blocking defects; (c) every indicated exception editorially approved or corrected with a before/after proof; (d) independently observed running-stage and physical-device result. Keep landscape spread relationships and portrait independent. Pin source Git, release, browser/font identity, viewport, screenshots, SHA-256 and source-addressed findings. Store private book page captures only in the private evidence volume; never push them to public Git or use them as social artwork.

The machine's `INVENTORY_COMPLETE_REVIEW_REQUIRED` is **not** `PRINT_QUALITY_ACCEPTED`. A scanned screenshot alone cannot certify ink balance, substantive prose, rights or accessibility; a unit test cannot certify physical iPad. If 1 of 1,000 leaves is unvisited or unreviewed, report the exact unfinished part, never "all done". A published print-quality claim requires editorial proof on every applicable leaf plus separately authorized EstatePublisher release receipts; this Skill does not grant publication permission.

**Source owner's tested model:** *What Makes a Page Modern?* v151/v216 and the documented *Client-Centered* v177→v178 isolated-sentence repair. They teach **procedure**, not universal page counts, fixed pixel coordinates or target fill percentages. The companion illustrated essay *The Proof of the Page* is editorial explanation, not a normative validator.
