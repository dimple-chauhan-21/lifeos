# DEC-003: People Are One `Contact` Entity With Multi-Select Roles

# Document Information

| Field | Value |
|---|---|
| Document | DEC-003 |
| File | `docs/decisions/DEC-003-contact-entity-consolidation.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/product/03_Feature_Catalogue.md`, `docs/product/00_Glossary.md` |
| Used By | `docs/product/03_Feature_Catalogue.md` |

---

## Context
Early product discussion listed Self, Family, Emergency Contact, Doctor, and Lawyer as candidate entity types under the People module. In practice, a single real person often occupies more than one of these roles at once (e.g., a brother who is also a lawyer and an emergency contact), which separate entity types cannot represent without duplicating the same person as multiple records.

## Decision
All people are modeled as a single `Contact` entity type, carrying one or more **Roles** (Family Member, Doctor, Lawyer, Emergency Contact, Other) rather than being split into separate entity types per role.

## Reason
Modeling roles as a multi-select field avoids duplicate records for the same real person and is more scalable as new roles are needed later — a new role is a new option in a list, not a new entity type and a new set of screens/relationships.

## Alternatives Considered
- **Separate entity type per role** (Doctor, Lawyer, Emergency Contact, Family as distinct types) — rejected: forces duplicate records for anyone with more than one role, and fragments the People module for no behavioral gain.
