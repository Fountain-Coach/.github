#!/usr/bin/env python3
"""FCIS chapter 160: Git-owned Skill integrity and read-only drift observation."""
import argparse
import hashlib
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

def validate(quiet=False):
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
        if not quiet:
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

def audit_observations(observations, source=None):
    """Read-only entrypoint comparison. Partial evidence never proves package parity."""
    source = source or {item["name"]: entries(SKILLS / item["name"]) for item in catalog()["skills"]}
    results, seen = [], set()
    for row in observations:
        if not isinstance(row, dict):
            raise ValueError("Observation must be an object")
        name, environment = row.get("skill"), row.get("environment")
        origin = row.get("origin", "unspecified")
        if name not in source or not isinstance(environment, str) or not environment.strip():
            raise ValueError("Observation requires known skill and named environment")
        if origin not in {"unspecified", "standalone-skill", "marketplace-plugin", "project-api"}:
            raise ValueError("Unsupported observed skill origin")
        identity = (environment, name, origin)
        if identity in seen:
            raise ValueError("Duplicate observation")
        seen.add(identity)
        presence = row.get("presence", "present")
        if presence == "absent":
            status = "MISSING" if row.get("inventoryComplete") is True else "UNVERIFIED"
            reason = "Complete inventory shows absent skill" if status == "MISSING" else "Inventory incomplete"
        elif presence == "present":
            observed = row.get("entrypointText")
            if not isinstance(observed, str) or not observed.strip():
                status, reason = "UNVERIFIED", "Entrypoint unavailable"
            else:
                canonical = source[name]["SKILL.md"].decode("utf-8")
                if canonical.startswith("---\n"):
                    canonical = canonical.split("\n---\n", 1)[1]
                if observed.startswith("---\n"):
                    observed = observed.split("\n---\n", 1)[1]
                if canonical.strip() == observed.strip():
                    status, reason = "UNVERIFIED", "Entrypoint matches, but complete package and selected version not verified"
                else:
                    status, reason = "DRIFT", "Installed entrypoint differs from canonical source"
        else:
            raise ValueError("Invalid presence")
        results.append({
            "skill": name, "environment": environment, "origin": origin,
            "status": status, "reason": reason,
            "canonicalSHA256": digest(source[name]),
            "effectiveVersion": "UNVERIFIED",
            "routingStatus": "UNVERIFIED",
            "routingReason": "No independently bound Skill-source execution trace",
        })
    for row in results:
        origins = sorted({other["origin"] for other in results
                          if other["environment"] == row["environment"]
                          and other["skill"] == row["skill"]})
        if len(origins) > 1:
            row["collisionOrigins"] = origins
            row["routingReason"] = (
                "Same skill name exposed by multiple installed origins; selection authority not established"
            )
    return results

def guard_standalone_installations(observations, names=None):
    """Read-only account-installed collision guard; no provider mutation."""
    names = set(names if names is not None else [i["name"] for i in catalog()["skills"]])
    if not isinstance(observations, list):
        raise ValueError("Guard observations must be an array")
    seen = {}
    environments = set()
    for item in observations:
        if not isinstance(item, dict):
            raise ValueError("Each installed-Skill witness must be an object")
        name = item.get("skill")
        environment = item.get("environment")
        if name not in names or not isinstance(environment, str) or not environment.strip():
            raise ValueError("Guard witness must select a canonical Skill and an environment")
        if item.get("origin") != "standalone-skill":
            raise ValueError("Only standalone account-Skill installations are guard targets")
        installed = item.get("installed")
        action = item.get("observedAction")
        if type(installed) is not bool or action not in {"add", "uninstall"}:
            raise ValueError("A verified account action (add/uninstall) is required")
        if (installed and action != "uninstall") or (not installed and action != "add"):
            raise ValueError("Observed account action and installed state disagree")
        key = (environment, name)
        if key in seen:
            raise ValueError("Duplicate standalone Skill observation")
        seen[key] = installed
        environments.add(environment)
    if not environments:
        raise ValueError("At least one account environment observation is required")
    results = []
    for environment in sorted(environments):
        for name in sorted(names):
            installed = seen.get((environment,name))
            state = "UNVERIFIED" if installed is None else ("CONFLICT" if installed else "CLEAR")
            results.append({
                "environment": environment,
                "skill": name,
                "state": state,
                "reason": {
                    "CONFLICT": "Standalone installation can shadow the canonical marketplace Skill",
                    "CLEAR": "Account UI offered Add, not Uninstall, for the exact standalone Skill",
                    "UNVERIFIED": "No exact account-installation action was observed",
                }[state],
            })
    return results


def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["check", "compare", "report", "audit", "guard"])
    p.add_argument("--skill")
    p.add_argument("--zip")
    p.add_argument("--observations")
    a = p.parse_args()
    c = validate(quiet=a.command in {"audit", "guard"})
    if a.command == "check":
        return
    if a.command == "audit":
        if not a.observations:
            raise ValueError("--observations required")
        observations = json.loads(Path(a.observations).read_text(encoding="utf-8"))
        if not isinstance(observations, list):
            raise ValueError("Observations must be a JSON array")
        print(json.dumps({"source": "Fountain-Coach/.github", "results": audit_observations(observations)}, indent=2))
        return
    if a.command == "guard":
        if not a.observations:
            raise ValueError("--observations required")
        observations = json.loads(Path(a.observations).read_text(encoding="utf-8"))
        results = guard_standalone_installations(observations, [i["name"] for i in c["skills"]])
        print(json.dumps({"source": "Fountain-Coach/.github",
                          "status": "CONFLICT" if any(r["state"] == "CONFLICT" for r in results)
                                  else ("UNVERIFIED" if any(r["state"] == "UNVERIFIED" for r in results)
                                        else "CLEAR"),
                          "results": results}, indent=2))
        if any(r["state"] == "CONFLICT" for r in results):
            raise SystemExit(2)
        if any(r["state"] == "UNVERIFIED" for r in results):
            raise SystemExit(3)
        return
    if not a.skill or a.skill not in {i["name"] for i in c["skills"]}:
        raise ValueError("Select a declared skill with --skill")
    name = a.skill
    files = entries(SKILLS / name)
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
