---
name: fcis-owner-access
description: Govern and verify Fountain Coach owner identity, passkey-first WebAuthn sign-in, secure browser sessions, recovery, and OAuth client access for access.fountain.coach and fcis.fountain.coach. Use when auditing owner login, migrating from file-backed Basic passwords, enrolling passkeys, investigating lost-device recovery, administering scoped grants, or accepting Mac/iPad Access. Reuse FountainAuthKit, the existing Host and FountainStore authorities; require evidence instead of invented services or unproved release claims.
---

# FCIS Owner Access — Passkeys and Recovery

## Authority and observed baseline

Keep the user's goal: **normal owner sign-in and independent recovery without SSH, passwords copied from an Ubuntu machine, or a second identity system**. The Basic login and existing grant API work, but passkeys and recovery are **NOT YET IMPLEMENTED**. Separate DOCUMENTED, SOURCE-TESTED, STAGED and LIVE-ACCEPTED states.

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

## Reporting and maintenance

Use [the acceptance matrix](references/acceptance.md) to report source revision, owner/issuer/Host binding, exact tested behavior, negative tests, real-device evidence and next missing gate. Unknown is **NOT_ESTABLISHED**, not a manufactured outage. A Git commit, HTTPS 200, or Press badge never proves deployed passkeys.

This is an **agent procedure**, not a new Kit, OIDC provider or account system. Maintain only in `Fountain-Coach/.github/.codex/skills/fcis-owner-access`; release via the single GitHub-backed Fountain Coach FCIS plugin under [Governance 160](https://governance.fountain.coach/chapters/160-skill-sovereignty-and-governed-distribution/), protected PR, SHA-256 file-tree verification, and independent hosted version/selection readback. **No skill.zip, duplicate plugin or standalone personal Skill.**
