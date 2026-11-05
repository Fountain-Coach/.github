# Owner-controlled WLAN staging

Use this path only for staging explicitly scoped to the owner's WLAN or intranet. It is a disposable preview, not a production publication.

## Goal

Stage the current admitted estate bytes with correct host-root semantics, iPad accessibility, and the secure browser capabilities the application needs.

## Procedure

- Prefer the simple staging path. Do not impose production SecretStore, approval, or publication ceremony on a disposable preview unless production-equivalent staging was explicitly requested.
- Use the Ubuntu Mac mini staging identity only when current host inspection confirms it. Preserve its stable staging IP and certificate identity rather than relying on a transient DHCP address.
- Drive acceptance in a browser and verify the capabilities the staged application actually uses.
- If Csound/WebAudio uses AudioWorklet, require HTTPS. Plain HTTP fails staging acceptance even if the page renders.

Keep the WLAN staging boundary explicit and separate from the public estate. Do not report staging evidence as production publication evidence.

## Resume an existing staged Reader

Read the source-owning Estate repository's `staging/environment.json`, `staging/ENVIRONMENT.md` and actual service/current symlink before naming the active release. The canonical author entrance is the registered `estate-shell-acceptance` service on the Ubuntu Mac mini; older IP/port examples or a registry's stale `observedRelease` are not live identity. Preserve the production-derived Reader provenance gate, source lock and immutable predecessor. A Skill update does not authorize a release switch.

The **last recorded 5 November 2026 checkpoint is v152**, `shared-shell-20261105-v152-editorial-archive-1609cb9`, Press source `1609cb909ae2f89b4b28223fe70c482638d6b854`, with v151 `shared-shell-20261105-v151-semantic-spread-17e32af` retained for rollback. The Reader root SHA-256 is `77f90b8db05a42700f727b4558f7e91a6406e2ae6bf25d59d953fa5ddae7b3d9`. The canonical [Linotype reference](https://github.com/Fountain-Coach/.github/blob/main/.codex/skills/linotype-estate-template/references/model-essay-spread-proofreading-and-archive.md) retains the full checkpoint and editorial findings. Treat this as recorded history until independently reread; never downgrade a newer release to match a Skill.

The recorded 35-work/105-case browser smoke pass is separate from full editorial proofreading, trusted physical iPad Safari/VoiceOver and source-aligned audio. v152 preserves the archived essay's direct routes while removing it from active promotion. Keep source-only generator follow-ups distinct from the already admitted immutable release; neither a source edit nor a Skill revision updates staging or public production.
