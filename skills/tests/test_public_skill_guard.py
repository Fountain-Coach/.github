import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from public_skill_guard import validate_paths

class PublicSkillGuardTests(unittest.TestCase):
    def test_existing_public_exceptions(self):
        validate_paths(["skills/canonical/README.md", "skills/canonical/fcis-go/SKILL.md",
                        ".codex/skills/fcis-owner-access/SKILL.md",
                        "plugins/fcis-skill-authoring-and-sync/skills/fcis-go/SKILL.md"])

    def test_new_private_or_unapproved_paths_refused(self):
        for path in ["skills/canonical/new-development/SKILL.md",
                     "skills/canonical/new-development/references/content.md",
                     ".codex/skills/new-development/SKILL.md",
                     "plugins/another/skills/new-development/SKILL.md",
                     "docs/some-new-skill/SKILL.md", "skills/private/content.txt",
                     "skills/paid/example.md", "skills/canonical/fcis-console-development/SKILL.md"]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                validate_paths([path])
