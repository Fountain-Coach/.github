"""Canonical FCIS Go HTTP API: one organization peer to FCIS-STACK.md.

This is source/schema validation only: never certifies a deployed Go service.
"""
import json
import hashlib
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


# Immutable 0.4.0 compatibility baseline (organization commit 57d7470).
BASELINE_PATHS = ['/oauth/owner/hosts', '/oauth/owner/host/describe', '/oauth/owner/hosts/pair/begin', '/oauth/owner/hosts/pair/status', '/oauth/owner/hosts/pair/decide', '/oauth/host/enrollment/prove', '/oauth/host/enrollment/activate', '/oauth/owner/grants', '/oauth/owner/revoke', '/oauth/owner/reference/openapi', '/.well-known/oauth-authorization-server', '/.well-known/oauth-protected-resource', '/.well-known/jwks.json', '/oauth/register', '/oauth/authorize', '/oauth/token', '/oauth/owner/passkeys/login', '/oauth/owner/passkeys/login/options', '/oauth/owner/passkeys/enroll/options', '/oauth/owner/passkeys/login/verify', '/oauth/owner/passkeys/enroll/verify', '/oauth/owner/passkeys/logout', '/mcp', '/healthz', '/oauth/host/instruments/discover', '/oauth/host/grants/renew', '/oauth/host/channel/probe', '/oauth/host/session/frame', '/oauth/owner/hosts/channel/status']
BASELINE_SCHEMAS = ['HostTargetID', 'FoundationDateSeconds', 'OwnerError', 'OwnerFleetHost', 'OwnerFleetInventory', 'HostObservation', 'PairBeginRequest', 'PairStart', 'PairStatus', 'PairDecisionRequest', 'PairProofRequest', 'MachineActivationRequest', 'MachineAdmissionReceipt', 'OwnerGrant', 'OwnerGrantOverview', 'OwnerRevokeRequest', 'OwnerRevokeReceipt', 'OwnerOpenAPIDocument', 'OAuthServerMetadata', 'ProtectedResourceMetadata', 'JSONWebKeySet', 'OAuthClientRegistration', 'OAuthClientRegistrationResult', 'OAuthTokenResult', 'OAuthError', 'PasskeyOptions', 'PasskeyCredentialAssertion', 'OwnerSessionResult', 'MCPJSONRPCRequest', 'MCPJSONRPCResponse', 'MachineSignedRequest', 'MachineGrantReceipt', 'HostInstrumentDiscovery', 'HostChannelProbe', 'HostSessionFrame', 'HealthStatus', 'FirstOwnerPasskeyAttestation', 'FirstOwnerBootstrapPolicy']
BASELINE_PATHS_SHA256 = '7290559144cda7d4b9d841e02233f86f96df8b2b5a8bfba1fb5af77b2548e940'
BASELINE_SCHEMAS_SHA256 = '043bc5c7c4909532590c50d6482ddcd99158d0ceaffce7444b7dc99ec080eed2'
BASELINE_SECURITY_SHA256 = '5ea921ceb9f07831cfb465dc09ad3f1cc511dc7b04e69ada9df813aaa5e24221'


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

    def test_one_active_skill_and_maintained_owner_openapi_sources(self):
        parent = ROOT / "plugins/fcis-skill-authoring-and-sync/skills"
        self.assertEqual([p.name for p in parent.iterdir()], ["fcis-go"])
        for name in ("fcis-owner-access", "fcis-go-runtime-migration"):
            canonical = ROOT / ".codex" / "skills" / name
            self.assertTrue((canonical / "SKILL.md").is_file())
            self.assertFalse((parent / name).exists())


    def test_admin_api_050_preserves_040_http_contract(self):
        def digest(value):
            return hashlib.sha256(json.dumps(value, sort_keys=True,
                separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
        a = self.api
        self.assertEqual(a["info"]["version"], "0.9.14")
        page = a["components"]["schemas"]["OwnerReasoningClientPage"]
        self.assertNotIn("instrumentObservations", page["required"])
        self.assertEqual(page["properties"]["items"]["items"], {"$ref": "#/components/schemas/OwnerReasoningClient"})
        observation = a["components"]["schemas"]["OwnerInstrumentObservation"]
        self.assertFalse(observation["additionalProperties"])
        self.assertEqual(set(observation["required"]), set(observation["properties"]))
        self.assertEqual(observation["properties"]["admission"], {"const": "not-established"})
        self.assertEqual(observation["properties"]["callable"], {"const": False})
        self.assertEqual(observation["properties"]["reasoningEligible"], {"const": False})
        # Preserve every predecessor operation byte-semantically except the
        # reviewed status GET Origin clarification. Restore that exact two-field
        # delta before comparing the original 0.4.0 compatibility digest.
        baseline = json.loads(json.dumps({p: a["paths"][p] for p in BASELINE_PATHS}))
        origin = baseline["/oauth/owner/hosts/pair/status"]["get"]["parameters"][0]
        self.assertEqual(origin["name"], "Origin")
        self.assertIs(origin["required"], False)
        self.assertEqual(origin["description"], "Read-only status: require the exact issuer Origin, or absent Origin only with browser Fetch Metadata same-origin, cors, empty destination and the exact issuer Host. A foreign or ambiguous Origin is refused. A current owner passkey session is still required. Mutation Origin and intent requirements are unchanged.")
        origin["required"] = True
        origin["description"] = "Exact browser Origin must be on the issuer allowlist. No Origin is a 403 on owner pairing routes."
        # The two formerly specified-only contact operations accidentally
        # promised a host.describe job. Restore only their reviewed response
        # description/schema delta for the immutable predecessor comparison.
        for path, method, old, new in (
            ("/oauth/host/channel/probe", "post",
             "Authenticated target result; execution and admission still separately verified",
             "Durable issuer readback of one authenticated outbound machine contact; not Host admission or execution"),
            ("/oauth/owner/hosts/channel/status", "get",
             "Store-correlated last channel witness",
             "Last persisted and reverified signed contact receipt for the owner-bound pairing; not current reachability or execution"),
        ):
            r = baseline[path][method]["responses"]["200"]
            self.assertEqual(r["description"], new)
            self.assertEqual(r["content"]["application/json"]["schema"], {"$ref": "#/components/schemas/HostChannelReceipt"})
            r["description"] = old
            r["content"]["application/json"]["schema"] = {"$ref": "#/components/schemas/HostObservation"}
        witness = a["components"]["schemas"]["HostChannelReceipt"]
        self.assertFalse(witness["additionalProperties"])
        self.assertEqual(set(witness["required"]), {"id", "requestID", "targetID", "machine", "artifactDigest", "machineKeyFingerprint", "nonce", "signedAtSeconds", "observedAt", "state", "terminal", "evidence"})
        self.assertEqual(witness["properties"]["state"], {"const": "channel-observed-unadmitted"})
        self.assertEqual(witness["properties"]["terminal"], {"const": True})
        self.assertEqual(witness["properties"]["observedAt"], {"$ref": "#/components/schemas/FoundationDateSeconds"})
        # Reviewed 0.8.0 delta: the existing issuer accepts the separately
        # consented Skill audience, not a new authentication mechanism.
        resource = next(p for p in baseline["/oauth/authorize"]["get"]["parameters"] if p["name"] == "resource")
        self.assertEqual(resource["description"], "Exact FCIS resource URL: /mcp (existing default when omitted), explicit /oauth/skills, or the separate configured HTTPS /access/v1/evaluation for authzen.evaluate; no audience substitution.")
        resource["description"] = "Exact FCIS MCP resource URL"
        # Reviewed 0.8.2 delta: additive metadata, never a registration grant.
        registration = baseline["/oauth/register"]["post"]
        self.assertTrue(registration["description"].startswith("Dynamic client registration; server validates exact redirect schemes/origins. Registration is not an execution grant."))
        registration["description"] = "Dynamic client registration; server validates exact redirect schemes/origins. Registration is not an execution grant."
        schemas = json.loads(json.dumps({n: a["components"]["schemas"][n] for n in BASELINE_SCHEMAS}))
        for name in ("token_endpoint_auth_method", "grant_types", "response_types", "scope"):
            del schemas["OAuthClientRegistration"]["properties"][name]
        for name in ("client_name", "grant_types", "response_types"):
            del schemas["OAuthClientRegistrationResult"]["properties"][name]
        schemas["OAuthClientRegistrationResult"]["required"] = ["client_id", "redirect_uris"]
        del schemas["OAuthServerMetadata"]["properties"]["scopes_supported"]
        del schemas["ProtectedResourceMetadata"]["properties"]["bearer_methods_supported"]
        # Reviewed 0.9.2 extension: conditional Voice-only bearer and signed
        # machine binding. Normalize ONLY those reviewed additions for the
        # immutable compatibility digest; leave every other old field checked.
        frame = baseline["/oauth/host/session/frame"]["post"]
        old_description = "Only admitted target and authenticated session/sequence/nonce permitted. Typed Host frame is not arbitrary remote shell, and response requires actual terminal evidence."
        self.assertTrue(frame["description"].startswith(old_description + " Existing Describe and Go Build session modes are unchanged."))
        frame["description"] = old_description
        self.assertEqual(frame["security"], [{}, {"oauthBearer": []}])
        frame["security"] = []
        self.assertIn("Authorization MUST be absent for existing Describe and Go Build modes", frame["requestBody"]["description"])
        frame["requestBody"]["description"] = "Machine-signed JSON body; Origin, Cookie and Authorization MUST be absent"
        self.assertTrue(frame.pop("x-fcis-voice-session-mode")["requiresExplicitOwnerPeerAdmission"])
        del schemas["HostSessionFrame"]["properties"]["sessionID"]["description"]
        # Reviewed 0.9.3 additive owner bridge projection on the existing resource.
        baseline["/oauth/owner/grants"].pop("post")
        for key in ("capabilityScopes", "policyRevision"):
            schemas["OwnerGrant"]["properties"].pop(key)
        bridge = baseline["/mcp"]["post"]
        self.assertEqual(bridge.pop("x-fcis-connect")["externalScope"], "fcis.connect")
        old_mcp = "JSON-RPC initialize, ping, tools/list and tools/call over MCP Streamable HTTP. Method-specific capability dispatch and typed instrument constraints are owned by admitted FCIS-KIT runtime, not this OpenAPI. Client bearer scope and current Host admission must be enforced."
        self.assertTrue(bridge["description"].startswith(old_mcp + " Connect"))
        del bridge["responses"]["401"]["headers"]
        bridge["description"] = old_mcp
        self.assertEqual(digest(baseline), BASELINE_PATHS_SHA256)
        self.assertEqual(digest(schemas), BASELINE_SCHEMAS_SHA256)
        self.assertEqual(digest(a["components"]["securitySchemes"]), BASELINE_SECURITY_SHA256)
        self.assertEqual(sum(len(v) for v in a["paths"].values()), 71)

    def test_voice_composer_projection_remains_private_and_owner_mediated(self):
        a = self.api
        base = "/oauth/owner/conversations/{conversationId}/voices"
        for path, method, operation, intent in (
            (base, "get", "readOwnerVoiceComposition", None),
            (base, "post", "arrangeOwnerVoices", "fountaincoach/voice.arrange"),
            (base + "/admissions", "post", "decideOwnerVoiceAdmission", "fountaincoach/voice.admit"),
        ):
            op = a["paths"][path][method]
            self.assertEqual(op["operationId"], operation)
            self.assertEqual(op["security"], [{"ownerPasskeySession": []}])
            self.assertEqual(op["x-fcis-go-target-state"], "specified-only-not-deployed")
            for r in op["responses"].values():
                self.assertEqual(r["headers"]["Cache-Control"]["schema"]["const"], "no-store")
            if intent is not None:
                self.assertEqual(op["x-fcis-owner-intent"], intent)
                headers = {x["name"]: x for x in op["parameters"] if x["in"] == "header"}
                self.assertTrue(headers["Origin"]["required"])
                self.assertEqual(headers["X-Fountain-Owner-Intent"]["schema"]["const"], intent)
        schemas = a["components"]["schemas"]
        for name in ("OwnerVoiceComposition", "OwnerVoiceArrangementCreate", "OwnerVoiceAdmissionDecision"):
            self.assertFalse(schemas[name]["additionalProperties"])
            self.assertEqual(set(schemas[name]["required"]), set(schemas[name]["properties"]) - ({"contentExchange", "peerTargetId"} if name == "OwnerVoiceAdmissionDecision" else set()))

    def test_native_voice_carrier_does_not_widen_legacy_machine_authority(self):
        a = self.api
        op = a["paths"]["/oauth/host/session/frame"]["post"]
        mode = op["x-fcis-voice-session-mode"]
        self.assertTrue(op["x-fcis-machine-signed-body"])
        self.assertTrue(mode["requiresMachineSignature"])
        self.assertTrue(mode["requiresCurrentScopedBearer"])
        self.assertTrue(mode["requiresExplicitOwnerPeerAdmission"])
        self.assertEqual(mode["legacyAuthorizationHeader"], "forbidden")
        self.assertTrue(mode["carrierOnly"])
        for name in ("OwnerVoiceAdmissionDecision", "OwnerVoiceAdmission"):
            schema = a["components"]["schemas"][name]
            self.assertNotIn("peerTargetId", schema["required"])
            self.assertEqual(schema["properties"]["peerTargetId"]["$ref"], "#/components/schemas/HostTargetID")

    def test_voice_text_exchange_is_explicit_and_additive(self):
        schemas = self.api["components"]["schemas"]
        for name in ("OwnerVoiceAdmission", "OwnerVoiceAdmissionDecision"):
            schema = schemas[name]
            self.assertNotIn("contentExchange", schema["required"])
            self.assertEqual(schema["properties"]["contentExchange"]["type"], "boolean")
        contribution = schemas["OwnerVoiceContribution"]
        self.assertNotIn("clientText", contribution["required"])
        self.assertEqual(contribution["properties"]["clientText"]["type"], "string")
        self.assertEqual(sum(len(v) for v in self.api["paths"].values()), 71)

    def test_dcr_public_client_metadata_profile_is_additive_not_authority(self):
        a = self.api
        schemas = a["components"]["schemas"]
        req = schemas["OAuthClientRegistration"]
        result = schemas["OAuthClientRegistrationResult"]
        self.assertFalse(req["additionalProperties"])
        self.assertEqual(req["required"], ["redirect_uris"])
        self.assertEqual(set(req["properties"]), {"redirect_uris", "client_name", "token_endpoint_auth_method", "grant_types", "response_types", "scope"})
        self.assertEqual(req["properties"]["token_endpoint_auth_method"]["const"], "none")
        self.assertEqual(req["properties"]["grant_types"]["contains"], {"const": "authorization_code"})
        self.assertTrue(req["properties"]["grant_types"]["uniqueItems"])
        self.assertEqual(req["properties"]["response_types"]["items"], {"type": "string", "const": "code"})
        pattern = req["properties"]["scope"]["pattern"]
        self.assertIsNotNone(re.fullmatch(pattern, "authzen.evaluate"))
        self.assertIsNone(re.fullmatch(pattern, "fcis.connect authzen.evaluate"))
        self.assertIsNone(re.fullmatch(pattern, "authzen.evaluate host.describe"))
        self.assertEqual(result["properties"]["grant_types"]["const"], ["authorization_code", "refresh_token"])
        self.assertEqual(result["properties"]["response_types"]["const"], ["code"])
        self.assertFalse({"scope", "access_token", "refresh_token", "client_secret"} & set(result["properties"]))
        self.assertEqual(a["paths"]["/oauth/register"]["post"]["security"], [])
        self.assertIn("explicit resource-bound owner consent", a["paths"]["/oauth/register"]["post"]["description"])

    def test_skill_admin_and_delivery_security_are_separate(self):
        operations = [(path, method, op) for path, methods in self.api["paths"].items()
                      for method, op in methods.items() if method in METHODS and "x-fcis-phase" in op]
        self.assertEqual(len(operations), 22)
        for path, method, op in operations:
            with self.subTest(operation=op["operationId"]):
                params = op.get("parameters", [])
                placeholders = set(re.findall(r"\{([^}]+)\}", path))
                self.assertEqual(placeholders, {p["name"] for p in params if p["in"] == "path"})
                self.assertTrue(all(p["required"] for p in params if p["in"] == "path"))
                if path.startswith("/oauth/owner/"):
                    self.assertEqual(op["security"], [{"ownerPasskeySession": []}])
                    if method == "post":
                        headers = {p["name"]: p for p in params if p["in"] == "header"}
                        self.assertTrue(headers["Origin"]["required"])
                        h = headers["X-Fountain-Owner-Intent"]
                        self.assertTrue(h["required"])
                        self.assertEqual(h["schema"]["const"], op["x-fcis-owner-intent"])
                elif path.startswith("/oauth/skills/"):
                    self.assertEqual(op["security"], [{"oauthBearer": []}])
                    self.assertEqual(op["x-fcis-resource"], "{issuerOrigin}/oauth/skills")
                    self.assertIn(op["x-fcis-required-scope"], ("skills.read", "skills.acquire", "skills.owned.read"))
                    self.assertIn("WWW-Authenticate", op["responses"]["401"]["headers"])
                else:
                    self.assertIn(path, ("/catalog/skills", "/.well-known/oauth-protected-resource/oauth/skills"))
                    self.assertEqual(method, "get")
                    self.assertEqual(op["security"], [])
                if path.startswith("/oauth/"):
                    for response in op["responses"].values():
                        self.assertEqual(response["headers"]["Cache-Control"]["schema"]["const"], "no-store")
                if method == "post":
                    self.assertTrue(op["requestBody"]["required"])
        self.assertEqual(sum(op["x-fcis-phase"] == "skill-management" for _, _, op in operations), 7)
        self.assertEqual(self.api["paths"]["/oauth/skills/releases/{releaseId}"]["get"]["x-fcis-required-scope"], "skills.read")

    def test_owned_active_skill_resource_is_independent_and_current_only(self):
        paths = self.api["paths"]
        owned = [(p, v["get"]) for p, v in paths.items() if p.startswith("/oauth/skills/owned")]
        self.assertEqual(len(owned), 3)
        for path, op in owned:
            self.assertEqual(op["security"], [{"oauthBearer": []}])
            self.assertEqual(op["x-fcis-resource"], "{issuerOrigin}/oauth/skills")
            self.assertEqual(op["x-fcis-required-scope"], "skills.owned.read")
            self.assertEqual(op["x-fcis-go-target-state"], "specified-only-not-deployed")
            self.assertEqual(list(paths[path]), ["get"])
        schemas = self.api["components"]["schemas"]
        entry = schemas["OwnedActiveSkillEntry"]["properties"]
        self.assertEqual(entry["draftHead"], {"type": "null"})
        self.assertEqual(entry["activeReleaseId"]["type"], "string")
        detail = schemas["OwnedActiveSkillDetail"]["properties"]
        self.assertEqual(detail["drafts"]["maxItems"], 0)
        self.assertEqual(detail["releases"]["maxItems"], 1)
        self.assertEqual(detail["releases"]["minItems"], 1)
        self.assertEqual(detail["nextCursor"], {"type": "null"})
        delivery = paths["/oauth/skills/owned/{skillName}/releases/{releaseId}"]["get"]
        self.assertTrue(delivery["responses"]["200"]["headers"]["X-FCIS-Receipt-ID"]["required"])
        self.assertIn("409", delivery["responses"])
        self.assertEqual(paths["/oauth/skills/releases/{releaseId}"]["get"]["x-fcis-required-scope"], "skills.read")
        self.assertEqual(paths["/oauth/owner/skills"]["get"]["security"], [{"ownerPasskeySession": []}])
        self.assertEqual(set(schemas["SkillProtectedResourceMetadata"]["properties"]["scopes_supported"]["items"]["enum"]), {"skills.read", "skills.acquire", "skills.owned.read"})
        self.assertIn("future active revisions", self.api["x-fcis-skill-distribution"]["clientResource"])

    def test_owned_skill_mcp_projects_existing_resource_and_operations(self):
        paths = self.api["paths"]
        self.assertEqual(list(paths["/oauth/skills"]), ["post"])
        op = paths["/oauth/skills"]["post"]
        self.assertEqual(op["operationId"], "invokeOwnedSkillMCPProtocol")
        self.assertEqual(op["security"], [{"oauthBearer": []}])
        self.assertEqual(op["x-fcis-resource"], "{issuerOrigin}/oauth/skills")
        self.assertEqual(op["x-fcis-required-scope"], "skills.owned.read")
        self.assertIn("WWW-Authenticate", op["responses"]["401"]["headers"])
        for r in op["responses"].values():
            self.assertEqual(r["headers"]["Cache-Control"]["schema"]["const"], "no-store")
        p = op["x-fcis-transport-projection"]
        self.assertEqual(p["instrument"], "fountaincoach.skill-access@0.2.0")
        self.assertEqual(p["securitySchemes"], [{"type": "oauth2", "scopes": ["skills.owned.read"]}])
        self.assertTrue(p["readOnly"])
        self.assertFalse(p["metadataBeforeGrant"])
        self.assertEqual(p["scopeChange"], "none")
        self.assertEqual(p["status"], "specified-only-not-deployed")
        self.assertEqual([(t["name"], t["operation"], t["apiOperation"]) for t in p["tools"]], [
            ("fountain_skills_inventory", "skills.inventory", "listOwnedActiveSkills"),
            ("fountain_skills_read_active", "skills.read-active", "readOwnedActiveSkillRelease"),
        ])
        self.assertEqual(set(p["tools"][0]["inputSchema"]["properties"]), {"limit", "cursor"})
        self.assertEqual(set(p["tools"][1]["inputSchema"]["required"]), {"skillName", "releaseId"})
        for t in p["tools"]:
            self.assertFalse(t["inputSchema"]["additionalProperties"])
        self.assertEqual(paths["/mcp"]["post"]["operationId"], "invokeMCPProtocol")

    def test_connect_is_distinct_from_capability_policy_and_legacy(self):
        paths = self.api["paths"]
        c = paths["/mcp"]["post"]["x-fcis-connect"]
        self.assertEqual(c["externalScope"], "fcis.connect")
        self.assertEqual(c["defaultCapabilities"], [])
        self.assertEqual(c["advertisedResourceScopes"], ["fcis.connect"])
        self.assertEqual(c["authenticationChallengeScope"], "fcis.connect")
        self.assertEqual(c["schemaDiscovery"]["stableDefinitions"], ["fcis.connect"])
        self.assertEqual(c["schemaDiscovery"]["otherDefinitions"], "never externally exposed on /mcp")
        m = c["connectionMessage"]
        self.assertEqual(m["name"], "fcis.connect")
        self.assertFalse(m["directInstrumentCalls"])
        self.assertFalse(m["legacyBearerCalls"])
        self.assertTrue(m["currentPolicyAtDispatchAndEffect"])
        self.assertTrue(m["acknowledgeWithoutEffect"])
        self.assertFalse(m["inputSchema"]["additionalProperties"])
        self.assertTrue(c["schemaDiscovery"]["requiresValidConnection"])
        self.assertFalse(c["schemaDiscovery"]["requiresCapabilityGrant"])
        self.assertFalse(c["schemaDiscovery"]["executionAuthority"])
        self.assertFalse(c["schemaDiscovery"]["privateBindings"])
        self.assertTrue(c["legacyScopeTransition"]["explicitOwnerConsent"])
        self.assertFalse(c["legacyScopeTransition"]["transferCapabilities"])
        self.assertFalse(c["legacyScopeTransition"]["unknownScopeFallback"])
        self.assertEqual(paths[c["resourceMetadataPath"]]["get"]["security"], [])

        self.assertTrue(c["currentPolicyOnEveryCall"])
        self.assertFalse(c["automaticGrant"])
        self.assertFalse(c["genericExecutor"])
        self.assertFalse(c["privateDataWithoutPermission"])
        self.assertNotIn("x-fcis-owner-bridge", paths["/mcp"]["post"])
        op = paths["/oauth/owner/grants"]["post"]
        self.assertEqual(op["operationId"], c["policyOperation"])
        self.assertEqual(op["security"], [{"ownerPasskeySession": []}])
        req = op["requestBody"]["content"]["application/json"]["schema"]
        self.assertFalse(req["additionalProperties"])
        self.assertEqual(req["properties"]["confirm"], {"const": True})
        self.assertIn("expectedPolicyRevision", req["required"])
        legacy = paths["/oauth/skills"]["post"]
        self.assertEqual(legacy["x-fcis-required-scope"], "skills.owned.read")
        system = json.loads((ROOT / "FCIS-SYSTEM.json").read_text())
        self.assertEqual(self.api["x-fcis-skill-distribution"]["clientResource"], system["skillAndScenarioSystem"]["distribution"]["clientResource"])
        self.assertIn("Single owner authorization bridge — fcis.connect", STACK.read_text())

    def test_skill_custody_public_catalogue_and_paid_receipt_shapes(self):
        schemas = self.api["components"]["schemas"]
        m = schemas["SkillPrivateReleaseManifest"]["properties"]
        self.assertEqual(m["schemaVersion"]["const"], 2)
        self.assertEqual(m["visibility"]["enum"], ["private"])
        self.assertEqual(m["pluginID"]["const"], "")
        self.assertEqual(m["pluginVersion"]["const"], "")
        self.assertNotIn("source", schemas["SkillOffer"]["properties"])
        self.assertNotIn("manifest", schemas["SkillOffer"]["properties"])
        self.assertNotIn("signature", schemas["SkillOffer"]["properties"])
        self.assertNotIn("customerTenantId", schemas["SkillOffer"]["properties"])
        self.assertEqual(schemas["SkillPrice"]["properties"]["amountMinor"]["type"], "integer")
        self.assertIn("acceptedTermsSHA256", schemas["SkillAcquisitionRequest"]["required"])
        self.assertIn("confirmedPrice", schemas["SkillAcquisitionRequest"]["required"])
        self.assertIn("receiptId", schemas["SkillAcquisition"]["required"])
        conditional = schemas["SkillEntitlement"]["allOf"][0]
        self.assertEqual(conditional["if"]["properties"]["basis"]["const"], "verified-payment")
        self.assertEqual(conditional["then"]["properties"]["paymentReceiptId"]["type"], "string")
        source = schemas["SkillLicensedSource"]["properties"]
        self.assertIn("sourceSHA256", source)
        self.assertIn("entitlementId", source)
        for forbidden in ("manifest", "signature", "draftId", "customerTenantId"):
            self.assertNotIn(forbidden, source)
        for route in self.api["paths"]:
            self.assertNotIn("/stripe/", route)
            self.assertNotIn("/webhook", route)
        self.assertEqual(self.api["x-fcis-skill-distribution"]["status"], "specified-only-not-deployed")



if __name__ == "__main__":
    unittest.main()
