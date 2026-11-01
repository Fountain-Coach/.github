---
name: satzfunk-voice-render
description: "Produce source-locked, privately auditioned literary voice recordings through the current Fountain Coach Satzfunk Realtime adapter and existing macOS Reframe/StageNative Keychain host. Use for British Vergil, Illustrating Inferno, Linotype Read Aloud, FCIS source-bound voice work, model deprecation migration and safe paid-render recovery. Requires actual code execution on an authorized connected Mac."
---

# Satzfunk Voice Render — current source-owned workflow

**Authority:** `Fountain-Coach/Satzfunk` owns the API adapter, source-bound audio receipts and private media. `Fountain-Coach/.github` owns this reusable agent Skill. Linotype owns book pagination and source-bound playback. No Skill creates a new runtime capability or grants publication rights.

**Required upstream OpenAPI dependency:** Read [FCIS Official OpenAPI dependency](../../../docs/FCIS-Official-OpenAPI-Dependency.md). Before any new paid request, check the source-owned Satzfunk `contracts/openai/realtime.lock.json` (immutable official OpenAI OpenAPI 3.1 revision and SHA-256), its unmodified 67-schema Realtime projection, `npm run contract:check`, and the actual outbound/inbound event validation in `src/openai-realtime-contract.mjs`. Use `node scripts/check-official-openapi.mjs --source <pinned-openapi.json>` for explicit upstream drift reviews. See source-owner [successful Realtime example](https://github.com/Fountain-Coach/Satzfunk/blob/main/docs/ai/2026-11-01-official-openapi-realtime-contract.md), preserving its distinction between genuine 34.2-second transport success and the rejected American female literary voice. Never replace the official schema with hand-written event JSON or treat a documented upstream compatibility exception as generic schema waiver.

## First choose the supported model and the approved literary voice

Consult [OpenAI's current deprecation schedule](https://developers.openai.com/api/docs/deprecations) before any paid recording. As of 1 November 2026, `gpt-4o-mini-tts`, `tts-1` and `tts-1-hd` are **deprecated** for January 6, 2027 shutdown; **do not generate new voice takes using `/audio/speech`**. OpenAI recommends `gpt-realtime-2.1-mini` via the Realtime API. This is an endpoint and event-protocol change, not a model-ID flag.

For British Vergil, read the canonical [literary voice specification](../linotype-estate-template/references/vergil-voice.md) **before** rendering. Vergil's character is independent of model and preset. Use an authored original audition passage, consistent natural British English and restrained literary direction. An existing preset (currently `marin`) is an **unaccepted candidate** even when the model transcript matches source text. If the accent/performance does not sound like Vergil, reject the result; do not present it as an edition.

## Repeatable host procedure

1. Inspect the current Satzfunk source, `AGENTS.md`, existing phase in `PLANS.md`, the written manuscript, voice directions and digest; use only an approved source revision. Read [the native host contract](references/host-contract.md).
2. On the connected authorized Mac, run the **owner-native** command `node scripts/vergil-realtime-audition.mjs plan` in the current Satzfunk Git checkout. It plans exactly one current-model short audition without calling the API. Do not use the obsolete bundled `record.mjs`, an improvised HTTP request or a copied token.
3. If the plan is source-exact and authorized, run `node scripts/vergil-realtime-audition.mjs render` **once**. The source-owned Node process retrieves the previously declared Keychain credential internally, writes an exclusive attempt receipt before the paid Realtime call, then saves a private PCM16 WAV and the model-generated text-evidence digest. No shell-secret interpolation, external microphone, voice cloning or automatic retry.
4. Run `node scripts/vergil-realtime-audition.mjs verify`. Check the source revision, output audio hash, PCM duration, completed response, terminal receipt and generated transcript comparison. A model-generated transcript is **not an independent transcript of the audible waveform**, and none of these measurements certifies accent, pacing or the literary character.
5. Prepare a separately hashed MP3 derivative **only for authorized owner-WLAN listening**. Keep the WAV master private in Satzfunk. The established staging inspector rejects unadmitted WAV files; do not weaken that rule. Validate an immutable candidate and preserved predecessor before activation; keep the unapproved audition separate from the Linotype reader. **No autoplay, separate transcript, public promotion or synthetic-voice impersonation.**
6. Report source, model, direction, audio and derivative SHA-256s; exact tests and host readback; artistically accepted/unaccepted status; staging and public state independently. Only a heard and author-approved full exact-text edition may be admitted into Linotype using SatzfunkPlayer.

## Fail closed

An unavailable model, Keychain, provider response, actual host, source digest or prior attempt is a precise blocker—not permission to silently switch to an obsolete model, browser TTS, a different voice or a fabricated file. An attempted paid render is never retried with the same identity. Preserve old FCIS `gpt-4o-mini-tts` recordings and receipts as historical evidence; their existence does not authorize continued deprecated generation or establish Vergil acceptance.

**Verified first use:** 1 November 2026: one 554-character original Vergil sample with `gpt-realtime-2.1-mini`/`marin`, 34.2-second private WAV, normalized model-generated transcript matching source. Artist's accent/performance judgement outstanding; rejected Cedar v111 removed from the active reader; private v112 offers only a listening derivative, not an approved book edition.
