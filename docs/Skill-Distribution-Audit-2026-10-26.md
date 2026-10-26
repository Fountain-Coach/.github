# Chapter 160 — ChatGPT account skill readback audit

**Observation date:** 26 October 2026  
**Canonical owner:** `Fountain-Coach/.github`  
**Canonical source revision observed:** `151c2944929c586dfdc74bc5f238fdda65bdde88`  
**Observed destination:** the account's installed ChatGPT Skills read interface (`skills__list` and individual `skills__read` resources), **not** the public `/v1/skills` API.

## Method and evidence boundary

Read the installed skill inventory and each resource exposed in the account's installed Skills bundle. Separately read the corresponding original resources from the organization GitHub repository at the revision above. Compare the available UTF-8 file bodies without changing either source or destination. For `SKILL.md`, the installed read surface exposes the *instruction body* while Git contains YAML frontmatter plus body; compare those bodies after removing frontmatter, **not** as raw full-file SHA-256 equality. All other comparable resources were checked for exact returned-text equality. The installed file inventory was compared against the canonical Git tree.

An installed skill's name, a body-level text comparison, or a list of readable resources is **not** independent proof of the complete downloaded ZIP or of the active execution/default-version pointer. The read interface does not return the Git source commit or an OpenAI project skill ID/version. Those remain **UNVERIFIED**. This observation cannot be used to assume the ChatGPT installation and public Skills API share any project or state.

## Results at source commit 151c294

| Account skill | Canonical files | Installed readable files | Readback result | Limits |
| --- | ---: | ---: | --- | --- |
| `teatro-scenario-composer` | 7 | 7 | 7 of 7 corresponding resources match; `SKILL.md` instruction body matches | Frontmatter as installed bytes, installation revision and effective version not independently available |
| `linotype-estate-template` | 13 | 13 | 13 of 13 corresponding resources match, including the two bundled scripts; `SKILL.md` body matches | Same limitations |
| `fcis-skill-authoring-and-sync` | 2 | 3 | `SKILL.md` body matches, **`agents/openai.yaml` differs**, and the installed bundle exposes an additional `assets/icon.svg` | Content divergence and unknown effective version |

### FCIS skill divergence

- Canonical `agents/openai.yaml`: 251 characters, only the `interface` display name, short description and default prompt.
- Installed account `agents/openai.yaml`: 403 characters; introduces `icon_small`, `icon_large`, `policy.products` and `policy.allow_implicit_invocation`, plus formatting differences. These fields were **observed downstream**, not admitted to canonical Git.
- Installed `assets/icon.svg` is readable, 1,738 characters, and matches the *installed Teatro Scenario Composer* icon content. The canonical FCIS skill package contains no corresponding resource.
- Those differences cannot be silently interpreted as an authorized revision or imported into the organization source. They may be a user/account edit or a platform-specific projection; their cause is not established by file readback alone.

## Corrective source action and next destination proof

The canonical FCIS Skill Authoring procedure at source revision 151c294 also contained obsolete domain-repository ownership statements despite the enacted Chapter 160 organization-only authority rule. This source-side contradiction is corrected separately on the reviewed `codex/ch160-canonical-skill-authority-correction` branch and reflected in the recalculated canonical manifest digest. The existing installed copy therefore **must not** be considered synchronized to the *new* canonical revision merely because its original instruction body matched 151c294.

Before claiming complete reconciliation: authorize **one named installation** and exact canonical source revision; use the supported ChatGPT account skill distribution workflow; preserve other skills; independently read back the full destination package and observed execution/version selection where exposed; classify unavailable evidence as `UNVERIFIED`. Public OpenAI project Skills require a separate authorized project credential and exact immutable-version ZIP/default-pointer receipt from Reframe's existing read-only observer.

**No remote installation was changed by this audit. No OpenAI project API upload or default-version change occurred. No Reframe GUI/MIDI2 live scenario was claimed.**
