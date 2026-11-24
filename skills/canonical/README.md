# Fountain Coach canonical Skill source

**Authority:** Fountain Coach, through the reviewed `Fountain-Coach/.github` repository and Governance Chapter 160. Provider directories are adapters, not instruction authorities.

## Active owner-operated instruction

`skills/canonical/fcis-go/SKILL.md` is the owner-controlled source for the single published FCIS-GO operator Skill. Its original `SKILL.md` was copied unchanged from the accepted ChatGPT version 0.1.40 during the source-ownership cutover. The provider copy is `.codex/skills/fcis-go/`; the installed marketplace copy is `plugins/fcis-skill-authoring-and-sync/skills/fcis-go/`.

The source and projected package have **separate versioned digests** in `skills/fcis-go-publication.json`. Run `python3 skills/provider_projection.py check` and `python3 skills/plugin_projection.py check` to detect provenance or content drift. For a reviewed owner-authorized source change, pin the canonical digest, run `provider_projection.py sync`, then `plugin_projection.py sync`, and validate the reviewed source and derived Git commits before the existing marketplace sync.

## Compatibility and restrictions

The nine earlier canonical Skill packages remain under `.codex/skills/` with their original digests and history as a **maintenance exception**. They are **not** republished by this change. No automatic Skill promotion or silent bulk relocation is authorized.

The OpenAI projection is a real, source-checked adapter. An Anthropic projection is not yet implemented, admitted, tested or offered as equivalent; do not fabricate `.claude/` packages or claim invocation proof. A model-service connection cannot authorize FCIS Host execution, owner state changes, or customer data custody. The existing ChatGPT plugin ID and version 0.1.40 remain unchanged by this source-only cutover.

**Separate acceptance:** vendor-independent FCIS owner login, grants, Host execution, durable Store receipt and state recovery remain the P0 business objective; none is established solely by publishing this instruction source.
