"""Regression for observed Client-Centered v177 empty-leaf -> v178 in-flow repair.

This checks canonical learning content, not the live server or a new compositor.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
LINOTYPE = ROOT / ".codex/skills/linotype-estate-template"
SKILL = LINOTYPE / "SKILL.md"
REF = LINOTYPE / "references/model-essay-spread-proofreading-and-archive.md"


class ClientCenteredLearningTests(unittest.TestCase):
    def test_update_existing_skill_and_avoid_second_reader(self):
        skill = SKILL.read_text()
        for term in ("Prevent isolated leaves caused by illustration insertion",
                     "inFlowFigure", "same source-addressed §book-prose§ flow",
                     "data-inline-after-paragraph", "existing Press",
                     "every composed leaf on the live staged URL"):
            self.assertIn(term.replace('§', chr(96)), skill)

    def test_negative_figure_leaf_and_source_anchor_are_recorded(self):
        ref = REF.read_text()
        for required in (
            "v177", "v178", "book-art-leaf", "between two §book-chapter-text§",
            "client-centered.s2.p14", "client-centered.s2.p6",
            "data-source-illustration-id", 'data-inline-after-paragraph="13"',
            "13 is not a reusable constant", "actual source paragraph order",
            "inFlowFigure", "NOT_ESTABLISHED",
        ):
            self.assertIn(required.replace('§', chr(96)), ref)
        self.assertIn("Do not “repair” it with whitespace removal", ref)

    def test_independent_witnesses_and_claim_limits(self):
        ref = REF.read_text()
        for required in (
            "fountain.coach@4a89ae5",
            "shared-shell-20261110-v178-client-centered-flow-4a89ae5",
            "shared-shell-20261110-v177-client-centered-bd8f6d9",
            "03e4497f6deabe173958bd632b721ac7f23ae95e3bbe0043a1204ad5039de78a",
            "e38301452ef0f07aa9440953d898dcf9ae13fcb828a7d4a97fac163976261d9a",
            "typedEstatePublisherReceiptEstablished: false",
            "iPad portrait-sized **4/4**",
            "landscape **7/7**",
            "phone **14/14**",
            "one secondary figure",
            "post-repair iPad Safari/VoiceOver is NOT_ESTABLISHED",
            "Ear listening Error: Listening release origin not admitted",
            "og:image:secure_url", "twitter:image",
            "no substituted local response",
            "not a typed EstatePublisher release receipt",
        ):
            self.assertIn(required, ref)


if __name__ == "__main__":
    unittest.main()
