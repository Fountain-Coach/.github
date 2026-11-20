"""Fail-closed source tests for the bounded live H3 HEAD.lock ACL correction.

Never execute --apply, install OS packages, or change running origin.
"""
from pathlib import Path
import os
import stat
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/fcis-h3-head-lock-acl-repair.sh"
if not SCRIPT.exists():
    SCRIPT = Path(__file__).with_name("fcis-h3-head-lock-acl-repair.sh")

class H3HeadLockACLTests(unittest.TestCase):
    def test_bash_syntax(self):
        subprocess.run(["bash", "-n", str(SCRIPT)], check=True)

    def test_explicit_owner_apply_required(self):
        p = subprocess.run(["bash", str(SCRIPT)], text=True,
                           capture_output=True, timeout=5)
        self.assertEqual(p.returncode, 2)
        self.assertIn("explicit --apply required", p.stderr)

    def test_live_mutation_is_precisely_scoped(self):
        s = SCRIPT.read_text()
        for phrase in (
            "[[ $(hostname) == ubuntu-2gb-hel1-1 ]]",
            "OLD=be5a12b295d8ff7cfd40fd1c3e756698580bd2e9",
            "STALE=390a21532930c4876a527d6d64252d26d4f199a1",
            "PROMOTER_BLOB=ffce53bb2577724a3d48f596376b8269c396090f",
            '[[ ! -e $BARE/HEAD.lock && ! -L $BARE/HEAD.lock ]]',
            '[[ -f $RECEIPT.prepared && -f $RECEIPT.ci.log && ! -e $RECEIPT.promoted ]]',
            'H3_PREVIOUS_PREPARED_RECEIPT_PRESERVED',
            'flock -n 8',
            'getfacl -p "$BARE"',
            'setfacl --restore="$TMP/preimage.acl"',
            'chown root:root "$BARE/HEAD"',
            'chmod +t "$BARE"',
            "setfacl -m 'u:fcis-operator:rwx,g::r-x,o::---' \"$BARE\"",
            'runuser -u fcis-operator -- test -w "$BARE"',
            'runuser -u fcis-git -- test ! -w "$BARE"',
            'runuser -u fcis-operator -- test ! -w "$BARE/config"',
            'runuser -u fcis-operator -- test ! -w "$BARE/HEAD"',
            'runuser -u fcis-operator -- test ! -w "$BARE/hooks"',
        ):
            self.assertIn(phrase, s)
        self.assertNotIn("chmod 777", s)
        self.assertNotIn('setfacl -m "u:fcis-git:rwx', s)
        self.assertNotIn("safe.directory=*", s)
        self.assertNotIn("systemctl", s)
        self.assertNotIn("/etc/caddy", s)

    def test_atomic_update_only_in_disposable_fixture(self):
        s = SCRIPT.read_text()
        self.assertIn('git clone --quiet --bare --no-hardlinks "$BARE" "$TMP/fixture.git"', s)
        self.assertIn('git --git-dir="$FIXTURE" update-ref refs/heads/main "$STALE" "$OLD"', s)
        self.assertLess(s.index('chown -R fcis-git:fcis-git "$FIXTURE"'), s.index('chmod -R g+rX "$FIXTURE"'))
        self.assertLess(s.index('chmod -R g+rX "$FIXTURE"'), s.index('chown root:fcis-git "$FIXTURE"'))
        self.assertNotIn('git --git-dir="$BARE" update-ref', s)
        self.assertIn("H3_DISPOSABLE_ATOMIC_CAS_VERIFIED", s)
        self.assertIn('actual Git main changed by fixture test', s)

    def test_umask_077_bare_clone_packed_refs_exposes_original_bug(self):
        """Real Git fixture: a bare clone can contain group-unreadable packed refs."""
        with tempfile.TemporaryDirectory(prefix="fcis-h3-packed-refs-") as root:
            base = Path(root)
            work, origin, fixture = (base / k for k in ("work", "origin.git", "fixture.git"))
            for argv in (
                ("git", "init", "-q", "-b", "main", str(work)),
                ("git", "-C", str(work), "-c", "user.name=H3 Test",
                 "-c", "user.email=h3@example.invalid", "commit", "-qm", "base", "--allow-empty"),
                ("git", "init", "--bare", "-q", str(origin)),
                ("git", "-C", str(work), "push", "-q", str(origin), "HEAD:refs/heads/main"),
            ):
                subprocess.run(argv, check=True, capture_output=True, timeout=10)
            old_mask = os.umask(0o077)
            try:
                subprocess.run(("git", "clone", "--quiet", "--bare", "--no-hardlinks",
                                str(origin), str(fixture)),
                               check=True, capture_output=True, timeout=10)
            finally:
                os.umask(old_mask)
            packed = fixture / "packed-refs"
            self.assertTrue(packed.is_file(), "Git clone must exercise packed-refs")
            before = stat.S_IMODE(packed.stat().st_mode)
            self.assertEqual(before & stat.S_IRGRP, 0,
                             "must reproduce restrictive clone file permissions")
            subprocess.run(("chmod", "-R", "g+rX", str(fixture)),
                           check=True, capture_output=True, timeout=10)
            after = stat.S_IMODE(packed.stat().st_mode)
            self.assertNotEqual(after & stat.S_IRGRP, 0)
            self.assertEqual(after & stat.S_IWGRP, 0,
                             "packed-refs must become group-readable, not writable")

if __name__ == "__main__":
    unittest.main(verbosity=2)
