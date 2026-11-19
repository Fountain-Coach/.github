"""Prerequisite-free FCIS composition source gate (no runtime or Go execution)."""
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
        self.assertGreaterEqual(len(doc["generation"]["requirementCatalog"]), 90)
        self.assertIn("FCIS-SYSTEM.json", (ROOT / "FCIS-STACK.md").read_text(encoding="utf-8"))

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
