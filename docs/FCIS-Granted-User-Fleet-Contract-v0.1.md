# FCIS granted-user Fleet contract — normative candidate v0.1

**Date:** 22 November 2026  
**Authority:** Fountain-Coach/.github → canonical FCIS OpenAPI / system contract, once separately reviewed  
**State:** SOURCE-DESIGN-CANDIDATE; not a live API, admitted member, deployed grant, or human-authorized release  
**Consumer:** existing Fountain Press Access origin and one shared Fleet interface with **owner** and **granted user** permission-scoped projections

## Goal and non-invention

The user wants the same Fleet Manager to work for the owner and people invited by the owner. A successful owner passkey is not another person's identity. A logged-in subject is not a member. A member has no machine permissions until an explicit owner-controlled grant and, where applicable, that user's consent.

The current **canonical FCIS-OPENAPI.json v0.4.0 has no admitted membership or granted-user Fleet endpoint**. Its owner machine inventory, Host inspection, pairing and issuer grant operations cannot be reused by replacing an `owner` URL segment or filtering the owner's JSON in JavaScript. The following identifiers are **proposals** for a later reviewed OpenAPI version; none shall be emitted as a production 200 or enabled as UI action before the issuer implements them.

### Four distinct authorities

1. **Human identity:** a separate subject, authenticated to the same issuer with its own credential/recovery policy; does not reuse the owner's passkey, session or provider token.
2. **Membership:** one active, issuer-Stored relation between owner/tenant and subject, with role, grantable scope, expiry, and explicit revocation. Invitation state is not membership.
3. **Effective capability grant:** verified resource+client+machine+operation+environment+expiry consent, narrower than both owner's authorized boundary and the Host's currently admitted manifest. A user can *discover* a machine without being permitted to *invoke* every capability.
4. **Execution/evidence:** the Host checks live grant and cryptographic peer identity on each typed operation; FountainStore holds accepted/refused/terminal record. MIDI2 transports lifecycle, not permission. A browser badge or discovery packet is not authorization.

## Proposed endpoints (not yet part of OpenAPI 0.4.0)

| Proposed operation | Method + path | Authority | Typed result and denial |
| --- | --- | --- | --- |
| List owner memberships and invitations | `GET /oauth/owner/members` | Verified owner session, exact accepted Origin | Redacted owner-scoped member records, pending/active/expired/revoked; never passkeys or tokens |
| Create a bounded invitation | `POST /oauth/owner/members/invite` | Fresh owner confirmation and intention, owner Store admission | Exact tenant/subject binding, expiry, requested role/scope and opaque one-use invitation ID; **no grant** |
| Accept or decline invitation | `POST /oauth/user/members/decide` | Separately authenticated invited subject; exact one-time invitation | Accepted membership or denied, with issuer Store receipt; wrong subject, used, expired or revoked invite refused |
| Grant bounded resource capability | `POST /oauth/owner/members/grants` | Owner fresh confirmation, issuer grant policy, verified enrolled Host | Bound subject/client/resource/Host/capability/environment/expiry; no SSH wildcard or fleet-wide implicit grant |
| Read effective user Fleet | `GET /oauth/user/hosts` | Independently authenticated member and effective current grants | Only discoverable resources; machine state and scoped read/write capability; **no owner-only inventory** |
| Revoke membership or delegated grant | `POST /oauth/owner/members/revoke` | Owner scope-specific approval, version precondition | Immutable revocation evidence, freshness and bounded refresh/access denial |
| Inspect one's active grants | `GET /oauth/user/grants` | Separate user session | Only current subject's capabilities and expiry, never another user's membership |
| Request additional capability | `POST /oauth/user/grants/request` | Authenticated user and issuer policy | Request pending owner action, never auto approval |

**These paths are proposed names, not yet part of a reviewed normative OpenAPI generation.** Their request/response schemas and error catalog must be authored in the source OpenAPI when implementing this slice; no new security authority or general shell/MIDI command vocabulary is authorized by this document.

## Machine-readable policy invariants for the future OpenAPI

Each membership record MUST bind: `tenantID`, `ownerSubjectReference`, `memberSubjectReference`, `role`, `status`, `invitationID`, `issuer`, `createdAt`, `expiresAt`, `authorizationEventID`, `policyRevision`, and typed current Store evidence. No public user identifier, private owner subject, contact address or invitation secret is exposed to unrelated parties.

Each grant MUST bind: `tenantID`, `subjectReference`, `clientID`, `resource`, `hostTargetID`, `operationID`, `environment`, `readOrMutation`, `expiresAt`, `issuerPolicyRevision`, `consentEventID`, and any distinct Host admission reference. Unknown/widened scope fails closed. A user cannot mutate owner Fleet, admit another Host, authorize another user, or see another member's resources merely by being a member.

**State machine:** `invited → invite-accepted → member-active → member-suspended/revoked/expired`, with `invite-denied` and `invite-expired` separate terminal outcomes. Machine states `provisioned`, `admitted`, `suspended`, `revoked` and `not-observed` are separate from membership state. An owner's revocation of a grant must invalidate its access/refresh families within a declared bound; paused/disconnected/replayed Host operation states remain distinguishable.

## Required negative acceptance

A two-subject/two-Host scenario MUST refuse wrong-subject invitation acceptance, replayed invite, expired invite, stolen provider cookie, cross-tenant listing, guessed Host IDs, non-member discovery, elevated read-to-write request, owner-only method from user session, operation with stale Host grant, wrong peer or Store, revoked token/refresh after restart, and duplicate event/transport replay. A valid owner->user grant must permit exactly its specified read operation on Host A, refuse Host B and mutation on A, then refuse both access and refresh after owner revocation. Independently witness issuer auth/refusal, admitted Host operation/refusal, native FountainStore receipt and browser AX state.

The required user-facing errors are distinct: `sign_in_required`, `membership_pending`, `membership_denied`, `grant_not_found`, `scope_denied`, `expired`, `revoked`, `host_not_admitted`, `host_not_observed`, `issuer_unavailable`, `operation_unverified`. These are **proposed application codes**, not yet current wire constants.

## Implementation order and exit gate

1. Keep existing owner passkey and Host authorization intact; implement source and real native Store owner Fleet read first ([Go PR #183](https://github.com/Fountain-Coach/midi2-gpu-fabric/pull/183)). This read does not enroll or authorize machines.
2. Extend canonical issuer OpenAPI with separately authenticated user subject and invitation/membership/effective-grant schemas; update generated source requirements, version, exact artifact pins and deterministic fixture consumers.
3. Implement issuer native Store invitation, acceptance, owner grant and revocation. Keep first owner identity independent; include restart and refusal tests before any browser action is enabled.
4. Implement user read-only projection only after effective grant policy is verified. Then extend existing Fountain Press Access with a role-derived user view and source-tested AX/visual coverage; do not duplicate private data into static HTML/JS.
5. Perform independently witnessed real Host operation, revocation and owner/user browser acceptance in a separate approved release. Preserve signed predecessor and rollback.

**Explicitly excluded now:** editing current OpenAPI without rebuilding the exact source pins, claiming live user sign-in, creating actual member identities or grants, deploying to a production issuer, issuing owner/agent signatures, presenting test fixtures as physical passkey approval, or treating owner MIDI2 observability as a blocking dependency of the user UX.
