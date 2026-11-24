"""Vendor adapters cannot acquire Fountain Coach source authority."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import provider_projection
from skillctl import digest, entries


class ProviderSourceProjectionTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.canonical = self.root / provider_projection.CANONICAL
        self.canonical.mkdir(parents=True)
        (self.canonical / "SKILL.md").write_text(
            "---\nname: fcis-go\ndescription: Owner FCIS instruction\n---\n"
            "# Authoritative FCIS source\n")
        self.adapter = self.root / provider_projection.OPENAI
        (self.adapter / "agents").mkdir(parents=True)
        (self.adapter / "SKILL.md").write_bytes(
            (self.canonical / "SKILL.md").read_bytes())
        (self.adapter / "agents/openai.yaml").write_text(
            "interface:\n  display_name: FCIS-GO\n")
        self.manifest = self.root / provider_projection.MANIFEST
        self.manifest.parent.mkdir(parents=True, exist_ok=True)
        self._write_manifest()

    def _write_manifest(self):
        data = {
            "owner": "Fountain-Coach/.github",
            "activePluginId": provider_projection.PLUGIN_ID,
            "activeSkill": {
                "name": "fcis-go",
                "canonicalPath": provider_projection.CANONICAL.as_posix(),
                "contentSHA256": digest(entries(self.canonical)),
                "projections": {"openai": {
                    "path": provider_projection.OPENAI.as_posix(),
                    "contentSHA256": digest(entries(self.adapter)),
                }}
            }
        }
        self.manifest.write_text(json.dumps(data))

    def test_owner_neutral_source_and_openai_are_identical(self):
        evidence = provider_projection.check(self.root)
        self.assertEqual(evidence["state"], "MATCHED")
        self.assertEqual(evidence["provider"], "openai")
        self.assertEqual(provider_projection.sync(self.root)["state"], "MATCHED")

    def test_accepted_neutral_change_projects_one_way(self):
        (self.canonical / "SKILL.md").write_text(
            (self.canonical / "SKILL.md").read_text() + "\nReviewed owner revision.\n")
        data = json.loads(self.manifest.read_text())
        data["activeSkill"]["contentSHA256"] = digest(entries(self.canonical))
        self.manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(provider_projection.AdapterProjectionError,
                                    "instruction drift"):
            provider_projection.check(self.root)
        evidence = provider_projection.sync(self.root)
        self.assertEqual(evidence["state"], "SYNCED")
        self.assertEqual(provider_projection.check(self.root)["state"], "MATCHED")
        self.assertEqual((self.adapter / "SKILL.md").read_bytes(),
                         (self.canonical / "SKILL.md").read_bytes())
        self.assertEqual(
            provider_projection.sync(self.root)["state"], "MATCHED")

    def test_unapproved_vendor_change_cannot_rewrite_canonical_source(self):
        previous = (self.canonical / "SKILL.md").read_bytes()
        (self.adapter / "SKILL.md").write_text("Vendor override\n")
        with self.assertRaisesRegex(provider_projection.AdapterProjectionError,
                                    "outside reviewed projection"):
            provider_projection.sync(self.root)
        self.assertEqual((self.canonical / "SKILL.md").read_bytes(), previous)

    def test_unpinned_neutral_change_cannot_update_adapter(self):
        previous = (self.adapter / "SKILL.md").read_bytes()
        (self.canonical / "SKILL.md").write_text("Unreviewed source\n")
        with self.assertRaisesRegex(provider_projection.AdapterProjectionError,
                                    "not admitted"):
            provider_projection.sync(self.root)
        self.assertEqual((self.adapter / "SKILL.md").read_bytes(), previous)

    def test_provider_path_cannot_become_source_authority(self):
        data = json.loads(self.manifest.read_text())
        data["activeSkill"]["canonicalPath"] = ".codex/skills/fcis-go"
        self.manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(provider_projection.AdapterProjectionError,
                                    "not owner-approved"):
            provider_projection.check(self.root)

    def test_unknown_neutral_member_requires_review(self):
        (self.canonical / "provider.yaml").write_text("not admitted\n")
        data = json.loads(self.manifest.read_text())
        data["activeSkill"]["contentSHA256"] = digest(entries(self.canonical))
        self.manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(provider_projection.AdapterProjectionError,
                                    "Unreviewed neutral"):
            provider_projection.sync(self.root)


if __name__ == "__main__":
    unittest.main()
