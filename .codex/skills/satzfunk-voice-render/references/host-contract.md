# Satzfunk voice rendering — verified host and publication boundary

## Current provider path

**Source owner:** `Fountain-Coach/Satzfunk`, `src/openai-realtime-voice.mjs`, `scripts/vergil-realtime-audition.mjs`, `corpora/vergil/british-vergil-audition-01.txt` and its direction file. This replaces the deprecated `/audio/speech` workflow for **new** British Vergil recordings. The Realtime model for the 1 November 2026 audition is `gpt-realtime-2.1-mini`, via WebSocket `/v1/realtime`. Its original author-approved voice passage was extracted from the canonical [Vergil voice specification](../../linotype-estate-template/references/vergil-voice.md).

**Credential host:** existing authorized macOS Reframe/StageNative Keychain entries, accessed inside the source-owned Node process without logging a token. The declared references remain:

- service `Reframe`, account `modernization.settings.openaiApiKey`;
- service `com.fountain-coach.stage-native`, account `openai.apiKey`.

Do not invent a new key, shell interpolation, delegated user setup, browser request, dependency repository, or keychain export. The exact running script was acceptance-tested on the existing Mac. A fake WebSocket event sequence covers the unit tests without touching Keychain.

## Pinned official provider interface

The source-owned Realtime adapter must pass the [FCIS Official OpenAPI dependency](../../../../docs/FCIS-Official-OpenAPI-Dependency.md). Its provider contract is pinned to `openai/openai-openapi` commit `c2aecc2fbe1ddff3e7500a0eaa5c2bc4c19c5318`, `openapi.json` SHA-256 `d80bb28992f6c2a86876d866dcae0b1f15e130de94238592bc57a4a579448b5f`. The 68-schema unchanged transitive projection, source-generated event fixtures and exact request builders must validate through the Satzfunk owner-native `npm run contract:check`. Two *upstream* anomalies have narrowly reviewed exceptions (`conversation: "none"` overlapping `oneOf`; official `response.done` nullable status details). Neither is a reason to invent a second provider client or claim a successful sounding British male voice.

## Source and one-attempt evidence

Initial private literary audition, 1 November 2026: the original 554-character excerpt beginning **“The first drawing shows a room”**, source SHA-256 `447d628b03e6b72ac0ba8d815b9a2086dd19172ead869c0f898e7cefb96f1a08`. Provider `gpt-realtime-2.1-mini`, preset `marin`, 34.2-second 24kHz mono PCM16 WAV, SHA-256 `0f6219c329e4dec9b46799c1a2b90b846340e6c3d23b8a008b5254d89f1790f6`. One paid attempt; immutable sanitized receipt; `verify` rechecks the stored bytes and source. The returned **model-generated output transcript** normalizes to the supplied excerpt but is not an independent acoustic transcription or an artistic voice verdict. British accent, characterization and exact audible coverage require additional listening judgement.

The previous `gpt-4o-mini-tts`/`cedar` “On Continuity” WAV and receipts remain **historical, unapproved** evidence. The dated Speech API was deprecated on 1 October 2026 for shutdown on 6 January 2027. Do not issue new paid requests using it. Do not substitute the model identifier in the old `/audio/speech` route: the replacement uses Realtime events.

## Private Linotype boundary

Satzfunk owns the private WAV master; Linotype owns pagination and source-bound SatzfunkPlayer integration. The existing native owner-WLAN staging inspector **refuses unadmitted WAV**. For author audition, retain a SHA-256-checked MP3 listening derivative and stage it only in an immutable owner-WLAN candidate after native inspector acceptance, preserving the prior active release and rollback.

The initially staged v111 Cedar reading was rejected artistically and removed; v109 source/reader were restored. The separately staged v112 `shared-shell-20261101-v112-vergil-realtime-audition` is the **unchanged v109 reader plus a private 34.2-second MP3 listening candidate**, SHA-256 `14eea06150dd16ffa604d7267178761c85970206c8a89b2248c40b9545ff36ef`. Native inspector and HTTPS readback returned success. The reader has **no accepted Vergil Read Aloud control**; no public release or physical iPad/VoiceOver claim follows.

Only an author-heard, author-approved full exact-text recording may be admitted into the Linotype book after its source rights and playback acceptance. Keep the literary narrator identity separate from provider/model/voice preset.
