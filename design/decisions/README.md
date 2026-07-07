# LifeOS — Design Decision Log

# Document Information

| Field | Value |
|---|---|
| Document | Design Decision Log Index |
| File | `design/decisions/README.md` |
| Version | 1.0 |
| Status | Active |
| Owner | Design Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/design/01_UX_Decision_Record.md` |
| Used By | All sprint folders under `design/` |

---

## Purpose

This is where design-specific decisions made *during* the five design sprints get recorded — the small, in-flight calls made while actually wireframing, building the design system, or specifying interactions (e.g., "changed the Dashboard from 3 columns to 2," "switched the Confirm Action modal's default button from destructive-red to neutral"). It exists to keep a clean separation between two related but distinct logs:

| Log | Scope | Example |
|---|---|---|
| **`docs/decisions/`** (`DEC-XXX`) | Product and architecture decisions — the entity model, platform structure, MVP scope, module boundaries | `DEC-012`: removing the Entity Settings tab |
| **`design/decisions/`** (`UX-XXX`) *(this folder)* | Tactical design-execution decisions made while building sprint deliverables — layout, component behavior, visual refinements | "Changed Dashboard from 3 columns to 2 columns" |

**If a decision made during design actually changes the product or platform** (a new entity type, a new capability, a changed MVP boundary) — it belongs in `docs/decisions/` as a new `DEC-XXX`, not here, regardless of which sprint surfaced it.

## Numbering

`docs/design/01_UX_Decision_Record.md` already uses `UX-001` through `UX-043` for the foundational decisions made before design work began. **New entries in this folder continue that same sequence, starting at `UX-044`**, rather than restarting at `UX-001` — this avoids two different decisions ever sharing the same ID. Number entries sequentially as they're logged; don't skip or reuse numbers.

## Format

Use [`TEMPLATE.md`](./TEMPLATE.md) for every new entry: **Context · Decision · Reason · Alternatives Considered**, plus the standard Document Information header used throughout this repository. Keep entries short — this log is for quick, real decisions as they happen, not a redo of the full Options/Trade-offs analysis already done in `docs/design/01_UX_Decision_Record.md`. If a decision genuinely needs that fuller treatment, it's probably a product-level decision — see above.

## Index

| ID | Title | Sprint | Status | Date |
|---|---|---|---|---|
| *(none yet — entries are added as real design decisions arise during the sprints)* | | | | |

## Adding a New Entry

1. Copy [`TEMPLATE.md`](./TEMPLATE.md) to `UX-0XX-short-title.md`, using the next number after the highest one already in this folder (starting at `044`).
2. Fill in Context, Decision, Reason, and Alternatives Considered.
3. Add a row to the Index table above.
