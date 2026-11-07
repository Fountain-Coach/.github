# FCIS Git PR release policy — source, mirrors and hosted readback

**Canonical source:** `Fountain-Coach/.github`. Reviewed policy snapshot:
`docs/FCIS-Main-Branch-Ruleset.json`.

## One Git PR owns source and derived package

1. The agent/maintainer changes a reviewed canonical FCIS Skill in
   `.codex/skills/<name>` and updates its full-tree digest.
2. The normal Git `post-commit` hook makes a **distinct derived commit**
   in the *same branch*, projecting the existing single plugin with five
   canonical SKILL packages and one incremented plugin patch version.
   If a clone lacks hooks, run `skills/plugin_projection.py sync`
   and `skills/marketplace_publish.py` explicitly before opening a PR.
3. The existing `test.yml` validates all canonical digests, all five
   derived trees, complete regression tests and formatting. GitHub's release
   workflow is read-only, and a direct bot push is forbidden.
4. A source PR is explicitly selected for auto-merge only when appropriate.
   GitHub `allow_auto_merge=true` merely enables opt-in per PR; it does
   not auto-merge arbitrary branches. The stored branch ruleset requires a
   PR and GitHub Actions `build` check, and disables deletion/force-push.
5. After merge, the actual published Git commit and plugin version are read
   back. The already imported GitHub marketplace may synchronize on its
   provider schedule or via the supported Admin Console `Sync now` action.
   Check resulting version and complete Skill content independently.

## Apply or verify GitHub configuration (authorized repository administrator)

First inspect the existing policy:

    gh api repos/Fountain-Coach/.github/rulesets
    gh api repos/Fountain-Coach/.github --jq '.allow_auto_merge'

After an authorized review, the declarative ruleset can be installed with:

    gh api repos/Fountain-Coach/.github/rulesets -X POST \
      --input docs/FCIS-Main-Branch-Ruleset.json

Enabling the built-in auto-merge option is separate:

    gh api repos/Fountain-Coach/.github -X PATCH -F allow_auto_merge=true

Read the resulting rule ID/contents and permission settings back. Do not
repeatedly POST duplicate rulesets; update the existing observed ID if
the policy changes. The `GitHub Actions` built-in app cannot be added to
the ruleset bypass list in this organization; this is why the old direct-push
release workflow was replaced. No bypass is required for the PR release.

GitHub checks make source distribution reproducible but not hosted Skill
installation. Personal Skills, project Skills API default pointers, and
workspace plugin versions are separate destinations. If a provider's
full-package/effective-version readback is unsupported, report UNVERIFIED
and leave FINAL DoD open, even when GitHub is green.

## Applied repository settings (7 November 2026)

Canonical `main` ruleset **26748083** was installed from the reviewed JSON and independently read back as active, with no bypass actors. It requires a PR and the GitHub Actions `build` check (app ID 15368), conversation resolution, and rejection of force-push and deletion. The repository's `allow_auto_merge=true` was read back. These settings do not establish that any particular PR has successfully auto-merged; that acceptance remains separate.

## GitHub unavailable

Git-only backups, verified bundles, and local validations continue to work.
A bare Git origin can be substituted and the same source/derived commits
moved without GitHub. Branch-protection rules and GitHub Actions are not
part of the Git object graph; the reviewed JSON policy and this procedure
allow deliberate reconfiguration on a replacement host. Never infer that
a new host has inherited GitHub's security settings.

## Acceptance evidence

- Source package SHA for every canonical Skill must equal its derived tree.
- A single canonical change yields one local source commit followed by one
  derived plugin commit; rerun with unchanged bytes yields no new commit.
- Source PR requires GitHub `build`; main is protected and auto-merge is
  individually opted in, not unconditional.
- Git recovery and ChatGPT installation/readback use different authorities.
