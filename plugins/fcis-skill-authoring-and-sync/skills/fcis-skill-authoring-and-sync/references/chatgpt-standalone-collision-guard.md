# ChatGPT standalone-Skill collision prevention and reversible cleanup

This is an observed user-account installation procedure, not GitHub marketplace
publication. Canonical source is Fountain-Coach/.github; the existing single
Fountain Coach FCIS GitHub-backed plugin provides all five Skills.

## Trigger

Run this guard immediately after each FCIS marketplace version sync, before
claiming a newly installed version is active in a ChatGPT task, and during
the scheduled FCIS convergence check. It is especially important when a new
chat returns an old procedural heading or old version of the no-ZIP rule.

## Exact scope and authority

The only account Skill identities governed by this rule are the five declared
canonical Skill names in `skills/openai-distribution.json`. Display labels in
different languages may vary; resolve to the canonical exact identity before
uninstallation. User authorized reversible uninstall of previously identified
Fountain Coach-owned standalone duplicates in their own ChatGPT workspace.
That does **not** authorize deleting authored Skills, touching unrelated
Skills, reinstalling another copy, or changing another user's account.

## Read-only account check

1. Confirm the authenticated workspace and that the existing Fountain Coach
   FCIS GitHub-backed plugin still exposes all five Skills and the intended
   version. Do not act on a name or source URL alone.
2. Visit ChatGPT Skills (`https://chatgpt.com/skills`) with the account owner.
   Search the exact standalone Skill name, inspect that account Skill's
   **own** action menu, and distinguish the two cases:
   - **Uninstall / Deinstallieren** present: a separately installed account
     Skill exists and may shadow the canonical plugin
   - **Add / Hinzufügen** offered: the authored standalone Skill is **not**
     currently installed; it must not be uninstalled or deleted
   If the action is unclear or the skill is not found, record UNVERIFIED
   rather than infer that it is absent from the account.
3. Record each observed action in a local (not Git-committed) JSON array, for
   example:

       [
         {"environment":"chatgpt-workspace-web",
          "skill":"linotype-estate-template",
          "origin":"standalone-skill",
          "installed":false,"observedAction":"add"}
       ]

   Run `python3 skills/skillctl.py guard --observations <local-file.json>`.
   `CLEAR` means an observed Add action; `CONFLICT` means an observed
   Uninstall action; `UNVERIFIED` means no exact witness. The tool exits
   0 for fully clear evidence, 2 for any conflict, and 3 for incomplete
   evidence. Never turn a partial inventory into a full five-skill pass.

## Reversible reconciliation (only when authorized)

For an exact canonical-owned duplicate in the approved workspace,
activate **Uninstall / Deinstallieren** on the standalone account Skill's
own actions menu. Do not choose **Delete / Löschen**. This deliberately
preserves authored history while taking the standalone installation out
of the runtime selection set.

Read back the same exact Skill after the provider settles. Require **Add /
Hinzufügen** for that standalone identity; if it still offers Uninstall,
the operation is not accepted. Repeat only for separately observed,
independently approved canonical identities. No bulk account wipe.

After cleanup, independently recheck the existing GitHub-backed plugin's
identity, version and five bundled Skills. Start a **fresh** ChatGPT
conversation with the plugin selected and request a read-only source-specific
fact (Linotype first substantive heading = `Fountain Press is the staging
and production publishing standard`, its publishing lane = Fountain Press).
That answer is an output-level routing witness, not a provider trace proving
the actual selected skill file or complete package content.

## Maintenance contract

Treat standalone account duplication as a collision regardless of whether
the standalone entrypoint text happens to match today. The reason is future
drift across two independent version authorities. Never reinstall
organization-owned FCIS Skills through an account ZIP or independent
personal Skill import. Keep the provider account check **separate** from
GitHub Actions: CI has no access to an authenticated person's ChatGPT
installation, and a successful Git merge cannot be an account-uninstall
receipt.

A recurring FCIS convergence check may use the owner-authorized account
session for readback and, for the exact preauthorized same-name set, the
same reversible Uninstall operation. If the account is unavailable or a
provider action becomes unsupported, fail closed with a precise notice. Do
not claim that no future conflict is possible: new accounts, reinstallation,
platform caching, and routing ambiguity remain outside source Git's control.

**Observed acceptance, 7 November 2026:** Linotype Estate Template,
estate publisher deployment, FCIS Skill Authoring and Sync, and Teatro
Scenario Composer each changed from an available Deinstallieren action to
their own Hinzufügen action in the authorized workspace. These changes
did not delete the authored originals. Plugin version 0.1.9 retained five
bundled Skills in the user-facing directory.
