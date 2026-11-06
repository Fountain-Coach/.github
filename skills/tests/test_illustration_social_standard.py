"""Fountain Press hero/social-image source contract regression.

Checks canonical procedural obligations, not the existence of production cards.
"""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
LINOTYPE=ROOT/".codex/skills/linotype-estate-template"
PUBLISHER=ROOT/".codex/skills/estate-publisher-deployment"

class IllustrationSocialStandardTests(unittest.TestCase):
    def test_existing_skills_own_policy_not_a_new_service(self):
        l=(LINOTYPE/"SKILL.md").read_text()
        p=(PUBLISHER/"SKILL.md").read_text()
        self.assertIn("Source-anchored illustration and social-image maintenance",l)
        self.assertIn("Publication hero and social-image admission",p)
        self.assertIn("EstatePublisher alone",p)
        self.assertIn("existing Linotype",l)
        self.assertIn("original Governance source unchanged",l)

    def test_hero_stays_at_original_source_beat(self):
        r=(LINOTYPE/"references/illustration-and-social-card.md").read_text()
        for term in ["data-inline-after-paragraph","data-source-illustration-id",
                     "*actual original* text position", "composed","70/70","folio **4/8 to 1/8**"]:
            self.assertIn(term,r)

    def test_social_visual_is_same_hero_or_first_landscape_page(self):
        r=(LINOTYPE/"references/illustration-and-social-card.md").read_text()
        for term in ["**raster derivative of the very same source-owned illustration**",
                     "**the publication's own first Linotype page composed in landscape**",
                     "1200 × 630", "sourceRevision","exact immutable reader/CSS revision"]:
            self.assertIn(term,r)
        self.assertIn("no hero",r.lower())
        self.assertIn("does not create a second Reader",r)
        self.assertIn("not a second",r.lower())

    def test_original_image_and_social_metadata_are_separate(self):
        r=(LINOTYPE/"references/illustration-and-social-card.md").read_text()
        for term in ["original asset path and SHA-256","alt text","rights",
                     "og:image:width", "og:image:height", "twitter:card=summary_large_image",
                     "without JavaScript","fragments are not sent"]:
            self.assertIn(term,r)
        self.assertIn("heroSourceSHA256",r)
        self.assertIn("shareImageSHA256",r)

    def test_no_generic_fallback_claim_or_unadmitted_promotion(self):
        l=(LINOTYPE/"SKILL.md").read_text()
        p=(PUBLISHER/"SKILL.md").read_text()
        ref=(LINOTYPE/"references/illustration-and-social-card.md").read_text()
        for text in (l,p,ref):
            self.assertIn("generic",text.lower())
            self.assertIn("89",text)
        self.assertIn("historical audit evidence",ref)
        self.assertIn("not a Governance acceptance gap",ref)
        self.assertIn("separately authorized",ref)
        self.assertIn("cannot silently",ref)
        self.assertIn("source owner's review",ref)

    def test_governance_does_not_require_illustrations_or_social_cards(self):
        l=(LINOTYPE/"SKILL.md").read_text()
        p=(PUBLISHER/"SKILL.md").read_text()
        ref=(LINOTYPE/"references/illustration-and-social-card.md").read_text()
        self.assertIn("Governance text-first exception",l)
        self.assertIn("Governance image-free publication acceptance",p)
        self.assertIn("without** illustrations",l)
        self.assertIn("Do not reject Governance",p)
        self.assertIn("outstanding mandatory Governance remediation",l)
        self.assertIn("or block a Governance release",ref)
        self.assertIn("other source-authored illustrated works",ref)
        self.assertIn("do not mass-delete",l)
        self.assertIn("private v163/v164",l)

    def test_reference_is_bundled(self):
        self.assertTrue((LINOTYPE/"references/illustration-and-social-card.md").is_file())

if __name__=="__main__":
    unittest.main()
