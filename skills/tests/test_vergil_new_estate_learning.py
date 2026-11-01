"""Checks canonical FCIS Skill lessons from the verified Vergil/new Bookshelf run.

These are procedure-instruction regressions, not live renderer/player/publisher tests.
The source-bound Swift and browser witnesses remain in their owning repos.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".codex" / "skills"


def content(name, relative):
    return (SKILLS / name / relative).read_text(encoding="utf-8")


class VergilSkillLessons(unittest.TestCase):
    def test_skill_identity_and_existing_source_owners(self):
        names = ["satzfunk-voice-render", "linotype-estate-template",
                 "estate-publisher-deployment"]
        for name in names:
            with self.subTest(name=name):
                entry = content(name, "SKILL.md")
                self.assertIn("name: " + name, entry)
                self.assertIn("references/", entry)

    def test_full_length_render_procedure_is_not_short_audition(self):
        entry = content("satzfunk-voice-render", "SKILL.md")
        text = content("satzfunk-voice-render", "references/long-form-source-fidelity.md")
        self.assertIn("Do not make the original short Satzfunk Node Realtime audition a universal prerequisite", entry)
        self.assertIn("native Swift FCIS", entry)
        self.assertIn("independent transcription of each actual recorded waveform", text)
        self.assertIn("same approved narrator implementation", text)

    def test_fidelity_guard_rejects_manual_and_biased_correction(self):
        text = content("satzfunk-voice-render", "references/long-form-source-fidelity.md")
        for required in [
            "vocabulary-only", "expected manuscript passage",
            "every unresolved passage one first attempt before any second",
            "candidate-audio recheck before paying for another take",
            "block assembly", "unresolved", "original WAV",
            "transcript-aligned", "artistically accepted"
        ]:
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_new_bookshelf_over_legacy_essay(self):
        entry = content("linotype-estate-template", "SKILL.md")
        text = content("linotype-estate-template", "references/new-estate-spoken-edition.md")
        self.assertIn("new-estate-spoken-edition.md", entry)
        for required in [
            "active new reader", "historical standalone essay",
            "source-block", "SHA-256", "SatzfunkPlayer",
            "persistent book frame", "page turns",
            "pause and hide", "First Readings",
            "Chromium and WebKit", "498.970", "499.032",
        ]:
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_stage_must_prove_correct_reader_and_preserve_current_state(self):
        entry = content("estate-publisher-deployment", "SKILL.md")
        text = content("estate-publisher-deployment",
                       "references/developing-estate-audio-staging.md")
        self.assertIn("developing-estate-audio-staging.md", entry)
        for required in [
            "existing stage symlink", "share a title", "immutable candidate",
            "added, modified, deleted, preserved", "rollback",
            "correct MP3 checksum", "not", "rights",
            "old standalone essay", "new Bookshelf"
        ]:
            with self.subTest(required=required):
                self.assertIn(required, text)
        self.assertIn("three separate authorities", entry)

    def test_live_witnesses_do_not_grant_public_or_artistic_authority(self):
        texts = [
            content("satzfunk-voice-render", "references/long-form-source-fidelity.md"),
            content("linotype-estate-template", "references/new-estate-spoken-edition.md"),
            content("estate-publisher-deployment",
                    "references/developing-estate-audio-staging.md")
        ]
        self.assertTrue(all("public" in t.lower() for t in texts))
        self.assertTrue(all("artistic" in t.lower() for t in texts))
        self.assertTrue(all("PR #5" in t or "PR #85" in t for t in texts))

    def test_no_new_skill_or_distribution_package(self):
        root = SKILLS
        self.assertFalse((root / "vergil-auto-correct").exists())
        self.assertFalse((root / "spoken-edition").exists())
        self.assertFalse((ROOT / "skills" / "proposals" / "vergil-skill.zip").exists())


if __name__ == "__main__":
    unittest.main()
