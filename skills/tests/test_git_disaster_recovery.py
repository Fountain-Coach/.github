import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[2]
SCRIPT = SOURCE / "scripts" / "git-disaster-recovery.sh"
HOOKS = SOURCE / ".githooks"


def run(*args, cwd=None, env=None):
    return subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True,
                          check=True)


class PureGitDisasterRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "source"
        self.repo.mkdir()
        run("git", "init", "-q", "-b", "main", str(self.repo))
        run("git", "config", "user.email", "test@example.invalid", cwd=self.repo)
        run("git", "config", "user.name", "Recovery Test", cwd=self.repo)
        (self.repo / "scripts").mkdir()
        (self.repo / ".githooks").mkdir()
        shutil.copy2(SCRIPT, self.repo / "scripts" / SCRIPT.name)
        for name in ("post-commit", "post-merge", "post-rewrite", "pre-push"):
            shutil.copy2(HOOKS / name, self.repo / ".githooks" / name)
        path = self.repo / "example.txt"
        path.write_text("first revision\n")
        run("git", "add", ".", cwd=self.repo)
        run("git", "-c", "core.hooksPath=/dev/null", "commit", "-qm", "Initial source", cwd=self.repo)
        self.bare = self.base / "recovery.git"
        self.bundles = self.base / "bundles"
        self.script = str(self.repo / "scripts" / SCRIPT.name)
        self.env = dict(os.environ, GIT_SSH_COMMAND="false")

    def setup_recovery(self):
        run(self.script, "setup", str(self.bare), str(self.bundles),
            cwd=self.repo, env=self.env)

    def test_bundle_and_bare_clone_without_github(self):
        self.setup_recovery()
        run(self.script, "verify", cwd=self.repo, env=self.env)
        latest = (self.bundles / "LATEST").read_text().strip()
        bundle = self.bundles / latest
        self.assertTrue(bundle.is_file())
        self.assertTrue(Path(str(bundle) + ".sha256").is_file())
        run("git", "clone", "-q", "-b", "main", str(bundle), str(self.base / "from-bundle"), env=self.env)
        run("git", "clone", "-q", str(self.bare), str(self.base / "from-mirror"), env=self.env)
        self.assertEqual((self.base / "from-bundle" / "example.txt").read_text(), "first revision\n")
        self.assertEqual((self.base / "from-mirror" / "example.txt").read_text(), "first revision\n")

    def test_hook_updates_both_copies_and_unmounted_drive_does_not_block_commit(self):
        self.setup_recovery()
        original_bundle = (self.bundles / "LATEST").read_text()
        (self.repo / "example.txt").write_text("second revision\n")
        run("git", "add", "example.txt", cwd=self.repo)
        run("git", "commit", "-qm", "Second revision", cwd=self.repo, env=self.env)
        second_bundle = (self.bundles / "LATEST").read_text()
        self.assertNotEqual(original_bundle, second_bundle)
        run(self.script, "verify", cwd=self.repo, env=self.env)
        run("git", "config", "--local", "fcis.recoveryMount", "/not-an-existing-mount",
            cwd=self.repo)
        (self.repo / "example.txt").write_text("third revision\n")
        run("git", "add", "example.txt", cwd=self.repo)
        run("git", "commit", "-qm", "Third revision", cwd=self.repo, env=self.env)
        self.assertEqual((self.bundles / "LATEST").read_text(), second_bundle)
        local_sha = run("git", "rev-parse", "HEAD", cwd=self.repo).stdout.strip()
        mirror_sha = run("git", "--git-dir", str(self.bare), "rev-parse",
                         "refs/heads/main").stdout.strip()
        self.assertEqual(local_sha, mirror_sha)

    def test_shallow_checkout_cannot_claim_disaster_recovery(self):
        (self.repo / "example.txt").write_text("second revision\n")
        run("git", "add", "example.txt", cwd=self.repo)
        run("git", "commit", "-qm", "Second revision", cwd=self.repo)
        shallow = self.base / "shallow"
        run("git", "clone", "-q", "--depth", "1", "file://" + str(self.repo),
            str(shallow), env=self.env)
        self.assertEqual(run("git", "rev-parse", "--is-shallow-repository",
                             cwd=shallow).stdout.strip(), "true")
        result = subprocess.run(
            [str(shallow / "scripts" / SCRIPT.name), "setup",
             str(self.base / "shallow-bare.git"), str(self.base / "shallow-bundles")],
            cwd=shallow, env=self.env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("shallow", result.stderr.lower())
        self.assertFalse((self.base / "shallow-bundles").exists())

    def test_corrupted_bundle_fails_verification(self):
        self.setup_recovery()
        latest = (self.bundles / "LATEST").read_text().strip()
        with (self.bundles / latest).open("ab") as out:
            out.write(b"tamper")
        result = subprocess.run([self.script, "verify"], cwd=self.repo, env=self.env,
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("checksum mismatch", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
