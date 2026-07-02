# DEC-006: `Reminder` and `Task` Are Kept as Distinct Concepts

# Document Information

| Field | Value |
|---|---|
| Document | DEC-006 |
| File | `docs/decisions/DEC-006-reminder-vs-task.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/product/03_Feature_Catalogue.md`, `docs/product/00_Glossary.md` |
| Used By | `docs/product/00_Glossary.md` |

---

## Context
"Reminder" (a platform capability attachable to any entity) and "Task" (a Planning-module entity) risked being conflated into a single, weaker to-do concept if not explicitly distinguished.

## Decision
`Reminder` and `Task` remain two separate concepts:
- **Reminder** — a lightweight, date-triggered notification attached to any entity (e.g., "Renew insurance tomorrow"). Fires a notification, then is marked done/snoozed/dismissed. No status workflow.
- **Task** — a fuller to-do entity in the Planning module, with due date, priority, and status (Open / In Progress / Done) (e.g., "Call insurance company," "Upload new policy," "Verify RC"). Can itself carry Reminders.

## Reason
These serve genuinely different needs: a Reminder is a single notification trigger tied to any entity in the system; a Task is a trackable unit of work with its own lifecycle, often one of several steps toward a Goal. Merging them would either overload Reminder with a status workflow it doesn't need everywhere, or force every entity's simple "remind me" need through the heavier Task model.

## Alternatives Considered
- **Single unified "Reminder/Task" concept** — rejected: forces a false choice between a lightweight notification and a trackable to-do, degrading both use cases.
