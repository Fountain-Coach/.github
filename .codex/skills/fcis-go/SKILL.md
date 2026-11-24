---
name: fcis-go
description: Mandatory entry and procedure router for Fountain Coach FCIS work, including standalone Go implementation, owner Console and Host management, Skills, source/specification parity, deployment, verification and recovery. Resolve the relevant owner-approved production Skill before FCIS work, and maintain the single existing marketplace integration without exposing private Skills or changing customer permissions.
---

# FCIS-GO — Fountain Coach Instruction System

## First operation — identify the owner task and current evidence

Resolve the user's concrete intended result, existing owned scope and Definition of Done. Select the applicable procedure in Mandatory task routing before implementation; do not run the marketplace work cycle for ordinary runtime development. Read the current `Fountain-Coach/.github/PLANS.md` ownership phase and the relevant governing source. For any missing fact, inspect the live source or supported provider UI; label absent provider evidence as **UNVERIFIED**. Never manufacture a new system, service, access ceremony, permission grant or prerequisite from speculation. A source test is not proof of installed behavior.

FCIS-GO is the **one active marketplace Skill** for maintaining the Fountain Coach instruction distribution and its customer-facing integrations. It governs procedures and evidence. It does not issue OAuth credentials, enroll Hosts, replace FountainStore or turn a Skill into an executable instrument.

## Roles and boundaries

- **Fountain Coach** maintains the shared FCIS technology and source engineering contracts in `Fountain-Coach/.github`; FountainStore owns individually admitted private Skill revisions. Chapter 160 and the root `AGENTS.md` govern authorship.
- **The customer** retains authority over their working knowledge, accepted extensions and purposes. Currently the platform owner is also the first customer; do not merge the two authority roles.
- **Nine historical source Skills** remain preserved under `.codex/skills/`, with source hashes and provenance. They are **not distributed in the FCIS-GO plugin**. An individually owner-approved and independently read-back private production revision becomes the operative instruction for its named task; the earlier Git copy remains historical. Neither instruction source grants execution permission.
- The existing hosted plugin `Plugin_fb9e0937c59c8191b9fa077fa5ea53ef` is the only FCIS-GO marketplace identity. The GitHub marketplace references `Fountain-Coach/.github` branch `main`; do not create or reimport another plugin.

## Marketplace and source maintenance work cycle — only for distribution tasks

1. **Inspect.** Read `AGENTS.md`, the active `PLANS.md` phase, `skills/fcis-maintenance.json`, `skills/openai-distribution.json`, `plugins/fcis-skill-authoring-and-sync/plugin.json`, `.agents/plugins/marketplace.json`, and the relevant canonical Skill source as necessary. Compare current Git commit, pinned tree SHA-256, one active published Skill, installed plugin version and effective provider state.
2. **Bound the change.** Identify observed defect or explicit owner direction and the smallest correction. Preserve the nine maintained Skills and their hashes unless separately reviewed source maintenance is authorized. Automatic lesson promotion and public Skill expansion remain suspended; explicit owner-private migration through the signed Store path is separate. FCIS-GO remains the only published Skill.
3. **Validate source and projection.** For changes to FCIS-GO, validate `.codex/skills/fcis-go/` and `agents/openai.yaml`; run `python3 skills/skillctl.py check`, `python3 skills/plugin_projection.py check`, relevant regression tests and `sh scripts/fcis-ci.sh source`. The publisher projects exactly `plugins/fcis-skill-authoring-and-sync/skills/fcis-go/`. Refuse unexpected package members, unreviewed deletion, bad digests or a changed plugin ID.
4. **Release through Git.** Use one reviewed source commit plus the existing separate derived-plugin commit via `skills/plugin_projection.py sync` and `skills/marketplace_publish.py`, the protected Git PR and verified CI. Increase the existing plugin version once for a changed public Skill. A green source test establishes Git/package integrity only.
5. **Synchronize and inspect.** In the existing authorized ChatGPT Workspace Admin Console, locate the original GitHub marketplace and use supported **Jetzt synchronisieren**. Independently read back accepted source revision, unchanged plugin ID, installed version, original logo and description, and exactly **one visible Skill: FCIS-GO**. Verify installed instruction text against canonical Git. If UI or provider authorization is inaccessible, record the exact missing step instead of claiming completion.
6. **Recover.** Inspect available supported provider restoration controls. If no previous-version selector is exposed, plan a protected Git restoration of an accepted prior source+plugin version, a provider sync and independent installed readback. Do not delete/reimport the marketplace or force-push `main`. Until the full reverse journey is witnessed, mark valid-version rollback **NOT_ESTABLISHED**.

## Mandatory task routing — production-owned procedures

Before starting or resuming FCIS implementation, resolve the task to its named procedure, read the active revision through an existing authorized FCIS Skill read surface, and use that revision as the operative instruction. Record the procedure name, release identity, and verification state in the owning work record. Read the normative FCIS-SYSTEM.json, FCIS-STACK.md, and FCIS-OPENAPI.json as applicable; preserve the active plan and original Definition of Done.

- Native Go implementation, specification coverage, OAuth/MCP/Host execution, Store, build/release/recovery: `fcis-go-runtime-migration`.
- Owner Console, passkey, Fleet, adding Hosts, instruments, client authorization and provider account selection: `fcis-owner-access` first; use `fcis-console-development` for Console implementation and the Go procedure for its native handlers.
- Skill custody, authoring, routing or marketplace: `fcis-go` plus the applicable owner-authorized private procedure. Other maintained engineering procedures remain in their declared ownership and are not automatically published or admitted.

Production private revisions supersede their historical Git instructions only after signed Store admission and independent authorized retrieval. During the explicitly bounded transition, use the existing verified maintained source for its still-unmigrated procedures and label it as such. Once a production procedure is admitted, do not silently fall back to a stale historical copy. If the required revision cannot be retrieved, report the concrete access failure and limit work to restoring the existing authorized route; do not create permissions, expose private source or invent a second system. A public Skill may route by private Skill name without containing its payload. Do not equate this instruction with a model-provider runtime enforcement mechanism: verify actual selection and consumption through the supported client. No new provider account, marketplace Skill, plugin identity or automatic admission.

Obtain separate real execution, Host and FountainStore receipts before claiming operational acceptance.

## Completion record

Report source commit and checked package tree, current GitHub marketplace revision, installed plugin identity/version/visible Skill count, receipt of actual operation, and one exact remaining action if a gate is open. Distinguish **source accepted**, **provider synchronized**, **effective invocation verified**, and **recovery independently demonstrated**. Close at the user's requested result.

Extended reading: https://fcis.fountain.coach/.
