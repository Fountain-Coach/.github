# GitHub-backed ChatGPT marketplace takeover — verified procedure

**Trigger:** The writer wants an existing ChatGPT workspace plugin to receive
ongoing GitHub updates without reinstalling a ZIP, duplicating the plugin,
losing its policies, or changing its identity. This is a *distribution lesson*,
not a new FCIS Kit capability or a new Skill identity.

## The accepted failure and the correction

A green GitHub Actions projection and a plugin ZIP were repeatedly mistaken for
ChatGPT marketplace synchronization. The uploaded ZIP did install a plugin,
but **did not connect it to GitHub**. The initially tried
**Marktplätze → Hinzufügen** action opened an archive uploader. The actual
GitHub importer was exposed in an authenticated Mac Safari Admin Console under
**Plugins → Hinzufügen (menu) → Marketplace importieren**. The successful import
adopted the installed plugin's actual `pluginId`, not a new identity.
A brief provider message that status could not be checked was transient; the
settled marketplace list and plugin detail established success.

## Repeatable workflow

1. **Define the actual result.** Distinguish: a standalone ChatGPT Skill,
   ZIP-installed workspace plugin, installed GitHub connector, GitHub portable
   marketplace package, and a **ChatGPT GitHub-imported marketplace**. All are
   different. For unattended updates the last is required.
2. **Verify canonical Git first.** Read the selected Skill in
   `Fountain-Coach/.github/.codex/skills/<name>/`, its pinned full-tree digest,
   the derived `plugins/<name>/plugin.json` and
   `.agents/plugins/marketplace.json`. Check the mirror against the canonical
   bytes and validate CI. Git publication alone is not ChatGPT installation.
3. **Preserve the existing workspace plugin.** In the authorized, signed-in
   Admin Console, open the installed plugin's detail page. Read the exact
   `/plugins/Plugin_...` URL, installed and activated state, version, and
   policies. If an existing plugin is being adopted, add **that observed**
   `pluginId` beside `name` and `source` in the matching single entry of
   `.agents/plugins/marketplace.json` only. Do not put it in
   `plugin.json`, invent the ID, or delete/reinstall the original.
4. **Publish the source correction.** Validate the marketplace declaration,
   source checks and complete Skill mirror. Merge the reviewed Git change.
   Preserve unrelated marketplace plugins; source Git updates do not themselves
   alter the ChatGPT workspace.
5. **Import through the supported provider interface.** In the *correct*
   ChatGPT workspace Admin Console, choose
   **Plugins → Hinzufügen → Marketplace importieren** (a menu entry).
   Do **not** choose ZIP upload, `Marktplätze → Hinzufügen`, a GitHub
   connector, or a guessed app-management URL. The observed import fields are:
   - **Quelle:** `https://github.com/Fountain-Coach/.github`
   - **Pfad:** empty (manifest at repository root)
   - **Branch, Tag oder Commit:** `main`

   Submit via the visible **Marktplatz importieren** action and authorize
   GitHub when the provider requests it. Use only supported authenticated
   controls; if unavailable, report the blocker without cookie extraction,
   undocumented provider calls, or another ZIP.
6. **Independently read back both identities.** In **Marktplätze** inspect
   GitHub origin, branch, exact last synced revision, **Abgeschlossen** state,
   imported/failure counts, and the **Auto-Synchronisierung** switch enabled.
   Open the imported marketplace's plugin and compare its full `Plugin_...`
   URL, version, installed and activated state with the original observation.
   A provider count of "1 hinzugefügt" does not prove a duplicate: the stable
   plugin ID is the deciding witness. Treat transient "status unavailable" as
   a symptom; reload or inspect the settled source/status before diagnosing.
7. **Audit for leftover ZIP-created duplicates.** The marketplace import can
   preserve its declared workspace plugin ID while another, independent
   ZIP-uploaded plugin with the *same display name* remains present. Inspect
   **Plugins → Workspace**: compare every candidate's actual `Plugin_...` URL,
   developer, availability and installed status against the marketplace's
   linked plugin ID. Retain the active GitHub-linked plugin. If explicitly
   authorized to clean up, delete only the independently identified private
   duplicate through its own **Plugin-Aktionen → Plugin löschen** controls;
   never delete by display name alone. A provider toast such as
   `plugins_upstream_failure` does not settle the result either way: reload
   the workspace inventory and prove that only the GitHub-linked ID remains.
8. **Verify later updates separately.** After the canonical Skill next changes,
   check GitHub Action's derived-only commit and plugin version bump, then read
   the same workspace plugin after its scheduled auto-sync. For an immediate
   explicit test, the supported **Jetzt synchronisieren** action is permissible,
   but label it *manual*, not evidence that the daily schedule executed.
   Confirm new hosted version, unchanged `pluginId`, active installation and
   the synchronized source revision.

## Negative acceptance rules

- **ZIP-installed and active, no imported GitHub marketplace:**
  `INSTALLED_NOT_SYNCHRONIZED`; never recommend another ZIP.
- **GitHub CI green or isolated `codex plugin add` succeeds, no provider
  readback:** `HOSTED_UNVERIFIED`.
- **Wrong/missing pluginId:** refuse takeover; preserve the existing identity
  and unrelated policies.
- **Two same-named workspace plugins:** distinguish IDs and GitHub provenance.
  Do not claim there is no duplicate from a successful marketplace import.
  Remove only an explicitly authorized, independently identified redundant
  entry, then re-read the workspace inventory. A failed delete toast does not
  override the final provider inventory either way.
- **Provider status remains unavailable or import action absent:** classify
  `BLOCKED`; do not silently delete/recreate or use a private API.
- **Imported marketplace but auto-sync off:** the *initial connection* exists,
  but automatic distribution is not enabled.
- **Import completed but destination plugin/version unexamined:** only the
  marketplace portion is proven, not installed version equality.
- **Future scheduled version not witnessed:** do not claim it happened from
  initial import alone, even when automatic synchronization is on.

## Origin of the lesson

The 30 October 2026 result was independently observed via authenticated Mac
Safari Admin Console and the canonical Git/GitHub tests. The distribution
receipts remain in `PLANS.md` and
`docs/FCIS-GitHub-ChatGPT-Distribution.md` at
`Fountain-Coach/.github@d793359`: source takeover PR #20; marketplace
`fountain-coach/.github` on `main`, synchronized Git `a81e566`,
**Abgeschlossen**, one imported, zero failed, auto-sync checked; the imported
plugin navigated to the *same* pre-existing workspace `Plugin_...` identity,
activated and installed at 0.1.1. This proves the initial GitHub-backed
workspace bridge, not a later daily version-update witness. An additional
workspace audit exposed two distinct plugins with the same display name: an
older private, unavailable ZIP entry and the active GitHub-connected entry.
The private plugin's own delete control was used with its separately verified
ID. Although the UI briefly displayed `plugins_upstream_failure`, a newly
loaded workspace inventory showed exactly one remaining FCIS plugin, the
GitHub-backed ID. The marketplace still reported one imported plugin,
**Abgeschlossen** and automatic sync on. The new audit step therefore requires
both workspace and marketplace readback, not a conclusion from either toast.
