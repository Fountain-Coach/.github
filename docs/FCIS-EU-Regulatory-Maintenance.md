# FCIS — European Regulatory Applicability and Change Maintenance

**Status:** Organization-owned maintenance procedure, 18 November 2026. **Authority:** [FCIS standalone Go stack](../FCIS-STACK.md) for service scope; [European Cybersecurity Profile, Governance 118](https://governance.fountain.coach/chapters/118-european-cybersecurity-profile/) for engineering risk posture; the current law and competent supervisory authorities for legal duties. **HTTP projection:** [FCIS-OPENAPI.json](../FCIS-OPENAPI.json) points here as non-executable metadata.

**Claim boundary:** This procedure defines **how** Fountain Coach maintains regulatory applicability and evidence. It does not assert that the new Go issuer is certified or legally compliant; a green automated check, HTTP response or Store receipt is not legal review. No new HTTP API, FCIS Kit, authority, database or mandatory customer administration service is created.

## Scope and source ownership

Include the actual deployed FCIS Go issuer, owner passkey/OAuth/MCP, enrolled Host and MIDI2 execution interfaces, the dedicated FCIS FountainStore, Access as a separate UI consumer, and downstream adapters **when they are admitted and released**. Assess the company/operator role, data flow and processing purpose, product and service classification, user/customer category, distribution, Member States reached, applicable supervisory body, and whether the law is already applicable or only proposed/future.

Maintain a **source-versioned applicability register with each affected deployable product/service**. A central policy documents the workflow but does not replace the owning product's evidence. The existing [FCIS editorial-app register](https://github.com/Fountain-Coach/fcis.fountain.coach/blob/main/compliance/register.json) was written for a private owner-WLAN publication and MUST NOT be reused as an unreviewed compliance decision for the Go authorization service or the whole Fountain Coach estate. Reuse its proven record shape and triggers, not its previous classifications.

## Required register record

For each candidate legal instrument or relevant national implementation, record:

- Stable regulation ID and **primary** official EU/Member-State source URL, version/consolidation date and date checked; distinguish enacted law, binding decision, guidance, proposal and commentary.
- Effective/application dates and transitional dates **for the applicable provision**, not one guessed global date.
- Role and precise product/service **applicability trigger**, with `applicable`, `not_applicable` (reasoned), or `requires_review` (unresolved). Record a rationale tied to actual architecture and deployment evidence.
- Legal/operational accountable owner, reviewer and review date, due date or next review, and jurisdiction/national implementation or exemption reasoning.
- Mapped controls, code/source/test/provenance links, release or processing effect, remediation action, independent evidence, residual uncertainty and decision/approval authority.
- A source-linked change history and a private incident/reporting workflow where needed. Keep protected personal data, keys, security logs, incident specifics and account identifiers outside the public Git register.

The register MUST distinguish **not applicable** from **not yet reviewed**, and obligations already in force from proposed legislation. An unavailable or stale source is `requires_review`; it is never interpreted as permission, a regulatory violation, or a legal certification.

## Minimum applicability review (not a blanket scope claim)

Review against what the product *does*, not what its repository names suggest:

| Area | Official starting source | Applicability question |
| --- | --- | --- |
| GDPR, including privacy/security and data-subject obligations | [Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | What personal data is processed, under what controller/processor roles, lawful basis, retention, DPA/transfer and incident obligations? |
| ePrivacy and German device-storage rules | [Directive 2002/58/EC](https://eur-lex.europa.eu/eli/dir/2002/58/oj) and current German TDDDG | Are cookies, browser storage, device identifiers or communications regulated? |
| AI Act | [Regulation (EU) 2024/1689, as amended](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) and [current Commission timeline](https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act) | Is FCIS or an admitted product an AI provider/deployer or subject to transparency, high-risk or prohibited-use rules? Do **not** infer this from use of MCP alone. |
| NIS2 and national cybersecurity rules | [Directive (EU) 2022/2555](https://eur-lex.europa.eu/eli/dir/2022/2555/oj) and current German implementation | Is the operator actually a covered essential/important entity or relevant digital-infrastructure provider? |
| Cyber Resilience Act | [Regulation (EU) 2024/2847](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) and [Commission reporting guidance](https://digital-strategy.ec.europa.eu/en/policies/cra-reporting) | Is an in-scope product with digital elements placed on the market, in what economic-operator role, with what vulnerability/security reporting duties? |
| Accessibility, digital content and consumer access | [Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj) plus BFSG/BFSGV and relevant EN 301 549 designation | Is the released offering a covered consumer service/product, e-book, dedicated reading software, or e-commerce service? |
| DSA, eIDAS, copyright and commerce | [DSA](https://eur-lex.europa.eu/eli/reg/2022/2065/oj), [eIDAS](https://eur-lex.europa.eu/eli/reg/2014/910/oj), applicable EU/German copyright, distance-selling, payment law | Does the **admitted functionality** include intermediary/hosting services, regulated trust services, public content, consumer contracts or payments? Ordinary OAuth is not automatically a trust service. |

**Timing illustration, not a legal conclusion:** Under the CRA, some reporting provisions apply from **11 September 2026** whereas most obligations apply from **11 December 2027**; this matters only for an **in-scope party**. AI Act requirements are phased and have been amended; re-read the consolidated law and Commission timeline rather than pinning an outdated uniform enforcement date.

## Ongoing maintenance and acceptance

1. **Monthly source review:** Check EUR-Lex consolidated texts, relevant Commission/ENISA/regulator releases, and the applicable German or other Member State official sources for changes. Record last checked date and links even when there is no material change. This is a required human/agent *procedure*, **not a claim that a recurring automation is currently running**.
2. **Event-driven review:** Recheck immediately for a material statutory update, regulator instruction, security incident, jurisdiction/operator/hosting change, new processing, logs, retention, account roles, uploads, AI inference/generation, external provider, consumer service, billing/Stripe adapter or digital-product distribution.
3. **Before the affected release:** Classify applicable obligations and evidence, assign any unresolved decision to a qualified reviewer and establish the actual release condition. A release cannot claim a resolved applicable legal requirement when its evidence remains missing; a speculative legal applicability question cannot expand the original Go cutover DoD without a binding rule or reproduced risk.
4. **Keep independent witnesses:** Cite exact law/source version, factual deployed behavior, source/release SHA and audit result. Security engineering checks, accessibility checks and FountainStore receipts support the decision but do not replace legal interpretation, DPO review, conformity assessment or supervisory authorization where required.
5. **Report honestly:** Distinguish `documented`, `source-tested`, `released`, `legally-reviewed` and `not-established`; never claim automatic real-time legal monitoring unless an actual admitted schedule and witnessed source readback exist.

## Non-goals and boundaries

- The first standalone Go FCIS cutover remains the exact [finite priority-one DoD](../FCIS-STACK.md#7-production-deployment-and-finite-dod--priority-one). This policy does not mandate building a legal-registry API or delaying cutover for unrelated or inapplicable regulation.
- An **applicable**, already-binding requirement for the actual release must be assessed and satisfied; an inapplicable area may be recorded as such with evidence. A candidate or proposal is not enforceable merely because a monitoring workflow identified it.
- A released product's established compliance gate remains with its source owner. The [Book of Reframe European publication gate](https://github.com/Fountain-Coach/book-of-reframe/blob/main/COMPLIANCE.md) is specific to that book, not the FCIS issuer; the original private FCIS editorial app has its own scoped register.
- The proposed Stripe/payment adapter is priority two. When admitted, assess consumer/payment/data duties separately, using official Stripe API dependencies for **technical provider schema**, not as legal authority.

**Next proof required:** A named FCIS Go owner/operator must create or update the register for the **actual deployed Go issuer and MCP/Host service**, classify current applicability with legal review where needed, and attach versioned evidence. Until then, organization policy adoption is **SOURCE-ONLY**, not a compliance sign-off.
