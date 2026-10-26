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


## Subsequent single-skill ChatGPT editor readback — 26 October 2026

After the source correction merged in organization PR #9, the maintainer-authorized ChatGPT Skills editor was used to update **only** `fcis-skill-authoring-and-sync` from the reviewed organization package. Following an actual browser reload, independent line-by-line reconstruction from the installed editor verified that the `SKILL.md` **instruction body** is exactly equal, after frontmatter separation and surrounding whitespace trimming, to the canonical organization source body: **6,316 of 6,316 characters matched**. The saved discovery description likewise matched the updated canonical skill description (282 characters). This is a real installed account-side body update, not a mock or mere successful-save claim.

The editor also accepted replacement text for the skill's `agents/openai.yaml` and removal of `assets/icon.svg` as staged changes, and reported no outstanding save changes. **However, after a fresh reload the previous icon and policy-bearing YAML were present again.** A second focused YAML save yielded the same result. Do not infer the cause (platform policy normalization versus file editor persistence) from that evidence alone. The remote `agents/openai.yaml` and icon therefore remain **DRIFT**, and complete ZIP/execution-version equality remains **UNVERIFIED**. No other installed account skill was edited.

The audit found a second canonical mismatch: the organization-authored `agents/openai.yaml` still referred to a generic `repo-owned` skill despite Chapter 160's single `Fountain-Coach/.github` authority. The reviewed source correction now changes its short description and default invocation text to the explicit organization-controlled model and pins the new file-tree SHA-256 `b545a106319bf82d577761fe01a58168a179429827b2c7954abe2b3d681c647d`. This is an **author-approved Git revision**, not adoption of the divergent installed policy fields or icon.

The public project-scoped OpenAI Skills API was **not** authenticated or mutated during the account reconciliation; an installed ChatGPT account skill is not proof of any project API skill. A real Reframe scenario remains subject to governed Copilot authoring, FountainStore evidence, and independent AX/window witnessing; none is claimed by this account-editor readback.

**Status:** canonical body matched after an authorized single-skill account update; supporting account resources visibly divergent; remote selected/default revision unverified. Keep reconciliation open until a supported exact bundle and execution-version readback establishes more.
