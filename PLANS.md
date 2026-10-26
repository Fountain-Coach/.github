# Skill Sovereignty implementation

Governance authority: Chapter 160 at https://governance.fountain.coach/chapters/160-skill-sovereignty-and-governed-distribution/.

## Reading record
Read: Chapter 160 (single canonical source), 07 (goal fidelity), 08 (acceptance), 43 (named releases), 44 (source versus projection).
Forbidden: remote adoption into canonical source without review, destructive bulk sync, moving default or latest pointer without release authorization.
Conflict: historical FCIS authoring instructions and earlier organization manifest called domain repos canonical owners. This plan adopts the published Chapter 160 rule instead. Domain copies remain provenance-bearing projections.
Excluded: unrelated skill changes, remote credentials or account mutations, new runtime servers.

## Implemented source-side acceptance
- Three complete skill packages imported under the organization .codex/skills directory, preserving their historical source commit as provenance.
- Per-file-tree SHA-256 in skills/openai-distribution.json, validated against actual bytes.
- Reproducible skill ZIP, normalized paths, ordering, file modes and timestamps.
- Read-only package comparator yields MATCHED, DRIFT or UNVERIFIED and exact altered/missing/unexpected file paths.
- Local versioned pre-commit and pre-push hooks. Per checkout installation: git config core.hooksPath .githooks.
- Eight automated positive and negative tests including missing remote, missing file, modified file, duplicate archive entry and unchanged canonical source.

## Pending remote acceptance
- Refresh each domain repository's derived package by exact org Git revision, separately read back and record.
- Public OpenAI Skills API read-only version inventory, content readback, selected default/latest, and comparison after independently authorized access.
- ChatGPT account readback using a supported adapter: a visible skill name alone remains UNVERIFIED.
- One explicitly authorized targeted version upload and remote readback; no unattended deletion, bulk overwrite or version promotion.
- Controlled divergence, changed active pointer and deletion simulation in disposable destinations, followed by approved restoration.

## Definition of Done
Canonical org source matches its declared SHA-256; exact ZIP re-build matches; hooks fail invalid source; known comparison failures are detected without mutating the original. End-to-end DoD additionally requires authorized and independently proven remote readback, pointer audit and one controlled reconciliation per distribution surface. Do not claim that final remote DoD until witnessed.
