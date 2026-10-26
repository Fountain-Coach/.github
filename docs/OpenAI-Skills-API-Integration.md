# Fountain Coach — OpenAI Skills API integration

**Status:** organization-owned interoperability contract; API publication not yet performed.
**Owner and sole canonical skill source:** `Fountain-Coach/.github`, including `.codex/skills/<name>/`, the catalog, digest checks, policy, and review history.
**Domain repositories:** derived Codex/Claude and runtime-specific projections; historical origin commits are provenance, not independent skill authorship.
**Authority:** [FCIS RFC 0001](../profile/README.md) and [Goal Fidelity and Non-Invention](FCIS-Non-Invention-and-Goal-Fidelity.md).

## The two different OpenAI surfaces

1. **Supported public API:** OpenAI documents `https://api.openai.com/v1/skills` for uploading, listing, retrieving, versioning, and selecting a default skill version. Documentation: https://developers.openai.com/api/docs/guides/tools-skills and https://developers.openai.com/api/reference/python/resources/skills . Hosted Responses API shells reference uploaded skills by ID and optional version; local shell and Agents API sandbox discovery use different mechanisms.
2. **ChatGPT account Skills:** `https://chatgpt.com/skills` is a user/workspace installation and discovery surface. An account's Git-backed Skills endpoint and its observed push behavior are **not** the published OpenAI API contract. In particular, do not infer that an API skill upload installs anything into ChatGPT Skills, or that a Git-backed account push creates an API skill. Verify each independently.

Do not put API keys, tokens, credentials, session cookies or account-specific endpoint authentication in Git. The user or runtime supplies credentials through its own protected configuration. This repository owns the *contract*, not an OpenAI-hosted account or an OpenAI token.

## FCIS ownership and execution

| FCIS layer | Responsibility |
| --- | --- |
| `AGENTS.md` and organization standards | Scope, prohibitions and review constraints |
| Organization `PLANS.md` and the selected destination's scoped plan | Requested skill, canonical source revision, destination, validation, acceptance and rollback |
| Canonical `.github/.codex/skills/<name>/SKILL.md` | Authoring, packaging, validation, targeted publish and verification procedure |
| External API / connector | Authenticated access to OpenAI or ChatGPT services; no policy and no independent source authority |

The organization repo owns **both** the canonical skill packages in `.codex/skills` and the desired distribution declarations in `skills/openai-distribution.json`. Each entry pins its canonical path and complete source file-tree SHA-256. The catalog is not a substitute for the skill payload; external receipts record source commit, package SHA-256, returned API skill ID/version and separate ChatGPT account readback. Copies are never promoted to source by being observed. These are never inferred from names or locally passing tests.

## Targeted deployment contract

1. Resolve the skill's *organization-owned* Git source under `Fountain-Coach/.github/.codex/skills`, recorded commit, digest and complete package. Read that repository's `AGENTS.md` and `PLANS.md` as well as the domain Kit contracts where execution semantics matter. Check one `SKILL.md`, `name`/`description` frontmatter and required `agents/openai.yaml`. Run Skill Creator validation where accessible and organization-specific tests. Package validation is not FCIS or live destination acceptance.
2. Compare the source package hash and available destination readback. Never reconcile by overwriting the entire destination catalog. Do not delete, retire or change unrelated packages just because they are undeclared or have drift.
3. For the public Skills API, perform at most one named skill create or version upload per authorized operation. Capture returned `skill_id`, version and default-version state, read back the exact new version (allow a bounded retry for transient `404` after upload), and verify the payload and intended version pointer. Do not change the default version without an explicitly scoped promotion.
4. For ChatGPT Skills, use only an authorized, supported installation workflow. If using an account-specific Git-backed adapter, distinguish its capabilities and errors from the public OpenAI API, preserve existing account packages, and verify the exact account/workspace installation by independent readback. Observed `HTTP 422` for an aggregate push does not authorize repeated aggregate retries.
5. Report `PROVEN`, `DOCUMENTED`, `INFERRED`, `PROPOSED`, or `BLOCKED` separately for each destination. No success claim without destination readback. Record the previous version for rollback; roll back only the selected package, without bulk reset.

## UX and initial intended selection

The workspace's useful author-facing selection begins with **Teatro Scenario Composer**, **Linotype Estate Template**, and **FCIS Skill Authoring and Sync** (the FCIS/OpenAI Skill Creator integration). Keep their identities distinct and complementary. This is the desired-state declaration, **not** a claim that all three are currently and persistently installed at `chatgpt.com/skills`. Other installed user skills remain untouched. Do not promise grouping, ordering or workspace UI customization that OpenAI's interface has not demonstrated.

The first public API acceptance must demonstrate **one explicitly approved**, source-pinned upload (if an authorized API credential and project are available), followed by version-content and default-pointer readback. ChatGPT account Skills must be inspected independently. Absent credentials prevent only the remote proof. No code should silently publish on git push; no GitHub Actions automation is required.

## Chapter 160 ownership and evidence

Published Chapter 160 declares `Fountain-Coach/.github` as the sole authority over the agent skill packages. Individual domain repository copies and ChatGPT/OpenAI installations are derived. Their changes can return as observations or proposals, never become source automatically. Historical import commits are retained as provenance. The 26 October 2026 [ChatGPT Skills file-level audit](Skill-Distribution-Audit-2026-10-26.md) records two matching installed file inventories and one observed FCIS skill metadata drift; these observations do not establish an active-version pointer or public API upload.

Execute python3 skills/skillctl.py check; then python3 -m unittest discover -s skills/tests -v. To create a deterministic ZIP, use python3 skills/skillctl.py package --skill teatro-scenario-composer --output /tmp/skill.zip. To compare an independently obtained exported package, use python3 skills/skillctl.py compare --skill teatro-scenario-composer --zip /tmp/observed.zip. Without readback, report remains UNVERIFIED. Optional local hooks: git config core.hooksPath .githooks. They do not control remote mutations or prevent administrators from changing ChatGPT installations.
