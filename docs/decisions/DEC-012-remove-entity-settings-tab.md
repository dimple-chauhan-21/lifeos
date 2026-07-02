# DEC-012: Entity Settings Is Removed as a Standalone Capability Tab

# Document Information

| Field | Value |
|---|---|
| Document | DEC-012 |
| File | `docs/decisions/DEC-012-remove-entity-settings-tab.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/design/01_UX_Decision_Record.md`, `docs/product/06_Screen_Inventory.md`, `docs/product/04_Information_Architecture.md` |
| Used By | `docs/product/06_Screen_Inventory.md`, `docs/product/04_Information_Architecture.md`, `docs/design/01_UX_Decision_Record.md` |

---

## Context
The Standard Entity Capability Set (`03_Feature_Catalogue.md`, Section 2.1) included an "Entity Settings" tab, and `06_Screen_Inventory.md` described its content as "minimal in V1 — Archive/Delete live here." While writing `01_UX_Decision_Record.md`, it became clear this tab holds no content beyond two actions that already have a defined, lighter-weight interaction pattern elsewhere: Archive and Soft Delete are immediate actions with an Undo toast (`docs/design/01_UX_Decision_Record.md`, UX-043), not destinations a user navigates to. A full seventh Capability Tab dedicated to two menu items is unjustified UI surface — comparable to a product like Notion not having a "Page Settings" tab, only a `...` overflow menu with Rename / Duplicate / Archive / Delete.

## Decision
"Entity Settings" is removed as a standalone Capability Tab. Archive and Delete are instead surfaced via a small overflow (`⋮`) menu on the Entity Overview header, available from any Entity's Overview without needing its own tab. The Entity's capability tabs become: **Overview, Timeline, Relationships, Attachments, Expenses, Reminders, Activity History** — plus the `⋮` menu (Archive, Delete) — rather than eight tabs including Settings.

## Reason
Removes one tab from the Capability Tab Shell (`docs/design/01_UX_Decision_Record.md`, UX-010) everywhere it's used across all 28 Entity Types, and removes one entry from the Screen Catalogue, tightening `06_Screen_Inventory.md`'s screen-count estimate further (Generic Entity Platform screens: 13 → 12; overall total: ~40 → ~39, or ~37 → ~36 after the previously recommended Add/Edit and Confirm Action merges). This is a pure simplification: no capability or functionality is lost, only a redundant navigation destination.

## Alternatives Considered
- **Keep Entity Settings as its own tab** — rejected: no content justifies a dedicated tab once Archive/Delete are already immediate actions per UX-043; keeping it would mean shipping an empty or near-empty tab on every Entity Type.
