# DEC-010: MVP Includes Supporting Entities Alongside Vehicle, Not Vehicle Alone

# Document Information

| Field | Value |
|---|---|
| Document | DEC-010 |
| File | `docs/decisions/DEC-010-mvp-supporting-entities.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/product/01_Product_Vision.md`, `docs/product/03_Feature_Catalogue.md`, `docs/decisions/DEC-001-vehicle-reference-implementation.md` |
| Used By | `docs/product/03_Feature_Catalogue.md` |

---

## Context
Vehicle was chosen as the reference implementation (`DEC-001`) and, on its own, was initially assumed to be sufficient MVP scope for the Assets vertical slice. On review, a Vehicle entity with nothing to relate to cannot actually exercise or prove the Relationships or Expenses capabilities — Vehicle alone proves nothing about the platform.

## Decision
MVP scope includes Vehicle plus a minimal set of supporting entities: **Insurance Policy**, **Expense**, **Document**, and **Contact** (for Dealer/Mechanic relationships) — alongside the full Platform core (Timeline, Attachments, Reminders, Relationships, Custom Fields, Activity History).

## Reason
Vehicle's Relationships tab and Expenses tab are only meaningful — and only testable — if there is something real for a Vehicle to relate to (an Insurance Policy it's insured by, a Document that is its registration certificate, a Contact who services it) and something real to log against it (a fuel or service Expense). Without these, the reference implementation cannot actually validate the platform it's meant to prove out.

## Alternatives Considered
- **Vehicle only, in isolation** — rejected: cannot exercise Relationships or Expenses, the two capabilities most central to the platform's value proposition, so it would fail to validate what a reference implementation is for.
