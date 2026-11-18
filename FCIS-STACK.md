# FCIS — Standalone Go Stack Specification

**Owner:** Fountain Coach · **Canonical architecture:** [`FCIS-STACK.md`](FCIS-STACK.md) · **Peer canonical HTTP API:** [`FCIS-OPENAPI.json`](FCIS-OPENAPI.json) (OpenAPI 3.1.0; equal organization source authority for HTTP wire contracts)  
**Architecture version:** 1.0 · **Decision date:** 18 November 2026  
**Decision status:** Owner-selected target; Git review/merge and deployed conformance remain separate  
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
| Public ingress | Existing `fcis.fountain.coach` origin, HTTPS/Caddy |
| Runtime protocol | MCP for AI clients; authenticated typed Host/MIDI2 instrument interfaces |
| Human authentication | WebAuthn/passkeys, bound to an explicitly authorized owner |
| Client authorization | OAuth 2.0 authorization code + PKCE S256; scoped grants and revocation |
| Persistence | Fresh dedicated **FountainStore**, accessed and managed natively by Go |
| Git authority | `Fountain-Coach/.github` for instruction/Skill ownership; source-owning repositories retain their executable contracts |
| Service deployment | Immutable source-bound Go artifact, service supervision and independently verified HTTPS release |
| Initial operators | Fountain Coach owner(s); clients and machines may re-enroll |
| First production priority | Go issuer **and** MCP active on the existing production origin, with native persistent authorization |
| Second priority | Provider-neutral payment instrument; Stripe is its first adapter |

**Explicit non-dependencies for the initial FCIS cutover:** Swift OAuth issuer, a legacy Swift snapshot, migration of historical refresh families, PostgreSQL, SQLite, Kubernetes, distributed replication, hosted-model inference, Stripe, or migration of other Fountain Coach services.

No architectural choice can silently widen the original cutover DoD. New gates require a reproduced failure or an already-applicable binding contract; see [FCIS Goal Fidelity](docs/FCIS-Non-Invention-and-Goal-Fidelity.md).

## 2.1 Peer canonical OpenAPI authority

The architectural source and its executable HTTP contract are maintained **together and at equal organization authority** in this repository: **[`FCIS-STACK.md`](FCIS-STACK.md)** owns system topology, persistence, instruction/capability boundaries and fixed DoD; **[`FCIS-OPENAPI.json`](FCIS-OPENAPI.json)** owns the exact Go-target HTTP paths, operationIds, request/response schemas, authentication mechanisms and refusals. Neither file derives its authority from the old Swift domain OpenAPI. Update both in one reviewed change when HTTP and architectural decisions intersect.

The former [`midi2-gpu-fabric/apps/estate-publisher/contracts/fcis-owner.openapi.json`](https://github.com/Fountain-Coach/midi2-gpu-fabric/blob/fix/fcis-go-store-parity-witness-20261117/apps/estate-publisher/contracts/fcis-owner.openapi.json) is a **pinned historical compatibility input**, not a second mutable Go-target contract. Existing Swift test fixtures and predecessor production evidence remain unchanged until their own owning migration. Any derived source-domain or Access UI copy must declare its exact canonical root revision and must never edit its own semantics independently.

Canonical OpenAPI describes HTTP boundaries only. MCP JSON-RPC method and tool schemas, MIDI2 IDL / MIDI-CI, FCIS-KIT execution contracts, and FountainStore WAL/on-disk semantics keep their separate authoritative owners. An OpenAPI operation marked `specified-only-not-deployed` is *not* an admitted Host command, released instrument, tested Go endpoint, or production evidence.

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

Register a stable owner identity through a restricted, explicit first-owner bootstrap. Verify WebAuthn challenge, origin, relying-party ID, signature, user verification, expiration, replay resistance and credential state. Passkey identity is **not** blanket Host authorization. Never reinitialize the owner or generate a new authority silently on restart/corruption. Private signing material is kept in protected secret custody outside Git and public APIs.

### 4.2 OAuth authority

Implement OAuth discovery, client registration, authorization/consent, authorization-code + PKCE S256 exchange, refresh rotation, token audiences, expiry, revocation, and durable grant records. Preserve the public **issuer URL**, not historical refresh tokens. Clients such as ChatGPT may reauthorize after the clean cutover.

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

Use a **new, private FCIS FountainStore root**, initially on a persistent Hetzner volume. Implement native Go bootstrap from an empty root; no requirement for a Swift-generated manifest, historical Store relocation, or production Swift process.

The canonical FountainStore engine and on-disk format are owned by [`Fountain-Coach/Fountain-Store`](https://github.com/Fountain-Coach/Fountain-Store). Native Go support must be versioned, tested against that owning contract and must not become a silent incompatible fork.

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

## 6. Security and operational invariants

- TLS terminates at Caddy; Go listens on a private interface.
- Signing keys, passkey secrets and service credentials are never committed to Git or rendered in diagnostic output.
- Bootstrap creates an authorized owner rather than exposing a public unauthenticated enrollment endpoint.
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

## 7. Production deployment and finite DoD — **priority one**

Deploy one Go-native FCIS on the existing Hetzner host, with Caddy retaining the existing `https://fcis.fountain.coach/` identity. Fresh owner bootstrap and client reauthorization are acceptable because the installation currently has only its owners/operators.

**Initial cutover succeeds exactly when:**

1. Public OAuth **and** MCP are served by the standalone Go runtime, with no Swift FCIS service in the active request path.
2. The FCIS-owned FountainStore initializes from empty storage; durable identity/grants and receipts survive restart.
3. Owner passkey sign-in and scoped OAuth code/PKCE authorization function against the public issuer.
4. One client (including ChatGPT when usable) authenticates and successfully invokes an admitted MCP operation.
5. One enrolled Host authenticates and returns independently verifiable admitted-operation evidence.
6. Grant revocation takes effect durably; the live release and rollback artifact are independently identified.

**Not part of this DoD:** historical Swift state/refresh-token migration, distributed replication, customer multi-tenancy, commercial billing, redesign of unrelated applications, a second publication domain, or a new instruction system.

**Observed predecessor (18 November 2026):** The Hetzner Go candidate was running read-only on localhost `18363`, while public OAuth/MCP Caddy routing still used Swift processes on `18361`/`18362`. That candidate used JSON authority state and a migration-dependent writable path. Its existence is implementation evidence **only**; it does not satisfy the clean target or production DoD.

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
- [FCIS European Regulatory Applicability and Change Maintenance](docs/FCIS-EU-Regulatory-Maintenance.md)
- [Governance publication](https://governance.fountain.coach/) — independent public edition; no automatic publication from this Git file

**Single-source rule:** An update to an external provider adapter, instrument release or hosted FCIS service is not an amendment of this document unless it changes the adopted stack contract. Conversely, editing this file never deploys a service or authorizes an instrument.
