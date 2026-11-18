"""FCIS H3 immutable Git ingress and signed owner promotion.

These tests use local disposable repositories and ephemeral signing keys. A green
GitHub job never establishes a deployed owner Git server or real owner identity.
"""
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]
RECEIVE = ROOT / ".githooks" / "pre-receive"
PROMOTE = ROOT / "scripts" / "fcis-git-promote.sh"
RUNNER = ROOT / "scripts" / "fcis-ci.sh"
REQUIRED = (
    "scripts/fcis-ci.sh",
    "skills/skillctl.py",
    "skills/plugin_projection.py",
    "skills/tests/test_fcis_posix_ci.py",
)


def run(*args, cwd=None, env=None):
    return subprocess.run(tuple(map(str, args)), cwd=cwd, env=env, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          check=False, timeout=80)


def require_ok(*args, cwd=None):
    result = run(*args, cwd=cwd)
    if result.returncode:
        raise AssertionError(f"Failed {args}: {result.stdout}")
    return result.stdout.strip()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class H3GitAcceptanceTests(unittest.TestCase):
    def setUp(self):
        context = tempfile.TemporaryDirectory(prefix="fcis-h3-offline-")
        self.addCleanup(context.cleanup)
        root = Path(context.name)
        self.bare = root / "origin.git"
        self.work = root / "work"
        self.policy = root / "policy"
        self.policy.mkdir()
        (self.policy / "receipts").mkdir()
        require_ok("git", "init", "--quiet", "--bare", "--initial-branch=main", self.bare)
        require_ok("git", "init", "--quiet", "--initial-branch=main", self.work)
        require_ok("git", "config", "user.name", "H3 Offline Test", cwd=self.work)
        require_ok("git", "config", "user.email", "h3@invalid.example", cwd=self.work)
        require_ok("git", "--git-dir", self.bare, "config", "fcis.repositoryID", "Fountain-Coach/.github")
        (self.policy / "repository-id").write_text("Fountain-Coach/.github\n")
        for name in REQUIRED:
            dest = self.work / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            if name == "scripts/fcis-ci.sh":
                shutil.copyfile(RUNNER, dest)
            elif name == "skills/skillctl.py":
                dest.write_text("print('fixture digest check')\n")
            elif name == "skills/plugin_projection.py":
                dest.write_text("print('fixture mirror check')\n")
            else:
                dest.write_text(
                    "import unittest\nclass TestFixture(unittest.TestCase):\n"
                    "    def test_pass(self): self.assertTrue(True)\n"
                )
        (self.work / "FCIS-OPENAPI.json").write_text("{}\n")
        (self.work / "AGENTS.md").write_text("Offline fixture: no secrets\n")
        require_ok("git", "add", ".", cwd=self.work)
        require_ok("git", "commit", "--quiet", "-m", "approved seed", cwd=self.work)
        require_ok("git", "push", "--quiet", self.bare, "HEAD:refs/heads/main", cwd=self.work)
        self.seed = self.ref("refs/heads/main")
        (self.bare / "hooks" / "pre-receive").write_bytes(RECEIVE.read_bytes())
        (self.bare / "hooks" / "pre-receive").chmod(0o700)
        (self.policy / "trusted-files.sha256").write_text(
            "".join(f"{sha(self.work / rel)}  {rel}\n" for rel in REQUIRED)
        )
        self.key = root / "test-owner-ed25519"
        if shutil.which("ssh-keygen"):
            require_ok("ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", self.key)
            (self.policy / "authorized_signers").write_text(
                "owner " + (root / "test-owner-ed25519.pub").read_text()
            )
        else:
            (self.policy / "authorized_signers").write_text("owner unavailable\n")
        self.n = 0

    def ref(self, ref):
        return require_ok("git", "--git-dir", self.bare, "rev-parse", ref)

    def candidate(self, *, problem=None):
        self.n += 1
        name = f"c{self.n:03d}"
        (self.work / f"candidate-{name}.txt").write_text("candidate\n")
        if problem == "test":
            p = self.work / "skills/tests/test_bad.py"
            p.write_text(
                "import unittest\nclass Fails(unittest.TestCase):\n"
                "    def test_error(self): self.fail('expected failure')\n"
            )
        if problem == "validator":
            (self.work / "skills/skillctl.py").write_text("raise SystemExit(22)\n")
        require_ok("git", "add", ".", cwd=self.work)
        require_ok("git", "commit", "--quiet", "-m", name, cwd=self.work)
        commit = require_ok("git", "rev-parse", "HEAD", cwd=self.work)
        ref = "refs/heads/candidates/" + name
        require_ok("git", "push", "--quiet", self.bare, f"HEAD:{ref}", cwd=self.work)
        return ref, commit

    def approve(self, ref, commit, *, old=None, expires=None):
        old = old or self.seed
        expires = expires or int(time.time()) + 600
        payload = self.policy.parent / f"approval-{self.n}.txt"
        policy_sha = sha(self.policy / "trusted-files.sha256")
        payload.write_text(
            f"FCIS-OWNER-PROMOTION-v1\n"
            f"repository=Fountain-Coach/.github\n"
            f"candidate_ref={ref}\n"
            f"candidate_sha={commit}\n"
            f"expected_main={old}\n"
            f"policy_sha256={policy_sha}\n"
            f"expires={expires}\n"
        )
        require_ok("ssh-keygen", "-Y", "sign", "-f", self.key, "-n",
                   "fcis-git-promotion", payload)
        return payload

    def promote(self, ref, commit, approval, *, old=None):
        return run("sh", PROMOTE, self.bare, self.policy, ref, commit,
                   old or self.seed, approval)

    def test_shell_parses_and_main_direct_push_denied(self):
        for path in (RECEIVE, PROMOTE, RUNNER):
            self.assertEqual(run("sh", "-n", path).returncode, 0)
        ref, commit = self.candidate()
        result = run("git", "push", self.bare, f"{commit}:refs/heads/main",
                     cwd=self.work)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("direct main push forbidden", result.stdout)
        self.assertEqual(self.ref("refs/heads/main"), self.seed)

    def test_immutable_candidate_ref_rejects_update_and_deletion(self):
        ref, _ = self.candidate()
        (self.work / "updated.txt").write_text("later\n")
        require_ok("git", "add", ".", cwd=self.work)
        require_ok("git", "commit", "--quiet", "-m", "later", cwd=self.work)
        attempted = run("git", "push", self.bare, f"HEAD:{ref}", cwd=self.work)
        self.assertNotEqual(attempted.returncode, 0)
        self.assertIn("immutable", attempted.stdout)
        deletion = run("git", "push", self.bare, f":{ref}", cwd=self.work)
        self.assertNotEqual(deletion.returncode, 0)

    def test_unapproved_ref_denied(self):
        self.candidate()
        bad = run("git", "push", self.bare, "HEAD:refs/tags/release",
                  cwd=self.work)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn("unapproved ref namespace", bad.stdout)

    @unittest.skipUnless(shutil.which("ssh-keygen"), "OpenSSH is unavailable")
    def test_unsigned_or_tampered_owner_approval_denied(self):
        ref, commit = self.candidate()
        approval = self.approve(ref, commit)
        approval.write_text(approval.read_text().replace(
            "repository=Fountain-Coach/.github",
            "repository=Other-Organization/.github"
        ))
        result = self.promote(ref, commit, approval)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.ref("refs/heads/main"), self.seed)

    @unittest.skipUnless(shutil.which("ssh-keygen"), "OpenSSH is unavailable")
    def test_expired_owner_approval_denied(self):
        ref, commit = self.candidate()
        approval = self.approve(ref, commit, expires=int(time.time()) - 10)
        result = self.promote(ref, commit, approval)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expired", result.stdout)
        self.assertEqual(self.ref("refs/heads/main"), self.seed)

    @unittest.skipUnless(shutil.which("ssh-keygen"), "OpenSSH is unavailable")
    def test_stale_expected_main_denied(self):
        ref, commit = self.candidate()
        approval = self.approve(ref, commit)
        result = self.promote(ref, commit, approval, old="f" * 40)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.ref("refs/heads/main"), self.seed)

    @unittest.skipUnless(shutil.which("ssh-keygen") and shutil.which("bwrap") and shutil.which("timeout"),
                         "Real Bubblewrap/OpenSSH sandbox unavailable")
    def test_valid_owner_approval_promotes_exact_revision_with_receipt(self):
        ref, commit = self.candidate()
        approval = self.approve(ref, commit)
        result = self.promote(ref, commit, approval)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.ref("refs/heads/main"), commit)
        receipt = self.policy / "receipts" / f"{commit}.{self.seed}.promoted"
        self.assertTrue(receipt.is_file())
        self.assertIn("state=promoted", receipt.read_text())
        self.assertIn("ci_log_sha256=", receipt.read_text())

    @unittest.skipUnless(shutil.which("ssh-keygen") and shutil.which("bwrap") and shutil.which("timeout"),
                         "Real Bubblewrap/OpenSSH sandbox unavailable")
    def test_failing_source_check_prevents_main_promotion(self):
        ref, commit = self.candidate(problem="test")
        approval = self.approve(ref, commit)
        result = self.promote(ref, commit, approval)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.ref("refs/heads/main"), self.seed)
        self.assertNotIn("ACCEPTED candidate=", result.stdout)

    @unittest.skipUnless(shutil.which("ssh-keygen") and shutil.which("bwrap") and shutil.which("timeout"),
                         "Real Bubblewrap/OpenSSH sandbox unavailable")
    def test_pinned_ci_validator_drift_refused(self):
        ref, commit = self.candidate(problem="validator")
        approval = self.approve(ref, commit)
        result = self.promote(ref, commit, approval)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("pinned CI authority", result.stdout)
        self.assertEqual(self.ref("refs/heads/main"), self.seed)


if __name__ == "__main__":
    unittest.main()
