# FCIS GitHub-backed ChatGPT distribution

Authority: Fountain Coach Governance Chapter 160. Only
Fountain-Coach/.github/.codex/skills/fcis-skill-authoring-and-sync/
owns the procedure. This plugin is a derived Git artifact, not independent
authority for editing the Skill or installing any ChatGPT account version.

## Identity and publication boundary

- Canonical Git repository: https://github.com/Fountain-Coach/.github
- Git marketplace: .agents/plugins/marketplace.json
- Portable plugin: plugins/fcis-skill-authoring-and-sync/
- Plugin: fcis-skill-authoring-and-sync (one identity); included Skills: all five exact canonical FCIS packages
- Existing ChatGPT workspace plugin ID: `Plugin_fb9e0937c59c8191b9fa077fa5ea53ef`
  (authenticated Admin Console readback, activated and installed at 0.1.1)
- No MCP service, runtime Kit capability, provider credentials or account action

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
