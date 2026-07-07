# Sprint 04 — High-Fidelity UI

# Document Information

| Field | Value |
|---|---|
| Document | Sprint 04 README |
| File | `design/sprint-04/README.md` |
| Version | 1.0 |
| Status | Active |
| Owner | Design Team |
| Last Updated | 2026-07-02 |
| Depends On | `design/sprint-03/design-system/`, `design/sprint-02/low-fidelity-wireframes/` |
| Used By | `design/sprint-05/` onward, Engineering (frontend build) |

---

## Purpose

Sprint 04 applies the Sprint 03 design system to every wireframe from Sprint 02, producing real, pixel-level screens across every required breakpoint. This is the first sprint where the product is actually visible in near-final form — and the first point at which Engineering can start referencing concrete visuals alongside `docs/product/` and `docs/design/`.

Per the Responsive Strategy (UX-039), each of the three breakpoints gets an **intentionally different layout**, not a scaled copy of the same one — the sidebar becomes a bottom nav/drawer on mobile, the Capability Tab Shell collapses to an accordion, and list views reduce columns. Design all three, not just desktop-first with mobile as an afterthought.

## What Belongs in Each Folder

| Folder | Contents |
|---|---|
| `high-fidelity/` | The complete set of finished, high-fidelity screens (source of truth for the overall set) |
| `desktop/` | Desktop-breakpoint variants |
| `tablet/` | Tablet-breakpoint variants |
| `mobile/` | Mobile-breakpoint variants, including the accordion tab and bottom-nav patterns from UX-010 and UX-039 |
| `review/` | Sign-off notes, feedback, and the record of Product Owner approval for this sprint's deliverables before Sprint 05 begins |

## Exit Criteria

Every screen in the Screen Inventory (`docs/product/06_Screen_Inventory.md`) has a finished high-fidelity design at all three breakpoints, consistent with the Sprint 03 design system. Reviewed and accepted, per `PROJECT_STATUS.md`, before Sprint 05 begins.
