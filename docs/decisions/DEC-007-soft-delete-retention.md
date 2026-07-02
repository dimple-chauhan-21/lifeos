# DEC-007: Soft-Deleted Entities Are Retained in Trash for 30 Days

# Document Information

| Field | Value |
|---|---|
| Document | DEC-007 |
| File | `docs/decisions/DEC-007-soft-delete-retention.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/product/03_Feature_Catalogue.md`, `docs/product/00_Glossary.md` |
| Used By | `docs/product/00_Glossary.md` |

---

## Context
`03_Feature_Catalogue.md` defined Soft Delete behavior (removed from views, recoverable for a grace period, then permanently purged) but left the exact retention window as an open question.

## Decision
The Soft Delete lifecycle is: **Deleted → Trash → 30 Days → Permanent Delete.** An entity in Trash can be restored at any point within the 30-day window; after 30 days it is permanently and irreversibly purged.

## Reason
30 days mirrors a widely understood pattern (Google Drive Trash) that users already have correct intuitions about, avoiding the need to teach a novel retention model. It balances giving users a real chance to recover a mistaken deletion against not retaining deleted sensitive data indefinitely.

## Alternatives Considered
- **Indefinite retention until manually emptied** — rejected: works against the product's stance on not retaining data longer than necessary, especially for sensitive document/medical/financial records.
- **Shorter windows (7 days)** — rejected: too easy to lose a recovery window while traveling or inactive.
