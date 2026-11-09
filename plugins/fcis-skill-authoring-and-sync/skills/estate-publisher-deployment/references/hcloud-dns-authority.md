# Hetzner DNS through the installed hcloud CLI

Use this procedure for a specifically authorized Fountain Coach DNS hostname, such as `access.fountain.coach`. DNS and the website publication remain separate effects. **Observed on 9 November 2026:** `hcloud v1.70.1` supports `hcloud zone` and `hcloud zone rrset`; a separate curl-based token adapter is not inherently required. CLI ability is not proof that the selected Hetzner project owns the DNS zone.

## Discover the actual authority (read-only)

1. Inspect `hcloud version`, `hcloud context list`, and `hcloud context active` (never print config files or tokens).
2. Inspect `hcloud zone list` and `hcloud zone describe fountain.coach` in the selected context. Compare `dig +short NS fountain.coach` with the zone's actual delegated nameservers. A project containing the web server is not necessarily the project holding the DNS zone.
3. Only after the existing authoritative zone is visible, inspect `hcloud zone rrset list fountain.coach` and `hcloud zone rrset describe fountain.coach access A` for the intended relative record name and type. Verify existing record values and TTL before proposing any mutation. A missing RRset is not a missing zone.
4. Interpret `Zone not found` and an empty zone list narrowly: **the zone is not visible through this selected project/context**. They do not demonstrate that `hcloud` lacks DNS support, that Hetzner DNS is unavailable globally, or that the request was denied for insufficient permissions. A specific 401/403 or other explicit refused operation is required to claim that kind of denial. If no authorized context exposes the authoritative zone, report exact **PROJECT_SCOPE_UNVERIFIED** and the next action (identify/select the existing zone-owning authorized project), not a new API dependency.
5. Preserve an existing working `hcloud` authentication context. Do not add SecretStore, an extra bearer-token enrollment, a CLI replacement, or a different account merely because the chosen project has no zone. Do not read or echo credentials. Never create a duplicate `fountain.coach` zone to address `Zone not found`; zone creation/transfer/delegation is a distinct, separately authorized operation.

## Bounded DNS write (only after zone visibility and explicit exact-tuple authorization)

Confirm hostname, existing RRset, type, target, TTL, zone owner, and rollback before writing. For the *currently declared* `access.fountain.coach` tuple only (A → `65.109.14.71`, TTL 300), if the **authoritative zone is visible in the selected context** and the RRset is confirmed absent, the installed CLI supports:

```sh
hcloud zone rrset create --name access --type A --record 65.109.14.71 --ttl 300 fountain.coach
```

This is an example of the native write path, **not permission to execute it** on another project or domain. For an existing RRset, read and review its entire value set first: `hcloud zone rrset set-records` replaces all values and an empty value set deletes the RRset. Never treat it as an additive write. Independently inspect the RRset through `hcloud` and query the authoritative DNS nameservers and public resolvers after an authorized write. Do not claim live DNS from a successful command alone.

Only then separately validate Caddy host admission, configured root, active immutable release, HTTPS/TLS, required FCIS CORS, and protected owner API responses; a DNS change is not a deployed management interface. Keep the previous release and rollback available. If a stage and local browser tests pass while DNS is unresolved, classify as **staged**, not public.

## Evidence that motivated the correction

On 9 November 2026 the owner's Mac `fountainai` context listed server `65.109.14.71` but no DNS zones, and `hcloud zone describe fountain.coach` returned `Zone not found`. The parent `fountain.coach` has Hetzner-delegated nameservers, while `access.fountain.coach` had no A response. These observations establish CLI capability and the selected-context zone visibility gap; **they do not prove an external authorization refusal**. A different signed-in, authorized project may expose the zone; do not assume one exists until witnessed.
