---
name: satzfunk-voice-render
description: "Produce and verify one exact-source narrated WAV with the existing Fountain Coach Satzfunk OpenAI speech adapter and macOS Reframe/StageNative Keychain credential, without exposing the key or improvising transport. Use for British Vergil, Illustrating Inferno, Linotype Read Aloud, FCIS speech readings, and repeated source-bound voice generation or failed paid-render retries. On a connected Mac, run the bundled deterministic plan/render/verify script; source authority, audition and staging remain separate. (requires code execution)"
---

# Satzfunk Voice Render — the proven host path

## Contract

Use the existing **Satzfunk** repository and its `src/openai-voice.mjs` adapter; do not write a new API HTTP client, inline `curl` command, or shell expression that reveals or exports a credential. Yesterday's accepted precedent is `Satzfunk/scripts/render-fcis-essay-readaloud.mjs` (31 October 2026): a Node process internally retrieves the Reframe/StageNative Keychain credential, uses `planSpeech`/`renderSpeech`, records an attempt before the paid request and prevents blind retries. Preserve the two declared Keychain services; never inspect, print, store or transport the key outside that process. A configured Mac Keychain is **not** a missing-user-permission problem.

Use [the bundled deterministic CLI](scripts/record.mjs). It imports the **existing** Satzfunk speech implementation at the selected checkout; the skill owns only preflight, receipts and verification. Read [host preparation and evidence](references/host-contract.md) before an actual render.

## Required execution

1. Resolve the approved, exact manuscript or source extraction. Obtain its **UTF-8 SHA-256** and stable work ID from the source owner; never paraphrase or use an adaptation. Resolve the actual macOS Satzfunk checkout and the recognized source revision. Reject a changed source digest.
2. Run `node <skill>/scripts/record.mjs plan --satzfunk-root <absolute-path> --source <absolute-text-file> --source-sha256 <64-hex> --work-id <slug> --voice cedar`. Default `cedar` is an **audition candidate**, not proof of a British accent. The bundled British Vergil instructions are exact, versioned input. Review its source hash, model, request count, output path and private status.
3. Execute **once**: run the same command with `render` in place of `plan`. The script creates an exclusive attempt receipt **before** Keychain access or paid synthesis; it retrieves the credential **inside** the Node process using the already-established macOS Keychain API call via `execFileSync`, and invokes the existing Satzfunk `renderSpeech`. Never pass `OPENAI_API_KEY=$(...)` in a shell command, print the secret or create a fallback browser-side speech request.
4. Run the same command with `verify`. It independently checks the source, actual generated WAV bytes, sample rate, PCM frames, duration, audio SHA-256 and attempt receipt. A file alone is not verified speech fidelity; the produced audio remains **private and artistically unreviewed** until a human audition.
5. Use existing Linotype and SatzfunkPlayer authority to attach the approved edition to a page only after the recording's source and rights match. Preserve page-frame pagination and existing source identities. Do not create a second transcript/player, invent word alignment, auto-play, or publish to production. Follow the canonical [Vergil voice specification](https://github.com/Fountain-Coach/.github/blob/main/.codex/skills/linotype-estate-template/references/vergil-voice.md).

## Hard refusals and recovery

- If host execution is unavailable or the security layer refuses a tool operation, **report that exact refusal**. Do not improvise a different credential transport, ask for a key, or claim a successful render. Tool permission errors are not Keychain errors.
- If no Keychain item is present or retrieval is denied, stop with a sanitized receipt; do not fall back to environment searches, clipboard, browser, custom API calls or an alternate synthetic voice.
- If a render failed **after recording its attempt**, never rerun blindly. Inspect `drafts/voice-editions/<id>/render-receipt.json` and the output WAV before separately deciding whether a fresh, explicitly authorized attempt identity is warranted. `verify` is safe and repeatable; `render` is not.
- Do not mark source-and-bytes verification as artistic acceptance, physical iPad/VoiceOver acceptance, published edition or a successful staging transition.

## Acceptance

Pass dry-run and negative tests before any paid call. For the real host, observe exactly one attempted request and one genuine WAV with matching SHA-256 and measured PCM duration, use the auditioned British-English voice or report that judgement as outstanding, and independently verify any requested staged playback in the existing page. Report source commit, source digest, audio digest, Mac host receipt, stage release and public state separately. No new service, key or author-managed setup is a prerequisite.