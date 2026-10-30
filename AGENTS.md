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
unrelated source. **Separate, explicitly delegated GitHub distribution:** once
an admitted canonical Skill revision reaches `main`, the bounded GitHub Action
`.github/workflows/fcis-marketplace-sync.yml` checks source proof, synchronizes
only the matching existing portable GitHub marketplace Skill with a new plugin
patch version when bytes changed, and commits only derived package files back to
`main`. This publication is Git-only, idempotent and fail-closed on drift or
unrelated changes; it is not ChatGPT account installation, hosted Skills API
publication, active-version promotion or workspace-administration authority.
Those distinct provider changes retain their governing permissions and proof.
This is an agent task-closure plus GitHub-source workflow, not evidence of an
unobserved Reframe learning service or a connected ChatGPT workspace.

A new blocker requires four traceable answers: requested outcome, current
failed operation, governing source, smallest necessary correction. An
unproven worry is a non-blocking hypothesis. A completed source patch is
not a completed live outcome.

This file governs this repository. Other Fountain Coach repositories must
carry an explicit root AGENTS import; GitHub does not automatically inject
organization-repository instructions into agents working elsewhere.
