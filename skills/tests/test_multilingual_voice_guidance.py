"""FCIS voice guidance: governed multilingual intake without invented runtime capability."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / ".codex/skills/satzfunk-voice-render/SKILL.md"
REFERENCE = SKILL.parent / "references/multilingual-writer-teacher.md"
CATALOG = ROOT / "skills/openai-distribution.json"

class MultilingualVoiceGuidanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_existing_canonical_voice_skill_is_extended(self):
        self.assertTrue(SKILL.is_file())
        self.assertIn("name: satzfunk-voice-render", self.skill)
        self.assertIn("references/multilingual-writer-teacher.md", self.skill)
        self.assertEqual(sum(s["name"] == "satzfunk-voice-render" for s in self.catalog["skills"]), 1)
        self.assertFalse(any(s["name"] == "multilingual-voice-editions" for s in self.catalog["skills"]))

    def test_both_audiences_and_own_voice_are_taught(self):
        for phrase in ["writers", "teachers", "pupils", "own-voice", "British-English", "source"]:
            self.assertIn(phrase.lower(), (self.skill + self.reference).lower())

    def test_no_unproven_clone_or_native_accent_claim(self):
        for phrase in ["NOT ESTABLISHED", "native listener", "source accent", "self-hosted synthesis"]:
            self.assertIn(phrase.lower(), self.reference.lower())
        self.assertIn("does not prove English voice cloning", self.reference)

    def test_consent_and_minors_boundary(self):
        for phrase in ["speaker authorization", "guardian/school consent", "pupil voice", "cloud transfer"]:
            self.assertIn(phrase.lower(), self.reference.lower())

    def test_fcis_kit_and_existing_reader_are_authoritative(self):
        for phrase in ["FountainCoachSpokenEditionKit", "reframe/spoken-edition.render", "existing cursor", "Linotype"]:
            self.assertIn(phrase, self.reference)
        self.assertIn("do not create a second linotype", self.reference.lower())

    def test_github_canonical_not_zip_or_hosted_claim(self):
        self.assertIn("Fountain-Coach/.github", self.reference)
        self.assertIn("skill.zip", self.reference)
        self.assertIn("derived", self.reference)
        self.assertIn("complete-content readback", self.reference)

if __name__ == "__main__":
    unittest.main()
