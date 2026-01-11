# FCIS-AIC-Preflight-RFC.md

## FCIS Apple Intelligence Compliance Specification (Preflight)

**Status:** Informational (Best Current Practice)  
**Intended Audience:** Developers submitting apps to the Apple App Store that integrate Apple Foundation Models  
**Publisher:** Fountain Coach (FCIS)  
**Version:** 1.2

---

## 1. Purpose and Scope

This document defines a preflight compliance framework for applications that integrate **Apple Intelligence via Apple Foundation Models**, and that implement **local, document-centric semantic systems**.

The goal of this specification is to:
- make application intent legible to App Store reviewers,
- reduce ambiguity around intelligence usage,
- and align developer implementations with Apple’s published guidance on privacy, user control, and on-device intelligence.

This document is **informational** and does not claim endorsement by Apple.

---

## 2. Terminology (Aligned with Apple Guidance)

- **Apple Intelligence**  
  System-provided intelligence capabilities delivered via Apple Foundation Models.

- **Intelligence Invocation**  
  A discrete, user-initiated request to Apple Intelligence through sanctioned system APIs.

- **Open-ended Prompt Interface**  
  A free-form text input or chat interface that accepts arbitrary requests without a predefined task scope, bounded outputs, or constraint messaging.

- **Task-Scoped Prompt Input**  
  A bounded input tied to a specific feature with a clear intent and constrained output (e.g. summarize this document, extract key points).

- **Semantic Artifacts**  
  User-visible, document-scoped outputs derived from intelligence invocation (e.g. summaries, annotations, classifications).

- **Semantic Memory**  
  Persistent storage of semantic artifacts within explicit user documents or projects.  
  *Semantic memory does not constitute model training, learning, or adaptation.*

- **Deterministic Execution**  
  Predictable Swift code paths that execute application logic in response to intelligence results.

---

## 3. Operational Boundaries and Threat Model

An FCIS-compliant application operates within the following boundaries:

- Intelligence is invoked only in direct response to explicit user actions.
- No intelligence operations occur autonomously or in the background.
- Apple Foundation Models are not modified, trained, extended, or replaced.
- Semantic artifacts are not shared across apps or users.
- No user data is transmitted to third-party AI or LLM services.
- Telemetry and logs exclude prompts, semantic artifacts, and user content; only non-content operational metrics are recorded.

These boundaries are designed to align with Apple’s privacy, safety, and platform integrity principles.

---

## 4. Normative Compliance Requirements

The key words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are to be interpreted as described in RFC 2119.

### FCIS-AIC-01
Applications **MUST** invoke intelligence exclusively through Apple-sanctioned Foundation Models APIs.

### FCIS-AIC-02
Applications **MUST NOT** expose unrestricted or open-ended natural language prompt interfaces.

Task-scoped prompt input **MAY** be provided when:
- The task is explicit and user-selected.
- The input is bounded to a specific document or file.
- The output type is fixed and user-visible.

### FCIS-AIC-03
All semantic artifacts **MUST** be user-visible and user-deletable.

### FCIS-AIC-04
Semantic artifacts **MUST** be scoped to explicit user documents, files, or projects.

### FCIS-AIC-05
Applications **MUST NOT** claim or imply model training, persistent learning, or adaptive behavior.

### FCIS-AIC-06
All post-inference application behavior **MUST** be implemented as deterministic Swift execution.

### FCIS-AIC-07
Applications **MUST** allow users to delete semantic artifacts and their derived metadata, and **MUST** honor system-level document deletion. Applications **SHOULD** document retention behavior and provide export or sharing of documents that contain semantic artifacts.

### FCIS-AIC-08
Applications **MUST NOT** log, transmit, or retain user content, prompts, or semantic artifacts in telemetry or logs. Telemetry **SHOULD** be limited to non-content operational metrics (counts, latency, error codes, resource usage) and **MAY** be aggregated or anonymized.

---

## 5. Architecture Conformance Profiles

### FCIS-AIC-Document-Centric Profile

Applications following this profile:
- Use explicit file formats (e.g. `.fountain`)
- Integrate with `UIDocument` / `FileDocument`
- Store all semantic artifacts on device
- Allow users to manage, export, or delete documents

### FCIS-AIC-Offline-First Profile

Applications following this profile:
- Do not require network connectivity for core functionality
- Do not depend on remote inference services
- Maintain consistent behavior offline

---

## 6. User Experience Compliance Patterns

To ensure reviewer clarity and user trust, FCIS-compliant applications:

- Present intelligence features as **assistance**, not agency
- Require explicit user action to invoke intelligence
- Clearly distinguish original user content from generated suggestions
- Avoid anthropomorphic, agentic, or autonomous framing

---

## 7. Informative Mapping to App Store Review Guidelines

See Apple App Store Review Guidelines: https://developer.apple.com/app-store/review/guidelines/

| FCIS Principle | Relevant App Store Guideline |
|---------------|------------------------------|
| User-controlled data | 5.1.1 Data Collection |
| On-device intelligence | 5.1.2 Data Use |
| Predictable app behavior | 2.5.1 Performance |
| No autonomous execution | 2.5.1 App Completeness |

**References (Informative):**
- Apple Foundation Models documentation: https://developer.apple.com/documentation/foundationmodels
- User Privacy and Data Use: https://developer.apple.com/app-store/user-privacy-and-data-use/

---

## 8. Preflight Self-Assessment Checklist

Before submission, the application should satisfy the following:

- [ ] All intelligence usage is routed through Foundation Models APIs
- [ ] Intelligence is user-initiated and task-scoped
- [ ] No free-form prompt interface is present
- [ ] All semantic artifacts are visible and deletable
- [ ] Retention and deletion behavior is documented; artifact and document erasure are honored
- [ ] Export or sharing exists for documents containing semantic artifacts (or documented file-based export)
- [ ] Telemetry/logging excludes user content, prompts, and semantic artifacts
- [ ] Terminology avoids references to learning or training
- [ ] Offline behavior is documented or self-evident

---

## 9. Conclusion

FCIS-compliant applications treat Apple Intelligence as a **system capability**, not a replaceable service.  
They prioritize transparency, user control, deterministic execution, and document-centric workflows.

This preflight specification is intended to support safe, predictable App Store submissions.

---

## Appendix A: Reviewer-Oriented Explanation (Informative)

This application integrates Apple Intelligence exclusively through Apple-provided Foundation Models APIs.

Key characteristics:

- Intelligence is invoked only when the user explicitly requests assistance.
- Generated outputs are stored as user-visible document content.
- Users can delete artifacts and documents using standard controls; retention behavior is documented.
- All application behavior following intelligence invocation is deterministic Swift code.
- No background processing, autonomous reasoning, or persistent learning occurs.
- No user data is sent to external AI services.
- Telemetry and logs contain no prompts, semantic artifacts, or user content.

The application functions as a **document-centric semantic workspace**, not as a general-purpose AI agent or conversational system.

---

## Related Policies (Informative)

- Security: ../.github/SECURITY.md
- Governance: ../.github/GOVERNANCE.md

---

**End of Document**
