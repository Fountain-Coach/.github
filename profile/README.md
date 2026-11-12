# Fountain Coach Instruction System (FCIS)
## RFC 0001 — Orthogonal Instruction Architecture for LLM-Governed Repositories

**Status:** Adopted  
**Category:** Standards Track  
**Organization:** fountain.coach  
**Applies to:** Fountain Coach-governed repositories and supported agent runtimes
**Version:** 1.5.0

---

## Abstract

This document defines the **Fountain Coach Instruction System (FCIS)**, a normative, organization-wide standard for governing instructions, plans, Skills, and tool-capability access across supported agent runtimes. It does not own or require a particular model provider.

FCIS establishes **four orthogonal instruction layers**:

1. `AGENTS.md` — behavioral law  
2. `PLANS.md` — intent and execution reasoning  
3. Skills (`SKILL.md`) — reusable execution techniques  
4. MCP servers — external capabilities and data access  

Strict separation of these layers is required to ensure **predictability, auditability, and scalability** of LLM-driven development.

**Name and ownership:** FCIS expands to **Fountain Coach Instruction System**. Fountain Coach governs its instruction contracts and source artifacts; an LLM or agent vendor owns its own models and service. Codex, when used, is an optional integration, not FCIS identity, authority, or a mandatory runtime. See [FCIS Name and Identity](../docs/FCIS-Name-and-Identity.md) and [Model Provider and Execution Boundary](../docs/FCIS-Model-Provider-Boundary.md).

---

## Compliance & Policies

- FCIS Apple Intelligence Compliance Specification (Preflight): [FCIS-AIC-Preflight-RFC](../docs/FCIS-AIC-Preflight-RFC.md)
- FCIS Accessibility Standard: [FCIS-AX-Standard](../docs/FCIS-AX-Standard.md)
- FCIS Visual Regression Testing Standard: [FCIS-VRT-Standard](../docs/FCIS-VRT-Standard.md)
- Security policy: [SECURITY](../.github/SECURITY.md)
- Publication and source policy: [FCIS Publication and Source Policy](../docs/FCIS-Publication-and-Source-Policy.md)
- Governance: [GOVERNANCE](../.github/GOVERNANCE.md)
- Contributing: [CONTRIBUTING](../.github/CONTRIBUTING.md)
- Code of Conduct: [CODE_OF_CONDUCT](../.github/CODE_OF_CONDUCT.md)

### Adopted external interoperability standards

- **OPDS Catalog 2.0 — adopted for digital publication catalog interoperability.** [Fountain Coach adoption and local publication profile](../docs/adopted-external-standards/OPDS-2.0.md) · [upstream specification](https://specs.opds.io/opds-2.0). OPDS is maintained by the upstream community; Fountain Coach owns only its adoption policy and its implementation in Fountain Press. This adoption is alongside, not under, the four FCIS instruction layers. It does not change RFC 0001 or the FCIS suite version.

---

## 1. Terminology and Conventions

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in RFC 2119.

---

## 2. Design Principle: Orthogonality

### 2.1 Definition

Within FCIS, *orthogonality* means:

> Instruction layers are **independent dimensions of responsibility**, such that
> modifying one layer does not redefine, weaken, or invalidate the others.

Orthogonality is a **hard requirement**, not a stylistic preference.

### 2.2 Motivation

LLM-based systems degrade rapidly when:
- responsibilities overlap
- priorities are implicit
- instructions conflict probabilistically

Orthogonality prevents these failure modes by making responsibility **explicit,
exclusive, and reviewable**.

### 2.3 Model and Runtime Independence (FCIS-MODEL-1)

FCIS is a **Fountain Coach-governed instruction and capability contract**, not a model service, inference engine,
provider subscription, or ownership claim over model weights. The four layers MUST remain meaningful regardless of
which eligible human, local model, hosted model, or agent runtime executes an admitted task.

- **Separate authorities:** Fountain Coach owns and reviews its authored policies, plans, canonical Skills, and
  FCIS capability contracts. Each model or agent provider retains its own service, model, authentication,
  availability, licensing, quota, and billing boundaries. FCIS MUST NOT claim ownership or control of that
  provider infrastructure merely because an adapter or Skill uses it.
- **Provider-neutral requirements:** An FCIS MUST, SHALL, or compliance rule MUST NOT require Codex, OpenAI,
  ChatGPT, Claude, or any named model/agent provider unless an *explicitly scoped integration contract* actually
  depends on that provider. A provider-specific adapter MAY impose its own verified technical prerequisites
  without widening the organization-wide FCIS standard.
- **Admitted reasoning:** When a task requires inference, the chosen provider/model/runtime MUST be explicitly
  available and authorized under its actual access, consent, security, price, and budget terms. Provider
  substitution is not automatic proof of equivalent capability, quality, or entitlements.
- **Independent tools and source:** Git-owned instruction source and separately admitted deterministic tool
  execution MUST NOT acquire a compulsory paid model dependency merely through an FCIS integration. Model
  selection does not change the owning Kit's capability permission or terminal-evidence requirements.
- **Portable projections, not fabricated support:** Provider-specific discovery directories and adapters are
  derived surfaces of their governing source. Their presence proves neither a running model nor compatibility
  with another runtime. Support for an additional runtime requires explicit adapter and acceptance evidence.

These rules preserve the original four instruction layers and the independent FCIS-MCP-2 execution boundary.

---

## 3. Instruction Layers (Normative)

Each instruction layer answers **exactly one question**.

| Layer | Question |
|------|----------|
| `AGENTS.md` | What is allowed or forbidden? |
| `PLANS.md` | What is intended and why? |
| Skills | How is a task executed? |
| MCP | What capabilities are available? |

No layer MAY answer another layer’s question.

---

## 4. AGENTS.md — Behavioral Law

### 4.1 Purpose

`AGENTS.md` **MUST** define non-negotiable behavioral constraints for the supported
actors and agent runtimes operating in a governed repository.

### 4.2 Mandatory Content

`AGENTS.md` **MUST** include:
- invariants and prohibitions
- safety and review requirements
- routing rules for PLANS.md and skills

### 4.3 Prohibited Content

`AGENTS.md` **MUST NOT**:
- contain step-by-step procedures
- include tool configuration details
- encode execution workflows

Violation constitutes a **law breach**.

---

## 5. PLANS.md — Intent and Reasoning Layer

### 5.1 Purpose

`PLANS.md` **MUST** capture the intent, structure, and risk management of multi-step work.

### 5.2 Invocation Rule

`AGENTS.md` **MUST** define when PLANS.md is required.
An executing agent **SHALL NOT** undertake qualifying tasks without a plan.

### 5.3 Required Structure

A plan **SHOULD** include:
- goal
- constraints
- phased approach
- test plan
- rollback plan
- definition of done

---

## 6. Skills — Execution Technique Modules

### 6.1 Definition

A skill **MUST**:
- exist in its own directory
- contain exactly one `SKILL.md`

### 6.2 Responsibilities

A skill **MUST** define:
- when it applies
- ordered execution steps
- output guarantees

### 6.3 Constraints

Skills **MUST NOT**:
- redefine behavioral law
- replace PLANS.md for complex work
- configure MCP servers

---

## 7. MCP Servers — Capability Layer

### 7.1 Role

MCP servers **MUST** provide access to external tools or data only.

They **MUST NOT**:
- encode workflow logic
- enforce policy
- substitute for skills

### 7.2 Configuration

MCP configuration **MUST** occur outside repositories.
Repositories **MUST NOT** rely on MCP presence for correctness.

### 7.3 Provider-Independent Capability Access (FCIS-MCP-2)

A capability and the reasoning provider that may choose to use it are separate authorities. A fully specified, admitted
computer, filesystem, process, service, or MCP operation **MAY** be invoked without an LLM session when its own
executable contract does not require inference. A tool provider's access or payment terms do not constitute an
LLM provider's model entitlement.

- **Independent availability:** Implementations **MUST** distinguish tool reachability, authorization, execution
  admission, and terminal evidence from model availability, credentials, usage quotas, and billing. A model quota
  refusal **MUST NOT** be presented as evidence that an independently reachable tool is unavailable.
- **No artificial paid dependency:** An FCIS consumer **MUST NOT** require an OpenAI, Codex, or other paid reasoning
  session solely to invoke an already admitted, fully specified external operation when a provider-independent
  execution path is available. It **MUST NOT** substitute an unapproved chargeable reasoning call for a deterministic
  tool operation. This rule does not manufacture a direct path where none has been implemented and proven.
- **Reasoning is a separate operation:** If the request needs interpretation, argument synthesis, or agentic tool
  selection, the actual reasoning lane **MUST** be admitted and elected under the existing provider, consent, cost,
  and budget contract. The absence of a usable reasoning lane **MUST** yield a truthful, typed refusal; it
  **MUST NOT** silently cause paid fallback or invented command arguments.
- **Existing execution authority remains binding:** An MCP connection or tool advertisement is discovery, not
  permission, execution admission, or success. For FCIS-KIT capabilities the owning kit **MUST** enforce
  FCIS-KIT-14/15 mechanical constraints, scoped authorization, lifecycle, refusal, and terminal evidence. An MCP
  client, host adapter, or model **MUST NOT** become a parallel executor or bypass the owning kit. MCP servers
  still enforce their own transport security and service-side access controls; this does not transfer FCIS
  execution policy to the server.
- **Cost truth:** Costs, quotas, and entitlements for the tool service and the model service **MUST** be
  represented separately, to the extent known. Unlimited or prepaid tool calls **MUST NOT** be described as
  unlimited model inference. Unknown pricing or runtime availability **MUST** remain unknown rather than
  presented as free, unlimited, or admitted.

This is an additive clarification of the existing MCP capability layer, not a fifth FCIS layer, a mandatory MCP
dependency, a new agent runtime, or permission to bypass existing owner-controlled operations. A consumer
**MUST NOT** claim provider-free execution merely because a server is configured: it needs an accepted tool call
and the required independent outcome evidence.

---

## 8. Orthogonality Violations (Non-Exhaustive)

The following are **spec violations**:

- procedures in `AGENTS.md`
- behavioral rules in skills
- workflow logic in MCP
- unplanned long-running tasks
- duplicated responsibility across layers

Violations **SHOULD** block merges.

---

## 9. Standard Repository Layout

The canonical organization-owned Skill source is `Fountain-Coach/.github/.codex/skills/` under
Governance Chapter 160. The `.codex` directory name is a retained **repository and distribution path**, not a
model or provider requirement. A participating repository declares its behavioral and planning layers:

```
repo-root/
  AGENTS.md
  PLANS.md
```

An admitted runtime MAY require a discoverable Skill projection in its own path (for example,
`.codex/skills/` for Codex or `.claude/skills/` for Claude Code). Such paths are **derived adapters** and
MUST NOT become competing canonical Skill sources. User-level configuration (for example,
`~/.codex/config.toml`) is adapter-specific and is never a general FCIS compliance prerequisite.

---

## 10. Compliance

A repository is FCIS-compliant if:
- all applicable layers are present
- responsibilities are orthogonal
- plans exist for complex work
- skills are modular and declarative

---

## 11. Rationale

FCIS uses a **compiler-like separation of responsibilities** across agent runtimes:
- law → intent → execution → capability
This mirrors successful patterns from compilers, operating systems, and safety-critical automation.
It does not mandate a particular model or inference vendor.

---

## 12. Security Considerations

Non-orthogonal instruction systems increase:
- unintended behavior
- silent policy drift
- non-reproducible execution

FCIS reduces these risks through explicit separation and review.

## 12.1 FCIS-KIT Instrument Store

FCIS-KIT extends the FCIS architecture from repository governance to governed capability distribution. An instrument
is a bounded capability that presents a typed MIDI2 surface, declares its permissions and execution lane, reports its
lifecycle, and carries the evidence needed for admission. Reframe remains the host authority; a supported agent or model may help build or
compose an instrument, but it does not decide admission or release.

The FCIS-KIT standard's [FCIS-KIT-14 mechanical constraint](../docs/FCIS-KIT-Standard.md#fcis-kit-14-mechanical-constraints)
is the binding form of that boundary: a typed executable predicate, named evaluator, bounded refusal state, and
terminal evidence requirement. It prevents an agent or runtime path from inventing or bypassing authority by ceremony.

The current milestone is the governed architecture and capability-plane contract. It is not a claim that a public
instrument marketplace, every proposed instrument, or every local/remote runtime already exists.

Read the detailed authority: [Chapter 91 — The FCIS-KIT Instrument Store Is the Capability Plane](https://governance.fountain.coach/chapters/91-fcis-kit-instrument-store-is-the-capability-plane/).
Read the repository declaration that materializes this relation: [FCIS_KIT_DECLARATION.md](https://github.com/Fountain-Coach/midi2-gpu-fabric/blob/main/FCIS_KIT_DECLARATION.md).

The organisation RFC above remains the normative FCIS layer model: `AGENTS.md` defines law, `PLANS.md` defines intent,
Skills define execution technique, and MCP provides capabilities. Chapter 91 applies that separation to instrument
construction and admission; it does not create a fifth instruction layer.

---

## 13. Versioning

FCIS uses semantic versioning for the standards suite. RFC 0001 defines the FCIS **architecture** (the four orthogonal layers); the suite version tracks the normative standards adopted on top of it.

- **MINOR** bump: a new additive standards-track document is adopted; the architecture and existing requirements are unchanged.
- **MAJOR** bump (**new RFC**): any backward-incompatible change to the FCIS architecture — the four-layer contract — requires a new RFC.

### Version history

- **v1.5.0** — Adopts **FCIS-MODEL-1 Model and Runtime Independence** and clarifies provider-neutral obligations, derived Skill paths, and external model-service ownership. The four-layer architecture is unchanged.
- **v1.4.0** — Adds **FCIS-MCP-2 Provider-Independent Capability Access**: separately admitted deterministic tools may be invoked without compulsory model turns, while reasoning, authorization, cost, and FCIS-KIT execution authority remain independently governed. Additive; the four-layer model is unchanged.
- **v1.3.0** — Adopts **FCIS-KIT-16 History-First Reconstruction**, requiring an evidence-backed reconstruction of
  the existing authority, proof, failure seam, reuse decision, and bounded acceptance before capability changes.
  Additive; RFC 0001 architecture unchanged.
- **v1.1.0** — Adopts the **FCIS-AX Standard** (accessibility as the machine-readable UI layer; every view, including custom-drawn views, exposes its content to the accessibility tree; agents and verification drive the AX tree, not pixels). Additive; RFC 0001 architecture unchanged.
- **v1.0.0** — RFC 0001 establishes the FCIS four-layer architecture (`AGENTS.md` / `PLANS.md` / Skills / MCP), alongside the FCIS-AIC-Preflight and FCIS-VRT standards.

---

## 14. Summary

FCIS establishes a **provider-independent contractual architecture** for supported agent runtimes:

- `AGENTS.md` defines law
- `PLANS.md` defines intent
- Skills define execution
- MCP defines capability

Adherence is mandatory for Fountain Coach repositories that adopt the FCIS standard, independent of their elected model provider.
