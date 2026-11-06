"""Canonical Fountain Press machine-readable publication policy and validator contract.

These are source checks, not independent staging, public or API observations.
"""
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
PRESS = ROOT / ".codex/skills/linotype-estate-template"
PUBLISHER = ROOT / ".codex/skills/estate-publisher-deployment"


class AgentReadablePublicationPolicyTests(unittest.TestCase):
    def test_existing_skill_is_primary_owner(self):
        skill = (PRESS / "SKILL.md").read_text()
        self.assertIn("Agent-readable publication maintenance", skill)
        self.assertIn("references/agent-readable-publication.md", skill)
        self.assertIn("same exact authoritative edition", skill)
        self.assertIn("governance-publish", skill)
        self.assertIn("fcis-skill-authoring-and-sync", skill)
        self.assertIn("docs-sync", skill)

    def test_no_internal_repository_instruction_leak(self):
        guidance = (PRESS / "references/agent-readable-publication.md").read_text()
        self.assertIn("Internal repo", guidance)
        self.assertIn("AGENTS.md", guidance)
        self.assertIn("lower-trust", guidance)
        self.assertIn("no", guidance.lower())
        self.assertIn("72", (PRESS / "SKILL.md").read_text())

    def test_deployment_keeps_machine_and_human_same_release(self):
        skill = (PUBLISHER / "SKILL.md").read_text()
        self.assertIn("Agent-readable publication release check", skill)
        self.assertIn("same immutable Press artifact", skill)
        self.assertIn("EstatePublisher", skill)
        self.assertIn("non-browser", skill)
        self.assertIn("separate", skill.lower())

    def test_positive_negative_parity_fixtures(self):
        command = [sys.executable, str(PRESS / "scripts/test_validate_agent_publication.py")]
        run = subprocess.run(command, text=True, capture_output=True, timeout=30)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertIn("Ran 15 tests", run.stderr)

    def test_validator_is_stdlib_and_has_no_publication_effect(self):
        script = (PRESS / "scripts/validate_agent_publication.py").read_text()
        self.assertIn("runtimeAndPublicationAuthorityVerified", script)
        self.assertIn("False", script)
        self.assertNotIn("requests.", script)
        self.assertNotIn("subprocess.", script)


if __name__ == "__main__":
    unittest.main()
