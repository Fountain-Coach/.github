# Fountain Coach Organization — Founding Agent Conduct

Before engineering, routing, publication or repository maintenance, read
[FCIS Goal Fidelity and Non-Invention](docs/FCIS-Non-Invention-and-Goal-Fidelity.md).

**Mandatory:** keep the requested outcome fixed; inspect existing functioning
capabilities first; distinguish observed/proven/documented/inferred/proposed;
never add a prerequisite to the DoD without a reproduced failure and an
applicable existing requirement; never treat tests of invented machinery as
proof of necessity; do not repeatedly ask the writer to say "proceed".
Preserve actual security boundaries while refusing speculative security
theatre. Correct unjustified expansions by reversible cleanup, not by
developing them further.

**External API contract rule (official OpenAPI dependent):** For every externally owned API adapter where the publisher supplies official OpenAPI, pin its immutable upstream revision and full-file digest, validate the actual request/response event shapes against unchanged vendor schemas, and retain source-bound successful examples as separate, labeled regression evidence. Record upstream defects explicitly; do not invent or silently fork provider schemas. See [FCIS Official OpenAPI Dependency](docs/FCIS-Official-OpenAPI-Dependency.md). This governs adapter correctness, **not** model quality, artistic acceptance, rights, release, or ownership of the provider protocol.

**Project continuity (mandatory for governed implementation):** Read the owning repository's current `PLANS.md` and resolve its accepted scenario, active phase, latest evidenced state and next unfinished action **before** proposing another plan or modifying source. Maintain that same phase **in place** during work and reconcile it before handoff; do not append a new session narrative on each turn. Keep the readable state concise and point to Git commits and existing acceptance records. FountainStore proves only Store operations independently witnessed there; GitHub collaboration metadata is not runtime proof. An unavailable Store is not automatically a blocker to an otherwise authorized Git operation. Preserve concurrent plan changes by checking the revision before writing. Consult the [FCIS project continuity contract](docs/FCIS-Non-Invention-and-Goal-Fidelity.md#project-continuity-and-transparent-execution) for exact boundaries.

**Active procedural learning (automatic canonical elevation):** After independently
accepted nontrivial work, proactively inspect actual result and available evidence
for a transferable, non-obvious procedure. Prefer revising an existing FCIS agent
Skill to creating a duplicate. For a Reframe scenario with a reconciled accepted
Swift terminal receipt, bound run/events, Store readback, AX and window-ID witness,
prepare an evidence-backed candidate and invoke `skills/auto_elevate.py` against
the exact evidence bundle and scenario source Git repository. A successful
validation automatically revises the one existing Skill under this organization's
`.codex/skills/`, updates its file-tree digest, and commits both canonical files
without a separate per-lesson approval. Repeated evidence is idempotent. Missing,
inconsistent, or invalidated evidence refuses mutation. If the work is not yet
independently witnessed, retain a non-admitted proposal; never fabricate proof.
Automatic elevation owns only canonical source learning. It cannot create a
Kit/runtime identity, rewrite the project's Definition of Done, or change
unrelated source. **Separate, explicitly delegated Git distribution:** the
versioned local `.githooks/post-commit` calls the existing
`skills/plugin_projection.py` and `skills/marketplace_publish.py` to make
one **separate derived commit** (never part of the canonical learning commit)
for the five reviewed Skill directories in the **existing single plugin**.
`test.yml` and the read-only main-branch
`.github/workflows/fcis-marketplace-sync.yml` refuse missing or drifting
mirrors. Source and derivative are reviewed in the *same PR*, and protected
`main` is updated only through required checks, not a bot push. A missing
local hook is not a bypass: CI fails when the exact mirrored package is absent.
This Git-owned procedure does not update ChatGPT account installations, the
hosted Skills API or active/default pointers. Independent provider
synchronization/readback remains a separate accepted operation; a source
commit is not hosted Skill acceptance.

**FCIS Skills: NO ZIP DELIVERY (binding, all agents and interfaces).**
Never create, attach, download for handoff, upload, recommend, or distribute
`skill.zip` or any ZIP archive as a means of releasing, installing, fixing,
overwriting, or synchronizing a Fountain Coach Skill. This prohibition
overrides generic Skill Creator packaging advice for organization-owned Skills.
Use **only** canonical `Fountain-Coach/.github` Git commits, protected merge,
the existing GitHub-backed marketplace, and independent provider readback.
A stale personal ChatGPT Skill may be updated **in place** only through a
supported editor when separately authorized; that is an account reconciliation,
not a second Skill distribution route. If no supported non-ZIP write surface
exists, record the blocker; do not fall back to ZIP. Read-only parsing of
historical/provider-supplied archive bytes is allowed for forensic comparison,
never as a creation or publication action. This rule does not affect
non-Skill archives or the tested Git disaster-recovery bundles.

**FCIS account Skill collision guard (binding for FCIS maintenance).**
The five canonical FCIS Skills are distributed through the single imported
GitHub-backed marketplace plugin. An independently installed account Skill of
the same canonical identity is a runtime authority collision even if its text
matches today. Following each marketplace synchronization, inspect the
authenticated account's exact installed state and run the read-only
`skills/skillctl.py guard` before claiming convergence. Under the user's
bounded authorization, a proven duplicate may be **uninstalled** using the
provider's reversible account control; never **delete** its authored copy,
touch unrelated Skills, or change the plugin identity. Preserve separate
evidence for the account uninstall, marketplace version, and actual fresh-chat
execution. GitHub Actions cannot see or manage account Skills, so a source
CI pass is not an account-cleanliness guarantee. Missing account access is
UNVERIFIED; no ZIP fallback or undocumented provider API.

A new blocker requires four traceable answers: requested outcome, current
failed operation, governing source, smallest necessary correction. An
unproven worry is a non-blocking hypothesis. A completed source patch is
not a completed live outcome.

This file governs this repository. Other Fountain Coach repositories must
carry an explicit root AGENTS import; GitHub does not automatically inject
organization-repository instructions into agents working elsewhere.
