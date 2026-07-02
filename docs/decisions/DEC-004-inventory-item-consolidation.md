# DEC-004: Furniture and Appliance Are One `Inventory Item` Entity With a Category Field

# Document Information

| Field | Value |
|---|---|
| Document | DEC-004 |
| File | `docs/decisions/DEC-004-inventory-item-consolidation.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/product/03_Feature_Catalogue.md`, `docs/product/00_Glossary.md` |
| Used By | `docs/product/03_Feature_Catalogue.md` |

---

## Context
Early product discussion risked three overlapping entity concepts describing the same underlying thing (a physical item in a home): `Assets > Furniture`, `Assets > Device`, and `Home > Appliance`. Furniture and Appliance in particular differ only by category, not by structure.

## Decision
Furniture and Appliance are consolidated into a single `Inventory Item` entity type in the **Home** module, distinguished by a **Category** field (Furniture, Appliance, Tool, Decoration, Other). `Device` remains a separate entity type under **Assets**, reserved for higher-value, portable personal electronics (laptop, phone, camera) tracked individually for warranty/insurance reasons regardless of which room they're in.

## Reason
Avoids near-duplicate entity types for the same concept. The Home vs. Assets distinction is preserved by module placement and intent (location-scoped household inventory vs. ownership-scoped personal electronics), not by inventing more entity types.

## Alternatives Considered
- **Keep Furniture and Appliance as separate entity types** — rejected: no structural difference beyond category; adds engineering cost without capability gain.
