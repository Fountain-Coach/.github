#!/usr/bin/env python3
"""Validate prerequisite-free FCIS source specification, not Go/runtime/production.

Uses only Python's standard library and the exact committed organization files.
Every failure refuses source admission. This is NOT an executable conformance test.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYSTEM = ROOT / "FCIS-SYSTEM.json"
SCHEMA = ROOT / "FCIS-SYSTEM.schema.json"
OPENAPI = ROOT / "FCIS-OPENAPI.json"
STACK = ROOT / "FCIS-STACK.md"
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}


def reject(message: str) -> None:
    raise ValueError(message)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    obj = {}
    for k, v in pairs:
        if k in obj:
            reject(f"duplicate JSON key: {k}")
        obj[k] = v
    return obj


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if not isinstance(value, dict):
        reject(f"expected JSON object in {path.name}")
    return value


def blob_sha(path: Path) -> str:
    content = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\x00" + content).hexdigest()


def schema_validate(value: object, rules: dict, schema: dict, at: str = "$") -> None:
    if "$ref" in rules:
        ref = rules["$ref"]
        if not ref.startswith("#/$defs/"):
            reject(f"{at}: unknown schema reference {ref!r}")
        name = ref[len("#/$defs/"):]
        if name not in schema["$defs"]:
            reject(f"{at}: undefined schema reference {ref!r}")
        return schema_validate(value, schema["$defs"][name], schema, at)
    types = {
        "object": lambda x: isinstance(x, dict),
        "array": lambda x: isinstance(x, list),
        "string": lambda x: isinstance(x, str),
        "integer": lambda x: isinstance(x, int) and not isinstance(x, bool),
        "boolean": lambda x: isinstance(x, bool),
    }
    if "type" in rules and not types[rules["type"]](value):
        reject(f"{at}: expected {rules['type']}")
    if "const" in rules and value != rules["const"]:
        reject(f"{at}: expected fixed value {rules['const']!r}")
    if "enum" in rules and value not in rules["enum"]:
        reject(f"{at}: value not admitted by schema")
    if isinstance(value, str):
        if len(value) < rules.get("minLength", 0):
            reject(f"{at}: string is too short")
        if "pattern" in rules and not re.search(rules["pattern"], value):
            reject(f"{at}: pattern mismatch")
    if isinstance(value, int) and not isinstance(value, bool) and "minimum" in rules:
        if value < rules["minimum"]:
            reject(f"{at}: integer below minimum")
    if isinstance(value, dict):
        missing = set(rules.get("required", [])) - value.keys()
        if missing:
            reject(f"{at}: missing fields {sorted(missing)}")
        if len(value) < rules.get("minProperties", 0):
            reject(f"{at}: too few properties")
        props = rules.get("properties", {})
        for name, item in value.items():
            if name in props:
                schema_validate(item, props[name], schema, at + "." + name)
            elif isinstance(rules.get("additionalProperties"), dict):
                schema_validate(item, rules["additionalProperties"], schema, at + "." + name)
            elif rules.get("additionalProperties") is False:
                reject(f"{at}: unexpected property {name}")
    if isinstance(value, list):
        if len(value) < rules.get("minItems", 0) or len(value) > rules.get("maxItems", float("inf")):
            reject(f"{at}: array bounds violated")
        if rules.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            reject(f"{at}: duplicate array item")
        if "items" in rules:
            for index, item in enumerate(value):
                schema_validate(item, rules["items"], schema, at + f"[{index}]")


def operation_index(api: dict) -> dict[tuple[str, str], dict]:
    idx = {}
    ids = set()
    for path, methods in api["paths"].items():
        for method, operation in methods.items():
            if method not in HTTP_METHODS:
                continue
            opid = operation["operationId"]
            if opid in ids:
                reject(f"OpenAPI duplicate operationId {opid}")
            ids.add(opid)
            idx[(method.upper(), path)] = operation
    return idx


def check(system: dict, api: dict) -> None:
    if system["sourcePinPolicy"]["httpContractVersion"] != api["info"]["version"]:
        reject("source-pin contract version differs from canonical HTTP API")
    if system["apis"]["fcis"]["version"] != api["info"]["version"]:
        reject("system HTTP API version differs from canonical HTTP API")
    if system["sourcePinPolicy"]["apiBlobSha"] != blob_sha(OPENAPI):
        reject("canonical FCIS OpenAPI Git blob checksum mismatch")
    if system["sourcePinPolicy"]["stackBlobSha"] != blob_sha(STACK):
        reject("FCIS-STACK.md Git blob checksum mismatch")
    for name, local in [("org", STACK), ("fcisHTTP", OPENAPI)]:
        if system["specificationSources"][name]["blobSha"] != blob_sha(local):
            reject(f"pinned specification blob mismatches {name}")
    if "FCIS-SYSTEM.json" not in STACK.read_text(encoding="utf-8"):
        reject("architecture is not linked to the canonical whole-system object")
    if "Voraussetzungslos" not in STACK.read_text(encoding="utf-8"):
        reject("the standalone architecture is not prerequisite-free")
    api_ops = operation_index(api)
    sys_ops = system["apis"]["fcis"]["operations"]
    if len(api_ops) != len(sys_ops):
        reject("HTTP operation count drift")
    seen = set()
    for row in sys_ops:
        method, path = row["method"], row["path"]
        key = (method, path)
        if key in seen or key not in api_ops:
            reject(f"missing or duplicate system HTTP operation {key}")
        seen.add(key)
        canonical = api_ops[key]
        pointer = "/paths/" + path.replace("~", "~0").replace("/", "~1") + "/" + method.lower()
        if row["id"] != canonical["operationId"] or row["security"] != canonical.get("security", "inherit-source") or row["sourcePointer"] != pointer:
            reject(f"canonical HTTP operation drift: {method} {path}")
    if system["apis"]["fcis"]["schemas"] != list(api["components"]["schemas"]):
        reject("HTTP schema inventory drift")
    if system["apis"]["fcis"]["securitySchemes"] != list(api["components"]["securitySchemes"]):
        reject("HTTP security scheme inventory drift")
    for k, label in [("fcis", "fcisHTTP"), ("fountainstore", "fountainStoreHTTP"), ("secretstore", "secretStoreHTTP")]:
        if len(system["apis"][k]["operations"]) != system["coverageBaseline"][label]:
            reject(f"{k} operation count != coverage baseline")
    for id, source in system["specificationSources"].items():
        if not re.fullmatch("[0-9a-f]{40}", source["ref"]) or not re.fullmatch("[0-9a-f]{40}", source["blobSha"]):
            reject(f"mutable source revision or invalid blob for {id}")
    for asset in system["frontend"]["assets"]:
        if asset not in system["specificationSources"]:
            reject(f"unmapped frontend source {asset}")
    if system["initialization"]["externalDependenciesForFirstStart"]:
        reject("fresh install depends on an existing FCIS system")
    if system["migration"]["requiredForFreshInstall"]:
        reject("existing migration is incorrectly mandatory")
    if system["initialization"]["initialState"]["phase"] != "UNCLAIMED":
        reject("fresh install is not unclaimed")
    if system["knownSpecificationLimitations"]:
        reject("whole-system specification contains acknowledged unresolved gaps")
    for name in ("enroll/options", "enroll/verify"):
        op = api["paths"]["/oauth/owner/passkeys/" + name]["post"]
        required_security = [{"firstOwnerSetup": []}, {"ownerPasskeySession": []}]
        if op["security"] != required_security:
            reject(f"first-owner bootstrap not independently specified in {name}")
    attestation = api["paths"]["/oauth/owner/passkeys/enroll/verify"]["post"]["requestBody"]["content"]["application/json"]["schema"]
    if attestation != {"$ref": "#/components/schemas/FirstOwnerPasskeyAttestation"}:
        reject("WebAuthn registration must not use login assertion body")
    required_ids = set()
    for i, _ in enumerate(system["coverageBaseline"]["domains"]):
        required_ids.add(f"FCIS-DOMAIN-{i+1:02d}")
    for row in sys_ops:
        required_ids.add("HTTP-" + row["id"])
    for key, prefix in (("fountainstore", "STOREHTTP-"), ("secretstore", "CUSTODYHTTP-")):
        for op in system["apis"][key]["operations"]:
            required_ids.add(prefix + op["id"])
    for asset in system["frontend"]["assets"]:
        required_ids.add("UI-ASSET-" + asset)
    for transform in system["frontend"]["sourceBindingReconciliation"]["requiredTransformations"]:
        required_ids.add(transform["id"])
    for command in system["initialization"]["requiredCommands"]:
        required_ids.add("CLI-" + re.sub(r"\W+", "-", command["name"]))
    catalog = system["generation"]["requirementCatalog"]
    ids = [row["id"] for row in catalog]
    if len(ids) != len(set(ids)) or set(ids) != required_ids:
        reject(f"coverage catalog mismatch: missing {sorted(required_ids-set(ids))}, unexpected {sorted(set(ids)-required_ids)}")
    if len(catalog) != system["generation"]["requirementGate"]["expectedRequirementCount"]:
        reject("generation coverage denominator mismatch")
    if system["generation"]["requirementGate"]["testsAllowedOnlyAfterGeneration"] is not True:
        reject("code generation and runtime tests are not separated")
    if system["designPrinciple"]["defaultProfile"] != "fresh-install":
        reject("default mode must be standalone, not migration")
    print(f"FCIS SPEC SOURCE PASS: schema, {len(sys_ops)} FCIS HTTP operations, "
          f"{len(catalog)} mandatory requirements, {len(system['specificationSources'])} pinned sources")
    print(f"  SYSTEM SHA-256 {hashlib.sha256(SYSTEM.read_bytes()).hexdigest()}")
    print(f"  OPENAPI SHA-256 {hashlib.sha256(OPENAPI.read_bytes()).hexdigest()}")
    print("  SOURCE ONLY: no Go generation, runtime tests, grants, deployment or production claim")


def main() -> int:
    schema = load(SCHEMA)
    system = load(SYSTEM)
    api = load(OPENAPI)
    schema_validate(system, schema, schema)
    check(system, api)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        print("FCIS SPEC REFUSED:", error, file=sys.stderr)
        sys.exit(1)
