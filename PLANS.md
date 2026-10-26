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


## Phase 3 — canonical procedure correction and independent ChatGPT account readback (26 October 2026)

**Goal:** Repair the existing FCIS skill-authoring procedure to obey the adopted Chapter 160 source authority, record independently observable differences from the account Skills projection, then validate one canonical package before any distribution mutation.

**Governance reading record**
- **Chapters read:** 07 (goal fidelity and bounded correction); 08 (evidence before status); 112 (runtime maintenance operation remains Kit-owned); 160 (Fountain-Coach/.github alone is canonical for agent skill packages). Organization AGENTS and the existing Chapter 160 implementation plan also apply.
- **Forbidden here:** making installed ChatGPT files canonical, bulk synchronization, importing unknown account metadata into the source, silently changing default versions, treating SKILL.md body readback as full ZIP and selected-execution proof, editing unrelated skills.
- **Conflict:** the existing canonical `fcis-skill-authoring-and-sync/SKILL.md` and the first paragraphs of `docs/OpenAI-Skills-API-Integration.md` assign skill ownership to domain repositories. This conflicts with the maintainer's explicit .github-only authority decision and Chapter 160. Repair the instructions at their source, while retaining historical origin commits as provenance only.
- **Excluded:** Reframe Kit and MIDI2 schema changes, unrequested new instruments, production release, account-wide overwrite, API-key export or authentication changes. OpenAI API project Skills and ChatGPT account Skills remain separate observed surfaces.

**Independent readback at authority commit `151c2944929c586dfdc74bc5f238fdda65bdde88`:** Via the installed ChatGPT Skills read interface and GitHub canonical file reads, Teatro Scenario Composer matched 7/7 accessible files, Linotype Estate Template matched 13/13 accessible files, and FCIS Skill Authoring matched its SKILL.md *body* but differed in `agents/openai.yaml`; account Skills also exposes `assets/icon.svg` that is not present in the canonical FCIS package. The installed FCIS icon has identical content to the installed Teatro icon. The installed YAML adds policy and icon properties, and changes formatting. Exact full archive content and effective execution/default-version pointers were not returned, so end-to-end synchronization remains **UNVERIFIED** even for the two content-matching packages.

**Source slice:** revise only the FCIS authoring Skill and organization distribution documentation, recompute its `skills/openai-distribution.json` SHA-256 from the actual canonical files, and preserve this evidence in a dated review record. Independent readback does not itself authorize an external push.

**Acceptance:** `python3 skills/skillctl.py check`, `python3 -m unittest discover -s skills/tests -v`, and Git hooks against the new org revision; inspect readback after any later one-skill authorized distribution, and report active-version state separately. A separately authorized Reframe Copilot scenario and a real OpenAI project readback are still required for full live acceptance.


## Phase 4 — correct remaining canonical metadata after account installation witness (26 October 2026)

- **Chapters read:** 07 (bounded scope and goal fidelity); 08 (independent evidence before claims); 160 (organization-owned canonical skill and external projection boundary).
- **Forbidden:** restoring obsolete `repo-owned` authoring instructions, treating a provider-generated icon/policy as canonical, silently editing additional skills, claiming save feedback proves exact package/version identity.
- **Conflict:** the already corrected canonical FCIS `SKILL.md` said `Fountain-Coach/.github` is the sole source, but its own `agents/openai.yaml` default prompt still directed the agent to a generic `repo-owned` skill; the installed account YAML also retained icon/policy extensions not authored by Git.
- **Excluded:** editing the installed platform's policy interface or unrelated skills; public API uploads, version promotion, Reframe UI/MIDI2 scenarios and Store receipt claims without actual host authentication and independent evidence.

**Source slice:** change only the FCIS `agents/openai.yaml` short description/default prompt in `Fountain-Coach/.github`; recalculate its complete file-tree digest and project the two-file canonical package into the selected Reframe Codex/Claude mirrors without touching other skills. Record the observed ChatGPT body match and supporting-file divergence in the account audit.

**Acceptance:** `python3 skills/skillctl.py check`; 8 source-side integrity tests; source/package quick validation; single-skill mirror checks and byte-for-byte readback. ChatGPT editor body and description were verified after reload; its YAML/icon and effective version remain divergent or unverified. Complete remote DoD remains open and no external API operation is implied.
