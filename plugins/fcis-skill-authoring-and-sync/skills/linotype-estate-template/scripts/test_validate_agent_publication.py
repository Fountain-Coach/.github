"""Positive and hostile fixtures for the offline agent-readable publication parity gate."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).with_name("validate_agent_publication.py")
SPEC = importlib.util.spec_from_file_location("press_agent_validation", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
sys.dont_write_bytecode = True  # Preserve canonical packaged Skill tree during CI tests.
SPEC.loader.exec_module(VALIDATOR)


def fixtures():
    root = {
        "publicationId": "governance",
        "editionId": "governance-2026",
        "sourceOwner": "Fountain-Coach/governance.fountain.coach",
        "sourceRevision": "a" * 40,
        "publicationState": "staged",
        "canonicalURL": "https://governance.fountain.coach/",
        "entries": [
            {"id": "chapter-07", "canonicalURL": "https://governance.fountain.coach/chapters/07/",
             "sourceSHA256": "1" * 64, "status": "current"},
            {"id": "chapter-08", "canonicalURL": "https://governance.fountain.coach/chapters/08/",
             "sourceSHA256": "2" * 64, "status": "reference"},
        ]
    }
    source = {"schema": VALIDATOR.SOURCE_SCHEMA, **root}
    guide = {
        "schema": VALIDATOR.GUIDE_SCHEMA,
        "publicationId": root["publicationId"],
        "editionId": root["editionId"],
        "sourceOwner": root["sourceOwner"],
        "sourceRevision": root["sourceRevision"],
        "audience": "external-agents",
        "executionAuthority": "none",
        "retrievalPolicy": "public",
        "actionPolicy": "no-agent-actions",
        "interpretationRules": [
            {"id": "current", "description": "Current is binding only within its owning edition."},
            {"id": "reference", "description": "Reference is historical, not a current rule."},
        ],
    }
    guide_bytes = (json.dumps(guide, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode()
    agent = {"schema": VALIDATOR.AGENT_SCHEMA, **copy.deepcopy(root), "guide": {
        "path": "agent-public-guidance.json",
        "sha256": hashlib.sha256(guide_bytes).hexdigest()
    }}
    return source, agent, guide, guide_bytes


class AgentPublicationTests(unittest.TestCase):
    def setUp(self):
        self.source, self.agent, self.guide, self.guide_bytes = fixtures()
        self.guide_path = pathlib.Path("agent-public-guidance.json")

    def check(self):
        return VALIDATOR.verify(self.source, self.agent, self.guide,
                                self.guide_bytes, self.guide_path)

    def test_complete_edition_current_reference_parity(self):
        receipt = self.check()
        self.assertEqual(receipt["entriesCompared"], 2)
        self.assertEqual((receipt["current"], receipt["reference"]), (1, 1))
        self.assertIs(receipt["runtimeAndPublicationAuthorityVerified"], False)

    def test_missing_chapter_rejected(self):
        self.agent["entries"].pop()
        with self.assertRaisesRegex(VALIDATOR.InvalidPublication, "entries"):
            self.check()

    def test_false_historical_status_rejected(self):
        self.agent["entries"][0]["status"] = "reference"
        with self.assertRaisesRegex(VALIDATOR.InvalidPublication, "entries"):
            self.check()

    def test_chapter_order_matters(self):
        self.agent["entries"].reverse()
        with self.assertRaisesRegex(VALIDATOR.InvalidPublication, "entries"):
            self.check()

    def test_stale_revision_rejected(self):
        self.agent["sourceRevision"] = "b" * 40
        with self.assertRaisesRegex(VALIDATOR.InvalidPublication, "sourceRevision"):
            self.check()

    def test_guide_digest_must_match_exact_bytes(self):
        self.guide_bytes += b" "
        with self.assertRaisesRegex(VALIDATOR.InvalidPublication, "bytes drifted"):
            self.check()

    def test_guide_source_revision_must_match(self):
        self.guide["sourceRevision"] = "b" * 40
        with self.assertRaisesRegex(VALIDATOR.InvalidPublication, "sourceRevision"):
            self.check()

    def test_guide_cannot_claim_execution_authority(self):
        self.guide["executionAuthority"] = "allowed"
        with self.assertRaisesRegex(VALIDATOR.InvalidPublication, "executable"):
            self.check()

    def test_guide_cannot_claim_tool_permissions(self):
        self.guide["actionPolicy"] = "execute-tools"
        with self.assertRaisesRegex(VALIDATOR.InvalidPublication, "executable"):
            self.check()

    def test_draft_chapter_not_published(self):
        self.source["publicationState"] = "published"
        self.agent["publicationState"] = "published"
        self.source["entries"][0]["status"] = "draft"
        self.agent["entries"][0]["status"] = "draft"
        with self.assertRaisesRegex(VALIDATOR.InvalidPublication, "draft falsely"):
            self.check()

    def test_noncanonical_host_rejected(self):
        self.agent["entries"][0]["canonicalURL"] = "http://localhost/private"
        with self.assertRaisesRegex(VALIDATOR.InvalidPublication, "canonical"):
            self.check()

    def test_duplicate_source_ids_rejected(self):
        self.agent["entries"][1]["id"] = self.agent["entries"][0]["id"]
        with self.assertRaisesRegex(VALIDATOR.InvalidPublication, "repeated"):
            self.check()

    def test_guide_path_traversal_rejected(self):
        self.agent["guide"]["path"] = "../agent-public-guidance.json"
        with self.assertRaisesRegex(VALIDATOR.InvalidPublication, "relative"):
            self.check()

    def test_unexpected_fields_cannot_grant_capability(self):
        self.agent["capabilities"] = [{"execute": "shell"}]
        with self.assertRaisesRegex(VALIDATOR.InvalidPublication, "expected fields"):
            self.check()

    def test_cli_accepts_declared_fixtures_only(self):
        with tempfile.TemporaryDirectory() as folder:
            files = {}
            for name, value in (("source.json", self.source), ("agent.json", self.agent)):
                target = pathlib.Path(folder) / name
                target.write_text(json.dumps(value))
                files[name] = target
            g = pathlib.Path(folder) / self.guide_path
            g.write_bytes(self.guide_bytes)
            command = [sys.executable, str(SCRIPT), "--source", str(files["source.json"]),
                       "--agent", str(files["agent.json"]), "--guide", str(g)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "static-parity-pass")
            self.agent["sourceRevision"] = "b" * 40
            files["agent.json"].write_text(json.dumps(self.agent))
            broken = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(broken.returncode, 0)
            self.assertIn("sourceRevision", broken.stderr)


if __name__ == "__main__":
    unittest.main()
