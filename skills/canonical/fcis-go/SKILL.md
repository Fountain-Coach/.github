---
name: fcis-go
description: Operate the owner-controlled Fountain Coach Instruction System marketplace integration. Use FCIS-GO to inspect canonical Git and maintained Skills, diagnose release or routing drift, prepare reviewed source changes, synchronize the existing ChatGPT plugin, verify installed capabilities, and plan or test recovery without changing customer permissions.
---

# FCIS-GO — Fountain Coach Instruction System

## First operation — identify the owner task and current evidence

Resolve the user's concrete intended result, existing Git-owned scope and Definition of Done before any implementation or tool use. Read the current `Fountain-Coach/.github/PLANS.md` ownership phase and the relevant governing source. For any missing fact, inspect the live source or supported provider UI; label absent provider evidence as **UNVERIFIED**. Never manufacture a new system, service, access ceremony, permission grant or prerequisite from speculation. A source test is not proof of installed behavior.

FCIS-GO is the **one active marketplace Skill** for maintaining the Fountain Coach instruction distribution and its customer-facing integrations. It governs procedures and evidence. It does not issue OAuth credentials, enroll Hosts, replace FountainStore or turn a Skill into an executable instrument.

## Roles and boundaries

- **Fountain Coach** maintains the shared FCIS technology and canonical instructions in `Fountain-Coach/.github`. Chapter 160 and the root `AGENTS.md` govern authorship.
- **The customer** retains authority over their working knowledge, accepted extensions and purposes. Currently the platform owner is also the first customer; do not merge the two authority roles.
- **Nine historical source Skills** remain maintained canonical procedures, retained under `.codex/skills/`, with source hashes and provenance. They are **not distributed in the FCIS-GO plugin** during the owner maintenance phase. Consult their current Git source for narrowly relevant work when required; their existence in Git grants no execution permission.
- The existing hosted plugin `Plugin_fb9e0937c59c8191b9fa077fa5ea53ef` is the only FCIS-GO marketplace identity. The GitHub marketplace references `Fountain-Coach/.github` branch `main`; do not create or reimport another plugin.

## Owner work cycle

1. **Inspect.** Read `AGENTS.md`, the active `PLANS.md` phase, `skills/fcis-maintenance.json`, `skills/openai-distribution.json`, `plugins/fcis-skill-authoring-and-sync/plugin.json`, `.agents/plugins/marketplace.json`, and the relevant canonical Skill source as necessary. Compare current Git commit, pinned tree SHA-256, one active published Skill, installed plugin version and effective provider state.
2. **Bound the change.** Identify observed defect or explicit owner direction and the smallest correction. Preserve the nine maintained Skills and their hashes unless separately reviewed source maintenance is authorized. New Skill admission and automatic lesson promotion remain suspended; this one published FCIS-GO Skill is an explicitly approved exception.
3. **Validate source and projection.** For changes to FCIS-GO, validate `.codex/skills/fcis-go/` and `agents/openai.yaml`; run `python3 skills/skillctl.py check`, `python3 skills/plugin_projection.py check`, relevant regression tests and `sh scripts/fcis-ci.sh source`. The publisher projects exactly `plugins/fcis-skill-authoring-and-sync/skills/fcis-go/`. Refuse unexpected package members, unreviewed deletion, bad digests or a changed plugin ID.
4. **Release through Git.** Use one reviewed source commit plus the existing separate derived-plugin commit via `skills/plugin_projection.py sync` and `skills/marketplace_publish.py`, the protected Git PR and verified CI. Increase the existing plugin version once for a changed public Skill. A green source test establishes Git/package integrity only.
5. **Synchronize and inspect.** In the existing authorized ChatGPT Workspace Admin Console, locate the original GitHub marketplace and use supported **Jetzt synchronisieren**. Independently read back accepted source revision, unchanged plugin ID, installed version, original logo and description, and exactly **one visible Skill: FCIS-GO**. Verify installed instruction text against canonical Git. If UI or provider authorization is inaccessible, record the exact missing step instead of claiming completion.
6. **Recover.** Inspect available supported provider restoration controls. If no previous-version selector is exposed, plan a protected Git restoration of an accepted prior source+plugin version, a provider sync and independent installed readback. Do not delete/reimport the marketplace or force-push `main`. Until the full reverse journey is witnessed, mark valid-version rollback **NOT_ESTABLISHED**.

For requests concerning implementation rather than marketplace management, determine the appropriate existing source-bound procedure and runtime owner. Read canonical maintained instructions through authorized Git tooling when relevant; obtain separate real execution, Host and FountainStore receipts before claiming operational acceptance.

## Completion record

Report source commit and checked package tree, current GitHub marketplace revision, installed plugin identity/version/visible Skill count, receipt of actual operation, and one exact remaining action if a gate is open. Distinguish **source accepted**, **provider synchronized**, **effective invocation verified**, and **recovery independently demonstrated**. Close at the user's requested result.

Extended reading: https://fcis.fountain.coach/.
