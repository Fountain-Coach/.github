#!/usr/bin/env python3
"""One-way, owner-pinned FCIS -> OpenAI Skill projection.

A provider never authors or approves the FCIS source. This command only
projects one admitted neutral SKILL.md after verifying both old adapter bytes
and the owner-reviewed neutral source digest. Anthropic is not admitted here.
"""
import argparse
import json
from pathlib import Path
import sys

from skillctl import ROOT, digest, entries

MANIFEST = Path("skills/fcis-go-publication.json")
CANONICAL = Path("skills/canonical/fcis-go")
OPENAI = Path(".codex/skills/fcis-go")
PLUGIN_ID = "Plugin_fb9e0937c59c8191b9fa077fa5ea53ef"


class AdapterProjectionError(ValueError):
    pass


def _read(root):
    path = root / MANIFEST
    if path.is_symlink() or not path.is_file():
        raise AdapterProjectionError("Owner publication manifest absent or symlinked")
    data = json.loads(path.read_text(encoding="utf-8"))
    active = data.get("activeSkill", {})
    adapter = active.get("projections", {}).get("openai", {})
    if (data.get("owner") != "Fountain-Coach/.github"
            or data.get("activePluginId") != PLUGIN_ID
            or active.get("name") != "fcis-go"
            or active.get("canonicalPath") != CANONICAL.as_posix()
            or adapter.get("path") != OPENAI.as_posix()):
        raise AdapterProjectionError("Source/adaptor identity is not owner-approved")
    neutral = entries(root / CANONICAL)
    if set(neutral) != {"SKILL.md"}:
        raise AdapterProjectionError("Unreviewed neutral FCIS source members")
    if digest(neutral) != active.get("contentSHA256"):
        raise AdapterProjectionError("Neutral FCIS source digest is not admitted")
    projected = entries(root / OPENAI)
    if "agents/openai.yaml" not in projected:
        raise AdapterProjectionError("OpenAI metadata missing")
    if digest(projected) != adapter.get("contentSHA256"):
        raise AdapterProjectionError("OpenAI adapter modified outside reviewed projection")
    return path, data, neutral, projected


def check(root=ROOT):
    root = Path(root).resolve(strict=True)
    _, data, neutral, projected = _read(root)
    if neutral["SKILL.md"] != projected["SKILL.md"]:
        raise AdapterProjectionError("OpenAI instruction drift from neutral source")
    return {"state": "MATCHED", "source": CANONICAL.as_posix(),
            "adapter": OPENAI.as_posix(), "provider": "openai",
            "contentSHA256": data["activeSkill"]["contentSHA256"],
            "pluginId": PLUGIN_ID}


def sync(root=ROOT):
    root = Path(root).resolve(strict=True)
    path, data, neutral, projected = _read(root)
    if neutral["SKILL.md"] == projected["SKILL.md"]:
        return check(root)
    output = root / OPENAI / "SKILL.md"
    if output.is_symlink():
        raise AdapterProjectionError("OpenAI instruction symlink refused")
    # Preserve the provider-owned metadata and original logo; update only
    # the projected instructions and their pinned hash in the same Git review.
    output.write_bytes(neutral["SKILL.md"])
    data["activeSkill"]["projections"]["openai"]["contentSHA256"] = digest(
        entries(root / OPENAI))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    result = check(root)
    result["state"] = "SYNCED"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "sync"))
    args = parser.parse_args()
    try:
        result = check() if args.command == "check" else sync()
    except (AdapterProjectionError, ValueError, OSError, KeyError) as exc:
        sys.exit(f"REFUSED: {exc}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
