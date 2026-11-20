"""Reproduce Git dubious-ownership refusal inside sanitized H3 source clone.

No SSH credentials, privileged host changes or live Git origin are used.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

PROMOTER = Path(__file__).resolve().parents[2] / "scripts" / "fcis-git-promote.sh"


def git(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], text=True, capture_output=True,
                          env=env, timeout=12)


class IsolatedCloneSafeDirectoryTests(unittest.TestCase):
    def test_promoter_has_exact_temporary_trust_no_wildcard(self):
        source = PROMOTER.read_text()
        self.assertIn('GIT_CONFIG_GLOBAL="$tmp/clone-safe.gitconfig"', source)
        self.assertIn("printf '[safe]\\n\\tdirectory = %s\\n' \"$bare\"", source)
        self.assertIn("chmod 0600 \"$tmp/clone-safe.gitconfig\"", source)
        self.assertIn("case \"$bare\" in *[!a-zA-Z0-9_./-]*)", source)
        self.assertIn('GIT_CONFIG_GLOBAL=/dev/null \\\n    git -C "$tmp/source"', source)
        self.assertNotIn("safe.directory=*", source)
        self.assertNotIn("git config --global --add safe.directory", source)

    def test_actual_local_git_clone_only_trusts_exact_origin(self):
        with tempfile.TemporaryDirectory(prefix="fcis-h3-git-safe-") as folder:
            root = Path(folder)
            source = root / "source"
            source.mkdir()
            self.assertEqual(git("init", "-q", str(source)).returncode, 0)
            created = git("-C", str(source), "-c", "user.name=H3 Fixture",
                          "-c", "user.email=fixture@example.test", "commit", "-qm",
                          "seed", "--allow-empty")
            self.assertEqual(created.returncode, 0, created.stderr)
            bare = root / "origin.git"
            sibling = root / "unapproved.git"
            for dest in (bare, sibling):
                r = git("clone", "--quiet", "--bare", str(source), str(dest))
                self.assertEqual(r.returncode, 0, r.stderr)
            isolated = root / "isolated"
            isolated.mkdir()
            trusted_config = isolated / "clone-safe.gitconfig"
            trusted_config.write_text("[safe]\n\tdirectory = " + str(bare) + "\n")
            trusted_config.chmod(0o600)
            clean = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                     "HOME": str(isolated), "GIT_CONFIG_NOSYSTEM": "1",
                     "GIT_TEST_ASSUME_DIFFERENT_OWNER": "1"}
            denied = git("-c", "core.hooksPath=/dev/null", "-c", "protocol.file.allow=always",
                         "clone", "--quiet", "--no-hardlinks", "--no-checkout",
                         str(bare), str(isolated / "denied"),
                         env={**clean, "GIT_CONFIG_GLOBAL": "/dev/null"})
            self.assertNotEqual(denied.returncode, 0,
                                "test fixture must reproduce the observed Git ownership refusal")
            self.assertIn("dubious ownership", denied.stderr)
            allowed = git("-c", "core.hooksPath=/dev/null", "-c", "protocol.file.allow=always",
                          "clone", "--quiet", "--no-hardlinks", "--no-checkout",
                          str(bare), str(isolated / "allowed"),
                          env={**clean, "GIT_CONFIG_GLOBAL": str(trusted_config)})
            self.assertEqual(allowed.returncode, 0, allowed.stderr)
            unapproved = git("-c", "core.hooksPath=/dev/null", "-c", "protocol.file.allow=always",
                             "clone", "--quiet", "--no-hardlinks", "--no-checkout",
                             str(sibling), str(isolated / "unapproved"),
                             env={**clean, "GIT_CONFIG_GLOBAL": str(trusted_config)})
            self.assertNotEqual(unapproved.returncode, 0)
            self.assertIn("dubious ownership", unapproved.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
