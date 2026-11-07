#!/usr/bin/env python3
"""Offline parity check for a *declared* Fountain Press agent-publication fixture.

This does not authorize publication, prove a live route or grant an agent tools.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

SOURCE_SCHEMA = "fountain.press.publication-source.v1"
AGENT_SCHEMA = "fountain.press.agent-readable-publication.v1"
GUIDE_SCHEMA = "fountain.press.agent-public-guidance.v1"
ROOT_FIELDS = ("publicationId", "editionId", "sourceOwner", "sourceRevision",
               "publicationState", "canonicalURL", "entries")
ENTRY_FIELDS = ("id", "canonicalURL", "sourceSHA256", "status")
STATES = {"draft", "staged", "published"}
ENTRY_STATES = {"current", "reference", "authored", "draft"}
POLICIES = {"public", "licensed", "restricted"}
SHA256 = re.compile(r"^[a-f0-9]{64}$")
REVISION = re.compile(r"^[a-f0-9]{40}([a-f0-9]{24})?$")
IDENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,180}$")


class InvalidPublication(ValueError):
    pass


def fail(message: str) -> None:
    raise InvalidPublication(message)


def document(path: Path) -> dict:
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"{path}: cannot read JSON: {exc}")
    if not isinstance(content, dict):
        fail(f"{path}: JSON root must be object")
    return content


def exact_keys(value: dict, required: set, label: str) -> None:
    if not isinstance(value, dict) or set(value) != required:
        fail(f"{label}: expected fields {sorted(required)}, found "
             f"{sorted(value) if isinstance(value, dict) else type(value).__name__}")


def valid_id(value, label: str) -> None:
    if not isinstance(value, str) or IDENT.fullmatch(value) is None:
        fail(f"{label}: invalid source identifier")


def valid_sha(value, label: str) -> None:
    if not isinstance(value, str) or SHA256.fullmatch(value) is None:
        fail(f"{label}: invalid SHA-256")


def https_url(value, label: str) -> str:
    if not isinstance(value, str):
        fail(f"{label}: HTTPS URL required")
    try:
        url = urlsplit(value)
        hostname = url.hostname
        port = url.port
    except ValueError:
        fail(f"{label}: malformed canonical URL")
    if (url.scheme != "https" or not hostname or url.username or url.password
            or port is not None or url.query or url.fragment
            or hostname in {"localhost", "127.0.0.1", "::1"}
            or hostname.endswith(".local") or hostname.endswith(".internal")
            or " " in value or not url.path.startswith("/")):
        fail(f"{label}: canonical source HTTPS URL required without query, fragment or private host")
    return hostname


def validate_source(source: dict, label: str) -> None:
    exact_keys(source, {"schema", *ROOT_FIELDS}, label)
    if source["schema"] != SOURCE_SCHEMA and label == "source":
        fail("source: unsupported fixture schema")
    if source["schema"] != AGENT_SCHEMA and label == "agent":
        fail("agent: unsupported fixture schema")
    for key in ("publicationId", "editionId"):
        valid_id(source[key], f"{label}.{key}")
    if not isinstance(source["sourceOwner"], str) or not re.fullmatch(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", source["sourceOwner"]):
        fail(f"{label}.sourceOwner: owner/repository identity required")
    if not isinstance(source["sourceRevision"], str) or not REVISION.fullmatch(source["sourceRevision"]):
        fail(f"{label}.sourceRevision: immutable Git revision required")
    if source["publicationState"] not in STATES:
        fail(f"{label}.publicationState: unknown state")
    host = https_url(source["canonicalURL"], f"{label}.canonicalURL")
    entries = source["entries"]
    if not isinstance(entries, list) or not entries:
        fail(f"{label}.entries: nonempty complete ordered source inventory required")
    ids = set()
    canonical = set()
    for position, item in enumerate(entries):
        exact_keys(item, set(ENTRY_FIELDS), f"{label}.entries[{position}]")
        valid_id(item["id"], f"{label}.entries[{position}].id")
        valid_sha(item["sourceSHA256"], f"{label}.entries[{position}].sourceSHA256")
        entry_host = https_url(item["canonicalURL"], f"{label}.entries[{position}].canonicalURL")
        if entry_host != host:
            fail(f"{label}.entries[{position}]: noncanonical external host")
        if item["status"] not in ENTRY_STATES:
            fail(f"{label}.entries[{position}]: undeclared status")
        if source["publicationState"] == "published" and item["status"] == "draft":
            fail(f"{label}.entries[{position}]: draft falsely presented in published edition")
        if item["id"] in ids or item["canonicalURL"] in canonical:
            fail(f"{label}.entries[{position}]: repeated source or canonical route")
        ids.add(item["id"])
        canonical.add(item["canonicalURL"])


def verify(source: dict, agent: dict, guide: dict, guide_bytes: bytes, guide_path: Path) -> dict:
    validate_source(source, "source")
    agent_base = {key: agent[key] for key in ROOT_FIELDS if key in agent}
    agent_base["schema"] = agent.get("schema")
    validate_source(agent_base, "agent")
    exact_keys(agent, {"schema", *ROOT_FIELDS, "guide"}, "agent")
    for key in ROOT_FIELDS:
        if agent[key] != source[key]:
            fail(f"source/agent parity mismatch: {key}")
    guidance = agent["guide"]
    exact_keys(guidance, {"path", "sha256"}, "agent.guide")
    path = guidance["path"]
    if (not isinstance(path, str) or not path or "\\" in path
            or PurePosixPath(path).is_absolute()
            or any(part in (".", "..") for part in path.split("/"))
            or PurePosixPath(path).name != guide_path.name):
        fail("agent.guide.path: must address the specified relative publication file")
    valid_sha(guidance["sha256"], "agent.guide.sha256")
    if hashlib.sha256(guide_bytes).hexdigest() != guidance["sha256"]:
        fail("agent.guide.sha256: public guidance bytes drifted")
    exact_keys(guide, {
        "schema", "publicationId", "editionId", "sourceOwner", "sourceRevision",
        "audience", "executionAuthority", "retrievalPolicy", "actionPolicy",
        "interpretationRules"
    }, "guide")
    if guide["schema"] != GUIDE_SCHEMA:
        fail("guide: unrecognized public guidance schema")
    for key in ("publicationId", "editionId", "sourceOwner", "sourceRevision"):
        if guide[key] != source[key]:
            fail(f"source/guide identity mismatch: {key}")
    if guide["audience"] != "external-agents":
        fail("guide.audience: not public agent-facing data")
    if guide["executionAuthority"] != "none" or guide["actionPolicy"] != "no-agent-actions":
        fail("guide: prose cannot grant executable capability")
    if guide["retrievalPolicy"] not in POLICIES:
        fail("guide.retrievalPolicy: source-declared access policy required")
    rules = guide["interpretationRules"]
    if not isinstance(rules, list) or not rules:
        fail("guide: versioned interpretation rules missing")
    ids = set()
    for i, rule in enumerate(rules):
        exact_keys(rule, {"id", "description"}, f"guide.interpretationRules[{i}]")
        valid_id(rule["id"], f"guide.interpretationRules[{i}].id")
        if rule["id"] in ids:
            fail("guide: duplicate interpretation rule")
        if not isinstance(rule["description"], str) or not rule["description"].strip():
            fail("guide: missing rule description")
        ids.add(rule["id"])
    return {
        "schema": "fountain.press.agent-publication-parity-receipt.v1",
        "status": "static-parity-pass",
        "publicationId": source["publicationId"],
        "editionId": source["editionId"],
        "sourceRevision": source["sourceRevision"],
        "entriesCompared": len(source["entries"]),
        "current": sum(e["status"] == "current" for e in source["entries"]),
        "reference": sum(e["status"] == "reference" for e in source["entries"]),
        "guideSHA256": guidance["sha256"],
        "runtimeAndPublicationAuthorityVerified": False
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Offline source/agent/public guidance parity; no publication effect")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--agent", type=Path, required=True)
    parser.add_argument("--guide", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        raw = args.guide.read_bytes()
        receipt = verify(document(args.source), document(args.agent), document(args.guide), raw, args.guide)
    except (InvalidPublication, OSError) as error:
        print(f"FAIL agent-readable publication: {error}", file=sys.stderr)
        return 1
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
