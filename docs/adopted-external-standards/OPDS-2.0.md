# OPDS Catalog 2.0 — Adopted External Standard

**Status:** Adopted by Fountain Coach (14 October 2026)  
**Classification:** External interoperability standard; **not** an FCIS-authored standard or a fifth FCIS instruction layer  
**Scope:** Fountain Coach publication catalogs and their consumer interfaces  
**Upstream specification:** https://specs.opds.io/opds-2.0  
**Upstream maintainers and issue tracker:** https://github.com/opds-community/specs  
**Implementation owner:** https://github.com/Fountain-Coach/fountain-press  
**Internal authority:** Fountain Coach's source-owning repositories, publication admission rules, and FCIS governance

## Adoption decision

Fountain Coach adopts **OPDS Catalog 2.0** as the preferred machine-readable interchange for exposing discoverable catalogs of released digital publications. This is a deliberate choice of an **existing community-owned standard**, not a claim that Fountain Coach owns, authored, forked, or can amend OPDS.

The canonical specification remains upstream. This document records only Fountain Coach's adoption, scope, conformance expectations, and mapping to its own publishing architecture. It does **not** reproduce the specification or introduce a parallel OPDS dialect.

FCIS continues to govern instructions, authority, plans, skills, and capabilities. OPDS governs **catalog interoperability**. Neither standard replaces the other.

## Normative local adoption profile

1. **Published catalog contract.** A Fountain Coach service that claims to offer an interoperable machine-readable **publication catalog** MUST offer an OPDS 2.0 feed, with the media type `application/opds+json`, and MUST identify its feed using a self link. Other internal editorial indexes MAY coexist; they are not substitutes for OPDS.
2. **Upstream conformance.** Every catalog intended for public release MUST validate against the applicable upstream OPDS 2.0 JSON Schema and meet the specification's semantic requirements. A passing schema check alone MUST NOT be presented as proof that links, acquisition claims, or publication states are truthful.
3. **Publication admission.** A catalog MUST project only authorized publication/edition records. Drafts, unapproved manuscripts, internal bookshop fixtures, unreleased builds, and private-source content MUST NOT silently become public OPDS entries. The source-owning repository and admitted edition manifest remain authoritative.
4. **Stable identity and provenance.** Publication identifiers, titles, authorship, languages, cover images, format links, availability, and revision/provenance MUST come from admitted source records. Do not synthesize ISBNs, prices, covers, acquisition rights, licensed formats, or released status.
5. **Truthful acquisition.** `download`, `preview`, `buy`, `borrow`, `subscribe`, and other acquisition relations MUST describe the actual link target and real access conditions. A complete web-reading edition MUST NOT be relabeled a sample merely to fill a field. A private candidate MUST NOT be listed publicly as an available publication.
6. **Separated responsibilities.** Fountain Press owns catalog projection and composition; First Reading owns the reading experience; Teatro owns its publication/performance-specific semantics. OPDS MAY link their admitted representations but MUST NOT be made the authority for semantic interpretation, rights, edition admission, execution, purchase, or deployment.
7. **Open web and implementer independence.** A static JSON catalog served over HTTPS is acceptable. No special hosted catalog service, live application server, third-party OPDS SDK, or GitHub Actions workflow is required by this adoption. Compatibility with OPDS 1.2 MAY be added only where a demonstrated reader needs it.
8. **Change control.** Because OPDS 2.0 is a living standard, each release SHOULD record the upstream specification/schema revision used for validation, along with the generated feed revision and conformance test result. An upstream change does not silently rewrite already-released publication facts.

The phrases MUST, MUST NOT, SHOULD, and MAY express Fountain Coach's adoption requirements, not amendments to upstream OPDS.

## Current implementation boundary (at adoption)

`Fountain-Coach/fountain-press` already generates **provisional** `/opds/v2/catalog.json` for a **private First Reading proof**. This is evidence of an existing implementation seam, **not** a declaration of public OPDS conformance, release, commercial availability, or deployment. The source manifest explicitly has `published: false`; it remains authoritative. The prior Governance anthology is rejected and MUST NOT be reinstated through the OPDS catalog.

Before production promotion, Fountain Press must document and demonstrate:

- feed and publication schema validation with an identified upstream revision;
- correct `self`, publication identity, and truthful link/acquisition semantics;
- only admitted, released, publicly accessible representations in a public catalog;
- links that resolve to actual resources with the advertised media type and access terms;
- local acceptance receipts; no automatic public deployment.

This adoption is **documentation/authority only** until those release gates are satisfied.

## Sources and boundaries

- [OPDS Catalog 2.0 — upstream living specification](https://specs.opds.io/opds-2.0)
- [OPDS 2.0 feed schema](https://specs.opds.io/schema/feed.schema.json)
- [OPDS 2.0 publication schema](https://specs.opds.io/schema/publication.schema.json)
- [Readium Web Publication Manifest — underlying publication model](https://readium.org/webpub-manifest/)
- [FCIS (org-level instruction architecture)](../../profile/README.md)
- [Fountain Coach publication and source policy](../FCIS-Publication-and-Source-Policy.md)
- [Fountain Press (implementation owner)](https://github.com/Fountain-Coach/fountain-press)

**Versioning:** The adoption of an external publication format does not itself change the FCIS RFC 0001 four-layer architecture or bump the FCIS suite version. A future new *FCIS-authored* standards-track document, if one is needed, follows FCIS's separate standards process.
