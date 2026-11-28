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
