# Owner-controlled WLAN staging

Use this path only for staging explicitly scoped to the owner's WLAN or intranet. It is a disposable preview, not a production publication.

## Goal

Stage the current admitted estate bytes with correct host-root semantics, iPad accessibility, and the secure browser capabilities the application needs.

## Fountain Press staging acceptance for books and editions

The canonical WLAN release serves the **same Fountain Press source-bound edition and original Linotype Reader** intended for any later authorized public production. The staging identity is read from the current estate registry and actual active service/symlink, never from a hard-coded v162 label or an old screenshot. For an admitted book, pin the original owner SHA, complete contents/statuses, rights, artwork and links; pin the Press compositor revision and manifest. Derive an immutable candidate from the accepted active predecessor with a declared route/asset diff; preserve private media and unrelated routes byte-for-byte. Use the existing stage's authorized source-lock/digest guard, authenticated SSH/rsync delivery, atomic activation and rollback. Do not publish through an arbitrary alternate page server.

Independently verify the active symlink, HTTPS-served HTML/JS/receipt digests, existing Reader navigation and original source identities. Exercise the entire corpus when full-book completeness is the stated goal; record exact missing items rather than substituting a sampler. A 6 November 2026 accepted **Governance v162** witness comprised 160/160 chapters, 72 current/88 reference, 70 original figures, 1,132/1,132 author links, 160/160 browser compositions and 10 focused Reader journeys; original stage lineage v161/v160 remained rollback-ready. Those counts describe *one edition*, not mandatory global fixtures. Physical iPad Safari/VoiceOver acceptance and public production release each demand their own observed evidence.

On successful stage acceptance, hand off the exact source-pinned Press release identity and artifact inventory to the **existing EstatePublisher production lane**; do not install a second compositor, copy stage-private assets into a public artifact, or treat staging as an authorization to release. If a public route has different asset hosts, declare and verify the transformation rather than silently rebuilding the work.

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
