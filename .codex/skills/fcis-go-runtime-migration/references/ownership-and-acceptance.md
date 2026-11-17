# FCIS Go ownership and acceptance

## One-source migration order

- **First slice:** Go machine/Host lifecycle runtime and deterministic build/test adapter. Preserve existing issuer, owner enrollment, signing keys, revocation semantics and two separate Store views.
- **Next:** FCIS MCP transport, instrument dispatch and machine inventory using exact existing authenticated messages. Preserve the versioned MIDI2 IDL and FCIS-KIT registry.
- **Then:** other portable headless runtime modules. Native macOS/iOS capabilities, CoreMIDI and the current FountainStore engine remain adapters unless a separately scoped replacement has proof.

## Build Instrument input/output

Input is only `action`, `workflow`, `sourceRevision`, `correlationID`, `idempotencyKey`. The Host selects working directories, signed release identity, toolchain and isolated cache on approved storage. Output is phase, bounded digests and run identities. `local-tested` never means a FountainStore terminal receipt. No arbitrary commands, ad-hoc `ssh`, environment or credentials.

## Refusal proof

Reject: unknown workflow or input key, wrong or dirty source revision, absent capability grant, unverified external mount, simultaneous build lease, expired/revoked identity, attempt to perform release through the build instrument, duplicate idempotency without an authoritative Store claim, and claimed Host success without Store terminal. A go test can execute code: require a trusted commit and an isolated no-secret/no-network build host before runtime admission.

## Acceptance boundary

Local Go tests prove code behavior. Host admission requires registered IDL/Kit adapter, release digest, trusted policy and persistent Store correlation. Live acceptance requires a current independently witnessed owner-selected Host readback after service restart and lease renewal. Source promotion and ChatGPT plugin sync are separate operations, with canonical Git and the unchanged plugin identity.
