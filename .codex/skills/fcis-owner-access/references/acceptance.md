# Owner authentication and recovery — evidence matrix

**Source design:** [Fountain Press Access passkey specification](https://github.com/Fountain-Coach/fountain-press/blob/ef9226a2dc25106caffc0ef3e87a7e110a17aef4/docs/access-passkey-first-owner-signin-2026-11-12.md) (historical design source; not proof of the current deployment). First-device owner passkey sign-in and returning sign-in were live-accepted on 12 November 2026; independent second-device account recovery remains unverified. For internal API updates, follow [the FCIS OpenAPI maintenance protocol](openapi-maintenance.md); its source-only contract checks do not certify owner recovery, Host revocation or production deployment.

**Binding governance:** [07](https://governance.fountain.coach/chapters/07-agent-operating-guide/), [08](https://governance.fountain.coach/chapters/08-validation-and-acceptance/), [142](https://governance.fountain.coach/chapters/142-fountainauthkit-governed-authorization-authority/), [143](https://governance.fountain.coach/chapters/143-simplicity-is-key-one-bootstrap-one-trusted-session/), [152](https://governance.fountain.coach/chapters/152-the-host-is-the-instrument/), [160](https://governance.fountain.coach/chapters/160-skill-sovereignty-and-governed-distribution/), [161](https://governance.fountain.coach/chapters/161-host-enrollment-client-consent-and-access-management/).

**Upstream:** [W3C WebAuthn Level 3](https://www.w3.org/TR/webauthn-3/), [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html), [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017.html). Verify normative versions at implementation.

| Gate | Real evidence required | Never substitute |
| --- | --- | --- |
| Existing subject | Same issuer principal and audited first enrollment | Linux username or extra account database |
| WebAuthn verifier | Fresh challenge, RP ID, origin, signature, UV, expired/replayed denial; wrong origin, wrong RP ID, wrong challenge and bad signature denied | Static form or happy-path-only test |
| Management session | Secure HttpOnly/SameSite cookie, CSRF, step-up, logout, expiration | Basic header/JS bearer described as BFF |
| Recovery | Second authenticator logs in, lost device is revoked, lost-all procedure approved | Server password file as routine UX |
| Authorization | Existing OAuth PKCE/scopes and real per-effect Host enforcement | Successful person authentication implying client authority |
| Grant revocation | Disposable-client revoked grant, denied refresh and MCP execution, durable Store receipt | Badge, mock, inventory alone |
| Actual devices | Physical iPad Safari and Mac with accessibility and interrupted-network acceptance | Simulated Chromium viewport |
| Continuity | Existing ChatGPT Host grant works, no extra issuer/Host, rollback available | Tests of newly invented infrastructure |
| Semantic operation discovery | Existing OpenAPI `operationId`/`summary`/`description` explain intent, non-use, authorization, effect and typed results; compare actual native route schemas | A vague tool name, HTTP status, prompt-only instructions or a generated operation unsupported by a handler |
| Capability inventory parity | Current issuer/Host admission and installed instrument identities match HTTP fleet projection and MCP `tools/list` for one pinned target/client/revision; new admitted instrument appears without another handwritten `host.describe` enum | An advertised instrument, stale static operation list, or Host description used as a grant |
| Callability and effects | Verified current client grant, target route and typed `tools/call` dispatch; refused unknown/revoked/expired/wrong-target; terminal FountainStore evidence | Enrollment/health badge, source-only Swift test or static OpenAPI claim |
| Skill release | Reviewed source, hash-pinned mirror, unchanged plugin ID and provider readback | ZIP, extra plugin or Git-only claim of installation |

Classify each test as PROVEN, FAILED, or NOT_ESTABLISHED. The source-only Skill revision cannot certify dynamic instrument discovery or generic authorized dispatch; require separately executed native conformance and real-client evidence. Preserve exact denied operation, source revision, and next smallest corrective step. Never surface private secrets, user account records, client inventory or bearer tokens in static Press, logs or prompts.
