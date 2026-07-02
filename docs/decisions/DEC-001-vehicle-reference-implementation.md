# DEC-001: Vehicle Is the Reference Implementation of the Entity Platform

# Document Information

| Field | Value |
|---|---|
| Document | DEC-001 |
| File | `docs/decisions/DEC-001-vehicle-reference-implementation.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/product/01_Product_Vision.md`, `docs/product/03_Feature_Catalogue.md` |
| Used By | `docs/product/00_Glossary.md`, `docs/decisions/DEC-010-mvp-supporting-entities.md` |

---

## Context
LifeOS is built platform-first: a generic Entity Platform (Attachments, Timeline, Reminders, Relationships, Custom Fields, Expenses, Notes, Activity Log) is meant to be shared by every domain (Vehicle, Property, Health, Documents, Devices, Pets), rather than each domain being built as an independent module. A single domain needed to be chosen to build first and prove the platform genuinely generic before it's reused elsewhere.

## Decision
**Vehicle** is the reference implementation. The platform is designed and validated against Vehicle first; every other domain is expected to be addable afterward using only a typed domain table, an entity-type config, and an Overview layout — no new platform infrastructure.

## Reason
Vehicle is tangible, easy to reason about, and exercises every core platform capability meaningfully (insurance, service expenses, documents, renewal reminders, dealer/mechanic relationships) without pulling in the added complexity of transaction logic (Finance) or the heaviest sensitivity requirements (Health). It gives an early, demonstrable win while still being a rigorous test of the platform.

## Alternatives Considered
- **Finance** as the reference implementation — rejected: highest daily-use value, but transaction/balance logic would front-load complexity unrelated to validating the generic platform itself.
- **Documents & Identity** as the reference implementation — rejected: too simple (mostly metadata + attachments), would under-test Relationships and Expenses.
- **Health** as the reference implementation — rejected: most sensitive data category, better used later once the platform and its encryption model are already proven.
