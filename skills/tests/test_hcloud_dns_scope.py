"""Regression: hcloud supports DNS; a missing zone in one context is not global refusal."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
DEPLOY = ROOT / ".codex/skills/estate-publisher-deployment"
AUTHORING = ROOT / ".codex/skills/fcis-skill-authoring-and-sync"


class HcloudDNSScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deploy = (DEPLOY / "SKILL.md").read_text(encoding="utf-8")
        cls.guide = (DEPLOY / "references/hcloud-dns-authority.md").read_text(encoding="utf-8")
        cls.blocker = (AUTHORING / "references/exact-blocker-continuity.md").read_text(encoding="utf-8")

    def test_cli_is_first_party_dns_tool(self):
        for keyword in ("hcloud zone", "hcloud zone rrset list",
                        "hcloud zone rrset describe", "hcloud zone rrset create"):
            self.assertIn(keyword, self.guide)
        self.assertIn("references/hcloud-dns-authority.md", self.deploy)

    def test_empty_project_is_not_global_denial(self):
        for keyword in ("Zone not found", "selected project/context",
                        "do not demonstrate", "PROJECT_SCOPE_UNVERIFIED"):
            self.assertIn(keyword.lower(), self.guide.lower())
        for keyword in ("NOT_ESTABLISHED", "not establish CLI incapability",
                        "not demand an additional API token"):
            self.assertIn(keyword.lower(), self.blocker.lower())

    def test_writes_are_bound_and_no_zone_duplication(self):
        for keyword in ("explicit exact-tuple authorization", "--name access",
                        "--type A", "--record 65.109.14.71", "--ttl 300",
                        "Never create a duplicate", "replaces all values"):
            self.assertIn(keyword.lower(), self.guide.lower())

    def test_publication_not_conflated_with_dns(self):
        for keyword in ("Caddy", "HTTPS", "FCIS CORS", "public", "staged"):
            self.assertIn(keyword, self.guide)
        self.assertIn("separately approved Caddy/HTTPS", self.deploy)


if __name__ == "__main__":
    unittest.main()
