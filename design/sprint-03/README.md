# Sprint 03 — Design System

# Document Information

| Field | Value |
|---|---|
| Document | Sprint 03 README |
| File | `design/sprint-03/README.md` |
| Version | 1.1 |
| Status | Active |
| Owner | Design Team |
| Last Updated | 2026-07-02 |
| Depends On | `design/sprint-02/low-fidelity-wireframes/`, `docs/design/01_UX_Decision_Record.md` |
| Used By | `design/sprint-04/` onward |

---

## Purpose

Sprint 03 turns the approved wireframes into a real, reusable design system — the visual vocabulary (color, type, spacing, icons, components) that every high-fidelity screen in Sprint 04 will be built from. This is where the Visual Language direction (UX-040), Motion philosophy inputs (UX-041), and Accessibility baseline (UX-036–038) from `docs/design/01_UX_Decision_Record.md` become concrete, testable tokens and components — not new decisions. If a tactical design-execution decision surfaces while building the system (e.g., a spacing or component adjustment), log it in [`design/decisions/`](../decisions/README.md) as a new `UX-XXX` entry (continuing from `UX-044`). If it turns out to actually be a product-level decision, log it in `docs/decisions/` as a `DEC-XXX` instead.

## What Belongs in Each Folder

| Folder | Contents |
|---|---|
| `design-system/` | The overall system documentation — principles, spacing scale, density rules, the calm/trustworthy tone direction (UX-040) expressed as concrete guidelines |
| `components/` | Specs for individual reusable components: the entity chip (UX-025), Confirm Action modal (UX-043), Capability Tab Shell (UX-010), Filterable List Shell (UX-017/018), urgency-tier treatment (UX-007) |
| `icons/` | The icon system covering all 12 Modules and 28 Entity Types (resolves Open UX Decision #8 from `docs/design/00_Design_Handoff.md`) |
| `typography/` | Type scale and usage rules |
| `colors/` | Color palette and tokens — including the dark mode decision (Open UX Decision #7) and the WCAG 2.1 AA contrast minimums from UX-038 |
| `review/` | Sign-off notes, feedback, and the record of Product Owner approval for this sprint's deliverables before Sprint 04 begins |

## Exit Criteria

A complete, documented design system exists — every component used across the Sprint 02 wireframes has a corresponding spec here. Reviewed and accepted, per `PROJECT_STATUS.md`, before Sprint 04 begins.
