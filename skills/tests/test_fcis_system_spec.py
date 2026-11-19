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
        self.assertEqual(len(doc["generation"]["requirementCatalog"]), 222)
        self.assertEqual(verifier.check_atomic_coverage(doc, base), 222)
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
