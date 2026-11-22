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
        self.assertEqual(len(doc["generation"]["requirementCatalog"]), 293)
        self.assertEqual(verifier.check_atomic_coverage(doc, base), 293)
        self.assertEqual(doc["generation"]["requirementGate"]["generatorReceipt"]["initialStatus"], "INCOMPLETE")
        self.assertEqual(doc["status"], "NORMATIVE_SPECIFICATION_CANDIDATE__NOT_GENERATED")

    def test_instrument_observability_has_separate_evidence_and_safe_transport(self):
        _, doc, _ = self._atomic_fixture()
        obs = doc["capabilitySystem"]["instrumentObservability"]
        self.assertTrue(obs["storeEvidence"]["commitBeforeVerifiedClaim"])
        self.assertTrue(obs["delivery"]["degradeNeverAuthorizes"])
        self.assertIn("not-established", obs["lifecycle"]["evidenceClasses"])
        self.assertIn("store-committed", obs["lifecycle"]["evidenceClasses"])
        self.assertIn("sessionCookie", obs["privacy"]["forbiddenFields"])
        self.assertIn("signingPrivateKey", obs["privacy"]["forbiddenFields"])
        self.assertIn("buildSHA256", obs["identity"]["declaredFields"])
        self.assertIn("reasonCode", obs["lifecycle"]["requiredEventFields"])
        self.assertIn("Standalone Go first-owner flow works with no external MIDI2 device, remote peer or Swift runtime",
                      obs["acceptance"]["scenarios"])

    def test_identity_field_removed_must_fail_generated_coverage(self):
        verifier, doc, base = self._atomic_fixture()
        doc["capabilitySystem"]["instrumentObservability"]["identity"]["declaredFields"].remove("buildSHA256")
        with self.assertRaisesRegex(ValueError, "coverage catalog mismatch"):
            verifier.check_atomic_coverage(doc, base)

    def test_authentication_lifecycle_stage_removed_must_fail_coverage(self):
        verifier, doc, base = self._atomic_fixture()
        doc["capabilitySystem"]["instrumentObservability"]["lifecycle"]["phases"].remove("refused")
        with self.assertRaisesRegex(ValueError, "coverage catalog mismatch"):
            verifier.check_atomic_coverage(doc, base)

    def test_secret_redaction_requirement_removed_must_fail_coverage(self):
        verifier, doc, base = self._atomic_fixture()
        doc["capabilitySystem"]["instrumentObservability"]["privacy"]["forbiddenFields"].remove("sessionCookie")
        with self.assertRaisesRegex(ValueError, "coverage catalog mismatch"):
            verifier.check_atomic_coverage(doc, base)

    def test_observability_scenario_removed_must_fail_coverage(self):
        verifier, doc, base = self._atomic_fixture()
        doc["capabilitySystem"]["instrumentObservability"]["acceptance"]["scenarios"].pop()
        with self.assertRaisesRegex(ValueError, "coverage catalog mismatch"):
            verifier.check_atomic_coverage(doc, base)

    def test_observability_cannot_authorize_from_transport(self):
        verifier, doc, _ = self._atomic_fixture()
        schema = json.loads((ROOT / "FCIS-SYSTEM.schema.json").read_text(encoding="utf-8"))
        doc["capabilitySystem"]["instrumentObservability"]["delivery"]["degradeNeverAuthorizes"] = False
        with self.assertRaisesRegex(ValueError, "expected fixed value True"):
            verifier.schema_validate(doc, schema, schema)

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
