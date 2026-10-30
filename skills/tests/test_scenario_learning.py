"""Scenario evidence is an input to skill proposals, never self-approval."""
from pathlib import Path
import copy
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scenario_learning as learning


class ScenarioLearningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((Path(__file__).resolve().parents[1] / "proposals" / "commands-discover-alias-boundary.json").read_text())

    def candidate(self):
        return copy.deepcopy(self.source)

    def test_real_pinned_scenario_proposes_revision_with_evidence_limit(self):
        result = learning.assess(self.candidate())
        self.assertEqual(result["scenario"], "commands-discover")
        self.assertEqual(result["targetSkill"], "fcis-skill-authoring-and-sync")
        self.assertEqual(result["classification"], "PROPOSED_EVIDENCE_LIMITED")
        self.assertCountEqual(result["missingRawEvidence"], ["storeReceipt", "axTranscript", "windowCapture"])
        self.assertEqual(len(result["sourceReferences"]), 3)

    def test_cannot_claim_admission(self):
        c = self.candidate()
        c["authority"]["admitted"] = True
        with self.assertRaises(learning.ProposalError):
            learning.assess(c)

    def test_cannot_claim_canonical_source_write_or_distribution(self):
        for key in ("canonicalChanged", "distributed"):
            c = self.candidate()
            c["authority"][key] = True
            with self.assertRaises(learning.ProposalError):
                learning.assess(c)

    def test_alias_is_not_new_skill(self):
        for name in ("commands", "help"):
            c = self.candidate()
            c["candidate"]["mode"] = "new"
            c["candidate"]["targetSkill"] = name
            with self.assertRaises(learning.ProposalError):
                learning.assess(c)

    def test_unmatched_existing_revision_target_refused(self):
        c = self.candidate()
        c["candidate"]["targetSkill"] = "unregistered-procedure"
        with self.assertRaises(learning.ProposalError):
            learning.assess(c)

    def test_reused_execution_receipt_refused(self):
        c = self.candidate()
        c["independentProof"]["executionIDs"] = ["execution-one", "execution-one"]
        with self.assertRaises(learning.ProposalError):
            learning.assess(c)

    def test_status_drift_must_not_count_as_current_acceptance(self):
        c = self.candidate()
        c["scenario"]["contractStatus"] = "executable"
        result = learning.assess(c)
        self.assertEqual(result["classification"], "PROPOSED_STATUS_DRIFT")

    def test_scenario_not_accepted_is_not_a_success(self):
        c = self.candidate()
        c["scenario"]["contractStatus"] = "draft"
        c["scenario"]["coverageStatus"] = "draft"
        result = learning.assess(c)
        self.assertEqual(result["classification"], "PROPOSED_SCENARIO_NOT_ACCEPTED")

    def test_declared_receipts_still_do_not_admit_skill(self):
        c = self.candidate()
        c["independentProof"] = {
            "executionIDs": ["run-one"],
            "storeReceipt": "store:document-id",
            "axTranscript": "ax:evidence-path",
            "windowCapture": "window:evidence-path",
        }
        result = learning.assess(c)
        self.assertEqual(result["classification"], "PROPOSED_REVIEW_REQUIRED")
        self.assertIn("no live scenario", result["claimBoundary"])

    def test_missing_witness_refused(self):
        c = self.candidate()
        del c["evidence"]["witness"]
        with self.assertRaises(learning.ProposalError):
            learning.assess(c)

    def test_bad_source_path_refused(self):
        c = self.candidate()
        c["scenario"]["contract"]["path"] = "../unrelated-secret"
        with self.assertRaises(learning.ProposalError):
            learning.assess(c)

    def test_real_readings_status_drift_is_not_accepted(self):
        source = Path(__file__).resolve().parents[1] / "proposals" / "readings-fresh-execution.json"
        c = json.loads(source.read_text())
        self.assertEqual(c["scenario"]["contractStatus"], "executable")
        self.assertEqual(c["scenario"]["coverageStatus"], "live-accepted")
        result = learning.assess(c)
        self.assertEqual(result["classification"], "PROPOSED_STATUS_DRIFT")
        self.assertEqual(result["targetSkill"], "fcis-skill-authoring-and-sync")
        self.assertEqual(result["missingRawEvidence"], ["storeReceipt", "axTranscript", "windowCapture"])

    def test_source_metadata_cannot_be_empty(self):
        c = self.candidate()
        c["candidate"]["transferTests"] = []
        with self.assertRaises(learning.ProposalError):
            learning.assess(c)


if __name__ == "__main__":
    unittest.main()
