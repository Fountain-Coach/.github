"""H2 portable POSIX Git-hook CI acceptance in isolated, network-free Git fixtures.

This tests source-level refusal and does not exercise a production owner Git server.
"""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts" / "fcis-ci.sh"
HOOK_COMMIT = ROOT / ".githooks" / "pre-commit"
HOOK_PUSH = ROOT / ".githooks" / "pre-push"


def execute(*args, cwd=None, env=None):
    environment = os.environ.copy()
    for key in ("FCIS_CI_BASE", "FCIS_CI_HEAD", "FCIS_CI_GO_MODULE",
                "FCIS_CI_GO_SHA", "FCIS_CI_GO_CACHE_ROOT"):
        environment.pop(key, None)
    if env:
        environment.update(env)
    return subprocess.run([str(a) for a in args], cwd=cwd, env=environment,
                          encoding="utf-8", stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False)


class FCISPortableCITests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="fcis-posix-h2-")
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name) / "source"
        (self.repo / "scripts").mkdir(parents=True)
        (self.repo / "skills/tests").mkdir(parents=True)
        shutil.copy2(RUNNER, self.repo / "scripts/fcis-ci.sh")
        (self.repo / "FCIS-STACK.md").write_text("test stack\n", encoding="utf-8")
        (self.repo / "FCIS-OPENAPI.json").write_text("{}\n", encoding="utf-8")
        (self.repo / "skills/skillctl.py").write_text("print('skill digest PASS')\n", encoding="utf-8")
        (self.repo / "skills/plugin_projection.py").write_text("print('plugin mirror PASS')\n", encoding="utf-8")
        (self.repo / "skills/tests/test_basic.py").write_text(
            "import unittest\nclass BasicTest(unittest.TestCase):\n"
            "    def test_works(self): self.assertTrue(True)\n", encoding="utf-8"
        )
        self.git("init", "-q")
        self.git("config", "user.name", "FCIS CI Test")
        self.git("config", "user.email", "ci@example.invalid")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "fixture seed")
        self.seed = self.rev()

    def git(self, *args):
        result = execute("git", *args, cwd=self.repo)
        self.assertEqual(result.returncode, 0, result.stdout)
        return result.stdout

    def rev(self):
        return self.git("rev-parse", "HEAD").strip()

    def commit(self, filename, data):
        (self.repo / filename).write_text(data, encoding="utf-8")
        self.git("add", filename)
        self.git("commit", "-q", "-m", filename)
        return self.rev()

    def check(self, *args, env=None):
        return execute("sh", self.repo / "scripts/fcis-ci.sh", *args,
                       cwd=self.repo, env=env)

    def test_posix_shell_parses_runner_and_both_client_hooks(self):
        for path in (RUNNER, HOOK_COMMIT, HOOK_PUSH):
            result = execute("sh", "-n", path)
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_source_gate_passes_offline_and_uses_committed_range(self):
        latest = self.commit("good.txt", "accepted\n")
        result = self.check("source", self.seed, latest)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("SOURCE PASS", result.stdout)
        self.assertIn("Formatting changed committed bytes:", result.stdout)

    def test_invalid_openapi_json_fails(self):
        (self.repo / "FCIS-OPENAPI.json").write_text("{ invalid json", encoding="utf-8")
        result = self.check("source")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("SOURCE PASS", result.stdout)

    def test_plugin_projection_failure_fails(self):
        (self.repo / "skills/plugin_projection.py").write_text("raise SystemExit(3)\n")
        result = self.check("source")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("SOURCE PASS", result.stdout)

    def test_source_unit_test_failure_fails(self):
        (self.repo / "skills/tests/test_basic.py").write_text(
            "import unittest\nclass BasicTest(unittest.TestCase):\n"
            "    def test_fails(self): self.fail('fixture failure')\n")
        result = self.check("source")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("SOURCE PASS", result.stdout)

    def test_committed_whitespace_error_in_full_range_fails(self):
        latest = self.commit("bad.txt", "bad trailing whitespace   \n")
        result = self.check("source", self.seed, latest)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("whitespace", result.stdout.lower())
        self.assertNotIn("SOURCE PASS", result.stdout)

    def test_fast_staged_gate_detects_whitespace(self):
        (self.repo / "staged.txt").write_text("bad staged    \n")
        self.git("add", "staged.txt")
        result = self.check("staged")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("Staged source contains whitespace errors", result.stdout)

    def test_hook_push_checks_all_new_branch_commits_from_main(self):
        self.git("branch", "-M", "main")
        self.git("checkout", "-q", "-b", "feature")
        self.commit("first.txt", "bad trailing whitespace  \n")
        self.commit("last.txt", "clean final commit\n")
        hook_input = "refs/heads/feature " + self.rev() + (
            " refs/heads/feature 0000000000000000000000000000000000000000\n"
        )
        result = subprocess.run(
            ["sh", str(HOOK_PUSH)], cwd=self.repo,
            input=hook_input, encoding="utf-8",
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            env={k: v for k, v in os.environ.items() if not k.startswith("FCIS_CI_")},
            check=False
        )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("whitespace", result.stdout.lower())

    def test_incomplete_github_diff_pair_refused(self):
        result = self.check("source", env={"FCIS_CI_BASE": self.seed})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FCIS_CI_HEAD is missing", result.stdout)

    def test_go_gate_requires_explicit_owned_module(self):
        result = self.check("go")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("GO PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
