# DEC-002: Documents Are One `Document` Entity With a Category Field

# Document Information

| Field | Value |
|---|---|
| Document | DEC-002 |
| File | `docs/decisions/DEC-002-document-entity-consolidation.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/product/03_Feature_Catalogue.md`, `docs/product/00_Glossary.md` |
| Used By | `docs/product/03_Feature_Catalogue.md` |

---

## Context
Early product discussion listed Passport, Driving License, Certificate, Contract, Visa, PAN Card, and Aadhaar as candidate entity types under the Documents module. Modeled individually, this produces many entity types that are structurally near-identical (a document number, an issuing authority, an issue/expiry date, one or more attached scans), differing mainly in classification.

## Decision
All identity/official documents are modeled as a single `Document` entity type, with a **Document Category** field (Passport, Driving License, PAN, National ID, Certificate, Contract, Warranty, Other) distinguishing the kind of document.

## Reason
Custom Fields already exist specifically to handle category-specific variation without new entity types. Fragmenting into many near-duplicate entity types adds no real capability, but does add ongoing engineering cost (each new document category would otherwise require a new domain table). This is the same modeling pattern used by Notion and similar systems — one entity type, differentiated by a category/type field.

## Alternatives Considered
- **Separate entity type per document kind** (Passport, License, Certificate, Contract as distinct types) — rejected: fragments the Documents module for no behavioral gain and works against the platform-first principle (`DEC-001`).
