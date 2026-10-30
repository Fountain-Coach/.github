#!/usr/bin/env python3
"""Elevate independently witnessed scenario learning into one canonical FCIS Skill.

Canonical Git source changes are delegated by the writer's automatic-learning
decision. This tool neither executes scenarios nor distributes hosted Skills.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from scenario_learning import ProposalError, assess
from skillctl import ROOT, digest, entries


class ElevationError(ValueError):
    pass


def git(root, *arguments, input_bytes=None):
    proc = subprocess.run(
        ["git", "-C", str(root), *arguments],
        input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise ElevationError(
            "git " + " ".join(arguments[:2]) + ": "
            + proc.stderr.decode("utf-8", errors="replace").strip()
        )
    return proc.stdout.decode("utf-8", errors="replace").strip()


def read_json(path, label):
    if path.is_symlink() or not path.is_file():
        raise ElevationError(f"{label}: missing or symlinked evidence")
    try:
        item = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise ElevationError(f"{label}: unreadable evidence: {exc}") from exc
    if not isinstance(item, dict):
        raise ElevationError(f"{label}: object required")
    return item


def required_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ElevationError(f"{label}: required text missing")
    return value


def evidence_file(folder, name):
    file = folder / name
    if file.is_symlink() or not file.is_file() or file.stat().st_size == 0:
        raise ElevationError(f"Missing or empty independent evidence: {name}")
    return file


def verify_evidence(proposal, evidence_dir, runtime_repo):
    """Reconcile the Swift runner's separate terminal and surface artifacts."""
    folder = Path(evidence_dir).resolve(strict=True)
    if not folder.is_dir():
        raise ElevationError("Evidence directory not found")
    record = read_json(evidence_file(folder, "run-record.json"), "run-record")
    receipt = read_json(evidence_file(folder, "terminal-receipt.json"), "terminal-receipt")
    reconciliation = read_json(evidence_file(folder, "predicate-reconciliation.json"), "predicate-reconciliation")
    binding = read_json(evidence_file(folder, "binding.json"), "binding")
    window = read_json(evidence_file(folder, "window.json"), "window sidecar")
    events_file = evidence_file(folder, "run-events.jsonl")
    for name in ("ax-transcript.txt", "store-readback.txt"):
        evidence_file(folder, name)
        if not (folder / name).read_text(encoding="utf-8").strip():
            raise ElevationError(f"Independent evidence is blank: {name}")
    png = evidence_file(folder, "window.png").read_bytes()
    if len(png) < 32 or not png.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ElevationError("Window capture is not a PNG")

    scenario = _plain(proposal["scenario"]["id"])
    if not re.fullmatch(r"[a-z0-9][a-z0-9_.-]{0,127}", scenario):
        raise ElevationError("Invalid executable scenario identity")
    run_id = required_text(record.get("runID"), "runID")
    commit = required_text(record.get("sourceCommit"), "sourceCommit")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ElevationError("Run source commit is not pinned")
    if record.get("state") != "accepted" or receipt.get("state") != "accepted":
        raise ElevationError("Scenario run and terminal receipt are not accepted")
    if reconciliation.get("state") != "satisfied":
        raise ElevationError("Terminal predicate reconciliation is not satisfied")
    machine = reconciliation.get("machinePredicateCount")
    satisfied = reconciliation.get("satisfiedPredicateCount")
    if not isinstance(machine, int) or isinstance(machine, bool) or machine < 1 or satisfied != machine:
        raise ElevationError("Terminal predicates are missing or inconsistent")
    if receipt.get("declaredPredicateCount", 0) < machine:
        raise ElevationError("Terminal receipt predicate count disagrees")
    if receipt.get("contractDocumentID") != f"scenario:contract:{scenario}":
        raise ElevationError("Terminal contract identity disagrees")

    identities = ("runID", "scenario", "sourceCommit", "pid", "managedStore", "executable")
    for key in identities:
        observed = record.get(key)
        if observed in (None, "") or receipt.get(key if key != "scenario" else "scenarioID") != observed:
            raise ElevationError(f"Terminal receipt {key} does not match run")
        if binding.get(key) != observed:
            raise ElevationError(f"Independent binding {key} does not match run")
    if record["scenario"] != scenario or reconciliation.get("scenarioID") != scenario:
        raise ElevationError("Scenario identity mismatch")
    if reconciliation.get("declaredPredicateCount") != receipt["declaredPredicateCount"]:
        raise ElevationError("Declared predicates disagree")
    if not isinstance(record["pid"], int) or isinstance(record["pid"], bool) or record["pid"] < 1:
        raise ElevationError("Invalid bound process")
    window_id = window.get("windowID")
    if not isinstance(window_id, int) or window_id < 1 or window.get("pid") != record["pid"]:
        raise ElevationError("Window sidecar does not bind to scenario process")
    if binding.get("windowId") != window_id or receipt.get("independentWindowID") != window_id:
        raise ElevationError("Window witness ID disagrees")
    if not isinstance(receipt.get("receiptID"), str) or not receipt["receiptID"]:
        raise ElevationError("Missing typed terminal receipt identity")
    expected_paths = {
        "ax": folder / "ax-transcript.txt",
        "window": folder / "window.png",
        "store": folder / "store-readback.txt",
        "run": folder / "run-record.json",
    }
    refs = binding.get("evidence")
    if not isinstance(refs, dict):
        raise ElevationError("Missing independent binding references")
    for name, expected in expected_paths.items():
        value = refs.get(name)
        if not isinstance(value, str) or Path(value).resolve() != expected:
            raise ElevationError(f"Binding evidence reference for {name} disagrees")

    try:
        events = [json.loads(line) for line in events_file.read_text().splitlines() if line.strip()]
    except (OSError, ValueError) as exc:
        raise ElevationError(f"Unparseable event ledger: {exc}") from exc
    if len(events) < 3 or not all(isinstance(x, dict) and x.get("runID") == run_id for x in events):
        raise ElevationError("Event ledger identities are incomplete or inconsistent")
    if events[0].get("event") != "prepared":
        raise ElevationError("Event ledger lacks preparation")
    if not any(x.get("state") == "running" for x in events[1:-1]):
        raise ElevationError("Event ledger lacks running state")
    if events[-1].get("event") != "state" or events[-1].get("state") != "accepted":
        raise ElevationError("Final event does not confirm acceptance")
    if any(x.get("state") == "invalidated" for x in events):
        raise ElevationError("Invalidated scenario cannot teach a skill")

    declared_runs = proposal["independentProof"]["executionIDs"]
    if declared_runs and run_id not in declared_runs:
        raise ElevationError("Declared execution IDs do not include the terminal run")
    runtime_root = Path(runtime_repo).resolve(strict=True)
    if Path(git(runtime_root, "rev-parse", "--show-toplevel")).resolve() != runtime_root:
        raise ElevationError("Runtime repository root does not match")
    git(runtime_root, "cat-file", "-e", commit + "^{commit}")
    contract = proposal["scenario"]["contract"]
    if contract["repository"] != "Fountain-Coach/midi2-gpu-fabric":
        raise ElevationError("Unexpected runner scenario repository")
    pinned = git(runtime_root, "rev-parse", contract["revision"] + ":" + contract["path"])
    if pinned != contract["blobSHA"]:
        raise ElevationError("Pinned scenario contract blob differs from Git")
    # The observed execution must use the candidate's exact pinned contract bytes.
    live_blob = git(runtime_root, "rev-parse", commit + ":" + contract["path"])
    if live_blob != pinned:
        raise ElevationError("Scenario contract changed since the learning candidate was pinned")
    return {"runID": run_id, "scenario": scenario, "sourceCommit": commit,
            "terminalReceiptID": receipt["receiptID"], "windowID": window_id}


def _plain(value):
    value = required_text(value, "lesson content")
    if (len(value) > 1200 or any(c in value for c in "\n\r\0<>")
            or value.lstrip().startswith(("#", "-", "*", chr(96), "[", "{"))
            or chr(96) * 3 in value or "<!--" in value or "-->" in value):
        raise ElevationError("Lesson text must be bounded, single-line plain prose")
    return value.strip()


def lesson_markdown(candidate, scenario, identity, evidence):
    if candidate["mode"] != "revise-existing":
        raise ElevationError("Automatic learning cannot create an unadmitted skill")
    lesson = _plain(candidate["lesson"])
    trigger = _plain(candidate["trigger"])
    novelty = _plain(candidate["novelty"])
    sections = []
    for key, title in (
        ("prerequisites", "Preconditions"),
        ("steps", "Procedure"),
        ("failureBoundaries", "Stop conditions"),
        ("transferTests", "Regression checks"),
    ):
        items = candidate.get(key)
        if not isinstance(items, list) or not items:
            raise ElevationError(f"Missing learning section: {key}")
        sections.append((title, [_plain(x) for x in items]))
    lines = [
        f"<!-- FCIS-AUTO-LESSON {identity} -->",
        f"### {scenario} — verified reusable procedure",
        "",
        f"**Lesson:** {lesson}",
        f"**Trigger:** {trigger}",
        f"**Distinct from prior instructions:** {novelty}",
        f"**Scenario provenance:** {evidence['scenario']} at {evidence['sourceCommit']}; "
        f"run {evidence['runID']}; typed receipt {evidence['terminalReceiptID']}.",
        "",
    ]
    for title, items in sections:
        lines.extend([f"**{title}:**", *[f"- {item}" for item in items], ""])
    lines.extend([f"<!-- /FCIS-AUTO-LESSON {identity} -->", ""])
    return "\n".join(lines)


def insert_lesson(original, block, identity):
    start = f"<!-- FCIS-AUTO-LESSON {identity} -->"
    end = f"<!-- /FCIS-AUTO-LESSON {identity} -->"
    if original.count(start) > 1 or original.count(end) > 1:
        raise ElevationError("Corrupted duplicate learned lesson markers")
    if start in original or end in original:
        if original.count(start) != 1 or original.count(end) != 1:
            raise ElevationError("Incomplete existing learned lesson")
        old = original[original.index(start):original.index(end) + len(end)]
        return original.replace(old, block.rstrip("\n"))
    if "## Verified scenario lessons\n" not in original:
        anchor = "## Output contract\n"
        if original.count(anchor) != 1:
            raise ElevationError("Canonical skill has no unique lesson insertion point")
        original = original.replace(anchor, "## Verified scenario lessons\n\n" + anchor, 1)
    anchor = "## Output contract\n"
    return original.replace(anchor, block + "\n" + anchor, 1)


def elevate(proposal_path, evidence_dir, runtime_repo, root=ROOT):
    root = Path(root).resolve(strict=True)
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise ElevationError("Canonical repository root does not match")
    proposal = read_json(Path(proposal_path), "scenario learning candidate")
    catalog_path = root / "skills" / "openai-distribution.json"
    catalog = read_json(catalog_path, "canonical distribution catalog")
    if catalog.get("owner") != "Fountain-Coach/.github":
        raise ElevationError("Wrong canonical Skill authority")
    names = {x["name"] for x in catalog["skills"]}
    try:
        assessment = assess(proposal, declared_skills=names)
    except (ProposalError, KeyError, TypeError) as exc:
        raise ElevationError(f"Invalid scenario learning candidate: {exc}") from exc
    if proposal["candidate"]["mode"] != "revise-existing":
        raise ElevationError("Automatic elevation is restricted to an existing FCIS Skill")
    if proposal["scenario"]["contractStatus"] != "live-accepted" or proposal["scenario"]["coverageStatus"] != "live-accepted":
        raise ElevationError("Scenario status is not consistently live-accepted")
    if assessment["classification"] in ("PROPOSED_STATUS_DRIFT", "PROPOSED_SCENARIO_NOT_ACCEPTED"):
        raise ElevationError("Scenario has unaccepted or drifting coverage")
    evidence = verify_evidence(proposal, evidence_dir, runtime_repo)
    target = assessment["targetSkill"]
    target_path = root / ".codex" / "skills" / target / "SKILL.md"
    if target_path.is_symlink() or not target_path.is_file():
        raise ElevationError("Unknown canonical Skill source")
    if git(root, "status", "--porcelain", "--untracked-files=all"):
        raise ElevationError("Canonical source has unrelated uncommitted changes; refusing automatic commit")
    item = next(x for x in catalog["skills"] if x["name"] == target)
    skill_dir = target_path.parent
    if digest(entries(skill_dir)) != item["contentSHA256"]:
        raise ElevationError("Canonical Skill differs from pinned source digest")

    lesson = proposal["candidate"]
    semantic_identity = "|".join((target, evidence["scenario"], " ".join(_plain(lesson["lesson"]).casefold().split())))
    identity = hashlib.sha256(semantic_identity.encode("utf-8")).hexdigest()[:20]
    block = lesson_markdown(lesson, evidence["scenario"], identity, evidence)
    old_bytes = target_path.read_bytes()
    old_catalog = catalog_path.read_bytes()
    updated = insert_lesson(old_bytes.decode("utf-8"), block, identity)
    if updated == old_bytes.decode("utf-8"):
        return {"state": "ALREADY_LEARNED", "targetSkill": target, "lessonID": identity,
                "runID": evidence["runID"], "commit": git(root, "rev-parse", "HEAD"),
                "fileTreeSHA256": item["contentSHA256"]}
    # The only authorized mutations: one existing SKILL.md and its catalog digest.
    relative_skill = target_path.relative_to(root).as_posix()
    relative_catalog = catalog_path.relative_to(root).as_posix()
    try:
        target_path.write_text(updated, encoding="utf-8")
        item["contentSHA256"] = digest(entries(skill_dir))
        catalog_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(root / "skills" / "skillctl.py"), "check"],
            cwd=root, capture_output=True, text=True,
        )
        if result.returncode:
            raise ElevationError("Canonical skill validation failed: " + result.stderr)
        git(root, "add", "--", relative_skill, relative_catalog)
        git(root, "commit", "-m", f"skills: auto-elevate {evidence['scenario']} into {target}")
    except Exception:
        target_path.write_bytes(old_bytes)
        catalog_path.write_bytes(old_catalog)
        subprocess.run(["git", "-C", str(root), "restore", "--staged", "--",
                        relative_skill, relative_catalog], capture_output=True)
        raise
    return {"state": "ELEVATED", "targetSkill": target, "lessonID": identity,
            "runID": evidence["runID"], "commit": git(root, "rev-parse", "HEAD"),
            "fileTreeSHA256": item["contentSHA256"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--runtime-repo", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = elevate(args.candidate, args.evidence_dir, args.runtime_repo)
    except (ElevationError, OSError, KeyError, TypeError, ValueError) as exc:
        parser.exit(1, f"REFUSED: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
