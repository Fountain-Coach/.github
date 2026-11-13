"""Contract regression: editorial style is semantic and source-owned."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
S=ROOT/".codex/skills/linotype-estate-template"

class EditorialStyleContract(unittest.TestCase):
    def test_existing_linotype_skill_updated_not_replaced(self):
        text=(S/"SKILL.md").read_text()
        self.assertIn("## Source-bound editorial introductions",text)
        self.assertIn("references/editorial-introduction-consistency.md",text)
        self.assertIn("Fountain-Coach/fountain-press/Scripts/editorial_proem.py",text)
        self.assertIn("Never promote a title, subtitle",text)

    def test_reference_prevents_fictional_editing_or_renderer(self):
        rules=(S/"references/editorial-introduction-consistency.md").read_text()
        for term in ("source-block", "frame-essay-abstract", "frame-editorial-proem",
                     "frame-lead", "First Readings", "no-hero", "EstatePublisher"):
            self.assertIn(term,rules)
        self.assertIn("does **not** make every estate hostname a book",rules)
        self.assertIn("Never generate missing prose",rules)

if __name__=="__main__":unittest.main()
