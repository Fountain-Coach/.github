# FCIS — Standalone Go Stack Specification

**Owner:** Fountain Coach · **Canonical architecture:** [`FCIS-STACK.md`](FCIS-STACK.md) · **Peer canonical HTTP API:** [`FCIS-OPENAPI.json`](FCIS-OPENAPI.json) (OpenAPI 3.1.0; equal organization source authority for HTTP wire contracts)
**Architecture version:** 1.2 · **Initial decision:** 18 November 2026 · **Prerequisite-free system decision:** 19 November 2026
**Decision status:** Standalone prerequisite-free Go system; optional existing-instance adoption preserves independently verified prior authority. Git source, generated implementation, test evidence and deployed state remain separate.
**Public service identity:** `https://fcis.fountain.coach/`
**Immediate priority:** Go-native production cutover · **Second priority:** payment instrument with a Stripe provider adapter

> **Claim boundary:** This specification is the canonical *target architecture*, not evidence of a running production release. A Git commit, source test, process, staging URL or a public status badge cannot replace runtime acceptance.

## 1. Identity and purpose

**FCIS** means **Fountain Coach Instruction System**. It is Fountain Coach's provider-neutral system of instruction and executable capability governance. [RFC 0001](profile/README.md) remains the normative four-layer instruction architecture:

| Layer | Exclusive responsibility |
| --- | --- |
| `AGENTS.md` | Behavioral law: what is allowed or forbidden |
| `PLANS.md` | Intended task and its finite Definition of Done |
| Canonical Skills | How a governed task is performed |
| MCP/instrument plane | What tools, data and admitted capabilities are callable |

The **FCIS Go service** is the owner-operated implementation of the identity, permission, capability-discovery and execution-control plane. It is **not** the owner of the LLM, a general-purpose arbitrary shell, a Git replacement, or an extra instruction layer.

For each request the runtime must establish **who** is calling, **which** capability/version is admitted, **where** execution is permitted, **which** scoped grant governs it, and **what actually happened**, with durable evidence.

The user-selected initial deployment is one owner-operated installation. There are no customer accounts or active commercial payment users whose legacy grants must be migrated. The architecture may grow to multiple organizations, but multi-tenancy is **not** a prerequisite to its first release.

## 2. Binding target decisions

| Concern | Target decision |
| --- | --- |
| Runtime | Native, standalone **Go**, with no Swift FCIS runtime dependency |
| Public ingress | Configurable issuer/RP origin; local loopback first installation or operator-controlled HTTPS. `fcis.fountain.coach` + Caddy is an optional deployed instance, not a prerequisite. |
| Runtime protocol | MCP for AI clients; authenticated typed Host/MIDI2 instrument interfaces |
| Human authentication | WebAuthn/passkeys, bound to an explicitly authorized owner |
| Client authorization | OAuth 2.0 authorization code + PKCE S256; scoped grants and revocation |
| Persistence | New self-initializing native Go **FountainStore** on private local persistent storage; optional separately approved logical import of verified existing FCIS authority |
| Git authority | `Fountain-Coach/.github` for instruction/Skill ownership; source-owning repositories retain their executable contracts |
| Service deployment | Immutable source-bound Go artifact, service supervision and independently verified HTTPS release |
| Initial operators | Fresh installation starts UNCLAIMED with zero owner/grants/remote Hosts; local single-use ticket enables first WebAuthn owner claim. Existing adoption preserves verified prior owner, grants and Hosts. |
| First production priority | One selected stable Go issuer **and** MCP with native persistent authorization; for this installation, the Go origin is `go.fcis.fountain.coach` and the Swift predecessor is retired separately |
| Second priority | Provider-neutral payment instrument; Stripe is its first adapter |

**Standalone prerequisites:** only a supported Linux OS, private writable filesystem, functioning cryptographic randomness, local operator access and WebAuthn-capable browser/authenticator. An existing FCIS instance, owner, Store, SecretStore, Host, MIDI2 device, GitHub service, Mac, Hetzner host, Caddy proxy, hosted AI model and Stripe account are **not** prerequisites. Historical security-state continuity is **required only when the separately selected adopt-existing profile is invoked**, and then must preserve verified grants, refresh-family and revocation semantics without exposing raw secrets.

No architectural choice can silently widen the original cutover DoD. New gates require a reproduced failure or an already-applicable binding contract; see [FCIS Goal Fidelity](docs/FCIS-Non-Invention-and-Goal-Fidelity.md).

## 2.1 Peer canonical OpenAPI authority

The architectural source and its executable HTTP contract are maintained **together and at equal organization authority** in this repository: **[`FCIS-STACK.md`](FCIS-STACK.md)** owns system topology, persistence, instruction/capability boundaries and fixed DoD; **[`FCIS-OPENAPI.json`](FCIS-OPENAPI.json)** owns the exact Go-target HTTP paths, operationIds, request/response schemas, authentication mechanisms and refusals. Neither file derives its authority from the old Swift domain OpenAPI. Update both in one reviewed change when HTTP and architectural decisions intersect.

The former [`midi2-gpu-fabric/apps/estate-publisher/contracts/fcis-owner.openapi.json`](https://github.com/Fountain-Coach/midi2-gpu-fabric/blob/fix/fcis-go-store-parity-witness-20261117/apps/estate-publisher/contracts/fcis-owner.openapi.json) is a **pinned historical compatibility input**, not a second mutable Go-target contract. Existing Swift test fixtures and predecessor production evidence remain unchanged until their own owning migration. Any derived source-domain or Access UI copy must declare its exact canonical root revision and must never edit its own semantics independently.

Canonical OpenAPI describes HTTP boundaries only. MCP JSON-RPC method and tool schemas, MIDI2 IDL / MIDI-CI, FCIS-KIT execution contracts, and FountainStore WAL/on-disk semantics keep their separate authoritative owners. An OpenAPI operation marked `specified-only-not-deployed` is *not* an admitted Host command, released instrument, tested Go endpoint, or production evidence.

## 2.2 Prerequisite-free whole-system contract (*Voraussetzungslos*)

[**FCIS-SYSTEM.json**](FCIS-SYSTEM.json) is the organization-root, machine-readable **whole-system composition**. It owns initialization, state transitions, Go-native Store/vault schema, Host/instrument/Skill/scenario lifecycle, tenant/provider boundaries, frontend binding, optional migration and acceptance. This architecture and its [peer HTTP OpenAPI](FCIS-OPENAPI.json) remain source contracts, not deployed evidence.

**Fresh install has zero FCIS prerequisites.** `fcis init` creates a private native Go FountainStore v1, encrypted Go SecretStore v1, issuer Ed25519 key, tenant/instance identity and one-use owner setup ticket. The default service binds to localhost only and serves the existing Fountain Press owner UX at `/manage/` from the Go binary. A WebAuthn-capable browser claims the first owner with a locally delivered expiring ticket. The first credential and setup-token burn commit atomically. Once CLAIMED, no bootstrap ticket can alter the owner or issue a grant; additional credentials require authenticated owner policy. No imported state, GitHub, SSH, Caddy or historical Host is needed.

A built-in read-only Go software Host provides local discovery and bounded receipts while the external instrument registry starts empty. Typed, versioned and signed external Host/MIDI2 instruments may be enrolled later with explicit owner authorization. The registry intersects per-client effective grants during MCP tools/list and revalidates on each tools/call; discovery alone cannot authorize execution. FCIS Skills and scenarios use bundled signed manifests and owner/tenant-controlled learning/promotion, not live Git as a mandatory database. Customers own their data and derived Skill rights, and may bring provider credentials only through scoped custody.

**Optional adopt-existing** is a separate, explicit operation that imports verified owner/passkey, client/grant/revocation, Host and secret-custody state. An **existing claimed** installation can choose this optional profile; it must retain the verified existing issuer identity. The owner-selected new Hetzner Go instance is instead a distinct `fresh-install` authority and must not adopt predecessor state. This optional migration cannot block, masquerade as or substitute for a prerequisite-free installation.

**Generation order:** complete and validate this cross-component specification first; generate all Go/embedded frontend source next; execute tests only after source generation; release and live acceptance remain distinct owner-authorized phases.

## 3. Logical topology

```text
HTTPS clients / owner / ChatGPT
            |
         Caddy
            |
     fcis.fountain.coach
            |
      FCIS Go service
      |     |      |
   OAuth   MCP   Host admission / instrument routing
      |     |      |
      +-----+------+
            |
     FCIS Go-owned FountainStore
       (dedicated persistent root)
            |
    durable grants, inventory,
    job state, typed receipts

Git (.github + source-owning repos)
    --> canonical instructions, admitted build/revision metadata

Authenticated enrolled Hosts <--> FCIS
    --> execute their own admitted instruments
```

These are **logical modules**, not a mandate for independent network microservices. One Go process is adequate initially. FountainStore can be an embedded native Go storage component with a single authoritative writer; it need not introduce a separate database server.

## 4. Modules and authority boundaries

### 4.1 Owner identity and WebAuthn

For a fresh instance, establish exactly one first owner using the time-limited local one-use setup ticket and verified WebAuthn registration. For optional adopt-existing, preserve the **existing** authorized owner identity and WebAuthn credential/public-key bindings. Verify WebAuthn challenge, origin, relying-party ID, signature, user verification, expiration, replay resistance and credential state. Passkey identity is **not** blanket Host authorization. First-owner bootstrap is permitted **only if an installation is independently verified to have no prior owner**; it is not the production migration path. Never reinitialize the owner or generate replacement authority silently on restart/corruption. Private signing material remains in protected SecretStore custody outside Git and public APIs; the headless Hetzner process must not depend on a Mac Keychain.

### 4.2 OAuth authority

Implement OAuth discovery, client registration, authorization/consent, authorization-code + PKCE S256 exchange, refresh rotation, token audiences, expiry, revocation, and durable grant records. The fresh instance uses its configured issuer origin and begins without grants. When adopting an existing issuer, preserve its public **issuer URL** and independently verified active grants, rotation-family validity and revocation state. Never copy raw bearer tokens into an unprotected migration record; reauthorize a client (such as ChatGPT) **only** if the specific predecessor grant cannot be securely imported and verified. Never activate a grant from an unauthenticated database copy.

Public protocol surface includes `/.well-known/oauth-authorization-server`, `/.well-known/jwks.json`, `/.well-known/oauth-protected-resource`, `/oauth/register`, `/oauth/authorize`, `/oauth/token`, owner/Host endpoints, and `/mcp`. The peer canonical [`FCIS-OPENAPI.json`](FCIS-OPENAPI.json) owns endpoint shapes. The HTTP operation inventory is source-declared there and may include unimplemented target operations, explicitly labeled as such; the operation list is not an inventory of callable MCP tools.

### 4.3 MCP interface

Serve MCP initialization, permitted capability discovery, typed invocation, refusals and lifecycle results. The MCP transport must not become a parallel operation executor or authorize operations by advertising tool names. Discoverability, client grant, execution admission and independently verified completion are different states.

### 4.4 Instrument/Host plane

Use the source-owned MIDI2 IDL and governed FCIS-KIT capability contracts. Every instrument declares stable identity, version, admissible operations, typed inputs and results, permissions, resource/cost boundaries, failure states and required terminal evidence.

Every enrolled machine has authenticated identity and a bounded capability inventory. Enrollment is not MIDI-CI readiness; MIDI-CI readiness is not an authorized session; a session is not a grant to invoke every operation. An individual Host executes its own admitted operations and returns verifiable evidence. The FCIS runtime routes and observes; it does not substitute an unrestricted SSH endpoint.

### 4.5 Git-owned instruction plane

Canonical organization behavior and Skills belong under this organization's `AGENTS.md`, `PLANS.md`, `.codex/skills/` and policy documents. Domain repositories own their source, schemas and released capabilities. Runtime records the **exact version/digest/admission**, not an alternative mutable copy of canonical Git source.

Maintain the single existing Git-backed FCIS Skill distribution. Do not create ZIP-based or competing Skills/plugins.

### 4.6 Durable execution and audit

For a named run record request identity, idempotency identity, actor, resource, target machine, capability/version, source/release digest, applied authorization decision, lifecycle events, terminal result, and evidence references. Persist revocations and terminal effects with the appropriate transactional invariants. Distinguish **requested**, **admitted**, **executing**, **succeeded**, **failed/refused**, and **unverified**. HTTP 200, a process PID or generated plan is not a terminal receipt.

## 5. FountainStore persistence contract

### 5.1 Ownership

Use a **new, private Go FountainStore root** on any supported Linux persistent filesystem. A fresh installation initializes its own Go-native v1 format, empty collections and first-owner state without predecessor or Swift runtime. The explicitly optional adopt-existing profile imports **verified existing FCIS logical authority** and preserves original owner/passkeys, client/grant/rotation/revocation and signed Host identities with independent readback. Import is not a prerequisite for the native Go Store.

The canonical FountainStore engine and on-disk format are owned by [`Fountain-Coach/Fountain-Store`](https://github.com/Fountain-Coach/Fountain-Store). The new native Go v1 physical format is defined explicitly in FCIS-SYSTEM.json and is not claimed byte-compatible with the Swift historical Store. Fountain-Store remains the storage semantics source owner; versioned source review and verified logical import prevent silent format divergence.

### 5.2 Logical collections (proposed schema)

- `fcis.owners`, `fcis.passkeys` — subjects and public WebAuthn credential state
- `fcis.oauth.clients`, `fcis.oauth.grants`, `fcis.oauth.revocations` — client, token-family and authorization lifecycle
- `fcis.hosts`, `fcis.admissions`, `fcis.instruments` — machine identities, admission and version references
- `fcis.executions`, `fcis.receipts`, `fcis.audit` — durable jobs, typed terminal evidence and append-only security events

The names are **target logical collections**, not an assertion that all presently exist. Sensitive secrets are excluded from ordinary records, logs and receipts.

### 5.3 Storage correctness

Native Store support must implement durable transaction/commit ordering, write-ahead logging, crash recovery, controlled manifest/table lifecycle, atomic mutation where required, single-writer fencing, backup/restore and exact readback. Any grant-rotation or revoke operation must be atomic with respect to its permission decisions, not a collection of unsafe independent writes.

The initial service uses one authoritative writer. Replicated high-availability writes are **future work**, not a proven feature of the current Go writer.

### 5.4 Service independence

FountainStore is the **owned storage technology**, not a requirement to keep an unrelated Swift-based Store daemon alive. Other applications may use their own instances. The FCIS persistent root must not be concurrently writable by unrelated Hosts.

### 5.5 Existing authority continuity and SecretStore custody

The [FCIS Migration Security Profile](docs/FCIS-Migration-Security-Profile.md) governs only the explicitly optional **adopt-existing** path, including the Hetzner-initiated old-to-new transfer for the current Fountain Coach instance. It is not a clean-install dependency. It requires source/target inventories, existing owner trust-root verification, source snapshot and verified restore, single-writer fencing, typed migration of security state, protected SecretStore custody, revocation-safe rollback and independently verified cutover. The existing Golden Key owner UX may approve a specific operation on any eligible enrolled device; a WebAuthn sign-in is not by itself a substitute for a separately required owner-root signature. The Mac is not a dependency or migration controller. The peer canonical OpenAPI needs no new HTTP method unless an existing public operation actually changes.


## 6. Security and operational invariants

- Fresh-install Go serves loopback only by default. Remote exposure requires explicit HTTPS/issuer/RP binding. Caddy is an optional deployment adapter, not a prerequisite.
- Signing keys, passkey secrets and service credentials are never committed to Git or rendered in diagnostic output.
- On an existing deployment, migration preserves the current authorized owner and authenticators; no silent replacement bootstrap or unrestricted enrollment. A genuinely empty new installation remains a separate case.
- Every client/Host grant is bounded to explicit scopes, audience, expiry, target and capability where applicable.
- Refresh rotation, revocation, idempotency and denial remain effective after restart.
- Provider/model availability, instrument execution admission and terminal evidence are independently represented.
- Only the owning capability contract can authorize effects; a model, MCP wrapper or transport cannot bypass it.
- The release uses an immutable Go artifact and source digest; the predecessor remains recoverable while the new public service is verified.
- Private configuration, database files, backups and rollback state stay outside public web roots.

## 6.1 European regulatory maintenance — applicability before claims

The standalone Go FCIS must be maintained against **applicable European Union and Member State law**, using the [FCIS European Regulatory Applicability and Change Maintenance procedure](docs/FCIS-EU-Regulatory-Maintenance.md). This is a continuing engineering and governance duty, **not** a new API authority, an instrument, a regulator, or a claim of legal certification. [Governance Chapter 118](https://governance.fountain.coach/chapters/118-european-cybersecurity-profile/) is the risk-based cybersecurity engineering profile, not a legal applicability ruling.

For the actual issuer/MCP/Host/FountainStore deployment, the responsible operator must maintain a **source-versioned applicability register** containing official EU and relevant national sources, operator/product classification, affected functionality and processing, legal effective dates, reasoned `applicable` / `not_applicable` / `requires_review` decisions, reviewer, next review date, controls, release evidence and unresolved findings. Recheck at least **monthly** and immediately following relevant legal changes, new jurisdictions, customer-facing features, AI use, personal-data processing, payments, incidents or distribution changes. An agent/automation may collect source changes, but only recorded competent review determines legal applicability; a recurring schedule is not established merely by writing this policy.

Review at minimum GDPR/ePrivacy, NIS2 and national implementation, Cyber Resilience Act, AI Act, EAA/national accessibility obligations, and eIDAS/DSA/consumer/copyright/payment duties **when product facts trigger them**. Do not assume every act applies to a private, single-owner Go service. A legal change proposal is not enacted law; a source test is not conformity evidence. An applicable binding obligation for the actual release must be addressed through its own proper acceptance, but an unproven compliance hypothesis does **not** silently expand the finite priority-one production cutover DoD below. The priority-two payment instrument requires its own applicability review when introduced.

## 6.2 Git-hook continuous integration and maintenance ownership

Fountain Coach selects **version-controlled, portable POSIX `/bin/sh` scripting** as FCIS CI orchestration. See the [dated criticism](docs/FCIS-Spec-OpenAPI-Critique-2026-11-18.md) and [maintenance and Git-hook CI plan](docs/FCIS-Maintenance-Hook-CI-Plan.md) for the phased implementation and independently testable acceptance. The organization owns the shared check entrypoint, actual tests and immutable source/release evidence; native Go checks and Go/FountainStore acceptance remain at their proper source owners.

Existing local `.githooks` and GitHub workflows are **current source mechanisms**. They are not an independently accepted owner-controlled Git server. The owner-operated bare Git origin MUST enforce its own reviewed `pre-receive` rules and exact-revision promotion; bypassable client hooks alone cannot protect `main`. Execute incoming candidate tests under a separate unprivileged identity, never as the protected Git hook user with owner keys. Promotion must be explicitly authorized, source-pinned, fail-closed on failed checks and atomic with respect to the observed predecessor SHA. An accepted Git revision is **not** a production release or a legal-compliance certificate.

Keep the existing GitHub `build` branch rule intact until a replacement owned-origin acceptance is independently demonstrated. GitHub Actions may re-run the **same source-owned scripts**, but must not remain the only place the organization can build, test and recover FCIS. Preserve offline Git bundle restore and distinct plugin-hosted version readback. No CI scheduler, public endpoint, background worker or new runtime instrument is created merely by adopting this specification.

## 7. Production deployment and finite DoD — **priority one**

**Selected Fountain Coach production profile — 23 November 2026: `fresh-install`.** Native Go starts with its **own empty** FountainStore, SecretStore, issuer keys, first owner, clients, grants and machine admissions. It **does not import or migrate Swift state**. `adopt-existing` remains a separately available, explicitly selected product profile; none of its predecessor-continuity checks is a dependency of this clean-start DoD. This corrects the earlier optional migration DoD that had been applied to the wrong selected profile.

**Deployment identity.** The issuer origin and WebAuthn RP ID must be explicit, coherent and stable for the selected instance. The current new installation is `https://go.fcis.fountain.coach` with RP ID `go.fcis.fountain.coach` on the owner-controlled Hetzner host. This is an observed instance selection, **not a mandatory host/domain prerequisite** for other fresh installations. Retirement of Swift on `fcis.fountain.coach` must not silently reidentify the Go issuer, redirect an OAuth token to another audience, or change the registered RP ID. A legacy hostname may be disabled or explicitly redirected after compatibility checks; it is **not** a second active issuer. No additional physical owner enrollment is required merely to implement the existing session/redirect path on the chosen Go origin.

**Seven jointly necessary and sufficient production gates (one frozen DoD):**

1. **GO-DOD-01 — Independent Go release.** A source-bound, reproducibly tested, immutable standalone Go binary owns the selected HTTPS issuer, OAuth metadata/token/authorization routes, MCP transport and Fountain Press `/manage/`. Its native Store and Vault belong to one private instance; no Swift service, Mac, GitHub connection, preexisting FCIS account, imported Store or external model is required to initialize or operate the core. Public discovery and service readiness are independently verified against the running binary and its exact release digest.
2. **GO-DOD-02 — One complete owner experience.** From an empty fresh Store, the owner claims one first WebAuthn credential on an eligible **physical iPad Safari** through the **existing Fountain Press Access frontend**, with a single-use expiring setup invitation and genuine user verification; no Mac/copy-paste test harness. A completed registration persists the owner and credential with the consumed invitation. It transitions predictably into a **verified native Go browser session** and then into the original Clients / Hosts / Skills / Reference workspace. Returning sign-in, valid-session return, expiry, sign-out and denied unauthenticated entry are separately witnessed. A credential row or HTTP 200 page **without a valid session** must never unlock the workspace. A Secure, HttpOnly, SameSite cookie is checked server-side across the management and OAuth routes; UI code stores no token or grant and does not refer to Swift as issuer.
3. **GO-DOD-03 — New-client OAuth lifecycle.** A **newly registered** public client completes authorization-code + PKCE S256 against the selected Go issuer, with exact redirect, resource, bounded scopes and explicit consent. Access/refresh, refresh rotation, expiry, refusal, grant revocation and denial of a spent/revoked token are proved; effective authorization survives restart without resurrecting revoked grants. Existing Swift clients or refresh families are **not** imported.
4. **GO-DOD-04 — Actual Go MCP execution.** One authorized fresh client (ChatGPT if supported, otherwise a standards-conforming independent client) discovers only operations available under its actual grant, calls **one already-admitted typed MCP/Host operation**, and receives an independently readable, durable FountainStore terminal receipt. Unknown, missing-scope, wrong-target and revoked requests fail without executing effects. MCP discovery and documentation alone do not satisfy this gate.
5. **GO-DOD-05 — One real freshly admitted Host.** At least one external owner-selected machine enrolls with a new machine identity under **this** Go issuer, is explicitly admitted and authorized, and completes one signed, scoped, target-bound operation with independent Host/Store evidence. Unknown, altered, replayed or unadmitted machines are refused. The built-in software Host can prove prerequisite-free offline operation, but does **not** substitute for this production external-Host witness. Fleet UI reports only issuer-backed admitted states; unsupported routes are visibly unavailable, not fabricated success.
6. **GO-DOD-06 — Persistence, custody and recovery.** On the real private Go Store/Vault: restart and crash-recovery tests preserve owner, session policy, clients, admitted Hosts and permission decisions; Store transactions have a single writer, safe revocation and replay fencing; keys/tokens remain out of logs, Git and static pages. An encrypted, independently restorable checkpoint and an immutable release rollback are tested without restoring revoked rights or replacing the owner unexpectedly. Negative WebAuthn origin/RP/challenge/signature, CSRF, cookie, OAuth and Host authorization tests pass. A successful source test alone is not a live recovery receipt.
7. **GO-DOD-07 — Public cutover and Swift retirement.** The **selected** production Go issuer and MCP are publicly usable over verified HTTPS, with complete end-to-end Owner → OAuth client → admitted Host → typed Store receipt acceptance. Public routing and supported clients have no Swift FCIS service in the active request path; predecessor Swift OAuth/MCP units are disabled/retired after the Go evidence is complete, with rollback provenance retained privately. Return and logout on the physical iPad remain correct after restart. Cutover, service identity, native receipts and failed-authority refusal are independently rechecked; no second live authority is advertised.

**Evidence and stopping rule.** Each gate has a pinned source revision and executable SHA-256, applicable positive and negative source tests, an independent HTTP/browser or Host observation, and a native Store/receipt reference when effects are claimed. Mark gates `NOT_ESTABLISHED` until their own witness exists. **DONE means all seven gates passed on the same deployed Go instance, not merely seven green unit suites or an HTTPS 200.** Stop when this DoD is met; proposed additions require a new owner-requested goal or an independently reproduced binding failure, never a moving finish line.

**Explicit non-goals:** legacy Swift data/credential/grant/machine-trust migration; all-fleet re-enrollment; distributed replication or HA, multi-tenancy, billing/Stripe, provider subscriptions, physical MIDI2 hardware interoperability, a new frontend, independent multi-device account recovery, a second Skill/plugin, or speculative extra approval ceremonies. These may be separate products or acceptance profiles, **not** blockers for this production release.

**Optional `adopt-existing` profile — NOT selected:** When separately and explicitly chosen for an existing installation, independently verify predecessor owner/key, client grant, refresh/revocation, Host and SecretStore custody continuity and non-resurrecting rollback per the Migration Security Profile. Do not apply those conditions to `fresh-install`.

**Observed predecessor (18 November 2026):** The Hetzner Go candidate was read-only on localhost `18363` while public OAuth/MCP used Swift `18361`/`18362`. Historical evidence is not the selected fresh Go release or its acceptance.

## 8. Scale without inventing a second stack

**Initial:** single Go process, dedicated Store, one owner/tenant, small fleet.
**Growing fleet:** bounded concurrent sessions, indexed Store access, execution queues, resource controls and predictable retention.
**Multiple organizations:** explicit tenant-scoped identity and permission/data isolation; no GUI-only filter.
**High availability:** multiple stateless Go frontends and verified replicated/failover storage; requires a proven coordinated writer or equivalent Store contract.

Scale is achieved by evolving FountainStore's measured concurrency, replication and recovery capacity. Neither SQL databases nor an unproven multiwriter design is a mandatory initial cutover dependency.

## 9. Future commercial capability — **priority two**

A payment gateway is provided by a **provider-neutral FCIS Payment Instrument**; Stripe is its first external adapter. It is **not** a built-in OAuth subsystem, not an alternate capability plane, and **not a dependency** of FCIS production cutover.

Candidate contract only (not admitted or released): `fountaincoach.payment@0.1.0`, with typed checkout creation, payment status, authenticated provider-event reconciliation, explicitly approved refund, and receipt readback. The owning instrument enforces price/account authority, cost boundaries, idempotency and safe replay. FountainStore records durable intent, provider identifiers and verified terminal events; a redirect alone never proves payment.

The Stripe adapter must pin and verify Stripe's **official** OpenAPI revision/projection where available, and separately verify webhook signature/event contracts. See [Official OpenAPI Dependency](docs/FCIS-Official-OpenAPI-Dependency.md). Payment completion must not silently grant unrestricted FCIS or Host capabilities.

This is a **second-priority specification seam**, not permission to start or deploy payment integration during the Go cutover.

## 10. Source ownership and top-down navigation

**This file and the peer [`FCIS-OPENAPI.json`](FCIS-OPENAPI.json) are canonical at the organization root, each for its declared authority (architecture and HTTP wire contract respectively).** Other repository READMEs should link here and declare their own boundary, never copy normative stack prose. Update this file through reviewed changes in `Fountain-Coach/.github`; downstream links are projections, and historical source/production claims must be verified independently.

| Source owner / consumer | Responsibility and relationship |
| --- | --- |
| [Organization profile](profile/README.md) | Top-level FCIS identity and four-layer standard |
| [Organization AGENTS](AGENTS.md) / [PLANS](PLANS.md) | Behavior and intent, not a competing architecture |
| [`midi2-gpu-fabric`](https://github.com/Fountain-Coach/midi2-gpu-fabric) | Current FCIS Go candidate source and Host runtime/integration |
| [`Fountain-Store`](https://github.com/Fountain-Coach/Fountain-Store) | Canonical persistence engine/format; Go conformance requirement |
| [`midi-backplane`](https://github.com/Fountain-Coach/midi-backplane) | Source-owned MIDI2 IDL and command transport |
| [`midi2`](https://github.com/Fountain-Coach/midi2) | MIDI 2.0/UMP/MIDI-CI protocol implementations |
| [`FountainAuthKit`](https://github.com/Fountain-Coach/FountainAuthKit) | Historical/reusable identity contract; not FCIS Go runtime dependency |
| [`FountainStoreHostEnrollmentKit`](https://github.com/Fountain-Coach/FountainStoreHostEnrollmentKit) | Existing Host-enrollment contract/fixture; not assumed live admission |
| [`joining-machine-daemon`](https://github.com/Fountain-Coach/joining-machine-daemon) | Reusable peer daemon recipe, not central issuer |
| [`Reframe`](https://github.com/Fountain-Coach/Reframe) | Creative workspace consuming admitted FCIS capabilities |
| [`fountain-press`](https://github.com/Fountain-Coach/fountain-press) | Access/publishing UI consumer, not token issuer |
| [`fountain.coach`](https://github.com/Fountain-Coach/fountain.coach) | Public estate navigation; separate publication authority |
| [`governance.fountain.coach`](https://github.com/Fountain-Coach/governance.fountain.coach) | Public Governance source; independent chapter/publication authority |

**Maintenance rule:** When a reviewed FCIS stack change alters an interface or a consuming repository's obligations, update this canonical document **first or in a coordinated reviewed change**, then update only affected contract/source-owner and README links. Do not automatically edit all 99 organization repositories for unrelated changes. A source PR is not a deployed release; link parity is not runtime admission.

## 11. Normative references

- [RFC 0001 — Orthogonal Instruction Architecture](profile/README.md)
- [Goal Fidelity and Non-Invention](docs/FCIS-Non-Invention-and-Goal-Fidelity.md)
- [FCIS-KIT Standard](docs/FCIS-KIT-Standard.md)
- [Official OpenAPI Dependency](docs/FCIS-Official-OpenAPI-Dependency.md)
- [Git Release Policy](docs/FCIS-Git-Release-Policy.md)
- [FCIS Source Critique, 18 November 2026](docs/FCIS-Spec-OpenAPI-Critique-2026-11-18.md)
- [FCIS Maintenance and POSIX Git-Hook CI Plan](docs/FCIS-Maintenance-Hook-CI-Plan.md)
- [FCIS European Regulatory Applicability and Change Maintenance](docs/FCIS-EU-Regulatory-Maintenance.md)
- [Governance publication](https://governance.fountain.coach/) — independent public edition; no automatic publication from this Git file

**Single-source rule:** An update to an external provider adapter, instrument release or hosted FCIS service is not an amendment of this document unless it changes the adopted stack contract. Conversely, editing this file never deploys a service or authorizes an instrument.
