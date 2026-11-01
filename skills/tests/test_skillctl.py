import hashlib
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import skillctl as ctl

class SovereigntyTests(unittest.TestCase):
    def test_canonical_packages(self):
        self.assertEqual(len(ctl.validate()["skills"]), 4)
    def test_repeatable_zip_and_roundtrip(self):
        files = ctl.entries(ctl.SKILLS / "teatro-scenario-composer")
        data = ctl.archive(files, "teatro-scenario-composer")
        self.assertEqual(data, ctl.archive(files, "teatro-scenario-composer"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "skill.zip"
            path.write_bytes(data)
            self.assertEqual(files, ctl.read_archive(path, "teatro-scenario-composer"))
    def test_new_route_template_reuse(self):
        text = (ctl.SKILLS / "linotype-estate-template" / "SKILL.md").read_text()
        self.assertIn("New public route: scenario reuse before publication", text)
        self.assertIn("an already-adopted template/preview scenario", text)

    def test_linotype_page_frame_simplicity_is_canonical(self):
        skill = (ctl.SKILLS / "linotype-estate-template" / "SKILL.md").read_text()
        reference = (ctl.SKILLS / "linotype-estate-template" / "references" / "page-is-the-frame.md").read_text()
        handoff = (ctl.SKILLS / "teatro-scenario-composer" / "references" / "linotype-handoff.md").read_text()
        self.assertIn("Reader-facing Linotype: the page is the frame", skill)
        self.assertIn("repaginate", skill)
        self.assertIn("over-edited", reference)
        self.assertIn("Complexity stays in the system", reference)
        self.assertIn("Write in the present tense of evidence", reference)
        self.assertIn("Reader-surface restraint at the handoff", handoff)
        self.assertIn("Present observed current behavior", handoff)

    def test_reader_navigation_is_one_book_with_distinct_scroll_modes(self):
        skill = (ctl.SKILLS / "linotype-estate-template" / "SKILL.md").read_text()
        ref_path = ctl.SKILLS / "linotype-estate-template" / "references" / "reader-navigation-and-score-composition.md"
        self.assertTrue(ref_path.is_file())
        reference = ref_path.read_text()
        self.assertIn("reader-navigation-and-score-composition.md", skill)
        self.assertIn("On Continuity → Bookshelf (complete collection contents facing its gallery) → work", reference)
        self.assertIn("Horizontal", reference)
        self.assertIn("Vertical", reference)
        self.assertIn("no page numbers", reference)
        self.assertIn("bottom bar", reference)
        self.assertIn("Returning restores", reference)
        self.assertIn("focus", reference)
        self.assertIn("design prototypes", reference)
        self.assertIn("live behavior unverified", reference)

    def test_bookshelf_collection_gallery_alternation(self):
        ref=(ctl.SKILLS / "linotype-estate-template" / "references" / "reader-navigation-and-score-composition.md").read_text()
        skill=(ctl.SKILLS / "linotype-estate-template" / "SKILL.md").read_text()
        for token in ("collection-gallery alternation", "text → its square-thumbnail gallery",
                      "vertically", "1:1", "object-fit: contain", "first authenticated narrative image",
                      "source order", "fixed bottom reader navigation", "dark", "same reader",
                      "retaining the horizontal shelf", "vertical gallery"):
            self.assertIn(token.lower(), ref.lower())
        self.assertIn("Bookshelf text/gallery alternation",skill)

    def test_bookshelf_contents_are_visible_without_extra_click(self):
        ref=(ctl.SKILLS / "linotype-estate-template" / "references" / "reader-navigation-and-score-composition.md").read_text()
        for phrase in ("complete scrolling table of contents", "every admitted source-ordered entry",
                       "Read Essays", "no extra collection-opening click",
                       "directly to the facing Bookshelf", "both contents and gallery",
                       "independently remembered position", "introductory pieces"):
            self.assertIn(phrase.lower(),ref.lower())
        self.assertNotIn("with an accessible action to enter the collection's complete vertical contents",ref)

    def test_teatro_score_largest_balanced_fit_is_source_bound(self):
        reference = (ctl.SKILLS / "linotype-estate-template" / "references" / "reader-navigation-and-score-composition.md").read_text()
        self.assertIn("Largest Balanced Fit", reference)
        self.assertIn("scale = min(W/w, H/h)", reference)
        self.assertIn("square", reference)
        self.assertIn("wide", reference)
        self.assertIn("tall", reference)
        self.assertIn("Teatro Score", reference)
        self.assertIn("dark", reference)
        self.assertIn("SatzfunkPlayer", reference)
        self.assertIn("one folio", reference)
        self.assertIn("do not", reference.lower())

    def test_static_chapter_158_lane(self):
        text = (ctl.SKILLS / "estate-publisher-deployment" / "SKILL.md").read_text()
        self.assertIn("Chapter 158", text)
        self.assertIn("authenticated", text)
        self.assertIn("not prerequisites", text)
        self.assertNotIn("must return `estate.publication.sync`", text)

    def test_modified_content(self):
        state, delta = ctl.compare({"SKILL.md": b"source"}, {"SKILL.md": b"changed"})
        self.assertEqual((state, delta["modified"]), ("DRIFT", ["SKILL.md"]))
    def test_added_removed(self):
        state, delta = ctl.compare({"SKILL.md": b"a", "assets/a": b"b"}, {"SKILL.md": b"a", "foreign": b"c"})
        self.assertEqual(state, "DRIFT")
        self.assertEqual(delta["missing"], ["assets/a"])
        self.assertEqual(delta["unexpected"], ["foreign"])
    def test_unverified_remote(self):
        self.assertEqual(ctl.compare({"SKILL.md": b"source"}, None)[0], "UNVERIFIED")
    def test_deleted_remote_preserves_source(self):
        original = {"SKILL.md": b"canonical"}
        self.assertEqual(ctl.compare(original, {})[0], "DRIFT")
        self.assertEqual(original["SKILL.md"], b"canonical")
    def test_duplicate_zip_member_rejected(self):
        import zipfile
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.zip"
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("sample/SKILL.md", "a")
                z.writestr("sample/SKILL.md", "b")
            with self.assertRaises(ValueError):
                ctl.read_archive(path, "sample")
    def test_unsafe_zip_member_rejected(self):
        import zipfile
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unsafe.zip"
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("other/SKILL.md", "a")
            with self.assertRaises(ValueError):
                ctl.read_archive(path, "sample")

    def test_active_learning_is_automatic_but_external_versions_stay_governed(self):
        org = (ctl.ROOT / "AGENTS.md").read_text()
        skill = (ctl.SKILLS / "fcis-skill-authoring-and-sync" / "SKILL.md").read_text()
        metadata = (ctl.SKILLS / "fcis-skill-authoring-and-sync" / "agents" / "openai.yaml").read_text()
        self.assertIn("Active procedural learning (automatic canonical elevation)", org)
        self.assertIn("## Active learning", skill)
        self.assertIn("independently accepted", skill)
        self.assertIn("skills/auto_elevate.py", skill)
        self.assertIn("without a separate per-lesson approval", org)
        self.assertIn("no per-lesson approval", metadata.lower())
        self.assertIn("not a background service", skill)
        self.assertIn("Scenario-based learning input", skill)
        self.assertIn("skills/scenario_learning.py", skill)
        self.assertIn("No ChatGPT/OpenAI version is changed", skill)

if __name__ == "__main__":
    unittest.main()
