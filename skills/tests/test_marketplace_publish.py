"""Automatic GitHub marketplace commit: isolated Git history and negative proof."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import marketplace_publish as publishing
import plugin_projection as projection
from skillctl import digest, entries

TRIGGER_DESCRIPTIONS = {
    "fcis-skill-authoring-and-sync": "Skill routing preflight and plugin maintenance",
    "fcis-owner-access": "iPad passkey session redirect Access",
    "fcis-go-runtime-migration": "Go runtime release, consult fcis-owner-access",
}
RESOLUTION_PRELUDE = (
    "**Governing-Skill resolution — before external tools:** "
    "Use skills__list and skills__read; choose fcis-owner-access for owner UX, "
    "fcis-go-runtime-migration for Go release, fcis-skill-authoring-and-sync "
    "for Skill routing; preserve the original user goal and Definition of Done.\n\n"
)


def git(root, *args):
    return subprocess.check_output(
        ["git", "-C", str(root), *args], text=True
    ).strip()


class MarketplacePublishTests(unittest.TestCase):
    def test_only_reviewed_mcp_configuration_is_derived_path(self):
        self.assertTrue(publishing.eligible_path(
            "plugins/fcis-skill-authoring-and-sync/mcp.json"))
        self.assertFalse(publishing.eligible_path(
            "plugins/fcis-skill-authoring-and-sync/other-mcp.json"))
        self.assertFalse(publishing.eligible_path(
            "plugins/other-plugin/mcp.json"))

    def test_original_logo_is_only_allowed_derived_brand_asset(self):
        self.assertTrue(publishing.eligible_path(
            "plugins/fcis-skill-authoring-and-sync/assets/fountain-coach-logo-transparent.png"))
        self.assertFalse(publishing.eligible_path(
            "plugins/fcis-skill-authoring-and-sync/assets/alternate-brand.png"))
        self.assertFalse(publishing.eligible_path(
            "plugins/fcis-skill-authoring-and-sync/assets/../../other.png"))

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "canonical"
        self.root.mkdir()
        git(self.root, "init", "-q", "-b", "main")
        git(self.root, "config", "user.name", "Isolated Test")
        git(self.root, "config", "user.email", "fcis-test@example.invalid")
        self.skill = self.root / ".codex/skills/fcis-skill-authoring-and-sync/SKILL.md"
        self.skill.parent.joinpath("agents").mkdir(parents=True)
        self.skill.write_text(
            "---\nname: fcis-skill-authoring-and-sync\n"
            "description: " + TRIGGER_DESCRIPTIONS[projection.SKILL]
            + "\n---\n\n# FCIS\n\n"
            "## First operational gate — stop the Invented-Prerequisite Loop\n\n"
            + RESOLUTION_PRELUDE
            + "Keep original goal; require observed failure, smallest correction; "
            "PROPOSED / non-blocking, reversal and a finite Definition of Done.\n"
        )
        self.skill.parent.joinpath("agents/openai.yaml").write_text(
            "interface:\n  display_name: FCIS\n"
        )
        skills = self.root / "skills"
        skills.mkdir()
        shutil.copy2(Path(__file__).resolve().parents[1] / "skillctl.py",
                     skills / "skillctl.py")
        rows = []
        for name in projection.CANONICAL_SKILLS:
            folder = self.root / ".codex" / "skills" / name
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "agents").mkdir(exist_ok=True)
            if name != projection.SKILL:
                description = TRIGGER_DESCRIPTIONS.get(name, "Reviewed")
                sample = ("---\nname: " + name + "\ndescription: " + description
                          + "\n---\n# " + name + "\n")
                if name in projection.ANTI_LOOP_GATED_SKILLS:
                    sample += ("\n## First operational gate — stop the Invented-Prerequisite Loop\n\n"
                               + RESOLUTION_PRELUDE
                               + "Keep original goal; require observed failure, smallest correction; "
                               "PROPOSED / non-blocking, reversal and a finite Definition of Done.\n")
                (folder / "SKILL.md").write_text(sample)
                (folder / "agents/openai.yaml").write_text(
                    "interface:\n  display_name: " + name + "\n"
                )
            row = {"name": name, "canonicalPath": ".codex/skills/" + name,
                   "contentSHA256": digest(entries(folder))}
            if name == projection.SKILL:
                row["marketplaceWebsiteURL"] = "https://fcis.fountain.coach/"
            rows.append(row)
        self.catalog = skills / "openai-distribution.json"
        self.catalog.write_text(json.dumps({
            "owner": "Fountain-Coach/.github", "skills": rows
        }))
        self.active = self.root / ".codex/skills/fcis-go/SKILL.md"
        self.active.parent.joinpath("agents").mkdir(parents=True)
        self.active.write_text(
            "---\nname: fcis-go\ndescription: Govern owner FCIS marketplace updates\n"
            "---\n# FCIS-GO\n\nVerify source and installed state.\n")
        self.active.parent.joinpath("agents/openai.yaml").write_text(
            "interface:\n  display_name: FCIS-GO\n")
        self.neutral = self.root / "skills/canonical/fcis-go/SKILL.md"
        self.neutral.parent.mkdir(parents=True)
        self.neutral.write_bytes(self.active.read_bytes())
        publication = {
            "owner":"Fountain-Coach/.github",
            "maintainedSourceCatalog":"skills/openai-distribution.json",
            "activePluginId":projection.WORKSPACE_PLUGIN_ID,
            "activeSkill":{
                "name":"fcis-go", "canonicalPath":"skills/canonical/fcis-go",
                "marketplaceWebsiteURL":"https://fcis.fountain.coach/",
                "contentSHA256":digest(entries(self.neutral.parent)),
                "projections":{"openai":{
                    "path":".codex/skills/fcis-go",
                    "contentSHA256":digest(entries(self.active.parent)),
                }}
            }
        }
        (self.root / projection.ACTIVE_MANIFEST_PATH).write_text(json.dumps(publication))
        self.marketplace = self.root / projection.MARKETPLACE_PATH
        self.marketplace.parent.mkdir(parents=True)
        self.marketplace.write_text(json.dumps({
            "name": "fountain-coach", "plugins": [{
                "name": "fcis-skill-authoring-and-sync",
                "pluginId": projection.WORKSPACE_PLUGIN_ID,
                "source": {"source": "local", "path": "./plugins/fcis-skill-authoring-and-sync"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            }],
        }))
        self.manifest = self.root / projection.PLUGIN_PATH / "plugin.json"
        self.manifest.parent.mkdir(parents=True)
        self.manifest.write_text(json.dumps({
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": "fcis-skill-authoring-and-sync",
            "version": "0.1.0",
            "repository": "https://github.com/Fountain-Coach/.github",
            "extensions": {"com.openai": {"interface": {"displayName": "FCIS"}}},
        }))
        projection.sync(self.root)
        git(self.root, "add", ".")
        git(self.root, "commit", "-q", "-m", "initial canonical and marketplace")
        self.original = git(self.root, "rev-parse", "HEAD")

    def accept_new_canonical_skill(self):
        # The only accepted public mutation is on the new active FCIS-GO Skill.
        self.neutral.write_text(self.neutral.read_text() +
                                "\nObserved owner-accepted maintenance lesson.\n")
        self.active.write_bytes(self.neutral.read_bytes())
        publication = self.root / projection.ACTIVE_MANIFEST_PATH
        content = json.loads(publication.read_text())
        content["activeSkill"]["contentSHA256"] = digest(entries(self.neutral.parent))
        content["activeSkill"]["projections"]["openai"]["contentSHA256"] = digest(
            entries(self.active.parent))
        publication.write_text(json.dumps(content))
        git(self.root, "add", "--", "skills/canonical/fcis-go/SKILL.md",
            ".codex/skills/fcis-go/SKILL.md", "skills/fcis-go-publication.json")
        git(self.root, "commit", "-q", "-m", "accepted canonical learning")

    def test_versioned_post_commit_hook_makes_separate_derived_commit(self):
        hooks = self.root / '.githooks'
        hooks.mkdir()
        import shutil
        for name in ('plugin_projection.py', 'marketplace_publish.py'):
            shutil.copy2(Path(__file__).resolve().parents[1] / name,
                         self.root / 'skills' / name)
        source_hook = Path(__file__).resolve().parents[2] / '.githooks' / 'post-commit'
        destination = hooks / 'post-commit'
        shutil.copy2(source_hook, destination)
        destination.chmod(0o755)
        (self.root / '.gitignore').write_text('__pycache__/\n')
        git(self.root, 'add', '.gitignore', '.githooks/post-commit',
            'skills/plugin_projection.py', 'skills/marketplace_publish.py')
        git(self.root, 'commit', '-q', '-m', 'Install local source and hook fixtures')
        git(self.root, 'config', 'core.hooksPath', '.githooks')
        self.accept_new_canonical_skill()
        result = projection.check(self.root)
        self.assertEqual(result['version'], '0.1.1')
        messages = git(self.root, 'log', '-2', '--pretty=%s').splitlines()
        self.assertEqual(messages, [
            'plugins: sync FCIS marketplace from canonical Skill',
            'accepted canonical learning',
        ])
        changed = set(git(self.root, 'show', '--pretty=format:', '--name-only',
                          'HEAD').splitlines())
        self.assertEqual(changed, {
            'plugins/fcis-skill-authoring-and-sync/plugin.json',
            'plugins/fcis-skill-authoring-and-sync/skills/fcis-go/SKILL.md',
        })

    def test_direct_main_push_is_refused(self):
        with self.assertRaisesRegex(publishing.PublicationError, "Direct push"):
            publishing.publish(self.root, perform_push=True)

    def test_no_change_means_no_new_commit(self):
        result = publishing.publish(self.root, perform_push=False)
        self.assertEqual(result["state"], "ALREADY_SYNCHRONIZED")
        self.assertEqual(git(self.root, "rev-parse", "HEAD"), self.original)

    def test_accepted_source_publishes_only_derived_paths_and_is_idempotent(self):
        self.accept_new_canonical_skill()
        source_commit = git(self.root, "rev-parse", "HEAD")
        projection.sync(self.root)
        result = publishing.publish(self.root, perform_push=False)
        self.assertEqual(result["state"], "DERIVED_COMMITTED_LOCAL")
        self.assertEqual(result["parent"], source_commit)
        self.assertEqual(result["version"], "0.1.1")
        changed = set(git(self.root, "show", "--pretty=format:", "--name-only", "HEAD").splitlines())
        self.assertEqual(changed, {
            "plugins/fcis-skill-authoring-and-sync/plugin.json",
            "plugins/fcis-skill-authoring-and-sync/skills/fcis-go/SKILL.md",
        })
        again = publishing.publish(self.root, perform_push=False)
        self.assertEqual(again["state"], "ALREADY_SYNCHRONIZED")
        self.assertEqual(again["commit"], result["commit"])

    def test_unrelated_dirty_file_refuses_without_commit(self):
        self.accept_new_canonical_skill()
        projection.sync(self.root)
        unrelated = self.root / "private-notes.txt"
        unrelated.write_text("preserve\n")
        before = git(self.root, "rev-parse", "HEAD")
        with self.assertRaises(publishing.PublicationError):
            publishing.publish(self.root, perform_push=False)
        self.assertEqual(git(self.root, "rev-parse", "HEAD"), before)
        self.assertEqual(unrelated.read_text(), "preserve\n")

    def test_pre_staged_change_refuses_without_commit(self):
        self.accept_new_canonical_skill()
        projection.sync(self.root)
        git(self.root, "add", "plugins/fcis-skill-authoring-and-sync/plugin.json")
        before = git(self.root, "rev-parse", "HEAD")
        with self.assertRaises(publishing.PublicationError):
            publishing.publish(self.root, perform_push=False)
        self.assertEqual(git(self.root, "rev-parse", "HEAD"), before)

    def test_unpinned_canonical_skill_refuses_without_commit(self):
        self.skill.write_text("unreviewed\n")
        before = git(self.root, "rev-parse", "HEAD")
        with self.assertRaises(publishing.PublicationError):
            publishing.publish(self.root, perform_push=False)
        self.assertEqual(git(self.root, "rev-parse", "HEAD"), before)

    def test_unknown_extra_mirror_file_refuses(self):
        extra = self.root / projection.MIRROR_PATH / "unrelated.txt"
        extra.write_text("do not remove\n")
        with self.assertRaises(projection.ProjectionError):
            projection.sync(self.root)
        with self.assertRaises(projection.ProjectionError):
            publishing.publish(self.root, perform_push=False)
        self.assertEqual(extra.read_text(), "do not remove\n")


if __name__ == "__main__":
    unittest.main()
