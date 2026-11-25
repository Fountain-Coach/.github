"""Git-owned FCIS marketplace projection and refusal tests."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import plugin_projection as projection
from skillctl import digest, entries

# Independent source fixtures: the provider chooses from descriptions first.
# These must remain explicit and not be derived from the projection validator.
TRIGGER_DESCRIPTIONS = {
    "fcis-skill-authoring-and-sync": "Skill routing preflight and plugin maintenance",
    "fcis-owner-access": "iPad passkey session redirect Access",
    "fcis-go-runtime-migration": "Go runtime release, consult fcis-owner-access",
}
RESOLUTION_PRELUDE = (
    "**Governing-Skill resolution — before external tools:** "
    "Use skills__list and skills__read; choose fcis-owner-access for owner UX, "
    "fcis-go-runtime-migration for Go release, fcis-skill-authoring-and-sync "
    "for Skill routing; preserve the original user goal and Definition of Done.\n\n"
)


class MarketplaceProjectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.canonical = self.root / ".codex/skills" / projection.SKILL
        self.canonical.mkdir(parents=True)
        self.canonical.joinpath("SKILL.md").write_text(
            "---\nname: fcis-skill-authoring-and-sync\ndescription: "
            + TRIGGER_DESCRIPTIONS[projection.SKILL] + "\n---\n\n"
            "# FCIS Skill Authoring\n\n"
            "## First operational gate — stop the Invented-Prerequisite Loop\n\n"
            + RESOLUTION_PRELUDE
            + "Preserve original goal; demand observed failure, smallest correction; "
            "PROPOSED / non-blocking; use reversal before a moving Definition of Done.\n"
        )
        self.canonical.joinpath("agents").mkdir()
        self.canonical.joinpath("agents/openai.yaml").write_text(
            "interface:\n  display_name: FCIS\n"
        )
        catalog = self.root / "skills/openai-distribution.json"
        catalog.parent.mkdir(parents=True)
        rows = []
        for name in projection.CANONICAL_SKILLS:
            folder = self.root / ".codex" / "skills" / name
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "agents").mkdir(exist_ok=True)
            if name != projection.SKILL:
                description = TRIGGER_DESCRIPTIONS.get(name, "Reviewed")
                sample = ("---\nname: " + name + "\ndescription: " + description
                          + "\n---\n# " + name + "\n")
                if name in projection.ANTI_LOOP_GATED_SKILLS:
                    sample += ("\n## First operational gate — stop the Invented-Prerequisite Loop\n\n"
                               + RESOLUTION_PRELUDE
                               + "Preserve original goal; demand observed failure, smallest correction; "
                               "PROPOSED / non-blocking; use reversal before a moving Definition of Done.\n")
                (folder / "SKILL.md").write_text(sample)
                (folder / "agents/openai.yaml").write_text(
                    "interface:\n  display_name: " + name + "\n"
                )
            row = {"name": name, "canonicalPath": ".codex/skills/" + name,
                   "contentSHA256": digest(entries(folder))}
            if name == projection.SKILL:
                row["marketplaceWebsiteURL"] = "https://fcis.fountain.coach/"
            rows.append(row)
        catalog.write_text(json.dumps({
            "owner": "Fountain-Coach/.github", "skills": rows
        }))
        self.active = self.root / ".codex/skills/fcis-go"
        self.active.mkdir(parents=True)
        (self.active / "agents").mkdir()
        (self.active / "SKILL.md").write_text(
            "---\nname: fcis-go\ndescription: Govern FCIS-GO marketplace publication\n---\n"
            "# FCIS-GO\n\nResolve owner purpose and source evidence.\n")
        (self.active / "agents/openai.yaml").write_text(
            "interface:\n  display_name: FCIS-GO\n")
        self.neutral = self.root / "skills/canonical/fcis-go"
        self.neutral.mkdir(parents=True)
        (self.neutral / "SKILL.md").write_bytes((self.active / "SKILL.md").read_bytes())
        active = {
            "owner":"Fountain-Coach/.github",
            "maintainedSourceCatalog":"skills/openai-distribution.json",
            "activePluginId":projection.WORKSPACE_PLUGIN_ID,
            "activeSkill":{
                "name":"fcis-go",
                "canonicalPath":"skills/canonical/fcis-go",
                "marketplaceWebsiteURL":"https://fcis.fountain.coach/",
                "contentSHA256":digest(entries(self.neutral)),
                "projections":{"openai":{
                    "path":".codex/skills/fcis-go",
                    "contentSHA256":digest(entries(self.active)),
                }},
            }
        }
        (self.root / projection.ACTIVE_MANIFEST_PATH).write_text(json.dumps(active))
        self.marketplace = self.root / projection.MARKETPLACE_PATH
        self.marketplace.parent.mkdir(parents=True)
        self.marketplace.write_text(json.dumps({
            "name": "fountain-coach",
            "plugins": [{
                "name": projection.PLUGIN,
                "pluginId": projection.WORKSPACE_PLUGIN_ID,
                "source": {
                    "source": "local",
                    "path": "./plugins/fcis-skill-authoring-and-sync"
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL"
                }
            }]
        }))
        self.manifest = self.root / projection.PLUGIN_PATH / "plugin.json"
        self.manifest.parent.mkdir(parents=True)
        self.manifest.write_text(json.dumps({
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": projection.PLUGIN,
            "version": "0.1.0",
            "repository": "https://github.com/Fountain-Coach/.github",
            "extensions": {"com.openai": {
                "interface": {"displayName": "FCIS"}
            }}
        }))

    def test_refuses_partial_or_invalid_marketplace_logo_asset(self):
        data = json.loads(self.manifest.read_text())
        interface = data["extensions"]["com.openai"]["interface"]
        interface["logo"] = "./assets/fountain-coach-logo.png"
        self.manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(projection.ProjectionError, "logo and composerIcon"):
            projection.check(self.root)
        interface["composerIcon"] = "./assets/fountain-coach-logo.png"
        self.manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(projection.ProjectionError, "missing, unsafe"):
            projection.check(self.root)
        asset = self.root / projection.PLUGIN_PATH / "assets/fountain-coach-logo.png"
        asset.parent.mkdir(parents=True)
        asset.write_bytes(b"not an image")
        with self.assertRaisesRegex(projection.ProjectionError, "PNG header"):
            projection.check(self.root)

    def test_first_sync_copies_only_exact_canonical_tree(self):
        result = projection.sync(self.root)
        self.assertEqual(result["state"], "SYNCED")
        self.assertEqual(result["version"], "0.1.0")
        self.assertEqual(entries(self.active), entries(self.root / projection.MIRROR_PATH))

    def _approve_mcp(self):
        path = self.root / projection.ACTIVE_MANIFEST_PATH
        data = json.loads(path.read_text())
        data["mcpConnection"] = {
            "schemaVersion": 1, "serverName": "fcis", "transport": "streamable-http",
            "url": "https://go.fcis.fountain.coach/mcp", "authentication": "oauth",
            "chargeBasis": "included-subscription", "sourceRelease": "a" * 40,
        }
        path.write_text(json.dumps(data))
        return path, data

    def test_approved_mcp_projects_once_without_skill_expansion(self):
        projection.sync(self.root)
        self._approve_mcp()
        with self.assertRaisesRegex(projection.ProjectionError, "MCP projection missing"):
            projection.check(self.root)
        result = projection.sync(self.root)
        self.assertEqual(result["version"], "0.1.1")
        self.assertEqual(result["mcpConnection"], "https://go.fcis.fountain.coach/mcp")
        self.assertEqual(set(result["skills"]), {"fcis-go"})
        config = json.loads((self.root / projection.MCP_PATH).read_text())
        self.assertEqual(config, {
            "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
            "mcpServers": {"fcis": {"type": "streamable-http",
                "url": "https://go.fcis.fountain.coach/mcp",
                "extensions": {"com.openai": {"auth": {"type": "oauth"}}}}}})
        self.assertEqual(projection.sync(self.root)["version"], "0.1.1")

    def test_mcp_refuses_paid_route_unknown_endpoint_and_credentials(self):
        projection.sync(self.root)
        path, data = self._approve_mcp()
        for field, value in (("chargeBasis", "metered"),
                             ("url", "https://untrusted.invalid/mcp"),
                             ("authentication", "none"),
                             ("apiKey", "synthetic-not-a-secret")):
            candidate = json.loads(json.dumps(data))
            candidate["mcpConnection"][field] = value
            path.write_text(json.dumps(candidate))
            with self.assertRaisesRegex(projection.ProjectionError, "Unapproved FCIS MCP"):
                projection.sync(self.root)
        self.assertFalse((self.root / projection.MCP_PATH).exists())

    def test_mcp_refuses_unreviewed_projection_overwrite(self):
        projection.sync(self.root)
        self._approve_mcp()
        projection.sync(self.root)
        path = self.root / projection.MCP_PATH
        config = json.loads(path.read_text())
        config["mcpServers"]["unknown"] = {"type": "streamable-http", "url": "https://untrusted.invalid"}
        path.write_text(json.dumps(config))
        with self.assertRaisesRegex(projection.ProjectionError, "Unreviewed MCP projection"):
            projection.sync(self.root)
        self.assertEqual(json.loads(path.read_text()), config)

    def test_repeat_sync_is_a_no_op(self):
        projection.sync(self.root)
        result = projection.sync(self.root)
        self.assertEqual(result["state"], "MATCHED")
        self.assertEqual(result["version"], "0.1.0")

    def test_metadata_only_website_drift_is_corrected_and_versioned(self):
        projection.sync(self.root)
        data = json.loads(self.manifest.read_text())
        data["extensions"]["com.openai"]["interface"]["websiteURL"] = "https://fountain.coach"
        self.manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(projection.ProjectionError, "websiteURL"):
            projection.check(self.root)
        result = projection.sync(self.root)
        self.assertEqual(result["state"], "SYNCED")
        self.assertEqual(result["version"], "0.1.1")
        updated = json.loads(self.manifest.read_text())
        self.assertEqual(
            updated["extensions"]["com.openai"]["interface"]["websiteURL"],
            "https://fcis.fountain.coach/",
        )
        self.assertEqual(entries(self.active), entries(self.root / projection.MIRROR_PATH))

    def test_source_change_requires_sync_and_versions_derived_release(self):
        projection.sync(self.root)
        (self.neutral / "SKILL.md").write_text(
            (self.neutral / "SKILL.md").read_text() + "\nVerified learning.\n"
        )
        (self.active / "SKILL.md").write_bytes((self.neutral / "SKILL.md").read_bytes())
        self._re_pin_active()
        with self.assertRaises(projection.ProjectionError):
            projection.check(self.root)
        result = projection.sync(self.root)
        self.assertEqual(result["version"], "0.1.1")
        self.assertEqual(result["state"], "SYNCED")
        self.assertEqual(projection.check(self.root)["state"], "MATCHED")
        self.assertEqual(
            json.loads(self.marketplace.read_text())["plugins"][0]["pluginId"],
            projection.WORKSPACE_PLUGIN_ID,
        )

    def test_only_one_active_skill_and_nine_retained_source_skills(self):
        result = projection.sync(self.root)
        self.assertEqual(set(result["skills"]), {"fcis-go"})
        self.assertEqual(result["changedSkills"], ["fcis-go"])
        self.assertEqual(set(result["maintainedCanonicalSkills"]), set(projection.CANONICAL_SKILLS))
        self.assertEqual(sorted(p.name for p in (self.root / projection.PLUGIN_PATH / "skills").iterdir()), ["fcis-go"])
        self.assertEqual(entries(self.root / ".codex/skills/fcis-go"),
                         entries(self.root / projection.PLUGIN_PATH / "skills/fcis-go"))
        self.assertEqual(len(json.loads(self.marketplace.read_text())["plugins"]), 1)

    def test_provider_cannot_override_accepted_neutral_instruction(self):
        projection.sync(self.root)
        (self.active / "SKILL.md").write_text(
            (self.active / "SKILL.md").read_text() + "\nUnapproved provider change.\n")
        # Even pinning the derived hash cannot let a vendor projection change
        # the Fountain Coach instruction source.
        self._re_pin_active()
        with self.assertRaisesRegex(projection.ProjectionError,
                                    "adapter instructions drift"):
            projection.check(self.root)
        with self.assertRaises(projection.ProjectionError):
            projection.sync(self.root)

    def test_neutral_source_revision_requires_explicit_adapter_reprojection(self):
        projection.sync(self.root)
        (self.neutral / "SKILL.md").write_text(
            (self.neutral / "SKILL.md").read_text() + "\nReviewed owner change.\n")
        old = (self.active / "SKILL.md").read_bytes()
        with self.assertRaises(projection.ProjectionError):
            projection.check(self.root)
        with self.assertRaises(projection.ProjectionError):
            projection.sync(self.root)
        self.assertEqual((self.active / "SKILL.md").read_bytes(), old)

    def test_rejects_provider_path_as_active_owner_authority(self):
        public = self.root / projection.ACTIVE_MANIFEST_PATH
        data = json.loads(public.read_text())
        data["activeSkill"]["canonicalPath"] = ".codex/skills/fcis-go"
        public.write_text(json.dumps(data))
        with self.assertRaisesRegex(projection.ProjectionError,
                                    "neutral FCIS source identity"):
            projection.check(self.root)

    def test_maintenance_source_edit_does_not_widen_public_surface(self):
        projection.sync(self.root)
        other = "linotype-estate-template"
        source = self.root / ".codex" / "skills" / other
        (source / "SKILL.md").write_text((source / "SKILL.md").read_text() +
                                        "\nReviewed security correction.\n")
        self._re_pin(other)
        result = projection.check(self.root)
        self.assertEqual(result["state"], "MATCHED")
        self.assertEqual(projection.sync(self.root)["state"], "MATCHED")
        self.assertEqual(result["version"], "0.1.0")
        self.assertFalse((self.root / projection.PLUGIN_PATH / "skills" / other).exists())

    def test_active_skill_revision_bumps_once(self):
        projection.sync(self.root)
        (self.neutral / "SKILL.md").write_text(
            (self.neutral / "SKILL.md").read_text() + "\nOwner-accepted release correction.\n")
        (self.active / "SKILL.md").write_bytes((self.neutral / "SKILL.md").read_bytes())
        self._re_pin_active()
        with self.assertRaises(projection.ProjectionError):
            projection.check(self.root)
        changed = projection.sync(self.root)
        self.assertEqual(changed["version"], "0.1.1")
        self.assertEqual(changed["changedSkills"], ["fcis-go"])
        self.assertEqual(projection.sync(self.root)["state"], "MATCHED")

    def test_retiring_old_exact_mirrors_removes_only_derived_copies(self):
        # Reconstruct one retired legacy mirror as if this were 0.1.39.
        name = "linotype-estate-template"
        import shutil
        old = self.root / projection.PLUGIN_PATH / "skills" / name
        shutil.copytree(self.root / ".codex/skills" / name, old)
        before = entries(self.root / ".codex/skills" / name)
        result = projection.sync(self.root)
        self.assertEqual(result["removedMaintainedMirrors"], [name])
        self.assertFalse(old.exists())
        self.assertEqual(entries(self.root / ".codex/skills" / name), before)
        self.assertEqual(sorted(p.name for p in old.parent.iterdir()), ["fcis-go"])

    def test_retirement_refuses_modified_old_mirror_without_deletion(self):
        import shutil
        name = "fcis-swift-build"
        old = self.root / projection.PLUGIN_PATH / "skills" / name
        shutil.copytree(self.root / ".codex/skills" / name, old)
        (old / "SKILL.md").write_text("Unreviewed live instruction\n")
        canonical = entries(self.root / ".codex/skills" / name)
        with self.assertRaisesRegex(projection.ProjectionError, "drifted"):
            projection.sync(self.root)
        self.assertTrue(old.exists())
        self.assertEqual(entries(self.root / ".codex/skills" / name), canonical)

    def _re_pin_active(self):
        path = self.root / projection.ACTIVE_MANIFEST_PATH
        data = json.loads(path.read_text())
        data["activeSkill"]["contentSHA256"] = digest(entries(self.neutral))
        data["activeSkill"]["projections"]["openai"]["contentSHA256"] = digest(entries(self.active))
        path.write_text(json.dumps(data))

    def _re_pin(self, name):
        catalog = self.root / "skills/openai-distribution.json"
        data = json.loads(catalog.read_text())
        next(item for item in data["skills"] if item["name"] == name)[
            "contentSHA256"
        ] = digest(entries(self.root / ".codex/skills" / name))
        catalog.write_text(json.dumps(data))

    def test_refuses_missing_governing_skill_preflight(self):
        projection.sync(self.root)
        for name in projection.ANTI_LOOP_GATED_SKILLS:
            with self.subTest(skill=name):
                path = self.root / ".codex/skills" / name / "SKILL.md"
                original = path.read_text()
                path.write_text(original.replace(RESOLUTION_PRELUDE, "", 1))
                self._re_pin(name)
                with self.assertRaisesRegex(projection.ProjectionError, "governing Skill resolution"):
                    projection.check(self.root)
                path.write_text(original)
                self._re_pin(name)
        self.assertEqual(projection.check(self.root)["state"], "MATCHED")

    def test_refuses_skill_resolution_displaced_below_other_action(self):
        projection.sync(self.root)
        path = self.canonical / "SKILL.md"
        original = path.read_text()
        path.write_text(original.replace(
            RESOLUTION_PRELUDE,
            "Run Git first.\n\n" + RESOLUTION_PRELUDE, 1))
        self._re_pin(projection.SKILL)
        with self.assertRaisesRegex(projection.ProjectionError, "governing Skill resolution"):
            projection.check(self.root)

    def test_refuses_missing_owner_ux_routing_in_metadata(self):
        projection.sync(self.root)
        name = "fcis-owner-access"
        path = self.root / ".codex/skills" / name / "SKILL.md"
        original = path.read_text()
        path.write_text(original.replace("iPad passkey session redirect Access", "generic automation"))
        self._re_pin(name)
        with self.assertRaisesRegex(projection.ProjectionError, "metadata missing routing trigger"):
            projection.check(self.root)

    def test_refuses_missing_skill_read_or_list_instruction(self):
        projection.sync(self.root)
        name = "fcis-owner-access"
        path = self.root / ".codex/skills" / name / "SKILL.md"
        original = path.read_text()
        path.write_text(original.replace(
            "Use skills__list and skills__read", "Use generic tooling", 1))
        self._re_pin(name)
        with self.assertRaisesRegex(projection.ProjectionError, "incomplete governing Skill resolution"):
            projection.check(self.root)

    def test_refuses_displaced_creator_first_gate(self):
        projection.sync(self.root)
        path = self.canonical / "SKILL.md"
        contents = path.read_text()
        contents = contents.replace(
            "# FCIS Skill Authoring\n\n## First operational gate",
            "# FCIS Skill Authoring\n\n## Unrelated work first\n\n## First operational gate",
            1,
        )
        path.write_text(contents)
        catalog = self.root / "skills/openai-distribution.json"
        data = json.loads(catalog.read_text())
        next(item for item in data["skills"] if item["name"] == projection.SKILL)[
            "contentSHA256"
        ] = digest(entries(self.canonical))
        catalog.write_text(json.dumps(data))
        with self.assertRaisesRegex(projection.ProjectionError, "first operational gate"):
            projection.sync(self.root)

    def test_refuses_synthetic_gate_with_no_observed_failure(self):
        projection.sync(self.root)
        path = self.root / ".codex/skills/fcis-owner-access/SKILL.md"
        path.write_text(path.read_text().replace("observed failure", "plausible concern"))
        catalog = self.root / "skills/openai-distribution.json"
        data = json.loads(catalog.read_text())
        next(item for item in data["skills"] if item["name"] == "fcis-owner-access")[
            "contentSHA256"
        ] = digest(entries(path.parent))
        catalog.write_text(json.dumps(data))
        with self.assertRaisesRegex(projection.ProjectionError, "incomplete first operational anti-loop gate"):
            projection.sync(self.root)

    def test_rejects_unreviewed_tenth_skill(self):
        projection.sync(self.root)
        extra = self.root / projection.PLUGIN_PATH / "skills" / "intruder"
        extra.mkdir()
        (extra / "SKILL.md").write_text("unreviewed\n")
        with self.assertRaisesRegex(projection.ProjectionError, "Unknown"):
            projection.sync(self.root)

    def test_refuses_unreviewed_extra_mirror_file(self):
        projection.sync(self.root)
        extra = self.root / projection.MIRROR_PATH / "unrelated.txt"
        extra.write_text("Do not delete\n")
        with self.assertRaises(projection.ProjectionError):
            projection.sync(self.root)
        self.assertEqual(extra.read_text(), "Do not delete\n")

    def test_refuses_default_install_policy(self):
        data = json.loads(self.marketplace.read_text())
        data["plugins"][0]["policy"]["installation"] = "INSTALLED_BY_DEFAULT"
        self.marketplace.write_text(json.dumps(data))
        with self.assertRaises(projection.ProjectionError):
            projection.sync(self.root)

    def test_refuses_lost_or_changed_workspace_plugin_identity(self):
        for alternative in (None, "Plugin_00000000000000000000000000000000"):
            data = json.loads(self.marketplace.read_text())
            if alternative is None:
                data["plugins"][0].pop("pluginId", None)
            else:
                data["plugins"][0]["pluginId"] = alternative
            self.marketplace.write_text(json.dumps(data))
            with self.assertRaisesRegex(projection.ProjectionError, "pluginId"):
                projection.sync(self.root)
            with self.assertRaisesRegex(projection.ProjectionError, "pluginId"):
                projection.check(self.root)

    def test_invalid_product_policy_is_refused_before_projection(self):
        source = self.root / ".codex/skills/linotype-estate-template"
        with (source / "agents/openai.yaml").open("a") as out:
            out.write("policy:\n  products:\n  - chatgpt\n  - atlas\n")
        catalog = self.root / "skills/openai-distribution.json"
        data = json.loads(catalog.read_text())
        next(item for item in data["skills"] if item["name"] == "linotype-estate-template"
             )["contentSHA256"] = digest(entries(source))
        catalog.write_text(json.dumps(data))
        with self.assertRaisesRegex(projection.ProjectionError, "policy.products"):
            projection.sync(self.root)

    def test_undersized_svg_is_refused_before_projection(self):
        source = self.root / ".codex/skills/teatro-scenario-composer"
        asset = source / "assets/icon.svg"
        asset.parent.mkdir()
        asset.write_text('<svg width="24" height="24" viewBox="0 0 24 24"/>')
        with (source / "agents/openai.yaml").open("a") as out:
            out.write("  icon_small: assets/icon.svg\n")
        catalog = self.root / "skills/openai-distribution.json"
        data = json.loads(catalog.read_text())
        next(item for item in data["skills"] if item["name"] == "teatro-scenario-composer"
             )["contentSHA256"] = digest(entries(source))
        catalog.write_text(json.dumps(data))
        with self.assertRaisesRegex(projection.ProjectionError, "below 48x48"):
            projection.sync(self.root)

    def test_refuses_changed_canonical_digest(self):
        self.canonical.joinpath("SKILL.md").write_text("Unrecorded source edit\n")
        with self.assertRaises(projection.ProjectionError):
            projection.sync(self.root)


if __name__ == "__main__":
    unittest.main()
