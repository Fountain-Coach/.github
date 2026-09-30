# Fountain Coach Security Architecture — Mandatory Implementation Briefing

**Priority:** highest. This is the company-wide security architecture for
Fountain Coach repositories and systems that can authorize, install, publish,
or operate a remote capability.

**Status:** mandatory architecture direction; implementation is incomplete
until the Definition of Done below is evidenced.

**Canonical source:** Fountain Coach `.github`. Repository-local copies are
projections and must link back here rather than silently diverge.

## 1. Why this briefing exists

The EstatePublisher history exposed a boundary failure: a typed connection
identifier and SecretStore preflight surrounded a concrete `/usr/bin/ssh`
runner that sent a shell program to a target. The identifier was not consumed
by the transport, and credential availability was not proof that the admitted
machine authenticated the session. Wrapping SSH in typed code does not create
machine-bound admission.

No repository may describe an SSH wrapper as a secure host-agent transport.

## 2. Legal and normative alignment

This architecture is intended to support, not automatically certify:

- [NIS2 Directive (EU) 2022/2555](https://eur-lex.europa.eu/eli/dir/2022/2555)
  for applicable risk management, access control, cryptography, incident,
  continuity, authentication, and supply-chain obligations.
- [Cyber Resilience Act, Regulation (EU) 2024/2847](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R2847)
  for applicable secure-by-design, vulnerability-handling, update, and user
  information obligations.
- [GDPR Article 32](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A32016R0679)
  where personal data is processed.
- [eIDAS 2, Regulation (EU) 2024/1183](https://eur-lex.europa.eu/eli/reg/2024/1183/oj)
  where legally recognized electronic identity or signatures are required.

Applicability remains entity-, product-, sector-, and data-dependent. This
document is not a legal compliance certification.

## 3. Required authority model

The normal remote-operation path is:

```text
owner approval
  → current FountainStore admission read-back
  → cryptographic machine/workload identity
  → authenticated typed transport
  → host-agent capability policy
  → typed host execution and read-back
  → separate provider capability, if needed
  → terminal FountainStore receipt
```

Each arrow is a real gate. A secret, hostname, reachable port, loaded SSH key,
or matching connection label is not machine admission.

## 4. Mandatory rules

1. **Machine identity is cryptographic.** Admission binds machine identity,
   peer identity, transport identity, capabilities, destination Store, owner
   authority, source/artifact identity, expiry, and revocation state.
2. **Transport consumes admission.** The transport authenticates the admitted
   peer and proves that its identity matches the Store admission. An opaque
   `connectionID` must select that identity; it may not be an unused label.
3. **Operations are typed.** EstatePublisher sends typed host-agent
   capabilities, never arbitrary shell fragments, command strings,
   identity-file paths, or bearer material.
4. **The host agent owns host effects.** It validates audience, nonce, expiry,
   authorization, capability, request digest, and idempotency before changing
   service, edge, release, or Store state.
5. **SSH is not normal production transport.** SSH is permitted only as an
   explicitly named bootstrap or emergency-recovery capability with separate
   authorization, logging, and acceptance evidence.
6. **Provider effects remain separate.** DNS, certificate, cloud, and host
   effects have distinct typed authorities. One side effect cannot manufacture
   authority for another.
7. **Receipts are durable and diagnostic.** FountainStore records phase,
   identity, target, capability, request/artifact digests, predecessor,
   idempotency, read-back, and safe diagnostic codes. Credentials and private
   keys never appear.
8. **Partial failure is explicit.** Host mutation, read-back, provider
   mutation, rollback, and recovery are distinct states. No terminal success
   exists without required read-back and sibling-conservation proof.
9. **Release provenance is verified.** Installation and update paths bind the
   signed or pinned artifact and source revision to the admitted machine and
   record the resulting evidence.
10. **Local-model reasoning is not authority.** The local model may reason over
    finite contract and grounded Store state and emit only a typed candidate,
    clarification, or refusal. Swift contracts, host agents, provider
    adapters, and FountainStore decide and prove effects.

## 5. Required EstatePublisher replacement

The normal EstatePublisher operation must use the declared native host-agent
transport. The current process runner that shells out to SSH is a retirement
target; do not add another wrapper around it.

The replacement must provide:

- FountainStore admission lookup and freshness validation;
- peer identity and capability negotiation;
- authenticated, encrypted transport bound to that identity;
- typed host-agent operations with no shell input;
- typed host read-back and safe failure classification;
- revocation and expiry handling;
- one correlated terminal FountainStore receipt; and
- negative tests for guessed IDs, stale receipts, wrong peers, missing
  capabilities, arbitrary shell, credential-without-admission, and partial
  host/provider failure.

## 6. Repository inheritance

Every Fountain Coach repository that can build, install, authorize, publish,
or operate a remote capability must:

1. link this briefing from its root `AGENTS.md`;
2. declare applicable FCIS and regulatory documents;
3. identify its typed capability kit and host adapter;
4. use this machine-admission and transport vocabulary;
5. reject SSH wrappers as normal production admission; and
6. record deviations as explicit, reviewed architecture exceptions.

## 7. Definition of Done

This architecture is complete only when evidence shows that:

- normal EstatePublisher operations use machine-bound typed transport;
- the admitted peer identity is cryptographically verified at execution;
- the host agent rejects arbitrary shell and stale or guessed admission;
- typed read-back and redacted failure evidence are persisted in FountainStore;
- host, DNS, certificate, and rollback boundaries remain separately proven;
- the Tennis retirement scenario completes without direct SSH mutation; and
- the full positive and negative acceptance suite passes.

Until then, EstatePublisher remote effects are **not proven** under this
architecture.
