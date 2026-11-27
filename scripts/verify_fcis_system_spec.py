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



def _slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", str(value)).strip("-").upper()


def _escape_pointer(value: str) -> str:
    return str(value).replace("~", "~0").replace("/", "~1")


def pointer_value(system: dict, pointer: str) -> object:
    if not pointer.startswith("/"):
        reject(f"invalid source pointer {pointer}")
    value = system
    for piece in pointer[1:].split("/"):
        key = piece.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict):
            if key not in value:
                reject(f"missing atomic source target: {pointer}")
            value = value[key]
        elif isinstance(value, list):
            if not key.isdigit() or int(key) >= len(value):
                reject(f"atomic source index invalid: {pointer}")
            value = value[int(key)]
        else:
            reject(f"atomic source pointer traverses a primitive: {pointer}")
    return value


def expected_atomic(system: dict) -> dict[str, dict[str, str]]:
    """Derive every subordinate requirement from actual contract fields and steps.

    A published catalog entry cannot manufacture an ungrounded pointer or drop
    a state/field while claiming the old denominator. Neither this function
    nor the catalog proves implementation; generation needs its own gate.
    """
    expected = {}

    def record(ident: str, pointer: str, cls: str, name: str) -> None:
        if ident in expected:
            reject(f"duplicate derived atomic requirement {ident}")
        pointer_value(system, pointer)
        expected[ident] = {
            "sourcePointer": pointer, "proofClass": cls, "name": name,
        }

    def array(stem: str, pointer: str, ident, label, cls: str) -> None:
        values = pointer_value(system, pointer)
        if not isinstance(values, list):
            reject(f"{pointer} must be an array for atomic coverage")
        for index, value in enumerate(values):
            record(stem + ident(value, index), f"{pointer}/{index}",
                   cls, label(value, index))

    def fields(stem: str, pointer: str, cls: str) -> None:
        value = pointer_value(system, pointer)
        if not isinstance(value, dict):
            reject(f"{pointer} must be an object for atomic coverage")
        for field in value:
            record(stem + _slug(field), f"{pointer}/{_escape_pointer(field)}",
                   cls, f"{cls}: {field}")

    two = lambda x, i: f"{i+1:02d}"
    array("INIT-TRANSITION-", "/initialization/stateMachine",
          two, lambda x, i: f"{x['state']} / {x['action']} -> {x['next']}", "state-machine")
    array("ADMISSION-TRANSITION-", "/capabilitySystem/admissionStateMachine",
          two, lambda x, i: f"{x['from']} / {x['event']} -> {x['to']}", "state-machine")
    array("VAULT-OP-", "/secretStoreFormat/operations",
          lambda x, i: _slug(x["id"]), lambda x, i: f"SecretStore operation {x['id']}", "custody-operation")
    array("SKILL-STATE-", "/skillAndScenarioSystem/lifecycle",
          lambda x, i: _slug(x), lambda x, i: f"Skill lifecycle: {x}", "skill-lifecycle")
    array("PRINCIPAL-", "/ownerAndTenancy/principalTypes",
          lambda x, i: _slug(x), lambda x, i: f"Authorization principal: {x}", "principal-type")
    array("COLLECTION-", "/persistence/logicalCollections",
          lambda x, i: _slug(x), lambda x, i: f"FountainStore collection {x}", "store-schema")
    array("MCP-METHOD-", "/capabilitySystem/mcp/methods",
          lambda x, i: _slug(x), lambda x, i: f"MCP method {x}", "mcp-transport")
    array("HOST-CONTROL-", "/capabilitySystem/hostTransport/control/required",
          lambda x, i: _slug(x), lambda x, i: f"Host signed request field {x}", "host-wire")
    array("HOST-RECEIPT-", "/capabilitySystem/hostTransport/receipts/required",
          lambda x, i: _slug(x), lambda x, i: f"Host terminal receipt field {x}", "host-receipt")
    array("STORE-WAL-", "/persistentStoreFormat/wal/frame/layout",
          two, lambda x, i: f"WAL physical field {x}", "store-wire")
    array("VAULT-AAD-", "/secretStoreFormat/envelope/aad",
          lambda x, i: _slug(x), lambda x, i: f"Vault authenticated data field {x}", "custody-wire")
    array("UI-TAB-", "/frontend/tabs",
          lambda x, i: _slug(x), lambda x, i: f"Frontend tab {x}", "frontend-bind")
    array("ADOPT-STEP-", "/migration/steps",
          two, lambda x, i: f"Optional migration operation {x}", "adoption")
    array("OUTPUT-", "/generation/requiredArtifacts",
          two, lambda x, i: f"Generated deliverable {x}", "generation")
    fields("SKILL-DISTRIBUTION-", "/skillAndScenarioSystem/distribution", "skill-distribution")
    fields("OWNER-POLICY-", "/ownerAndTenancy", "owner-policy")
    fields("BOOTSTRAP-", "/initialization/setupTicket", "bootstrap")
    for field, stem, cls in (
        ("stages", "LEARN-STAGE-", "learning-stage"),
        ("evidence", "LEARN-EVIDENCE-", "learning-evidence"),
        ("refusals", "LEARN-REFUSAL-", "learning-refusal"),
        ("continuousBehavior", "LEARN-CYCLE-", "learning-cycle"),
    ):
        array(stem, "/skillAndScenarioSystem/learningAcceptance/" + field,
              lambda x, i: _slug(x["id"]), lambda x, i: f"{cls}: {x['id']}", cls)
    for field, stem, cls in (
        ("requirements", "CHAT-REQ-", "chat-requirement"),
        ("refusals", "CHAT-REFUSAL-", "chat-refusal"),
    ):
        array(stem, "/reasoningAndConversationSystem/" + field,
              lambda x, i: _slug(x["id"]), lambda x, i: f"{cls}: {x['id']}", cls)
    return expected


def check_atomic_coverage(system: dict, base_ids: set[str]) -> int:
    derived = expected_atomic(system)
    catalog = system["generation"]["requirementCatalog"]
    ids = [row["id"] for row in catalog]
    required_ids = base_ids | set(derived)
    if len(ids) != len(set(ids)) or set(ids) != required_ids:
        reject("coverage catalog mismatch: missing "
               f"{sorted(required_ids - set(ids))}, unexpected {sorted(set(ids) - required_ids)}")
    for row in catalog:
        ident = row["id"]
        if ident in derived:
            for field, expected in derived[ident].items():
                if row.get(field) != expected:
                    reject(f"atomic {ident} {field} drift: {row.get(field)!r}")
        if row.get("mandatory") is not True:
            reject(f"non-mandatory requirement {ident}")
    groups = {}
    for row in derived.values():
        cls = row["proofClass"]
        groups[cls] = groups.get(cls, 0) + 1
    actual = system["coverageBaseline"].get("atomicRequirementGroups")
    if actual != groups:
        reject(f"atomic coverage group mismatch: {actual} != {groups}")
    count = len(catalog)
    if count < 222:
        reject(f"atomic coverage floor lost: {count} < 222")
    for path, recorded in [
        ("coverageBaseline.atomicRequirementCount",
         system["coverageBaseline"].get("atomicRequirementCount")),
        ("generation.requirementGate.expectedRequirementCount",
         system["generation"]["requirementGate"].get("expectedRequirementCount")),
        ("generation.requirementGate.minimumAtomicRequirementCount",
         system["generation"]["requirementGate"].get("minimumAtomicRequirementCount"))
    ]:
        if recorded != count:
            reject(f"{path} differs from derived atomic total {count}")
    classes = system["generation"]["requirementGate"].get("atomicCoverageClasses")
    if set(classes or []) != set(groups) or len(classes) != len(groups):
        reject("atomic coverage class inventory drift")
    receipt = system["generation"]["requirementGate"]["generatorReceipt"]
    if receipt.get("initialStatus") != "INCOMPLETE":
        reject("generation may not start COMPLETE")
    if set(receipt.get("requiredMappingFields", [])) != {
        "requirementID", "sourcePath", "symbol", "sourceSHA256",
        "implementationKind", "refusalPath", "terminalProofWhereApplicable"
    }:
        reject("independent generation coverage receipt is not source-and-refusal bound")
    if "INCOMPLETE" not in receipt.get("resumption", ""):
        reject("generation resumption does not fail closed")
    return count


def check_learning_acceptance(system: dict, api: dict) -> None:
    """Require the learning cycle and its exact existing operation bindings."""
    lesson = system["skillAndScenarioSystem"]["learningAcceptance"]
    if lesson["scenarioId"] != "FCIS-LEARN-01" or lesson["status"] != "SPECIFIED_ONLY":
        reject("learning contract identity or premature acceptance")
    required = {
        "stages": ["baseline", "proposal", "scenario-review", "signed-admission",
                   "fresh-consumption", "independent-improvement"],
        "evidence": ["baseline-run", "learned-draft", "release-chain", "consumption", "next-run"],
        "refusals": ["invalid-evidence", "invalid-promotion", "invalid-consumption",
                     "invalid-improvement", "privacy-or-scope"],
        "continuousBehavior": ['episode-closure', 'default-assessment', 'domain-independence', 'polyphonic-reflection', 'durable-disposition', 'proposal-before-promotion', 'next-attempt-consumption', 'general-acceptance'],
    }
    for field, identities in required.items():
        if [x["id"] for x in lesson[field]] != identities:
            reject(f"learning {field} coverage/order drift")
    operations = ["readOwnerSkill", "readOwnerSkillRelease", "createOwnerSkillDraft",
                  "readOwnerSkillDraft", "reviewOwnerSkillDraft", "admitOwnerSkillRelease"]
    extension = api["x-fcis-learning-acceptance"]
    if (lesson["operationIds"] != operations or extension["operationIds"] != operations
            or extension["scenarioId"] != lesson["scenarioId"]
            or extension["canonicalContract"] != "FCIS-SYSTEM.json#/skillAndScenarioSystem/learningAcceptance"
            or extension["reviewEvidenceKind"] != "scenario-verified"
            or extension["status"] != "specified-only-not-deployed"):
        reject("learning OpenAPI binding or source-only state drift")
    by_id = {op["operationId"]: op for op in operation_index(api).values()}
    for operation in operations:
        if operation not in by_id or by_id[operation].get("security") != [{"ownerPasskeySession": []}]:
            reject(f"learning operation authorization drift: {operation}")
    review = api["components"]["schemas"]["SkillDraftReview"]
    if "scenario-verified" not in review["properties"]["evidenceKind"]["enum"]:
        reject("learning scenario evidence review missing")
    if not any("FCIS-LEARN-01" in x for x in system["acceptance"]["postGenerationTesting"]):
        reject("learning live acceptance omitted from product testing")


def check_owner_chat(system: dict, api: dict) -> None:
    chat = system["reasoningAndConversationSystem"]
    ext = api["x-fcis-owner-chat"]
    policy = chat["policy"]
    if (chat["scenarioId"] != "FCIS-CHAT-01" or chat["status"] != "SPECIFIED_ONLY"
            or ext["status"] != "specified-only-not-deployed"):
        reject("owner chat premature acceptance")
    if (policy["additionalInferenceChargeCeilingMinor"] != 0
            or policy["permittedExternalChargeBasis"] != "included-subscription"
            or policy["noPaidFallback"] is not True
            or any(policy[k] is not False for k in ("workspaceCreditsAllowed",
                   "automaticRechargeAllowed", "ownerBillingMutationAllowed"))
            or policy["unknownEntitlement"] != "refuse-before-transmission"
            or ext["additionalInferenceChargeCeilingMinor"] != 0
            or ext["permittedExternalChargeBasis"] != "included-subscription"
            or ext["noFallback"] is not True):
        reject("subscription-only reasoning policy drift")
    required_collections = ["fcis.conversations", "fcis.messages", "fcis.reasoning-turns"]
    if ([x["id"] for x in chat["collections"]] != required_collections
            or any(x not in system["persistence"]["logicalCollections"] for x in required_collections)
            or list(system["persistence"]["conversationCollections"]) != required_collections):
        reject("owner conversation custody drift")
    required = {
        "requirements": ["owner-history", "subscription-only", "external-mcp",
            "native-adapter", "selection-and-consent", "durable-turn",
            "cross-provider-continuity", "instrument-evidence", "privacy-deletion",
            "owner-ux", "publication-boundary", "domain-composition",
            "domain-grounding", "domain-situation", "domain-context-binding"],
        "refusals": ["unknown-or-extra-charge", "unauthorized-context",
            "conflicting-turn", "private-disclosure", "false-history-or-learning",
            "stale-domain-context"],
    }
    for field, ids in required.items():
        if [x["id"] for x in chat[field]] != ids:
            reject(f"owner chat {field} coverage/order drift")
    operations = ["listOwnerReasoningClients", "listOwnerConversations", "createOwnerConversation",
        "readOwnerConversation", "updateOwnerConversation", "deleteOwnerConversation",
        "listOwnerConversationMessages", "appendOwnerMessage", "startOwnerReasoningTurn",
        "readOwnerReasoningTurn", "cancelOwnerReasoningTurn",
        "readOwnerVoiceComposition", "arrangeOwnerVoices", "decideOwnerVoiceAdmission"]
    if (chat["operationIds"] != operations or ext["operationIds"] != operations
            or ext["canonicalContract"] != "FCIS-SYSTEM.json#/reasoningAndConversationSystem"):
        reject("owner chat operation binding drift")
    by_id = {op["operationId"]: (method, op) for (method, _), op in operation_index(api).items()}
    for name in operations:
        if name not in by_id:
            reject("owner chat operation missing: " + name)
        method, op = by_id[name]
        if op.get("security") != [{"ownerPasskeySession": []}]:
            reject("owner chat operation authorization drift: " + name)
        if op.get("x-fcis-go-target-state") != "specified-only-not-deployed":
            reject("owner chat operation premature acceptance")
        for response in op["responses"].values():
            if response["headers"]["Cache-Control"]["schema"]["const"] != "no-store":
                reject("owner chat private caching drift")
        if method != "GET":
            headers = {p["name"]: p for p in op["parameters"] if p["in"] == "header"}
            if (not headers["Origin"]["required"] or not headers["X-Fountain-Owner-Intent"]["required"]
                    or headers["X-Fountain-Owner-Intent"]["schema"]["const"] != op["x-fcis-owner-intent"]):
                reject("owner chat mutation intent drift")
    start = api["components"]["schemas"]["OwnerReasoningTurnCreate"]
    for name, value in (("subscriptionOnly", True), ("additionalInferenceChargeCeilingMinor", 0),
                        ("disclosureConsent", True)):
        if name not in start["required"] or start["properties"][name]["const"] != value:
            reject("owner chat send boundary drift: " + name)
    if not {"contextMessageIds", "skillReleaseIds"}.issubset(start["required"]):
        reject("owner chat exact context binding drift")
    check_situated_context(system, api)
    if not any("FCIS-CHAT-01" in x for x in system["acceptance"]["postGenerationTesting"]):
        reject("owner chat acceptance omitted")



def check_situated_context(system: dict, api: dict) -> None:
    schemas = api["components"]["schemas"]
    start = schemas["OwnerReasoningTurnCreate"]
    turn = schemas["OwnerReasoningTurn"]
    binding = schemas["OwnerDomainContextBinding"]
    context = schemas["OwnerSituatedContext"]
    ref = schemas["OwnerDomainResourceRef"]
    sha = {"type": "string", "pattern": "^[0-9a-f]{64}$"}
    if ("situatedContext" in start["required"]
            or start["properties"].get("situatedContext") != {"$ref": "#/components/schemas/OwnerSituatedContext"}
            or "domainContextBinding" in turn["required"]
            or turn["properties"].get("domainContextBinding") != {"$ref": "#/components/schemas/OwnerDomainContextBinding"}):
        reject("situated context must be optional on existing turn contract")
    if (set(context["required"]) != {"domain", "grounding", "situation", "expectedContextSHA256"}
            or context["properties"]["expectedContextSHA256"].get("pattern") != sha["pattern"]
            or set(ref["required"]) != {"id", "revision", "sourceSHA256"}
            or ref["properties"]["sourceSHA256"] != sha
            or any(x.get("additionalProperties") is not False for x in (binding, context, ref))):
        reject("situated exact source and consent binding drift")
    situation = context["properties"]["situation"]
    if (set(situation["required"]) != {"arrangementId", "wiringState", "selectedObjects"}
            or situation.get("additionalProperties") is not False
            or set(situation["properties"]["wiringState"]["enum"]) != {"not-applicable", "unwired", "wired"}):
        reject("situated empty and unwired context drift")
    if (set(binding["required"]) != {"domain", "grounding", "contextSHA256"}
            or set(binding["properties"]) != set(binding["required"])
            or binding["properties"]["contextSHA256"].get("pattern") != sha["pattern"]
            or "situatedContext" in turn["properties"]):
        reject("Situation must not persist as a turn artifact")
    refusal = {"domain_unavailable", "grounding_unconfirmed", "situation_stale", "context_conflict"}
    if (not refusal.issubset(schemas["OwnerConversationError"]["properties"]["error"]["enum"])
            or not refusal.issubset(turn["properties"]["reason"]["anyOf"][0]["enum"])):
        reject("situated refusal coverage drift")
    ext = api["x-fcis-owner-chat"]["situatedReasoning"]
    if (ext["newOperations"] != [] or ext["status"] != "specified-only-not-deployed"
            or ext["canonicalContract"] != "FCIS-SYSTEM.json#/reasoningAndConversationSystem"
            or not any("situated Reframe" in x for x in system["acceptance"]["postGenerationTesting"])):
        reject("situated scope or acceptance drift")

def check(system: dict, api: dict) -> None:
    check_learning_acceptance(system, api)
    check_owner_chat(system, api)
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
    count = check_atomic_coverage(system, required_ids)
    catalog = system["generation"]["requirementCatalog"]
    if system["generation"]["requirementGate"]["testsAllowedOnlyAfterGeneration"] is not True:
        reject("code generation and runtime tests are not separated")
    if system["designPrinciple"]["defaultProfile"] != "fresh-install":
        reject("default mode must be standalone, not migration")
    print(f"FCIS SPEC SOURCE PASS: schema, {len(sys_ops)} FCIS HTTP operations, "
          f"{count} mandatory requirements, {len(system['specificationSources'])} pinned sources")
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
