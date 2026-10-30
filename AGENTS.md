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

A new blocker requires four traceable answers: requested outcome, current
failed operation, governing source, smallest necessary correction. An
unproven worry is a non-blocking hypothesis. A completed source patch is
not a completed live outcome.

This file governs this repository. Other Fountain Coach repositories must
carry an explicit root AGENTS import; GitHub does not automatically inject
organization-repository instructions into agents working elsewhere.
