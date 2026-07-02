# DEC-009: Relationships Use a Hybrid Model — System Relationships Plus Custom Relationships

# Document Information

| Field | Value |
|---|---|
| Document | DEC-009 |
| File | `docs/decisions/DEC-009-hybrid-relationship-model.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/product/03_Feature_Catalogue.md`, `docs/product/00_Glossary.md` |
| Used By | `docs/product/00_Glossary.md` |

---

## Context
`03_Feature_Catalogue.md` raised an open question on whether Relationship types should be a closed, fixed list or fully freeform/user-defined.

## Decision
Relationships use a hybrid model:
- **System Relationships** — a fixed, closed set maintained by the platform: `Owns`, `Belongs To`, `Insures`, `Maintained By`, `Lives At`, `Related To`.
- **Custom Relationships** — a user-defined, freeform relationship label for cases the closed list doesn't cover.

## Reason
A closed list keeps the most common relationships consistent, searchable, and predictable across the whole system (important for Global Search and future automation). A freeform escape hatch prevents the closed list from blocking legitimate relationships it didn't anticipate, without requiring a platform change to add one.

## Alternatives Considered
- **Fully closed list only** — rejected: too rigid; every unanticipated relationship type would require a platform change.
- **Fully freeform only** — rejected: produces inconsistent, unsearchable relationship labels over time (e.g., "insures," "insured by," "insurance for" all meaning the same thing).
