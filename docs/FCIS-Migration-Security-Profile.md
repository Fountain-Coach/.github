# FCIS Migration Security Profile — Hetzner-Initiated Store and SecretStore Continuity

**Owner decision:** 19 November 2026
**Authority:** `Fountain-Coach/.github`, subordinate to the peer canonical [FCIS stack](../FCIS-STACK.md) and [FCIS HTTP OpenAPI](../FCIS-OPENAPI.json); FountainStore's engine/format and the host's secret provider keep their separate source owners.
**Status:** Binding target contract; **not evidence that the transfer or production cutover ran**.
**Execution origin:** The **existing headless Hetzner server**, through its admitted service and operator authority.
**Destination:** A standalone Go FCIS service and dedicated Go-native FountainStore instance on Hetzner, retaining the existing `https://fcis.fountain.coach/` issuer.

## Owner-selected invariant

**Replacing the storage/runtime implementation MUST NOT change the identity of the owner, trusted authenticators, machine identities, effective grants, revoked permissions, issuer identity, or the authorized custody of service secrets.**

The existing Hetzner host **initiates, coordinates, journals, verifies and, when authorized, activates** the transition from old FountainStore + SecretStore to the new FCIS Store + protected secret custody. The server is the workhorse; **no MacBook, Mac mini, arbitrary operator workstation, local Keychain prompt, local SSH login or new enrollment UX is a prerequisite**. A legitimate approval can be requested using the **already deployed Golden Key experience** on any currently eligible enrolled device. Do not equate successful WebAuthn login with the separate owner-root signature unless the deployed authority explicitly establishes that delegation.

This decision **supersedes** the 18 November specification's permission to bootstrap a *new owner* or omit historical grant continuity. A new private *physical Store instance* is acceptable; a newly invented owner identity or independently authoritative grant database is not.

## Authorities to inspect and preserve

| Source authority | What must remain identical/effective |
| --- | --- |
| Owner trust | Stable principal/subject, trust-set public fingerprint, owner-signed authority and rotation/revocation records. A label such as `owner-primary` is not identity proof. |
| WebAuthn | Existing RP ID, user handle, credential IDs, public keys, signature-counter and backup metadata where applicable, active/revoked status. No authenticator private-key export or default re-registration. |
| OAuth | Public issuer and metadata identity, clients, redirect and resource registrations, consent/grants, scope and audience, expiry, refresh-family rotation state and revocations. Reauthorization is required only for nontransferable/invalid records and does not silently recreate a grant. |
| Machine/Host | Enrolled device and service identities, signed admissions, capability scopes/versions, revocations, lease limits and resource bindings. Enrollment does not imply a grant to every Host operation. |
| FountainStore | Single-writer mutation ordering, snapshots/WAL checkpoint, audit/event lineage and terminal evidence in the source-owned format. |
| SecretStore | Retain existing protected Hetzner-side key custody, opaque secret references and service credentials; preserve authority through admitted adapters and verifiable key operations. |

**Never** infer ownership from SSH root access, a valid-looking copied row, the name `owner-primary`, or a newly generated key. A private key in Keychain or SecretStore may be non-exportable; when it is, leave it in its original custodian and route use only via existing authorized short-lived operations.

## Headless transfer sequence

1. **Discover on Hetzner, read-only.** Identify actual authoritative old/new Store roots, source/writer processes, SecretStore backend/custody, issuer, trust-set and public-key fingerprints, active and revoked identities/grants, current Caddy mapping and Go source/release identity. Record observed versus documented facts. Merely receiving `host.describe` does not establish Store access.
2. **Authenticate the exact operation.** Use the existing Hetzner operator/Host contract and current owner policy. If human consent is required, invoke existing Golden Key on an eligible enrolled device; no new UX or fixed workstation dependency. A missing owner-root signer is a typed refusal, not permission to generate a substitute.
3. **Fence and back up source.** Arrange a consistent source snapshot/WAL watermark with a single writer or equivalent transactional barrier. Preserve verified encrypted immutable backups of both Store and SecretStore (including recovery requirements). Prove isolated restore/readback before modifying the destination; never delete the predecessor during migration.
4. **Import logical Store authority.** Transfer owner subject, WebAuthn public metadata, OAuth clients/grants/revocations, token-family state, signed Hosts/admissions, audit events and required terminal receipts through source-owned typed version adapters. Verify identities, signatures, issuer, scope, expiry, replay state and provenance before activation. Treat unsupported/unverifiable records as **quarantined and inactive**, with counts and reason codes, rather than forging equivalent grants.
5. **Keep secret custody server-side.** Prefer reusing existing Hetzner SecretStore and references from the Go host adapter. If a provider/backend change is actually required, use only an owner-authorized, host-internal encrypted channel and a provider-supported export/import operation; verify public-key equivalence by controlled signing challenge, and preserve independent recovery. No secret values in ordinary FountainStore, Git, chat, model prompts, MCP, MIDI2, browser state, logs or receipts.
6. **Verify Go before switching public routing.** Compare stable IDs, public-key fingerprints, trust-set digest, grant/revoke parity, watermark, expiration and signed Host state. Test negative cases: revoked/expired/forged grants, refresh replay, wrong issuer/RP ID/host/scope/audience, counter rollback, duplicate IDs and tampered ciphertext. Verify passkey login, scoped OAuth, one admitted MCP/Host operation, crash/restart and independent Store receipt.
7. **Cut over with one authority.** Pin Go artifact and configuration digest, preserve the source writer fenced, then use existing owner-authorized Caddy/service promotion to retain public `fcis.fountain.coach` and serve OAuth **and** MCP from Go alone. Independently inspect issuer metadata, JWKS, TLS, MCP handshake, owner session, Host call and durable revocation readback.
8. **Reconcile rollback.** Any authorization mutation after cutover, especially revocation or rotation, must survive rollback. If the predecessor cannot be reconciled to the effective security state, do not re-enable it for writes. Fail closed and use existing controlled reauthorization instead of resurrecting revoked permission.

## Finite Definition of Done

- Exact source/destination Store IDs, paths, service/custody owners, issuer, trust-set public fingerprint and Go release digest identified from **Hetzner readback**.
- Encrypted and independently restored source backups; verified complete Store snapshot/watermark; original Store and SecretStore left intact.
- Owner identity and existing WebAuthn public state transferred, or each nontransferable record individually quarantined with no authorization widening.
- OAuth grants, client registrations and revocations preserved with verifiable provenance; signed machine admissions and revocations match the effective source state.
- SecretStore key use remains in authorized protected custody; private material never appears in public or ordinary persistence channels.
- Go restart/negative authorization tests, OAuth/MCP, admitted Host terminal receipts, old/new single-writer fencing and rollback reconciliation pass.
- Existing public origin serves only Go FCIS OAuth + MCP and live owner/Host evidence is independently witnessed.

If any acceptance predicate is unverified, record it precisely; a Git commit, source test, proof sketch or Host description **is not** the production migration.

## Standards and source boundaries

[NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html) (authenticator lifecycle); [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html) (OAuth security BCP); [RFC 7009](https://www.rfc-editor.org/rfc/rfc7009.html) (revocation semantics); [RFC 8414](https://www.rfc-editor.org/rfc/rfc8414.html) (issuer metadata); [RFC 8707](https://www.rfc-editor.org/rfc/rfc8707.html) and [RFC 9728](https://www.rfc-editor.org/rfc/rfc9728.html) (resource binding/metadata); [W3C WebAuthn Level 3](https://www.w3.org/TR/webauthn-3/) (credential and RP binding); [NIST SP 800-57](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final) (key custody/lifecycle); and ISO/IEC 27001:2022 (risk-managed operational controls where adopted/applicable).

No cited standard defines the complete FountainStore-to-FountainStore format. **This is Fountain Coach's own security acceptance contract**, not an RFC, authorization bypass or proof of a completed operation. No second API, Git source of identity, public migration endpoint, Skill ID, plugin or provider login is created merely by adopting it.
