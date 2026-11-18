"""Canonical FCIS Go HTTP API: one organization peer to FCIS-STACK.md.

This is source/schema validation only: never certifies a deployed Go service.
"""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
OPENAPI = ROOT / "FCIS-OPENAPI.json"
STACK = ROOT / "FCIS-STACK.md"
OWNER_SKILL = ROOT / ".codex/skills/fcis-owner-access/SKILL.md"
GO_SKILL = ROOT / ".codex/skills/fcis-go-runtime-migration/SKILL.md"

METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
PREDECESSOR = {
    ("get", "/oauth/owner/hosts"): "readOwnerFleet",
    ("get", "/oauth/owner/host/describe"): "describeSelectedHost",
    ("post", "/oauth/owner/hosts/pair/begin"): "beginHostPair",
    ("get", "/oauth/owner/hosts/pair/status"): "readHostPairStatus",
    ("post", "/oauth/owner/hosts/pair/decide"): "decideHostPair",
    ("post", "/oauth/host/enrollment/prove"): "submitSignedMachinePairProof",
    ("post", "/oauth/host/enrollment/activate"): "activatePretrustedMachine",
    ("get", "/oauth/owner/grants"): "readOwnerGrants",
    ("post", "/oauth/owner/revoke"): "revokeOwnerGrant",
    ("get", "/oauth/owner/reference/openapi"): "readOwnerOpenAPIReference",
}
REQUIRED_GO = {
    ("get", "/.well-known/oauth-authorization-server"),
    ("get", "/.well-known/oauth-protected-resource"),
    ("get", "/.well-known/jwks.json"),
    ("post", "/oauth/register"),
    ("get", "/oauth/authorize"),
    ("post", "/oauth/authorize"),
    ("post", "/oauth/token"),
    ("get", "/oauth/owner/passkeys/login"),
    ("post", "/oauth/owner/passkeys/login/options"),
    ("post", "/oauth/owner/passkeys/login/verify"),
    ("post", "/oauth/owner/passkeys/enroll/options"),
    ("post", "/oauth/owner/passkeys/enroll/verify"),
    ("post", "/oauth/owner/passkeys/logout"),
    ("post", "/mcp"),
    ("post", "/oauth/host/instruments/discover"),
    ("post", "/oauth/host/grants/renew"),
    ("post", "/oauth/host/session/frame"),
    ("post", "/oauth/host/channel/probe"),
    ("get", "/oauth/owner/hosts/channel/status"),
}


def all_refs(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "$ref":
                yield value
            else:
                yield from all_refs(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from all_refs(item)


class FCISRootOpenAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = json.loads(OPENAPI.read_text(encoding="utf-8"))
        cls.stack = STACK.read_text(encoding="utf-8")

    def test_canonical_peer_authority(self):
        api = self.api
        self.assertEqual(api["openapi"], "3.1.0")
        self.assertEqual(api["x-fcis-canonical-authority"],
                         "Fountain-Coach/.github/FCIS-OPENAPI.json")
        self.assertEqual(api["x-fcis-peer-spec"], "FCIS-STACK.md")
        self.assertIn("FCIS-OPENAPI.json", self.stack)
        self.assertIn("FCIS-OPENAPI.json", OWNER_SKILL.read_text())
        self.assertIn("FCIS-OPENAPI.json", GO_SKILL.read_text())
        self.assertTrue(api["x-fcis-relationship"]["notProductionProof"])
        self.assertIn("not", api["x-fcis-specification-state"].lower())

    def test_all_operations_are_named_typed_and_source_only(self):
        found = {}
        for path, methods in self.api["paths"].items():
            self.assertTrue(path.startswith("/") and not path.startswith("//"))
            for method, op in methods.items():
                if method not in METHODS:
                    continue
                self.assertTrue(op["operationId"])
                self.assertTrue(op["summary"])
                self.assertTrue(op["description"])
                self.assertTrue(op["responses"])
                self.assertEqual(op["x-fcis-go-target-state"],
                                 "specified-only-not-deployed")
                self.assertEqual(op["x-fcis-production-state"],
                                 "NOT_ESTABLISHED_GO")
                self.assertEqual(op["x-fcis-implementation-state"],
                                 "go-target-specified-only")
                for p in op.get("parameters", []):
                    self.assertIs(type(p["required"]), bool,
                                  f"{method} {path} {p.get('name')}")
                    self.assertIn("schema", p)
                ident = op["operationId"]
                self.assertNotIn(ident, found, f"duplicate operationId {ident}")
                found[ident] = (method, path)
        self.assertGreaterEqual(len(found), 30)

    def test_all_schema_and_security_references_resolve(self):
        api = self.api
        for target in all_refs(api):
            self.assertTrue(target.startswith("#/"), target)
            node = api
            for fragment in target[2:].split("/"):
                node = node[fragment.replace("~1", "/").replace("~0", "~")]
            self.assertIsNotNone(node)
        schemes = api["components"]["securitySchemes"]
        self.assertNotIn("legacyOwnerBasic", schemes)
        for route, methods in api["paths"].items():
            for method, op in methods.items():
                if method not in METHODS:
                    continue
                for security in op.get("security", []):
                    self.assertTrue(set(security).issubset(schemes),
                                    f"undefined scheme for {method} {route}")

    def test_predecessor_preserved_but_noncanonical(self):
        api = self.api
        self.assertEqual(api["x-fcis-predecessor"]["operations"], 10)
        self.assertEqual(api["x-fcis-predecessor"]["version"], "0.2.1")
        for (method, path), identifier in PREDECESSOR.items():
            self.assertEqual(api["paths"][path][method]["operationId"],
                             identifier)
            self.assertIn("x-fcis-predecessor-operation",
                          api["paths"][path][method])
        self.assertIn("historical", api["x-fcis-predecessor"]["authority"])
        self.assertNotIn("enum",
                         api["components"]["schemas"]["OwnerFleetHost"]["properties"]
                         ["capabilities"]["items"])

    def test_go_surface_and_separate_instrument_authority(self):
        for method, path in REQUIRED_GO:
            self.assertIn(method, self.api["paths"][path])
        self.assertEqual(self.api["paths"]["/mcp"]["post"]["security"],
                         [{"oauthBearer": []}])
        for route in ("/oauth/host/instruments/discover",
                      "/oauth/host/grants/renew",
                      "/oauth/host/session/frame"):
            self.assertTrue(self.api["paths"][route]["post"]
                            ["x-fcis-machine-signed-body"])
        self.assertNotIn("/stripe", self.api["paths"])
        self.assertNotIn("/payment", self.api["paths"])
        for tag in ("ownerBootstrap", "fountainStore", "midi2", "instrument",
                    "payment"):
            self.assertIn(tag, self.api["x-fcis-non-http-contracts"])

    def test_machine_enrollment_uses_signed_body_not_owner_passkey(self):
        for route in ("/oauth/host/enrollment/prove",
                      "/oauth/host/enrollment/activate"):
            op = self.api["paths"][route]["post"]
            self.assertEqual(op["security"], [])
            self.assertTrue(op["x-fcis-machine-signed-body"])
            self.assertTrue(op["requestBody"]["required"])
            self.assertIn("Origin", op["requestBody"]["description"])
            self.assertIn("Cookie", op["requestBody"]["description"])
            self.assertIn("Authorization", op["requestBody"]["description"])
            self.assertNotIn("owner passkey required",
                             " ".join(r["description"] for r in op["responses"].values()).lower())
        proof = self.api["paths"]["/oauth/host/enrollment/prove"]["post"]
        self.assertIn("device-signed proof",
                      proof["responses"]["401"]["description"])

    def test_european_regulatory_maintenance_is_non_http_and_evidence_scoped(self):
        policy = ROOT / "docs/FCIS-EU-Regulatory-Maintenance.md"
        self.assertTrue(policy.is_file())
        body = policy.read_text(encoding="utf-8")
        self.assertIn("FCIS-EU-Regulatory-Maintenance.md", self.stack)
        extension = self.api["x-fcis-regulatory-maintenance"]
        self.assertEqual(extension["policy"], "docs/FCIS-EU-Regulatory-Maintenance.md")
        self.assertTrue(extension["doesNotExpandCutoverDoD"])
        self.assertIn("regulatoryMaintenance", self.api["x-fcis-non-http-contracts"])
        self.assertTrue({"GDPR", "ePrivacy", "NIS2", "AI Act", "Cyber Resilience Act", "eIDAS"}.issubset(set(re.findall(r"GDPR|ePrivacy|NIS2|AI Act|Cyber Resilience Act|eIDAS", body))))
        self.assertIn("monthly", body.lower())
        self.assertIn("requires_review", body)
        self.assertNotIn("/regulation", self.api["paths"])
        self.assertNotIn("/compliance", self.api["paths"])

    def test_skills_are_mirrored_in_single_existing_plugin(self):
        for name in ("fcis-owner-access", "fcis-go-runtime-migration"):
            canonical = ROOT / ".codex" / "skills" / name
            derived = ROOT / "plugins/fcis-skill-authoring-and-sync/skills" / name
            files = {p.relative_to(canonical) for p in canonical.rglob("*")
                     if p.is_file()}
            self.assertEqual(files, {p.relative_to(derived)
                                     for p in derived.rglob("*") if p.is_file()})
            for path in files:
                self.assertEqual((canonical / path).read_bytes(),
                                 (derived / path).read_bytes())


if __name__ == "__main__":
    unittest.main()
