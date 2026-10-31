"""Git-owned FCIS marketplace projection and refusal tests."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import plugin_projection as projection
from skillctl import digest, entries


class MarketplaceProjectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.canonical = self.root / ".codex/skills" / projection.SKILL
        self.canonical.mkdir(parents=True)
        self.canonical.joinpath("SKILL.md").write_text(
            "---\nname: fcis-skill-authoring-and-sync\ndescription: FCIS\n---\n\nEvidence first.\n"
        )
        self.canonical.joinpath("agents").mkdir()
        self.canonical.joinpath("agents/openai.yaml").write_text(
            "interface:\n  display_name: FCIS\n"
        )
        catalog = self.root / "skills/openai-distribution.json"
        catalog.parent.mkdir(parents=True)
        catalog.write_text(json.dumps({
            "owner": "Fountain-Coach/.github",
            "skills": [{
                "name": projection.SKILL,
                "marketplaceWebsiteURL": "https://fcis.fountain.coach/",
                "contentSHA256": digest(entries(self.canonical))
            }]
        }))
        self.marketplace = self.root / projection.MARKETPLACE_PATH
        self.marketplace.parent.mkdir(parents=True)
        self.marketplace.write_text(json.dumps({
            "name": "fountain-coach",
            "plugins": [{
                "name": projection.PLUGIN,
                "pluginId": projection.WORKSPACE_PLUGIN_ID,
                "source": {
                    "source": "local",
                    "path": "./plugins/fcis-skill-authoring-and-sync"
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL"
                }
            }]
        }))
        self.manifest = self.root / projection.PLUGIN_PATH / "plugin.json"
        self.manifest.parent.mkdir(parents=True)
        self.manifest.write_text(json.dumps({
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": projection.PLUGIN,
            "version": "0.1.0",
            "repository": "https://github.com/Fountain-Coach/.github",
            "extensions": {"com.openai": {
                "interface": {"displayName": "FCIS"}
            }}
        }))

    def test_first_sync_copies_only_exact_canonical_tree(self):
        result = projection.sync(self.root)
        self.assertEqual(result["state"], "SYNCED")
        self.assertEqual(result["version"], "0.1.0")
        self.assertEqual(entries(self.canonical), entries(self.root / projection.MIRROR_PATH))

    def test_repeat_sync_is_a_no_op(self):
        projection.sync(self.root)
        result = projection.sync(self.root)
        self.assertEqual(result["state"], "MATCHED")
        self.assertEqual(result["version"], "0.1.0")

    def test_metadata_only_website_drift_is_corrected_and_versioned(self):
        projection.sync(self.root)
        data = json.loads(self.manifest.read_text())
        data["extensions"]["com.openai"]["interface"]["websiteURL"] = "https://fountain.coach"
        self.manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(projection.ProjectionError, "websiteURL"):
            projection.check(self.root)
        result = projection.sync(self.root)
        self.assertEqual(result["state"], "SYNCED")
        self.assertEqual(result["version"], "0.1.1")
        updated = json.loads(self.manifest.read_text())
        self.assertEqual(
            updated["extensions"]["com.openai"]["interface"]["websiteURL"],
            "https://fcis.fountain.coach/",
        )
        self.assertEqual(entries(self.canonical), entries(self.root / projection.MIRROR_PATH))

    def test_source_change_requires_sync_and_versions_derived_release(self):
        projection.sync(self.root)
        self.canonical.joinpath("SKILL.md").write_text(
            self.canonical.joinpath("SKILL.md").read_text() + "\nVerified learning.\n"
        )
        catalog = self.root / "skills/openai-distribution.json"
        data = json.loads(catalog.read_text())
        data["skills"][0]["contentSHA256"] = digest(entries(self.canonical))
        catalog.write_text(json.dumps(data))
        with self.assertRaises(projection.ProjectionError):
            projection.check(self.root)
        result = projection.sync(self.root)
        self.assertEqual(result["version"], "0.1.1")
        self.assertEqual(result["state"], "SYNCED")
        self.assertEqual(projection.check(self.root)["state"], "MATCHED")
        self.assertEqual(
            json.loads(self.marketplace.read_text())["plugins"][0]["pluginId"],
            projection.WORKSPACE_PLUGIN_ID,
        )

    def test_refuses_unreviewed_extra_mirror_file(self):
        projection.sync(self.root)
        extra = self.root / projection.MIRROR_PATH / "unrelated.txt"
        extra.write_text("Do not delete\n")
        with self.assertRaises(projection.ProjectionError):
            projection.sync(self.root)
        self.assertEqual(extra.read_text(), "Do not delete\n")

    def test_refuses_default_install_policy(self):
        data = json.loads(self.marketplace.read_text())
        data["plugins"][0]["policy"]["installation"] = "INSTALLED_BY_DEFAULT"
        self.marketplace.write_text(json.dumps(data))
        with self.assertRaises(projection.ProjectionError):
            projection.sync(self.root)

    def test_refuses_lost_or_changed_workspace_plugin_identity(self):
        for alternative in (None, "Plugin_00000000000000000000000000000000"):
            data = json.loads(self.marketplace.read_text())
            if alternative is None:
                data["plugins"][0].pop("pluginId", None)
            else:
                data["plugins"][0]["pluginId"] = alternative
            self.marketplace.write_text(json.dumps(data))
            with self.assertRaisesRegex(projection.ProjectionError, "pluginId"):
                projection.sync(self.root)
            with self.assertRaisesRegex(projection.ProjectionError, "pluginId"):
                projection.check(self.root)

    def test_refuses_changed_canonical_digest(self):
        self.canonical.joinpath("SKILL.md").write_text("Unrecorded source edit\n")
        with self.assertRaises(projection.ProjectionError):
            projection.sync(self.root)


if __name__ == "__main__":
    unittest.main()
