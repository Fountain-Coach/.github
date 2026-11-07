"""FCIS PR and Git-native release policy regression checks."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class GitReleasePolicyTests(unittest.TestCase):
    def test_main_ruleset_requires_pr_ci_and_no_bypass(self):
        rule = json.loads((ROOT / "docs/FCIS-Main-Branch-Ruleset.json").read_text())
        self.assertEqual(rule["enforcement"], "active")
        self.assertEqual(rule["conditions"]["ref_name"]["include"], ["refs/heads/main"])
        self.assertEqual(rule["bypass_actors"], [])
        by_type = {item["type"]: item for item in rule["rules"]}
        self.assertIn("deletion", by_type)
        self.assertIn("non_fast_forward", by_type)
        self.assertIn("pull_request", by_type)
        checks = by_type["required_status_checks"]["parameters"]["required_status_checks"]
        self.assertEqual(checks, [{"context": "build", "integration_id": 15368}])

    def test_ci_requires_actual_five_skill_package_parity(self):
        test = (ROOT / ".github/workflows/test.yml").read_text()
        self.assertIn("python3 skills/skillctl.py check", test)
        self.assertIn("python3 skills/plugin_projection.py check", test)
        self.assertIn("python3 -m unittest discover -s skills/tests -v", test)
        self.assertIn("contents: read", test)

    def test_main_release_workflow_is_read_only(self):
        workflow = (ROOT / ".github/workflows/fcis-marketplace-sync.yml").read_text()
        self.assertIn("contents: read", workflow)
        self.assertIn("python3 skills/plugin_projection.py check", workflow)
        self.assertNotIn("python3 skills/plugin_projection.py sync", workflow)
        self.assertNotIn("python3 skills/marketplace_publish.py", workflow)
        self.assertNotIn("contents: write", workflow)

    def test_hook_preserves_two_separate_commits(self):
        hook = (ROOT / ".githooks/post-commit").read_text()
        self.assertIn("FCIS_SKIP_DERIVED", hook)
        self.assertIn('python3 "$repo/skills/plugin_projection.py" sync', hook)
        self.assertIn('python3 "$repo/skills/marketplace_publish.py"', hook)
        self.assertIn("git-disaster-recovery.sh", hook)
        publisher = (ROOT / "skills/marketplace_publish.py").read_text()
        self.assertIn('if perform_push:', publisher)
        self.assertIn('raise PublicationError("Direct push', publisher)


if __name__ == "__main__":
    unittest.main()
