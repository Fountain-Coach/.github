---
name: fcis-console-development
description: Design, implement, test and release the Fountain Coach FCIS Console using Vite, React, TypeScript and its existing Go runtime. Use for frontend design, UX evaluation, responsive layouts, navigation, passkey return, Skills and Hosts views, access and activity, billing and usage design, component development, browser acceptance and embedded asset integration. Preserve canonical API and owner authority; demonstrate the actual customer journey rather than merely delivering UI code.
---

# FCIS Console Development

## Resolve the work before changing source

Read the current Fountain-Coach/.github `AGENTS.md`, active `PLANS.md`, `docs/FCIS-Non-Invention-and-Goal-Fidelity.md` and `docs/FCIS-Founding-Experience-and-Console-Study.md` (especially section 3.1). Read the owning implementation repository's `AGENTS.md`, `PLANS.md` and applicable contracts. Use the existing FCIS-GO route for owner work; consult canonical owner-access and Go migration procedures for their respective boundaries. Do not treat a source Skill as an execution grant or assume it is installed by a provider.

Identify the requested journey, current verified UI/runtime, applicable role, existing routes and finite observable success. Use the actual FCIS Go module in `Fountain-Coach/midi2-gpu-fabric/apps/estate-publisher/fcis-go-native` unless its owning source has changed. Inspect the working implementation first. Preserve production and the already accepted passkey flow. Treat a design hypothesis or missing proof as such, not as a blocker requiring additional machinery.

## Compose the experience

- Start with the user's object and goal, not a catalogue of backend endpoints. Define the visible result, selection and action, feedback and recovery. Compare the real journey against Tailscale (control plane), Linear (coherence), Apple (adaptive interaction), GitHub (version lifecycle) and Stripe (commercial clarity); consult the founding study rather than inventing benchmark findings.
- Establish reusable CSS tokens, semantic primitives, navigation and object/detail composition before multiplying screens. Keep hierarchy, spacing, typography, focus, touch targets and controls consistent; use restrained progressive disclosure. Fountain Press remains the reading environment, not the interaction model for operating FCIS.
- Compose for physical iPad Safari first, then desktop and narrow screens. Preserve selection and safe deep-link return through navigation, refresh and sign-in. Show only meaningful actions, with loading, empty, pending, denied, failed, unknown and verified-complete states. Show the outcome without manual refresh, server-log inspection or repeated user confirmation.
- Start the initial Console with the actual single FCIS-GO inventory and account context. Keep proposed capabilities visibly distinct from admitted ones. Do not fabricate records, prices, permissions, successful execution or payment to make a screen look complete.

## Implement within the selected stack

- Use Vite, React, TypeScript, React Router and TanStack Query. Generate TypeScript HTTP bindings from the reviewed canonical `FCIS-OPENAPI.json`; verify actual handler availability before using a specified operation. Keep route/object identity in navigation and server truth in query state, not duplicated mutable global state. Reconcile mutations with authoritative reads and receipts; do not infer success from optimistic state or redirects.
- Reuse existing Go authentication, authorization, origin/intent checks, Secure HttpOnly sessions, native FountainStore and instrument contracts. Preserve the prepared WebAuthn challenge and native user-gesture invocation; verify actual protected readback before accepting sign-in and intended return. Keep tokens and private data out of static bundles and browser persistence. Distinguish authorization from display.
- Pin dependencies and lockfile; use the owning repository's reproducible build and review path. Build static production assets and embed them in the existing Go executable. Preserve same-origin HTTPS, content-addressed static caching and private non-cacheable session responses. Do not add a Node production server, Next.js/SSR, CDN, separate identity, Store or deployment service. A standalone executable must operate without package-registry or model-provider access.
- Design Billing and Usage with the other account surfaces. Payment remains the existing provider-neutral payment instrument with Stripe as first adapter, under the study's priority-two boundary. Distinguish paid service entitlement, scoped execution grants and model-provider spend. Use hosted checkout/customer portal and verified receipts when the payment scope is authorized; no live charges, card collection or new commercial authority from a UI task. Preserve customer knowledge ownership and permitted retrieval/export.

## Verify and deliver the journey

1. Baseline the existing journey and document the small intended improvement. Use a design prototype only when useful; label its data and limits. Do not replace the working path before the new bounded path is accepted.
2. Run repository-owned type checks, production build, focused component/contract tests and relevant existing Go regression tests. Verify generated API bindings against their source; preserve existing authorization and passkey regressions. Never introduce a broad new test gate unrelated to the requested outcome.
3. Exercise the built application served by Go, not just the Vite dev server. Use Playwright including WebKit for new journeys; check accessible roles, keyboard/focus, responsive layout, visible result, deep links, reload, refusal/error recovery and absence of unexpected external calls. Inspect rendered screenshots or visual evidence; tests and mock fixtures do not establish deployed UX. Use actual physical iPad Safari for the requested device acceptance; do not claim a virtual browser is that device.
4. Use existing signed immutable release and rollback procedures for separately authorized staging/production changes. Verify the served build and, for state-changing operations, the independent server/Store receipt. A browser redirect is not a session, payment or instrument receipt. Do not make the owner repeatedly perform debug gestures; investigate existing telemetry and evidence first.
5. Reconcile the existing plan in place: report source revision, scope, build/test result, actual route/device and visible outcome, evidence of real state when applicable, and only the exact unverified remaining action. Distinguish prototype, source accepted, isolated acceptance, deployed and live accepted. Stop at the requested result; keep other work separate.

## Boundary

This is an owner-authored development procedure. It does not expand the single published FCIS-GO marketplace Skill, admit an instrument, authorize a production replacement or change the existing P0 DoD. The founding study governs the chosen frontend direction; the current runtime contracts and actual evidence govern implementation and acceptance.
