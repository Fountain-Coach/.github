"""Policy regression checks for the writer-adopted Fountain Press publication standard.

These assert canonical procedure consistency, not a deployed Reader, production
receipt, native iPad acceptance, or compliance certification.
"""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
LINOTYPE = ROOT / ".codex/skills/linotype-estate-template"
PUBLISHER = ROOT / ".codex/skills/estate-publisher-deployment"


def read(skill, rel):
    return (skill / rel).read_text(encoding="utf-8")


class FountainPressStandardTests(unittest.TestCase):
    def test_both_existing_skills_discover_fountain_press_release_work(self):
        for skill in (LINOTYPE, PUBLISHER):
            body = read(skill, "SKILL.md")
            self.assertTrue(body.startswith("---\nname: "))
            metadata = body.split("---", 2)[1]
            self.assertIn("Fountain Press", metadata)
            self.assertIn("staging", metadata)
            self.assertIn("production", metadata)
            self.assertIn("Fountain Press", body)

    def test_compose_once_reuse_press_reader_in_both_lanes(self):
        a = read(LINOTYPE, "SKILL.md")
        b = read(PUBLISHER, "SKILL.md")
        self.assertIn("single source-bound publication composition", a)
        self.assertIn("same reviewed composition", a)
        self.assertIn("never", b.lower())
        self.assertIn("new production Reader", b)
        self.assertIn("same Fountain Press source-bound edition", read(PUBLISHER, "references/wlan-staging.md"))
        self.assertIn("declared", read(LINOTYPE, "references/development-staging-production.md"))

    def test_owner_and_release_authorities_do_not_collapse(self):
        for skill in (LINOTYPE, PUBLISHER):
            body = read(skill, "SKILL.md")
            self.assertIn("FountainStore", body)
            self.assertIn("EstatePublisher", body)
            self.assertIn("source", body.lower())
            self.assertIn("separate", body.lower())
            self.assertIn("production", body.lower())
        self.assertIn("EstatePublisher alone", read(PUBLISHER, "SKILL.md"))
        self.assertIn("Production requires distinct approval", read(PUBLISHER, "SKILL.md"))
        self.assertIn("public production", read(PUBLISHER, "references/deployment-matrix.md"))

    def test_complete_governance_corpus_is_evidence_not_a_new_global_quota(self):
        a = read(LINOTYPE, "SKILL.md")
        b = read(PUBLISHER, "SKILL.md")
        self.assertIn("160", a)
        self.assertIn("1,132", a)
        self.assertIn("current / 88 reference", a)
        self.assertIn("not a universal required chapter count", a)
        self.assertIn("160/160", b)
        self.assertIn("not a public", b)
        self.assertIn("stage success", a.lower())

    def test_nonbook_and_private_media_remain_distinct(self):
        a = read(LINOTYPE, "SKILL.md")
        b = read(PUBLISHER, "SKILL.md")
        self.assertIn("non-book surface", a)
        self.assertIn("do not invent a book", a)
        self.assertIn("Nonbook", b)
        self.assertIn("private", b)

    def test_all_new_linked_skill_references_are_packaged(self):
        for skill in (LINOTYPE, PUBLISHER):
            text = read(skill, "SKILL.md")
            import re
            for target in re.findall(r"\]\((references/[^)#]+)", text):
                with self.subTest(skill=skill.name, path=target):
                    self.assertTrue((skill / target).is_file(), target)


if __name__ == "__main__":
    unittest.main()
