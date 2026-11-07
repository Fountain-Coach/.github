#!/usr/bin/env python3
"""Project all five canonical FCIS Skills into one existing GitHub-backed plugin.

The plugin identity stays unchanged; this performs only derived Git file changes.
It never installs or promotes a hosted ChatGPT version.
"""
import argparse
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from skillctl import ROOT, digest, entries

SKILL = "fcis-skill-authoring-and-sync"
PLUGIN = SKILL
PLUGIN_PATH = Path("plugins") / PLUGIN
MIRROR_PATH = PLUGIN_PATH / "skills" / SKILL
MARKETPLACE_PATH = Path(".agents/plugins/marketplace.json")
WORKSPACE_PLUGIN_ID = "Plugin_fb9e0937c59c8191b9fa077fa5ea53ef"

# Fixed reviewed inventory: adding a sixth skill is a separate admission, not
# an accidental consequence of a catalog change.
CANONICAL_SKILLS = (
    "estate-publisher-deployment",
    "fcis-skill-authoring-and-sync",
    "linotype-estate-template",
    "satzfunk-voice-render",
    "teatro-scenario-composer",
)


class ProjectionError(ValueError):
    pass


def _read_json(path):
    if path.is_symlink() or not path.is_file():
        raise ProjectionError(f"Required manifest missing or symlinked: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ProjectionError(f"Manifest must be an object: {path}")
    return value


def validate_skill_host_metadata(name, files):
    """Catch provider-documented policy and SVG asset rejects before Git merge."""
    meta = files["agents/openai.yaml"].decode("utf-8")
    if re.search(r"(?m)^  icon:\s*", meta):
        raise ProjectionError(f"{name}: unsupported interface.icon; use icon_small/large")
    match = re.search(r"(?ms)^policy:\n((?:[ \t]+[^\n]*\n)*)", meta)
    if match and re.search(r"(?m)^  products:\s*$", match.group(1)):
        products = re.findall(r"(?m)^  -\s*(\S+)\s*$", match.group(1))
        if not products or any(product not in {"CHAT", "CODEX"} for product in products):
            raise ProjectionError(f"{name}: unsupported policy.products (only CHAT/CODEX)")
    for field, raw_path in re.findall(
        r"(?m)^  (icon_small|icon_large):\s*([^\n]+)$", meta
    ):
        path = raw_path.strip().strip("'\"").removeprefix("./")
        if path not in files:
            raise ProjectionError(f"{name}: {field} asset missing: {path}")
        if path.endswith(".svg"):
            try:
                root = ET.fromstring(files[path])
                width = float(root.attrib["width"])
                height = float(root.attrib["height"])
                box = [float(x) for x in root.attrib["viewBox"].replace(",", " ").split()]
            except (ET.ParseError, KeyError, TypeError, ValueError) as exc:
                raise ProjectionError(f"{name}: malformed {field} SVG") from exc
            if width < 48 or height < 48 or len(box) != 4 or box[2] < 48 or box[3] < 48:
                raise ProjectionError(f"{name}: {field} SVG below 48x48 provider minimum")


def inspect(root=ROOT):
    root = Path(root).resolve(strict=True)
    plugin = _read_json(root / PLUGIN_PATH / "plugin.json")
    market = _read_json(root / MARKETPLACE_PATH)

    if plugin.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ProjectionError("Portable plugin schema is missing")
    if plugin.get("name") != PLUGIN or not re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", "")):
        raise ProjectionError("Plugin identity or version invalid")
    if plugin.get("repository") != "https://github.com/Fountain-Coach/.github":
        raise ProjectionError("Plugin repository must remain canonical")
    interface = plugin.get("extensions", {}).get("com.openai", {}).get("interface", {})
    if not interface.get("displayName"):
        raise ProjectionError("Plugin display name missing")

    # One installed workspace plugin, not five new installations.
    if market.get("name") != "fountain-coach" or len(market.get("plugins", [])) != 1:
        raise ProjectionError("Marketplace must retain the single existing plugin")
    item = market["plugins"][0]
    if item.get("name") != PLUGIN or item.get("source") != {
        "source": "local", "path": "./plugins/fcis-skill-authoring-and-sync"
    }:
        raise ProjectionError("Marketplace source or identity changed")
    if item.get("pluginId") != WORKSPACE_PLUGIN_ID:
        raise ProjectionError("Preserve the existing hosted workspace pluginId")
    if item.get("policy", {}).get("installation") != "AVAILABLE":
        raise ProjectionError("No automatic workspace installation")
    if item.get("policy", {}).get("authentication") != "ON_INSTALL":
        raise ProjectionError("Marketplace authentication policy changed")

    catalog = _read_json(root / "skills" / "openai-distribution.json")
    if catalog.get("owner") != "Fountain-Coach/.github":
        raise ProjectionError("Wrong canonical Skill owner")
    declared = catalog.get("skills")
    if not isinstance(declared, list) or len(declared) != len(CANONICAL_SKILLS):
        raise ProjectionError("Canonical Skill inventory has changed; explicit review required")
    records = {i["name"]: i for i in declared}
    if set(records) != set(CANONICAL_SKILLS):
        raise ProjectionError("Canonical Skill inventory differs from reviewed five")

    source, digests = {}, {}
    for name in CANONICAL_SKILLS:
        if records[name].get("canonicalPath") != f".codex/skills/{name}":
            raise ProjectionError(f"Wrong canonical path for {name}")
        files = entries(root / ".codex" / "skills" / name)
        h = digest(files)
        if h != records[name].get("contentSHA256"):
            raise ProjectionError(f"Unpinned canonical bytes for {name}")
        if "agents/openai.yaml" not in files:
            raise ProjectionError(f"Missing OpenAI metadata for {name}")
        validate_skill_host_metadata(name, files)
        source[name], digests[name] = files, h

    website = records[SKILL].get("marketplaceWebsiteURL")
    if not isinstance(website, str) or not re.fullmatch(r"https://[^\s]+/", website):
        raise ProjectionError("Missing canonical FCIS website")
    return root, plugin, source, digests, website


def _mirrors(root):
    parent = root / PLUGIN_PATH / "skills"
    if parent.is_symlink():
        raise ProjectionError("Refusing skill directory symlink")
    if parent.exists():
        extras = sorted(p.name for p in parent.iterdir() if p.name not in CANONICAL_SKILLS)
        if extras:
            raise ProjectionError("Unknown plugin skill entries: " + ", ".join(extras))
    observed = {}
    for name in CANONICAL_SKILLS:
        dest = parent / name
        if dest.is_symlink() or (dest.exists() and not dest.is_dir()):
            raise ProjectionError("Refusing unexpected mirror type: " + name)
        if dest.exists() and not (dest / "SKILL.md").is_file():
            raise ProjectionError("Incomplete existing mirror: " + name)
        observed[name] = entries(dest) if dest.exists() else {}
    return observed


def check(root=ROOT):
    root, plugin, source, digests, website = inspect(root)
    if plugin["extensions"]["com.openai"]["interface"].get("websiteURL") != website:
        raise ProjectionError("Plugin websiteURL differs from canonical metadata")
    observed = _mirrors(root)
    for name in CANONICAL_SKILLS:
        if observed[name] != source[name]:
            expected, actual = source[name], observed[name]
            missing = sorted(expected.keys() - actual.keys())
            extra = sorted(actual.keys() - expected.keys())
            modified = sorted(p for p in expected.keys() & actual.keys() if expected[p] != actual[p])
            raise ProjectionError(f"Derived {name} drift: missing={missing}, extra={extra}, modified={modified}")
    return {"state": "MATCHED", "plugin": PLUGIN, "version": plugin["version"],
            "sourceSkill": SKILL, "contentSHA256": digests[SKILL], "skills": digests}


def sync(root=ROOT):
    root, plugin, source, digests, website = inspect(root)
    interface = plugin["extensions"]["com.openai"]["interface"]
    metadata_changed = interface.get("websiteURL") != website
    if metadata_changed:
        interface["websiteURL"] = website
    existing = _mirrors(root)

    changed = set()
    for name in CANONICAL_SKILLS:
        current = existing[name]
        target = source[name]
        unexpected = current.keys() - target.keys()
        if unexpected:
            raise ProjectionError(f"Refusing to remove unreviewed {name} files: {sorted(unexpected)}")
        if current != target:
            changed.add(name)

    # Validate all packages before touching any derived files.
    for name in changed:
        dest = root / PLUGIN_PATH / "skills" / name
        for relative, data in source[name].items():
            path = dest / relative
            if path.is_symlink():
                raise ProjectionError(f"Refusing mirror symlink: {name}/{relative}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

    # One existing plugin identity, one patch bump even if multiple skills changed.
    # A brand-new empty test fixture starts at its initial version.
    if any(existing.values()) and (changed or metadata_changed):
        major, minor, patch = map(int, plugin["version"].split("."))
        plugin["version"] = f"{major}.{minor}.{patch + 1}"
    if metadata_changed or (any(existing.values()) and changed):
        (root / PLUGIN_PATH / "plugin.json").write_text(
            json.dumps(plugin, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    result = check(root)
    if changed or metadata_changed:
        result["state"] = "SYNCED"
        result["changedSkills"] = sorted(changed)
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
