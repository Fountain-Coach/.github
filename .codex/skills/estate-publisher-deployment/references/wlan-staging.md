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
