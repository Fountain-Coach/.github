# FCIS — Founding Experience and Console Study

**Owner:** Fountain Coach
**Date:** 24 November 2026
**Status:** Owner-directed design study; proposed UX targets, not deployed functionality or a new execution gate.
**Authority:** [FCIS Stack](../FCIS-STACK.md), [active owner-independence plan](../PLANS.md), [Goal Fidelity and Non-Invention](FCIS-Non-Invention-and-Goal-Fidelity.md).
**Purpose:** Turn our experience of founding and operating FCIS into the experience of its first customer.

## 1. Why this study exists

Fountain Coach is establishing a commercial, provider-neutral instruction and capability system whose customers retain authority over their working knowledge. The founder is also its first customer; these two roles must remain distinct.

Our own use exposed an important distinction: a technically verified service is not necessarily an operable product. Repeated passkey and return-navigation difficulties, ambiguous feedback, and repeated agent/operator handoffs made ordinary owner tasks unnecessarily difficult. A successful backend release alone did not establish a usable owner journey. We also experienced inconsistent provider-side installation inventories; this is evidence of an unverified distribution surface, not a finding of unauthorized access.

The original Fountain Press interface expresses our editorial identity, but reading and operating are different activities. Reading needs continuity, typography and reflection. Operating needs orientation, persistent object selection, predictable actions, timely feedback, and intelligible recovery. The console must not require customers to learn the implementation in order to use the product.

**Founding principle:** The interface shall make the owner's or customer's actual authority legible and usable, without becoming an additional authority. A customer pays for services, not for surrendering ownership of their knowledge.

### Verified starting point

- [Runtime PR 201](https://github.com/Fountain-Coach/midi2-gpu-fabric/pull/201#issuecomment-7128195925): FCIS-GO 0.1.40 signed release admitted to the existing native FountainStore; exact release bytes read back, sequence 1 to 2; provider installation was not inspected.
- [Runtime PR 202](https://github.com/Fountain-Coach/midi2-gpu-fabric/pull/202#issuecomment-7128464075): corrected passkey return deployed and physical iPad sign-in confirmed by owner; live assertion/session telemetry and Store sequence 4 independently read back.
- The existing single published FCIS-GO Skill and nine source-maintained historical Skills remain the bounded inventory. Independent read/inspection and signed admission are established; a full console-based edit/promote/restore lifecycle and complete independent operation/recovery are not yet established. Do not claim that production payment, customer onboarding, or provider reconciliation has been accepted.

## 2. Comparative study

Study actual task journeys rather than copy appearances. Record the reference product, date, surface/device, steps, feedback, recovery path and relevance to FCIS. Separate observations from proposed FCIS choices. Product documentation and screenshots are starting material, not proof of our implementation.

| Reference | Study question | Transferable design hypothesis |
| --- | --- | --- |
| [Tailscale administration](https://tailscale.com/docs/manage) | How does a person inspect machines, identities, access and policy without reasoning about the transport? | Object-centred control plane; clear membership and scoped authority |
| [Linear](https://linear.app/now/behind-the-latest-design-refresh) | How do consistent navigation, density, selection and restrained actions support daily work? | Quiet, fast, coherent workspace; progressive disclosure |
| [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) | How do passkeys, adaptive navigation, system gestures, accessibility and confirmation feel on iPad? | Native-feeling browser interaction, meaningful focus, predictable return and fewer steps |
| [GitHub releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) | How are draft, review, immutable version, provenance and restoration distinguished? | Versioned lifecycle with explicit promotion; Git details remain available but need not dominate customer UX |
| [Stripe Checkout](https://docs.stripe.com/payments/checkout) and [customer portal](https://docs.stripe.com/customer-management) | How do price, checkout, billing state, invoices, cancellation, failure and refund become understandable? | Hosted payment entry initially, coherent commercial state in FCIS, explicit reconciliation |

Use the current working Press UI as the before-study baseline. Capture ordinary task steps and pain points with the owner on physical iPad; use desktop and narrow/mobile browser layouts for comparison. Never record actual credentials, payment details, session tokens or private customer content in study artifacts.

## 3. Proposed experience: the FCIS Console

Investigate an adaptive, object-centred operating environment, retaining the existing Go service, issuer, owner identity, grants, native Store and instrument contracts. Fountain Press remains the reading and publication environment and a place to explain the system. Preserve the brand without forcing book pagination or editorial navigation onto operating tasks.

Proposed navigation: Overview, Skills, Instruments, Hosts, Access, Integrations; Account/Billing, Usage, Activity and Settings. Show only capabilities available to the current role. This is an information architecture hypothesis, not an endpoint list or permission grant. Do not create a second identity, Store, control plane, payment authority, or marketplace as a consequence of the study. A separate customer-facing workspace is a design question, not an implementation prerequisite.

Selection stays stable on navigation, refresh and return from authentication or external payment when the selected object is still accessible. Each object has its own meaningful context, actions, evidence and history. Show unavailable, unverified, pending, denied, failed and completed states accurately. Make the smallest necessary action discoverable; don't ask customers to reload or inspect server logs to discover outcomes. Use accessible semantics, keyboard and touch navigation, clear focus and responsive layouts; verify real iPad use rather than assume virtual browser parity.

### 3.1 Selected implementation stack — owner decision, 24 November 2026

Use **Vite + React + TypeScript** for the proposed FCIS Console. This is the selected implementation direction for the experience study, not a claim that React is already deployed. Preserve the existing native Go runtime and all admitted authority.

| Layer | Selected technology / responsibility |
| --- | --- |
| Build | Vite, producing a static production bundle |
| Interface | React and TypeScript |
| Design language | Fountain Coach CSS design tokens, semantic HTML and adaptive layouts; study-derived components rather than a mandatory third-party design system |
| Navigation | React Router; stable object routes, selection and safe return after authentication or checkout |
| Server state | TanStack Query; authoritative reads, bounded refresh and mutation-result reconciliation |
| HTTP bindings | TypeScript bindings generated from the peer canonical FCIS-OPENAPI.json; unavailable operations remain unavailable |
| Human authentication | Browser WebAuthn and existing FCIS Go owner sessions; no frontend token store or additional identity provider |
| Runtime and persistence | Existing FCIS Go and native FountainStore; the browser is not an authority |
| Payment | Provider-neutral FCIS Payment Instrument, with Stripe as the first adapter, subject to section 4 |
| Browser acceptance | Playwright for new console journeys (including WebKit), accessibility checks and actual physical iPad Safari acceptance; preserve existing regression evidence |

**Deployment shape:** build the frontend as static assets, embed the verified bundle in the Go executable using Go's existing embedded-asset approach, and serve it from the existing same-origin HTTPS management surface. Node.js and package tooling are build-time dependencies only. No separate Node server, Next.js/SSR, external CDN, additional runtime deployment service or second authentication system is required. An installed standalone FCIS executable must remain independently operable without a package registry, GitHub, ChatGPT or Stripe access for core owner operations.

Pin dependency versions and the lockfile when implementation begins. Tie the static build and API bindings to the reviewed source revision and retain the existing immutable Go release/rollback path. Keep assets cacheable by content identity while session-dependent responses remain private and non-cacheable. The Go service continues to enforce authorization, origin/intent checks, Secure HttpOnly sessions and actual Store effects. Client navigation or cached data cannot grant authority; a failed or unknown mutation is not a completed operation. Preserve the accepted passkey gesture and return semantics, including direct Skills navigation, and never expose tokens, card data or private Store records in static assets.

Use the existing Press implementation as the working baseline until a bounded console replacement passes acceptance; do not interrupt the accepted owner path or expand the P0 definition of done. Start the design prototype with the authenticated single FCIS-GO inventory and its account context, not invented API operations or fake payment success. Study the commercial journey now; enable actual test-mode payment only within the separate priority-two scope. This decision selects the tools and deployment boundary; it does not authorize production replacement or new paid services by itself.

## 4. Commercial experience

Payment is a first-class subject of the design study now, not an additional blocker for the already defined P0 owner-operation/recovery milestone. Runtime payment remains priority two under [FCIS Stack §9](../FCIS-STACK.md#9-future-commercial-capability--priority-two).

Separate platform subscription/licence, individually licensed or metered instrument services, and separately selected/billed model inference. These are candidate commercial relationships, not adopted prices or compulsory charging rules. A Skill is an instruction artifact, not an automatic billable event. Do not assume deterministic operations require paid inference or that buying a product grants arbitrary execution rights.

Use the existing proposed provider-neutral FCIS Payment Instrument, with Stripe as its first adapter, not payment code embedded in OAuth or the frontend. Investigate hosted Checkout and customer portal, explicit product/price/account/consent, invoice and receipt readback, spend limits, cancellations and approved refunds. Provider events must be authenticated and reconciled idempotently to durable FountainStore receipts. A success redirect is never payment proof. Commercial entitlement and scoped execution grants are separate decisions; buying a service cannot silently grant broad Host permissions. Preserve customer-owned knowledge and an appropriate export/retrieval path after cancellation, independent of access to paid services.

Keep test and live environments visibly distinct. No live customer charging, card collection by FCIS, pricing commitment, subscription creation, provider account change, or real money movement is authorized by this study. Review applicable EU/German commercial, tax, consumer, privacy, accessibility and payment requirements in the existing applicability register before any corresponding commercial launch; distinguish actual obligations from hypotheses.

## 5. Study journeys and proposed acceptance

Use exactly one Skill, FCIS-GO, to learn and demonstrate the management experience before expanding the inventory. Measure real task completion, number of explicit actions and avoidable reauthentication, time to usable state, navigation/selection continuity, and whether the customer can tell the verified outcome without agent assistance. Baseline measurements are pending; no numerical performance claim is made.

| Journey | Observable target | Evidence |
| --- | --- | --- |
| Return sign-in | One passkey gesture once ready; intended workspace/object opens directly; intelligible refusal and recovery | Actual physical iPad, issuer and Store readback |
| Inspect FCIS-GO | Select the Skill; active release, version, provenance and provider distribution state are readable without Git or manual refresh | Existing Store-backed inventory and owner observation |
| Edit/review/release | Inspect source, make a bounded draft change, compare changes, explicitly promote a verified version | Existing canonical authority, signed revision and independent active readback; no promotion on failed review |
| Restore | Select an accepted earlier release and explicitly restore it without resurrecting revoked access or rewriting history | Independent release and Store evidence, not just UI |
| Host and access | Select a Host/capability or client; see actual scoped authority; one authorized deterministic operation and one refused/revoked operation | Existing P0 execution and denial receipts, real owner-visible result |
| Activity and recovery | Identify what happened, what did not happen, and the available next action, without deciphering backend internals | Typed receipts, redacted operational evidence and real usability observation |
| Commercial test journey | Clearly priced test purchase, verified payment status, bounded entitlement, invoice/receipt, cancellation or approved test refund; duplicate/failure states understandable | Stripe test-mode evidence plus verified Store reconciliation; no live charges |
| Knowledge continuity | Understand and exercise permitted retrieval/export and cancellation boundaries | Existing/proposed knowledge custody contract, independently witnessed where implemented |

No target is considered accepted by a mockup or source test alone. A UX defect warrants a bounded source-owned correction, not a general architecture program. The current P0 DoD remains fixed; study targets for later management/payment are distinct.

## 6. Study sequence and finite deliverables

1. **Observe:** document the actual owner experience and baseline the reference journeys. Keep a concise comparison with concrete transferable findings and known tradeoffs.
2. **Compose:** test a cohesive console information architecture and adaptive layouts, starting with the signed FCIS-GO object and account/billing context. Record rejected alternatives and why.
3. **Validate:** run the relevant owner journeys against existing backend contracts. Distinguish visual prototypes, source implementation, isolated tests, production evidence and physical use.
4. **Decide:** produce a reviewed design direction, prioritized bounded implementation slices, and separate later commercial test acceptance. Keep the owner-independence DoD intact and update the active plan in place.

The study is pinned when this source is reviewed, cross-linked from the canonical stack and active plan, and available at its stable Git path. Completion of the study itself means a reviewed comparison, an explicit UX direction and a finite set of evidence-based journeys, not delivery of every proposed feature. Do not expand the active Skill inventory or publish a new plugin, website, or governance chapter merely to record this study.

## 7. Open questions

- What is the simplest customer-visible distinction between owning a workspace, licensing an instrument and allowing an operation?
- Which state belongs in the main object view, and which belongs in its activity or history?
- How does the console convey actual availability and refusal without making the customer act as the administrator of its infrastructure?
- Which pricing and cancellation model best supports independent customer knowledge ownership?
- Which existing Go and Press components already meet the proposed UX, and which genuinely fail observed journeys?

Keep the study here as the single working source. Later public editorial exposition in Fountain Press may reference the reviewed conclusions; it must not become a competing operational specification.
