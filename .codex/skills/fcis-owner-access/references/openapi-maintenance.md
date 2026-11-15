# Internal FCIS owner OpenAPI — maintenance protocol

**Scope:** Maintain the existing *internal, FCIS-owned* API contract, not a vendor/official upstream OpenAPI dependency or a second HTTP authority. This procedure is a reusable part of **FCIS Owner Access**, not a new FCIS-KIT capability, protocol, client, service or plugin.

## Address the actual source before editing

| Authority | Owning artifact in `Fountain-Coach/midi2-gpu-fabric` |
| --- | --- |
| HTTP routes, guards and JSON response types | `apps/estate-publisher/Sources/EstatePublisherCore/FountainHostMCPOAuth.swift` (`FountainHostMCPOAuthHandler`) |
| Machine enrollment and current grant admission | `apps/estate-publisher/Sources/EstatePublisherCore/FountainHostMachineEnrollment.swift` plus issuer FountainStore/FCIS admission |
| Owner pairing and explicit decision | `apps/estate-publisher/Sources/EstatePublisherCore/FountainHostOwnerPairing.swift` |
| Owner grant revocation evidence | `apps/estate-publisher/Sources/EstatePublisherCore/FountainHostMCPAuthorizationRevoke.swift` and the existing FountainAuthKit |
| HTTP contract | `apps/estate-publisher/contracts/fcis-owner.openapi.json` (OpenAPI 3.1; initial version 0.1.0, nine declared HTTP operations, 17 schemas) |
| Human-maintained contract release guide | `apps/estate-publisher/docs/fcis-owner-openapi.md` |
| Read-only conformance | `apps/estate-publisher/Tests/fcis-owner-openapi.test.mjs`; `Tests/EstatePublisherCoreTests/FountainHostOwnerOpenAPIContractTests.swift` and existing owner/machine handler tests |
| Consumer (not auth authority) | `Fountain-Coach/fountain-press/runtime/fcis-access-workspace.mjs` and `docs/access-owner-relationships.md` |
| Automated source guard | `Fountain-Coach/midi2-gpu-fabric/.github/workflows/ci.yaml` job `fcis-owner-openapi-contract` |

These are **ownership pointers**, not a claim about live production. At the initial 15 November 2026 source acceptance, the separate `GET /oauth/owner/hosts` route was source-tested but the public endpoint returned **404**. Re-read source SHA, deployed predecessor, current published route and owner authentication before making fresh claims.

## For each proposed API change

1. **Resolve scope and current truth.** Read the current domain `AGENTS.md`, `PLANS.md`, published Governance 07/08/142/152/160/161 and the checked-in OpenAPI guide. Identify the one operation and current source SHA; inspect Swift dispatch, actual type definitions, matching tests, current Press callers, the exact Caddy route (where deployed), and previous acceptance evidence. Decide whether the request changes contract only, Swift behavior, Access consumer, or a separately authorized release. Do not infer implemented behavior from a proposed schema.
2. **Preserve independent authorities.** FountainAuthKit owns owner authentication, OAuth grants and revocation; signed issuer/FountainStore records own machine admission; Host owns execution and terminal evidence; Press reads and operates these APIs but maintains no parallel permission or machine database. A passkey session is not a Host grant. Do not infer online/healthy/last-seen from `authorizationState=verified`, or treat `approved-pending-channel` as enrolled.
3. **Change only the corresponding route and OpenAPI entries.** Match exact path, method, operationId, security scheme, allowed `Origin`, headers, request fields, Swift `Codable` response fields, optional/omitted values, errors, `$ref` and implementation/deployment status. Maintain `x-fcis-not-admitted` as **metadata only**, never speculative paths or SDK methods. Do **not** replace distinct fleet inventory with `host.describe?inventory=1` or rewrite standards-based OAuth discovery/PKCE as a private format. Respect existing `Date` encoding: Fleet and Host observation times are ISO strings; older Swift `Date` Codable values are numeric Foundation reference-date seconds unless their actual encoder changes.
4. **Enforce the security negative cases.** `GET /oauth/owner/hosts` and owner pairing require a real owner **passkey** session; legacy Basic must not bypass that requirement. Owner pairing uses allowlisted `Origin`, exact body and `x-fountain-owner-intent` for decisions. Signed device `/oauth/host/enrollment/prove` and `/activate` prohibit browser `Origin`, `Cookie`, and `Authorization`; they do not become owner-session operations just because an error status overlaps. Host target IDs must be issuer-admitted opaque identifiers, not hostnames, IPs, or URLs. Refusals and unavailable Store evidence fail closed and must not look like successful enrollment or revocation.
5. **Version the interface.** Update `info.version` using the source guide: major for incompatible wire/auth changes, minor for admitted additive features, patch for clarifications. A proposal may be marked not-admitted without an HTTP path; addition requires the native Kit/Host authority and tests first. Keep the spec internal and free of actual owner account IDs, private IPs, tokens, machine keys and Store snapshots.
6. **Verify at both boundaries.** From the domain repository root run `node --test apps/estate-publisher/Tests/fcis-owner-openapi.test.mjs` and `git diff --check`. Run the native focused Swift suite against the **same source revision** in an isolated Ubuntu/Swift environment: `swift test --package-path apps/estate-publisher --filter 'FountainHost(OwnerOpenAPIContract|OwnerTarget|OwnerPairingHTTP|MCPAuthorizationOwnerHTTP|MachineEnrollment)Tests'`. Include both valid and refused real handler response JSON (200/201, 400/401/403/404/409, 503 as applicable); use synthetic records only when clearly labeled. Follow up with Press JS/Python and browser tests only when the consumer changed. If a test cannot run, report its exact prerequisite instead of substituting a mock acceptance result.
7. **Reconcile release as a distinct operation.** A green OpenAPI file is **source conformance only**. Before production, compare the existing signed issuer executable and exact Caddy matcher/digest and release policy. Release the issuer and URL matcher with predecessor, rollback and HTTPS readback **before** its dependent Press fleet view. Observe real owner-passkey browser access, foreign-origin/unauthenticated refusal, admitted Host identity, and independent FountainStore/Host job receipts. A browser mock, HTTP 200, successful PR or GitHub marketplace version is not production or physical-iPad acceptance.
8. **Close with provenance and source ownership.** Commit code, contract, tests and evidence on the correct domain PR; update the domain `PLANS.md` and the Press consumer's pinned contract revision when relevant. Record source SHA, contract version, tested operations and failures, CI/native result, deployed revision/receipts or `NOT_ESTABLISHED`, and next smallest unfinished gate. Do not silently merge, deploy or claim hosted Skills changed.

### Example triggers

- “We added a new host observation field; update FCIS OpenAPI and check Swift parity.”
- “The fleet endpoint now returns 401; verify the contract and passkey/CORS refusal.”
- “Prepare a backward-compatible owner grant response change and its contract tests.”
- “Verify the signed issuer/Caddy fleet release is consistent with OpenAPI.”

**Not this workflow:** An external provider's *official* schema must follow `Fountain-Coach/.github/docs/FCIS-Official-OpenAPI-Dependency.md` with a pinned upstream digest. MIDI2 IDL or generated reasoning-contract changes follow their own Kit/IDL and `generated-contract-regeneration` procedure; changing OpenAPI does not supersede them.
