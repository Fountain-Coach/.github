"""FCIS dated contract criticism and owner-owned POSIX Git hook maintenance.

Source-only: these checks never assert that an owner Git origin or Go service was deployed.
"""
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills"))

from skillctl import entries, digest  # noqa: E402


class FCISMaintenancePlanTests(unittest.TestCase):
    def test_canonical_linkage_and_finite_cutover(self):
        stack = (ROOT / "FCIS-STACK.md").read_text(encoding="utf-8")
        critique = (ROOT / "docs/FCIS-Spec-OpenAPI-Critique-2026-11-18.md").read_text(encoding="utf-8")
        plan = (ROOT / "docs/FCIS-Maintenance-Hook-CI-Plan.md").read_text(encoding="utf-8")
        for filename in ("FCIS-Spec-OpenAPI-Critique-2026-11-18.md",
                         "FCIS-Maintenance-Hook-CI-Plan.md"):
            self.assertIn(filename, stack)
        self.assertIn("FCIS-OPENAPI.json", critique)
        self.assertIn("FCIS-OPENAPI.json", plan)
        self.assertIn("## 7. Production deployment and finite DoD", stack)
        for finding in range(1, 17):
            self.assertIn(f"C{finding:02d} |", critique)
        for slice_number in range(1, 7):
            self.assertIn(f"H{slice_number}:", plan)
        self.assertIn("pre-receive", plan)
        self.assertIn("pre-push", plan)
        self.assertIn("NOT_INSTALLED", plan)
        self.assertIn("source-only", critique.lower())

    def test_three_skills_source_integrity_and_existing_plugin_parity(self):
        catalog = json.loads((ROOT / "skills/openai-distribution.json").read_text(encoding="utf-8"))
        self.assertEqual(len(catalog["skills"]), 9)
        records = {row["name"]: row for row in catalog["skills"]}
        for name in ("fcis-owner-access", "fcis-go-runtime-migration",
                     "fcis-skill-authoring-and-sync"):
            canonical = entries(ROOT / ".codex" / "skills" / name)
            mirrored = entries(ROOT / "plugins" / "fcis-skill-authoring-and-sync" / "skills" / name)
            self.assertEqual(canonical, mirrored)
            self.assertEqual(digest(canonical), records[name]["contentSHA256"])
            intro = canonical["SKILL.md"].decode("utf-8")
            self.assertIn("FCIS-Maintenance-Hook-CI-Plan.md", intro)
            self.assertIn("FCIS-Spec-OpenAPI-Critique-2026-11-18.md", intro)
        version = json.loads((ROOT / "plugins/fcis-skill-authoring-and-sync/plugin.json")
                             .read_text(encoding="utf-8"))["version"]
        self.assertEqual(len(version.split(".")), 3)
        self.assertTrue(all(part.isdigit() for part in version.split(".")))

    def test_existing_hooks_remain_honest_until_owned_server_installed(self):
        hooks = ROOT / ".githooks"
        pre_push = (hooks / "pre-push").read_text(encoding="utf-8")
        post_commit = (hooks / "post-commit").read_text(encoding="utf-8")
        self.assertIn("skillctl.py", pre_push)
        self.assertIn("git-disaster-recovery.sh", pre_push)
        self.assertIn("plugin_projection.py", post_commit)
        self.assertIn("marketplace_publish.py", post_commit)
        self.assertIn("FCIS_SKIP_DERIVED", post_commit)
        plan = (ROOT / "docs/FCIS-Maintenance-Hook-CI-Plan.md").read_text(encoding="utf-8")
        self.assertIn("bypassable", plan.lower())
        self.assertIn("GitHub", plan)


if __name__ == "__main__":
    unittest.main()
