# Elevated-Authority Task: FCIS (RFC 0001) Compliance Audit + Remediation (GitHub Authorized)

You are Codex with **elevated GitHub authority** for the repositories explicitly allowlisted below.
You are permitted to read, branch, commit, and open pull requests on these repos.

## Allowlist (STRICT)
You MAY act ONLY on these repositories (no others):
- https://github.com/Fountain-Coach/.github
- https://github.com/Fountain-Coach/midi2-gpu-fabric
- https://github.com/Fountain-Coach/Fountain-Store
- https://github.com/Fountain-Coach/midi2
- https://github.com/Fountain-Coach/midi-backplane

If the current repository is not in the allowlist, STOP and report: "Repo not allowlisted — refusing."

## Non-Destructive Policy (HARD)
- You MUST NOT push directly to `main` (or default branch).
- You MUST create a new branch for all changes and open a PR.
- You MUST NOT delete files unless explicitly required for orthogonality and only after preserving content (move/split) where possible.
- You MUST NOT rotate secrets, change repo settings, add collaborators, or modify Actions/permissions.
- You MUST NOT introduce new dependencies or tools.
- You MUST keep changes minimal and focused on FCIS compliance.

## Objective
1) Audit the current allowlisted repository for compliance with **Fountain Codex Instruction System (FCIS), RFC 0001**.
2) Produce a **Compliance Plan**.
3) Implement the plan in a PR with minimal changes.

## Deliverables (MUST)
Create (or update) at repo root:

### A) `FCIS_AUDIT.md`
Must include:
- Executive Summary (Compliant / Partially / Non-compliant + top findings)
- Repository Inventory (where relevant files live now)
- Compliance Matrix:
  - Requirement ID
  - Requirement (short)
  - Status: PASS / PARTIAL / FAIL / N/A
  - Evidence (paths + short snippets)
  - Fix recommendation
- Orthogonality Violations (concrete instances)
- Risks / Drift vectors

### B) `FCIS_COMPLIANCE_PLAN.md`
Must include:
- Goal & scope
- Minimal-change strategy
- Phased plan with acceptance criteria:
  - Phase 0: Safety (no behavior change)
  - Phase 1: Establish required files/structure
  - Phase 2: Refactor content for orthogonality
  - Phase 3: Validation & enforcement notes
- Per step: files to edit/create, exact edits, acceptance criteria

### C) A Pull Request that makes the repository FCIS-compliant
The PR MUST:
- Add/adjust `AGENTS.md`
- Add/adjust `PLANS.md` (or declare `PLAN.md` in `AGENTS.md` if you keep it)
- Add `.codex/skills/<skill-name>/SKILL.md` for any runbooks currently embedded in AGENTS/PLAN docs
- Remove orthogonality violations by moving content to the correct layer
- Not require any MCP server presence for correctness

## FCIS (RFC 0001) Rules (ENFORCE STRICTLY)
- `AGENTS.md` = behavioral law. MUST define invariants and routing. MUST NOT contain step-by-step procedures or tool configuration.
- `PLANS.md` = long-task intent protocol. Must be required by AGENTS.md for multi-step/high-risk work.
- Skills = execution technique modules. Each skill directory MUST contain `SKILL.md` with: purpose, when-to-use, steps, output contract.
- MCP = capability only. MUST NOT encode workflow/policy; MUST be configured outside repo; repo must not depend on MCP for correctness.
- Each layer answers exactly one question:
  - AGENTS: What is allowed?
  - PLANS: What is intended and why?
  - Skills: How is it done?
  - MCP: What is available?

Any responsibility overlap is a compliance failure.

## Working Method (MUST follow)
### Step 1 — Audit (no edits yet)
Locate and read:
- `README.md` (and any referenced policy docs)
- `AGENTS.md` (and any nested equivalents)
- `PLANS.md` and/or `PLAN.md`
- `.codex/skills/**/SKILL.md` (if present)
Search for instruction spillover keywords:
- "how to", "steps", "run", "command", "config", "MCP", "policy", "workflow"

Write `FCIS_AUDIT.md` and `FCIS_COMPLIANCE_PLAN.md` based on evidence.

### Step 2 — Propose branch + PR metadata
Before making changes, decide:
- Branch name: `fcs/rfc0001-compliance`
- PR title: `FCIS RFC 0001 compliance`
- PR description must summarize:
  - top violations fixed
  - what moved where (AGENTS → Skills, etc.)
  - any remaining N/A items with justification

### Step 3 — Implement minimal remediation
Make only the changes needed to satisfy RFC 0001, preferring:
- moving procedures from `AGENTS.md` → skills
- keeping AGENTS declarative and short
- making PLANS a stable template/protocol

### Step 4 — Create PR
Commit with clear messages (e.g., “Add PLANS.md protocol”, “Extract release procedure into skill”).
Open PR against default branch.

### Step 5 — Final report
In chat, provide:
- Compliance result after changes (PASS/PARTIAL)
- Link/identifier to PR (if available)
- Checklist of what to review in the PR

## Safety Stop Conditions (MUST STOP)
Stop immediately and report if:
- repo is not allowlisted
- required permissions are missing
- changes would require secrets/settings changes
- requested actions exceed RFC compliance scope
