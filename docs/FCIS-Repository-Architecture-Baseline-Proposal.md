# FCIS Repository Architecture Baseline Assessment

**Status:** Proposed  
**Category:** Informational proposal  
**Applies to:** Fountain Coach organization repositories, when a repository architecture baseline is requested  
**Authority:** Subordinate to RFC 0001 of the Fountain Codex Instruction System (FCIS)  
**Version:** 0.1.0 (proposal)

---

## 1. Purpose

This proposal defines a reusable baseline analysis for understanding how a repository represents and executes multi-step work. It is intended to be run once per repository, with the same abstract questions asked of each repository and the findings expressed using that repository's actual terms.

The analysis maps existing architecture. It does not prescribe a target architecture, declare a repository compliant or non-compliant, or authorize implementation changes. Its purpose is to establish an evidence-backed starting point for later design and implementation decisions.

The baseline focuses on how a system:

- represents an objective and its completion condition;
- selects and advances units of work;
- persists state and resumes after interruption;
- coordinates tools, models, services, and processes;
- records and evaluates evidence;
- enforces lifecycle, budget, retry, and stop conditions; and
- keeps execution authority under the control of the repository's intended owner.

## 2. Position relative to FCIS

RFC 0001 defines the FCIS architecture as four orthogonal instruction layers:

1. `AGENTS.md` defines behavioral law.
2. `PLANS.md` defines intent and execution reasoning.
3. Skills define reusable execution techniques.
4. Model Context Protocol servers provide external capabilities and data access.

This assessment adds no instruction layer and changes no responsibility in RFC 0001. It is an analysis method and a record of observed repository architecture. Its reusable audit prompt may be maintained as an organization-level document; a repository-specific procedure for running the analysis belongs in the appropriate skill or repository workflow.

This proposal is informational and non-binding. It does not change the adopted FCIS suite or its version. If the organization later adopts a normative requirement to perform these baselines, that requirement should be added through the FCIS standards process. Under the existing version policy, an additive standard that leaves RFC 0001's four-layer architecture unchanged would be a minor suite-version change; changing that architecture would require a new RFC and a major version.

## 3. Relationship to FCIS-KIT-16

FCIS-KIT-16 requires a history-first reconstruction before implementing, replacing, extracting, deprecating, or declaring an existing capability blocked. It defines the evidence that must be gathered for that decision and places the detailed procedure and verifier in the repository's skills layer.

The Repository Architecture Baseline is broader and less change-specific. It maps how a repository is structured and how multi-step execution, state, and evidence work at the time of analysis. It does not satisfy, replace, or waive FCIS-KIT-16 when that requirement applies. A baseline can help locate the relevant authority and evidence for a later history-first reconstruction.

## 4. Analysis principles

A baseline assessment should:

- use the repository's own names and concepts before proposing generalized labels;
- trace actual code paths and persisted state, rather than relying on names, comments, prompts, or documentation alone;
- separate observed facts, inferences, and unestablished claims;
- cite evidence with file paths, line ranges, call paths, or test names;
- state the commit or revision inspected and the date of analysis;
- identify uncertainty and missing evidence without filling gaps by assumption; and
- remain read-only.

Patterns such as durable workflows, state machines, checkpoint and resume, event-driven orchestration, separation of control from execution, replaceable adapters, and evidence-based completion are useful lenses. They are not required implementation choices.

## 5. Baseline assessment prompt

The following prompt is the reusable analysis instrument. Run it from the repository being assessed.

> Audit this repository to establish an evidence-backed baseline of its architecture for multi-step work that may be interrupted and needs a defensible completion condition.
>
> This is a read-only analysis. Do not edit files, run deployments, contact external services, or assume that a particular architecture or implementation is required. Discover the repository's own concepts and terminology, then map them to the concerns below.
>
> Trace the implementation from entry points through storage, orchestration, work execution, evidence, and terminal state. Inspect relevant APIs, command handlers, skills, plans, scenarios, queues, stores, model adapters, validators, and tests as applicable. Treat documentation and names as claims to verify against code paths and tests.
>
> Assess:
>
> 1. **Objective representation:** How an intended outcome and its completion condition are represented.
> 2. **State and authority:** Where objective and execution state live, how long they persist, and which component is authoritative.
> 3. **Work selection:** What determines the next unit of work and how work is sequenced.
> 4. **Orchestration:** What coordinates execution across tools, models, services, and processes, and what triggers continuation.
> 5. **Progress and recovery:** How progress is recorded and work resumes after interruption, failure, or process restart.
> 6. **Evidence and completion:** How outputs are checked and who or what can mark work complete, blocked, paused, failed, or cancelled.
> 7. **Limits and controls:** How budgets, retries, permissions, and stop conditions are represented and enforced.
> 8. **Replaceability:** Whether tools and model providers can be replaced without transferring canonical state or completion authority to them.
> 9. **Verification:** Which tests establish these behaviors, including interruption, incomplete work, duplicate execution, and terminal-state reporting.
>
> For each concern, classify the evidence as **implemented**, **partial**, **absent**, or **unclear**. Give precise file paths and line ranges, call paths, or test names. Separate observed facts from inferences. Do not infer behavior from prompt text or documentation alone.
>
> Return:
>
> - repository name, inspected revision, and analysis date;
> - a concise description of the current architecture using the repository's own vocabulary;
> - a control-flow and state-flow map using the actual component names;
> - a findings table with concern, classification, evidence, and confidence;
> - the strongest existing patterns and where they appear;
> - gaps or ambiguities affecting persistence, continuation, recovery, or trustworthy completion; and
> - unresolved questions that repository evidence cannot answer.
>
> Do not turn the baseline into a task-specific implementation proposal or a compliance verdict. Do not prescribe a database, scheduler, state-machine library, protocol, command name, or model provider. The goal is to establish what exists, how it behaves, and what remains unestablished.

## 6. Suggested baseline record

A repository-specific report may be stored alongside its architecture or audit records. It should identify the repository and revision assessed, analysis date, scope, findings, evidence, and unresolved questions. A baseline records an observed state; it does not itself establish implementation, compliance, release, or runtime acceptance.

---

**End of proposal**
