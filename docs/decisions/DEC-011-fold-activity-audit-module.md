# DEC-011: Activity & Audit Is Folded Into Dashboard and Settings, Not a Standalone Module

# Document Information

| Field | Value |
|---|---|
| Document | DEC-011 |
| File | `docs/decisions/DEC-011-fold-activity-audit-module.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/product/03_Feature_Catalogue.md`, `docs/product/04_Information_Architecture.md` |
| Used By | `docs/product/03_Feature_Catalogue.md`, `docs/product/04_Information_Architecture.md` |

---

## Context
`03_Feature_Catalogue.md` originally listed `Activity & Audit` as its own top-level Module (#12), holding two things: a Global Activity Feed and a Security Audit Log. While drafting `04_Information_Architecture.md`, it became clear both already have a natural home elsewhere: the Global Activity Feed is conceptually identical to a "Recent Activity" Dashboard widget (already defined), and the Audit Log already surfaces under Settings > Security (already defined in `03_Feature_Catalogue.md`, Section 2.2). Keeping it as a third, separate top-level module added a navigation entry without adding any capability not already reachable elsewhere.

## Decision
`Activity & Audit` is removed as a standalone top-level Module. Its two pieces of functionality are relocated:
- **Global Activity Feed** → a widget under **Dashboard** ("Recent Activity").
- **Security Audit Log** → remains under **Settings > Security**, where it was already defined.

Per-entity Activity History (Timeline-adjacent, defined in the Standard Entity Capability Set) is unaffected — it was never part of this module and continues to live on each Entity.

## Reason
Reduces the Product Hierarchy's top-level node count from 13 to 12 with no loss of functionality, directly satisfying Information Architecture Principle 8 (new/existing top-level structure should stay shallow and predictable). A module that exists only to hold two things which already belong elsewhere adds navigation surface without adding value.

## Alternatives Considered
- **Keep as a standalone module** — rejected: no functional gain over folding it into Dashboard + Settings, and it works against the IA's own shallow-hierarchy principle.
