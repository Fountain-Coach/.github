# FCIS Go ownership and acceptance

## Peer canonical API acceptance order

The **single writable FCIS HTTP contract** is `Fountain-Coach/.github/FCIS-OPENAPI.json` at the same Git authority level as `FCIS-STACK.md`. Lock exact canonical revision before implementing. The 10 historical Swift owner/machine operations are predecessor input only. The root contract defines 30 HTTP operations and 36 JSON schemas as source-specified Go target, not a census of currently callable tools. Check actual Go route/auth/error parity and terminal evidence per operation; never mutate the old owner OpenAPI independently. Keep separate proof for OAuth WebAuthn, MCP, machine-signature calls and private native FountainStore transaction/recovery. The latter is not an OpenAPI path.

The Go service creates a **new physical FountainStore root on headless Hetzner**, then verifies and imports the existing FCIS owner/passkey, OAuth client/grant/revocation and signed Host authority state. Its protected SecretStore references and signing custody remain under the existing owner-granted Hetzner provider. A new *instance* is not a new *owner*. The predecessor Swift runtime can retire after cutover; raw historical bearer tokens and arbitrary Swift directory copies are not a requirement. Verified rotation/revocation state and issuer continuity **are** required. Payment/Stripe remains priority two.

## Headless Hetzner migration order (owner correction, 19 November 2026)

- **Initiate from currently authorized Hetzner source.** Read back old/new Store authority, SecretStore custodian, trust-set fingerprints, passkeys and revocations. Do not migrate from a Mac or use a workstation Keychain as an operator prerequisite.
- **Bounded transfer:** consistent source snapshot + independently verified restore; retained secret custody; typed logical FCIS data import; original owner/issuer/admitted machines; negative revocation and replay tests. See [FCIS Migration Security Profile](../../../docs/FCIS-Migration-Security-Profile.md).
- **Current target:** standalone Go OAuth/passkey/MCP + Host transport in `FCIS-OPENAPI.json`, with a new *physical* FountainStore root and intact *logical* owner identity/permissions. Preserve the versioned MIDI2 IDL and FCIS-KIT registry; expose no new public migration endpoint.
- **Outside FCIS cutover:** native macOS/iOS apps and CoreMIDI capability migration, customer billing, multi-tenant conversion and distributed replication. FountainStore on-disk format remains owned by `Fountain-Coach/Fountain-Store` and does not require retaining a Swift FCIS runtime after acceptance.

## Independent Go development verification — owner-authorized, not Host-admitted

The owner chooses independent isolated headless Linux development tests so FCIS Go can be built while the old production FCIS is unavailable or being replaced; **no particular Mac is a prerequisite**. **Do not block a trusted, pinned Go source test on an OAuth/Host capability grant issued by the service under replacement.** The development lane is not a second FCIS instrument and cannot perform production effects.

- Source: require an owner-approved immutable Git commit from the private runtime repository, obtained through existing authorized Git access or transferred as a verified Git bundle from the owner's existing checkout. Verify `HEAD` equals the selected full SHA and the checkout is clean; an anonymous inaccessible private repository is a **source access issue**, not a failed production grant.
- Worker: use an approved isolated headless Linux worker, unprivileged account, isolated checkout, scratch/cache and fixed `scripts/fcis-ci.sh go` from canonical `.github`. Keep real signing keys, OAuth sessions, mounted production FountainStore and production release paths out of the sandbox. No network access to the test process after pinned source/dependency acquisition; declare unavailable dependencies rather than enabling unbounded downloads.
- Commands: `go mod verify`, `go vet ./...`, `go test -race -count=1 ./...`, `go build ./...`. Run only against the reviewed commit with `GOPROXY=off`, `GOFLAGS=-mod=readonly`, isolated Go caches and bounded resources. Record Go version, Git SHA, clean-tree status, exit codes, redacted logs and source/test evidence. This yields `DEV-VERIFIED` or `DEV-FAILED` — never a FountainStore production receipt.
- Permission: Git checkout access and explicit owner authorization for local tests are sufficient. The production Host's `workstation.go.verify` grant is not a prerequisite. It remains mandatory for calls *through that instrument*, along with signed Host evidence when a production effect is invoked.
- Stop: refuse untrusted source, unsafe executor or missing authenticated checkout; preserve read-only production and make the precise access/isolation limitation visible. Never create a second permission service, Swift adapter, new build instrument or CI provider to evade a simple Go test.

## Production admission and release — separate authority

Only after DEV-VERIFIED evidence: promote a signed source-bound executable via the existing expressly authorized release process; require real owner passkeys/client OAuth, typed Host/MIDI2 grants, native FountainStore execution receipts, public OAuth/MCP checks and rollback readback. Missing Host admission blocks *privileged release*, not independent source development.

## Build Instrument input/output

Input is only `action`, `workflow`, `sourceRevision`, `correlationID`, `idempotencyKey`. The Host selects working directories, signed release identity, toolchain and isolated cache on approved storage. Output is phase, bounded digests and run identities. `local-tested` never means a FountainStore terminal receipt. No arbitrary model-supplied commands, fabricated machine grants, environment or credentials. Actual owner-authorized existing SSH/systemd/Caddy release paths may be used when independently authenticated; do not treat one missing MCP release tool as proof of no SSH authority.

## Refusal proof

Reject: unknown workflow or input key, wrong or dirty source revision, absent capability grant, unverified external mount, simultaneous build lease, expired/revoked identity, attempt to perform release through the build instrument, duplicate idempotency without an authoritative Store claim, and claimed Host success without Store terminal. A go test can execute code: require a trusted commit and an isolated no-secret/no-network build host before runtime admission.

## Acceptance boundary

Local Go tests prove code behavior. Host admission requires registered IDL/Kit adapter, release digest, trusted policy and persistent Store correlation. Live acceptance requires independently verified **Hetzner-initiated Store/SecretStore owner-state continuity** (including retained trust-root custody and old revocations), Go OAuth/MCP public route readback, existing owner passkey/client authorization, native Store restart readback, one admitted Host receipt and scoped revocation, each bound to the exact released build. Rollback must never re-enable an old revoked grant. Source promotion and ChatGPT plugin sync are separate operations, with canonical Git and the unchanged plugin identity.

## Regression: do not repeat the 17 November three-hour escalation

**Original goal:** a usable FCIS Go migration Skill plus deterministic Go Build instrument. The old production Host advertised only `host.describe` as proven callable, which is irrelevant to isolated source verification. **Observed:** Go worker, Linux sandbox and Swift Host adapter became SOURCE-TESTED (seven focused native tests), but a live `workstation.go.verify` grant, FountainStore terminal and ninth ChatGPT installed Skill were not established. Continuing into issuer redesign, repeated SwiftPM rebuilds and provider synchronization did not satisfy the live DoD.

**Correct bounded response to the same facts:** first distinguish **independent Go source verification** (owner-approved isolated headless Linux, clean pinned Git and fixed Go checks) from **production FCIS instrument invocation** (owner-signed `workstation.go.verify` grant and Host/FountainStore terminal). If `workstation.go.verify` is not admitted, stop *that privileged instrument dispatch*, but continue safe standalone Go development tests when a trusted checkout and sandbox are available. Source-test failure calls for a focused code correction, not rebuilding a Swift issuer, granting Host rights or demanding another ChatGPT plugin. Keep the 15-minute bounded iteration; compiler success never implies live grant or release. Do not trade another three-hour development loop for an unobserved acceptance predicate.
