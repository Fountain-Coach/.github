"""Canonical skill regression for accepted v151 model and editorial archive boundaries."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
SKILL=ROOT/".codex/skills/linotype-estate-template/SKILL.md"
REF=ROOT/".codex/skills/linotype-estate-template/references/model-essay-spread-proofreading-and-archive.md"

class ModelEssayProofTests(unittest.TestCase):
    def test_single_existing_skill_and_reference(self):
        self.assertTrue(SKILL.is_file())
        self.assertTrue(REF.is_file())
        self.assertIn("model-essay-spread-proofreading-and-archive.md",SKILL.read_text())
        self.assertIn("independently browser-verified",SKILL.read_text())
        self.assertIn("one semantic field",SKILL.read_text())
    def test_spread_preserves_source_and_widow_rule(self):
        text=REF.read_text()
        for term in ("two-leaf semantic field","Satzspiegel","source-character","readable opening",
                     "actual source", "facing recto","intrinsic-aspect","iPad portrait",
                     "before/after","72%"):
            self.assertIn(term.lower(),text.lower())
        self.assertIn("not a universal arbitrary rule",text)
        self.assertIn("Apply the model, not its screenshot",text)
    def test_archival_state_not_deletion_or_public_release(self):
        text=REF.read_text()
        for term in ("archival-status editorial note","original direct route",
                     "active edition's contents","current share inventory",
                     "not deletion","public production"):
            self.assertIn(term.lower(),text.lower())
        self.assertIn("don't claim persisted Store archival",text)
    def test_proofread_is_a_full_edition_acceptance_task(self):
        text=REF.read_text()
        for term in ("every active publication", "titles", "captions", "factual claims",
                     "credits", "grammar", "source offsets", "screen-reader labels",
                     "editorial decision needed", "not yet verified"):
            self.assertIn(term.lower(),text.lower())
        self.assertIn("mechanized typo/lint scan is not the same",text)

if __name__=="__main__":unittest.main()
