"""FCIS H3 immutable Git ingress and signed owner promotion.

These tests use local disposable repositories and ephemeral signing keys. A green
GitHub job never establishes a deployed owner Git server or real owner identity.
"""
from pathlib import Path
import hashlib
import os
import shutil
import socket
import subprocess
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]
RECEIVE = ROOT / ".githooks" / "pre-receive"
PROMOTE = ROOT / "scripts" / "fcis-git-promote.sh"
APPROVE = ROOT / "scripts" / "fcis-git-approve.sh"
RUNNER = ROOT / "scripts" / "fcis-ci.sh"
REQUIRED = (
    "scripts/fcis-ci.sh",
    "skills/skillctl.py",
    "skills/plugin_projection.py",
    "skills/tests/test_fcis_posix_ci.py",
)

# H3 tests intentionally exercise a *second* Bubblewrap sandbox. Ubuntu 24.04
# bwrap-userns-restrict prevents nested user namespaces after the first outer
# sandbox has been established. Do not weaken the host AppArmor profile, permit
# network access, or report nested integration tests as passed. Only skip those
# two tests when this source process is positively inside the exact already
# networkless, read-only, synthetic-UID H3 outer CI configuration.
_OUTER_PASSWD = "fcis-ci:x:65534:65534:FCIS isolated CI:/tmp:/bin/sh\n"
_OUTER_H3_SKIP_REASON = (
    "nested userns intentionally denied by Ubuntu AppArmor inside positively "
    "verified outer H3 CI; run real positive H3 sandbox tests on unprivileged host"
)


def _qualifies_outer_h3_ci(facts):
    return (
        facts["root"] == "/source"
        and facts["uid"] == 65534
        and facts["home"] == "/tmp"
        and facts["passwd"] == _OUTER_PASSWD
        and "unpriv_bwrap" in facts["apparmor"]
        and "(enforce)" in facts["apparmor"]
        and facts["interfaces"] == ("lo",)
        and facts["source_writable"] is False
        and facts["operator_policy_visible"] is False
    )


def _in_verified_outer_h3_ci():
    try:
        facts = {
            "root": str(ROOT),
            "uid": os.geteuid(),
            "home": os.environ.get("HOME"),
            "passwd": Path("/etc/passwd").read_text(),
            "apparmor": Path("/proc/self/attr/current").read_text().strip(),
            "interfaces": tuple(sorted(name for _, name in socket.if_nameindex())),
            "source_writable": os.access("/source", os.W_OK),
            "operator_policy_visible": Path("/var/lib/fcis-owner-git-policy").exists(),
        }
        return _qualifies_outer_h3_ci(facts)
    except (OSError, ValueError):
        return False


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
        if problem == "isolation":
            p = self.work / "skills/tests/test_isolation.py"
            p.write_text(
                "import os, unittest, socket, shutil, pwd\n"
                "class SandboxTest(unittest.TestCase):\n"
                "    def test_private_operator_policy_is_invisible(self):\n"
                f"        self.assertFalse(os.path.exists({str(self.policy)!r}))\n"
                "    def test_no_external_network_interface(self):\n"
                "        self.assertEqual([name for _,name in socket.if_nameindex() if name != 'lo'], [])\n"
                "    def test_posix_tools_and_synthetic_identity(self):\n"
                "        self.assertTrue(shutil.which('awk'))\n"
                "        self.assertEqual(pwd.getpwuid(os.getuid()).pw_name, 'fcis-ci')\n"
            )
        require_ok("git", "add", ".", cwd=self.work)
        require_ok("git", "commit", "--quiet", "-m", name, cwd=self.work)
        commit = require_ok("git", "rev-parse", "HEAD", cwd=self.work)
        ref = "refs/heads/candidates/" + name
        require_ok("git", "push", "--quiet", self.bare, f"HEAD:{ref}", cwd=self.work)
        return ref, commit

    def approve(self, ref, commit, *, old=None, expires=None):
        old = old or self.seed
        payload = self.policy.parent / f"approval-{self.n}.txt"
        policy_sha = sha(self.policy / "trusted-files.sha256")
        if expires is None:
            # Test the same reviewed POSIX owner approval helper as production operators.
            require_ok("sh", APPROVE, self.key, "Fountain-Coach/.github",
                       ref, commit, old, policy_sha, payload)
        else:
            # An intentionally expired signed fixture is outside the helper's permitted operation.
            payload.write_text(
                f"FCIS-OWNER-PROMOTION-v1\nrepository=Fountain-Coach/.github\n"
                f"candidate_ref={ref}\ncandidate_sha={commit}\n"
                f"expected_main={old}\npolicy_sha256={policy_sha}\n"
                f"expires={expires}\n"
            )
            require_ok("ssh-keygen", "-Y", "sign", "-f", self.key, "-n",
                       "fcis-git-promotion", payload)
        return payload

    def promote(self, ref, commit, approval, *, old=None):
        return run("sh", PROMOTE, self.bare, self.policy, ref, commit,
                   old or self.seed, approval)

    def test_nested_ci_detection_requires_every_outer_security_boundary(self):
        expected = {
            "root": "/source",
            "uid": 65534,
            "home": "/tmp",
            "passwd": _OUTER_PASSWD,
            "apparmor": "bwrap//&unpriv_bwrap (enforce)",
            "interfaces": ("lo",),
            "source_writable": False,
            "operator_policy_visible": False,
        }
        self.assertTrue(_qualifies_outer_h3_ci(expected))
        refusals = {
            "root": "/tmp",
            "uid": 1000,
            "home": "/home/owner",
            "passwd": "owner:x:1000:1000:owner:/home/owner:/bin/sh\n",
            "apparmor": "unconfined",
            "interfaces": ("lo", "eth0"),
            "source_writable": True,
            "operator_policy_visible": True,
        }
        for key, forged in refusals.items():
            with self.subTest(boundary=key):
                facts = dict(expected)
                facts[key] = forged
                self.assertFalse(_qualifies_outer_h3_ci(facts))
        # The inner nested tests are never replaced by fabricated passing
        # receipts. Outside exact outer confinement they still run normally.
        self.assertIn("run real positive H3", _OUTER_H3_SKIP_REASON)

    def test_shell_parses_and_main_direct_push_denied(self):
        for path in (RECEIVE, PROMOTE, APPROVE, RUNNER):
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

    @unittest.skipIf(_in_verified_outer_h3_ci(), _OUTER_H3_SKIP_REASON)
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

    @unittest.skipIf(_in_verified_outer_h3_ci(), _OUTER_H3_SKIP_REASON)
    @unittest.skipUnless(shutil.which("ssh-keygen") and shutil.which("bwrap") and shutil.which("timeout"),
                         "Real Bubblewrap/OpenSSH sandbox unavailable")
    def test_sandbox_hides_operator_files_and_nonloopback_interfaces(self):
        ref, commit = self.candidate(problem="isolation")
        approval = self.approve(ref, commit)
        result = self.promote(ref, commit, approval)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.ref("refs/heads/main"), commit)

    @unittest.skipUnless(shutil.which("ssh-keygen"), "OpenSSH is unavailable")
    def test_changed_trusted_policy_after_signing_refused(self):
        ref, commit = self.candidate()
        approval = self.approve(ref, commit)
        with (self.policy / "trusted-files.sha256").open("a") as out:
            out.write("invalid-policy-update\n")
        result = self.promote(ref, commit, approval)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.ref("refs/heads/main"), self.seed)

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
