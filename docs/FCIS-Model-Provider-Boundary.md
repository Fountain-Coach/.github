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

## Business independence before marketplace expansion — owner priority P0

**Accepted owner decision, 24 November 2026.** Fountain Coach's commercial
value is its independently operable, customer-respecting FCIS technology,
rather than ChatGPT plugin placement. The business must not delegate its
authoritative customer identity, customer work, capability grants, durable
receipts, administration or recoverability to an agent marketplace.
ChatGPT/OpenAI and other reasoning/marketplace services are optional clients
and adapters governed by their providers, not Fountain Coach's permission
authority. Git-hosted canonical source remains reviewed and recoverable; a
live FCIS operation must not require GitHub availability or a model subscription.

**Observed distribution limitation:** the single FCIS-GO 0.1.40 ChatGPT
marketplace plugin was published with one Skill and read back independently.
The account's browser and iPadOS plugin lists nevertheless differ; Plugin
Management's catalog and permission APIs disagree for the same plugin identities
and do not expose a reliable cross-device installation actor audit. This is
an unresolved **provider administration and provenance** question, not proof
of an unauthorized grant or a broken FCIS runtime. Preserving the working
plugin while independently proving owned operation is the bounded remedy.

**First business release gate:** reuse the current standalone Go/Access/native
FountainStore/software Host contracts and any verified implementations.
Demonstrate an actual owner-controlled browser/client, without ChatGPT login
or plugin, that can (1) authenticate the owner and inspect effective access,
(2) discover one admitted, versioned bounded capability, (3) execute it
under an explicitly authorized grant with a durable independent receipt,
(4) observe refusal after revocation or an absent grant, and (5) recover
verified owner-owned state from a known accepted snapshot/release. Inspect
existing evidence first and implement only the observed gaps. A new identity
or host subsystem is not an implied prerequisite; customer registration,
multi-tenancy and paid inference/payment are separate, later scopes.

**Distribution stance:** retain existing single-Skill FCIS-GO as an optional
maintained marketplace adapter (and nine historical canonical Skills in
maintenance). Do not expand marketplace/runtime capabilities to mask a
provider-admin inconsistency. Keep model choice and model-provider spend
outside the deterministic owner execution gate. Closure requires live
owner-facing use and independent issuer/Host/Store evidence, never a source
document, test harness or ChatGPT catalog screenshot alone.

## FCIS-BYOM — Bring Your Own Model (pinned product concept)

**Reference label:** `FCIS-BYOM` — **Bring Your Own Model**. **Status:** proposed customer-access and commercial delivery pattern, **not** an implemented customer product or a new normative runtime requirement. The word *own* identifies the customer's choice and responsibility for an independently licensed model service or an actually controlled local model; it does **not** imply ownership of third-party foundation-model weights, APIs, or infrastructure.

**Concept:** A customer signs in to a Fountain Coach-owned authorization authority and receives narrowly scoped access to FCIS-governed Skills and capabilities of an admitted Fountain Host. Independently, the customer uses a permitted model/provider connection (for example, their eligible ChatGPT account, OpenAI or Anthropic API subscription/credentials, or an admitted local model). Fountain Coach supplies identity, consent, capability admission, bounded host execution and independently verifiable results; the reasoning provider supplies inference. Login to Fountain Coach is not login to an AI provider, and a provider's model response never authorizes host effects.

**Commercial hypothesis:** Fountain Coach may charge for access to authorized capabilities, hosted execution or managed services, without automatically paying for customer inference. For a genuinely customer-funded provider call, costs and entitlements remain with that customer's provider agreement. A separate Fountain Coach-funded inference offering is a different, explicitly metered and consented commercial lane; never silently substitute it or pass provider charges to the customer without authorization.

**Required truth at execution:** Explicit provider and model selection when inference is needed; verifiable provider eligibility and permission for the intended app; transparent customer/provider spend responsibility, rate/budget limits and refusal; scoped OAuth/resource grants; isolation among customer identities and resources; typed execution receipts; effective revocation. A ChatGPT subscription must never be assumed to permit third-party API access or unrestricted commercial resale. Do not require a paid model call for a separately admitted deterministic host operation.

**Current boundary (13 November 2026):** Owner passkey registration and returning-owner login have been witnessed, and authenticated `host.describe` has succeeded through the existing Host client connection. Fountain Press Access has an issuer-session integration in production, with owner authenticated-inventory acceptance still outstanding. Customer self-registration, multi-customer authorization isolation in the live service, subscription/payment entitlements, provider adapters and billing/meters for customers, and a complete BYOM customer execution are **not** accepted. The existing Reframe ChatGPT-plan inference attempt was previously blocked; do not infer that this concept unblocks it.

**Smallest demonstrator, when separately authorized:** one customer identity, one service entitlement, one bounded resource grant, one permitted customer-funded inference path when needed, one executed capability with issuer/Host evidence, and a proved denied operation after revocation. This is a proposed acceptance scenario, not a demand to build a new identity database, another issuer, or a general-purpose chatbot.

## Migration and verification boundary

This FCIS v1.5.0 clarification changes **governance semantics**, not the behavior or name of an existing integration. In particular, existing repositories and contracts mentioning Codex (for example `Fountain-Coach/FountainCodexLaneKit` and the `midi2-gpu-fabric` CodexKit or authentication surfaces) are **candidates for a separate source and runtime audit**, not evidence that vendor-independent model selection has been implemented. Provider-labeled source files or historical records must not be globally rewritten: identify whether each occurrence is an integration name, an actual technical dependency, a historical artifact, or a misplaced normative requirement.

For any runtime migration, first inspect the implementation and its active plan. Locate the selection and identity of the reasoning lane, the provider adapter interface and authentication, the task/capability boundary, provider-specific budget and failure behavior, and a reproducible successful path. Then change the *smallest proved dependency*. Verify the old supported provider still works and the new provider only where independently demonstrated. Do not assume ChatGPT subscriptions grant API access, make model sessions unlimited, or bypass model-provider licensing or payment.

## Acceptance distinction

**Proved by a documentation release:** RFC 0001 no longer mandates Codex, the model boundary is explicit, and provider-specific discovery paths are treated as derived. **Not proved:** that Reframe, Fountain Host, existing Copilot adapters, external model APIs, or independently hosted models already interoperate; that all Codex-named runtime components may be renamed safely; or that production deployments inherited this document. Such outcomes require separate source and live runtime evidence.
