# FCIS GitHub-backed ChatGPT distribution

Authority: Fountain Coach Governance Chapter 160. Only
Fountain-Coach/.github/.codex/skills/fcis-skill-authoring-and-sync/
owns the agent procedure. This plugin is a derived package, not a second
independent source.

## Scope and identity

- Canonical Git repository: https://github.com/Fountain-Coach/.github
- Git marketplace file: .agents/plugins/marketplace.json
- Portable plugin root: plugins/fcis-skill-authoring-and-sync/
- ChatGPT plugin name: fcis-skill-authoring-and-sync
- Included agent Skill: fcis-skill-authoring-and-sync
- No MCP server, runtime Kit identity, provider credentials or external action

## Update a derived Git plugin after accepted FCIS learning

From the organization repository, first verify the accepted lesson's canonical
source commit and that skills/openai-distribution.json pins the exact Skill
tree. Then, as a separate distribution-preparation operation:

    python3 skills/plugin_projection.py sync
    python3 skills/plugin_projection.py check
    python3 skills/skillctl.py check
    python3 -m unittest discover -s skills/tests -v

The sync operation copies exactly the canonical Skill file tree into the
plugin's skills/ folder. It increases the portable plugin patch version only
when updating an existing mirror. It refuses unknown extra files, bad owner
metadata or an unpinned canonical Skill. Commit and review that distribution
change through GitHub (for example, gh pr create). Git source publication is
not evidence of a ChatGPT installation or selected active execution version.

A canonical auto_elevate.py commit remains exactly a canonical Skill + digest
change; it does not run this separate distribution operation, publish an
OpenAI version or silently install a ChatGPT plugin. Do not add automatic
GitHub Actions publishing on learning commits.

## First ChatGPT workspace import

A ChatGPT workspace admin performs the initial import:

1. In the intended workspace Admin Console, open Plugins > Add > Import marketplace.
2. Source: https://github.com/Fountain-Coach/.github
3. Path: leave empty, because .agents/plugins/marketplace.json is at repository root.
4. Branch: main, once the reviewed marketplace PR has been merged.
5. Authorize GitHub, import and review the import report; keep the installation
   available only to intended members until independent post-install readback.
6. After future reviewed plugin commits, the marketplace may synchronize daily,
   or the admin may select Marketplaces > fountain-coach > Sync now.

If an existing *workspace plugin* is to move under GitHub management without
changing its identity or policies, read its actual ID in the Admin Console URL
and add that exact ID as pluginId to its matching marketplace entry before
import. This can preserve an eligible existing workspace plugin; it does not
migrate an independently installed personal Skill automatically. Do not guess
an ID or delete the current standalone personal installation in anticipation.

After import, verify the installed Skill instructions, bundled file tree,
plugin version and workspace selected/active state. Only after this evidence
supports replacement should the old independent Skill be retired. The
ChatGPT account installation and OpenAI project Skills API are distinct.

Vendor documentation:
https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github
https://developers.openai.com/plugins/build/plugins
