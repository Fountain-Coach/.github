# Fountain Coach Governance

## Purpose
This repository defines the governance, style, and release principles of the Fountain Coach organization.

### FCIS-VRT Quadrupel Rhythm
| State | Git Equivalent | Description |
|--------|----------------|-------------|
| **Commit** | Drift Frame | Active change |
| **Tag** | Baseline Frame | Stable reference |
| **Release** | Quiet Frame | Reproducible state |
| **Snapshot** | Archive Frame | Permanent record |

### Branching and Releases
- Feature branches: `feature/<topic>`  
- Baseline tags: `B-<version>`  
- Quiet releases: `Q-<version>`  
- Archive snapshots: `A-<version>`

### Founding rule: goal fidelity and non-invention

The organization-wide conduct authority is
[FCIS Goal Fidelity and Non-Invention](../docs/FCIS-Non-Invention-and-Goal-Fidelity.md).
A maintainer or agent MUST NOT turn an unverified risk or desired future
architecture into a blocker to a previously accepted capability. Every
proposed dependency must identify the user-requested outcome, observed failed
operation, already applicable contract and smallest necessary correction.
A test suite for proposed machinery does not establish that it was needed.
Keep genuine safety and authorization boundaries, and separate deferred
improvements from the current DoD. Agents carry the work forward without
requiring the user to repeat "proceed accordingly".

### Decision Making
- Changes must pass review by at least one maintainer from another repository layer.
- Merges require a Quiet Frame alignment test via FCIS-VRT (VRT-Render or VRT-Protocol as declared by the repo).

---
© 2025 Fountain Coach
