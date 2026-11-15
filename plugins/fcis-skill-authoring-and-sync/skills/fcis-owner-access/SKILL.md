---
name: fcis-owner-access
description: Govern and verify Fountain Coach owner passkeys, secure sessions, recovery, OAuth client/Host access, and the internal FCIS owner OpenAPI 3.1 contract. Use for access.fountain.coach or fcis.fountain.coach owner login, machine inventory, scoped grants and revocation, or when creating, updating, versioning, validating, troubleshooting or releasing FCIS owner API endpoints and their Swift/OpenAPI conformance. Reuse FountainAuthKit, existing Swift issuer/Host, FountainStore and contract tests; do not invent another authority or claim deployment from source tests.
---

# FCIS Owner Access — Passkeys and Recovery

## Authority and observed baseline

Keep the user's goal: **normal owner sign-in and independent recovery without SSH, passwords copied from an Ubuntu machine, or a second identity system**. First-device Golden Key and WebAuthn passkey enrollment, sign-out, and returning passwordless sign-in were live-accepted on a physical iPad on 12 November 2026. **Independent second-device account recovery remains NOT_ESTABLISHED**; inspect current issuer/owner evidence before making a fresh status claim. Separately classify DOCUMENTED, SOURCE-TESTED, STAGED and LIVE-ACCEPTED operations.

Read published Governance [07](https://governance.fountain.coach/chapters/07-agent-operating-guide/), [08](https://governance.fountain.coach/chapters/08-validation-and-acceptance/), [142](https://governance.fountain.coach/chapters/142-fountainauthkit-governed-authorization-authority/), [152](https://governance.fountain.coach/chapters/152-the-host-is-the-instrument/), [161](https://governance.fountain.coach/chapters/161-host-enrollment-client-consent-and-access-management/), and [143](https://governance.fountain.coach/chapters/143-simplicity-is-key-one-bootstrap-one-trusted-session/) for trusted session and recovery. Check published `chapter-status.json`: Chapter 142 is a current *proposal*, not proof of deployed OIDC.

Preserve authority boundaries:
- `access.fountain.coach/manage/` is the **Fountain Press UI**, not a credential issuer, grant database, or authorization writer.
- `fcis.fountain.coach` is the existing **OAuth issuer and MCP protected resource**; the Host already has a `FountainHostMCPOwnerAuthenticating` adapter for upstream human authentication.
- FountainAuthKit owns scoped OAuth code/PKCE, client registry, refresh, consent and grant revocation; sign-in **does not itself authorize** client/Host execution.
- The admitted Host owns protected operations; FountainStore provides durable evidence. A UI status is not an operation receipt.
- The Ubuntu Mac mini's observed `fcis-access-staging` is a read-only snapshot, not the Hetzner production issuer. Do not infer their credential equality.

The design anchor is `Fountain-Coach/fountain-press/docs/access-passkey-first-owner-signin-2026-11-12.md`. Read owning `AGENTS.md`, `PLANS.md`, production source provenance and exact scenario before editing.

## Repeatable procedure

1. **Inspect current identity and actual failure.** Inspect issuer metadata, running Host adapter, published Access JS, credential *metadata only*, current source SHA and current authorization; do not request, dump, paste, log, display or commit any password, Basic header, signing key, bearer/refresh token, passkey secret or SSH private key. Do not reset user credentials or disturb the existing ChatGPT grant.
2. **Bind the existing owner.** Register passkeys only following an independently verified owner action, associating the WebAuthn credential with the existing issuer subject; do not invent a second account, local permission store or login domain.
3. **Use vetted WebAuthn/FIDO2 verification.** On the issuer's chosen HTTPS origin, require fresh unpredictable challenge, correct Relying Party ID, origin, credential public key/signature, user verification, expiration, replay resistance, and rate limiting. Verify `access` vs `fcis` origins explicitly, default to an issuer-hosted top-level ceremony and avoid homemade authentication crypto.
4. **Preserve OAuth.** Apply [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html), exact registered redirect URIs, authorization-code + PKCE S256, resource audiences, bounded consent, existing signing/grant/refresh continuity and denial after revocation. Never turn human login into automatic Host power.
5. **Select secure browser sessions.** Follow [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017.html); evaluate a same-origin backend-for-frontend that holds OAuth tokens server-side and issues an opaque Secure/HttpOnly/SameSite cookie. Require CSRF defense, timeouts, logout, reauth/step-up, and negative browser-origin tests. A session cache is not another authority. Never put credentials or grants into static Press content or localStorage.
6. **Establish independent recovery.** Enroll a second usable authenticator with recent owner verification, revoke lost devices, prove second-device login and define a reviewed lost-all-device procedure. Keep existing Basic fallback controlled and audited during migration; retire it only after replacement and recovery are independently accepted. No unverified email/SMS shortcut.
7. **Implement in bounded source-owning slices.** Host/Kit own the verifier and authority; Press owns the user interface; Host/Store own effect receipts. Do not invent a second service, new `mcp.fountain.coach` front end or dead UI controls.
8. **Run the acceptance matrix.** Verify isolated WebAuthn wrong origin/RP/challenge/key/UV/replay denial, cookie/CSRF/logout/expiry tests, *physical* iPad Safari and Mac sign-in, accessibility, second-factor recovery, existing ChatGPT `host.describe`, and distinct disposable-client revoke -> refresh denied -> real MCP denied -> Store receipt. Simulated iPad viewports support but do not replace native testing.

## Internal FCIS OpenAPI maintenance

For an internal FCIS owner API change, OpenAPI drift, newly admitted Host endpoint, grant/machine response, or question about the published fleet API, follow [the FCIS OpenAPI maintenance protocol](references/openapi-maintenance.md). It maintains `midi2-gpu-fabric/apps/estate-publisher/contracts/fcis-owner.openapi.json` and the **existing** Swift issuer, machine Store, Host response and Fountain Press consumer in one source-addressed contract. Require the checked-in Node source-drift gate and native Swift handler-response conformance; keep documentation, implementation, signed issuer/Caddy release and iPad acceptance **distinct**. The internal 3.1 contract is FCIS-owned and must not be confused with an external provider's official OpenAPI dependency. No new API authority, runtime Kit, operation, second Skill or plugin is created by this procedure.

## Reporting and maintenance

Use [the acceptance matrix](references/acceptance.md) to report source revision, owner/issuer/Host binding, exact tested behavior, negative tests, real-device evidence and next missing gate. Unknown is **NOT_ESTABLISHED**, not a manufactured outage. A Git commit, HTTPS 200, or Press badge never proves deployed passkeys.

This is an **agent procedure**, not a new Kit, OIDC provider or account system. Maintain only in `Fountain-Coach/.github/.codex/skills/fcis-owner-access`; release via the single GitHub-backed Fountain Coach FCIS plugin under [Governance 160](https://governance.fountain.coach/chapters/160-skill-sovereignty-and-governed-distribution/), protected PR, SHA-256 file-tree verification, and independent hosted version/selection readback. **No skill.zip, duplicate plugin or standalone personal Skill.**
