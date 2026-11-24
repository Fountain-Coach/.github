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

    def test_business_independence_is_p0_without_vendor_execution_claims(self):
        plan = (ROOT / "PLANS.md").read_text()
        readme = (ROOT / "README.md").read_text()
        stack = (ROOT / "FCIS-STACK.md").read_text()
        provider = (ROOT / "docs/FCIS-Model-Provider-Boundary.md").read_text()
        self.assertIn("P0 — FOUNTAIN COACH BUSINESS INDEPENDENCE", plan)
        self.assertIn("Business priority P0", readme)
        self.assertIn("**Immediate priority:** Go-native production cutover", stack)
        self.assertIn("Business independence before marketplace expansion", provider)
        self.assertIn("without ChatGPT login", provider)
        self.assertIn("independently readable receipt", plan)
        self.assertIn("NOT ESTABLISHED", plan)
        self.assertIn("No architectural choice can silently widen", stack)
        self.assertIn("marketplace adapter", provider)
        self.assertIn("owner decision", provider.lower())
        # This is an instruction/priority contract, not source-level proof
        # of a released issuer, customer product or alternative LLM runtime.
        self.assertIn("not an FCIS capability guarantee", provider)

    def test_openai_projection_is_not_owner_canonical_source(self):
        import json
        import sys
        sys.path.insert(0, str(ROOT / "skills"))
        from skillctl import digest, entries
        from provider_projection import check as check_adapter
        from plugin_projection import check as check_plugin
        pub = json.loads((ROOT / "skills/fcis-go-publication.json").read_text())
        active = pub["activeSkill"]
        self.assertEqual(active["canonicalPath"], "skills/canonical/fcis-go")
        canonical = entries(ROOT / active["canonicalPath"])
        self.assertEqual(set(canonical), {"SKILL.md"})
        self.assertEqual(active["contentSHA256"], digest(canonical))
        provider = active["projections"]["openai"]
        self.assertEqual(provider["path"], ".codex/skills/fcis-go")
        projected = entries(ROOT / provider["path"])
        self.assertEqual(projected["SKILL.md"], canonical["SKILL.md"])
        self.assertEqual(provider["contentSHA256"], digest(projected))
        self.assertEqual(check_adapter(ROOT)["state"], "MATCHED")
        self.assertEqual(check_plugin(ROOT)["state"], "MATCHED")
        self.assertEqual(check_plugin(ROOT)["version"], "0.1.40")
        self.assertEqual(set(check_plugin(ROOT)["skills"]), {"fcis-go"})
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
