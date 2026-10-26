import hashlib
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import skillctl as ctl

class SovereigntyTests(unittest.TestCase):
    def test_canonical_packages(self):
        self.assertEqual(len(ctl.validate()["skills"]), 3)
    def test_repeatable_zip_and_roundtrip(self):
        files = ctl.entries(ctl.SKILLS / "teatro-scenario-composer")
        data = ctl.archive(files, "teatro-scenario-composer")
        self.assertEqual(data, ctl.archive(files, "teatro-scenario-composer"))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "skill.zip"
            path.write_bytes(data)
            self.assertEqual(files, ctl.read_archive(path, "teatro-scenario-composer"))
    def test_modified_content(self):
        state, delta = ctl.compare({"SKILL.md": b"source"}, {"SKILL.md": b"changed"})
        self.assertEqual((state, delta["modified"]), ("DRIFT", ["SKILL.md"]))
    def test_added_removed(self):
        state, delta = ctl.compare({"SKILL.md": b"a", "assets/a": b"b"}, {"SKILL.md": b"a", "foreign": b"c"})
        self.assertEqual(state, "DRIFT")
        self.assertEqual(delta["missing"], ["assets/a"])
        self.assertEqual(delta["unexpected"], ["foreign"])
    def test_unverified_remote(self):
        self.assertEqual(ctl.compare({"SKILL.md": b"source"}, None)[0], "UNVERIFIED")
    def test_deleted_remote_preserves_source(self):
        original = {"SKILL.md": b"canonical"}
        self.assertEqual(ctl.compare(original, {})[0], "DRIFT")
        self.assertEqual(original["SKILL.md"], b"canonical")
    def test_duplicate_zip_member_rejected(self):
        import zipfile
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.zip"
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("sample/SKILL.md", "a")
                z.writestr("sample/SKILL.md", "b")
            with self.assertRaises(ValueError):
                ctl.read_archive(path, "sample")
    def test_unsafe_zip_member_rejected(self):
        import zipfile
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unsafe.zip"
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("other/SKILL.md", "a")
            with self.assertRaises(ValueError):
                ctl.read_archive(path, "sample")

if __name__ == "__main__":
    unittest.main()
