# Fountain Coach — OpenAI Skills API integration

**Status:** organization-owned interoperability contract; API publication not yet performed.
**Owner:** `Fountain-Coach/.github` (policy, supported API mapping, catalog contract).
**Source owners:** the individual Fountain Coach Git repositories containing the canonical `.codex/skills/<name>/` packages.
**Authority:** [FCIS RFC 0001](../profile/README.md) and [Goal Fidelity and Non-Invention](FCIS-Non-Invention-and-Goal-Fidelity.md).

## The two different OpenAI surfaces

1. **Supported public API:** OpenAI documents `https://api.openai.com/v1/skills` for uploading, listing, retrieving, versioning, and selecting a default skill version. Documentation: https://developers.openai.com/api/docs/guides/tools-skills and https://developers.openai.com/api/reference/python/resources/skills . Hosted Responses API shells reference uploaded skills by ID and optional version; local shell and Agents API sandbox discovery use different mechanisms.
2. **ChatGPT account Skills:** `https://chatgpt.com/skills` is a user/workspace installation and discovery surface. An account's Git-backed Skills endpoint and its observed push behavior are **not** the published OpenAI API contract. In particular, do not infer that an API skill upload installs anything into ChatGPT Skills, or that a Git-backed account push creates an API skill. Verify each independently.

Do not put API keys, tokens, credentials, session cookies or account-specific endpoint authentication in Git. The user or runtime supplies credentials through its own protected configuration. This repository owns the *contract*, not an OpenAI-hosted account or an OpenAI token.

## FCIS ownership and execution

| FCIS layer | Responsibility |
| --- | --- |
| `AGENTS.md` and organization standards | Scope, prohibitions and review constraints |
| `PLANS.md` in the executing owner repository | Requested skill and destination, source revision, validation, acceptance and rollback |
| Owner skill `SKILL.md` | Authoring, packaging, validation, targeted publish and verification procedure |
| External API / connector | Authenticated access to OpenAI or ChatGPT services; no policy and no independent source authority |

The organization catalog is a *declaration of desired distribution*, not a second copy of skill contents. `skills/openai-distribution.json` holds a small, reviewed initial selection with owning repository and path; execution receipts may subsequently record source commit, package SHA-256, returned API skill ID/version, and separate ChatGPT readback. These are never inferred from names or locally passing tests.

## Targeted deployment contract

1. Resolve the skill's declared Git source, recorded commit and complete package. Read owner `AGENTS.md` and `PLANS.md`. Check that there is exactly one `SKILL.md`, the frontmatter contains only `name` and `description`, and `agents/openai.yaml` exists when required by the ChatGPT authoring workflow. Run OpenAI Skill Creator validation where accessible and owner-specific tests. Treat package validation as distinct from FCIS acceptance.
2. Compare the source package hash and available destination readback. Never reconcile by overwriting the entire destination catalog. Do not delete, retire or change unrelated packages just because they are undeclared or have drift.
3. For the public Skills API, perform at most one named skill create or version upload per authorized operation. Capture returned `skill_id`, version and default-version state, read back the exact new version (allow a bounded retry for transient `404` after upload), and verify the payload and intended version pointer. Do not change the default version without an explicitly scoped promotion.
4. For ChatGPT Skills, use only an authorized, supported installation workflow. If using an account-specific Git-backed adapter, distinguish its capabilities and errors from the public OpenAI API, preserve existing account packages, and verify the exact account/workspace installation by independent readback. Observed `HTTP 422` for an aggregate push does not authorize repeated aggregate retries.
5. Report `PROVEN`, `DOCUMENTED`, `INFERRED`, `PROPOSED`, or `BLOCKED` separately for each destination. No success claim without destination readback. Record the previous version for rollback; roll back only the selected package, without bulk reset.

## UX and initial intended selection

The workspace's useful author-facing selection begins with **Teatro Scenario Composer**, **Linotype Estate Template**, and **FCIS Skill Authoring and Sync** (the FCIS/OpenAI Skill Creator integration). Keep their identities distinct and complementary. This is the desired-state declaration, **not** a claim that all three are currently and persistently installed at `chatgpt.com/skills`. Other installed user skills remain untouched. Do not promise grouping, ordering or workspace UI customization that OpenAI's interface has not demonstrated.

The first live acceptance must demonstrate **one** source-pinned upload to the public API (if an authorized API credential and project are available), followed by version readback, and independently inspect account Skills state. An absent credential prevents that remote acceptance, not the documentation or validation. No code should silently publish on git push; no GitHub Actions automation is required.

## Superseding Chapter 160 ownership

Historical descriptions above of separate domain repositories as skill authorities are superseded by the adopted and published Chapter 160: Fountain-Coach/.github alone owns canonical skill definitions. Domain copies are projections. The three complete canonical packages are held in .codex/skills under this repository. Migration origin revisions remain provenance, not current authority.

Execute python3 skills/skillctl.py check; then python3 -m unittest discover -s skills/tests -v. To create a deterministic ZIP, use python3 skills/skillctl.py package --skill teatro-scenario-composer --output /tmp/skill.zip. To compare an independently obtained exported package, use python3 skills/skillctl.py compare --skill teatro-scenario-composer --zip /tmp/observed.zip. Without readback, report remains UNVERIFIED. Optional local hooks: git config core.hooksPath .githooks. They do not control remote mutations or prevent administrators from changing ChatGPT installations.
