# FCIS — Standalone Go Stack Specification

**Owner:** Fountain Coach · **Canonical architecture:** [`FCIS-STACK.md`](FCIS-STACK.md) · **Peer canonical HTTP API:** [`FCIS-OPENAPI.json`](FCIS-OPENAPI.json) (OpenAPI 3.1.0; equal organization source authority for HTTP wire contracts)
**Architecture version:** 1.6 · **Initial decision:** 18 November 2026 · **Prerequisite-free system decision:** 19 November 2026
**Decision status:** Standalone prerequisite-free Go system; optional existing-instance adoption preserves independently verified prior authority. Git source, generated implementation, test evidence and deployed state remain separate.
**Public service identity:** `https://fcis.fountain.coach/`
**Immediate priority:** Go-native production cutover · **Second priority:** payment instrument with a Stripe provider adapter
**Owner/customer experience study:** [FCIS — Founding Experience and Console Study](docs/FCIS-Founding-Experience-and-Console-Study.md) (design study, not additional runtime authority or a cutover prerequisite).

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
| Instruction and Skill custody | Git owns authored organization law, plans and engineering contracts. FountainStore owns private Skill content and revisions; Git/provider copies are explicit optional distribution projections. |
| Service deployment | Immutable source-bound Go artifact, service supervision and independently verified HTTPS release |
| Initial operators | Fresh installation starts UNCLAIMED with zero owner/grants/remote Hosts; local single-use ticket enables first WebAuthn owner claim. Existing adoption preserves verified prior owner, grants and Hosts. |
| First production priority | Go issuer **and** MCP active on the existing production origin, with native persistent authorization |
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

**Optional adopt-existing** is a separate, explicit operation that imports verified owner/passkey, client/grant/revocation, Host and secret-custody state. The currently operating Fountain Coach Hetzner deployment belongs to this optional profile and must retain the existing issuer identity; it cannot be claimed by a new owner bootstrap. This optional migration cannot block, masquerade as or substitute for a prerequisite-free installation.

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

### 4.3 MCP compatibility interface

MCP is an optional external-client projection, not the native FCIS communication architecture or a prerequisite for any MIDI2 peer relationship. Preserve existing authorized MCP interfaces while their consumers require them; do not remove a proven path before its replacement is accepted. Serve MCP initialization, permitted capability discovery, typed invocation, refusals and lifecycle results on that compatibility interface. The MCP transport must not become a parallel operation executor or authorize operations by advertising tool names. Discoverability, client grant, execution admission and independently verified completion are different states.

### 4.4 Instrument/Host plane

Use the source-owned MIDI2 IDL and governed FCIS-KIT capability contracts. Every instrument declares stable identity, version, admissible operations, typed inputs and results, permissions, resource/cost boundaries, failure states and required terminal evidence.

**Owner decision, 27 November 2026 — MIDI2 instruments everywhere:** The LLM/reasoning runtime, semantic voices, authorization, Composer and FountainStore persistence participate through one governed MIDI2 instrument plane. MIDI-CI discovers and describes instruments; typed UMP carries their native communications over admitted transports, including local software peers. The mandatory authorization instrument mediates protected effects using existing owner, admission, consent and grant rules; OAuth, WebAuthn and provider-specific protocols are implementation details at their respective boundaries, not competing FCIS command planes. FountainStore remains the durable evidence authority. The native architecture requires neither MCP nor a particular model provider. Preserve the existing independent first-owner bootstrap, recovery and deterministic operation, without an external model or physical MIDI device. This is a target contract for existing logical modules, not a mandate to create five services, a new authorization authority, a new MIDI standard or a new registry.

Every enrolled machine has authenticated identity and a bounded capability inventory. Enrollment is not MIDI-CI readiness; MIDI-CI readiness is not an authorized session; a session is not a grant to invoke every operation. An individual Host executes its own admitted operations and returns verifiable evidence. The FCIS runtime routes and observes; it does not substitute an unrestricted SSH endpoint.

### 4.5 Store-owned Skills and independent distribution

Organization law, plans, engineering contracts and source collaboration remain Git-owned. Private Skill authorship, immutable draft/revision history, review decisions, admission and rights belong in native FountainStore, under the existing owner/tenant authority. The [Skill custody and publication boundary](docs/FCIS-Skill-Custody-and-Publication.md) governs all new authoring. The existing public FCIS-GO 0.1.40 Git-backed projection and nine already-public legacy maintenance trees remain compatibility exceptions; do not widen or destroy them. GitHub is a publication channel, not our private Skill repository or commercial distribution authority.

The **FCIS Admin API**, in the existing Go process and canonical OpenAPI **0.5.0**, owns the target owner Skill management operations under `/oauth/owner/skills`. Preserve the existing private schema-2 signed release/active-pointer transaction and public schema-1 FCIS-GO. Private draft creation, source/scenario evidence review, exact signed admission and historical readback use the same owner authentication, intent checks, revision CAS and trusted release signer. New private source must never enter Git or provider publication by default. Restoration is a new explicit signed admission, not WAL rewind. The owner session does not replace a required release signature.

The owner-directed Console design uses Vite, React and TypeScript compiled into the same Go executable, as selected in the [Founding Experience study](docs/FCIS-Founding-Experience-and-Console-Study.md). Generate bindings from the peer OpenAPI; use same-origin owner sessions. The working Press frontend and its pinned source bindings remain the existing baseline until the replacement is implemented and accepted; neither the new routes nor a new UI are claimed deployed by this specification.

**Independent commercial distribution (priority two):** a separate owner-signed offer binds one admitted release, source digest, immutable price in currency minor units, explicit distribution rights/terms and selected catalogue visibility. Listing publishes approved metadata and terms only, never private Skill bytes. New price/terms require a new offer; withdrawal stops new acquisitions without automatically revoking existing entitlements. The initial contract supports one-time exact-revision licences (including explicitly free offers), not subscriptions, meter rates or blanket licence transfer. Customer acquisition requires admitted customer identity and resource-bound OAuth consent. The separately scoped `/oauth/skills` resource returns only authorized exact licensed revisions; the `/mcp` audience and Host grants cannot authorize source delivery. Entitlements are current tenant/principal/release-bound Store records; revocation denies future delivery subject to the accepted terms but cannot recall delivered copies. Preserve customer-owned knowledge and rights. Public GitHub/ChatGPT distribution is optional; a client integration or native provider installation must be independently supported and verified.

New owner/API and commercial operations are specified-only until independently implemented and tested. No new service, signer, identity authority, production release, native provider installation or automatic commercial admission is inferred. Preserve the original independent owner-operation P0 DoD.


### 4.5.1 FCIS-LEARN-01 — evidence-to-next-attempt learning

"Good work should teach the next attempt" is a product acceptance obligation, not a model memory feature. The machine-readable `skillAndScenarioSystem.learningAcceptance` in [FCIS-SYSTEM.json](FCIS-SYSTEM.json) specifies the mandatory cross-operation scenario. The canonical OpenAPI `x-fcis-learning-acceptance` binds the existing operations; it introduces no new HTTP endpoint or wire shape.

**Continuous behavior, not a maintenance command.** Every ordinary admitted work episode reaches a recoverable assessment disposition: useful bounded proposal, no lesson, insufficient evidence, or pending when the existing reasoning context is unavailable. Episode closure uses the owning scenario and independent outcome witness; a successful individual instrument receipt is not itself an accepted task. Use the already authorized reasoning context and independently addressed Voices for reflection, with attributed objections and counterexamples. The same lifecycle selects existing Skills by task across domains, never by hard-coded identity or correction. Persist only bounded private evidence and proposal references in existing tenant custody, with a stable episode identity and idempotent recovery. A proposal is not review, admission, publication, or permission. Preserve explicit owner approval and signature, the active predecessor, current client authorization, the founding transition and zero additional inference charges. Do not make assessment availability a prerequisite to deterministic work.

The following six-stage chain remains the positive learning predicate. General acceptance additionally requires ordinary work to initiate assessment without a maintenance request, across more than one admitted domain, with useful and no-lesson outcomes, insufficient evidence, stale/refused authority, interruption/recovery, and actual independent subsequent reuse. One manually revised Skill or one fixture cannot establish this system property. These are source requirements, not evidence that continuous learning is deployed.

1. Witness a real, source-bound, authorized task at the existing active Skill revision R0. Retain the observed deficiency, independently accepted correction, input/source/capability/run identities, terminal receipts, a reusable trigger, explicit constraints, counterexamples and the predeclared subsequent-task predicate. An invalidated run is negative evidence, not an accepted result.
2. Propose only the bounded, reusable change to that existing private Skill. Use the existing private draft operation under owner-authorized intent; do not make a model an owner, automatically promote its suggestion, publish it, or copy private work into Git. Retain attribution and an exact draft digest.
3. Review the draft as `scenario-verified`: independently resolve the accepted run and evidence references from the existing Store and owning domain evidence. Require the same owner/tenant, scenario, task/source identities, terminal receipt, accepted correction and exact draft binding. Source-only review is not scenario evidence. Reject unverified, unrelated, conflicting or cross-tenant evidence without changing the active Skill.
4. Under existing owner consent and release signer, admit R1 as a new private signed revision against exact active predecessor R0. Read back the manifest, signature, source hash, history and atomic active pointer independently. The review and release may not confer execution rights, change rights/licence or publish the lesson.
5. Start a distinct real reasoning session via an actually supported, explicitly selected and authorized provider/client. Select the same Skill by task, resolve its current active R1, verify and supply its exact authorized instruction bytes to that model invocation *before* work. Record the provider/client, request/run and active release/source-digest binding through the participating adapter, not a model's assertion that it read a Skill. Require independent capability authorization for any effect. Missing, stale or unauthorized retrieval/consumption refuses the governed work; no old Git fallback, session impersonation, token transfer or invented provider entitlement.
6. Independently witness the subsequent real comparable task meeting the predeclared predicate because the correction is applied, without the owner repeating the lesson. Preserve a linked baseline, accepted correction, draft/review, R0/R1 release chain, new invocation and terminal outcome with a separately witnessed counterexample/refusal. Use a distinct run and a bounded comparable input, not a replayed fixture, a quoted instruction or a result manufactured by the same validator. Persist the acceptance in existing tenant-owned evidence/receipt custody. Missing independent improvement remains NOT_ESTABLISHED.

The existing `fcis.skills`, execution/receipt/audit, Skill draft/review/revision/inventory and provider/Host boundaries own these effects. The current owner API may support source review without scenario review; a CLI custody receipt or marketplace installation is not evidence of learning. Preserve the previous P0 independent owner-operation/fresh-install gate, one public FCIS-GO adapter, separate provider authorization and existing explicit review/signature policy. The legacy Git automatic-elevation path stays suspended; learning proposals and owner-private reviewed admission do not require Git publication or automatic admission. This scenario is a required product outcome, not a prerequisite for deterministic authorized operations, startup or commercial/payment work. Source acceptance is distinct from runtime and live two-attempt acceptance.


### 4.5.2 FCIS-CHAT-01 — owner conversation and reasoning client

The owner directs a task in the native FCIS Console, resumes a previous conversation and selects an actually connected reasoning client. The existing Go process owns the provider-independent conversation controller; the existing React Console is its human interface. FountainStore is the authoritative history, not the provider. This extends the product contract without extending the P0 independent operation/fresh-install gate. The canonical machine contract is `reasoningAndConversationSystem` in FCIS-SYSTEM.json and the peer OpenAPI 0.7.1 owner chat operations.

**Strict owner decision, 25 November 2026:** External reasoning may consume only the selected account's already-included subscription allowance, with zero additional inference expenditure. No separately metered API lane, workspace credit consumption, overage, recharge, paid fallback or automatic provider selection. A provider's supported current entitlement and enforceable no-extra-charge behavior must be verified before any outbound native reasoning request; missing, exhausted or ambiguous evidence refuses before transmission. A local policy integer of zero, provider login, a subscription name, historical success or a price estimate alone is insufficient. FCIS shall not change the provider's billing settings. The native FCIS HTTP API and MCP are local/product protocol surfaces, not an external separately billed inference lane.

**Reasoning connection modes.** The preferred native instrument relationship is MIDI-CI and typed UMP, with an eligible LLM behind its governed reasoning instrument and required authorization. External ChatGPT-like clients may use the existing OAuth/PKCE and MCP /mcp compatibility boundary where supported: reasoning remains in the selected external subscription client and FCIS exposes only individually authorized capabilities. Neither MCP nor a provider-specific interface is required for native instrument communication. A generic MCP bearer or Host grant does not authorize private Skill source; an authorized participating client must hold explicit skills.owned.read on its exact approved resource and verify rights and provenance. If the supported client cannot do that, the governed task is unavailable. Native FCIS Chat requires a supported account-based reasoning adapter with actual result delivery, independently verified included allowance and refusal of additional charges. MCP tool access alone cannot start native model sessions or retrieve full external transcripts. Do not emulate a provider's browser session, reuse cookies, create an alternative paid lane or equate a Workspace Agent trigger/status with reasoning return. FCIS keeps native mode unavailable until genuinely supported. External chat history is not silently imported; only explicitly authorized work evidence or owner-selected lawful import is retained.

**Owner-owned Skill consumer (26 November 2026, HTTP 0.8.0 target):** Use the existing installation-bound `/oauth/skills` OAuth resource and one separately consented `skills.owned.read` scope for the current single owner/default tenant. Consent explicitly names the client, resource, active owned library (including future active revisions), read-only operations and duration; no automatic grants, mixed Host/commercial scopes, other tenants, drafts, history, customer licence, execution or spend. The new active-only inventory, detail and exact signed release GETs reuse the native Store and existing signer. The issuer revalidates current grant, owner identity and active pointer before disclosure; the selected exact release must verify, and a redacted delivery receipt must commit and independently read back before returning bytes. Existing owner-session administration and signed native recovery are unchanged. Current grants and revocation remain in the same management surface; refresh preserves audience/scope. A delivery receipt is not proof of client consumption; the founding gate remains inactive until independent actual fresh-client use, denial and recovery and owner acceptance. No new provider, separate inference charge, Store or identity service. The contract is specified only.

**Owner Skill MCP transport (HTTP 0.8.1 target):** The existing resource URL `/oauth/skills` also accepts MCP Streamable HTTP JSON-RPC POST, using the existing MCP transport and `skills.owned.read` consent. The same two typed Skill Access v0.2.0 operations project as `fountain_skills_inventory` and `fountain_skills_read_active`, with explicit per-tool OAuth scope and no private metadata before authorization. Dispatch through the existing bounded active inventory and exact signed current-release read, preserving signature, independent receipt, scope, expiry, revocation, cursor and no-store checks. Return verified UTF-8 source and exact signed material only to the authorized participating client; actual verified model use is a separate acceptance predicate. Do not combine with the `/mcp` Host resource, duplicate the Store or registry, create a provider account, incur inference charges, change existing access, or enable the founding gate. This separate-resource projection remains a compatibility path; the single owner bridge decision below supersedes the former assumption that a plugin could connect to both resource URLs. No extra published Skill.

**Single owner authorization bridge — fcis.connect (owner decision, 28 November 2026; FCIS-OWNER-BRIDGE-01):** Connect — establish a resource-bound, explicitly owner-consented relationship. The single external /mcp OAuth scope is fcis.connect; it conveys connection authentication and permission to consult FCIS-managed grants, not ambient owner privilege. No capability is granted merely by connecting. A new connection starts with an empty capability policy. FCIS owner management changes the effective operation permissions on the current authorization family under verified owner session, same-origin intent, explicit confirmation, expected policy revision and durable receipt. Both discovery and every dispatch independently intersect that policy with current signed/admitted capability, owner, client, tenant, resource, target, operation and effect checks. Removing permission takes effect on the same token, including replay; adding an explicitly allowed operation does not require an OAuth scope or registration change. All exposed tool definitions remain typed, explicit and reviewable; no generic executor. The internal skill permission skills.owned.read retains signed active-source checks and durable delivery evidence, not an external scope of this bridge. New/materially changed exposed tool definitions may need provider review independently. Existing individual-scope /mcp grants and legacy /oauth/skills remain isolated compatibility during replacement, not the target design; do not broaden old tokens or retire recovery before independently proving the new connection. No commercial grant, payment, inference, automatic policy expansion or private data before authorization.

**Normative authorization boundary — AuthZEN 1.0 (owner decision, 28 November 2026; FCIS-OWNER-BRIDGE-01).** The 0.9.9 connection-policy target remains an FCIS policy-administration interface, not a proprietary decision protocol. The FCIS Bridge and native protected-operation adapters are Policy Enforcement Points (PEPs); the existing Go authorization engine is the Policy Decision Point (PDP). One authoritative policy/entitlement state remains in FountainStore. No external provider administers FCIS permissions, and no second authorization service, Store or trust root is required.

Pinned external authorities (these exact editions, not moving drafts):

| Authority | Scope in FCIS |
|---|---|
| [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749), [PKCE RFC 7636](https://www.rfc-editor.org/rfc/rfc7636), [RFC 9700 / BCP 240, January 2025](https://www.rfc-editor.org/rfc/rfc9700), [RFC 8414](https://www.rfc-editor.org/rfc/rfc8414), [RFC 8707](https://www.rfc-editor.org/rfc/rfc8707), [RFC 9728](https://www.rfc-editor.org/rfc/rfc9728), [RFC 7591](https://www.rfc-editor.org/rfc/rfc7591) | Existing resource-bound public-client registration, authentication/delegation, PKCE, discovery and token lifecycle. fcis.connect is FCIS-defined consent to connect, not permission to execute. |
| [W3C WebAuthn Level 2 Recommendation, 8 April 2021](https://www.w3.org/TR/2021/REC-webauthn-2-20210408/) | Existing owner passkey baseline; no claim of full WebAuthn conformance or mandate to replace working credentials. |
| [OpenID AuthZEN Authorization API 1.0 Final, 11 January 2026](https://openid.net/specs/authorization-api-1_0-final.html) | Normative PEP-PDP information model and HTTPS JSON decision interface, sections 5, 6, 9, 10, 11. |
| [NIST SP 800-162, January 2014, updated 2 August 2019](https://csrc.nist.gov/pubs/sp/800/162/upd2/final) | Adopted ABAC access-control methodology; not a wire protocol or certification. |
| [W3C ODRL Information Model 2.2](https://www.w3.org/TR/2018/REC-odrl-model-20180215/) and [Vocabulary & Expression 2.2](https://www.w3.org/TR/2018/REC-odrl-vocab-20180215/), 15 February 2018 Recommendations | Adopted digital-rights expression model for assets, parties, permissions, prohibitions, duties and constraints. Commercial policy evaluation is a separately implemented slice, not a claim that an existing grant is ODRL conformant. |

FCIS profile: the PEP constructs AuthZEN subject (type/id), resource (type/id), action (name), and optional context from verified identity, exact target, admitted operation and authoritative current circumstances; caller assertions never establish owner, tenant, admission, consent, payment, rights or policy revision. The PDP resolves current Store state and returns decision boolean plus optional context. Unknown/unsupported attributes cannot grant privilege. FCIS-defined decision-context members, if used, are explicitly local extensions, not standardized AuthZEN semantics. All actual effects remain mediated by the existing typed MIDI2/FCIS-KIT instrument and terminal evidence path. A positive decision is necessary but not sufficient for an effect. Every dispatch is checked against current policy; discovery is not consent. The PEP fails closed on missing, false, malformed, stale or unavailable decision. A mutation must recheck authority at its existing commit fence.

The single-evaluation HTTP projection is POST /access/v1/evaluation on the existing issuer's configured HTTPS PDP origin, protected for separately authenticated/admitted PEPs; ordinary fcis.connect and legacy external tokens do not authenticate a PEP. FCIS uses the existing issuer and an explicitly owner-consented, separate OAuth resource equal to the exact evaluation endpoint and single internal scope authzen.evaluate. This resource is never a scope of /mcp, never part of the provider plugin, and grants only evaluation, not data delivery or execution. The owner consents to the trusted PEP as a policy caller for the current owner tenant. The PEP authenticates the acting connection; the PDP loads the exact active connection event from FountainStore, checks owner, client, tenant, resource, current grant and admission, and does not accept caller-supplied policy or entitlement attributes. A wire decision describes current durable connection policy, not the validity of any particular end-user access token; the PEP must authenticate the actual bearer and recheck its authority at the effect fence. The subject type is fcis.oauth-connection with the authorization event ID; resource type fcis.bridge with the exact /mcp audience; action name is the admitted internal operation scope. No bearer values in the JSON or decision context. The in-process path authenticates the bearer directly and shares the same current grant predicate. A new installation without an HTTPS origin does not advertise the wire PDP. Local Go calls use the same evaluator and verified context without creating a network dependency; the wire projection must independently satisfy sections 5, 6, 10 and 11 before an interoperability claim. Return application/json and 200 for a valid decision (including false); missing required attributes or malformed request return 400, unauthenticated PEP 401, authenticated but unauthorized PEP 403, processing failure 500, with error text. Unknown JSON members are ignored, order is irrelevant, and X-Request-ID is echoed when supplied. Protect transport integrity/confidentiality, verify PEP and PDP trust, limit requests, avoid private policy disclosure, and preserve redacted decision/policy revision/terminal receipt correlation. Metadata GET /.well-known/authzen-configuration identifies the exact HTTPS PDP and evaluation endpoint (section 9); omit unsupported batch/search endpoints, optional capabilities and signed metadata. No anonymous decision endpoint. No full AuthZEN conformance/interoperability, ODRL engine, or payment acceptance claim from source tests. Batch and search are later feature slices; never represent them as deployed by default.

The owner policy administration route remains FCIS-specific and passkey/intent/revision/receipt protected; it is not an AuthZEN endpoint. The specified FCIS Payment Instrument (section 9) reconciles authenticated provider settlement bound to acquisition, asset, customer, amount and currency before issuing an entitlement in FountainStore. ODRL duties and constraints describe permitted use; they do not prove settlement. AuthZEN consumes current rights as decision inputs, never initiates payment or mints entitlements. Preserve existing owner/legacy permissions during the replacement, with no widened access and no live charging.

**Conversation custody.** `fcis.conversations`, `fcis.messages` and `fcis.reasoning-turns` extend the existing private tenant FountainStore; no new Store or identity system. Conversation titles, selected client/model, archive state, ordered human messages, actual returned assistant messages and reasoning-turn lifecycle survive restart, sign-out, disconnect and provider change. The owner can create, list, read, rename, archive, restore, export and explicitly delete conversations independently of provider availability. Use existing owner session, origin/intent checks, tenant/actor-derived IDs, bounded pagination and CAS/idempotency. Never persist hidden chain-of-thought, provider credentials, unapproved external history or raw private source in audit/telemetry. Keep encrypted backups and deletion tombstones according to defined retention; do not resurrect deleted conversation content on restore. Separately required redacted execution and rights evidence follows its own retention and access rules; do not promise removal of copies held independently by external providers.

**Work and learning.** Append the human message durably before a separately consented turn. Bind each turn to exact selected client/model, current signed Skill revision/digest, authorized context, request and result references, and linked independent execution receipts. A completed provider run without actual answer is not a completed chat turn; an answer cannot certify an instrument effect. Unknown/failed/refused/cancelled are separate from completion and require no paid fallback or blind retry. Owner review and signed private admission remain the only promotion route in FCIS-LEARN-01. The new reasoning client can continue the same owner conversation with selected context only after explicit disclosure consent and actual supported eligibility; no provider-owned session required.

**Semantic engraving and evidence feedback (26 November 2026):** the human composes, instruments perform, the Composer engraves. Apply the owned MIDI2-first contract (FCIS-MIDI2-01) and the existing Reframe Score/one-definition-two-projections/MIDI2 Monitor principles. A participant is identified by role and relation before output, not a strip of telemetry. The same typed observation, lifecycle, correlation and verified FountainStore receipt has an accessible, quiet human projection and an independently readable machine projection. An unadmitted observed instrument is neither an eligible reasoning client nor a callable operation. HTTP 0.7.1 adds optional `instrumentObservations` to the existing reasoning-client page, separate from `items`; absent evidence is omitted, historical observation is dated, and the receipt details are disclosed on demand. No raw packets, hidden reasoning, invented activity, model invocation, added permission, new endpoint or second Store. First verify actual MIDI-CI observation -> committed receipt -> independent readback -> Console AX/DOM/reload; later verify actual correlated per-voice lifecycle and results under the existing consent and subscription-only rules. Human and agent observe the same semantic object; neither projection creates execution authority.

**FCIS-POLYPHONY-01 — interactive polyphony (owner decision, 26 November 2026):** A voice is a persistent personification of reasoning, not a model, process, provider or required independent thread. **Owner extension, 27 November 2026:** each semantic voice is a first-class, independently addressable MIDI2 instrument instance; its durable identity is distinct from its versioned capability contract, provider and transient articulation or execution. The human composes, voices articulate, instruments perform, Composer engraves and FountainStore retains authorized continuity. Use the existing MIDI-CI discovery and typed MIDI2/FCIS-KIT invocation and lifecycle plane; admission and scoped grants remain separate from discovery. This is an adopted FCIS architecture requirement, not a MIDI Association normative extension or a claim of current implementation. Several voices can be articulated successively by one authorized external reasoning client. The composition preserves separately addressable contributions, replies, disagreement, revisions and links to independently witnessed instrument results on a shared scenario. Same-model agreement is not independent verification and never authorizes an effect. Use Desktop Commander as the observed reference for direct interactive tool use: short authenticated requests, independently continuing authorized work, correlated progress/result retrieval and selective intervention. Realize the equivalent natively through owned MIDI2 instrument contracts, with mandatory scoped authorization and private authorized continuity in FountainStore. The LLM, voices, authorization, Composer and persistence share that plane; provider protocols are encapsulated. MCP is not required for polyphony; retain its existing authorized compatibility projection without making it a dependency. Keep the Composer a human-intervenable semantic engraving, not a prescribed workflow or mandatory agent hierarchy. A voice may remain present without active inference. Native outbound inference, independently running threads, Codex and other provider runtimes remain optional, never prerequisites to interactive polyphony. Preserve the existing subscription-only, consent, authorization, custody and evidence boundaries. Accept this subcase through an ordinary eligible external reasoning conversation: distinct voices develop a shared scenario, disagree or revise, actually use admitted instruments, and recover attributed contributions and evidence after reconnection; independently witness the Composer on the intended iPad. Do not require an unsupported native adapter for this subcase. This is a specified target, not a new P0 gate or proof of deployment.

**Acceptance:** Create and resume a private conversation after reload/restart; independently witness selected Skill and permitted instrument use over the native MIDI2 instrument relationship, including authorization refusal and receipt readback without MCP. Test existing MCP compatibility independently where retained. Verify a native subscription-only turn with actual returned answer only if the provider genuinely supports it. Disconnect/change reasoning client and resume retained history; witness cross-tenant, stale, revoked, unavailable, exhausted and ambiguous-spend refusal before outbound request. Verify archive, authorized export, deletion/tombstone restore and existing independent signed learning loop. Inspect the real Console on iPad with evidence-linked result and unavailable state. Source-only UI, a simulated provider, a vendor-side status or a merged contract is not live acceptance.

### Situated reasoning — domain composition (FCIS-CHAT-01 reference subcase)

Reframe is the first reference domain, not a mandatory application dependency. A domain is a source-owner-controlled, versioned declaration of applicable Skill identities and revision constraints, authoritative knowledge references and source owners, permitted Instrument/capability identities and version constraints, domain-owned Grounding schema/confirmation requirements and acceptance scenario references. Each invocation resolves exact active signed Skill releases and source digests. It composes existing resources; it creates no second registry, storage engine, permission system, execution runtime or provider. No domain confers a grant. Resolve declarations through the existing authorized source/Store paths; a missing domain is unavailable rather than invented from chat. Preserve ordinary unscoped conversations and deterministic operations.

Grounding records confirmed owner intention, preservation duties, method and transformation constraints as an immutable semantic identity. Its domain owns its schema, content and confirmation. Display state and timestamps are not semantic identity. A changed confirmed semantic field or a policy-bearing source relationship makes dependent interpretation stale; a changed source revision requires revalidation and may retain Grounding only if its source owner proves the policy relationship unchanged; preserve historical provenance, and reuse only independently valid unchanged-source deterministic artifacts. Where the declared domain requires Grounding, absent, unconfirmed, contradictory or stale Grounding blocks affected interpretation until clarified and confirmed. A domain explicitly requiring no Grounding may use null. Never drop semantic obligations to fit provider context.

Situation is current placement/arrangement, selected or wired objects and their authoritative state. Derive it from the selected application/domain state and verified source references, not the transcript. An empty selection stays empty. A selection does not grant source access or execution permission. Distinguish source knowledge from derived situation and conversation. Persist only domain/Grounding reference and the verified context digest in existing private reasoning-turn custody, not the transient Situation projection or a new authoritative fact about the domain. The existing request/idempotency digest and separately authorized source and execution evidence retain lineage.

An owner may submit the optional situatedContext on the existing startOwnerReasoningTurn operation. The server resolves the exact domain declaration, validates current same-tenant resource identities, confirmed Grounding and selection, intersects current grants with the domain's admitted capability set, verifies current signed Skill releases, and binds the actual resolved semantic context and exact ordered approved messages to disclosure consent before dispatch. The owner reviews the exact resolved binding using authorized source projections; the request includes its expectedContextSHA256. The binding contains domain and Grounding references, transient arrangement and selected/wired object references, exact authorized knowledge/source revisions and content digests, selected message identities and content digests, applicable active Skill release IDs and source digests, and admitted Instrument/capability identities and versions within the current grant. Canonical UTF-8 JSON with recursively sorted object keys and preserved array order, compact separators and exact string content defines the binding digest; no digest field, raw credentials or unapproved private material enters it. Server recomputation must match before dispatch. If the necessary source projection is unavailable, refuse; no speculative new endpoint is specified. The domain manifest names required Skills, not their private payload. In-flight revision change before transmission refuses or requires fresh selection/consent; after transmission retain original lineage and mark dependent results stale where applicable, never silently reinterpret them. Tool calls separately revalidate scope and current grants. The returned turn includes domainContextBinding with the domain/Grounding references and server-computed digest; linked receipts remain independent. A resumed or changed-provider conversation re-resolves current context and retains earlier lineage. No automatic disclosure, provider fallback, hidden history ingestion or change to subscription-only policy.

Acceptance within FCIS-CHAT-01: select Reframe's actual existing manuscript/passage references and confirmed Grounding; show the resolved domain/Skill/Instrument identities, context consumption by a genuinely authorized reasoning invocation, and independently verified source-grounded result and any authorized receipt. Change selection and Grounding, verify stale/foreign/unauthorized context refusal before disclosure, preserve old result lineage and restore the conversation without inventing context. Verify unscoped and empty selection behavior, missing domain/required Grounding, and provider unavailability without blocking unrelated deterministic owner operations. This is a reference subcase, not a new P0 gate, a claim of migrated Reframe or proof of subscription entitlement.

**Public contract and private implementation:** The organization publishes only reviewed interoperability and product behavior; private source, unpublished implementation know-how, actual conversations, tenant data, Skill contents and sensitive evidence remain in existing authorized private source/Store custody. See [FCIS intellectual property and publication boundary](docs/FCIS-Intellectual-Property-and-Publication.md).

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
- `fcis.skill-revisions`, `fcis.skill-inventory` — immutable exact signed releases and per-Skill active pointers (existing native custody)
- `fcis.skill-drafts`, `fcis.skill-reviews` — immutable private draft bytes and append-only review decisions (target API)
- `fcis.skill-offers`, `fcis.skill-acquisitions`, `fcis.skill-entitlements` — signed offer terms/state, idempotent acquisition and exact licensed delivery entitlement (priority-two target API)

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

**Fresh-install profile:** deploy the same generated native Go FCIS on any supported Linux host, initialize private Store/vault, claim its first owner with local WebAuthn, then optionally add HTTPS and enrolled Hosts. **Adopt-existing profile:** deploy onto the existing **headless Hetzner** host, retaining `https://fcis.fountain.coach/` behind Caddy; the host initiates independently authorized Store/SecretStore continuity and preserves verified prior owner/Host identities, public-key bindings, grants and revocations. No Mac-dependent ceremony or automatic mass reauthorization.

**The optional Fountain Coach existing-instance production cutover succeeds exactly when:**

1. Public OAuth **and** MCP are served by the standalone Go runtime, with no Swift FCIS service in the active request path.
2. The FCIS-owned Go FountainStore initializes an empty physical root and receives verified old-to-new security-state continuity; owner, grants, revoked permissions and Store receipts survive restart without widened authority.
3. The existing owner passkey bindings and scoped OAuth code/PKCE authorization function against the public issuer, with key custody and any necessary owner approval remaining in the existing authorized Hetzner/Golden Key paths.
4. One client (including ChatGPT when usable) authenticates and successfully invokes an admitted MCP operation.
5. One enrolled Host authenticates and returns independently verifiable admitted-operation evidence.
6. Historical and new grant revocations take effect durably, original secret custody remains protected, and the live release and **revocation-safe** rollback artifact are independently identified.

**Not part of this DoD:** copying a complete unrelated Swift Store directory or exporting raw bearer tokens; distributed replication, customer multi-tenancy, commercial billing, redesign of unrelated applications, a second publication domain, or a new instruction system. **Required within this DoD:** verified logical FCIS Store-to-Store state transfer and existing SecretStore custody continuity. Specific nontransferable credentials fail closed for controlled reauthorization; never silently manufacture a grant.

**Observed predecessor (18 November 2026):** The Hetzner Go candidate was running read-only on localhost `18363`, while public OAuth/MCP Caddy routing still used Swift processes on `18361`/`18362`. That candidate used JSON authority state and a migration-dependent writable path. Its existence is implementation evidence **only**; it does not satisfy the clean target or production DoD.

## 8. Scale without inventing a second stack

**Initial:** single Go process, dedicated Store, one owner/tenant, small fleet.
**Growing fleet:** bounded concurrent sessions, indexed Store access, execution queues, resource controls and predictable retention.
**Multiple organizations:** explicit tenant-scoped identity and permission/data isolation; no GUI-only filter.
**High availability:** multiple stateless Go frontends and verified replicated/failover storage; requires a proven coordinated writer or equivalent Store contract.

Scale is achieved by evolving FountainStore's measured concurrency, replication and recovery capacity. Neither SQL databases nor an unproven multiwriter design is a mandatory initial cutover dependency.

## 9. Future commercial capability — **priority two**

The owner-directed [Founding Experience and Console Study](docs/FCIS-Founding-Experience-and-Console-Study.md#4-commercial-experience) considers payment and usage in the interface from the outset. This design study does not change the priority-two runtime boundary or authorize live charges.

A payment gateway is provided by a **provider-neutral FCIS Payment Instrument**; Stripe is its first external adapter. It is **not** a built-in OAuth subsystem, not an alternate capability plane, and **not a dependency** of FCIS production cutover.

Candidate contract only (not admitted or released): `fountaincoach.payment@0.1.0`, with typed checkout creation, payment status, authenticated provider-event reconciliation, explicitly approved refund, and receipt readback. The owning instrument enforces price/account authority, cost boundaries, idempotency and safe replay. FountainStore records durable intent, provider identifiers and verified terminal events; a redirect alone never proves payment.

The Stripe adapter must pin and verify Stripe's **official** OpenAPI revision/projection where available, and separately verify webhook signature/event contracts. See [Official OpenAPI Dependency](docs/FCIS-Official-OpenAPI-Dependency.md). Payment completion must not silently grant unrestricted FCIS or Host capabilities. The FCIS acquisition API uses only an admitted Payment Instrument and reconciles an authenticated terminal receipt bound to the exact acquisition, customer, offer, amount and currency before committing a paid entitlement. A checkout return is not settlement proof; direct Stripe webhook/refund/card operations belong to the instrument, not the Admin API. When payment is unavailable, fail closed without charging or minting entitlement. No live charging is authorized by this specification.

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
