#!/usr/bin/env python3
"""FCIS chapter 160: Git-owned deterministic skill packaging and drift observation."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "skills" / "openai-distribution.json"
SKILLS = ROOT / ".codex" / "skills"

def digest(files):
    h = hashlib.sha256()
    for name, data in sorted(files.items()):
        h.update(name.encode("utf-8") + b"\0" + str(len(data)).encode("ascii") + b"\0" + data)
    return h.hexdigest()

def entries(folder):
    if not folder.is_dir() or not (folder / "SKILL.md").is_file():
        raise ValueError("Missing skill directory or SKILL.md")
    result = {}
    for p in sorted(folder.rglob("*")):
        if p.is_symlink():
            raise ValueError("Symlinks are not valid skill payload files")
        if not p.is_file():
            continue
        rel = p.relative_to(folder).as_posix()
        if rel.startswith(".") or "/." in rel or "__pycache__" in rel or rel.endswith(".pyc"):
            raise ValueError("Hidden or generated file in package: " + rel)
        result[rel] = p.read_bytes()
    if not result:
        raise ValueError("Empty package")
    return result

def archive(files, name):
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path, data in sorted(files.items()):
            info = zipfile.ZipInfo(name + "/" + path, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return out.getvalue()

def read_archive(path, name):
    files = {}
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            parts = Path(info.filename).parts
            if not parts or parts[0] != name or len(parts) < 2 or ".." in parts:
                raise ValueError("Unsafe or unexpected ZIP member: " + info.filename)
            key = "/".join(parts[1:])
            if key in files:
                raise ValueError("Duplicate ZIP member: " + key)
            files[key] = z.read(info)
    if "SKILL.md" not in files:
        raise ValueError("ZIP missing SKILL.md")
    return files

def catalog():
    data = json.loads(CATALOG.read_text())
    if data["owner"] != "Fountain-Coach/.github":
        raise ValueError("Wrong canonical skill owner")
    names = [s["name"] for s in data["skills"]]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate skill names")
    return data

def validate():
    data = catalog()
    for item in data["skills"]:
        name = item["name"]
        files = entries(SKILLS / name)
        actual = digest(files)
        if actual != item["contentSHA256"]:
            raise ValueError(f"{name}: canonical content mismatch: {actual}")
        if item.get("canonicalPath") != ".codex/skills/" + name:
            raise ValueError(name + ": canonical path not in organization")
        if not (SKILLS / name / "agents" / "openai.yaml").is_file():
            raise ValueError(name + ": missing ChatGPT metadata")
        print("VALID", name, actual)
    return data

def compare(expected, observed):
    if observed is None:
        return "UNVERIFIED", {"reason": "No complete destination content readback"}
    if expected == observed:
        return "MATCHED", {}
    return "DRIFT", {"missing": sorted(set(expected) - set(observed)),
                     "unexpected": sorted(set(observed) - set(expected)),
                     "modified": sorted(p for p in expected.keys() & observed.keys() if expected[p] != observed[p])}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["check", "package", "compare", "report"])
    p.add_argument("--skill")
    p.add_argument("--zip")
    p.add_argument("--output")
    a = p.parse_args()
    c = validate()
    if a.command == "check":
        return
    if not a.skill or a.skill not in {i["name"] for i in c["skills"]}:
        raise ValueError("Select a declared skill with --skill")
    name = a.skill
    files = entries(SKILLS / name)
    if a.command == "package":
        if not a.output:
            raise ValueError("--output required")
        data = archive(files, name)
        Path(a.output).write_bytes(data)
        print(json.dumps({"skill": name, "fileTreeSHA256": digest(files), "zipSHA256": hashlib.sha256(data).hexdigest(), "zip": a.output}, indent=2))
        return
    if a.command == "report" and not a.zip:
        print(json.dumps({"skill": name, "status": "UNVERIFIED", "reason": "No remote readback was supplied; installation visibility alone is not content proof"}, indent=2))
        return
    if not a.zip:
        raise ValueError("--zip required")
    remote = read_archive(a.zip, name)
    state, delta = compare(files, remote)
    print(json.dumps({"skill": name, "status": state, "canonicalSHA256": digest(files),
                      "observedSHA256": digest(remote), **delta}, indent=2))
    if state != "MATCHED":
        raise SystemExit(2)

if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, zipfile.BadZipFile, KeyError) as exc:
        print("REFUSED:", exc, file=sys.stderr)
        raise SystemExit(1)
