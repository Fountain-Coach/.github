"""Governed sixth Skill: owner WebAuthn, recovery and current authority remain distinct."""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / ".codex/skills/fcis-owner-access/SKILL.md"
MATRIX = ROOT / ".codex/skills/fcis-owner-access/references/acceptance.md"

class OwnerAccessSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = SKILL.read_text()
        cls.matrix = MATRIX.read_text()
        cls.catalog = json.loads((ROOT / "skills/openai-distribution.json").read_text())

    def test_only_one_canonical_owner_skill_inside_six(self):
        self.assertEqual(len(self.catalog["skills"]), 6)
        names = [x["name"] for x in self.catalog["skills"]]
        self.assertEqual(names.count("fcis-owner-access"), 1)
        self.assertIn("fcis-owner-access", names)
        self.assertIn("fcis-owner-access", (ROOT / "skills/plugin_projection.py").read_text())

    def test_governance_interlinks_and_design_source(self):
        for slug in ("07-agent-operating-guide", "08-validation-and-acceptance",
                     "142-fountainauthkit-governed-authorization-authority",
                     "152-the-host-is-the-instrument",
                     "161-host-enrollment-client-consent-and-access-management"):
            self.assertIn("governance.fountain.coach/chapters/" + slug, self.body)
        self.assertIn("access-passkey-first-owner-signin-2026-11-12.md", self.body)

    def test_web_authn_and_browser_session_security(self):
        for term in ("challenge", "Relying Party ID", "origin", "signature",
                     "user verification", "RFC 9700", "RFC 10017",
                     "HttpOnly", "CSRF", "SameSite"):
            self.assertIn(term, self.body)

    def test_recovery_and_fidelity(self):
        for term in ("second usable authenticator", "existing ChatGPT grant",
                     "read-only snapshot", "existing issuer subject",
                     "physical", "MCP denied"):
            self.assertIn(term, self.body)

    def test_no_second_identity_or_zip(self):
        for term in ("not a new Kit", "no extra issuer", "No skill.zip"):
            self.assertTrue(term.lower() in self.body.lower() or
                            term.lower() in self.matrix.lower())
        self.assertIn("single GitHub-backed Fountain Coach FCIS plugin", self.body)

    def test_negative_acceptance_matrix(self):
        for term in ("wrong", "revoked", "expired", "CSRF", "lost", "iPad"):
            self.assertIn(term.lower(), self.matrix.lower())

    def test_internal_fcis_openapi_maintenance_is_part_of_existing_skill(self):
        reference = (ROOT / ".codex/skills/fcis-owner-access/references/openapi-maintenance.md").read_text()
        metadata = (ROOT / ".codex/skills/fcis-owner-access/agents/openai.yaml").read_text()
        self.assertIn("internal FCIS owner OpenAPI 3.1 contract", self.body)
        self.assertIn("references/openapi-maintenance.md", self.body)
        self.assertIn("OpenAPI 3.1", metadata)
        self.assertIn("FCIS OpenAPI maintenance protocol", self.matrix)
        self.assertIn("not a new FCIS-KIT capability", reference)
        self.assertEqual(len(self.catalog["skills"]), 6)

    def test_openapi_existing_sources_versions_and_native_contract_checks(self):
        ref = (ROOT / ".codex/skills/fcis-owner-access/references/openapi-maintenance.md").read_text()
        for required in (
            "contracts/fcis-owner.openapi.json",
            "FountainHostMCPOAuthHandler",
            "FountainHostMachineEnrollment",
            "FountainHostOwnerPairing",
            "FountainHostMCPAuthorizationRevoke",
            "node --test apps/estate-publisher/Tests/fcis-owner-openapi.test.mjs",
            "swift test --package-path apps/estate-publisher",
            "FountainHost(OwnerOpenAPIContract|OwnerTarget|OwnerPairingHTTP|MCPAuthorizationOwnerHTTP|MachineEnrollment)Tests",
            "git diff --check",
            "info.version",
            "x-fcis-not-admitted"
        ):
            self.assertIn(required, ref)

    def test_openapi_refuses_fabricated_scope_and_release_claims(self):
        ref = (ROOT / ".codex/skills/fcis-owner-access/references/openapi-maintenance.md").read_text()
        for required in (
            "approved-pending-channel",
            "authorizationState=verified",
            "host.describe?inventory=1",
            "passkey",
            "Origin",
            "Cookie",
            "Authorization",
            "Foundation reference-date seconds",
            "404",
            "signed issuer/Caddy",
            "physical-iPad acceptance",
        ):
            self.assertIn(required.lower(), ref.lower())

    def test_openapi_avoids_replacing_upstream_or_Kit_contracts(self):
        ref = (ROOT / ".codex/skills/fcis-owner-access/references/openapi-maintenance.md").read_text()
        self.assertIn("FCIS-Official-OpenAPI-Dependency.md", ref)
        self.assertIn("generated-contract-regeneration", ref)
        self.assertIn("not a new FCIS-KIT capability", ref)


if __name__ == "__main__":
    unittest.main()
