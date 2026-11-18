# FCIS canonical stack and HTTP contract — critical review

**Frozen review date:** 18 November 2026. **Canonical subjects:** [FCIS-STACK.md](../FCIS-STACK.md) (architecture v1.0) and [FCIS-OPENAPI.json](../FCIS-OPENAPI.json) (OpenAPI 3.1, document version 0.3.1). **Scope:** currently committed organization source, separately identified unmerged Go candidates, and the existing organization Git/Skill delivery checks. This is a *dated review*, not a legal/security certification, a deployed-runtime inventory, or an amendment of the HTTP wire contract. Reevaluate each finding against current Git revisions before acting.

## Overall judgment

The ownership split is sound: FCIS Go owns issuer/OAuth/MCP orchestration; each admitted Host and MIDI2/FCIS-KIT instrument owns execution; FountainStore owns durable effects; the organization Git repository owns agent instructions; OpenAPI owns the HTTP boundary alone. The missing link is **executable, owner-controlled conformance and release authority**. The current organization \`build\` check is demonstrably narrower than its name suggests; 30 Go-target HTTP operations are declared \`specified-only-not-deployed\`, not currently proven live. Do not invent more endpoints to solve that deficiency.

### P0 — discrepancies to resolve before a *corresponding* release claim

| ID | Source finding (observed 18 Nov) | Implementation acceptance | Owner |
| --- | --- | --- | --- |
| C01 | Draft Go server \`midi2-gpu-fabric\` PR #145 \`apps/estate-publisher/fcis-go-native/internal/native/server.go\` hard-pins the historical 0.2.1 owner OpenAPI, while organization root is 0.3.1. | Pin exact canonical root blob/digest in Go and verify every implemented method, request, auth, error and response. Keep predecessor 0.2.1 as non-authoritative fixture. | FCIS Go runtime + \`fcis-owner-access\` |
| C02 | Draft Go \`internal/native/mcp.go\` advertises protocol \`2025-03-26\`; root OpenAPI describes \`initialize\`, \`Mcp-Session-Id\` and generic JSON-RPC. The published MCP specification 2026-07-28 instead defines the modern stateless era, \`server/discover\`, per-request metadata and method/name headers. | Declare supported protocol eras, validate 2026-07-28 independently, and keep a bounded legacy path for clients that still negotiate an older era. Do not claim ChatGPT's actual negotiated era without a captured handshake/request. | FCIS Go runtime + MCP conformance |
| C03 | Draft Go README in PR #145 depends on importing historical Swift authority and private JSON state; the newly adopted FCIS stack instead chooses a fresh native Go FountainStore and allows owner/client reauthorization. | Implement the *selected* clean bootstrap; independently prove Store commit/restart, revocation, receipt and rollback. Retain historical migration tests only if needed for predecessor continuity, not as a mandatory cutover dependency. | FCIS Go + Fountain-Store |
| C04 | Current OpenAPI marks **all** 30 HTTP operations \`specified-only-not-deployed\`, and \`skills/tests/test_fcis_root_openapi.py\` hard-requires this global value. | Represent spec intent and release capability separately; make runtime conformance tests accept a versioned implementation/release manifest without pretending an operation is live from source. | Canonical contract maintainers |

### P1 — wire accuracy, security and drift

| ID | Finding | Smallest required correction |
| --- | --- | --- |
| C05 | One loose \`PasskeyCredentialAssertion\` is reused for login assertion and registration attestation. | Distinct login and enrollment request/response schemas, correct WebAuthn type/refusal tests. |
| C06 | Pair-begin, pair-decision and owner-revoke POST request bodies omit \`required: true\`. | Mark genuinely mandatory bodies and reject absent, duplicate or malformed payloads in Go tests. |
| C07 | \`OAuthTokenResult\` marks response token properties \`writeOnly\`; this conveys the wrong contract for returned tokens. | Correct read/write schema semantics and verify no-store responses and token-redaction behavior. |
| C08 | Device-signing is described by \`x-fcis-machine-signed-body\` and prose, while OpenAPI \`security: []\` makes standard tooling treat these operations as unauthenticated. | Define explicit interoperable signed-request metadata (e.g., OpenAPI security representation or a precise security extension), binding key ID, canonical bytes, target, nonce, clock window, replay, and refusal. Preserve its non-OAuth machine mechanism. |
| C09 | \`MCPJSONRPCResponse\` does not enforce exactly one of a typed \`result\` or \`error\` with valid request ID; tool input schemas are independent of the generic HTTP OpenAPI. | Adopt JSON-RPC response one-of rules; validate the actual generated/client-specific FCIS-KIT tool catalog separately. |
| C10 | Draft Go builds tool discovery with a small hardcoded list rather than a client/grant-specific current admitted registry. | Generate discovery from admitted typed Host instruments and permission projection; revalidate at call time and do not publish invented permissions. |
| C11 | OpenAPI doesn't specify the supported MCP era, version negotiation and older-client compatibility matrix. | Add precise per-era ingress metadata, header checks, errors, negative tests, and an explicit deprecation policy. |

### P1 — continuity and governance

| ID | Finding | Required follow-up |
| --- | --- | --- |
| C12 | Existing organization workflow only runs canonical Skill SHA-256, plugin parity, Python unit tests and \`git diff --check\`. It does **not** build or race-test the separate Go module. | Invoke the same repo-owned validation commands from POSIX hooks, owner CI and GitHub as a *mirror*. Go compilation and runtime conformance remain source-owner-specific. |
| C13 | GitHub ruleset requires GitHub Actions \`build\`; local hooks can be disabled. Git recovery mirror/bundles exist, but no owner bare Git acceptance hook has been witnessed live. | Stage owner Git server \`pre-receive\` enforcement, isolated candidate validation and atomic authorized \`main\` promotion; retain current GitHub protection until accepted. |
| C14 | The GitHub workflow uses \`git diff --check\` without an explicit PR/base range, so a clean checkout normally checks no changes. Some policy/procedure prose still mentions 5–8 packaged Skills while the verified inventory is nine. | Use a real base/head diff and eliminate stale hand-counted inventories in affected implementation instructions. |
| C15 | Organization EU regulatory procedure requires periodic review but no active scheduled monitor or issuer-specific legal applicability record was verified. | Implement source/evidence review and named human applicability assessment; do not assert blanket applicability or fabricate an autonomous monitor. |
| C16 | No evidenced binding ties \`source SHA → OpenAPI digest → Go binary → Store receipt → live HTTPS readback\` into a single promotion decision. | Produce independently verifiable immutable acceptance record; release approval remains a distinct authorized transition. |

## Source addresses and independent standards

- Canonical: [stack](../FCIS-STACK.md), [HTTP contract](../FCIS-OPENAPI.json), [test](../skills/tests/test_fcis_root_openapi.py), [current GitHub CI](../.github/workflows/test.yml), [existing hooks](../.githooks), [Git release policy](FCIS-Git-Release-Policy.md), [EU regulation policy](FCIS-EU-Regulatory-Maintenance.md).
- Historical Go source candidate: [PR #145](https://github.com/Fountain-Coach/midi2-gpu-fabric/pull/145) (draft, source-only) and related unmerged PRs #146–#149; inspect latest branch before implementation.
- MCP: [2026-07-28 specification release](https://blog.modelcontextprotocol.io/posts/2026-07-28/) (stateless era), [MCP current specification](https://modelcontextprotocol.io/specification/2026-07-28).
- Git: [githooks reference](https://git-scm.com/docs/githooks) for the client/server enforcement distinction. 
- These statuses are **18 November findings**; upstream standards, implementation branches and installed plugin versions may change independently. Avoid a hand-maintained “all deployed endpoints” census; generate and compare it against actual handler/manifest inputs.

## Acceptance and non-goals

Findings are requirements for their *own affected slice*, not sixteen new prerequisites to the original finite Go production DoD. Priority-two payments, universal multi-tenancy, replacing Git, rewriting MIDI2, alternate authorization services and legal certification are excluded. A source fix must show its exact test; a deployment claim additionally requires real OAuth/MCP/Host/Store/HTTPS evidence. The bounded, owned implementation sequence lives in [FCIS Maintenance and Git-Hook CI Plan](FCIS-Maintenance-Hook-CI-Plan.md).
