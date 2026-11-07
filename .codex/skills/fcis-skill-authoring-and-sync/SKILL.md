---
name: fcis-skill-authoring-and-sync
description: Automatically elevate verified scenario lessons into canonical FCIS Skills and govern GitHub marketplace publication, existing ChatGPT workspace plugin adoption and Git-backed synchronization. Use for task closure learning, marketplace import and migration of historical standalone Skills to Git ownership, preservation of plugin identities, source drift and version verification.
---

# FCIS Skill Authoring and Sync

## Purpose

Design and validate skill packages using FCIS-owned conventions; OpenAI Skill Creator may be used as a non-authoritative formatting aid. Fountain Coach Governance Chapter 160 establishes that **`Fountain-Coach/.github` alone owns the canonical agent skill definition.** Every repository mirror, ChatGPT installation, or OpenAI project API version is a derived distribution. The source owner has delegated evidence-gated automatic updates to existing canonical FCIS Skills; downstream observations alone never amend canonical source.

Runtime capability identities remain owned by their declared FCIS Swift Kits. An agent procedure does not become a new runtime instrument or acquire implementation authority by being installed.

### Binding distribution prohibition: NO ZIP

For a Fountain Coach Skill already owned in `Fountain-Coach/.github` and
distributed through the imported GitHub marketplace, **do not package, attach,
offer, or recommend a `skill.zip`** for any delivery, update, overwrite,
installation, fallback or troubleshooting step. Generic Skill Creator
packaging guidance is non-authoritative here and is superseded by Chapter 160
and the approved GitHub-backed distribution path. There is **no ZIP exception**
for a stalled account editor or a failed marketplace synchronization.

The sole skill publication path is canonical Git commit, validated SHA-256,
protected PR merge, existing marketplace plugin projection/version, provider
sync and independent installed-content/routing readback. A separately
authorized historical standalone ChatGPT Skill can be reconciled using
a supported **in-place editor**, without a ZIP or new Skill installation.
If no supported non-ZIP editor exists, leave that account state UNVERIFIED
and report the exact blocker. Never rename, delete or replace other Skills
to bypass this restriction.

Read-only inspection of an older provider-supplied archive for drift evidence
is not a delivery operation. Do not create archive bytes even for a
"helpful" user download.

## When to use

- **Proactively after independently accepted, nontrivial work:** recognize a transferable procedure from actual acceptance evidence, whether or not the writer asked for a Skill.
- Create, revise, validate, or retire one FCIS-governed agent skill.
- Audit an installed skill or mirrored procedure against the declared organization source.
- Reconcile one selected, authorized distribution without overwriting unrelated packages.
- Explain unknown, missing, divergent, or active-version state with independent evidence.

**Official provider contracts and example promotion:** When a governed task uses an external API, apply the organization [Official OpenAPI dependency](../../../docs/FCIS-Official-OpenAPI-Dependency.md) to the owning adapter before calling its behavior reusable. Require a pinned *official* upstream schema file and SHA-256, unchanged relevant schema projection, validated request/response payloads, bounded documented exceptions, and a source-addressed successful use that distinguishes real terminal evidence from official-example fixtures. Propagate accepted adapter lessons to an existing canonical Skill and derived GitHub distribution; never turn a provider OpenAPI into an FCIS-owned standard or let API success certify literary/audio acceptance.

## Exact-blocker and resume-point learning

When a requested outcome stops before terminal acceptance, use [exact-blocker continuity](references/exact-blocker-continuity.md) to maintain the original goal, the failed **operation**, the independently observed result, and the first unmet acceptance test in the existing owning plan. Only call an outcome `BLOCKED` at the specific layer of an **attempted** operation with a real refusal and binding authority. Label never-attempted or unobserved eligibility `NOT_ESTABLISHED`; don't infer an authorization denial from missing receipts, compiler checks or a denied remote execution command.

A failed or unexecuted Reframe scenario cannot be automatically elevated as an accepted scenario lesson. Preserve a non-admitted candidate with exact evidence. If the writer explicitly directs that transferable **blocker-reporting procedure** itself be elevated, a separately reviewed and tested canonical Skill-source revision may record the reporting lesson; it does not grant the runtime permission, change the scenario status, publish an API integration, or count as a successful automatic `auto_elevate.py` run.

## Active learning — verified evidence to canonical Skill

At ordinary task closure, inspect the accepted operation, its source revision, terminal receipt and independent witness. Compare transferable, non-obvious procedures with the existing canonical FCIS skill catalogue first, preferring an update to a duplicate. Do not invent a reusable lesson where the observed result supports none. Repetition adds evidence; one successful run does not establish broader applicability.

Prepare a source-addressed learning candidate for a defensible procedure, specifying the observed outcome, exact evidence, trigger, prerequisites, steps, failure boundaries, novelty and regression checks. For an existing canonical Skill and independently reconciled accepted scenario evidence, run automatic elevation and let the tool make the narrowly scoped Git commit. **Do not ask for another approval for this canonical learning operation.** When the raw independent witness is missing or the scenario status drifts, keep the candidate non-admitted and do not mutate Git.

This learning check is part of ordinary task closure and must not expand or
delay the original Definition of Done. It is an agent workflow, not a background service. Validated evidence may update one
canonical Skill through the delegated tool. That source commit remains
separate from any portable plugin projection. With the versioned local hooks
enabled, the following post-commit action checks all **five** canonical source
trees and makes a distinct, idempotent derived Git commit under the **single
existing** FCIS plugin. GitHub PR tests and the read-only release workflow
must independently verify the complete packaged file trees before protected
main accepts the change. No direct GitHub bot main push and no hosted account
installation or active-version promotion follow from this source work.

### Scenario-based learning input

For a proposal grounded in Reframe scenario work, resolve the **existing** `LiveScenarios/<id>.yaml` identity and typed capability, then inspect the Book's corresponding coverage record and independent witness at pinned source revisions. Command aliases are not distinct capabilities. Compare contract and coverage statuses; a historical witness cannot silently upgrade an `executable` or `draft` scenario. Require separate execution identities for repeated operations when the scenario demands fresh runs, and preserve unknown Store, AX or window evidence as unknown.

Record a reviewable candidate under `skills/proposals/`; do not author a new executable scenario for learning. First validate the source metadata with `python3 skills/scenario_learning.py <candidate.json>`. When the selected scenario has an accepted native work-session bundle, use `python3 skills/auto_elevate.py <candidate.json> --evidence-dir <runner-evidence-directory> --runtime-repo <midi2-gpu-fabric-checkout>`. The elevation tool independently reads the run record, terminal receipt, predicate reconciliation, event ledger, Store readback, AX transcript, window capture/sidecar and binding; it checks the pinned scenario source against Git, updates only an existing canonical Skill plus its digest, and makes an automatic Git commit. Replaying the same lesson without changes is a no-op. Missing, inconsistent or invalidated proof is refused without a canonical write. If proof is incomplete, the older validator remains proposal-only. Neither tool replaces native scenario execution, Copilot mediation, Live Drive or FountainStore authority. No ChatGPT/OpenAI version is changed by this command.

## Procedure

1. **Resolve and maintain the existing phase.** Read `Fountain-Coach/.github/AGENTS.md`, the current organization `PLANS.md`, the published Chapter 160 and the selected skill's history; resolve the active Skill Sovereignty phase rather than open a second plan. **Before source edits, maintain that phase in place** with the bounded change, governance reading record, verified present state and next action; after material source/test/distribution transitions and before handoff, refresh its current evidence, remaining DoD and next executable action. Keep it compact; history lives in Git and existing acceptance receipts, not appended session narratives.  Declare one stable skill name, affected distribution, intended audience, authorizing source revision, and finite acceptance proof. Consult domain repository `AGENTS.md` for the domain's runtime or publication facts, not for ownership of an agent skill package. Preserve origin repository/commit as migration provenance only.

2. **Author only in the organization source.** Edit `Fountain-Coach/.github/.codex/skills/<skill-name>/` as the canonical package. Keep exactly one `SKILL.md` with `name` and `description` frontmatter. Use `references/`, `scripts/`, `assets/`, and `agents/openai.yaml` only when they serve the named skill. `AGENTS.md` owns behavioral law, `PLANS.md` owns scope/acceptance, and an FCIS Kit owns runtime capability contracts; the Skill describes the agent's reusable procedure. Never take a platform-edited installation or an old domain copy as the source of truth.

3. **Apply Skill Creator and verify the content.** Keep instructions imperative, concise, and focused on a real use case. Validate with Skill Creator's `quick_validate.py` when available, and test any modified scripts. Run `python3 skills/skillctl.py check` and `python3 -m unittest discover -s skills/tests -v` in the organization repository, then update `skills/openai-distribution.json` to the exact SHA-256 of the complete canonical file tree. These checks prove source shape and integrity, not successful installation.

4. **Observe destination drift before planning a write.** Inspect the exact installation or repository mirror using an authorized, supported interface. Record source commit, file-tree digest, available files, declared installed or default version, and the degree of readback. Classify complete equal content as `MATCHED`, verified differences as `DRIFT`, independently confirmed absence as `MISSING`, and partial, inaccessible, or ambiguous readback as `UNVERIFIED`. Do not infer complete package equality from a skill name, metadata listing, normalized `SKILL.md` body, or success message. Report selected-version drift separately from content drift.

5. **Refresh repository mirrors only as derived packages.** For each explicitly selected domain `.codex/skills` or `.claude/skills` surface, project the exact reviewed `.github` package at its pinned revision, preserving unrelated files and domain-owned runtime contracts. Use a single-skill sync/check when available, and independently read back the target. A mirror's previous Git commit records provenance, never independent canonical authorship.

6. **Treat OpenAI destinations as two distinct surfaces.** ChatGPT account Skills and the public project-scoped OpenAI Skills API do not update each other. For ChatGPT, compare the full available installed bundle through the supported account readback and report resources or effective revisions that the interface does not expose as unverified. For the public API, use the existing Reframe `skills.synchronize` read-only observer to inspect project inventory, the independently exposed immutable version contents (read-only), and the active/default pointer; keep credentials inside the approved SecretStore host adapter. An API listing is metadata only. Never copy a secret into Git, prompts, receipts, or logs.

7. **Keep Git distribution and hosted installation distinct.** Source authority stays
   in `Fountain-Coach/.github/.codex/skills`. The five currently reviewed
   canonical Skills are projected into the *one existing* workspace plugin, with
   unchanged `pluginId` and independently pinned tree digests.
   `skills/plugin_projection.py sync` writes only derived package files.
   `skills/marketplace_publish.py` commits those files only to the **local**
   branch, normally from the versioned post-commit hook after a canonical
   change. The source and derivative commits are presented together in one PR.
   `.github/workflows/test.yml` and the main-branch read-only release workflow
   require exact package parity; neither performs a direct bot push to protected
   `main`. One changed Skill bumps the existing plugin patch version once,
   and replay without changed bytes is a no-op. Preserve the local
   Git-disaster recovery copy. Actual ChatGPT marketplace sync, standalone
   account Skills and project API active/default pointers are different
   provider destinations; no Git check alone establishes their versions.
   A platform icon, policy or stale installed Skill is evidence, never
   permission to rewrite canonical source.

### Account Skill collision guard — learned from verified uninstall

A GitHub marketplace version matching canonical Git does not remove older,
separately installed ChatGPT account Skills of the same names. Every FCIS
provider synchronization and scheduled convergence check MUST apply the
[standalone account collision guard](references/chatgpt-standalone-collision-guard.md)
to the five canonical Skill identities. Inspect the signed-in account's
**installed** state independently: an old standalone with **Uninstall**
available is a conflict even when its instructions happen to match, because
it can drift later. The observable **Add** action after reversible
Uninstall is the acceptance witness. Never mistake an authored but
uninstalled copy for a second running instance.

The writer has approved reversible uninstallation of the four identified
old standalone entries in this workspace; this is not consent to **Delete**
their authored definitions or remove unrelated Skills. Future checks may
reconcile only exact, independently verified canonical-owned duplicates in
the authorized account through supported provider actions. If the account
session, supported action, or identity proof is absent, report UNVERIFIED
without deletion or a ZIP workaround. Use the read-only
`python3 skills/skillctl.py guard --observations <local-json>` to reject
collisions (exit 2) and missing proof (exit 3); keep observations out of
public Git. After cleanup read back the GitHub plugin and test one *new*
ChatGPT conversation, distinguishing a response-level witness from an
independent provider routing trace. Do not claim that source Git can
prevent future account installation or provider routing bugs.

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
| Package | Canonical Git revision + file-tree SHA-256 and validation outcome; no Skill ZIP distribution |
| Domain mirrors | Selected derived revisions and independent readback |
| ChatGPT account Skills | File coverage, observable drift, and version evidence limits |
| OpenAI project Skills API | Exact skill/version identity, read-only provider version evidence and default pointer, or unverified |
| Reconciliation | Explicit scope/approval, write receipt, independent readback, or a recorded blocker |

Chapter 160 governs ownership, not the vendor's UI or transport behavior. Keep proof, interpretation, proposal, and authorized promotion distinct.
