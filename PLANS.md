# Skill Sovereignty implementation

## Current continuation — scenario-based active skill learning (30 October 2026)

**Status:** **SOURCE-VALIDATED SCENARIO-LEARNING PILOT; external skill versions NOT YET RECONCILED.** **Accepted goal:** demonstrate the active proposal protocol against a real, previously accepted Reframe scenario with pinned source and independent published witness, before any new runtime learning or skill distribution. Proposals remain non-admitted.

**Governance reading record**
- **Read:** FCIS Goal Fidelity (source-level, non-invented goal); Governance 07 (finite scope and truthful acceptance), 08 (artifact-backed claims), 112 (runtime capability requires existing Swift Kit identity), 119 (scenario terminal evidence, no self-approval), 160 (one canonical skill source, candidate is not distribution).
- **Forbidden:** treating a command alias as a standalone capability, inferring proof from a skill name or summary, promoting a skill from one historical witness, inventing Store events, quietly changing scenario status, or creating new Kit/runtime/host authority to test the proposal.
- **Conflict:** scenario authoring must normally originate in Copilot and persist through FountainStore before YAML materialization. This pilot consumes an **existing** named scenario and its published historical witness; it neither authors a new executable scenario nor bypasses Copilot confirmation.
- **Excluded:** new Reframe scenario / MIDI2 operation, native learning observer, OpenAI/ChatGPT distribution, Store migration, GUI drive without a running bound process, public release and unrelated Reader work.

**Finite source-side acceptance:** consume existing real named scenarios and pinned published witnesses; produce one non-admitted revision proposal for an accepted scenario and one status-drift warning for a discrepant scenario; reject alias-as-skill, duplicate execution IDs, forged admission and unsafe provenance; keep raw Store/AX/window evidence explicitly missing. Verify the canonical package hash and focused source tests. No native runner, Copilot mediation, FountainStore execution or background monitoring is claimed.

**Current evidence:** The existing active-learning rule was committed at `Fountain-Coach/.github@33d816e54da1cc1a75bc510409183d2c0fd32d8b`. This bounded source continuation adds `skills/scenario_learning.py`, two pinned JSON candidates and negative tests. The real `commands-discover` scenario (integration `live-accepted`, Book `live-accepted`) yields `PROPOSED_EVIDENCE_LIMITED` for a revision of the existing FCIS skill authoring procedure, rather than a new command-named skill. The real `readings-comparison` scenario (integration `executable`, Book `live-accepted`) yields `PROPOSED_STATUS_DRIFT` without silently promoting historical evidence. Original raw Store, AX and window-ID artifacts were not independently reread. Native source checks: **4/4** canonical skill trees; **24/24** tests; both source proposal validators and `git diff --check` passed. Updated complete skill-tree SHA-256: `85cd39f54f6ccb9caa3abc605a395115821590362b61908e6393da9953caf111`, pinned in `skills/openai-distribution.json`. This demonstrates reproducible source-level candidate classification only.

**Linked pilot:** [Reframe R27 current phase](https://github.com/Fountain-Coach/Reframe/blob/main/PLANS.md#r27--estate-semantic-sorting-and-eventual-reader-migration-2026-10-29) was updated **in place** at `cac12bffb02cc1a1590ecc883ab828f0cc750f5e` to resume the original Reader goal from R28 v65, retain **R27-01** as the next unfinished step and keep public release separately authorized. Its root `AGENTS.md` now imports the explicit read/write/hand-off rule at `48176dc98119cd3aa37f94aa96184b65c0d5dd74`. No separate scenario was created.

**Next:** when Reframe's running Copilot scenario authoring and native `ReframeScenarioRunner`/Live Drive path are available, verify the matching scenario through the managed Store, AX and window-ID witness; only then upgrade the candidate evidence classification or seek admission of the procedural revision. Resolve the `readings-comparison` integration-vs-Book status discrepancy through its owning scenario workflow, never by editing a status to fit the proposal. Keep Reframe R27-01 on its independent accepted phase. No hosted Skill/version, public Governance or Reader release was changed.

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

## Phase 5 — bounded account editor and read-only Reframe observer follow-up (26 October 2026)

**Goal:** Reconcile only the installed `fcis-skill-authoring-and-sync` ChatGPT package to the canonical `.github` revision and observe the exact public OpenAI project version through the existing Reframe read-only provider. Keep ChatGPT account and public project versions distinct; do not assert Reframe GUI/MIDI2 acceptance without its own live evidence.

**Governance reading record**
- **Chapters read:** 07 (no invented prerequisite and bounded work), 08 (independent artifact-backed proof), 160 (sole canonical source; observed differences never grant source authority). Organization `AGENTS.md` and the existing skill authoring/sync procedure also apply.
- **Forbidden here:** bulk update or deletion of other ChatGPT skills, importing icon/policy additions into Git, copying credentials into tools or logs, pretending the provider's fixture tests are remote project readback, or inventing a scenario command to compensate for missing live acceptance.
- **Conflict:** the editor's folder-upload flow exposed an added root-level `openai.yaml` instead of replacing `agents/openai.yaml`; the attempted account-side correction therefore did not achieve the required exact bundle comparison. Treat this as an observation of the UI path, not proof that the account service deliberately reauthors packages.
- **Excluded:** destructive account updates, production OpenAI project version promotion, private source publication, unrelated Reframe GUI or Kit changes. A prospective runtime scenario must be separately authored and admitted through Reframe.

**Observed execution:** Canonical organization head `4e70d5f` retains the versioned `b545a106319bf82d577761fe01a58168a179429827b2c7954abe2b3d681c647d` package digest. On the authorized Mac's ChatGPT FCIS skill editor, a folder upload did not replace the expected relative resource; a root-level `openai.yaml` appeared in the file tree. Removal was selected in the editor, but a durable save and subsequent ZIP/version readback were not established; the installed Skills read interface did not expose that root file. No unqualified account synchronization claim is permitted.

**Reframe observer check:** Source at `Fountain-Coach/midi2-gpu-fabric` commit `f7d5741` contains the GET-only exact-version ZIP/default-pointer observer and the existing `skills.synchronize` Store adapter. The source scan found test call sites but no production invocation and no matching `LiveScenarios` contract. An isolated native focused test build was started without reading secret data; test completion and authenticated project readback require separate terminal receipts. A registered Keychain item alone is not project authorization or successful API access.

**Current acceptance:** Canonical source and selected Reframe mirrors remain proven by preceding phases. ChatGPT content remains `DRIFT`; selected account version, project API version/default pointer and Reframe GUI/MIDI2 proof remain `UNVERIFIED`. Do not advance the DoD or report a completed remote update.

**Phase 5 native terminal addendum (26 October 2026):** The existing Reframe project Skills GET-only provider, exact-version ZIP reader and FountainStore observation adapter completed **23/23 native focused XCTest cases** with shell exit 0 from the isolated `f7d5741` checkout using an external APFS SwiftPM scratch path (8 exact-version, 6 inventory provider, 9 Store adapter). The existing MaintenanceKit observer passed **11/11** separately; total 34/34 tests, no source changes. The original system-volume link failure (no space left on device) was bypassed only by relocating this session's scratch build; the partial invalid cache was removed, verified clean isolated checkout and retained successful logs/build. This is native fixture proof, not an authenticated public Skills API project readback, effective ChatGPT account version or a Reframe GUI/MIDI2 run. Refer to `docs/Skill-Distribution-Audit-2026-10-26.md` for exact terminal evidence and three exported account ZIP receipts.
