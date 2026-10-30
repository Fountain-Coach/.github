# FCIS GitHub-backed ChatGPT distribution

Authority: Fountain Coach Governance Chapter 160. Only
Fountain-Coach/.github/.codex/skills/fcis-skill-authoring-and-sync/
owns the procedure. This plugin is a derived Git artifact, not independent
authority for editing the Skill or installing any ChatGPT account version.

## Identity and publication boundary

- Canonical Git repository: https://github.com/Fountain-Coach/.github
- Git marketplace: .agents/plugins/marketplace.json
- Portable plugin: plugins/fcis-skill-authoring-and-sync/
- Plugin and included Skill: fcis-skill-authoring-and-sync
- No MCP service, runtime Kit capability, provider credentials or account action

## The automatic GitHub distribution path (writer-authorized)

After accepted scenario evidence, the governed source agent may run
skills/auto_elevate.py. It commits ONLY the canonical Skill and its digest.
After that source commit is pushed to the canonical repository's main branch,
.github/workflows/fcis-marketplace-sync.yml runs automatically:

1. Check the canonical full-tree SHA-256 and run the organization unit tests.
2. Run python3 skills/plugin_projection.py sync.
3. Verify python3 skills/plugin_projection.py check and git diff --check.
4. Run python3 skills/marketplace_publish.py, which allows only the one existing
   plugin's mirror files and plugin.json, refuses unrelated or staged changes,
   verifies the GitHub origin and unchanged remote parent, and commits/pushes
   just the derived files as a fast-forward to main.
5. Only when the canonical Skill file-tree bytes change does the portable
   plugin's patch version increase. Replaying unchanged input is a no-op.

GitHub Actions uses only the repository's GITHUB_TOKEN with contents:write.
The workflow cannot upload to ChatGPT/OpenAI, select a hosted active version,
delete an existing installation, acquire credentials, or rewrite Kit source.
An out-of-date main branch, invalid source digest, unknown extra mirrored file,
failed test or unrelated dirty change refuses publication visibly. The
derivative-only commit cannot retrigger the path-filtered workflow. A source
commit and a derived commit remain separately inspectable in Git history.

For manual read-only verification, run:

    python3 skills/plugin_projection.py check
    python3 skills/skillctl.py check
    python3 -m unittest discover -s skills/tests -v

The explicit projection command python3 skills/plugin_projection.py sync
remains available for diagnosis or a deliberate manual recovery, but it is no
longer necessary after a verified canonical commit reaches main when GitHub
Actions succeeds. Monitor its workflow result; do not misreport a failed
Actions run as a deployed marketplace update.

## Separate ChatGPT workspace import and ongoing hosted readback

A ChatGPT workspace admin must first import the GitHub marketplace via the
authorized workspace administration interface (if available to that workspace):

- Repository: https://github.com/Fountain-Coach/.github
- Path: empty; the marketplace descriptor is at the repository root
- Branch: main
- Marketplace: fountain-coach
- Plugin: fcis-skill-authoring-and-sync, not installed by default

After a successful initial import, ChatGPT can synchronize imported GitHub
marketplaces daily or on an admin-triggered sync. GitHub package publication
does not establish that the user's ChatGPT workspace has imported it.
Check the actual account or workspace installation's contents and selected
execution version using an authenticated supported readback before declaring
that the hosted installation is up to date.

If an existing *workspace plugin* should retain its ID, inspect the actual
pluginId on the authorized admin surface before modifying the marketplace
entry. An independently created account Skill is a distinct installation;
do not delete it just because the Git marketplace became available.

There is deliberately no action for OpenAI's project-scoped Skills API, and
no unattended account Skill installation or active/default promotion.

Vendor documentation:
https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github
https://developers.openai.com/plugins/build/plugins
