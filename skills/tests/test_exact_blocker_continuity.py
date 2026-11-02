"""Regression gates: exact blocker != untested upstream eligibility."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / ".codex/skills/fcis-skill-authoring-and-sync"


class ExactBlockerContinuityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL / "SKILL.md").read_text()
        cls.ref = (SKILL / "references/exact-blocker-continuity.md").read_text()

    def test_existing_skill_not_duplicate(self):
        self.assertIn("references/exact-blocker-continuity.md", self.skill)
        self.assertIn("NOT_ESTABLISHED", self.skill)
        self.assertIn("non-admitted candidate", self.skill)
        self.assertIn("separately reviewed", self.skill)

    def test_original_goal_is_still_native_ipad_and_mac(self):
        for text in ("native Reframe Composer", "macOS", "physical iPad",
                     "ChatGPT subscription", "no OpenAI API key",
                     "no silent paid fallback"):
            self.assertIn(text, self.ref)

    def test_exact_refusal_not_provider_denial(self):
        for text in ("BLOCKED_TOOL_EXECUTION", "NOT_ESTABLISHED",
                     "not `blocked_access_denied`", "security checks",
                     "typecheck", "no OpenAI sign-in callback"):
            # Name the evidence and the particular operation;
            # never turn a denied local tool call into a denied model grant.
            self.assertIn(text.lower(), self.ref.lower())

    def test_no_false_elevation_or_install(self):
        for text in ("auto_elevate.py", "non-admitted",
                     "no accepted terminal witness",
                     "Mac accepted MCP tool execution",
                     "persisted execution evidence", "PR #96", "PR #97"):
            self.assertIn(text.lower(), self.ref.lower())


if __name__ == "__main__":
    unittest.main()
