"""Owner-first FCIS-GO marketplace identity and maintenance release checks."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills"))
from plugin_projection import CANONICAL_SKILLS, WORKSPACE_PLUGIN_ID, check


class FCISGOOwnershipTests(unittest.TestCase):
    def test_nine_source_skills_are_in_maintenance_without_deletion(self):
        data = json.loads((ROOT / "skills/fcis-maintenance.json").read_text())
        self.assertEqual(data["owner"], "Fountain-Coach/.github")
        self.assertEqual(data["mode"], "maintenance")
        self.assertEqual(data["pluginId"], WORKSPACE_PLUGIN_ID)
        self.assertEqual(data["policy"]["automaticSkillElevation"], "suspended")
        self.assertEqual(data["policy"]["newSkillAdmission"], "suspended")
        self.assertEqual({r["name"] for r in data["skills"]}, set(CANONICAL_SKILLS))
        for row in data["skills"]:
            self.assertEqual(row["state"], "maintenance")
            self.assertTrue((ROOT / row["source"] / "SKILL.md").is_file())
        self.assertEqual(check(ROOT)["state"], "MATCHED")

    def test_existing_plugin_id_and_original_logo_are_retained(self):
        market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        self.assertEqual(len(market["plugins"]), 1)
        self.assertEqual(market["plugins"][0]["pluginId"], WORKSPACE_PLUGIN_ID)
        plugin = json.loads((ROOT / "plugins/fcis-skill-authoring-and-sync/plugin.json").read_text())
        self.assertEqual(plugin["name"], "fcis-skill-authoring-and-sync")
        self.assertEqual(plugin["repository"], "https://github.com/Fountain-Coach/.github")
        interface = plugin["extensions"]["com.openai"]["interface"]
        self.assertEqual(interface["displayName"], "FCIS-GO")
        self.assertEqual(interface["developerName"], "Fountain Coach")
        self.assertEqual(interface["shortDescription"], "Good work should teach the next attempt.")
        self.assertIn("Each customer develops their own working knowledge", interface["longDescription"])
        self.assertIn("fcis.fountain.coach", interface["longDescription"])
        self.assertEqual(interface["logo"], interface["composerIcon"])
        logo = ROOT / "plugins/fcis-skill-authoring-and-sync" / interface["logo"].removeprefix("./")
        self.assertTrue(logo.is_file())
        self.assertEqual(
            hashlib.sha256(logo.read_bytes()).hexdigest(),
            "8c5fad1c3db56138d5959da75991dc8034a0be537ce46da6ffcc0d9655e7f729",
        )

if __name__ == "__main__":
    unittest.main()
