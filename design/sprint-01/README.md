# Sprint 01 — Foundations: Sitemap, Navigation, User Flows, Templates

# Document Information

| Field | Value |
|---|---|
| Document | Sprint 01 README |
| File | `design/sprint-01/README.md` |
| Version | 1.0 |
| Status | Active |
| Owner | Design Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/design/00_Design_Handoff.md`, `docs/design/01_UX_Decision_Record.md` |
| Used By | `design/sprint-02/` onward |

---

## Purpose

Sprint 01 translates the approved UX Decision Record (`docs/design/01_UX_Decision_Record.md`) and Design Handoff (`docs/design/00_Design_Handoff.md`) into the first visual artifacts: where things live, how a user moves between them, and the reusable template shapes everything downstream is built on. Nothing in this sprint is high-fidelity — it establishes structure, not visual style.

**Do not start this sprint until the decisions flagged "Requiring Product Owner Approval" in `docs/design/01_UX_Decision_Record.md` are resolved** — in particular UX-001 (Navigation), UX-008 (Generic Entity Layout), and UX-013 (Form Structure), since this sprint's deliverables are direct expressions of those decisions.

## What Belongs in Each Folder

| Folder | Contents |
|---|---|
| `sitemap/` | A visual sitemap of all 12 Modules and their Entity Types, derived directly from the Product Hierarchy in `docs/product/04_Information_Architecture.md`, Section 1 |
| `navigation/` | Diagrams of the four navigation layers (Global, Local, Context, Cross-Entity) and the resolved primary navigation pattern (UX-001), including the responsive variants per breakpoint (UX-039) |
| `user-flows/` | Flow diagrams for the journeys in `docs/product/05_User_Journeys.md`, redrawn as navigable screen-to-screen flows rather than behavioral prose |
| `templates/` | Early structural specs (not high-fidelity) for the six reusable templates named in `docs/design/00_Design_Handoff.md`, Section 6: Entity Form, Entity Overview, Capability Tab Shell, Filterable List Shell, Confirm Action, Attachment/File Viewer |
| `review/` | Sign-off notes, feedback, and the record of Product Owner approval for this sprint's deliverables before Sprint 02 begins |

## Exit Criteria

This sprint is complete only once its deliverables are reviewed and accepted by the Product Owner (see `PROJECT_STATUS.md`) — not merely drafted. Sprint 02 (Low-Fidelity Wireframes) depends on the templates defined here, so incomplete or unapproved templates should not carry forward.
