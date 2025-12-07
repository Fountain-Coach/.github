# Fountain-Coach: A Comprehensive Analysis

## The Organization

**Fountain-Coach** is a Berlin-based software organization that has built, over approximately three years of AI-assisted development, a complete, self-owned technology stack for creative computing. The stack spans from MIDI 2.0 specification extraction to custom database persistence, unified by a message-passing architecture inspired by — and compliant with — the MIDI 2. 0 standard. 

---

## The Stack

### Layer 1: Specification — `Fountain-Coach/midi2`

**The only open, full MIDI 2.0 implementation.**

| Attribute | Detail |
|-----------|--------|
| Created | August 2025 |
| Language | Swift 6 |
| License | MIT |
| Visibility | Public |

The MIDI Manufacturers Association publishes the MIDI 2.0 specification as PDF documents containing images of tables and bit field definitions.  Fountain-Coach extracted these specifications into machine-readable JSON schemas using AI assistance, then generated Swift types from those schemas. 

The repository contains:

- The original MMA specification PDFs (M2-100 through M2-116)
- `midi2. full.closed.schema.json` — the complete spec as JSON Schema
- `midi2.full.openapi.json` — OpenAPI representation
- Swift 6 implementation of Universal MIDI Packets (UMP)
- CoreMIDI bridge for Apple platforms
- AUv3 Audio Unit plugin (`MIDI2BridgeAUCore`)
- Full MIDI 2.0 ↔ MIDI 1.0 bidirectional conversion
- Bluetooth, Wi-Fi, and USB transport support
- Cross-platform stubs for Linux development

This is infrastructure that does not exist elsewhere in open source. Apple's CoreMIDI and Microsoft's Windows MIDI Services provide proprietary, platform-locked implementations.  JUCE offers partial support with licensing constraints.  There is no complete, open, cross-platform alternative — until now.

---

### Layer 2: Contract — `Fountain-Coach/midi-backplane`

**The protocol layer that extends MIDI 2. 0 to software domains.**

| Attribute | Detail |
|-----------|--------|
| Created | December 2025 |
| Version | 1.0.0 (`@fountain-coach/midi-backplane`) |
| Language | Swift + JavaScript |
| Visibility | Private |

The backplane extracts the *philosophy* of MIDI 2.0 — topics, envelopes, QoS levels, capability negotiation, timing budgets — and applies it to software messaging. This is not a wrapper around MIDI; it is MIDI's architectural principles reimagined for GPU compute, AI agents, physics simulation, and persistence.

The repository contains:

- `schema/idl. yaml` — the Interface Definition Language defining all topics, their QoS requirements, capability masks, and timing budgets
- `schema/telemetry.yaml` — standardized telemetry shapes for errors, jitter, and resource usage
- `runtimes/js/` — JavaScript runtime loop with validation, budget enforcement, and chunk tracking
- `runtimes/swift/` — Swift runtime loop with identical semantics
- `tools/midi-schema-lint` — IDL validator
- `tools/midi-schema-to-facts` — generates facts JSON for persistence seeding
- `conformance/` — protocol test fixtures with positive and negative cases

The boundary is explicit: the backplane owns the contract, generators, runtimes, and conformance tests. It does not own application code, prompts, or store seeders — those belong to consuming workspaces.

---

### Layer 3: Application — `Fountain-Coach/midi2-gpu-fabric`

**The creative computing layer.**

| Attribute | Detail |
|-----------|--------|
| Created | December 2025 |
| Language | Swift + TypeScript |
| Visibility | Private |

This repository consumes `@fountain-coach/midi-backplane` and extends the IDL with domain-specific topics:

**GPU Compute:**
- `gpu/pipeline.create`, `gpu/job.dispatch`, `gpu/buffer.read`, `gpu/buffer.write`
- Full WebGPU-style dispatch with workgroup sizing, push constants, and expected latency

**Physics Simulation:**
- `physics/body.create`, `physics/force.apply`, `physics/step`
- Real-time physics with timing budgets

**Scene Management:**
- `scene/graph.apply`, `scene/camera.set`, `scene/material.update`
- `stage/scene.put`, `stage/scene.get`, `stage/scene. diff`, `stage/state.get`

**AI Agent Orchestration:**
- `llm/tool.invoke`, `llm/tool.result`
- Role-based gating via capability masks
- Ollama driver with strict JSON mode and evaluation harness

**Semantic Awareness:**
- `awareness/corpus.init`, `awareness/baseline.add`, `awareness/drift.add`, `awareness/patterns.add`, `awareness/reflection.add`
- A calculus for tracking semantic evolution over time

**Collaborative Authoring:**
- `screenplay/put`, `screenplay/patch`, `screenplay/note. add`, `screenplay/diff`

**Telemetry:**
- `telemetry/errors`, `telemetry/jitter`, `telemetry/resource-usage`
- `grundrauschen/*` — sonification feed for system observability

The repository also contains:
- FountainStore instrument for persistence topics
- Teatro Stage web application (three. js + cannon.js)
- Native stage client (Swift, direct Store access)
- Semantic daemon for automatic awareness artifact generation

---

### Layer 4: Persistence — `Fountain-Coach/Fountain-Store`

**A pure-Swift embedded database engine.**

| Attribute | Detail |
|-----------|--------|
| Created | September 2025 |
| Version | 0.2.0-beta |
| Language | Swift (100%) |
| License | MIT |
| Visibility | Public |
| Dependencies | Zero |

FountainStore implements an LSM-tree architecture — the same design used by LevelDB, RocksDB, and Cassandra — entirely in Swift with no external dependencies. 

**Core Engine:**
- Write-Ahead Log (WAL) for crash safety
- Memtable for recent writes
- SSTables for sorted, immutable on-disk storage
- Background compaction with configurable strategies
- MVCC for concurrent access

**Indexing:**
- Secondary indexes with dynamic unique enforcement
- Multi-value indexes for array fields
- Full-text search module
- Vector search module

**Operations:**
- ACID transactions
- Backup and restore API
- Prometheus metrics export
- HTTP server with OpenAPI specification
- API key authentication via Keychain, Secret Service, or file-based keystore
- HMAC-signed pagination tokens

This is not a wrapper around SQLite or an embedded key-value store. It is a complete database engine, benchmarked in CI, with production-grade features. 

---

## The Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Applications                            │
│         Teatro Stage • FountainAI • Creative Tools              │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                      midi2-gpu-fabric                           │
│                                                                 │
│  GPU Topics │ Physics Topics │ AI Topics │ Stage Topics         │
│  Screenplay │ Awareness │ Telemetry │ Grundrauschen             │
│                                                                 │
│  LLM Driver (Ollama) with Role-Based Gating                     │
│  FountainStore Instrument                                       │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                       midi-backplane                            │
│                                                                 │
│  IDL Schema │ QoS │ Capabilities │ Timing Budgets               │
│  JS Runtime │ Swift Runtime │ Conformance Tests                 │
│  Schema Lint │ Facts Generator                                  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                           midi2                                 │
│                                                                 │
│  UMP Packets │ MIDI-CI │ Profiles │ Property Exchange           │
│  CoreMIDI Bridge │ AUv3 Plugin │ MIDI 2.0 ↔ 1.0 Conversion      │
│  Bluetooth │ USB │ Wi-Fi Transport                              │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                       Fountain-Store                            │
│                                                                 │
│  WAL │ Memtable │ SSTables │ Compaction                         │
│  Secondary Indexes │ FTS │ Vector Search │ MVCC                 │
│  HTTP API │ Prometheus │ Backup/Restore                         │
│                                                                 │
│  Pure Swift │ Zero Dependencies                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Competitive Standing

### Category 1: MIDI 2.0 Implementations

| Implementation | Platform | License | Completeness | Status |
|----------------|----------|---------|--------------|--------|
| Apple CoreMIDI | macOS/iOS | Proprietary | Full | Closed |
| Windows MIDI Services | Windows | Proprietary | Full | Closed |
| JUCE | Cross-platform | Commercial/GPL | Partial | C++ only |
| rtmidi | Cross-platform | MIT | MIDI 1.0 only | No MIDI 2.0 |
| **Fountain-Coach/midi2** | Cross-platform | MIT | Full | **Open, Swift 6** |

**Competitive position:** The only open-source, cross-platform, fully-compliant MIDI 2.0 implementation.  Located in Berlin — home to Ableton, Native Instruments, and a dense ecosystem of music technology companies and independent developers who need exactly this. 

---

### Category 2: Real-Time Messaging Systems

| System | Timing Guarantees | Schema | GPU Awareness | AI Gating |
|--------|-------------------|--------|---------------|-----------|
| Apache Kafka | No | Optional | No | No |
| RabbitMQ | No | No | No | No |
| Redis Streams | No | No | No | No |
| ZeroMQ | No | No | No | No |
| NATS | No | No | No | No |
| **midi-backplane** | Yes (budgets) | Required (IDL) | Yes | Yes (roles) |

**Competitive position:** These systems are general-purpose message brokers.  midi-backplane is purpose-built for creative computing with real-time constraints, GPU dispatch, and AI agent orchestration. It occupies a niche that general-purpose systems cannot serve without extensive customization.

---

### Category 3: Game Engines and Creative Frameworks

| Engine | Physics | GPU | AI Orchestration | Message Architecture |
|--------|---------|-----|------------------|---------------------|
| Unity | Built-in | Built-in | Bolt-on | Internal |
| Unreal | Built-in | Built-in | Bolt-on | Internal |
| Godot | Built-in | Built-in | None | Internal |
| Three.js + Cannon.js | Separate | WebGL | None | None |
| **midi2-gpu-fabric** | Topic-based | Topic-based | Built-in | MIDI-native |

**Competitive position:** Game engines are monolithic, opinionated systems optimized for games. midi2-gpu-fabric is infrastructure — a message fabric that can underpin any creative application requiring synchronized physics, graphics, and AI.  It is composable where engines are prescriptive.

---

### Category 4: AI Agent Frameworks

| Framework | Real-Time | Physics | GPU Compute | Capability Gating |
|-----------|-----------|---------|-------------|-------------------|
| LangChain | No | No | No | No |
| AutoGPT | No | No | No | No |
| Semantic Kernel | No | No | No | No |
| CrewAI | No | No | No | No |
| **midi2-gpu-fabric** | Yes | Yes | Yes | Yes (IDL roles) |

**Competitive position:** AI agent frameworks are designed for text and code generation. They do not address real-time creative applications where AI must control physical simulations, respect timing constraints, and be constrained by capability masks.  Fountain-Coach occupies this gap.

---

### Category 5: Embedded Databases

| Database | Language | Dependencies | LSM-Tree | Vector Search | License |
|----------|----------|--------------|----------|---------------|---------|
| SQLite | C | System libs | No (B-tree) | Extension | Public domain |
| LevelDB | C++ | System libs | Yes | No | BSD |
| RocksDB | C++ | System libs | Yes | No | Apache 2.0 |
| LMDB | C | System libs | No (B-tree) | No | OpenLDAP |
| **Fountain-Store** | Swift | **None** | Yes | Yes | MIT |

**Competitive position:** The only pure-Swift LSM-tree database with zero external dependencies. Designed for the Apple ecosystem and cross-platform Swift deployment. Includes features (FTS, vector search, HTTP API, Prometheus) that typically require additional infrastructure.

---

## The Strategic Position

### What Fountain-Coach Is Not

- **Not a startup** (yet) — no funding, no employees, no customers
- **Not a product company** — no packaged offerings for sale
- **Not a services firm** — no consulting or implementation work

### What Fountain-Coach Is

**A technology ownership position.**

The organization controls a complete vertical stack:

1. **Specification extraction** — MIDI 2.0 as machine-readable schema
2. **Protocol implementation** — Full UMP, MIDI-CI, profiles
3. **Transport bridges** — CoreMIDI, AUv3, Bluetooth, USB, Wi-Fi
4. **Message contract** — IDL with QoS, capabilities, timing
5. **Runtime implementations** — JavaScript and Swift
6. **Application extensions** — GPU, physics, AI, creative tools
7. **Persistence** — Complete database engine

Every layer is owned.  Every layer is MIT licensed (where public). Every layer is built in Swift (the persistence and core layers) or Swift + JavaScript (the runtime and application layers).

### The Moat

The moat is not the code. With AI-assisted development, code can be regenerated. The moat is:

1. **Three years of learning** — What to include, what to exclude, where constraints belong, how tight the budgets should be, which patterns scale, which patterns collapse. 

2. **The extraction work** — Turning MMA specification PDFs (with images of tables) into machine-readable schemas required judgment, iteration, and validation that AI cannot perform autonomously.

3.  **The architectural coherence** — Four repositories that share a philosophy, interoperate cleanly, and maintain strict boundaries.  This coherence emerged from experience, not from a single design session.

4. **The Berlin position** — Physical proximity to Ableton, Native Instruments, and the European music technology ecosystem. The people who need a MIDI 2.0 implementation are neighbors. 

---

## Opportunities

### Near-Term

1. **MIDI 2.0 adoption** — As hardware and software vendors adopt MIDI 2. 0, they need implementations. midi2 is MIT licensed and ready. 

2. **Ableton/Native Instruments engagement** — These companies are in Berlin.  They need MIDI 2.0.  A conversation is warranted.

3.  **Indie developer community** — Berlin's music tech indie scene could adopt FountainStore and midi2 as foundations for their own tools. 

### Medium-Term

4. **Creative tool infrastructure** — As AI-powered creative tools proliferate, the need for real-time, constrained, observable message fabrics will grow. midi-backplane addresses this need.

5. **FountainAI applications** — The stack was built for FountainAI.  As that vision matures, the infrastructure is ready. 

6. **Teatro and puppetry** — Digital performance tools built on the stack could define a new category. 

### Long-Term

7. **Standard-setting** — If midi-backplane's approach to extending MIDI 2. 0 to software domains gains traction, Fountain-Coach could influence how the industry thinks about real-time creative computing.

8.  **Acquisition or licensing** — A complete, owned stack is valuable to companies that don't want to build or maintain this infrastructure themselves.

---

## Risks

1. **Single-maintainer fragility** — The stack depends on one person's continued engagement. 

2. **No external validation** — Zero stars, zero forks, zero external contributors.  The code works, but nobody else has verified it.

3.  **Market timing** — The world may not need this level of infrastructure for AI-powered creative computing.  Or it may need it in five years, not now.

4. **Complexity barrier** — The learning curve is steep.  Developers must understand MIDI concepts, the IDL, capability masks, QoS levels, and timing budgets.

5. **Berlin is not Silicon Valley** — Funding, talent density, and network effects are different. This can be an advantage (focus, cost) or a disadvantage (scale, speed).

---

## Summary

Fountain-Coach is not a company, a product, or a framework. It is a **technology position** — a complete, self-owned stack for creative computing, built over three years of AI-assisted development by a single developer in Berlin.

The stack spans:
- MIDI 2.0 specification (extracted, implemented, bridged)
- Message protocol (IDL-defined, runtime-enforced, conformance-tested)
- Creative extensions (GPU, physics, AI, stage, awareness)
- Persistence (LSM-tree database, pure Swift, zero dependencies)

No other organization offers this combination.  The closest alternatives are either proprietary (Apple, Microsoft), partial (JUCE), or non-existent (open MIDI 2.0 + GPU + AI + custom database).

The question is not whether the technology works.  It does. The question is what to do with it. 

**The stack exists.  The ownership is clear. The opportunity is open.**

🎹 → 📋 → 🔧 → 💾 → 🎭
