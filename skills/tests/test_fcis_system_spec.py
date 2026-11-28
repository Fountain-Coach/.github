"""Prerequisite-free FCIS composition source gate (no runtime or Go execution)."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = [
    ROOT / "FCIS-SYSTEM.json",
    ROOT / "FCIS-SYSTEM.schema.json",
    ROOT / "scripts/verify_fcis_system_spec.py",
]


class FCISWholeSystemContractTests(unittest.TestCase):
    def test_root_cannot_remove_entire_spec_gate(self):
        for path in REQUIRED:
            self.assertTrue(path.is_file(), f"required canonical source missing: {path}")
        source_ci = (ROOT / "scripts/fcis-ci.sh").read_text(encoding="utf-8")
        self.assertIn("verify_fcis_system_spec.py", source_ci)
        self.assertIn("Missing whole-system FCIS composition", source_ci)

    def test_prerequisite_free_source_contract(self):
        doc = json.loads((ROOT / "FCIS-SYSTEM.json").read_text(encoding="utf-8"))
        self.assertEqual(doc["designPrinciple"]["name"], "Voraussetzungslos")
        self.assertEqual(doc["designPrinciple"]["defaultProfile"], "fresh-install")
        self.assertEqual(doc["initialization"]["externalDependenciesForFirstStart"], [])
        self.assertEqual(doc["initialization"]["initialState"]["phase"], "UNCLAIMED")
        self.assertFalse(doc["migration"]["requiredForFreshInstall"])
        self.assertEqual(doc["knownSpecificationLimitations"], [])
        self.assertGreaterEqual(len(doc["generation"]["requirementCatalog"]), 222)
        self.assertIn("FCIS-SYSTEM.json", (ROOT / "FCIS-STACK.md").read_text(encoding="utf-8"))


    @staticmethod
    def _atomic_fixture():
        sys.path.insert(0, str(ROOT / "scripts"))
        import verify_fcis_system_spec as verifier
        doc = json.loads((ROOT / "FCIS-SYSTEM.json").read_text(encoding="utf-8"))
        base = {row["id"] for row in doc["generation"]["requirementCatalog"]
                if "proofClass" not in row}
        return verifier, doc, base

    def test_exact_atomic_coverage_is_derived_from_source(self):
        verifier, doc, base = self._atomic_fixture()
        count = len(doc["generation"]["requirementCatalog"])
        self.assertGreater(count, 222)
        self.assertEqual(verifier.check_atomic_coverage(doc, base), count)
        self.assertEqual(count, doc["coverageBaseline"]["atomicRequirementCount"])
        self.assertIn("skill-distribution", doc["coverageBaseline"]["atomicRequirementGroups"])
        self.assertEqual(doc["generation"]["requirementGate"]["generatorReceipt"]["initialStatus"], "INCOMPLETE")

    def test_missing_atomic_requirement_fails_closed(self):
        verifier, doc, base = self._atomic_fixture()
        doc["generation"]["requirementCatalog"].pop()
        with self.assertRaisesRegex(ValueError, "coverage catalog mismatch"):
            verifier.check_atomic_coverage(doc, base)

    def test_wrong_atomic_source_pointer_fails_closed(self):
        verifier, doc, base = self._atomic_fixture()
        row = next(r for r in doc["generation"]["requirementCatalog"]
                   if r["id"].startswith("HOST-RECEIPT-"))
        row["sourcePointer"] = "/generation/requiredArtifacts/0"
        with self.assertRaisesRegex(ValueError, "sourcePointer drift"):
            verifier.check_atomic_coverage(doc, base)

    def test_modified_state_machine_fails_atomic_coverage(self):
        verifier, doc, base = self._atomic_fixture()
        doc["initialization"]["stateMachine"].pop()
        with self.assertRaisesRegex(ValueError, "coverage catalog mismatch"):
            verifier.check_atomic_coverage(doc, base)

    def test_reduced_denominator_and_false_completion_refused(self):
        verifier, doc, base = self._atomic_fixture()
        copy_a = copy.deepcopy(doc)
        copy_a["generation"]["requirementGate"]["expectedRequirementCount"] -= 1
        with self.assertRaisesRegex(ValueError, "derived atomic total"):
            verifier.check_atomic_coverage(copy_a, base)
        copy_b = copy.deepcopy(doc)
        copy_b["generation"]["requirementGate"]["generatorReceipt"]["initialStatus"] = "COMPLETE"
        with self.assertRaisesRegex(ValueError, "may not start COMPLETE"):
            verifier.check_atomic_coverage(copy_b, base)

    def test_authzen_authority_and_wire_refusals(self):
        verifier, doc, _ = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text(encoding="utf-8"))
        verifier.check_authzen(doc, api)
        for key, value in (("defaultCapabilities", ["host.describe"]), ("denyStatus", 403),
                           ("status", "deployed"), ("unknownFields", "reject")):
            candidate = copy.deepcopy(api)
            candidate["x-fcis-authzen"][key] = value
            bad_doc = copy.deepcopy(doc)
            bad_doc["authorityAndIdentity"]["authorizationDecision"] = candidate["x-fcis-authzen"]
            with self.assertRaisesRegex(ValueError, "AuthZEN authority"):
                verifier.check_authzen(bad_doc, candidate)
        candidate = copy.deepcopy(api)
        candidate["paths"]["/access/v1/evaluation"]["post"]["security"] = []
        with self.assertRaisesRegex(ValueError, "protected evaluation"):
            verifier.check_authzen(doc, candidate)
        candidate = copy.deepcopy(api)
        candidate["components"]["schemas"]["AuthZENSubject"]["additionalProperties"] = False
        with self.assertRaisesRegex(ValueError, "wire drift"):
            verifier.check_authzen(doc, candidate)

    def test_runtime_deployment_fail_closed(self):
        verifier, doc, _ = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text(encoding="utf-8"))
        verifier.check_runtime_deployment(doc, api)
        for key, value in (
            ("status", "deployed"),
            ("authority", "bearer approval"),
            ("rollback", "restore old Store"),
            ("executor", "public generic shell"),
        ):
            candidate = copy.deepcopy(api)
            candidate["x-fcis-runtime-deployment"][key] = value
            bad = copy.deepcopy(doc)
            bad["authorityAndIdentity"]["runtimeDeployment"] = candidate["x-fcis-runtime-deployment"]
            with self.assertRaisesRegex(ValueError, "runtime deployment"):
                verifier.check_runtime_deployment(bad, candidate)
        for path, method in (
            ("/oauth/owner/deployments", "post"),
            ("/oauth/owner/deployments/{deploymentId}/decision", "post"),
            ("/oauth/owner/deployments/{deploymentId}/activate", "post"),
        ):
            candidate = copy.deepcopy(api)
            candidate["paths"][path][method]["security"] = []
            with self.assertRaisesRegex(ValueError, "owner route"):
                verifier.check_runtime_deployment(doc, candidate)
        candidate = copy.deepcopy(api)
        candidate["components"]["schemas"]["RuntimeDeploymentManifest"]["additionalProperties"] = True
        with self.assertRaisesRegex(ValueError, "closed schema"):
            verifier.check_runtime_deployment(doc, candidate)

    def test_deployment_handoff_is_closed_own_connection_and_owner_decision(self):
        verifier, doc, _ = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text())
        verifier.check_runtime_deployment(doc, api)
        for mutate in (
            lambda p, m, a: p["messageKinds"].update({"deployment.activate": p["messageKinds"]["deployment.prepare"]}),
            lambda p, m, a: p["messageKinds"]["deployment.inspect"]["inputSchema"]["required"].append("ownerId"),
            lambda p, m, a: m["inputSchema"]["properties"]["mode"].update(const="rollback"),
            lambda p, m, a: p.update(binding="caller-selected deployment"),
            lambda p, m, a: a["components"]["schemas"]["RuntimeDeploymentReview"].update(additionalProperties=True),
        ):
            bad = copy.deepcopy(api)
            d = copy.deepcopy(doc)
            p = bad["x-fcis-runtime-deployment"]["projection"]
            m = bad["paths"]["/mcp"]["post"]["x-fcis-connect"]["connectionMessage"]
            mutate(p, m, bad)
            m["deploymentHandoff"] = copy.deepcopy(p)
            d["authorityAndIdentity"]["runtimeDeployment"] = copy.deepcopy(bad["x-fcis-runtime-deployment"])
            with self.assertRaisesRegex(ValueError, "deployment (projection|handoff)"):
                verifier.check_runtime_deployment(d, bad)

    def test_machine_renewal_owner_ceiling_signed_receipt_and_refusals(self):
        verifier, doc, _ = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text(encoding="utf-8"))
        verifier.check_machine_renewal(doc, api)
        path = "/oauth/host/grants/renew"
        for key, value in (
            ("maximumLeaseMilliseconds", 86400001),
            ("proofFreshnessMilliseconds", 0),
            ("ownerCeiling", "automatic unlimited owner authority"),
            ("authority", "renew expired grants"),
            ("atomicity", "write each grant separately"),
            ("replay", "renew again on any nonce"),
            ("supervision", "use old expiry"),
        ):
            candidate = copy.deepcopy(api)
            bad_doc = copy.deepcopy(doc)
            profile = candidate["paths"][path]["post"]["x-fcis-machine-renewal"]
            profile[key] = value
            bad_doc["authorityAndIdentity"]["hosts"]["machineGrantRenewal"] = profile
            with self.assertRaisesRegex(ValueError, "machine renewal"):
                verifier.check_machine_renewal(bad_doc, candidate)
        candidate = copy.deepcopy(api)
        candidate["components"]["schemas"]["MachineGrantRenewalRequest"]["properties"]["scope"] = {"type": "string"}
        with self.assertRaisesRegex(ValueError, "closed wire schema"):
            verifier.check_machine_renewal(doc, candidate)
        candidate = copy.deepcopy(api)
        candidate["components"]["schemas"]["MachineGrantRenewalReceipt"]["properties"]["evidence"]["properties"].pop("issuerSignature")
        with self.assertRaisesRegex(ValueError, "closed wire schema"):
            verifier.check_machine_renewal(doc, candidate)
        candidate = copy.deepcopy(api)
        candidate["paths"][path]["post"]["security"] = [{"oauthBearer": []}]
        with self.assertRaisesRegex(ValueError, "authority or route"):
            verifier.check_machine_renewal(doc, candidate)


    def test_connection_domain_refusal_preserves_protocol_boundary(self):
        verifier, doc, _ = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text())
        verifier.check_connection_discovery(doc, api)
        for mutate in (
            lambda p, a: p["refusalResult"]["codes"].pop("skill_revision_conflict"),
            lambda p, a: p["refusalResult"].update(protocolBoundary="always HTTP 200"),
            lambda p, a: a["components"]["schemas"]["FCISConnectionRefusal"].update(additionalProperties=True),
            lambda p, a: p["refusalResult"].update(authority="no authorization needed"),
        ):
            bad = copy.deepcopy(api)
            sysdoc = copy.deepcopy(doc)
            message = bad["paths"]["/mcp"]["post"]["x-fcis-connect"]["connectionMessage"]
            mutate(message, bad)
            sysdoc["capabilitySystem"]["mcp"]["connectionDiscovery"]["connectionMessage"] = copy.deepcopy(message)
            with self.assertRaisesRegex(ValueError, "connection refusal contract drift"):
                verifier.check_connection_discovery(sysdoc, bad)

    def test_owner_admin_requires_explicit_golden_key_decision(self):
        verifier, doc, _ = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text(encoding="utf-8"))
        verifier.check_owner_admin(doc, api)
        base = "/oauth/owner/admin/requests/{requestId}/decision"
        bad = copy.deepcopy(api)
        bad["paths"][base]["post"]["security"] = [{"oauthBearer": []}]
        with self.assertRaisesRegex(ValueError, "Golden Key"):
            verifier.check_owner_admin(doc, bad)
        bad = copy.deepcopy(api)
        bad["components"]["schemas"]["OwnerAdminDecisionInput"]["properties"]["confirm"] = {"type": "boolean"}
        with self.assertRaisesRegex(ValueError, "approve/decline"):
            verifier.check_owner_admin(doc, bad)
        bad = copy.deepcopy(api)
        m = bad["paths"]["/mcp"]["post"]["x-fcis-connect"]["connectionMessage"]
        m["inputSchema"]["properties"]["ownerSession"] = {"type": "string"}
        with self.assertRaisesRegex(ValueError, "caller authority"):
            verifier.check_owner_admin(doc, bad)
        bad = copy.deepcopy(api)
        bad["paths"][base]["post"]["responses"]["200"]["headers"] = {}
        with self.assertRaisesRegex(ValueError, "caching"):
            verifier.check_owner_admin(doc, bad)

    def test_owner_admin_proposal_custody_cannot_be_removed(self):
        verifier, doc, base = self._atomic_fixture()
        doc["persistence"]["logicalCollections"].remove("fcis.owner-admin-requests")
        with self.assertRaisesRegex(ValueError, "coverage catalog mismatch"):
            verifier.check_atomic_coverage(doc, base)

    def test_learning_acceptance_contract(self):
        verifier, doc, base = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text(encoding="utf-8"))
        verifier.check_learning_acceptance(doc, api)
        self.assertEqual(verifier.check_atomic_coverage(doc, base),
                         len(doc["generation"]["requirementCatalog"]))

    def test_learning_missing_stage_refusal_and_premature_acceptance(self):
        verifier, doc, _ = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text(encoding="utf-8"))
        for field in ("stages", "evidence", "refusals", "continuousBehavior"):
            candidate = copy.deepcopy(doc)
            candidate["skillAndScenarioSystem"]["learningAcceptance"][field].pop()
            with self.assertRaisesRegex(ValueError, "learning .* coverage/order drift"):
                verifier.check_learning_acceptance(candidate, api)
        candidate = copy.deepcopy(doc)
        candidate["skillAndScenarioSystem"]["learningAcceptance"]["status"] = "LIVE-ACCEPTED"
        with self.assertRaisesRegex(ValueError, "premature acceptance"):
            verifier.check_learning_acceptance(candidate, api)

    def test_continuous_learning_cannot_be_reduced_to_one_example(self):
        verifier, doc, base = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text(encoding="utf-8"))
        candidate = copy.deepcopy(doc)
        rows = candidate["skillAndScenarioSystem"]["learningAcceptance"]["continuousBehavior"]
        rows[-1]["id"] = "single-manual-example"
        with self.assertRaisesRegex(ValueError, "learning continuousBehavior coverage/order drift"):
            verifier.check_learning_acceptance(candidate, api)
        candidate = copy.deepcopy(doc)
        candidate["generation"]["requirementCatalog"] = [
            row for row in candidate["generation"]["requirementCatalog"]
            if row["id"] != "LEARN-CYCLE-DEFAULT-ASSESSMENT"]
        with self.assertRaisesRegex(ValueError, "coverage catalog mismatch"):
            verifier.check_atomic_coverage(candidate, base)
        verifier.check_learning_acceptance(doc, api)

    def test_learning_cannot_substitute_source_review_or_drop_authority(self):
        verifier, doc, _ = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text(encoding="utf-8"))
        candidate = copy.deepcopy(api)
        candidate["x-fcis-learning-acceptance"]["reviewEvidenceKind"] = "source-review"
        with self.assertRaisesRegex(ValueError, "learning OpenAPI binding"):
            verifier.check_learning_acceptance(doc, candidate)
        candidate = copy.deepcopy(api)
        candidate["paths"]["/oauth/owner/skills/{skillName}/drafts/{draftId}/review"]["post"]["security"] = []
        with self.assertRaisesRegex(ValueError, "learning operation authorization"):
            verifier.check_learning_acceptance(doc, candidate)

    def test_learning_removal_fails_atomic_coverage(self):
        verifier, doc, base = self._atomic_fixture()
        doc["generation"]["requirementCatalog"] = [
            row for row in doc["generation"]["requirementCatalog"]
            if row["id"] != "LEARN-STAGE-FRESH-CONSUMPTION"]
        with self.assertRaisesRegex(ValueError, "coverage catalog mismatch"):
            verifier.check_atomic_coverage(doc, base)

    def test_owner_chat_contract_and_atomic_coverage(self):
        verifier, doc, base = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text(encoding="utf-8"))
        verifier.check_owner_chat(doc, api)
        self.assertEqual(verifier.check_atomic_coverage(doc, base),
                         len(doc["generation"]["requirementCatalog"]))

    def test_owner_chat_refuses_paid_or_unverified_reasoning(self):
        verifier, doc, _ = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text(encoding="utf-8"))
        for field, value in (("additionalInferenceChargeCeilingMinor", 1),
                             ("noPaidFallback", False), ("workspaceCreditsAllowed", True),
                             ("automaticRechargeAllowed", True), ("ownerBillingMutationAllowed", True),
                             ("unknownEntitlement", "dispatch")):
            candidate = copy.deepcopy(doc)
            candidate["reasoningAndConversationSystem"]["policy"][field] = value
            with self.assertRaisesRegex(ValueError, "subscription-only reasoning policy drift"):
                verifier.check_owner_chat(candidate, api)
        for field in ("subscriptionOnly", "additionalInferenceChargeCeilingMinor", "disclosureConsent"):
            candidate = copy.deepcopy(api)
            candidate["components"]["schemas"]["OwnerReasoningTurnCreate"]["required"].remove(field)
            with self.assertRaisesRegex(ValueError, "owner chat send boundary drift"):
                verifier.check_owner_chat(doc, candidate)

    def test_owner_chat_refuses_missing_history_and_authorization(self):
        verifier, doc, _ = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text(encoding="utf-8"))
        candidate = copy.deepcopy(doc)
        candidate["persistence"]["logicalCollections"].remove("fcis.messages")
        with self.assertRaisesRegex(ValueError, "owner conversation custody drift"):
            verifier.check_owner_chat(candidate, api)
        candidate = copy.deepcopy(api)
        candidate["paths"]["/oauth/owner/conversations"]["get"]["security"] = []
        with self.assertRaisesRegex(ValueError, "owner chat operation authorization drift"):
            verifier.check_owner_chat(doc, candidate)
        candidate = copy.deepcopy(doc)
        candidate["reasoningAndConversationSystem"]["status"] = "LIVE-ACCEPTED"
        with self.assertRaisesRegex(ValueError, "owner chat premature acceptance"):
            verifier.check_owner_chat(candidate, api)

    def test_situated_reference_contract_is_optional_and_bound(self):
        verifier, doc, base = self._atomic_fixture()
        api = json.loads((ROOT / "FCIS-OPENAPI.json").read_text(encoding="utf-8"))
        verifier.check_situated_context(doc, api)
        for edit, error in (
            (lambda a: a["components"]["schemas"]["OwnerReasoningTurnCreate"]["required"].append("situatedContext"), "must be optional"),
            (lambda a: a["components"]["schemas"]["OwnerSituatedContext"]["required"].remove("expectedContextSHA256"), "exact source and consent"),
            (lambda a: a["components"]["schemas"]["OwnerSituatedContext"]["properties"]["situation"]["properties"]["wiringState"]["enum"].remove("unwired"), "empty and unwired"),
            (lambda a: a["components"]["schemas"]["OwnerReasoningTurn"]["properties"].update(situatedContext={}), "must not persist"),
            (lambda a: a["components"]["schemas"]["OwnerConversationError"]["properties"]["error"]["enum"].remove("context_conflict"), "refusal coverage"),
            (lambda a: a["x-fcis-owner-chat"]["situatedReasoning"]["newOperations"].append("invented"), "scope or acceptance"),
        ):
            candidate = copy.deepcopy(api)
            edit(candidate)
            with self.assertRaisesRegex(ValueError, error):
                verifier.check_situated_context(doc, candidate)
        candidate = copy.deepcopy(doc)
        candidate["generation"]["requirementCatalog"] = [x for x in candidate["generation"]["requirementCatalog"] if x["id"] != "CHAT-REQ-DOMAIN-CONTEXT-BINDING"]
        with self.assertRaisesRegex(ValueError, "coverage catalog mismatch"):
            verifier.check_atomic_coverage(candidate, base)

    def test_exact_spec_and_http_contract_consistency(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts/verify_fcis_system_spec.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("SOURCE PASS", completed.stdout)
        self.assertIn("SOURCE ONLY", completed.stdout)


if __name__ == "__main__":
    unittest.main()
