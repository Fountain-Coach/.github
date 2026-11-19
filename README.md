# Fountain Coach — Organization source and FCIS architecture

This repository is the **canonical Git owner of Fountain Coach's organization-wide instruction contracts, agent Skills and FCIS architecture**. It is not a running FCIS server and does not publish the public Governance or Fountain Coach websites.

## Start here

| Authority | Canonical source | What it owns |
| --- | --- | --- |
| **FCIS whole-system specification** | [FCIS-SYSTEM.json](FCIS-SYSTEM.json) · [validation schema](FCIS-SYSTEM.schema.json) | Prerequisite-free FCIS composition: bootstrap, Go Store/vault, owner/customer, OAuth/MCP, Host/MIDI2, Skills/scenarios, frontend, generation coverage and deployment profiles |
| **FCIS standalone Go stack** | [FCIS-STACK.md](FCIS-STACK.md) | Architecture companion and security invariants; fresh-install independence and optional existing-instance adoption |
| **FCIS canonical HTTP OpenAPI** | [FCIS-OPENAPI.json](FCIS-OPENAPI.json) | Peer normative HTTP operations and wire schemas for the standalone Go target; all implementation/production statuses separately verified |
| **FCIS RFC 0001** | [Organization profile](profile/README.md) | The four independent layers: AGENTS, PLANS, Skills and MCP |
| **Behavioral law** | [AGENTS.md](AGENTS.md) | Organization agent invariants and instruction routing |
| **Active intents** | [PLANS.md](PLANS.md) | Source task history, actual state, evidence and next actions |
| **Goal Fidelity** | [Founding rule](docs/FCIS-Non-Invention-and-Goal-Fidelity.md) | Do not invent requirements or move an owner-controlled DoD |
| **Capabilities** | [FCIS-KIT standard](docs/FCIS-KIT-Standard.md) | Owned instrument contracts, mechanical constraints, release and proof |
| **External providers** | [Official OpenAPI policy](docs/FCIS-Official-OpenAPI-Dependency.md) | Source-pinned provider adapters, tests and example provenance |
| **Canonical Skills** | [`.codex/skills/`](.codex/skills/) | Reusable agent procedures, distributed through the existing Git-backed plugin |

### Current architecture priorities

**First:** Prerequisite-free standalone Go FCIS as defined in [FCIS-SYSTEM.json](FCIS-SYSTEM.json): zero prior FCIS state, private native Store/vault, single-use first-owner WebAuthn claim, OAuth/MCP, bundled Access UX, software Host and optional admitted machine/MIDI2 instruments. **Separately**, the existing `fcis.fountain.coach` installation may be adopted with identity, grants and custody preserved; this is not a first-install prerequisite.

**Second:** A separately admitted provider-neutral payment instrument with **Stripe as the first adapter**. Payment integration does not block FCIS Go cutover.

These are **architecture decisions**, not claims that the new Go service or payment instrument has been released. For authoritative whole-system scope and source coverage, read [FCIS-SYSTEM.json](FCIS-SYSTEM.json), then [FCIS-STACK.md](FCIS-STACK.md) and the peer [FCIS-OPENAPI.json](FCIS-OPENAPI.json). The JSON specification is still a normative candidate, not a generated binary, a passed test or a production release.

## Source-owning and consuming repositories

The stack specification [maps each source boundary](FCIS-STACK.md#10-source-ownership-and-top-down-navigation) without copying the specification into domain repositories. Primary source owners include [midi2-gpu-fabric](https://github.com/Fountain-Coach/midi2-gpu-fabric), [Fountain-Store](https://github.com/Fountain-Coach/Fountain-Store), [midi-backplane](https://github.com/Fountain-Coach/midi-backplane), [midi2](https://github.com/Fountain-Coach/midi2), [FountainAuthKit](https://github.com/Fountain-Coach/FountainAuthKit) and the enrolled-Host contracts. Consumer and publication boundaries remain owned by [Reframe](https://github.com/Fountain-Coach/Reframe), [Fountain Press](https://github.com/Fountain-Coach/fountain-press), [Fountain Coach public site](https://github.com/Fountain-Coach/fountain.coach) and [public Governance](https://github.com/Fountain-Coach/governance.fountain.coach).

## Maintenance contract

1. Change the architecture **only** in the canonical [FCIS-STACK.md](FCIS-STACK.md) through a reviewed Git PR. The RFC, security standards and domain protocol owners retain their separate normative authority.
2. When that change affects an actual interface or consuming obligation, update the affected source-owning repository's contract and its short README backlink. Never copy a second normative architecture into downstream README files.
3. Verify canonical links and the repository's required checks. Git source admission, installed plugins, admitted capabilities, published sites and live production must be accepted separately.
4. Keep **priority two** external payment work distinct from the already accepted **priority one** Go cutover DoD.

The organization's [canonical FCIS Skills](.codex/skills/) remain source-controlled in this repository. Their marketplace, agent or API projections are derived, not competing authorities.

**Maintenance:** HTTP paths, authentication and response shapes are changed in the organization-root `FCIS-OPENAPI.json`; legacy domain OpenAPI is a pinned predecessor/projection, not another writable source. Canonical Skills `fcis-owner-access` and `fcis-go-runtime-migration` govern changes and verification.
