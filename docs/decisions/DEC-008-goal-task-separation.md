# DEC-008: `Goal` and `Task` Remain Separate Entities; a Goal Owns Tasks

# Document Information

| Field | Value |
|---|---|
| Document | DEC-008 |
| File | `docs/decisions/DEC-008-goal-task-separation.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/product/03_Feature_Catalogue.md`, `docs/product/00_Glossary.md` |
| Used By | `docs/product/00_Glossary.md` |

---

## Context
`03_Feature_Catalogue.md` raised an open question on whether `Goal` is truly distinct from `Task`, or whether Goal should simply be a Task with no fixed due date.

## Decision
`Goal` and `Task` remain two separate entity types in the Planning module. A Goal (e.g., "Lose 10kg") owns one or more Tasks (e.g., "Morning walk," "Meal prep") via a Relationship. Tasks can also exist independently of any Goal.

## Reason
A Goal describes an outcome; a Task describes a unit of work. Collapsing them into one entity type would either force every Task to carry goal-level fields it doesn't need, or force every Goal to behave like a single actionable item when it's really a container for several.

## Alternatives Considered
- **Single `Task` entity with an optional due date standing in for Goal** — rejected: loses the meaningful distinction between a tracked outcome and an actionable step, and complicates the Planning module's UI with a single type trying to serve two purposes.
