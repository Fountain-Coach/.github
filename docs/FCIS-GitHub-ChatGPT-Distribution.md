# FCIS GitHub-backed ChatGPT distribution

Authority: Fountain Coach Governance Chapter 160. The active FCIS-GO
procedure is now owned by `skills/canonical/fcis-go/SKILL.md` in canonical
Fountain Coach Git. The `.codex/skills/fcis-go/` directory and installed
ChatGPT marketplace plugin are checked OpenAI projections. The historical nine
Skills remain separately pinned in maintenance at their legacy source paths.
A provider installation does not author, replace or grant access to FCIS.

## One-way owner to provider projection — 24 November 2026

Current authority chain:

1. `skills/canonical/fcis-go/SKILL.md` — owner-authored FCIS instructions.
2. `skills/fcis-go-publication.json` — approved source and OpenAI-adapter
   identity plus **separate** content digests.
3. `skills/provider_projection.py check` — verifies the OpenAI Skill's
   instructions match the owner source. A vendor-side change cannot be
   accepted by merely changing the projected checksum.
4. For an explicitly accepted neutral revision, update the source digest
   in the manifest, run `skills/provider_projection.py sync` to update only
   the OpenAI instruction copy and its projection digest, then run
   `skills/plugin_projection.py sync` to derive the existing one-Skill
   marketplace package. Protect and validate both commits through Git.
5. Independently read the installed provider version and content after
   the existing marketplace `Jetzt synchronisieren` action.

This initial source-ownership migration preserves the **existing 0.1.40**
OpenAI adapter byte-for-byte. A new provider or a new Skill is **not**
admitted by creating a directory. Anthropic is an optional future adapter,
not an implemented or accepted integration. Migration of the nine historical
maintained `.codex/skills/` sources is deferred to separate reviewed
compatibility decisions. An accepted source revision is not proof of
independent owner-facing capability execution or marketplace rollback.

## Identity and publication boundary

- Canonical Git repository: https://github.com/Fountain-Coach/.github
- Git marketplace: .agents/plugins/marketplace.json
- Portable plugin: plugins/fcis-skill-authoring-and-sync/
- Plugin: fcis-skill-authoring-and-sync (one identity); included source packages: nine canonical FCIS Skills (maintenance mode as of 24 November 2026)
- Existing ChatGPT workspace plugin ID: `Plugin_fb9e0937c59c8191b9fa077fa5ea53ef`
  (authenticated Admin Console readback, activated and installed at 0.1.1)
- No MCP service, runtime Kit capability, provider credentials or account action

## FCIS-GO first ownership milestone — 24 November 2026

The owner has frozen automatic Skill elevation and new Skill admission while
establishing source-to-provider release ownership. All nine canonical reviewed
Skill trees remain intact and are identified as maintained assets in
`skills/fcis-maintenance.json`. `skills/auto_elevate.py` refuses automated
promotion during this phase. Reviewed observed-defect and security maintenance
continues.

The existing plugin identity remains `Plugin_fb9e0937c59c8191b9fa077fa5ea53ef`.
`FCIS-GO` is its public display name; Fountain Coach is its publisher. Its
logo and composer icon reference the unchanged transparent Fountain Coach
brand mark from `Fountain-Coach/fcis.fountain.coach`, maintained as a pinned
derived asset in `plugins/fcis-skill-authoring-and-sync/assets/`. The public
reading at `fcis.fountain.coach` explains the FCIS method and distinguishes
the technology owner from each customer's retained knowledge.

The nine-Skill Git projection is a compatibility baseline, not the customer
product definition or a promise that every installed Skill is the active
execution path. A change to provider-visible Skill availability requires a
separate consumer/routing inventory and independently supported provider
readback. Source merge and mirrored package parity are distinct from
installation, effective provider selection, and reversible hosted rollback.
A supported previous-version restoration must be witnessed through the actual
workspace marketplace before declaring full ownership acceptance.

## FCIS-GO single-Skill marketplace publication — owner decision 24 November 2026

The first managed FCIS-GO customer-facing plugin must contain **exactly one**
active Skill: `fcis-go`. All nine existing historical canonical Skills remain
source-maintained with their original provenance and pinned hashes in
`skills/openai-distribution.json`. Automatic evidence elevation is suspended.
The explicitly admitted active operator Skill is retained at
`.codex/skills/fcis-go/` and separately pinned in
`skills/fcis-go-publication.json`. No other FCIS Skill is published through
the GitHub plugin.

The existing plugin slug `fcis-skill-authoring-and-sync`, fixed marketplace
identity `Plugin_fb9e0937c59c8191b9fa077fa5ea53ef`, GitHub marketplace,
source repository, publisher, front page, original logo and approved copy are
preserved. Only the derived package under
`plugins/fcis-skill-authoring-and-sync/skills/` changes. A migration is
authorized to remove the nine old **derived mirror directories** only if
their full file trees match the current pinned historical sources exactly.
No `.codex/skills/` source tree is deleted or moved. The single new mirror
must match the pinned active canonical Skill. Any extra, modified or symlinked
mirror is refused.

A single plugin patch version is issued for the reviewed change. Git tests
and source/package parity must pass before protected merge; source-only
success is distinct from hosted delivery. The owner then synchronizes
the existing marketplace with `Jetzt synchronisieren` and independently
verifies: one marketplace plugin, unchanged ID, new version, loaded original
Fountain Coach icon, **one visible Skill named FCIS-GO**, exactly matched
installed entrypoint and zero remaining old nine entries. A provider refusal
or incomplete inspection remains explicitly unaccepted. Product release
is separated from the still-unproven valid-version rollback operation.

All earlier historical sections below document the prior nine-Skill
distribution. They are provenance, not instructions to republish nine Skills.

## FCIS-GO hosted installation and recoverability (24 November 2026)

The original GitHub marketplace `fountain-coach/.github`, branch `main`, now
reports a completed manual sync of revision `159dc244`: one existing plugin
updated and zero failed. The authenticated Workspace Admin Console readback
shows plugin `Plugin_fb9e0937c59c8191b9fa077fa5ea53ef`, product name
`FCIS-GO`, installed version `0.1.39`, publisher Fountain Coach, approved
short description and workspace-default installation enabled. The same-origin
marketplace-provided logo rendered as a 128 x 128 PNG and matches the
source-pinned 460 x 460 original Fountain Coach mark after resampling
(white-composited mean difference about 0.2 of 255 per channel).
All nine installed Skill entrypoints exactly match the Git-derived
`SKILL.md` files. Their **canonical source mode is maintenance**;
the existing nine-entry consumer-facing bundle remains visible.

The unrelated private `Fountain Host FCIS` plugin
`plugin_asdk_app_6aef6a108bd081919baf80e8b7843d03` was deleted
using Admin Console Plugin Actions > Delete. A refreshed workspace-scoped
Admin Plugins listing showed only FCIS-GO. This does not remove the
separate Host service, repository, or evidence.

### Supported recovery boundary

The existing marketplace settings display `Branch, Tag oder Commit: main`
as **read-only**. Available controls include manual sync, automatic daily
sync and marketplace deletion. No previous-version selector or restore
button is exposed. The provider's published import/sync guidance says
**invalid updates retain the last working plugin**, which is not evidence
that an earlier valid version can be chosen on demand:
https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github

For a controlled recovery of a previously accepted valid release, the
candidate supported path is a **reviewed protected Git restoration** of
the exact prior plugin source and derived package; the existing
marketplace's `Jetzt synchronisieren`; then independent readback of
the unchanged plugin ID, installed version, contents and Git source
revision. To restore the preferred current release, repeat through
a reviewed Git source revision and another independently verified sync.
Preserve previous Git identity and passing source/package evidence.
**Do not delete or re-import a marketplace, create a replacement plugin,
force-update main or treat Git revert as hosted acceptance.**

At this point no live restore has been exercised: valid-version rollback
remains `NOT_ESTABLISHED`. Prepare a safe reversible exercise that
retains the owner maintenance restriction before downgrading any live Skills.

## One reviewed plugin, five canonical Skills (7 November 2026)

The portable Agent Plugins format supports multiple Skill directories under one
plugin's `skills/` root. Preserve the installed GitHub-backed FCIS plugin identity
and its marketplace `pluginId`. The **five current organization canonical Skills**
are projected into that existing plugin, with independent full-tree SHA-256
verification for every Skill, while the plugin has **one** semantic patch version.
One changed Skill causes one plugin patch bump; unchanged content is idempotent.
A sixth Skill is never silently admitted. Do not create five new plugins or
modify personal ChatGPT account Skills to fix this Git package.

The publisher and GitHub Actions only produce derived Git bytes. Marketplace
import/sync and effective ChatGPT skill routing remain provider-side acts,
with separate independent readback. A missing plugin runtime on web/desktop
is not proof of platform refusal until the actual installed plugin version
and the selected Skill provenance have been observed.

## Provider-compatible metadata is part of release validity (7 November 2026)

Portable plugin import may process only part of a plugin even when the
marketplace reports one plugin updated and zero failed. In the actual
workspace's initial v0.1.7 import, the plugin was installed but only three
of five packaged Skills appeared. The omitted Linotype and Teatro Skills had
`policy.products` names `chatgpt`, `codex`, `api`, `atlas`, while the official
OpenAI skill agent metadata rules support only `CHAT` and `CODEX`. Their
original SVG icons also declared 24x24 geometry, while OpenAI's published
icon rules require at least 48x48. The repaired canonical packages retain
the same Skill names and artwork, use supported product policy values, and
present a valid 48x48 vector. `plugin_projection.py` now tests these metadata
preconditions (including negative regressions) before permitting the Git
release. This is a source-supported likely cause, not a claim of hosted
acceptance until all five Skills have been observed in the imported plugin.

Sources:
- https://developers.openai.com/plugins/deploy/submission-errors
- https://developers.openai.com/plugins/build/plugins

## Git-native canonical-to-derived source distribution (7 November 2026)

The existing local `.githooks/post-commit` recognizes a canonical Skill,
the canonical digest catalogue, or the projection program changing. After the
first canonical commit it uses `skills/plugin_projection.py sync` and
`skills/marketplace_publish.py` to create a **separate derived Git commit**
in the same review branch. This does not push GitHub main or alter an account.
Only the reviewed five Skill trees and existing `plugin.json` may be
modified, with one patch bump of the single existing plugin when content
changes. An unchanged projection is a no-op.

On pull requests, `.github/workflows/test.yml` validates all five canonical
source tree digests, checks all five derived tree contents against them,
runs regression tests, and checks formatting. Protected `main` admits
merges only after the required checks pass. `fcis-marketplace-sync.yml`
is now a **read-only verification** of what was merged: GitHub Actions
does not make a second commit or bypass branch protection. GitHub's
auto-merge option may be enabled for a selected PR once its review
requirements are met. No unconditional merge of arbitrary PRs is granted.

If a clone has no hooks, run the same bounded commands on a review branch:

    python3 skills/skillctl.py check
    python3 skills/plugin_projection.py sync
    python3 skills/marketplace_publish.py
    python3 skills/plugin_projection.py check
    python3 -m unittest discover -s skills/tests -v

Then submit the canonical and derived commits through the same PR.
CI refuses an unprojected canonical source change. Do not "fix" that
by disabling CI or pushing directly to `main`.

GitHub commits, package contents, hosted import and active runtime are
four distinct acceptance stages. Passing local checks is not evidence
that a new ChatGPT skill version is available.

## Separate ChatGPT workspace import and ongoing hosted readback

A ChatGPT workspace admin must first import the GitHub marketplace via the
authorized workspace administration interface (if available to that workspace):

- Repository: https://github.com/Fountain-Coach/.github
- Path: empty; the marketplace descriptor is at the repository root
- Branch: main
- Marketplace: fountain-coach
- Plugin: fcis-skill-authoring-and-sync, takeover of existing installed workspace plugin (source policy does not force installation)

After a successful initial import, ChatGPT can synchronize imported GitHub
marketplaces daily or on an admin-triggered sync. GitHub package publication
does not establish that the user's ChatGPT workspace has imported it.
Check the actual account or workspace installation's contents and selected
execution version using an authenticated supported readback before declaring
that the hosted installation is up to date.

The existing ZIP-uploaded workspace plugin is now explicitly addressed by
`pluginId` alongside `name` and `source` in `.agents/plugins/marketplace.json`.
The ID was independently read from the actual authenticated plugin detail URL;
it is **not** placed in `plugin.json`. The projection verifier refuses a missing
or changed takeover ID, and the identity is preserved on future source updates.

Provider-side acceptance (30 October 2026): authenticated Mac Safari
verified the supported **Plugins > Hinzufügen > Marketplace importieren**
workflow. The correct repository root was imported into the writer's workspace
with branch `main`. The marketplace detail page confirms the GitHub source
`fountain-coach/.github`, source revision `a81e566`, state **Abgeschlossen**,
one imported plugin and zero failures. The marketplace's **automatic sync**
switch is `aria-checked=true`. Clicking FCIS in that imported marketplace
opened the existing `Plugin_fb9e0937c59c8191b9fa077fa5ea53ef` identity,
which remains **Aktiviert**, **Installiert** and at **0.1.1**. This independently
proves the initial GitHub-to-workspace connection and preservation of this
one plugin ID; it did **not** prove that no other same-named plugin existed.
A separate workspace inventory later found the redundant private ZIP-uploaded
plugin `Plugin_13ac379589248191ae51f74ce1768eac` alongside the GitHub
entry. Its identity-scoped admin delete action briefly raised
`plugins_upstream_failure`, but a fresh workspace inventory proved that the
private entry was absent and **only the GitHub-backed ID remained**. A transient
provider toast cannot replace final workspace readback in either direction.

**First post-import version upgrade witnessed (30 October 2026):** The
accepted installation-lesson PR #21 merged as `5d19ac4`; GitHub Actions run
`41114586095` succeeded and published the exact canonical Skill as plugin
**0.1.2**, derived-only Git commit `d3abfc0be206b81e33f4667fe102f81b2a761dd8`.
The operator used the supported **Jetzt synchronisieren** action in the
previously imported marketplace. ChatGPT subsequently reported
**Abgeschlossen**, revision `d3abfc0`, **1 updated, 0 failed**, unchanged
installed plugin `Plugin_fb9e0937c59c8191b9fa077fa5ea53ef` at
**0.1.2**, active and installed. Auto-sync remained enabled. This proves a
**manually initiated** full GitHub-to-ChatGPT update. It does not prove the
separate unattended daily trigger has executed.
Do not upload another static ZIP or use undocumented private provider APIs.

An independently created account Skill is a distinct installation; do not
delete it just because the Git marketplace became available.

There is deliberately no action for OpenAI's project-scoped Skills API, and
no unattended account Skill installation or active/default promotion.

Vendor documentation:
https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github
https://developers.openai.com/plugins/build/plugins


## Read-only ChatGPT installed-entrypoint audit (7 November 2026)

For a supported readback, create a local JSON array of observations such as
[{"environment":"chatgpt-web","skill":"linotype-estate-template","entrypointText":"literal observed entrypoint"}].
For confirmed absence use {"environment":"chatgpt-web","skill":"satzfunk-voice-render","presence":"absent","inventoryComplete":true}.
Run: python3 skills/skillctl.py audit --observations /path/to/observations.json

DRIFT means the observed entrypoint text differs from the canonical text.
MISSING requires independent evidence that the relevant destination inventory is complete; a list of skills exposed to one chat is not proof of account-wide absence. UNVERIFIED means
missing evidence, incomplete inventory, or a matching entrypoint without
independently verified full package contents and selected effective version.
The existing skillctl compare command supports complete ZIP file-tree checks.
No entrypoint comparison alone proves actual ChatGPT routing or an active version.
No account installation, marketplace update, or provider mutation occurs.

## Same-name standalone Skills can shadow an updated GitHub plugin (7 November 2026)

A successful imported marketplace update, plugin version and visible bundled
Skill names do **not** determine which instruction source the ChatGPT model
will select. In the authorized workspace, plugin 0.1.8 correctly listed five
Skills while a fresh chat explicitly selecting Fountain Coach FCIS returned
the older Linotype standalone Skill's first heading. The Admin Skills catalog
confirmed a separate historical account Skill of that same identity and body.
This is a real incompatible output witness, not a definitive internal routing
trace. Do not claim the GitHub plugin is absent or that provider routing has
been proven solely from a model answer.

For read-only evidence, run `skillctl.py audit --observations` with distinct
`origin` values (`standalone-skill`, `marketplace-plugin`, `project-api`),
scoped to the same environment and named Skill. This distinguishes old entrypoint
content drift from an installed plugin whose complete contents and execution
version remain unverified. Same-name origins produce a `routingStatus=UNVERIFIED`
collision witness. Never coerce that into MATCHED from version metadata.

Retaining a standalone Skill preserves its ownership/history and prior use.
Disabling, overwriting, renaming, or deleting it is an independent user-account
mutation, not an automatic effect of GitHub marketplace sync. Prefer a
supported non-destructive per-skill routing/installation control if one is
available; otherwise name the exact old Skill and destination and obtain
targeted authorization before altering it. Existing private Skills must not be
silently deleted just to make an acceptance test green.

## No Skill ZIP delivery: enforced source contract (7 November 2026)

FCIS explicitly prohibits generating, attaching or uploading a Skill ZIP as
an installation/update/repair workaround. A historical individual ChatGPT
Skill may be edited only through a supported in-place editor under explicit
narrow authorization, or left unresolved. Do not create another personal Skill
or package an archive just because a generic Skill Creator guide proposes it.

The `skills/skillctl.py package` CLI and its archive-writing helper are
removed. Unit tests require the legacy CLI to refuse and verify that it writes
no file. The remaining ZIP **reader** only compares older provider-supplied
readback evidence and cannot publish or create a ZIP. GitHub PR CI runs these
tests alongside all five canonical file-tree and marketplace checks. The only
FCIS publication path remains the reviewed Git-backed marketplace plugin.

Repository enforcement cannot change OpenAI's built-in Skill Creator text in
other accounts; workspace instructions and actual provider routing still
require independent acceptance. Never claim an installation is current from
this source-side prohibition alone.
