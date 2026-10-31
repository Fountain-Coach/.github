#!/usr/bin/env python3
"""Project one FCIS-owned Git Skill into a GitHub-backed ChatGPT plugin.

This is a derived package. Sync is an explicit distribution-preparation step;
nothing here installs, activates, publishes or deletes an account Skill.
"""
import argparse
import json
from pathlib import Path
import re

from skillctl import ROOT, digest, entries

SKILL = "fcis-skill-authoring-and-sync"
PLUGIN = "fcis-skill-authoring-and-sync"
PLUGIN_PATH = Path("plugins") / SKILL
MIRROR_PATH = PLUGIN_PATH / "skills" / SKILL
MARKETPLACE_PATH = Path(".agents/plugins/marketplace.json")
# Existing uploaded ChatGPT workspace plugin, observed in the authenticated admin URL.
# OpenAI marketplace takeover must preserve this identity rather than add another.
WORKSPACE_PLUGIN_ID = "Plugin_fb9e0937c59c8191b9fa077fa5ea53ef"


class ProjectionError(ValueError):
    pass


def _read_json(path):
    if path.is_symlink() or not path.is_file():
        raise ProjectionError(f"Required manifest missing or symlinked: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ProjectionError(f"Manifest must be an object: {path}")
    return value


def inspect(root=ROOT):
    root = Path(root).resolve(strict=True)
    manifest_path = root / PLUGIN_PATH / "plugin.json"
    market_path = root / MARKETPLACE_PATH
    plugin = _read_json(manifest_path)
    market = _read_json(market_path)

    if plugin.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ProjectionError("Plugin manifest lacks the portable schema")
    if plugin.get("name") != PLUGIN or not re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", "")):
        raise ProjectionError("Plugin identity or semantic version invalid")
    if plugin.get("repository") != "https://github.com/Fountain-Coach/.github":
        raise ProjectionError("Plugin does not point to canonical Git owner")
    if not plugin.get("extensions", {}).get("com.openai", {}).get("interface", {}).get("displayName"):
        raise ProjectionError("Plugin display name missing")

    if market.get("name") != "fountain-coach" or len(market.get("plugins", [])) != 1:
        raise ProjectionError("Marketplace must contain exactly one bounded FCIS entry")
    item = market["plugins"][0]
    if item.get("name") != PLUGIN or item.get("source") != {
        "source": "local", "path": "./plugins/fcis-skill-authoring-and-sync"
    }:
        raise ProjectionError("Marketplace source path or plugin identity differs")
    if item.get("pluginId") != WORKSPACE_PLUGIN_ID:
        raise ProjectionError("Existing ChatGPT workspace pluginId must be preserved")
    if item.get("policy", {}).get("installation") != "AVAILABLE":
        raise ProjectionError("Marketplace must not silently install a plugin")
    if item.get("policy", {}).get("authentication") != "ON_INSTALL":
        raise ProjectionError("Marketplace authentication policy mismatch")

    catalog = _read_json(root / "skills" / "openai-distribution.json")
    if catalog.get("owner") != "Fountain-Coach/.github":
        raise ProjectionError("Canonical Skill ownership mismatch")
    try:
        declared = next(x for x in catalog["skills"] if x["name"] == SKILL)
    except (KeyError, StopIteration) as exc:
        raise ProjectionError("Canonical Skill has no catalog entry") from exc
    source = entries(root / ".codex" / "skills" / SKILL)
    source_digest = digest(source)
    if declared["contentSHA256"] != source_digest:
        raise ProjectionError("Canonical Skill file tree differs from pinned digest")
    website = declared.get("marketplaceWebsiteURL")
    if not isinstance(website, str) or not re.fullmatch(r"https://[^\s]+/", website):
        raise ProjectionError("Canonical FCIS marketplace website URL missing or invalid")
    return root, plugin, source, source_digest, website


def check(root=ROOT):
    root, plugin, source, source_digest, website = inspect(root)
    interface = plugin["extensions"]["com.openai"]["interface"]
    if interface.get("websiteURL") != website:
        raise ProjectionError("Plugin websiteURL differs from canonical distribution metadata")
    dest = root / MIRROR_PATH
    if not dest.exists():
        raise ProjectionError("Plugin skill mirror not yet materialized")
    mirror = entries(dest)
    if source != mirror:
        missing = sorted(source.keys() - mirror.keys())
        unexpected = sorted(mirror.keys() - source.keys())
        modified = sorted(p for p in source.keys() & mirror.keys() if source[p] != mirror[p])
        raise ProjectionError(
            f"Derived Skill drift: missing={missing}, unexpected={unexpected}, modified={modified}"
        )
    return {"state": "MATCHED", "plugin": PLUGIN, "version": plugin["version"],
            "sourceSkill": SKILL, "contentSHA256": source_digest}


def sync(root=ROOT):
    root, plugin, source, _, website = inspect(root)
    interface = plugin["extensions"]["com.openai"]["interface"]
    metadata_changed = interface.get("websiteURL") != website
    if metadata_changed:
        interface["websiteURL"] = website

    dest = root / MIRROR_PATH
    existing = entries(dest) if (dest / "SKILL.md").is_file() else {}
    unexpected = set(existing) - set(source)
    if unexpected:
        raise ProjectionError("Refusing to remove unreviewed mirror files: " + ", ".join(sorted(unexpected)))

    mirror_changed = existing != source
    if mirror_changed:
        for relative, data in source.items():
            target = dest / relative
            if target.is_symlink():
                raise ProjectionError(f"Refusing to replace a mirror symlink: {relative}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

    if existing and (mirror_changed or metadata_changed):
        major, minor, patch = map(int, plugin["version"].split("."))
        plugin["version"] = f"{major}.{minor}.{patch + 1}"

    if metadata_changed or (existing and mirror_changed):
        (root / PLUGIN_PATH / "plugin.json").write_text(
            json.dumps(plugin, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    if not mirror_changed and not metadata_changed:
        return check(root)
    result = check(root)
    result["state"] = "SYNCED"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "sync"])
    args = parser.parse_args()
    try:
        result = check() if args.command == "check" else sync()
    except (ProjectionError, OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"REFUSED: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
