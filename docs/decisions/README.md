# LifeOS — Decision Log

# Document Information

| Field | Value |
|---|---|
| Document | Decision Log Index |
| File | `docs/decisions/README.md` |
| Version | 1.0 |
| Status | Active |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/product/00_Glossary.md` |
| Used By | All Product, Design & Engineering Documents |

---

This directory records every major product and architecture decision for LifeOS, in the order they were made. Each decision gets its own file (`DEC-XXX-short-title.md`) so that future contributors understand *why* something is the way it is, not just *what* it is — and don't accidentally reverse a deliberate decision without knowing its reasoning.

Terminology used below follows [`docs/product/00_Glossary.md`](../product/00_Glossary.md).

## Index

| ID | Title | Status | Date |
|---|---|---|---|
| [DEC-001](./DEC-001-vehicle-reference-implementation.md) | Vehicle is the reference implementation of the Entity Platform | Approved | 2026-07-02 |
| [DEC-002](./DEC-002-document-entity-consolidation.md) | Documents (Passport, License, Certificate, etc.) are one `Document` entity with a Category field | Approved | 2026-07-02 |
| [DEC-003](./DEC-003-contact-entity-consolidation.md) | People (Doctor, Lawyer, Family, etc.) are one `Contact` entity with multi-select Roles | Approved | 2026-07-02 |
| [DEC-004](./DEC-004-inventory-item-consolidation.md) | Furniture and Appliance are one `Inventory Item` entity with a Category field | Approved | 2026-07-02 |
| [DEC-005](./DEC-005-knowledge-note-vs-notes-naming.md) | The `Note` entity is renamed `Knowledge Note` to avoid collision with the `Notes` capability | Approved | 2026-07-02 |
| [DEC-006](./DEC-006-reminder-vs-task.md) | `Reminder` and `Task` are kept as distinct concepts | Approved | 2026-07-02 |
| [DEC-007](./DEC-007-soft-delete-retention.md) | Soft-deleted entities are retained in Trash for 30 days before permanent deletion | Approved | 2026-07-02 |
| [DEC-008](./DEC-008-goal-task-separation.md) | `Goal` and `Task` remain separate entities; a Goal owns Tasks via Relationship | Approved | 2026-07-02 |
| [DEC-009](./DEC-009-hybrid-relationship-model.md) | Relationships use a hybrid model: a closed set of System Relationships plus user-defined Custom Relationships | Approved | 2026-07-02 |
| [DEC-010](./DEC-010-mvp-supporting-entities.md) | MVP includes Insurance Policy, Expense, Document, and Contact alongside Vehicle, not Vehicle alone | Approved | 2026-07-02 |
| [DEC-011](./DEC-011-fold-activity-audit-module.md) | `Activity & Audit` is folded into Dashboard (Recent Activity) and Settings (Audit Log), not kept as a standalone module | Approved | 2026-07-02 |
| [DEC-012](./DEC-012-remove-entity-settings-tab.md) | `Entity Settings` is removed as a standalone Capability Tab; Archive/Delete move to a `⋮` overflow menu on Entity Overview | Approved | 2026-07-02 |
| [DEC-013](./DEC-013-v1-backup-strategy.md) | V1 backups: automated daily Postgres dumps to a local Docker-mounted directory, kept provider-agnostic for future cloud storage | Approved | 2026-07-02 |

## Adding a New Decision

1. Create `DEC-XXX-short-title.md` using the next sequential number.
2. Include: Context, Decision, Reason, Alternatives Considered, Status, Date, Related Documents.
3. Add a row to the Index table above.
