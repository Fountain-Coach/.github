# Existing host path, source owner, and staging handoff

The successful FCIS speech operation on 31 October 2026 is implemented by `Fountain-Coach/Satzfunk/scripts/render-fcis-essay-readaloud.mjs` and `src/openai-voice.mjs`.

It retrieves Keychain credentials **inside Node** using `/usr/bin/security find-generic-password -s <service> -a <account> -w` as a child process with captured, unlogged output. Declared references, in order:

- service `Reframe`, account `modernization.settings.openaiApiKey`
- service `com.fountain-coach.stage-native`, account `openai.apiKey`

The `src/openai-voice.mjs` owner supports `gpt-4o-mini-tts`, `wav` and the `cedar` or `marin` built-in presets. Its `renderSpeech` implementation requires the output to be inside the checkout's `drafts/` tree. The skill's CLI imports that module; it never implements OpenAI request transport itself.

For the initial v109 *On Continuity* British Vergil candidate, the verified source input contains ten authorial text blocks (title + paragraphs 1–9), 2,637 characters, source SHA-256 `fb57e1726c816497beed41a12504a276a7eeed8b9e1359e35ed07426c56f4b4c`. The active private v109 estate source was observed under `/home/benedikt/estate-shell-acceptance-staging/releases/shared-shell-20261101-v109-secondary-art-in-prose`. This snapshot identifies the work; always recheck the live source and the exact manuscript before rendering or staging. Bibliographical footnotes are not automatically spoken prose.

Two-stage responsibility: Satzfunk owns private, recorded media and receipt; the Linotype/SatzfunkPlayer integration owns private staged playback, source binding, transport continuity and accessible controls. The page is the frame. No separate transcript, Continuous mode, live browser generation, speculative cue timestamps or public promotion.

The CLI's `plan` operation creates an idempotent source plan, `render` attempts exactly once, and `verify` checks existing media. Explicit publication/rights approval and artistic audition remain independent of a successful audio file.
