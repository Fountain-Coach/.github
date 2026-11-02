# Exact-blocker continuity — preserve the original goal, not the failed route

**Trigger:** A writer asks to stop, resume later, or elevate learnings from a capability attempt that has not reached its original-path terminal success. Apply to provider login, paid-entitlement checks, remote tool invocation, physical-device acceptance and other governed tasks. This is a **procedural lesson**, not a runtime FCIS instrument.

## One durable handoff, no invented prerequisites

Use the existing owning project's active `PLANS.md` phase and its source-addressed acceptance record. Keep this compact handoff:

1. **Goal:** Restate the exact user-visible result and exclusions (platforms, private/public, billing, provider, tool, storage). Do not change it to an easier proxy.
2. **Owning implementation:** Repository, pinned main/source revision, authoritative runtime files and previously accepted scenario/operation IDs. Identify the actual user-facing surface separately from auxiliary test tools.
3. **Last verified point:** Each real operation, exact command or typed invocation, environment/device, observed response and immutable evidence address. Separate `PROVEN` terminal success, `OBSERVED` intermediate event, `DOCUMENTED` policy and `NOT_ESTABLISHED`.
4. **Exact blocker, if any:** Name the requested original-path operation, the **specific attempt that failed**, its returned failure, the applicable binding rule, and the smallest correction to make that same attempt possible. Scope the blocker to that operation. A compiler- or remote-tool refusal may block a particular probe without proving a provider-entitlement denial. If no provider authorization was attempted, label eligibility `NOT_ESTABLISHED`, not `BLOCKED_ACCESS_DENIED`.
5. **Next executable action:** A single source-grounded action that resumes the first unmet acceptance predicate. List the original-path positive terminal event and negative conditions. Do not ask the writer to reauthorize decisions already made; require their interaction only at actual credential/consent gates.
6. **Skill-learning classification:** Use an already existing canonical FCIS Skill when a rule is transferable. An independently accepted scenario can use `auto_elevate.py` after full Store/AX/window evidence and status reconciliation. A blocked/unexecuted scenario has **no accepted terminal witness**: keep an evidence-addressed proposal non-admitted. An explicit writer instruction may justify an ordinary reviewed canonical instruction update for accurate reporting/continuation; name it as **source-reviewed procedural guidance**, never `auto-elevated success`.

## Specific Reframe subscription example (2 November 2026)

**Original goal:** The private native Reframe Composer on macOS and physical iPad uses the writer's existing ChatGPT subscription for a real streamed reply. No Codex app-server, no OpenAI API key, no silent paid fallback, no open-source conversion, or mandatory paid desktop relay. The iPad app is the product's primary surface, not a ChatGPT web client.

**Owning source:** `Fountain-Coach/midi2-gpu-fabric` (not the `Fountain-Coach/Reframe` product bootstrap). Earlier accepted *Mac tool* work D03/D04 is not ChatGPT *model inference*. See merged [PR #96](https://github.com/Fountain-Coach/midi2-gpu-fabric/pull/96) and [PR #97](https://github.com/Fountain-Coach/midi2-gpu-fabric/pull/97), plus `docs/acceptance/2026-11-02-chatgpt-plan-provider-preflight.md` in the owning repository.

**Observed:** macOS `ReframeLLMClient.swift` uses an API-key configuration; native iPad R38 `R38PrivateComposerSession.swift` uses CodexKit; `ReframeCorePortable` supports macOS and iOS. The physical iPad was later `available (paired)` in `xcrun devicectl list devices`. An isolated Mac Swift OAuth probe passed `swiftc -typecheck -parse-as-library`. An attempt to use Remote Desktop Commander to produce that probe executable was explicitly refused by the remote tool's security checks. Consequently, **no OpenAI sign-in callback**, OAuth grant inspection, or completed streamed response was recorded. The scratch probe was not committed or installed as a product.

**Exact classification:** `BLOCKED_TOOL_EXECUTION` for that one standalone probe's executable-production attempt. `NOT_ESTABLISHED` for selected-private-client registration, this ChatGPT workspace's eligibility and grant of `chatgpt.tokens.use.direct`, and `NOT_ESTABLISHED` for inference on either Reframe platform. The policy distinction open-source versus selected private clients is **DOCUMENTED** (upstream), not a reproduced denial for this account.

**Next:** Resume the existing governed native provider route; resolve the local test-tool execution limitation by a supported path, **not a bypass**. Initiate legitimate provider authorization for the private Reframe client, with writer-controlled browser consent; validate issued client, signed identity and actually granted scope. Only after grant, run one `store:false`, `stream:true` Responses call and witness `response.completed` with native GUI and persisted execution evidence on **each** host. If OpenAI actually returns `access_denied`, unsupported-client or unsupported-workspace, record the exact provider response against the corresponding attempt. Never substitute Codex or a billed key.

## Regression checks

- A missing sign-in attempt or absent receipt MUST stay `NOT_ESTABLISHED`; no imaginary provider refusal.
- A refusal from an intermediary tool MUST carry that intermediary and failed command; it cannot be expanded into an OpenAI rejection.
- Mac accepted MCP tool execution MUST NOT be counted as subscription-backed native iPad or Mac inference.
- Source typechecking, simulation, pairing, a documentation PR, or a Skill update MUST NOT satisfy real provider auth or native UI/Store acceptance.
- A blocked scenario MUST NOT invoke scenario `auto_elevate.py` or mutate an installed/active ChatGPT Skill without the corresponding independent authority.
- The handoff MUST identify the single earliest unpassed original-path test, with exact resumption source and unchanged no-Codex/no-API-key/no-fallback constraints.
