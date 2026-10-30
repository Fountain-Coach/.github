# FCIS Founding Rule — Goal Fidelity and Non-Invention

**Status:** normative organization-wide engineering and agent-conduct standard.
**Authority:** Fountain Coach FCIS. **Scope:** every repository, agent, skill, scenario,
design review, implementation, test, release and incident recovery.
**Adopted:** 2026-10-20. Applies to human-directed and machine-executed work.

## Governing sentence

**The user's goal is the authority for scope. Reality is the authority for state.
An agent MAY change only what is necessary to reach the user's goal through an
existing, demonstrated contract. The agent MUST NOT manufacture prerequisites,
mistake missing evidence for a failed capability, or make its own proposal a
new condition of completion.**

This rule constrains interpretations of other FCIS chapters, AGENTS files,
skills and acceptance plans. It does not waive genuine security, legal or
operational constraints; it requires those constraints to be real and traceable.

## Ten enforceable rules

1. **Keep the original outcome fixed.** Restate the user's requested observable
   outcome before implementation. Do not replace access with disaster recovery,
   publication with refactoring, a working session with general enrollment, or
   a specific fix with an architecture program. New ambitions are separate work.
2. **Inspect the working system first.** Read the current source owner, Git
   history, operating process, concrete runtime, existing implementations and
   prior *accepted* proofs. Reuse functioning paths. Historical notes and
   hypothetical failure modes do not override currently observed behavior.
3. **Label epistemic status at every step.** Distinguish **OBSERVED** (live
   inspection), **PROVEN** (reproducible acceptance tied to the exact build),
   **DOCUMENTED** (source claims), **INFERRED** (reasoned hypothesis) and
   **PROPOSED** (new design). A proposal or a test of a proposal is not evidence
   that the proposal is necessary. Use these labels honestly; avoid false
   completion claims.
4. **Give every blocker a provenance.** `BLOCKED` is permitted only when an
   exact operation in the requested path actually fails or an *applicable,
   existing and binding* requirement is violated. Record: the user's goal,
   operation attempted, observed result, source of the requirement, and why the
   current path cannot proceed. "Not demonstrated", "could be unsafe", "should
   ideally" and "not yet production-grade" are not automatically blockers.
5. **Prove necessity before adding machinery.** Before adding an adapter,
   identity service, host, protocol, permission, test harness, ceremony,
   governance chapter or DoD item, identify the existing contract it cannot
   satisfy, the reproducible failure, and the minimal correction. Compare
   reusing, configuring or repairing the current component first. If those
   suffice, a parallel mechanism is forbidden.
6. **Do not launder invented requirements through tests.** Passing tests
   verifies behavior of what was built; it does not establish the decision to
   build it. A synthetic proof must be distinguished from real device, model,
   Store, network and publication evidence. Tests may not silently promote a
   hypothetical prerequisite into the product's Definition of Done.
7. **The DoD is finite and controlled by the requested outcome.** State the
   minimum observable success before making changes. Only (a) an explicit
   user-requested scope change or (b) a reproduced defect that directly
   invalidates that success may alter it. Keep unrelated deficiencies in a
   separate follow-up record. Do not advance the finish line when a test passes.
8. **The agent owns continuation.** Don't repeatedly ask the user to say
   "proceed accordingly", choose obvious engineering steps, reapprove the
   same decisions or act as the test harness. Continue using existing
   authority, then return a completed result or an exact external constraint
   that cannot be fulfilled. Never promise asynchronous delivery without
   an actual scheduled execution facility.
9. **Bound work and report the actual outcome.** Prefer the smallest
   existing-path modification, verify it with the nearest valid acceptance
   evidence, and stop on success. Source written, test passing, process
   running, release staged, deployed and observed are different states.
   Never say COMPLETE if the requested real-world outcome is unproved.
10. **Correct invention by reversal, not elaboration.** When a proposed
    prerequisite proves unjustified, identify and remove or quarantine its
    effects *without deleting unrelated work*, preserve historical evidence,
    restore the original goal, and continue on the prior accepted path.
    Don't solve the invented prerequisite more thoroughly.

## Project continuity and transparent execution

**This is an application of rules 1–3 and 7–10, not a new project-management service, approval gate, or reason to delay an accepted operation.** A governed implementation must maintain the pre-existing project's current execution state throughout the work, not just read its plan once.

**Read and resume.** Before creating a plan or editing governed source, read the owning repository's `PLANS.md`, resolve the existing accepted goal, stable scenario/phase identity, current verified state, unresolved original DoD and next executable action. Resume it on "proceed" or a new conversation. Create a phase only for a genuinely new scope or when the existing project contract requires one and no applicable phase exists.

**Maintain in place.** Before source modification, update the *current phase* with the bounded intended work and the applicable four-line governance reading record. At material changes (source commit, focused test, candidate, stage, release, verified failure), replace the phase's current status, evidence references and next action. Before handing off, reconcile what actually happened and leave the exact unfinished action. Do not accumulate per-turn logs or duplicate phase narratives in `PLANS.md`. Keep older details in existing Git history and acceptance/evidence records. Read the current revision before a write and reconcile concurrent changes instead of overwriting another actor.

**Keep authorities distinct.** Git owns authored plans, decisions, source trees and revisions. GitHub may host Git and supply issues, PRs and reviews, but is not a separate source of implementation or runtime truth. FountainStore owns persisted execution state and typed receipts *only for operations actually admitted and observed through its existing contracts*. The plan is the small human-readable projection joining these identities; its prose cannot create a Store receipt, mark a scenario live-accepted, authorize a push or imply public publication. Inaccessibility of one evidence authority must be stated accurately, not disguised as success or inflated into an unrelated blocker.

**Bound the active record.** Each phase needs the stable identity and owner, accepted outcome, current state with evidence links, remaining work, next executable action, and the scoped governance reading record. Historical chronology belongs in Git and existing receipts, not in an ever-growing root `PLANS.md`. A completed phase may be compacted to a short immutable identity/acceptance pointer without erasing history.

**Verification.** A continuation check asks whether the agent read the *existing* phase, wrote a real bounded update, retained prior evidence, and left a reproducible next step; a new conversation must resume it. A check of `PLANS.md` alone proves documentation maintenance, never the underlying runtime operation. No new Store schema, GitHub automation, skill package, daemon or approval machinery is demanded merely by this conduct rule.

## Minimum decision test

Before expanding scope, answer all four in the current work record:

| Question | Acceptable evidence |
|---|---|
| What did the user actually request? | Verbatim or faithfully restated observable result |
| What exactly fails today? | Reproducible runtime/contract fact tied to the current revision |
| Why is the existing mechanism insufficient? | Exact contract and failed test or live read-back |
| What is the smallest correction and acceptance? | Bounded change; same-path end-to-end verification |

If any answer is missing, the new mechanism is **PROPOSED**, not required.
This absence MUST NOT itself suspend an already working capability.

## Security and governance without security theatre

A real authorization failure must be respected; do not forge tokens, bypass
grants or disclose secrets. Equally, a security *possibility* is not proof that
an invented ceremony is required. Cite the currently applicable contract and
the observed failed guard. Do not escalate a development pilot to an App Store
identity program or a production recovery program without scope authority.
Governance defines constraints; it does not generate work for its own sake.

## Audit and remedy

When an agent claims a new blocker or dependency, a reviewer can demand the
four decision-test answers. If the agent cannot supply them, the claim is
reclassified as **HYPOTHESIS / NON-BLOCKING** and removed from the DoD.
An invented step can be investigated separately, but must not hijack the
original work. Acceptance remains tied to the user's requested capability.

## Application hierarchy

1. **FCIS:** This text and its Governance edition establish the rule.
2. **Organization:** `Fountain-Coach/.github` declares inheritance and
   review criteria. Organization defaults are not automatically read by every
   execution environment, so downstream files MUST explicitly point here.
3. **Repository:** Each root `AGENTS.md`, project instructions and acceptance
   guides must import the rule and may add narrow, genuinely applicable
   domain-specific invariants; they must not weaken or reinterpret it as a
   blanket requirement to expand scope.
4. **Directory:** Nested `AGENTS.md`, skills, scenario runners and DoD
   templates must apply the same four-question gate at execution time.
5. **Runtime:** Existing typed contracts and live authority still decide
   what the system can do. Prose never overrides a tested runtime fact.

If any local instruction would create a speculative blocker, the agent must
interpret it in light of this founding rule, preserve any actual invariant,
and separate unrelated future work. No new software subsystem is required
merely to enforce this conduct standard.

## Failure pattern that motivated this rule

In Reframe R38, an accepted physical iPad-to-Codex conversation was repeatedly
reframed into replacement-host recovery and new owner-enrollment requirements.
The agent then wrote code, generated tests and used those tests to legitimize
the expanded scope. The tests were real; the claimed necessity was not.
This is **goal substitution → speculative prerequisite → implementation →
test-based legitimization → new dependency → moving DoD**. FCIS rejects the
entire loop, not only inaccurate success claims.

**Default operating maxim:** *Do not invent the problem to justify the solution.*
