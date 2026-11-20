"""LINOTYPE-FOLIO-01: source-owned argument/figure/next-argument procedure.

Test instruction ownership and positive/negative evidence contracts, not a
new runtime paginator nor fictitious author approval.
"""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
ESTATE=ROOT/".codex/skills/linotype-estate-template"
PROOF=ROOT/".codex/skills/linotype-proof-press"
REFERENCE=ESTATE/"references/semantic-illustration-folio-relations.md"


class SemanticIllustrationFolioLesson(unittest.TestCase):
    def test_canonical_source_has_one_relation_lesson_not_new_skill(self):
        doc=REFERENCE.read_text()
        self.assertIn("# LINOTYPE-FOLIO-01",doc)
        self.assertIn("before-we-can-work-together.p07",doc)
        self.assertIn("before-we-can-work-together.plate-02",doc)
        self.assertIn("before-we-can-work-together.p08",doc)
        self.assertIn("**illustrated by**",doc)
        self.assertIn("**introduces the following example**",doc)
        self.assertIn("Do not infer relationships merely from HTML siblings",doc)
        self.assertIn("source/composition record",doc)
        self.assertIn("does not establish",doc)
        self.assertIn("not an automatic demand",doc.lower())
        self.assertIn("EDITORIAL_REVIEW_REQUIRED",doc)
        self.assertIn("no one-line prose stub",doc)
        self.assertNotIn("make every page at least 85%",doc.lower())

    def test_existing_linode_skill_and_proof_use_same_reference(self):
        estate=(ESTATE/"SKILL.md").read_text()
        frame=(ESTATE/"references/page-is-the-frame.md").read_text()
        plates=(ESTATE/"references/linotype-semantic-data-plates.md").read_text()
        proof=(PROOF/"SKILL.md").read_text()
        contract=(PROOF/"references/proof-contract.md").read_text()
        self.assertIn("semantic-illustration-folio-relations.md",estate)
        self.assertIn("semantic-illustration-folio-relations.md",frame)
        self.assertIn("semantic-illustration-folio-relations.md",plates)
        self.assertIn("semantic-illustration-folio-relations.md",proof)
        self.assertIn("semantic-illustration-folio-relations.md",contract)
        self.assertIn("no following prose stub",proof)
        self.assertIn("figure+caption",proof)
        self.assertIn("source coverage",proof)
        self.assertIn("before** choosing the leaf boundary",frame.lower())
        self.assertIn("without reserving the next paragraph",plates)

    def test_no_new_publication_authority_or_runtime_proof_claim(self):
        ref=REFERENCE.read_text().lower()
        for term in ("not a newly deployed compositor","not establish","physical-ipad",
                     "universal minimum fill percentage", "do not invent a second cms"):
            self.assertIn(term,ref)
        self.assertIn("private v228 WebKit proof".lower(),ref)
        self.assertIn("source-owned",ref)

    def test_unrelated_skill_identities_unchanged(self):
        self.assertIn("name: linotype-estate-template",(ESTATE/"SKILL.md").read_text())
        self.assertIn("name: linotype-proof-press",(PROOF/"SKILL.md").read_text())
        self.assertFalse((ROOT/".codex/skills/linotype-folio").exists())


if __name__=="__main__":
    unittest.main()
