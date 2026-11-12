# FCIS — Model Provider and Execution Boundary

**Status:** Adopted FCIS-MODEL-1 interpretation; runtime interoperability not implied
**Source:** [RFC 0001 v1.5.0](../profile/README.md) and [FCIS Name and Identity](FCIS-Name-and-Identity.md)
**Authority:** Fountain Coach governs its instructions, not independent model infrastructures.

## Ownership and separation

The **Fountain Coach Instruction System (FCIS)** governs the authored behavioral law, plans, canonical Skills and their versioned projections, plus contracts for discovering external capabilities. It does **not** own a foundation model, an inference service, the model provider's execution infrastructure, the vendor's SDK/API, or its subscription entitlements. Third-party model service terms remain independent of FCIS rights, releases, and tool admission.

An agent executing a Fountain Coach task has separate concerns: the source-governed **task and policy**; an explicitly selected and authorized **reasoning provider** when inference is required; a supported **adapter** that connects the task to that provider; and an independently permitted, typed **capability/tool execution** with its own receipt. Tool availability does not prove model entitlement. Model availability does not grant tool or FCIS-KIT execution authority.

A deterministic, admitted tool operation must not be forced through a paid model turn solely because a particular chat client can call the tool. A task requiring inference must not be passed off as provider-free execution. Preserve consent, model selection, quota/budget truth, refusal and terminal evidence separately.

## Distribution and provider adapters

- **Canonical Skill source:** `Fountain-Coach/.github/.codex/skills/`, as required by Governance Chapter 160. The legacy `.codex` path is a Git source identity and does not give Codex a privileged semantic role.
- **Derived distributions:** `.codex/skills`, `.claude/skills`, the reviewed GitHub-backed ChatGPT marketplace plugin, and any other explicitly admitted discovery surface are adapters or projections, not independent sources.
- **Optional reasoning clients:** OpenAI Codex, ChatGPT, third-party cloud models, and local models are possible implementation choices, not an FCIS capability guarantee. A new runtime is supported only after its exact technical requirements and effective invocation are verified.
- **Execution effects:** The owning runtime/Kit, MCP service, or approved host operation owns permission checks, scopes, lifecycle and terminal receipts. A model response cannot replace such evidence.

## Migration and verification boundary

This FCIS v1.5.0 clarification changes **governance semantics**, not the behavior or name of an existing integration. In particular, existing repositories and contracts mentioning Codex (for example `Fountain-Coach/FountainCodexLaneKit` and the `midi2-gpu-fabric` CodexKit or authentication surfaces) are **candidates for a separate source and runtime audit**, not evidence that vendor-independent model selection has been implemented. Provider-labeled source files or historical records must not be globally rewritten: identify whether each occurrence is an integration name, an actual technical dependency, a historical artifact, or a misplaced normative requirement.

For any runtime migration, first inspect the implementation and its active plan. Locate the selection and identity of the reasoning lane, the provider adapter interface and authentication, the task/capability boundary, provider-specific budget and failure behavior, and a reproducible successful path. Then change the *smallest proved dependency*. Verify the old supported provider still works and the new provider only where independently demonstrated. Do not assume ChatGPT subscriptions grant API access, make model sessions unlimited, or bypass model-provider licensing or payment.

## Acceptance distinction

**Proved by a documentation release:** RFC 0001 no longer mandates Codex, the model boundary is explicit, and provider-specific discovery paths are treated as derived. **Not proved:** that Reframe, Fountain Host, existing Copilot adapters, external model APIs, or independently hosted models already interoperate; that all Codex-named runtime components may be renamed safely; or that production deployments inherited this document. Such outcomes require separate source and live runtime evidence.
