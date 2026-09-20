# FCIS-KIT Standard (Owned Kits, Factoring and Release)

**Status:** Adopted
**Category:** Standards Track
**Applies to:** Fountain Coach org repositories that publish or consume Fountain Coach Swift packages
**Version:** 1.2.0

---

## 1. Purpose

Fountain Coach repositories depend mostly on packages the organization itself owns. Nothing in FCIS has governed
when a capability is factored into a kit, how that kit is released, or how a consumer moves to a new version. The
resulting drift is measurable rather than theoretical: in one consumer, three of five owned kits are pinned to raw
commits with no recorded reason, so a fix landing upstream stays invisible until somebody re-pins by hand.

A good practice already exists in the organization — a generic seam released upstream, consumed by version, with
the kit receiving none of the consumer's domain types — but it exists as one worked example rather than a rule,
which means it is followed when someone remembers it. A constraint also already exists in repository compliance
plans (*"no new dependencies"*) with nothing to enforce it and no stated procedure for the case it implies: that a
capability we lack is built in a kit we own.

FCIS-KIT makes both explicit. It governs factoring, versioning, release and consumption. It does not govern what a
kit should contain, which is a product question.

---

## 2. Terminology

- **Owned Kit**: a Swift package in a Fountain Coach organization repository, consumed by another repository.
- **Third-Party Dependency**: a package not owned by the organization.
- **Seam**: the generic capability an owned kit exposes. A seam is defined by what it does, never by who calls it.
- **Consumer**: a repository that depends on an owned kit.
- **Revision Pin**: a dependency expressed as a raw commit or branch instead of a version requirement.
- **In-Repo Module**: a package declared by a path inside the consuming repository. It is versioned by the
  repository that contains it and is not an owned kit for the purposes of this standard.
- **External Path Dependency**: a package declared by a path that resolves outside the consuming repository — a
  dependency on a checkout rather than on a release.
- **Counterpart Provenance**: the record, in the consumer, of the upstream tag or commit a change arrived from.
- **Mechanical Constraint**: an FCIS-declared condition represented in an executable contract and enforced by the
  owning kit. It has a typed identity/version, executable predicate, named evaluator, bounded refusal state, and
  terminal evidence requirement. It is not a prose instruction, prompt convention, screenshot, or inferred boundary.
- **Kit-Only Execution Authority**: the owning FCIS-KIT is the sole runtime authority for an admitted capability's
  mechanical constraints, execution, lifecycle, refusal, and terminal evidence. A consumer, CLI, scenario runner, or
  host adapter may not become an execution authority or fallback.

---

## 3. Compliance Requirements

The key words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are to be interpreted as described in RFC 2119.

### FCIS-KIT-01: Declaration
Repositories that publish or consume owned kits **MUST** declare them, and the consumption mode of each, using the
template in Section 4. The declaration **MUST** be discoverable in repository docs, not inferred from a manifest.

### FCIS-KIT-02: Owned Before Third-Party
A capability the organization lacks **MUST** be built in an owned kit rather than introduced as a new third-party
dependency. A third-party dependency **MAY** be added only with a recorded exception naming the capability, why an
owned implementation is not feasible, and who accepted the exception. This requirement elevates the existing
"no new dependencies" constraint from repository compliance plans to an org-wide rule with a defined exit.

### FCIS-KIT-03: The Seam Is Generic
An owned kit **MUST NOT** contain a consumer's domain types, vocabulary, or product decisions. A kit that must be
told about the caller to be useful has not been factored; it has been moved. Consumers bind their own types to the
kit's seam on their own side of the boundary.

### FCIS-KIT-04: Semantic Versioning
Owned kits **MUST** be released with semantic versions. Consumers **MUST** express dependencies as version
requirements. A version **MUST NOT** be re-tagged or moved once published.

### FCIS-KIT-05: Revision Pins Are Temporary and Documented
A revision pin **MUST** record, adjacent to the dependency declaration, its **reason**, its **exit condition**, and
an **owner**. A revision pin without all three is non-compliant. A revision pin **MUST NOT** be used to avoid
cutting a release.

### FCIS-KIT-06: In-Repo Modules and External Paths
An **In-Repo Module** is compliant and needs no version requirement; it ships with its repository. An **External
Path Dependency MUST NOT** be committed: it binds the build to a directory layout on one machine rather than to a
release. Where such a dependency is needed during development, it **MUST** remain a local, uncommitted override.

### FCIS-KIT-07: Release Mechanics
A release **MUST** be an annotated tag on a commit whose own test suite passes, published as a GitHub release
(`gh release create`). Release notes **MUST** name the seam added or changed, and **MUST** state any breaking
surface explicitly. A release **MUST NOT** be cut from a working tree that differs from the tagged commit.

### FCIS-KIT-08: Upstream First
A change to an owned kit **MUST** land in the kit and be released before a consumer depends on it. Vendoring,
forking, patching in place, or duplicating kit source into a consumer **MUST NOT** be used as a substitute for a
release, including temporarily.

### FCIS-KIT-09: Bump Discipline
A version bump in a consumer **MUST** be a single-purpose change touching the manifest, the resolved file, and the
minimum adaptation the new version requires. Bumping a kit **MUST NOT** be combined with unrelated feature work in
the same commit.

### FCIS-KIT-10: Counterpart Provenance
A consumer **MUST** record the upstream tag or commit a change arrived from, and what it brings, in the
repository's plan or changelog. "Updated dependencies" is not a record.

### FCIS-KIT-10A: Resolved-Graph Coherence
A consumer **MUST** verify the dependency graph it actually builds, not only the declarations in its manifest. The
verification **MUST** report the resolved tag/revision for every owned kit, confirm that the revision is present in
the declared upstream repository, and identify the executable or artifact under test. A live-drive, visual-regression,
release, or publication claim **MUST** fail when the artifact contains a deprecated or retired UI surface that the
consumer source no longer declares, or when the resolved graph cannot be reproduced from the committed manifest and
lockfile.

SwiftPM caches **MUST NOT** be treated as provenance. A consumer **MUST** resolve/build from the committed package
identity and run a negative surface check over the resulting artifact before claiming current UI behaviour. When an
upstream fix exists only on an unreleased commit, the consumer **MUST** either consume a documented temporary
revision pin under FCIS-KIT-05 or wait for a release; it **MUST NOT** silently combine that cache with a semver
declaration and call the result current.

### FCIS-KIT-11: Evidence Lives With the Seam
A kit change motivated by a consumer's need **MUST** be proved by the kit's own tests. A seam demonstrated only in
the consumer is untested from the kit's perspective and **MUST NOT** be released as though it were covered.

### FCIS-KIT-12: Deprecation Before Removal
Removing or narrowing public API **MUST** be preceded by a release that deprecates it, with the replacement named.
Removal is a major version.

### FCIS-KIT-13: Other Standards Still Apply
A kit change that reaches a user interface **MUST** satisfy FCIS-AX; one that changes rendered output **MUST**
satisfy FCIS-VRT; one that touches on-device inference **MUST** satisfy FCIS-AIC-Preflight. Being in a kit is not
an exemption from the standard that governs the surface.

### FCIS-KIT-14: Mechanical Constraints
Every admitted capability **MUST** expose the conditions that gate its execution, admission, mutation, or terminal
claim as mechanical constraints in its executable contract. Each constraint **MUST** name its typed identity and
contract version, executable predicate, evaluating authority, bounded refusal state, and terminal evidence requirement.

An agent, scenario runner, instrument, consumer, or host adapter **MUST NOT** create, widen, reinterpret, or bypass a
mechanical constraint. When the required constraint is not admitted or cannot be evaluated, the operation **MUST** stop
as unestablished; it **MUST NOT** acquire a substitute prompt, flag, document, human ceremony, or parallel authority.
Under FCIS-KIT-15, the owning kit runtime—not a consumer or host adapter—must enforce the predicate and expose its
refusal and terminal evidence. FCIS-KIT-14 strengthens the existing FCIS layers; it does not create a fifth
instruction layer.

### FCIS-KIT-15: Kit-Only Execution Authority

Every admitted capability **MUST** execute and enforce its mechanical constraints inside its owning FCIS-KIT. The kit
owns the executable operation, authorization/admission predicate, lifecycle, refusal state, Store/SecretStore effect
boundary, and terminal evidence needed for that capability.

Host applications and CLIs **MAY** parse a machine-facing request, invoke the released kit contract, and render the
typed result. They **MUST NOT** implement, mediate, widen, reinterpret, authorize, retry, or provide a fallback for
the capability operation. A host adapter, adapter protocol, direct consumer executor, generic wrapper, or alternate
transport that can perform the capability operation is forbidden.

If a capability cannot be executed and proven by its owning kit, it is non-compliant and **MUST** stop as
`unestablished`. Existing adapter implementations are migration debt; they do not establish compliance and **MUST NOT**
be used as evidence of a kit-only implementation.

The governed instrument-plane application of FCIS-KIT-14 is [Chapter 91 — The FCIS-KIT Instrument Store Is the
Capability Plane](https://governance.fountain.coach/chapters/91-fcis-kit-instrument-store-is-the-capability-plane/),
and its repository declaration is [FCIS_KIT_DECLARATION.md](https://github.com/Fountain-Coach/midi2-gpu-fabric/blob/main/FCIS_KIT_DECLARATION.md).

---

## 4. Repository Declaration Template

```
FCIS-KIT:
  owns:
    - <kit name>: <what seam it provides>
  consumes:
    - kit: <name>
      mode: semver
      requirement: from "<version>"
    - kit: <name>
      mode: revision
      revision: <sha>
      reason: <why a release cannot be used yet>
      exit: <the condition under which this becomes semver>
      owner: <who>
  third-party-exceptions:
    - package: <name>
      capability: <what it provides>
      why-not-owned: <reason>
      accepted-by: <who>
```

---

## 5. Consumption Inventory

This inventory records observed state at adoption time. It is authoritative until each entry is either moved to a
version requirement or given the record FCIS-KIT-05 requires.

Verified against `apps/modernization-studio/Package.swift` and the upstream tag lists on 2026-08-02.

| Consumer | Kit | Mode | Upstream tags | Compliant |
| --- | --- | --- | --- | --- |
| midi2-gpu-fabric | FountainEditorKit | semver — `from: "0.2.0"` | released | Yes |
| midi2-gpu-fabric | UncertaintyScoreKit | semver — `from: "0.8.5"` | released | Yes |
| midi2-gpu-fabric | FountainStudioEditorKit | revision — `4aaeae89` | `v0.1.0` exists; **the pin is not at it** | No |
| midi2-gpu-fabric | ScoreKit | revision — `73c1f2d0` | **no tags — never released** | No |
| midi2-gpu-fabric | FountainKitFacebookConnector | revision — `fedbdf56` | **no tags — never released** | No |
| midi2-gpu-fabric | instrument, FountainTelemetryKit | in-repo module | n/a | Yes (FCIS-KIT-06) |

Two of the three pinned kits have never been released at all, so the pin is not a deliberate hold at a known
version — it is the absence of a release. That is the condition FCIS-KIT-04 and FCIS-KIT-07 exist to end, and it
is why FCIS-KIT-05 requires a pin to carry an exit rather than merely a justification.

Non-compliant entries are not defects to be hidden. Each **SHOULD** be resolved by cutting a release from (or
after) the pinned commit, or by recording the reason, exit condition and owner FCIS-KIT-05 requires.

---

## 6. Reference Precedent

`UncertaintyScoreKit v0.8.3` is the pattern FCIS-KIT-03, 04 and 07 describe: a generic
address/rack/map/inspector seam released upstream, consumed by version, with the kit receiving none of the
consumer's domain types. The consumer binds its own context to the same address on its own side. This standard
generalizes that release rather than inventing a procedure.

---

## 7. Implementation Status

- **midi2-gpu-fabric**: declaration pending; inventory recorded in Section 5. Two kits compliant by semver, two
  in-repo modules compliant, three revision pins to resolve — two of which require a first release upstream.
- **FountainEditorKit, FountainStudioEditorKit, ScoreKit, UncertaintyScoreKit, Fountain-Store**: publisher
  declarations pending.
- Other org repositories: declaration pending.

---

**End of Standard**
