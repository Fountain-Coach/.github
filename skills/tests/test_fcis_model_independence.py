"""FCIS organization-wide requirements must not require a model vendor."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class FCISModelIndependenceTests(unittest.TestCase):
    def test_rfc_no_longer_mandates_codex(self):
        document = (ROOT / "profile/README.md").read_text()
        for prohibited in (
            "All Codex-operated repositories",
            "how OpenAI Codex is instructed",
            "Codex **SHALL NOT**",
            "FCIS treats Codex as",
            "architecture** for Codex",
            "fountain.coach Codex repositories",
        ):
            with self.subTest(prohibited=prohibited):
                self.assertNotIn(prohibited, document)
        for required in (
            "FCIS-MODEL-1",
            "**Version:** 1.5.0",
            "Provider-neutral requirements",
            "Model and Runtime Independence",
            "external",
        ):
            self.assertIn(required, document)

    def test_provider_docs_and_compliance_are_scoped(self):
        identity = (ROOT / "docs/FCIS-Name-and-Identity.md").read_text()
        boundary = (ROOT / "docs/FCIS-Model-Provider-Boundary.md").read_text()
        compliance = (ROOT / "compliance-check.md").read_text()
        ax = (ROOT / "docs/FCIS-AX-Standard.md").read_text()
        self.assertIn("FCIS-MODEL-1", identity)
        self.assertIn("does **not** own a foundation model", boundary)
        self.assertNotIn("You are Codex with", compliance)
        self.assertIn("actually supported and verified", compliance)
        self.assertIn("provider-specific projection", ax)


if __name__ == "__main__":
    unittest.main()
