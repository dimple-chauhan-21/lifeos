# DEC-005: The `Note` Entity Is Renamed `Knowledge Note` to Avoid Collision With the `Notes` Capability

# Document Information

| Field | Value |
|---|---|
| Document | DEC-005 |
| File | `docs/decisions/DEC-005-knowledge-note-vs-notes-naming.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/product/03_Feature_Catalogue.md`, `docs/product/00_Glossary.md` |
| Used By | `docs/product/03_Feature_Catalogue.md`, `docs/product/00_Glossary.md` |

---

## Context
LifeOS has two distinct concepts that were both informally called "Note": (1) the **Notes capability**, a lightweight freeform annotation attachable to any entity (e.g., "Dealer notes" on a Vehicle), and (2) a standalone, first-class **Note entity** in the Knowledge module (e.g., "Grocery list"). Left unresolved, this collision would eventually produce ambiguous terms like "Note," "Notes," "Entity Note," "Entity Notes" across documentation and, later, code.

## Decision
The standalone entity is renamed **Knowledge Note**. The capability keeps the name **Notes**. A Knowledge Note does not itself carry the Notes capability (it would be redundant, since a Knowledge Note already *is* freeform text).

## Reason
Resolving this now, before any schema or UI work begins, prevents a naming collision that would otherwise be expensive to untangle later. The rename is scoped to product documentation only — the platform capability's public name ("Notes") is unchanged.

## Alternatives Considered
- **"Personal Note"** — considered as an alternative rename; **"Knowledge Note"** was preferred because it names the entity by its owning module (consistent with naming patterns like "Medical Record"), making the entity's home immediately obvious.
