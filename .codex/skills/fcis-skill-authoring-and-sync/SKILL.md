---
name: fcis-skill-authoring-and-sync
description: Create, revise, audit, and distribute FCIS-governed agent skills from the sole canonical source Fountain-Coach/.github. Use for authoring, drift detection, and governed reconciliation of repository-local Codex/Claude mirrors, ChatGPT account Skills, or the public OpenAI Skills API.
---

# FCIS Skill Authoring and Sync

## Purpose

Design and validate skill packages using the OpenAI Skill Creator while enforcing Fountain Coach Governance Chapter 160: **`Fountain-Coach/.github` alone owns the canonical agent skill definition.** Every repository mirror, ChatGPT installation, or OpenAI project API version is a derived distribution. Changes observed downstream may return as proposals, but never automatically become source.

Runtime capability identities remain owned by their declared FCIS Swift Kits. An agent procedure does not become a new runtime instrument or acquire implementation authority by being installed.

## When to use

- Create, revise, validate, or retire one FCIS-governed agent skill.
- Audit an installed skill or mirrored procedure against the declared organization source.
- Reconcile one selected, authorized distribution without overwriting unrelated packages.
- Explain unknown, missing, divergent, or active-version state with independent evidence.

## Procedure

1. **Resolve and maintain the existing phase.** Read `Fountain-Coach/.github/AGENTS.md`, the current organization `PLANS.md`, the published Chapter 160 and the selected skill's history; resolve the active Skill Sovereignty phase rather than open a second plan. **Before source edits, maintain that phase in place** with the bounded change, governance reading record, verified present state and next action; after material source/test/distribution transitions and before handoff, refresh its current evidence, remaining DoD and next executable action. Keep it compact; history lives in Git and existing acceptance receipts, not appended session narratives.  Declare one stable skill name, affected distribution, intended audience, authorizing source revision, and finite acceptance proof. Consult domain repository `AGENTS.md` for the domain's runtime or publication facts, not for ownership of an agent skill package. Preserve origin repository/commit as migration provenance only.

2. **Author only in the organization source.** Edit `Fountain-Coach/.github/.codex/skills/<skill-name>/` as the canonical package. Keep exactly one `SKILL.md` with `name` and `description` frontmatter. Use `references/`, `scripts/`, `assets/`, and `agents/openai.yaml` only when they serve the named skill. `AGENTS.md` owns behavioral law, `PLANS.md` owns scope/acceptance, and an FCIS Kit owns runtime capability contracts; the Skill describes the agent's reusable procedure. Never take a platform-edited installation or an old domain copy as the source of truth.

3. **Apply Skill Creator and verify the content.** Keep instructions imperative, concise, and focused on a real use case. Validate with Skill Creator's `quick_validate.py` when available, and test any modified scripts. Run `python3 skills/skillctl.py check` and `python3 -m unittest discover -s skills/tests -v` in the organization repository, then update `skills/openai-distribution.json` to the exact SHA-256 of the complete canonical file tree. These checks prove source shape and integrity, not successful installation.

4. **Observe destination drift before planning a write.** Inspect the exact installation or repository mirror using an authorized, supported interface. Record source commit, file-tree digest, available files, declared installed or default version, and the degree of readback. Classify complete equal content as `MATCHED`, verified differences as `DRIFT`, independently confirmed absence as `MISSING`, and partial, inaccessible, or ambiguous readback as `UNVERIFIED`. Do not infer complete package equality from a skill name, metadata listing, normalized `SKILL.md` body, or success message. Report selected-version drift separately from content drift.

5. **Refresh repository mirrors only as derived packages.** For each explicitly selected domain `.codex/skills` or `.claude/skills` surface, project the exact reviewed `.github` package at its pinned revision, preserving unrelated files and domain-owned runtime contracts. Use a single-skill sync/check when available, and independently read back the target. A mirror's previous Git commit records provenance, never independent canonical authorship.

6. **Treat OpenAI destinations as two distinct surfaces.** ChatGPT account Skills and the public project-scoped OpenAI Skills API do not update each other. For ChatGPT, compare the full available installed bundle through the supported account readback and report resources or effective revisions that the interface does not expose as unverified. For the public API, use the existing Reframe `skills.synchronize` read-only observer to inspect project inventory, the exact immutable version's ZIP, and the active/default pointer; keep credentials inside the approved SecretStore host adapter. An API listing is metadata only. Never copy a secret into Git, prompts, receipts, or logs.

7. **Reconcile only after explicit, targeted authorization.** Name the skill, destination, canonical source revision, expected prior installation and whether an active/default version would change. Submit one reviewed package at a time through the supported destination workflow, preserve the previous version and unrelated skills, and independently read back the resulting contents and version. A platform-specific policy or icon field found only in an installed copy is an observation, not permission to import it into Git. Do not silently delete, overwrite, retire, promote, or roll back anything; do not automate publishing on a Git push or through GitHub Actions.

8. **Close with bounded evidence and a maintained plan.** Reconcile the active organization `PLANS.md` phase in place with exact commits, validation, distribution status and next unfinished action. Report `PROVEN`, `DRIFT`, `MISSING`, or `UNVERIFIED` per destination, with the exact source commit and evidence address. An installation is synchronized only to the degree the complete package and effective selected execution version have both been independently verified. Leave a divergence open when an authorization or supported readback is absent; do not invent a replacement API or claim organization-wide synchronization from one skill.

## Output contract

| Field | Required result |
| --- | --- |
| Skill | Stable organization-owned identity |
| Source | `Fountain-Coach/.github`, exact path and Git commit |
| Package | Canonical file-tree SHA-256 and validation outcome |
| Domain mirrors | Selected derived revisions and independent readback |
| ChatGPT account Skills | File coverage, observable drift, and version evidence limits |
| OpenAI project Skills API | Exact skill/version identity, ZIP content result, and default pointer, or unverified |
| Reconciliation | Explicit scope/approval, write receipt, independent readback, or a recorded blocker |

Chapter 160 governs ownership, not the vendor's UI or transport behavior. Keep proof, interpretation, proposal, and authorized promotion distinct.
