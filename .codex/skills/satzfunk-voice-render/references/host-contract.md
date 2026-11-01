# Existing host path, source owner, and staging handoff

The successful FCIS speech operation on 31 October 2026 is implemented by `Fountain-Coach/Satzfunk/scripts/render-fcis-essay-readaloud.mjs` and `src/openai-voice.mjs`.

It retrieves Keychain credentials **inside Node** using `/usr/bin/security find-generic-password -s <service> -a <account> -w` as a child process with captured, unlogged output. Declared references, in order:

- service `Reframe`, account `modernization.settings.openaiApiKey`
- service `com.fountain-coach.stage-native`, account `openai.apiKey`

The `src/openai-voice.mjs` owner supports `gpt-4o-mini-tts`, `wav` and the `cedar` or `marin` built-in presets. Its `renderSpeech` implementation requires the output to be inside the checkout's `drafts/` tree. The skill's CLI imports that module; it never implements OpenAI request transport itself.

For the initial v109 *On Continuity* British Vergil candidate, the verified source input contains ten authorial text blocks (title + paragraphs 1–9), 2,637 characters, source SHA-256 `fb57e1726c816497beed41a12504a276a7eeed8b9e1359e35ed07426c56f4b4c`. The active private v109 estate source was observed under `/home/benedikt/estate-shell-acceptance-staging/releases/shared-shell-20261101-v109-secondary-art-in-prose`. This snapshot identifies the work; always recheck the live source and the exact manuscript before rendering or staging. Bibliographical footnotes are not automatically spoken prose.

Two-stage responsibility: Satzfunk owns private, recorded media and receipt; the Linotype/SatzfunkPlayer integration owns private staged playback, source binding, transport continuity and accessible controls. The page is the frame. No separate transcript, Continuous mode, live browser generation, speculative cue timestamps or public promotion.

The CLI's `plan` operation creates an idempotent source plan, `render` attempts exactly once, and `verify` checks existing media. Explicit publication/rights approval and artistic audition remain independent of a successful audio file.

## Verified private Linotype staging boundary — 1 November 2026

**Do not put the WAV master into the existing owner-WLAN preview root.** The actual `serve_shared_shell_preview.py` inspector refuses every WAV outside its narrowly admitted sound-study paths. The first immutable British Vergil candidate `v110` failed with `RuntimeError: WAV not allowed on preview`; the active stage was rolled back to v109 and HTTPS recovery witnessed. This is a real native policy, not a reason to weaken admission, provision a new service, or announce a missing credential.

Retain the source-locked WAV master and its SHA-256 in Satzfunk's private drafts. Create a separate, checksum-verified compatible **MP3 listening derivative** using the existing host encoder; record both master and derivative digests, encoding, complete text digest, permissions and audio disclosure in the private edition. Use the native preview inspector **against the complete candidate before changing the active symlink**, then validate exactly the changed files relative to the active immutable predecessor. Reuse the existing owner-WLAN HTTPS/SSH/staging service and keep the predecessor for immediate rollback. Never stage an unlisted media type or call derivative validation an artistic audition.

**Accepted witness:** the corrected `v111-british-vergil-mp3` candidate passed the native inspector, preserved 1,261 predecessor files, and served an MP3 derivative at SHA-256 `36c1f88c05e896fc1c2f509a898d2858dab1352fdff49d6b3f9f63660a241e40` from the independently verified WAV master `73e20acd6d063b420c33beb6eb8176a5069eba0949a233412a090c9783757168`. Browser preflight and then live HTTPS playback passed in Chrome and WebKit at landscape, portrait and phone sizes (six live profiles, zero errors/overflow). The actual code and proof are in `Fountain-Coach/fountain.coach` PR #4; this reference does not grant public release or claim physical iPad/VoiceOver or the author's vocal approval.
