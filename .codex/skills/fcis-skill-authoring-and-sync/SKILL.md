---
name: fcis-skill-authoring-and-sync
description: Create or update skills governed by FCIS, then synchronize the selected repo-owned package to its declared agent surfaces. Use when authoring, auditing, reconciling, or distributing Codex skills across repository-local, Claude-mirror, or ChatGPT Skills storage.
---

# FCIS Skill Authoring and Sync

## Purpose

Use the OpenAI Skill Creator for skill-package design and validation while keeping FCIS authority, repository ownership, and distribution surfaces explicit.

## When to use

- Create, revise, validate, or reconcile a repository-owned skill.
- Compare a skill available through ChatGPT with its source in a Fountain Coach repository.
- Synchronize a selected skill to a repository-local agent mirror or to the account's ChatGPT Skills service.

## Procedure

1. **Resolve ownership and scope.** Read the owning repository's root `AGENTS.md`, applicable scoped instructions, current plan, and existing skill history. Identify the skill's stable name, owning repository, intended audience, required agent surfaces, and finite acceptance proof. Keep unrelated repositories and skills out of the change.

2. **Use FCIS as the repository authority.** Keep behavioral law in `AGENTS.md`, task intent and DoD in `PLANS.md`, reusable execution steps in a skill, and external access in MCP. For a repository-owned skill, keep the canonical package in that repository's `.codex/skills/<skill-name>/`. Give each skill directory exactly one `SKILL.md`; use adjacent `references/`, `scripts/`, `assets/`, or `agents/openai.yaml` only when they support that skill. Do not make a global ChatGPT Skills checkout the sole source for an FCIS-owned procedure.

3. **Apply the Skill Creator within that boundary.** Write a concise YAML frontmatter with only `name` and `description`. Make the description state the capability and concrete triggers. Use imperative steps, progressive disclosure, and deterministic scripts only where they remove repeated fragile work. Keep required FCIS sections and repository-specific authorities intact. Generate `agents/openai.yaml` when the agent interface needs it, and run the Skill Creator's `quick_validate.py`. That validator checks package shape; it does not establish FCIS compliance or prove the procedure works.

4. **Validate the procedure against the owner repository.** Check the skill's steps against its current `AGENTS.md`, standards, runtime contracts, and existing acceptance evidence. Add or update focused procedure validation only when the skill changes execution behavior. Do not create a new FCIS law, standard, DoD gate, runtime, or validation subsystem merely to accommodate the generic Skill Creator.

5. **Handle repository-local mirrors separately.** If the owner repository defines Codex-to-Claude synchronization, use its single-skill mode when available: check and synchronize only the named package, preserving unrelated drift and Claude-only packages. Do not run an all-skill rewrite to publish one package when other packages already drift. A passing targeted mirror check establishes only that repository-local mirror; it says nothing about the account's ChatGPT Skills service.

6. **Publish to ChatGPT Skills only when the user requests that surface.** Treat the account's ChatGPT Skills Git store as a distribution target, not as the authority for an FCIS-owned package. Copy the exact package and resources from the owning repository, retain source repository/commit provenance, and update one skill package per commit and push. The account service has rejected a multi-skill aggregate push with HTTP 422 and the response `invalid push content: aggregate skills push may modify only one skill`. This is a destination constraint, not an FCIS rule. Do not describe this account-level Skills store as the public OpenAI API or as an organization-wide skill registry.

7. **Verify each target independently.** After each commit or push, compare the target package with the owner source, inspect the target revision, and record the result. Report a surface as synchronized only when its exact source identity, contents, and commit are verified. Preserve and report failed syncs; do not claim that local validation installed or published a skill.

## Output contract

Report a mapping for each skill:

| Field | Required result |
| --- | --- |
| Skill identity | Stable directory name and intended audience |
| Source | Owning repository, path, and commit |
| ChatGPT Skills | Synced commit or explicit not-requested/blocked state |
| Repository mirror | Codex/Claude status and check result, when applicable |
| Validation | Skill Creator validation and owner-procedure evidence |
| Drift | Remaining differences, unsupported resources, or unknowns |

Separate verified synchronization from recommendation or inferred mapping. Stop after the requested surfaces are reconciled; do not imply an organization-wide sync from a single-skill result.
