"""Source-only checks for the owner-operated Mac to Hetzner H3 bootstrap.

Never invokes SSH, SCP, generates a real key or modifies a host.
"""
from pathlib import Path
import hashlib
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
MAC = ROOT / "scripts" / "fcis-h3-mac-onetime-setup.sh"
HOST = ROOT / "scripts" / "fcis-h3-hetzner-bootstrap.sh"
if not MAC.is_file():
    MAC = Path(__file__).with_name("fcis-h3-mac-onetime-setup.sh")
    HOST = Path(__file__).with_name("fcis-h3-hetzner-bootstrap.sh")


class MacOwnerSetupSourceTests(unittest.TestCase):
    def test_bash_syntax(self):
        subprocess.run(["bash", "-n", str(MAC)], check=True)

    def test_explicit_apply_required_before_any_network_or_key_effect(self):
        r = subprocess.run(["bash", str(MAC)], capture_output=True, text=True, timeout=5)
        self.assertEqual(r.returncode, 2)
        self.assertIn("explicit --apply required", r.stderr)
        self.assertLess(MAC.read_text().index("explicit --apply required"), MAC.read_text().index("curl -fsSL"))

    def test_pinned_bootstrap_sha256_matches_real_source_bytes(self):
        text = MAC.read_text()
        match = re.search(r"^SOURCE_SHA256='([a-f0-9]{64})'$", text, re.MULTILINE)
        self.assertIsNotNone(match)
        self.assertEqual(hashlib.sha256(HOST.read_bytes()).hexdigest(), match.group(1))

    def test_owner_public_key_only_transfer_and_gating(self):
        text = MAC.read_text()
        transfer = [line for line in text.splitlines() if line.startswith("scp -q")]
        self.assertEqual(len(transfer), 2)
        self.assertNotIn('"$SIGNER_KEY"', "\n".join(transfer))
        self.assertIn('"$LOCAL_TMP/owner.pub"', "\n".join(transfer))
        self.assertIn('"$LOCAL_TMP/receiver.pub"', "\n".join(transfer))
        self.assertLess(text.index(' --inspect'), text.index('ssh-keygen -t ed25519'))
        self.assertLess(text.index(' --check-keys'), text.rindex(' --apply'))
        self.assertIn('StrictHostKeyChecking=yes', text)
        self.assertIn('ACTUAL_SHA256', text)
        self.assertNotIn('curl | bash', text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
