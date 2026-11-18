# FCIS Go ownership and acceptance

## Peer canonical API acceptance order

The **single writable FCIS HTTP contract** is `Fountain-Coach/.github/FCIS-OPENAPI.json` at the same Git authority level as `FCIS-STACK.md`. Lock exact canonical revision before implementing. The 10 historical Swift owner/machine operations are predecessor input only. The root contract defines 30 HTTP operations and 36 JSON schemas as source-specified Go target, not a census of currently callable tools. Check actual Go route/auth/error parity and terminal evidence per operation; never mutate the old owner OpenAPI independently. Keep separate proof for OAuth WebAuthn, MCP, machine-signature calls and private native FountainStore transaction/recovery. The latter is not an OpenAPI path.

The clean Go service may initialize its own **fresh dedicated FountainStore instance**, re-enroll its sole owner/clients/Hosts, and retire Swift FCIS runtime entirely. Never claim the old issuer's token continuity or Swift snapshot relocation is necessary. Payment/Stripe remains priority two, outside cutover.

## Historical migration order (superseded by the standalone-Go owner decision)

- **Historical first slice (not binding for clean cutover):** Go machine/Host lifecycle and deterministic build candidate originally expected the existing Swift issuer, keys and Store snapshots. This is **not** the current Go target.
- **Current target:** Standalone Go OAuth/passkey/MCP + machine/Host transport in `FCIS-OPENAPI.json`, with fresh native FountainStore identity and persistence. Preserve the versioned MIDI2 IDL and FCIS-KIT registry.
- **Outside FCIS Go cutover:** native macOS/iOS apps and CoreMIDI capabilities remain separately owned; FountainStore on-disk format remains source-owned by `Fountain-Coach/Fountain-Store`, not a requirement to keep a Swift daemon.

## Independent Go development verification — owner-authorized, not Host-admitted

The owner explicitly chooses independent isolated Ubuntu development tests so FCIS Go can be built while the old production FCIS is unavailable or being replaced. **Do not block a trusted, pinned Go source test on an OAuth/Host capability grant issued by the service under replacement.** The development lane is not a second FCIS instrument and cannot perform production effects.

- Source: require an owner-approved immutable Git commit from the private runtime repository, obtained through existing authorized Git access or transferred as a verified Git bundle from the owner's existing checkout. Verify `HEAD` equals the selected full SHA and the checkout is clean; an anonymous inaccessible private repository is a **source access issue**, not a failed production grant.
- Worker: use an approved external Ubuntu machine, unprivileged account, isolated checkout, scratch/cache and fixed `scripts/fcis-ci.sh go` from canonical `.github`. Keep real signing keys, OAuth sessions, mounted production FountainStore and production release paths out of the sandbox. No network access to the test process after pinned source/dependency acquisition; declare unavailable dependencies rather than enabling unbounded downloads.
- Commands: `go mod verify`, `go vet ./...`, `go test -race -count=1 ./...`, `go build ./...`. Run only against the reviewed commit with `GOPROXY=off`, `GOFLAGS=-mod=readonly`, isolated Go caches and bounded resources. Record Go version, Git SHA, clean-tree status, exit codes, redacted logs and source/test evidence. This yields `DEV-VERIFIED` or `DEV-FAILED` — never a FountainStore production receipt.
- Permission: Git checkout access and explicit owner authorization for local tests are sufficient. The production Host's `workstation.go.verify` grant is **not** a prerequisite. It remains mandatory for calls *through that instrument*, along with signed Host evidence when a production effect is invoked.
- Stop: refuse untrusted source, unsafe executor or missing authenticated checkout; preserve read-only production and make the precise access/isolation limitation visible. Never create a second permission service, Swift adapter, new build instrument or CI provider to evade a simple Go test.

## Production admission and release — separate authority

Only after DEV-VERIFIED evidence: promote a signed source-bound executable via the existing expressly authorized release process; require real owner passkeys/client OAuth, typed Host/MIDI2 grants, native FountainStore execution receipts, public OAuth/MCP checks and rollback readback. Missing Host admission blocks *privileged release*, not independent source development.

## Build Instrument input/output

Input is only `action`, `workflow`, `sourceRevision`, `correlationID`, `idempotencyKey`. The Host selects working directories, signed release identity, toolchain and isolated cache on approved storage. Output is phase, bounded digests and run identities. `local-tested` never means a FountainStore terminal receipt. No arbitrary model-supplied commands, fabricated machine grants, environment or credentials. Actual owner-authorized existing SSH/systemd/Caddy release paths may be used when independently authenticated; do not treat one missing MCP release tool as proof of no SSH authority.

## Refusal proof

Reject: unknown workflow or input key, wrong or dirty source revision, absent capability grant, unverified external mount, simultaneous build lease, expired/revoked identity, attempt to perform release through the build instrument, duplicate idempotency without an authoritative Store claim, and claimed Host success without Store terminal. A go test can execute code: require a trusted commit and an isolated no-secret/no-network build host before runtime admission.

## Acceptance boundary

Local Go tests prove code behavior. Host admission requires registered IDL/Kit adapter, release digest, trusted policy and persistent Store correlation. Live acceptance requires Go OAuth/MCP public route readback, owner passkey/client authorization, native Store restart readback, one admitted Host receipt and scoped revocation, each bound to the exact released build. Source promotion and ChatGPT plugin sync are separate operations, with canonical Git and the unchanged plugin identity.

## Regression: do not repeat the 17 November three-hour escalation

**Original goal:** a usable FCIS Go migration Skill plus deterministic Go Build instrument. **Observed:** Go worker, Linux sandbox and Swift Host adapter became SOURCE-TESTED (seven focused native tests), but a live `workstation.go.verify` grant, FountainStore terminal and ninth ChatGPT installed Skill were not established. Continuing into issuer redesign, repeated SwiftPM rebuilds and provider synchronization did not satisfy the live DoD.

**Correct bounded response to the same facts:** first distinguish **independent Go source verification** (owner-approved isolated Ubuntu, clean pinned Git and fixed Go checks) from **production FCIS instrument invocation** (owner-signed `workstation.go.verify` grant and Host/FountainStore terminal). If `workstation.go.verify` is not admitted, stop *that privileged instrument dispatch*, but continue safe standalone Go development tests when a trusted checkout and sandbox are available. Source-test failure calls for a focused code correction, not rebuilding a Swift issuer, granting Host rights or demanding another ChatGPT plugin. Keep the 15-minute bounded iteration; compiler success never implies live grant or release. Do not trade another three-hour development loop for an unobserved acceptance predicate.
