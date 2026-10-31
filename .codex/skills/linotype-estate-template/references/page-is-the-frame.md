# The page is the frame — modern Linotype reader contract

Use this reference for reader, folio, source-linked listening, semantic illustration, and responsive page-composition work. Keep it subordinate to current source owners, FCIS/Governance, Fountain Press and publication authority.

## 1. Start from the reader's present task

Keep the work primary. Ask what the reader needs **now** to read, hear, navigate, return, or understand the source. Put only that on the primary surface.

Treat **over-edited** as a concrete failure mode: individually reasonable labels, controls, diagrams, status chips, architecture maps, production explanations, covers, modes, and provenance can accumulate until the interface explains itself instead of presenting the work. Remove or demote an element when the reader must understand the interface before understanding the source.

Use this smell test for every visible element:

1. Which current reader action or comprehension need does this serve?
2. Does it remove mental work, or create another concept to decode?
3. Can it live in a secondary disclosure, provenance page, authoring surface, or repository instead?
4. Would the work remain clear if this element disappeared?

Prefer subtraction when the answer is unclear. **Complexity stays in the system; do not make it the reader's burden.**

## 2. Compose pages instead of scaling content

Treat the available reading area as a measured frame.

- Keep typography at its readable authored/accessibility size. Never shrink type merely to fit one screen.
- Add physical leaves when content needs more room. Do not make the default paginated leaf vertically scroll to absorb overflow.
- Use actual geometry, not browser names. Portrait normally presents one leaf. Landscape may present two only when each leaf remains readable at the current type size and safe area.
- Preserve margins and hierarchy as layout semantics, not decorative paper simulation. Modern CSS, React/Vite and responsive controls are compatible with Linotype; faux-book skeuomorphism is not required.
- Let 200% text enlargement, WCAG text-spacing overrides and larger system type **repaginate**. Do not clip, overlap, hide, or reduce type to preserve a page count.
- Keep an explicit continuous-reading alternative when it materially helps accessibility or source inspection. Do not use that alternative to excuse broken pagination.

The page count is a projection of source + viewport + typography. Never make it the durable identity of the text.

## 3. Preserve semantic position across reflow

Address the source by stable work/revision/passage identity and source offset where applicable.

- Preserve the addressed passage across page turns, rotation, resize, theme change and repagination.
- Resolve a copied passage link to the source location, then compose the page for the receiving device. Do not copy a transient page number as the semantic address.
- When a viewport changes, keep the reader near the same source position rather than the same obsolete leaf index.
- Refuse unknown/stale source addresses visibly. Do not silently substitute a nearby passage and call it restored.

## 4. Make semantic illustration earn its place

Do not default to illustration merely because a concept is abstract or because Linotype has a visual surface.

Use an illustration when it reduces text, exposes a spatial/temporal relation, or makes a definition immediately easier to grasp. Keep it source-bound and accessible.

Remove, simplify, or demote an illustration when it:

- repeats prose without reducing effort;
- requires a second explanation to understand;
- turns a concrete application into a conceptual art object;
- becomes visual decoration around an already understandable passage;
- misrepresents an executable/runtime object as a static metaphor.

A semantic illustration succeeds when the reader understands **more with less explanation**.

## 5. Treat listening as a property of the source

When a passage can be heard, keep listening inside the reading relationship.

- Offer a small deliberate Play/Pause action near the relevant work or passage; never autoplay.
- Keep the audio session stable while the page recomposes. Rotation or repagination must not restart the recording.
- Bind time to stable passage/section identity, not page number.
- Let a synchronized or section-timed transcript compose inside the same page system and link deliberately back to source.
- Prefer the minimum transport needed for listening: play/pause, position, transcript/source return, close. Add a cover, episode browser, production status, local audition UI, architecture map or DAW controls only when the user's actual task requires that separate experience.
- Keep voice provenance truthful and concise. Store detailed render receipts, provider/model evidence and authoring controls outside the reader surface unless they are directly relevant to the reader's decision.

Do not create a second player engine or second paginator to make audio visible.

## 6. Write in the present tense of evidence

Reader trust depends on temporal honesty.

Present what the work **does now** and what has actually been observed or published. Do not fill a reader-facing page with:

- a future test that has no scheduled/authorized execution;
- a hypothetical provider transfer;
- roadmap promises;
- planned domains presented as current destinations;
- inferred capability presented as an established result.

If an uncertainty affects the current reader action, state it narrowly. Otherwise keep future work in plans, issue tracking, governance, or authoring records rather than the public/editorial page.

Where evidence ends, let the prose end.

## 7. Keep architecture and provenance available without foregrounding them

Do not erase underlying rigor. Preserve exact source, rights, accessibility, versioning, renderer/player ownership, publication receipts and rollback evidence in their owning records.

Expose those details through appropriate secondary routes or disclosures when a reader, maintainer, auditor, or author needs them. Do not force every reader to traverse the system architecture in order to read an essay or hear a passage.

## 8. Acceptance checklist

For a changed Linotype reader, verify only the states relevant to the requested outcome:

- source text reconstructs exactly from composed leaves;
- no default paginated leaf clips or vertically scrolls to hide overflow;
- readable type survives phone/tablet portrait and landscape, plus requested accessibility enlargement;
- source position survives rotation/reflow and copied passage links;
- keyboard/touch controls remain reachable and named;
- illustrations reduce rather than add explanatory burden;
- audio, when present, remains source-bound and does not become a nested application by default;
- reader-facing text states observed current behavior and contains no speculative future success;
- architecture/evidence remains available in its owning records without dominating the reading surface.

Stop when the requested reading/listening experience is clear and proved. Do not keep editing merely because more explanation or interface can be added.
