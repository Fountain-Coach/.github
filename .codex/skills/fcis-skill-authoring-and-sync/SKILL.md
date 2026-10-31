---
name: fcis-skill-authoring-and-sync
description: Automatically elevate verified scenario lessons into canonical FCIS Skills and govern GitHub marketplace publication, existing ChatGPT workspace plugin adoption and Git-backed synchronization. Use for task closure learning, marketplace import and ZIP-to-Git migration, preservation of plugin identities, source drift and version verification.
---

# FCIS Skill Authoring and Sync

## Purpose

Design and validate skill packages using FCIS-owned conventions; OpenAI Skill Creator may be used as a non-authoritative formatting aid. Fountain Coach Governance Chapter 160 establishes that **`Fountain-Coach/.github` alone owns the canonical agent skill definition.** Every repository mirror, ChatGPT installation, or OpenAI project API version is a derived distribution. The source owner has delegated evidence-gated automatic updates to existing canonical FCIS Skills; downstream observations alone never amend canonical source.

Runtime capability identities remain owned by their declared FCIS Swift Kits. An agent procedure does not become a new runtime instrument or acquire implementation authority by being installed.

### Distribution override for organization-owned Skills

For a Fountain Coach Skill already owned in `Fountain-Coach/.github` and distributed through the imported GitHub marketplace, **do not package, attach, offer, or recommend a `skill.zip` as the normal deliverable.** Generic Skill Creator packaging guidance is non-authoritative here and is superseded by Chapter 160 plus the established GitHub-backed distribution path.

The normal completion artifact is: canonical Git commit + validated file-tree digest + GitHub marketplace projection/version + hosted sync/readback state when observable. A ZIP is permitted only when the writer explicitly requests a legacy/manual archive, when diagnosing a ZIP-to-Git migration, or when a distinct provider API itself requires archive bytes internally. In those cases, never present the archive as the canonical source or as the preferred installation path.

## When to use

- **Proactively after independently accepted, nontrivial work:** recognize a transferable procedure from actual acceptance evidence, whether or not the writer asked for a Skill.
- Create, revise, validate, or retire one FCIS-governed agent skill.
- Audit an installed skill or mirrored procedure against the declared organization source.
- Reconcile one selected, authorized distribution without overwriting unrelated packages.
- Explain unknown, missing, divergent, or active-version state with independent evidence.

## Active learning — verified evidence to canonical Skill

At ordinary task closure, inspect the accepted operation, its source revision, terminal receipt and independent witness. Compare transferable, non-obvious procedures with the existing canonical FCIS skill catalogue first, preferring an update to a duplicate. Do not invent a reusable lesson where the observed result supports none. Repetition adds evidence; one successful run does not establish broader applicability.

Prepare a source-addressed learning candidate for a defensible procedure, specifying the observed outcome, exact evidence, trigger, prerequisites, steps, failure boundaries, novelty and regression checks. For an existing canonical Skill and independently reconciled accepted scenario evidence, run automatic elevation and let the tool make the narrowly scoped Git commit. **Do not ask for another approval for this canonical learning operation.** When the raw independent witness is missing or the scenario status drifts, keep the candidate non-admitted and do not mutate Git.

This learning check is part of ordinary task closure and must not expand or delay the original Definition of Done. It is an agent workflow, not a background service or evidence of a running Reframe learning observer. Validated scenario lessons may update existing canonical Git Skills through the delegated tool; they cannot grant Swift Kit capabilities or change the running scenario. A separate, delegated GitHub Action synchronizes the derived marketplace package after the verified canonical revision reaches `main`, checking the complete source tree and bumping the plugin version only when the canonical bytes change. This GitHub-only publication cannot install a ChatGPT account Skill, publish to the OpenAI Skills API or move a hosted active version; those effects remain separately governed.

### Scenario-based learning input

For a proposal grounded in Reframe scenario work, resolve the **existing** `LiveScenarios/<id>.yaml` identity and typed capability, then inspect the Book's corresponding coverage record and independent witness at pinned source revisions. Command aliases are not distinct capabilities. Compare contract and coverage statuses; a historical witness cannot silently upgrade an `executable` or `draft` scenario. Require separate execution identities for repeated operations when the scenario demands fresh runs, and preserve unknown Store, AX or window evidence as unknown.

Record a reviewable candidate under `skills/proposals/`; do not author a new executable scenario for learning. First validate the source metadata with `python3 skills/scenario_learning.py <candidate.json>`. When the selected scenario has an accepted native work-session bundle, use `python3 skills/auto_elevate.py <candidate.json> --evidence-dir <runner-evidence-directory> --runtime-repo <midi2-gpu-fabric-checkout>`. The elevation tool independently reads the run record, terminal receipt, predicate reconciliation, event ledger, Store readback, AX transcript, window capture/sidecar and binding; it checks the pinned scenario source against Git, updates only an existing canonical Skill plus its digest, and makes an automatic Git commit. Replaying the same lesson without changes is a no-op. Missing, inconsistent or invalidated proof is refused without a canonical write. If proof is incomplete, the older validator remains proposal-only. Neither tool replaces native scenario execution, Copilot mediation, Live Drive or FountainStore authority. No ChatGPT/OpenAI version is changed by this command.

## Procedure

1. **Resolve and maintain the existing phase.** Read `Fountain-Coach/.github/AGENTS.md`, the current organization `PLANS.md`, the published Chapter 160 and the selected skill's history; resolve the active Skill Sovereignty phase rather than open a second plan. **Before source edits, maintain that phase in place** with the bounded change, governance reading record, verified present state and next action; after material source/test/distribution transitions and before handoff, refresh its current evidence, remaining DoD and next executable action. Keep it compact; history lives in Git and existing acceptance receipts, not appended session narratives.  Declare one stable skill name, affected distribution, intended audience, authorizing source revision, and finite acceptance proof. Consult domain repository `AGENTS.md` for the domain's runtime or publication facts, not for ownership of an agent skill package. Preserve origin repository/commit as migration provenance only.

2. **Author only in the organization source.** Edit `Fountain-Coach/.github/.codex/skills/<skill-name>/` as the canonical package. Keep exactly one `SKILL.md` with `name` and `description` frontmatter. Use `references/`, `scripts/`, `assets/`, and `agents/openai.yaml` only when they serve the named skill. `AGENTS.md` owns behavioral law, `PLANS.md` owns scope/acceptance, and an FCIS Kit owns runtime capability contracts; the Skill describes the agent's reusable procedure. Never take a platform-edited installation or an old domain copy as the source of truth.

3. **Apply Skill Creator and verify the content.** Keep instructions imperative, concise, and focused on a real use case. Validate with Skill Creator's `quick_validate.py` when available, and test any modified scripts. Run `python3 skills/skillctl.py check` and `python3 -m unittest discover -s skills/tests -v` in the organization repository, then update `skills/openai-distribution.json` to the exact SHA-256 of the complete canonical file tree. These checks prove source shape and integrity, not successful installation.

4. **Observe destination drift before planning a write.** Inspect the exact installation or repository mirror using an authorized, supported interface. Record source commit, file-tree digest, available files, declared installed or default version, and the degree of readback. Classify complete equal content as `MATCHED`, verified differences as `DRIFT`, independently confirmed absence as `MISSING`, and partial, inaccessible, or ambiguous readback as `UNVERIFIED`. Do not infer complete package equality from a skill name, metadata listing, normalized `SKILL.md` body, or success message. Report selected-version drift separately from content drift.

5. **Refresh repository mirrors only as derived packages.** For each explicitly selected domain `.codex/skills` or `.claude/skills` surface, project the exact reviewed `.github` package at its pinned revision, preserving unrelated files and domain-owned runtime contracts. Use a single-skill sync/check when available, and independently read back the target. A mirror's previous Git commit records provenance, never independent canonical authorship.

6. **Treat OpenAI destinations as two distinct surfaces.** ChatGPT account Skills and the public project-scoped OpenAI Skills API do not update each other. For ChatGPT, compare the full available installed bundle through the supported account readback and report resources or effective revisions that the interface does not expose as unverified. For the public API, use the existing Reframe `skills.synchronize` read-only observer to inspect project inventory, the exact immutable version's ZIP, and the active/default pointer; keep credentials inside the approved SecretStore host adapter. An API listing is metadata only. Never copy a secret into Git, prompts, receipts, or logs.

7. **Keep GitHub distribution and hosted installation distinct.** The writer explicitly authorized the existing FCIS Skill's GitHub marketplace projection after verified canonical learning: `.github/workflows/fcis-marketplace-sync.yml` runs the source/digest tests, projects that one Skill with `skills/plugin_projection.py sync`, verifies byte equality, and uses `skills/marketplace_publish.py` for a derived-only fast-forward Git commit. Changed Skill bytes increment the plugin patch version; unchanged bytes are a no-op. Do not publish unrelated files or silently rewrite the original. ChatGPT account installation, Skills API upload and selected active/default version changes still require their own supported authorized workflow and independent readback. A platform-specific icon or policy field found only in an installed copy is an observation, not permission to import it into Git.

### Verified GitHub-to-ChatGPT installation lesson

For a request to install, adopt, repair or synchronize an existing ChatGPT workspace plugin from GitHub, first read [the verified marketplace takeover procedure](references/chatgpt-github-marketplace-takeover.md). Do not confuse ZIP upload with an imported GitHub marketplace. In the authenticated workspace Admin Console, preserve the installed plugin's exact ID in the GitHub marketplace declaration, choose **Plugins → Hinzufügen → Marketplace importieren**, and independently read back the Git revision, completed import, enabled auto-sync, and the original installed plugin identity and version. Treat a transient status warning as a symptom until the settled provider status is inspected. This lesson comes from an independently witnessed provider installation, not a Reframe native scenario.

8. **Close with bounded evidence and a maintained plan.** Reconcile the active organization `PLANS.md` phase in place with exact commits, validation, distribution status and next unfinished action. Report `PROVEN`, `DRIFT`, `MISSING`, or `UNVERIFIED` per destination, with the exact source commit and evidence address. An installation is synchronized only to the degree the complete package and effective selected execution version have both been independently verified. Leave a divergence open when an authorization or supported readback is absent; do not invent a replacement API or claim organization-wide synchronization from one skill.

## Verified scenario lessons

<!-- FCIS-AUTO-LESSON 58fd839333f71c4fe51b -->
### commands-discover — verified reusable procedure

**Lesson:** When learning from an accepted Reframe command scenario, use its declared Composer MIDI2 ingress, witness the semantic chat reply through a bound Reframe-labelled AX row rather than a missing child title, and reconcile capability identity with terminal phase in one persisted Store event before automatically updating an existing canonical FCIS Skill.
**Trigger:** An independently accepted Reframe scenario provides a reusable procedure involving command dialogue, virtualized response presentation, and persisted capability lifecycle evidence.
**Distinct from prior instructions:** The earlier proposal checks scenario status and aliases but not current triadic input authority, virtualized AX reply semantics, or matching the capability and terminal phase within one persisted lifecycle event. Two invalidated live attempts establish the distinct failure boundaries.
**Scenario provenance:** commands-discover at d10e6a6b32d9019793290099321bd6d64d71c4b2; run 045bdb10-ada3-4bce-be60-dc5525345b1b; typed receipt 85547b2f-b6ff-4822-8c94-02f691c02639.

**Preconditions:**
- A committed scenario contract and source revision with reproducible native Swift runner validation and an existing owning capability identity.
- An independently accepted run with matching terminal receipt, event ledger, managed Store readback, AX transcript and CoreGraphics window-ID evidence.
- An existing organization-owned FCIS agent Skill whose procedure is the right target; command aliases are not new capabilities.

**Procedure:**
- Resolve the scenario by stable ID, owning capability identity and actual operation instead of command spelling or Book acceptance status.
- Enter writer dialogue through the declared Composer MIDI2 transport and canonical three participants, retaining AX as an independent read-only surface witness.
- Witness long or virtualized results from the semantic Reframe-labelled chat row when the inner title is not exposed in the currently available accessibility tree.
- Require the capability identity and terminal phase to agree within one persisted FountainStore lifecycle record; unrelated records cannot jointly satisfy a terminal predicate.
- Match source commit, executable, managed Store, run ID, terminal receipt, AX transcript, window sidecar and accepted event sequence before invoking automatic canonical Skill elevation.
- On missing or invalidated evidence, retain a non-admitted proposal; after an accepted run, revise the existing canonical Skill and package digest through the automatic Git commit path.

**Stop conditions:**
- Never bypass a MIDI2-only command ingress with AX settext or reinterpret a runtime transport refusal as accepted behavior.
- Never turn a successful Store result into live acceptance when the required independent AX result is absent.
- Never join a capability identity from one Store event to a terminal phase from another, or use an invalidated run as a transferable lesson.
- Do not create a Kit capability, change the runtime contract authority, or install or publish ChatGPT and OpenAI Skill versions as a side effect of canonical learning.

**Regression checks:**
- For an AX command-input attempt refused by the triadic MIDI2 contract, classify the run invalidated and prohibit automatic learning.
- For a long Reframe reply with a visible semantically labelled chat row and hidden child title, require a recorded same-row AX witness and matching Store terminal event.
- For two Store events containing a capability identity and a terminal phase separately, reject a fabricated combined terminal success.
- For a fully accepted source-pinned run, verify exactly one existing canonical Skill plus digest is committed, then repeat the same lesson without producing a duplicate commit.

<!-- /FCIS-AUTO-LESSON 58fd839333f71c4fe51b -->

## Output contract

| Field | Required result |
| --- | --- |
| Skill | Stable organization-owned identity |
| Source | `Fountain-Coach/.github`, exact path and Git commit |
| Package | Canonical Git revision + file-tree SHA-256 and validation outcome; no user-facing ZIP unless explicitly requested for a legacy/manual path |
| Domain mirrors | Selected derived revisions and independent readback |
| ChatGPT account Skills | File coverage, observable drift, and version evidence limits |
| OpenAI project Skills API | Exact skill/version identity, ZIP content result, and default pointer, or unverified |
| Reconciliation | Explicit scope/approval, write receipt, independent readback, or a recorded blocker |

Chapter 160 governs ownership, not the vendor's UI or transport behavior. Keep proof, interpretation, proposal, and authorized promotion distinct.
