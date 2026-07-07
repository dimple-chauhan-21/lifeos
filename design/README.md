# LifeOS — Design Workspace

# Document Information

| Field | Value |
|---|---|
| Document | Design Workspace Overview |
| File | `design/README.md` |
| Version | 1.1 |
| Status | Active |
| Owner | Design Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/design/00_Design_Handoff.md`, `docs/design/01_UX_Decision_Record.md`, `design/decisions/README.md` |
| Used By | All future design deliverables in this repository |

---

## Purpose

This is where every UX Design deliverable for LifeOS lives, organized into five sequential sprints that carry the product from approved UX decisions to a fully specified, animation-ready interface — ready for Engineering to build against. It sits alongside, and depends on, the Product and Decision documentation already established in `docs/`:

- **`docs/product/`** — what the product is and does (Vision, PRD, Feature Catalogue, Information Architecture, User Journeys, Screen Inventory)
- **`docs/design/`** — the foundational design decision record (`00_Design_Handoff.md`, `01_UX_Decision_Record.md`)
- **`docs/decisions/`** — the running product/architecture Decision Log (`DEC-XXX`), including UX decisions with product-level impact like `DEC-012`
- **`design/decisions/`** — the design-execution Decision Log (`UX-XXX`, continuing from `UX-044`) for tactical calls made *during* the sprints below — see [`design/decisions/README.md`](./decisions/README.md) for the exact split between the two logs
- **`design/`** *(this folder)* — the actual design deliverables produced sprint by sprint

Nothing in `design/` should introduce a new product-level decision without first logging it in `docs/decisions/`. Tactical, in-flight design decisions (layout tweaks, component behavior refinements) get logged in [`design/decisions/`](./decisions/README.md) instead — see that folder's README for the precise distinction.

## The Five Sprints

| Sprint | Focus | Produces | Depends On |
|---|---|---|---|
| [Sprint 01](./sprint-01/README.md) | Foundations | Sitemap, navigation model, user flows, early template structure | `docs/design/01_UX_Decision_Record.md` |
| [Sprint 02](./sprint-02/README.md) | Low-Fidelity Wireframes | Grayscale, structural wireframes for every screen in `docs/product/06_Screen_Inventory.md` | Sprint 01's templates |
| [Sprint 03](./sprint-03/README.md) | Design System | Components, icons, typography, color (incl. dark mode), spacing/density rules | Sprint 02's wireframes |
| [Sprint 04](./sprint-04/README.md) | High-Fidelity UI | Finished, pixel-level screens across desktop, tablet, and mobile | Sprint 03's design system |
| [Sprint 05](./sprint-05/README.md) | Interactions & Animation | Motion and interaction specs, with reduced-motion fallbacks | Sprint 04's high-fidelity screens |

Each sprint builds directly on the one before it and should not start until the prior sprint's deliverables are **reviewed and accepted**, not merely drafted — sprint completion is tracked as a milestone in `/PROJECT_STATUS.md` at the repository root.

## Other Folders

| Folder | Purpose |
|---|---|
| [`decisions/`](./decisions/README.md) | Design-execution decisions (`UX-044` onward) made during the sprints — distinct from `docs/decisions/`'s product/architecture `DEC-XXX` log |
| [`exports/`](./exports/) | Final, production-ready assets exported for Engineering handoff (e.g., icon sets, design tokens, redlines) — populated as sprints complete, not a work-in-progress space |
| [`assets/`](./assets/) | Source design assets referenced across sprints: `icons/`, `illustrations/`, `logos/`, `fonts/` |

## Workflow Discipline

- **Every sprint folder has its own `README.md`** explaining exactly what belongs there and its exit criteria — read it before adding anything to that sprint.
- **Tactical design decisions made during a sprint get logged in [`design/decisions/`](./decisions/README.md)** as a new `UX-XXX` entry (continuing from `UX-044`). **Decisions that change the product or platform itself get logged in `docs/decisions/`** as a new `DEC-XXX` entry, exactly as Product has done throughout this project (see `docs/design/00_Design_Handoff.md`, Section 12, Recommendation 7).
- **`PROJECT_STATUS.md` is updated only at milestone acceptance** — when a sprint's deliverables are reviewed and accepted by the Product Owner, not after each individual file is added.
