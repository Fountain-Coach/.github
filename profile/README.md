# Fountain Codex Instruction System (FCIS)
## RFC 0001 — Orthogonal Instruction Architecture for LLM-Governed Repositories

**Status:** Adopted  
**Category:** Standards Track  
**Organization:** fountain.coach  
**Applies to:** All Codex-operated repositories  
**Version:** 1.0.0

---

## Abstract

This document defines the **Fountain Codex Instruction System (FCIS)**, a normative, organization-wide standard for governing how OpenAI Codex is instructed, constrained, and enabled across repositories.

FCIS establishes **four orthogonal instruction layers**:

1. `AGENTS.md` — behavioral law  
2. `PLANS.md` — intent and execution reasoning  
3. Skills (`SKILL.md`) — reusable execution techniques  
4. MCP servers — external capabilities and data access  

Strict separation of these layers is required to ensure **predictability, auditability, and scalability** of LLM-driven development.

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

`AGENTS.md` **MUST** define non-negotiable behavioral constraints under which Codex
operates in a repository.

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
Codex **SHALL NOT** execute qualifying tasks without a plan.

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

```
repo-root/
  AGENTS.md
  PLANS.md
  .codex/
    skills/
      <skill-name>/
        SKILL.md
```

User-level configuration:
```
~/.codex/config.toml
~/.codex/AGENTS.override.md
```

---

## 10. Compliance

A repository is FCIS-compliant if:
- all applicable layers are present
- responsibilities are orthogonal
- plans exist for complex work
- skills are modular and declarative

---

## 11. Rationale

FCIS treats Codex as a **compiler-like system**:
- law → intent → execution → capability
This mirrors successful separation patterns from compilers, operating systems, and safety-critical automation.

---

## 12. Security Considerations

Non-orthogonal instruction systems increase:
- unintended behavior
- silent policy drift
- non-reproducible execution

FCIS reduces these risks through explicit separation and review.

---

## 13. Versioning

- RFC 0001 defines FCIS v1.0.0
- Backward-incompatible changes require a new RFC

---

## 14. Summary

FCIS establishes a **contractual architecture** for Codex:

- `AGENTS.md` defines law
- `PLANS.md` defines intent
- Skills define execution
- MCP defines capability

Adherence is mandatory for all fountain.coach Codex repositories.
