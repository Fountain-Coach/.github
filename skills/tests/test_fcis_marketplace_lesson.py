"""Regression contract for the accepted ChatGPT marketplace import lesson."""
from pathlib import Path
import unittest

BASE = Path(__file__).resolve().parents[2] / ".codex/skills/fcis-skill-authoring-and-sync"


class FcisMarketplaceLessonTests(unittest.TestCase):
    def test_lesson_link_and_trigger(self):
        skill = (BASE / "SKILL.md").read_text()
        self.assertIn("marketplace import", skill.lower())
        self.assertIn("references/chatgpt-github-marketplace-takeover.md", skill)

    def test_observed_workflow_and_failure_boundaries(self):
        lesson = (BASE / "references/chatgpt-github-marketplace-takeover.md").read_text()
        for phrase in (
            "Marketplace importieren",
            "Marktplätze → Hinzufügen",
            "Auto-Synchronisierung",
            "INSTALLED_NOT_SYNCHRONIZED",
            "HOSTED_UNVERIFIED",
            "Jetzt synchronisieren",
            "Plugins → Workspace",
            "Plugin-Aktionen → Plugin löschen",
            "plugins_upstream_failure",
            "two distinct plugins",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, lesson)

    def test_github_backed_skill_does_not_fall_back_to_zip_delivery(self):
        skill = (BASE / "SKILL.md").read_text()
        agent = (BASE / "agents" / "openai.yaml").read_text()
        self.assertIn("do not package, attach, offer, or recommend a `skill.zip`", skill)
        self.assertIn("Generic Skill Creator packaging guidance is non-authoritative here", skill)
        self.assertIn("never return or recommend skill.zip as the normal deliverable", agent)

    def test_reference_is_not_an_installation_specific_template(self):
        lesson = (BASE / "references/chatgpt-github-marketplace-takeover.md").read_text()
        self.assertNotIn("Plugin_fb9e0937c59c8191b9fa077fa5ea53ef", lesson)
        self.assertIn("pluginId", lesson)
        self.assertIn("plugin.json", lesson)


if __name__ == "__main__":
    unittest.main()
