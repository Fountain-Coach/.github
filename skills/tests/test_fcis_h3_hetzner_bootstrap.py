"""Host-free refusal tests for the bounded owner-Git H3 installer.

All SSH test keys are ephemeral, created inside a disposable local directory.
Never run the apply path, and never make root/systemd/Caddy changes.
"""
import os
from pathlib import Path
import base64
import shutil
import struct
import subprocess
import tempfile
import unittest

BOOTSTRAP = Path(__file__).resolve().parents[2] / "scripts" / "fcis-h3-hetzner-bootstrap.sh"
if not BOOTSTRAP.is_file():
    BOOTSTRAP = Path(__file__).with_name("fcis-h3-hetzner-bootstrap.sh")
# Disposable test public keys only. No corresponding private keys are retained.
ED25519_PUBLIC = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIL6niuPd0S0q6RZxEQ2RLm69Ib4LRpwzVa2xqC3++P9f"
RSA_PUBLIC = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC5scvVuGvReqWTWfcfls7J3/jQZPxq7A/YZftxJqEptM3FTDu9gsT4j2l3xnAuES5yCtKm9d+DvurOtLKcJRYdrjlhnJdZExu0Vo8rnag9FHQPc4PNsE7KpAnQGO1n1cyrx0Z6nSDmxhHiUtljPvNnlN0b0DnC+LGAmGUD1lXn05PF4M/ftBb9pUbMbOmHYh/vh0Awus/6GGOU+iToPxQsxZ7Dm+j7H/1Sl3YQve/hV9sXYuf7jhh2nVJ/C8SxDXQbwA3rEeSHSUr113BzhJWbMzA3+CpnDXpGEfS45S+XRSDlaQrkIuf8tEDtofG3mzwGiMrC5bfDi47WaT1zmoVT"



class H3BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.env = os.environ.copy()
        if not shutil.which("ssh-keygen"):
            # Minimal test-local fingerprint verifier for container environments
            # missing OpenSSH. Live Ubuntu requires the real ssh-keygen binary.
            bindir = self.folder / "bin"
            bindir.mkdir()
            verifier = bindir / "ssh-keygen"
            verifier.write_text("#!/usr/bin/env python3\nimport base64, struct, sys\ntry:\n    assert sys.argv[1:3] == ['-l','-f']\n    text = open(sys.argv[3]).read().strip().split()\n    assert len(text) in (2,3)\n    key = base64.b64decode(text[1], validate=True)\n    n = struct.unpack('>I',key[:4])[0]\n    assert key[4:4+n].decode('ascii') == text[0]\n    assert n in (7,11)\nexcept Exception:\n    sys.exit(1)\nprint('256 SHA256:TEST (test-only shim)')\n")
            verifier.chmod(0o755)
            self.env["PATH"] = str(bindir) + os.pathsep + self.env.get("PATH", "")

    def run_script(self, *args):
        return subprocess.run(["/bin/sh", str(BOOTSTRAP), *map(str, args)],
                              text=True, capture_output=True, timeout=10, env=self.env)

    def make_key(self, name, kind="ed25519"):
        target = self.folder / (name + ".pub")
        target.write_text((RSA_PUBLIC if kind == "rsa" else ED25519_PUBLIC) + " test-fixture\n")
        return target

    def test_posix_shell_syntax(self):
        subprocess.run(["/bin/sh", "-n", str(BOOTSTRAP)], check=True)

    def test_inspect_is_read_only(self):
        result = self.run_script("--inspect")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("INSPECTED (no changes)", result.stdout)
        self.assertIn("tool", result.stdout)

    def test_valid_ed25519_owner_and_receiver(self):
        owner = self.make_key("owner")
        receiver = self.make_key("receiver")
        result = self.run_script("--check-keys", owner, receiver)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("KEYS VALIDATED (no changes)", result.stdout)

    def test_rsa_receiver_allowed_owner_rsa_refused(self):
        owner = self.make_key("owner-ed25519")
        rsa = self.make_key("receiver-rsa", "rsa")
        accepted = self.run_script("--check-keys", owner, rsa)
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        refused = self.run_script("--check-keys", rsa, owner)
        self.assertEqual(refused.returncode, 2)
        self.assertIn("owner signer must be Ed25519", refused.stderr)

    def test_symlinked_owner_public_key_refused(self):
        owner = self.make_key("owner")
        receiver = self.make_key("receiver")
        link = self.folder / "owner-symlink.pub"
        link.symlink_to(owner)
        result = self.run_script("--check-keys", link, receiver)
        self.assertEqual(result.returncode, 2)
        self.assertIn("symlinked", result.stderr)

    def test_multiple_owner_public_keys_refused(self):
        owner = self.make_key("owner")
        receiver = self.make_key("receiver")
        owner.write_bytes(owner.read_bytes() + owner.read_bytes())
        result = self.run_script("--check-keys", owner, receiver)
        self.assertEqual(result.returncode, 2)
        self.assertIn("exactly one line", result.stderr)

    def test_injected_key_options_refused(self):
        owner = self.make_key("owner")
        receiver = self.make_key("receiver")
        owner.write_text('command="sh -c evil" ' + owner.read_text())
        result = self.run_script("--check-keys", owner, receiver)
        self.assertEqual(result.returncode, 2)
        self.assertIn("malformed SSH public key", result.stderr)

    def test_bad_sha_refused_before_mutation(self):
        result = self.run_script("--apply", "wrong", "/does/not/exist", "/does/not/exist")
        if os.geteuid() == 0:
            self.assertIn("malformed pinned Git SHA", result.stderr)
        else:
            self.assertIn("root authorization required", result.stderr)
        self.assertEqual(result.returncode, 2)

    def test_unexpected_args_refused(self):
        result = self.run_script("--apply")
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage", result.stderr)

    def test_source_has_required_separation(self):
        source = BOOTSTRAP.read_text()
        for fragment in [
            'refs/heads/main',
            'fsck --full',
            'rev-parse --is-shallow-repository',
            'git clone --quiet --bare',
            'getent passwd "$name"',
            'command="git-receive-pack',
            'chown root:root "$BARE/config" "$BARE/hooks" "$BARE/hooks/pre-receive"',
            'chown root:fcis-operator "$POLICY" "$POLICY/repository-id" "$POLICY/authorized_signers" "$POLICY/trusted-files.sha256"',
            'chown root:fcis-git "$ROOT" "$BARE"',
            'chmod 2750 "$ROOT" "$BARE"',
            'chmod 0750 "$POLICY"',
            'chmod 0640 "$POLICY/repository-id" "$POLICY/authorized_signers" "$POLICY/trusted-files.sha256"',
            'groupadd --system fcis-operator',
            '--gid fcis-operator --groups fcis-git',
            'runuser -u fcis-git -- test ! -w "$BARE"',
            'runuser -u fcis-operator -- test ! -w "$BARE"',
            'runuser -u fcis-git -- test ! -r "$POLICY/authorized_signers"',
            'printf \'[safe]\\n\\tdirectory = %s\\n\'',
            'runuser -u fcis-operator',
        ]:
            self.assertIn(fragment, source)
        self.assertNotIn("systemctl", source)
        self.assertNotIn("/etc/caddy", source)
        self.assertNotIn("curl | sh", source)
        self.assertNotIn('chmod 2770 "$ROOT" "$BARE"', source)
        self.assertNotIn('chown -R fcis-git:fcis-git "$ROOT"', source)
        self.assertNotIn('chown -R fcis-operator:fcis-git "$POLICY"', source)
        self.assertIn('RECEIVER_HOME=/var/lib/fcis-owner-git-receiver', source)
        self.assertIn('OPERATOR_HOME=/var/lib/fcis-owner-git-operator', source)



if __name__ == "__main__":
    unittest.main(verbosity=2)
