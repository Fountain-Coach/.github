import hashlib
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import skillctl as ctl

class SovereigntyTests(unittest.TestCase):
    def test_canonical_packages(self):
        self.assertEqual(len(ctl.validate()["skills"]), 5)
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
        for token in ("collection-gallery alternation", "one collection identity as one horizontal navigation unit",
                      "vertically", "1:1", "object-fit: contain", "first authenticated narrative image",
                      "source order", "fixed bottom reader navigation", "dark", "same reader",
                      "horizontal collection navigation", "gallery scroll"):
            self.assertIn(token.lower(), ref.lower())
        self.assertIn("Bookshelf collection identity and coordinated text/gallery views",skill)

    def test_bookshelf_contents_are_visible_without_extra_click(self):
        ref=(ctl.SKILLS / "linotype-estate-template" / "references" / "reader-navigation-and-score-composition.md").read_text()
        for phrase in ("complete scrolling table of contents", "source order",
                       "Read Essays", "without extra navigation steps",
                       "containing Bookshelf collection", "two coordinated projections",
                       "gallery scroll", "introductory source entries"):
            self.assertIn(phrase.lower(),ref.lower())
        self.assertNotIn("with an accessible action to enter the collection's complete vertical contents",ref)

    def test_one_collection_one_selected_work_in_both_projections(self):
        ref=(ctl.SKILLS / "linotype-estate-template" / "references" / "reader-navigation-and-score-composition.md").read_text()
        for phrase in ("one collection identity as one horizontal navigation unit", "two coordinated projections",
          "selected work identity per collection", "compact/portrait", "Contents / Images",
          "seven and thirty-two text entries", "seven and thirty illustrated items", "visible image",
          "remains outside all scrollports", "native iPad gestures"):
            self.assertIn(phrase.lower(),ref.lower())

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

    def test_official_openapi_is_a_pinned_external_dependency_not_a_kit(self):
        policy = (ctl.ROOT / 'docs' / 'FCIS-Official-OpenAPI-Dependency.md').read_text()
        agents = (ctl.ROOT / 'AGENTS.md').read_text()
        authoring = (ctl.SKILLS / 'fcis-skill-authoring-and-sync' / 'SKILL.md').read_text()
        voice = (ctl.SKILLS / 'satzfunk-voice-render' / 'SKILL.md').read_text()
        host = (ctl.SKILLS / 'satzfunk-voice-render' / 'references' / 'host-contract.md').read_text()
        for item in (policy, agents, authoring, voice):
            self.assertIn('Official OpenAPI', item)
        for phrase in ('c2aecc2fbe1ddff3e7500a0eaa5c2bc4c19c5318',
                       'd80bb28992f6c2a86876d866dcae0b1f15e130de94238592bc57a4a579448b5f',
                       'oneOf', '34.2', 'American female', '67-schema'):
            self.assertIn(phrase, policy)
        self.assertIn('npm run contract:check', voice)
        self.assertIn('official provider', host.lower())
        self.assertIn('never', policy.lower())

    def test_british_vergil_narrator_source_and_linotype_handoff(self):
        base = ctl.SKILLS / "linotype-estate-template"
        spec = (base / "references" / "vergil-voice.md").read_text()
        entry = (base / "SKILL.md").read_text()
        frame = (base / "references" / "page-is-the-frame.md").read_text()
        handoff = (ctl.SKILLS / "teatro-scenario-composer" / "references" / "linotype-handoff.md").read_text()
        for phrase in ("The Voice of Illustrating Inferno", "British Vergil",
                       "already-available", "not a condition of use", "exact written text",
                       "AI-generated", "Zork, Bee, N.", "not an OpenAI consent script",
                       "The first drawing shows a room", "We shall not decide too early"):
            self.assertIn(phrase.lower(), spec.lower())
        self.assertIn("references/vergil-voice.md", entry)
        self.assertIn("The written page itself is the transcript", frame)
        self.assertIn("Do not add a Continuous reading mode", frame)
        self.assertIn("companion Linotype", handoff)
        self.assertIn("not Teatro's live stage sound", handoff)
        self.assertNotIn("Keep an explicit continuous-reading alternative", frame)
        self.assertNotIn("Let a synchronized or section-timed transcript compose", frame)

    def test_semantic_ink_bounds_are_independent_from_figure_outer_box(self):
        skill_root = ctl.SKILLS / "linotype-estate-template"
        entry = (skill_root / "SKILL.md").read_text()
        page = (skill_root / "references/page-is-the-frame.md").read_text()
        spec_path = skill_root / "references/semantic-illustration-ink-boundaries.md"
        self.assertTrue(spec_path.is_file())
        spec = spec_path.read_text()
        for text in (entry, page):
            self.assertIn("semantic-illustration-ink-boundaries.md", text)
        for phrase in (
            "Three separate measured boundaries",
            "Satzspiegel",
            "getBBox()",
            "visible",
            "drawn",
            "28",
            "30",
            "not universal",
            "WEB READER",
            "physical iPad",
            "source words",
            "rightInset",
        ):
            self.assertIn(phrase.lower(), spec.lower())
        self.assertIn("drawn internal rectangle", entry)
        self.assertIn("actual iPad", page)
        self.assertIn("no letters crossing", entry.lower() + " " + spec.lower())

    def test_ink_escaping_frame_is_negative_case_not_passed_css_geometry(self):
        skill_root = ctl.SKILLS / "linotype-estate-template"
        spec = (skill_root / "references/semantic-illustration-ink-boundaries.md").read_text()
        self.assertIn("1047.17", spec)
        self.assertIn("1046", spec)
        self.assertIn("outside", spec)
        self.assertIn("44", spec)
        self.assertIn("66ec9c5144953766bc99e7f9cf704b5ea17cf7a0", spec)
        self.assertIn("source", spec.lower())
        self.assertIn("not proof", spec.lower())
        handoff = (ctl.SKILLS / "teatro-scenario-composer" / "references/linotype-handoff.md").read_text()
        self.assertIn("semantic-illustration-ink-boundaries.md", handoff)
        self.assertIn("correctly aligned image element does not prove", handoff)
        self.assertIn("live Teatro execution", handoff)

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
