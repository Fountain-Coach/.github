# FCIS Go ownership and acceptance

## Peer canonical API acceptance order

The **single writable FCIS HTTP contract** is `Fountain-Coach/.github/FCIS-OPENAPI.json` at the same Git authority level as `FCIS-STACK.md`. Lock exact canonical revision before implementing. The 10 historical Swift owner/machine operations are predecessor input only. The root contract defines 30 HTTP operations and 36 JSON schemas as source-specified Go target, not a census of currently callable tools. Check actual Go route/auth/error parity and terminal evidence per operation; never mutate the old owner OpenAPI independently. Keep separate proof for OAuth WebAuthn, MCP, machine-signature calls and private native FountainStore transaction/recovery. The latter is not an OpenAPI path.

The clean Go service may initialize its own **fresh dedicated FountainStore instance**, re-enroll its sole owner/clients/Hosts, and retire Swift FCIS runtime entirely. Never claim the old issuer's token continuity or Swift snapshot relocation is necessary. Payment/Stripe remains priority two, outside cutover.

## Historical migration order (superseded by the standalone-Go owner decision)

- **Historical first slice (not binding for clean cutover):** Go machine/Host lifecycle and deterministic build candidate originally expected the existing Swift issuer, keys and Store snapshots. This is **not** the current Go target.
- **Current target:** Standalone Go OAuth/passkey/MCP + machine/Host transport in `FCIS-OPENAPI.json`, with fresh native FountainStore identity and persistence. Preserve the versioned MIDI2 IDL and FCIS-KIT registry.
- **Outside FCIS Go cutover:** native macOS/iOS apps and CoreMIDI capabilities remain separately owned; FountainStore on-disk format remains source-owned by `Fountain-Coach/Fountain-Store`, not a requirement to keep a Swift daemon.

## Build Instrument input/output

Input is only `action`, `workflow`, `sourceRevision`, `correlationID`, `idempotencyKey`. The Host selects working directories, signed release identity, toolchain and isolated cache on approved storage. Output is phase, bounded digests and run identities. `local-tested` never means a FountainStore terminal receipt. No arbitrary model-supplied commands, fabricated machine grants, environment or credentials. Actual owner-authorized existing SSH/systemd/Caddy release paths may be used when independently authenticated; do not treat one missing MCP release tool as proof of no SSH authority.

## Refusal proof

Reject: unknown workflow or input key, wrong or dirty source revision, absent capability grant, unverified external mount, simultaneous build lease, expired/revoked identity, attempt to perform release through the build instrument, duplicate idempotency without an authoritative Store claim, and claimed Host success without Store terminal. A go test can execute code: require a trusted commit and an isolated no-secret/no-network build host before runtime admission.

## Acceptance boundary

Local Go tests prove code behavior. Host admission requires registered IDL/Kit adapter, release digest, trusted policy and persistent Store correlation. Live acceptance requires Go OAuth/MCP public route readback, owner passkey/client authorization, native Store restart readback, one admitted Host receipt and scoped revocation, each bound to the exact released build. Source promotion and ChatGPT plugin sync are separate operations, with canonical Git and the unchanged plugin identity.

## Regression: do not repeat the 17 November three-hour escalation

**Original goal:** a usable FCIS Go migration Skill plus deterministic Go Build instrument. **Observed:** Go worker, Linux sandbox and Swift Host adapter became SOURCE-TESTED (seven focused native tests), but a live `workstation.go.verify` grant, FountainStore terminal and ninth ChatGPT installed Skill were not established. Continuing into issuer redesign, repeated SwiftPM rebuilds and provider synchronization did not satisfy the live DoD.

**Correct bounded response to the same facts:** inspect the installed registry and existing `host.describe`-only grant first. If `workstation.go.verify` is not admitted, report the exact missing authorization and **stop**; do not write another issuer/Host/Store adapter under a generic "proceed." If the task is explicitly *source implementation*, limit it to one tested candidate and one focused repair, separate Git proof from runtime admission, then stop at the 15-minute hard limit. A source-merged PR or compiler success is not a live grant or hosted plugin version. Do not trade another three-hour development loop for an unobserved acceptance predicate.
