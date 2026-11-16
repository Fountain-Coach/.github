---
name: fcis-swift-build
description: Deterministically select the admitted FCIS Swift Build Instrument for Swift compilation, tests, Xcode verification, Reframe workflows, workstation disk pollution, cache isolation, macOS versus Ubuntu builds, or build failures. Never run ad-hoc compiler, shell, SSH, or new build pipeline in its place.
---

# FCIS Swift Build — instrument caller

The skill is **not** the compiler, launcher, security authority, or build admission. Its only job is to select an admitted native instrument. Target `fountaincoach.swift-build@0.1.0`; Fountain Coach extension operation `workstation.swift.verify`; existing MIDI2 `reframe/capability.invoke` / `reframe/capability.event` envelope. The source contract lives in `Fountain-Coach/midi2-gpu-fabric/docs/fcis-swift-build-instrument-v0.1.0.md`; this installed Skill is the canonical .github agent instruction, not its runtime owner.

## One bounded call

1. Resolve the user's request to **one registered workflow**. This first candidate declares `reframe.quick`, `reframe.focused`, and `reframe.governance`. A semantic daemon, EstatePublisher, ReframeScenarioRunner, iPad/Xcode or another package is not silently mapped to these. It needs an explicitly admitted workflow profile.
2. Discover the active version, tool, owner, permissions and workflow from the **live FCIS Host capability registry**. Do not infer availability from this skill, GitHub source, a catalog tile, a passing test or an OpenAPI page. If not admitted, report `UNAVAILABLE — Swift Build Instrument not admitted` and stop. **Never substitute a direct** `swift`, `swiftc`, `swift build`, `swift test`, `xcodebuild`, manual `ssh`, raw shell, custom worktree, cache workaround or compiler helper.
3. Submit exactly one typed `action` (`plan|execute|status`), `workflow`, 40-character lowercase `sourceRevision`, `correlationID`, and `idempotencyKey`. No command strings, paths, environment overrides, alternate build directories, temporary credential, or approval are allowed in LLM-supplied input.
4. The native Host must independently attest the original installed workstation policy/launcher digest, committed source, owner grant, platform, approved mount/filesystem and resolved source/TMP/cache/module/DerivedData/log/artifact paths, free space, parallelism and exclusive build lease. Refuse internal MacBook Data outputs, ExFAT scratch, missing external APFS mount, insufficient disk, any unverified cache path or overlapping run.
5. The instrument—not the LLM—invokes the original launcher, binds execution to FountainStore, and returns exact source/toolchain/artifact/exit receipts. Interpret the authoritative terminal: `planned`, `running`, `succeeded`, `refused`, `failed`, `cancelled`, or `interrupted`. Source parsing is not compilation; compilation is not test passage; test passage is not product acceptance.
6. Duplicate idempotency retrieves the original bound run. Conflicting payload or uncertain Store/process state refuses or remains interrupted. No automatic re-run with a different key, no disk cleanup, no second compiler or invented fallback.

## Development boundary

At v0.1.0, only a typed **source candidate** and pure plan/refusal are implemented. The instrument is not yet registered, released or callable in FCIS Host. In an operational request, report unavailability instead of self-authorizing an execution. For work **developing** the instrument, use `fountain-coach-instrument-creation`; it governs scenario, source, tests, evidence, admission and release, but does not replace the workstation launcher.

See the source-bound scenario `Fountain-Coach/midi2-gpu-fabric/apps/estate-publisher/Scenarios/fcis-swift-build-instrument-20261116.yaml` and plan `Fountain-Coach/midi2-gpu-fabric/docs/plans/fcis-swift-build-instrument-20261116.md`.
