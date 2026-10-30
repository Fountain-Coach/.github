#!/usr/bin/env python3
"""Read-only source validator for scenario-derived FCIS skill proposals.

This validates a proposal's declared provenance and permission boundary.
It does not read FountainStore, execute a scenario, approve a Skill, or
verify third-party evidence addresses against their owning repositories.
"""
import argparse
import json
import re
from pathlib import Path

from skillctl import catalog


class ProposalError(ValueError):
    pass


def require_string(record, key, label):
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ProposalError(f"{label}.{key}: nonempty string required")
    return value


def source(record, label):
    if not isinstance(record, dict):
        raise ProposalError(f"{label}: source object required")
    repository = require_string(record, "repository", label)
    path = require_string(record, "path", label)
    revision = require_string(record, "revision", label)
    blob_sha = require_string(record, "blobSHA", label)
    if not repository.startswith("Fountain-Coach/") or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ProposalError(f"{label}: unexpected repository")
    if path.startswith("/") or any(part in ("", ".", "..") for part in path.split("/")):
        raise ProposalError(f"{label}: unsafe path")
    if not re.fullmatch(r"[0-9a-f]{40}", revision) or not re.fullmatch(r"[0-9a-f]{40}", blob_sha):
        raise ProposalError(f"{label}: revision/blob must be a pinned SHA-1")
    return f"https://github.com/{repository}/blob/{revision}/{path}"


def strings(record, key, label, minimum):
    values = record.get(key)
    if not isinstance(values, list) or len(values) < minimum:
        raise ProposalError(f"{label}.{key}: at least {minimum} entries required")
    for index, value in enumerate(values):
        if not isinstance(value, str) or not value.strip():
            raise ProposalError(f"{label}.{key}[{index}]: nonempty string required")
    return values


def assess(proposal, declared_skills=None):
    if not isinstance(proposal, dict) or proposal.get("schemaVersion") != 1:
        raise ProposalError("Unsupported proposal schema")
    if proposal.get("state") != "PROPOSED_NOT_ADMITTED":
        raise ProposalError("Scenario learning must remain a proposal")
    proposal_id = require_string(proposal, "proposalId", "proposal")
    if not re.fullmatch(r"[a-z0-9][a-z0-9.-]{8,127}", proposal_id):
        raise ProposalError("Invalid proposal identity")
    scenario = proposal.get("scenario")
    if not isinstance(scenario, dict):
        raise ProposalError("Missing scenario identity")
    scenario_id = require_string(scenario, "id", "scenario")
    command = require_string(scenario, "command", "scenario")
    require_string(scenario, "capability", "scenario")
    contract_address = source(scenario.get("contract"), "scenario.contract")
    coverage_address = source(scenario.get("coverage"), "scenario.coverage")
    contract_status = require_string(scenario, "contractStatus", "scenario")
    coverage_status = require_string(scenario, "coverageStatus", "scenario")
    alias_commands = strings(scenario, "aliasCommands", "scenario", 1)
    if command not in alias_commands:
        raise ProposalError("The scenario command must be among its declared command spellings")

    evidence = proposal.get("evidence")
    if not isinstance(evidence, dict):
        raise ProposalError("Missing scenario witness")
    witness_address = source(evidence.get("witness"), "evidence.witness")
    if evidence.get("witnessKind") not in ("published-summary", "independent-bundle"):
        raise ProposalError("Unknown witness kind")
    strings(evidence, "observedFacts", "evidence", 1)

    skill = proposal.get("candidate")
    if not isinstance(skill, dict):
        raise ProposalError("Missing learning candidate")
    mode = require_string(skill, "mode", "candidate")
    name = require_string(skill, "targetSkill", "candidate")
    require_string(skill, "lesson", "candidate")
    require_string(skill, "trigger", "candidate")
    require_string(skill, "novelty", "candidate")
    for key, minimum in (("prerequisites", 1), ("steps", 2), ("failureBoundaries", 1), ("transferTests", 2)):
        strings(skill, key, "candidate", minimum)
    if declared_skills is None:
        declared_skills = {item["name"] for item in catalog()["skills"]}
    if mode == "revise-existing":
        if name not in declared_skills:
            raise ProposalError("Revision target is not a canonical FCIS skill")
    elif mode == "new":
        normalized_aliases = {alias.strip("/").replace(" ", "-") for alias in alias_commands}
        if name in declared_skills or name in normalized_aliases:
            raise ProposalError("Duplicate existing Skill or command alias proposed as new Skill")
    else:
        raise ProposalError("Unrecognized candidate mode")

    authority = proposal.get("authority")
    if not isinstance(authority, dict) or any(authority.get(key) is not False for key in ("admitted", "canonicalChanged", "distributed")):
        raise ProposalError("Learning proposal claims unauthorized admission or mutation")

    proof = proposal.get("independentProof")
    if not isinstance(proof, dict):
        raise ProposalError("Missing independent-proof declaration")
    event_ids = proof.get("executionIDs")
    if not isinstance(event_ids, list) or any(not isinstance(value, str) or not value for value in event_ids):
        raise ProposalError("Execution IDs must be an explicit list")
    if len(event_ids) != len(set(event_ids)):
        raise ProposalError("Reused execution identity cannot prove independent runs")
    for key in ("storeReceipt", "axTranscript", "windowCapture"):
        if proof.get(key) is not None and (not isinstance(proof[key], str) or not proof[key].strip()):
            raise ProposalError(f"Empty {key} proof reference")

    missing = [key for key in ("storeReceipt", "axTranscript", "windowCapture") if not proof.get(key)]
    if contract_status != coverage_status:
        classification = "PROPOSED_STATUS_DRIFT"
    elif contract_status != "live-accepted":
        classification = "PROPOSED_SCENARIO_NOT_ACCEPTED"
    elif missing or not event_ids:
        classification = "PROPOSED_EVIDENCE_LIMITED"
    else:
        classification = "PROPOSED_REVIEW_REQUIRED"
    return {
        "proposalId": proposal_id,
        "scenario": scenario_id,
        "targetSkill": name,
        "classification": classification,
        "missingRawEvidence": missing,
        "sourceReferences": [contract_address, coverage_address, witness_address],
        "claimBoundary": "Source metadata and declared evidence only; no live scenario, Store, AX, canonical promotion or provider effect verified",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proposal", type=Path)
    arguments = parser.parse_args()
    try:
        result = assess(json.loads(arguments.proposal.read_text()))
    except (ProposalError, OSError, json.JSONDecodeError, KeyError) as exc:
        parser.exit(1, "REFUSED: " + str(exc) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
