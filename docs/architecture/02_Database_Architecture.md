# LifeOS — Database Architecture

# Document Information

| Field | Value |
|---|---|
| Document | Database Architecture |
| File | `docs/architecture/02_Database_Architecture.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Engineering Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/architecture/00_Engineering_Overview.md`, `docs/architecture/01_System_Architecture.md`, `docs/product/00_Glossary.md` |
| Used By | Migration implementation, `docs/architecture/03_API_Design.md` (or equivalent next document) |

---

## Purpose

`docs/architecture/00_Engineering_Overview.md`, Section 7 sketched the database strategy at a high level; `01_System_Architecture.md` established the Service ownership map every table ultimately serves. This document goes to full architectural depth on the database itself — the philosophy, models, and rules governing every table — **without writing SQL**. No column types, no DDL, no migration files: those come after this document is approved, per the confirmed engineering process.

---

## 1. Database Philosophy

- **One database, one schema.** No schema-per-tenant or database-per-tenant, even though the architecture is SaaS-ready — tenancy is expressed through a column (`owner_id`), not database-level partitioning, which would be premature operational complexity for a currently single-user product (see Section 21).
- **Strong typing over generic storage, except where real variability exists.** The `docs/decisions/` consolidations (Document, Contact, Inventory Item) already rejected "one entity type per near-duplicate concept" in favor of typed Category fields — the database continues that discipline: typed columns wherever a domain's fields are actually fixed, and the Custom Field mechanism (Section 7) reserved specifically for genuine, per-user variability.
- **Referential integrity is enforced by the database itself**, wherever structurally possible — this was the deciding factor in choosing the shared base `entities` table over fully independent per-type tables (`docs/architecture/00_Engineering_Overview.md`, Section 7): a real foreign key is stronger than an application-level convention.
- **Every table exists to serve exactly one Service.** The schema is a direct, intentional mirror of the Service Boundaries already defined in `docs/architecture/01_System_Architecture.md`, Section 5 — not an independently-designed layer that happens to be read by services.
- **Growth-oriented by construction.** Adding the 29th Entity Type should mean *one new table plus a few rows of registration data* — never a change to an existing table. This is the database-level expression of the Platform Layer / Domain Layer dependency rule (`01_System_Architecture.md`, Section 1).

---

## 2. Entity Ownership Model

Ownership (`owner_id`) is recorded in **exactly one place: the base `entities` table.** No detail table (`vehicles`, `contacts`, ...) and no Platform table (`attachments`, `reminders`, ...) carries its own `owner_id` — they inherit ownership transitively through their `entity_id` reference back to `entities`.

- **Why not duplicate `owner_id` everywhere:** a single source of truth for "who owns this" means there is never a risk of a detail row and its base row disagreeing about ownership, and — critically for Section 21 — evolving the tenancy model later means changing the meaning of **one column in one table**, not auditing every table in the schema.
- **The one case this doesn't fully cover:** a `Relationship` connects *two* entities, which could in principle belong to different owners. The database cannot cheaply express "both sides of this row must share the same `owner_id`" as a simple declarative constraint. This is a deliberate, accepted gap — enforced instead as an invariant in `RelationshipService` (`docs/architecture/01_System_Architecture.md`, Section 5), not silently assumed away.
- **V1 reality:** exactly one `owner_id` value exists (a single seeded user), but the column is real, populated, and enforced from day one — per the original "SaaS-ready architecture" commitment, this is *activated* later, not *added* later.

---

## 3. Base Entity Strategy

The `entities` table is the architectural anchor of the entire Platform Layer (`docs/architecture/01_System_Architecture.md`, Section 1). It holds **only what is universally true of every Entity, regardless of type**: an identifier, its type, its owner, its name, favorite status, lifecycle state, and timestamps. Nothing type-specific belongs here, ever — that discipline is what keeps this table stable as new Domain Layer packages are added indefinitely.

- **`entity_type` is a controlled vocabulary, not a freeform string.** Rather than a database enum (which requires a migration to alter every time a new type is added, working against the "register, don't restructure" growth goal), `entity_type` should reference a small **entity type registry** — a lookup table populated by each Domain package announcing itself. Adding a new Domain Entity Type becomes a data insertion (one registry row) plus one new migration for its own detail table, never an alteration to an existing enum or table.
- **Why commonly-needed domain concepts (like "has an expiry date") don't live on the base table**, even though many domains share the idea: "expiry" isn't universal (a Contact has none). Keeping `entities` strictly universal is what keeps it stable. Cross-domain features that need to know about expiry-like fields (the Dashboard's Expiring Soon widget) work by having each Domain register *which of its own fields* represent an expiry-like date — the same registration pattern used for Search (Section 11) — rather than the base table growing a speculative `expiry_date` column that most Entity Types would leave null.

---

## 4. Detail Table Strategy

One table per Domain Entity Type (`vehicles`, `contacts`, `insurance_policies`, `documents`, ...), each in a strict 1:1 relationship with a base `entities` row (formalized at the key level in Section 15). A detail table holds **only fields genuinely specific to that Entity Type** — a Vehicle's VIN, a Contact's phone number — with real, type-appropriate constraints (Section 17).

- **The governing rule, expressed at the schema level**: a detail table never has a foreign key pointing to another detail table. This is the database-level enforcement of `01_System_Architecture.md`, Section 2's rule that "a Domain package never imports another Domain package directly." Any connection between two Entity Instances — regardless of their types — goes through the generic `relationships` table (Section 5), referencing `entities.id` on both sides, never a direct `vehicles.id → insurance_policies.id` foreign key.
- Shared *concepts* across domains (cost tracking, expiry tracking) are expressed through Platform tables and Relationships, not duplicated as similarly-named columns across many detail tables where a generic mechanism already covers the need.

---

## 5. Relationship Model

**One `relationships` table serves every possible connection between any two Entities, regardless of their types** — a Vehicle-to-Insurance-Policy link and a Contact-to-Contact link are structurally identical rows, differing only in `relationship_type`.

- Two entity-reference columns (conventionally `entity_a_id`, `entity_b_id`), **both referencing `entities.id`** — never a detail table. This is the clearest architectural payoff of the confirmed base-table decision: without a shared `entities` table, this one generic table would be impossible to build with real foreign keys at all.
- `relationship_type` plus an `is_system_type` flag implements the hybrid model from `docs/decisions/DEC-009-hybrid-relationship-model.md`.
- **Directionality — one row per relationship, not two.** Although some Relationship Types are directional (`Owns`/`Belongs To` are inverses) and others are symmetric (`Related To`), the architecture stores **exactly one row per actual relationship**, with `entity_a_id` conventionally holding the "subject" side where direction is meaningful. Querying "everything related to Entity X" means checking both columns (`entity_a_id = X OR entity_b_id = X`), which is a marginally less trivial query than a single indexed lookup — but storing the relationship twice (once per direction) would risk the two mirrored rows silently drifting out of sync after an edit, which is a worse failure mode than a slightly less trivial read query.
- **Uniqueness**: the combination of (`entity_a_id`, `entity_b_id`, `relationship_type`) should be constrained unique, preventing the same relationship from being recorded twice by accident.

---

## 6. Attachment Model

A single `attachments` table serves every Entity Type: a reference back to `entities.id`, file metadata (filename, MIME type, size, upload timestamp), and a storage reference — a pointer into MinIO, never the file bytes themselves.

- **No folder/hierarchy concept**, by design — no self-referencing "parent attachment" or "folder" column exists on this table. This is the schema-level enforcement of `docs/design/01_UX_Decision_Record.md`, UX-031 (flat, filterable Attachments) and `docs/product/04_Information_Architecture.md`, Principle 2 (no nesting below Entity Type).
- **No versioning**, per `docs/product/00_Glossary.md`'s existing resolution — there is no "supersedes" or "version of" column. Re-uploading a file creates an entirely new `attachments` row; the old one persists independently unless the user explicitly deletes it.

## 7. Custom Field Model

Two tables, matching the Definition/Value distinction already canonical in `docs/product/00_Glossary.md`, Section 2:

- **`custom_field_definitions`**: one row per (`entity_type`, field name), declaring the field's data type (text, number, date, boolean, single-select) and whether it's required. Managed centrally per Entity Type (Settings), not per instance.
- **`custom_field_values`**: one row per (Entity Instance, Custom Field Definition), holding the actual value.

**A real architectural decision on how a Custom Field Value is stored**: rather than one generic, untyped column (e.g., a single text or JSONB field for every value regardless of declared type), this architecture uses **multiple, nullable, type-specific columns** (a text value, a numeric value, a date value, a boolean value) on `custom_field_values`, with only the one column matching the field's declared type ever populated for a given row. This costs a handful of unused nullable columns per row, but buys real database-level typing, sorting, and filtering on Custom Field values — directly required by Global Search's ability to filter and rank on them (`docs/product/04_Information_Architecture.md`, Section 8). A single untyped column would push all of that type-awareness into application code and make numeric/date filtering meaningfully harder to do correctly. This is flagged in the Quality Review below as the one modeling choice most worth revisiting if it proves awkward once real Custom Fields are built.

## 8. Audit Model

`audit_log` is architecturally distinct from `activity_log` (Section 9) and from Operational Logging (`docs/product/00_Glossary.md`, Section 4) — it exists solely for security-relevant events: login, logout, failed login, data export, sensitive-field access. Rows reference the acting user, an event type, a timestamp, and minimal context (e.g., originating IP) — not necessarily a specific Entity, since many audit events (login, export) aren't scoped to one.

- **Immutability is an architectural property, not just a convention.** No Service exposes an update or delete path for this table — `AuditService` (an addition to the Service map in `01_System_Architecture.md`, Section 5) only ever inserts. This should be reinforced at the database level (e.g., revoking UPDATE/DELETE privileges on this table from the application's database role) as a defense-in-depth measure, not relied upon as an application-layer promise alone.

## 9. Reminder Model

`reminders`: a reference to `entities.id`, a title, a due date, an optional recurrence rule, and a status (pending / done / snoozed / dismissed, per `docs/design/01_UX_Decision_Record.md`, UX-035).

- **Recurring reminders are one row, not a growing series of rows.** A recurring Reminder's due date advances in place after it fires, rather than spawning a new row per occurrence — this avoids unbounded row growth for something like a decade-long monthly reminder, and matches the product-level model where a Reminder is a single, ongoing thing, not a series.
- **Completed or dismissed reminders are never deleted** — their status changes, and that status change is itself a Timeline-worthy event (per `docs/product/05_User_Journeys.md`, J2.2), which feeds into Section 10 below.

## 10. Timeline Model

Per `docs/product/00_Glossary.md`: **Timeline is the union of `activity_log` (system-generated) and `timeline_entries` (user-logged)** — both reference `entities.id`.

**Architecturally, there is no separate, physically-stored "timeline" table.** Maintaining one would mean keeping a third table in sync with the two actual sources of truth every time either changes — a real consistency risk for no benefit. Instead, `TimelineService` (`docs/architecture/01_System_Architecture.md`, Section 5) computes the Timeline at read time as an ordered union of `activity_log` and `timeline_entries` rows for the requested entity. This keeps exactly two tables as the source of truth, with "Timeline" remaining a query/view concept — matching how the Glossary already defines it, not introducing a third, competing physical representation.

---

## 11. Search Indexing Strategy

Rather than maintaining a search index directly on the `entities` table (which would require every Domain's detail-table edits to somehow reach back and update a table they don't own — a violation of the Service Boundaries in `01_System_Architecture.md`, Section 5), search indexing gets its **own dedicated table, owned exclusively by `SearchService`**: an entity reference, a full-text search vector, and a last-indexed timestamp.

- Each Domain Service, on create/update, tells `SearchService` which of its own fields are searchable (the same Configuration-driven registration pattern used for Capability applicability, `docs/product/03_Feature_Catalogue.md`, Section 6) — `SearchService` maintains the search vector; no Domain Service or the base `entities` table needs to know how search indexing actually works internally.
- This vector combines: the entity's name, its Domain-registered searchable fields, its Tags, its Custom Field text values, and Attachment/Document filenames — matching the scope already defined in `docs/product/04_Information_Architecture.md`, Section 8.
- A dedicated PostgreSQL full-text index (Section 18) is used, per the confirmed "Postgres FTS first, defer a dedicated search engine" strategy (`docs/architecture/00_Engineering_Overview.md`, Section 12).

## 12. Soft Delete Strategy

Implemented entirely through `entities.lifecycle_state` (`active` / `archived` / `trashed`) and a nullable `trashed_at` timestamp — no other table needs its own lifecycle state.

- **No cascading state change to related Platform rows.** When an Entity is soft-deleted, its Attachments, Relationships, Reminders, Notes, etc. are **not** individually marked deleted — they remain exactly as they are in the database, simply rendered invisible because every query path joins through `entities.lifecycle_state = 'active'` by default (or explicitly requests Trashed/Archived, e.g., for the Archive & Trash List). This is a deliberate simplification: it means no Platform table needs its own lifecycle column, and restoring an Entity from Trash instantly and correctly restores the visibility of everything attached to it, with no separate "un-delete the children" step.
- **Relationships spanning a trashed Entity behave the same way** — the `relationships` row is untouched in the database; it's simply not traversable while either side is trashed (per `docs/product/05_User_Journeys.md`, J8.2 — "hidden... not left dangling"), and becomes traversable again automatically the moment the entity is restored, with no additional bookkeeping required.

## 13. Archiving Strategy

Archiving uses the same `lifecycle_state` column, value `archived`, with `trashed_at` remaining null. The only structural difference between Archive and Trash is that **Archive is not time-bound** (no automatic purge) while **Trash is** (the 30-day Celery purge job, per `docs/decisions/DEC-007-soft-delete-retention.md`) — both are otherwise identical mechanisms, differing only in which `lifecycle_state` value is set and whether `trashed_at` is populated.

## 14. Naming Conventions

| Convention | Rule | Example |
|---|---|---|
| Tables | Plural, `snake_case` | `entities`, `custom_field_definitions` |
| Primary key column | Always `id` | `entities.id` |
| Foreign keys | `{referenced_singular}_id` | `entity_id`, `owner_id` |
| Disambiguated foreign keys | When a table has more than one reference to the same target, suffix by role, not by target name alone | `relationships.entity_a_id` / `entity_b_id`, never two columns both named `entity_id` |
| Timestamps | `created_at`, `updated_at` on every table; `trashed_at` (nullable) on `entities` only | — |
| Booleans | Prefixed `is_`/`has_` | `is_favorite`, `is_system_type`, `is_required` |
| Enum-like values | Backed by a constrained/lookup pattern (Section 3), not free text | `entity_type`, `lifecycle_state`, `field_type` |

## 15. Primary Key Strategy

**Every table uses a UUID primary key** — including `entities` and every detail and Platform table — never an auto-incrementing integer. **One deliberate exception**: `entity_types` (Section 3) is keyed by `entity_type` itself, a string natural key, not a UUID — it is a small, fixed, non-sensitive controlled vocabulary rather than owner-scoped data, so the ID-enumeration rationale below doesn't apply, and every reference to `entity_type` elsewhere in this document already treats it as a readable string, not an opaque ID.

- **Why UUIDs**: sequential integer IDs leak information (how many Vehicles exist, ID-enumeration attacks) that compounds the IDOR risk already flagged as a top security concern (`docs/architecture/00_Engineering_Overview.md`, Section 15); UUIDs also support future scenarios this architecture is explicitly kept open to — merging data across self-hosted instances, or migrating a single-user instance into a hosted multi-tenant one (Section 21) — far more gracefully than integers ever could.
- **Detail tables use the same UUID as their corresponding `entities` row** — `entity_id` on a detail table is *both* its primary key and its foreign key to `entities.id`, not an independent auto-incrementing key of its own. This is what makes the 1:1 relationship between a base row and its detail row airtight at the schema level, not just a convention two separate keys happen to follow.

---

## 16. Foreign Key Strategy

Real, database-enforced foreign keys are used wherever a relationship is structurally guaranteed: every detail table → `entities`, every Platform table (`attachments`, `reminders`, `notes`, `timeline_entries`, `custom_field_values`, ...) → `entities`, `custom_field_values` → `custom_field_definitions`, and both sides of `relationships` → `entities` (Section 5).

- **Cascading behavior is conceptually tied to the Soft Delete model (Section 12)**: because real, permanent deletion only ever happens once, at the 30-day Trash purge (`docs/decisions/DEC-007`), foreign keys should cascade at that point — deleting an `entities` row should cascade-delete its detail row and every Platform row referencing it. This means the purge job is the **only** code path that performs genuine hard deletes, and it can rely on the database's own cascade behavior rather than the application manually deleting from a dozen tables in the correct order — reducing the risk of orphaned rows if a step were ever missed in application code.
- `relationships` foreign keys point to `entities.id` specifically, never to a detail table — already established in Section 5, restated here as a foreign-key-specific rule.

## 17. Constraints

| Constraint | Applies To | Purpose |
|---|---|---|
| `NOT NULL` | `owner_id`, `entity_type` on `entities`; `entity_id` on every Platform table | These values must always exist for a row to be meaningful |
| `UNIQUE (entity_a_id, entity_b_id, relationship_type)` | `relationships` | Prevents the same relationship from being recorded twice |
| `UNIQUE (entity_type, field_name)` | `custom_field_definitions` | Prevents defining the same Custom Field twice for one Entity Type |
| `CHECK` (constrained value set) | `lifecycle_state`, `field_type` where not backed by a lookup table | Enforces the closed set of valid values at the database level, not just in application code |

**A known, deliberately accepted gap**: "both sides of a `Relationship` must share the same `owner_id`" (Section 2) cannot be cheaply expressed as a declarative database constraint given the polymorphic-feeling, self-referential shape of the `relationships` table. This is enforced in `RelationshipService` instead. It's stated here explicitly so it's a known, accepted boundary between database-level and application-level integrity — not an oversight discovered later.

## 18. Indexing Philosophy

- **Every foreign key column is indexed.** Unlike some database systems, PostgreSQL does not do this automatically — every `entity_id` column across every Platform and detail table, plus `owner_id`, gets an explicit index.
- **One composite index matters more than any other**: (`owner_id`, `entity_type`, `lifecycle_state`) on `entities` — this is the shape of the single most common query in the entire product (list all active Vehicles for this owner, per the Filterable List Shell, `docs/design/00_Design_Handoff.md`, Section 6).
- **A GIN index** on the `search_index` table's search vector column (Section 11).
- **Avoid speculative indexing.** Index what the known query patterns (sort/filter behavior already specified in `docs/design/01_UX_Decision_Record.md`, UX-017/018) actually need; revisit with real query-plan analysis once genuine usage data exists rather than indexing preemptively against imagined access patterns.

## 19. Migration Strategy

- **Alembic, one linear migration history** — no branching migration heads in the normal course of development, consistent with the single-repository, single-team model established in `docs/architecture/00_Engineering_Overview.md`.
- **Every migration must be reversible** (a working `downgrade`, not just `upgrade`) — already a CI-enforced check per `docs/architecture/00_Engineering_Overview.md`, Section 17.
- **The single most important migration invariant**: adding a new Domain Entity Type should produce a migration that creates exactly one new detail table (plus its registry row, Section 3) — it should **never** need to alter `entities` or any Platform table. A migration that does alter a Platform table to accommodate a new domain is a signal that the Platform/Domain boundary (`docs/architecture/01_System_Architecture.md`, Section 1) has been violated somewhere, and should be treated as a design defect to fix, not merged as routine schema evolution.
- **Migrations are the only sanctioned path for schema change** — no ad hoc schema edits against a running database, even in local development, so the migration history remains the single, complete source of truth for what the schema actually is at any point in time.

## 20. Backup & Restore Considerations

Building on `docs/decisions/DEC-013-v1-backup-strategy.md` (daily Postgres dumps to a local Docker-mounted directory):

- **A complete backup requires both Postgres and MinIO.** File content lives in MinIO, not the database — the database only stores *references* to files (Section 6). A Postgres-only backup would faithfully restore every Vehicle, Document, and Attachment *record*, but leave every one of those Attachment records pointing at files that no longer exist. Backup and restore procedures must treat the Postgres dump and the MinIO bucket export as one paired unit, never one without the other.
- **Restore order matters conceptually**: the Postgres dump is restored first (recreating all entity, detail, and Attachment metadata rows), then the MinIO bucket content is restored/synced second (recreating the actual files those rows already reference). Restoring MinIO first would briefly leave orphaned files with no metadata pointing at them — harmless, but the given order avoids even that transient state.
- **A small consistency window is an accepted tradeoff**, not a flaw to eliminate: a file uploaded between the MinIO snapshot and the Postgres dump could exist in one backup but not the other. For a single-user, personal-data product, this is a reasonable tradeoff against the operational complexity of true cross-store transactional backups — revisit only if this product ever handles data where that gap becomes unacceptable.
- **Backups are encrypted at rest**, per `docs/architecture/00_Engineering_Overview.md`, Section 15 — a requirement on the backup mechanism, not a separate system.

## 21. Future Multi-Tenant Strategy

The entire ownership model (Section 2) was designed so this evolution is cheap:

- **Today**: `entities.owner_id` names a single user.
- **Household sharing (near-future)**: introduce a join table (e.g., `household_members`) between users and a household concept, with `owner_id` reinterpreted as "belongs to this household" rather than "belongs to this single user" — a data-model addition, not a restructuring of every existing table, precisely because ownership was never duplicated across tables (Section 2).
- **Hosted multi-tenant SaaS (further future)**: `owner_id` could be joined by a higher-level `tenant_id` if genuine multi-tenant isolation is ever needed beyond household sharing — again, a change to the meaning and foreign-key target of **one column in one table**, not an audit of the entire schema, because that discipline was maintained from the start.
- **PostgreSQL Row-Level Security (RLS)** is noted as a strong future defense-in-depth option — enforcing tenant isolation at the database level itself, beneath the Service-layer scoping already in place (`docs/architecture/01_System_Architecture.md`, Section 4) — but is explicitly **not** needed for single-user V1, where Service-layer scoping alone is sufficient. Flagged as a future hardening step, not a current requirement.

---

## Quality Review

**New architectural calls made within this document**, none of which contradict the four foundational decisions already confirmed (`docs/architecture/00_Engineering_Overview.md`) — these are implementation-level judgment calls made *within* that confirmed direction, the same way Celery (background jobs) and the error-code mapping table were decided without individually re-confirming each with the Product Owner:

- UUID primary keys everywhere, including detail tables sharing their base entity's UUID (Section 15) — except `entity_types` itself, a deliberate, documented exception (Section 15).
- `relationships` stored as one row per connection, not two mirrored rows (Section 5).
- A dedicated `search_index` table, rather than a search vector living directly on `entities` (Section 11) — this refines `docs/architecture/00_Engineering_Overview.md`, Section 7's looser description of a `tsvector` "column on entities" into a cleanly Service-owned table, for the Service Boundary reasons in Section 5 of `01_System_Architecture.md`.
- An `entity_type` registry/lookup table rather than a database enum (Section 3) — resolves an ambiguity `00_Engineering_Overview.md` left open (it named the column but not its backing mechanism).
- Multiple typed nullable columns for Custom Field Values, rather than one generic column (Section 7).

**The one choice most worth revisiting once real implementation begins**: the Custom Field Value storage approach (Section 7). Multiple nullable typed columns give real DB-level typing and filtering, but waste a few nullable columns per row and require the Service layer to always read/write the correct column for a given field's declared type. If Custom Fields turn out to need more types than the current five (text/number/date/boolean/select), this is the table most likely to need a second look.

**Consistency check against prior architecture documents:** every table introduced here maps to exactly one Service already named in `docs/architecture/01_System_Architecture.md`, Section 5 (no new, unaccounted-for tables were introduced); every foreign-key rule enforces a dependency rule already stated in Section 1 of that document (Domain → Platform, never the reverse); `docs/decisions/DEC-007` (30-day Trash), `DEC-009` (hybrid Relationships), `DEC-011` (Activity & Audit split), and `DEC-013` (V1 backup strategy) are all reflected exactly as approved, with no reinterpretation.

**No new product or UX decisions were introduced.** This document is entirely an internal elaboration of already-approved architecture.

---

## Document Status

**Version:** 1.0
**Status:** Approved
**Dependencies:**
- `docs/architecture/00_Engineering_Overview.md`
- `docs/architecture/01_System_Architecture.md`
- `docs/product/00_Glossary.md`

**Generated On:** 2026-07-02
**Approval Note:** Approved with explicit agreement on: typed Custom Field storage (Section 7), the entity type registry (Section 3), the dedicated search index table (Section 11), and Relationship ownership validation living in the Service layer rather than the database (Section 2/17).

**Next Document:** `docs/architecture/03_API_Design.md`
