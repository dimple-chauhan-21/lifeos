# LifeOS — Product Glossary

# Document Information

| Field | Value |
|---|---|
| Document | Product Glossary |
| File | `docs/product/00_Glossary.md` |
| Version | 1.1 |
| Status | Draft |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `01_Product_Vision.md`, `02_Product_Requirements_Document.md`, `03_Feature_Catalogue.md`, `docs/architecture/01_System_Architecture.md` |
| Used By | All Product, Design & Engineering Documents |

---

## Purpose

This document is the single source of truth for every important concept used in LifeOS. It exists to eliminate ambiguity between Product, Design, and Engineering — every future document is expected to use these definitions exactly as written here, and to add to this glossary before introducing a new term elsewhere. This document contains no implementation, database, or API detail, and remains valid regardless of the underlying technology stack.

Each term includes a **Definition**, its **Purpose** (why the concept exists), its **Scope** (where/how broadly it applies), **Examples**, and **Notes** where a distinction from a similar-sounding term needs to be made explicit.

---

## 1. Product Terminology

| Term | Definition | Purpose | Scope | Examples | Notes |
|---|---|---|---|---|---|
| **Product** | LifeOS itself — the complete system being designed and built. | Names the whole so every other term can be scoped beneath it. | Entire system. | "LifeOS is a self-hosted personal operating system." | — |
| **Module** (formally **Product Module**) | A navigable area of the product, typically grouping related Entity Types or a cross-cutting capability. | Organizes the product into a structure users can navigate. | Product-level; no implementation implication. | Assets, Finance, Dashboard. | See also *Domain*, *Package* (Section 10). In Engineering documents, referred to explicitly as **Product Module** to avoid confusion with a code **Package** — see `docs/architecture/01_System_Architecture.md`, Section 2. Within Product/Design documents alone, plain "Module" remains unambiguous and is used as-is. |
| **Feature** | A specific, describable piece of functionality. | The unit at which product decisions are scoped and prioritized. | Can be domain-specific or platform-wide. | "Vehicle: Odometer Log," "Global Search." | Every Capability is a Feature; not every Feature is a Capability. |
| **Capability** | A platform-level Feature that applies generically across many Entity Types. | The reusable building block that makes LifeOS platform-first rather than module-first. | Cross-cutting; defined once, applied everywhere relevant. | Attachments, Timeline, Reminders. | See also *Generic Capability* (Section 2) — same concept, not a separate one. |
| **Domain** | A subject area of a person's life represented by one or more Entity Types within a Module. | Groups Entity Types that share real-world context. | Usually maps one-to-one with a Module. | Assets domain, Finance domain. | Module is the navigable UI grouping; Domain is the subject-matter grouping it represents. |
| **Platform** | The shared engine underlying every Module — the generic mechanisms reused across all domains. | Avoids rebuilding the same capability once per domain. | System-wide. | Entity Platform, Global Search. | See also *Platform Layer* (Section 10). |
| **MVP** | Minimum Viable Product — the smallest functional scope that delivers real usable value and validates the platform's core assumptions. | Defines the first release worth shipping. | One per major delivery cycle. | Vehicle + supporting entities (see `03_Feature_Catalogue.md`, Section 7). | See also *Release*. |
| **Release** | A defined, shippable version of LifeOS containing a specific scope of features. | The unit of delivery planning. | Product-wide, versioned. | "MVP Release," "Release 1.1." | See also *Milestone*. |
| **Milestone** | A significant checkpoint marking completion of a meaningful body of work, within or across Releases. | Tracks progress without itself being shippable. | Can span multiple Modules/Features. | "Entity Platform Core Complete." | Not user-facing, unlike a Release. |

---

## 2. Entity Platform Terminology

| Term | Definition | Purpose | Scope | Examples | Notes |
|---|---|---|---|---|---|
| **Entity** | Any single trackable "thing" in LifeOS. | The fundamental unit the entire platform is built around. | System-wide. | A specific Vehicle, a specific Document. | See also *Entity Type*, *Entity Instance*. |
| **Entity Type** | The category/blueprint an Entity belongs to, defining its typed fields and behavior. | Distinguishes "what kind of thing" an Entity is. | Fixed set defined by the platform. | Vehicle, Document, Contact. | — |
| **Entity Instance** | One specific, individual record of a given Entity Type. | The actual data a user creates and manages. | Unique per record. | "Rohan's Honda City" is an Entity Instance of the Vehicle Entity Type. | — |
| **Generic Capability** | Synonym for *Capability* (Section 1), used when emphasizing that it applies across Entity Types rather than being type-specific. | Reinforces the platform-first principle. | Same as Capability. | Attachments, Timeline. | Not a distinct concept from *Capability* — use "Capability" as the standard term going forward. |
| **Domain Entity** | An Entity Type that belongs to a specific domain/module. | Distinguishes user-facing, domain-specific entity types from system entity types. | Everything under Assets, Documents, Finance, Health, Planning, Home, Knowledge, People. | Vehicle, Insurance Policy, Contact. | See also *Platform Entity*. |
| **Platform Entity** | An Entity Type that exists to power a Capability rather than represent a domain concept directly. | Distinguishes system-supporting records from user-facing domain records. | Attachment, Reminder, Relationship, Custom Field Definition/Value, Tag, Timeline Event, Activity Log Entry, Audit Log Entry, Notification. | An Attachment record behind a Vehicle's uploaded photo. | Rarely browsed as their own module (Reminders/Notifications are the exception). |
| **Overview** | The default view of a single Entity Instance, showing its typed fields and Custom Field values. | The "home tab" of any entity page. | One per Entity Instance. | A Vehicle's Overview shows Make, Model, Year, VIN. | Distinct from Timeline (history) and Attachments (files) — current-state fields only. |
| **Metadata** | Data about an Entity Instance that isn't a user-facing typed or custom field. | System bookkeeping distinct from user-entered content. | Every Entity Instance. | Created On, Last Modified By. | Visible (e.g., in Activity History), not directly user-editable like typed fields. |
| **Custom Field** | A user-defined field added to a specific Entity Type beyond its built-in typed fields. | Lets the platform stay generic while supporting domain-specific variation. | Defined per Entity Type. | "Dealer Notes" on Vehicle. | See also *Custom Field Definition*, *Custom Field Value*. |
| **Custom Field Definition** | The declaration of a Custom Field for an Entity Type — its name and data type. | Defines what a Custom Field is, once, for all instances of that type. | One per Entity Type per field. | "Dealer Notes: Text" defined once for Vehicle. | — |
| **Custom Field Value** | The actual value entered for a Custom Field on one specific Entity Instance. | The data itself. | One per Entity Instance per Custom Field Definition. | "Dealer Notes: Ask for service discount" on one specific Vehicle. | — |

---

## 3. Relationship Terminology

| Term | Definition | Purpose | Scope | Examples | Notes |
|---|---|---|---|---|---|
| **Relationship** | A typed link between any two Entities, visible from both sides. | Lets entities interconnect — the core of "entity-driven, not module-driven." | System-wide, between any two Entity Instances. | Vehicle → Insurance Policy. | See also *System Relationship*, *Custom Relationship*. |
| **Parent Entity** | In a Relationship with a meaningful direction, the "owning"/primary side. | Gives directionality to ownership/containment-style relationships. | Only meaningful for hierarchical relationship types (`Owns`, `Belongs To`, `Lives At`). | In "Property owns Inventory Item," Property is the Parent Entity. | Not every Relationship has a meaningful direction — see `Related To`, which is symmetric. |
| **Child Entity** | The subordinate side of a Parent/Child Relationship. | The counterpart to Parent Entity. | Same as Parent Entity. | In "Property owns Inventory Item," the Inventory Item is the Child Entity. | — |
| **Linked Entity** | Generic term for "the entity on the other end of a Relationship," used when Parent/Child direction doesn't apply. | Describes symmetric or non-hierarchical relationships. | Any Relationship. | In "Contact related to Contact," each is a Linked Entity to the other. | — |
| **Relationship Type** | The label describing the nature of a Relationship. | Gives meaning to a link beyond "these two things are connected." | Drawn from System Relationships or freely defined as a Custom Relationship. | Owns, Insures, Maintained By. | See also *System Relationship*, *Custom Relationship*. |
| **System Relationship** | A relationship type maintained by the platform, from a fixed, closed list. | Keeps the most common relationships consistent and searchable system-wide. | `Owns`, `Belongs To`, `Insures`, `Maintained By`, `Lives At`, `Related To`. | Vehicle —Insures→ Insurance Policy. | See `docs/decisions/DEC-009-hybrid-relationship-model.md`. |
| **Custom Relationship** | A user-defined, freeform relationship label used when the closed list doesn't cover a case. | Prevents the closed list from blocking a legitimate connection. | Defined ad hoc by the user. | "Gifted By," "Inherited From." | See `docs/decisions/DEC-009-hybrid-relationship-model.md`. |

---

## 4. Timeline & Activity

| Term | Definition | Purpose | Scope | Examples | Notes |
|---|---|---|---|---|---|
| **Timeline** | The chronological feed of everything that happened to a specific Entity — system-generated and user-logged events combined. | Answers "when did this happen" for a given entity. | One per Entity Instance. | "Serviced — 2026-03-10," "Insurance renewed — 2026-01-05." | See also *Event*, *Activity*. |
| **Activity** | A system-generated record that something changed on an Entity (created, edited, archived, related). | The automatic, non-editable side of what appears on a Timeline. | One per change, per Entity Instance. | "Odometer field edited by user — 2026-06-01." | All Activity appears on the Timeline; not everything on the Timeline is Activity (a manually logged service is not). Not to be confused with **Operational Logging** (below) — a completely different, non-product-facing concept. |
| **Audit Log** | A separate, security-focused, immutable log of sensitive system events. | Security and compliance visibility, distinct from product-data change tracking. | System-wide, viewable in Settings > Security — not per-entity. | Login, failed login, data export, sensitive field access. | Distinct from Activity Log: Audit Log tracks security events; Activity Log tracks data changes. Also distinct from **Operational Logging** (below), which is not security-focused and not user-visible at all. |
| **Operational Logging** | Structured, engineering-facing log output (request logs, error stack traces, background job execution logs) written for developers and operators — never shown to an end user anywhere in the product. | Diagnoses and monitors system behavior at the infrastructure level. | System-wide; written to stdout/container logs, not stored in any product-facing table. | A request log line: `GET /api/v1/vehicles/{id} 200 42ms`. | **Not to be confused with Activity or Audit Log** — Operational Logging is never shown to a user and is never written to the `activity_log` or `audit_log` tables. See `docs/architecture/01_System_Architecture.md`, Section 10. This is an engineering-only concept, included here specifically to prevent it from being confused with the two product-facing log concepts above. |
| **Event** | A single occurrence recorded on a Timeline — the generic term covering both Activity entries and user-logged entries. | The atomic unit a Timeline is built from. | One per occurrence. | A single logged service record is one Event. | See also *Timeline*, *Activity*. |
| **History** | Informal, general term for the accumulated record of Events for an entity. | Casual shorthand only. | — | "Check the vehicle's history" = check its Timeline. | Not a distinct data concept — use *Timeline* or *Activity History* in formal writing; "History" is not introduced as a separate system. |
| **Change Log** | Not a LifeOS product concept. Reserved for documentation/engineering release notes about the software itself. | Avoids confusing product entity history with software release notes. | Project documentation only, not product data. | A `CHANGELOG.md` describing software releases. | Explicitly excluded from entity-level vocabulary — do not use for entity history; see Timeline/Activity/Audit Log instead. |

---

## 5. Productivity Concepts

| Term | Definition | Purpose | Scope | Examples | Notes |
|---|---|---|---|---|---|
| **Task** | A trackable to-do Entity with due date, priority, and status (Open / In Progress / Done). | Represents actionable work. | Planning module; can belong to a Goal. | "Call insurance company." | See also *Reminder*, *Goal*. |
| **Goal** | A longer-horizon personal objective, tracked via progress and typically composed of multiple Tasks. | Represents an outcome a user is working toward. | Planning module. | "Lose 10kg." | Goal owns Tasks via Relationship — see `docs/decisions/DEC-008-goal-task-separation.md`. |
| **Reminder** | A lightweight, date-triggered notification attached to any Entity. | Ensures a future date isn't forgotten, without the overhead of a full Task. | Attachable to any Entity Type. | "Renew insurance tomorrow." | See `docs/decisions/DEC-006-reminder-vs-task.md`. |
| **Checklist** | An Entity representing a list of check-off items grouped under one title. | Tracks a set of small, related items without each needing its own due date/priority. | Knowledge module. | "Packing List — Goa Trip." | Distinct from Task: a checklist item is a simple check-off, not a fully tracked unit of work. |
| **Project** | Not currently a defined Entity Type in LifeOS. | — | — | — | If a future need for multi-task, multi-person initiatives arises beyond Goal + linked Tasks, define this deliberately via a new Decision Log entry rather than using the term informally. |
| **Calendar Event** | A scheduled, dated occurrence, one-off or recurring. | Represents something happening at a specific time, distinct from a Task's due date. | Planning module. | "Dentist appointment — 2026-08-01, 10:00 AM." | Distinct from Reminder: a Calendar Event is the thing itself happening; a Reminder is a notification that can point to anything, including a Calendar Event. |

---

## 6. Document Management

| Term | Definition | Purpose | Scope | Examples | Notes |
|---|---|---|---|---|---|
| **Document** | The Entity Type representing an official or identity document, classified by a Document Category field. | First-class record of an official document's metadata (number, issuing authority, expiry). | Documents module. | Passport, Driving License, PAN. | See `docs/decisions/DEC-002-document-entity-consolidation.md`. Distinct from *Attachment* — see below. |
| **Attachment** | A file (image, PDF, document, video, or audio) linked to any Entity. | Holds the actual file content associated with an entity. | Attachable to any Entity Type. | A photo attached to a Vehicle; the scanned PDF attached to a Document entity. | A Document entity's scanned copy is itself stored *as* an Attachment — Document is the metadata record, Attachment is the file. |
| **File** | The raw underlying binary content of an Attachment. | Precise term for the content itself, versus the record describing it. | Always exists inside an Attachment. | `passport_scan.pdf`. | "File" and "Attachment" are used interchangeably in casual usage; formally, Attachment is the record, File is its content. |
| **Media** | Umbrella term for image, video, and audio Attachments specifically, as opposed to document-type Attachments. | Used when discussing preview/playback behavior, which differs from document preview. | A subset of Attachment. | A photo or a voice note is Media; a PDF is not typically called Media. | — |
| **Version** | Not currently a supported concept — each Attachment is a single, standalone file; re-uploading creates a new Attachment, not a new version of an existing one. | — | — | — | Document/Attachment versioning is a plausible future capability, not part of the current model — flagged so it isn't assumed present. |
| **Archive** | A reversible action that removes an Entity from default views without deleting any of its data. | Declutters active views without losing anything. | Any Entity. | Archiving a sold Vehicle. | Not a step toward deletion — a separate, non-destructive state. See also *Trash*. |
| **Trash** | The holding state for a soft-deleted Entity during its 30-day recovery window. | Gives a user a real chance to recover a mistaken deletion. | Any Entity. | A deleted Contact sitting in Trash for 25 more days. | See `docs/decisions/DEC-007-soft-delete-retention.md`. |
| **Soft Delete** | The act of moving an Entity to Trash — removed from normal views, recoverable for 30 days. | Safety net against accidental deletion. | Any Entity. | — | See also *Permanent Delete*. |
| **Permanent Delete** | The irreversible removal of an Entity and its data after the 30-day Trash window expires (or a manual "delete forever" from Trash). | True, final data removal. | Any Entity, only reachable after Soft Delete. | — | — |

---

## 7. Financial Concepts

| Term | Definition | Purpose | Scope | Examples | Notes |
|---|---|---|---|---|---|
| **Expense** | A logged expenditure, either standalone or linked to another Entity to build its cost-of-ownership picture. | Tracks money spent. | Finance module; attachable via Relationship to any Entity. | A fuel expense linked to a Vehicle. | — |
| **Income** | A logged income entry. | Tracks money received. | Finance module. | Salary, freelance payment. | — |
| **Budget** | Not currently a defined Entity Type in LifeOS. | — | — | — | `02_Product_Requirements_Document.md` explicitly positions LifeOS as *not* a budgeting engine (Product Boundaries). If budgeting is introduced later, scope it deliberately via a new Decision Log entry rather than assuming it from this term's presence here. |
| **Loan** | An Entity Type representing money owed, with a repayment plan. | Tracks debt obligations. | Finance module. | Home loan, car loan. | — |
| **Investment** | An Entity Type representing an investment holding. | Tracks asset value over time. | Finance module. | Mutual fund, stocks. | — |
| **Insurance Policy** | An Entity Type representing an insurance policy of any kind. | Tracks coverage, premium, and renewal. | Finance module; commonly related to Assets/Health entities. | Vehicle insurance, health insurance. | "Insurance" alone is not the entity name — the formal Entity Type is **Insurance Policy**, to avoid ambiguity between the general concept and the record. |

---

## 8. Search Concepts

| Term | Definition | Purpose | Scope | Examples | Notes |
|---|---|---|---|---|---|
| **Global Search** | The cross-cutting capability that searches entity names, fields, custom fields, tags, and attachment filenames across every module in one query. | Answers "where did I keep that." | System-wide. | Searching "insurance" surfaces every related Insurance Policy, Vehicle, and Document. | — |
| **Filter** | A refinement applied to a set of results after the fact. | Narrows results by module, entity type, date, or tag. | Any list/search view. | Filter Global Search results to "Finance" only. | — |
| **Tag** | A freeform label applicable to any Entity, managed globally and shared across all modules. | Cross-cutting, user-defined organization that doesn't fit a structured field. | Any Entity. | "urgent," "2026-taxes." | See also *Label* (below), *Category*. |
| **Category** | A structured, predefined classification field specific to certain Entity Types. | Distinguishes sub-kinds of a single Entity Type without creating new Entity Types. | Defined per Entity Type where applicable. | Document Category = Passport; Inventory Item Category = Furniture. | Distinct from Tag: Category is structured and type-specific; Tag is freeform and universal. |
| **Label** | Not a distinct concept from *Tag* in LifeOS. | — | — | — | This document standardizes on **Tag** as the single term going forward; do not use "Label" in future documents — it implies a second, separate system that does not exist. |
| **Favorite** | A per-Entity flag that pins it for quick access from the Dashboard. | Quick access to frequently needed entities. | Any Entity. | Favoriting a primary Vehicle. | — |

---

## 9. Dashboard Concepts

| Term | Definition | Purpose | Scope | Examples | Notes |
|---|---|---|---|---|---|
| **Dashboard** | The assistant-style home view of LifeOS, surfacing what needs attention today. | Answers "what do I need to do next" on login. | One per user. | Today's Agenda, Expiring Soon. | Explicitly not an analytics/reporting view — see `02_Product_Requirements_Document.md`. |
| **Widget** | A single, self-contained block of information on the Dashboard. | The building block the Dashboard is composed of. | Dashboard only. | "Expiring Soon" widget, "Upcoming Trips" widget. | See also *Assistant Card*. |
| **Assistant Card** | A Widget specifically framed as a proactive, assistant-style prompt rather than passive information display. | Distinguishes "FYI" widgets from "you should do something" widgets. | Dashboard only. | "Your car insurance expires in 5 days — renew now." | Every Assistant Card is a Widget; not every Widget is an Assistant Card. |
| **Notification** | A system-generated message delivered to the user through one or more enabled channels. | Proactively informs the user outside the Dashboard (in-app, email). | System-wide, most commonly triggered by a Reminder. | An email sent when a Reminder fires. | See also *Alert*. |
| **Alert** | A Notification specifically flagging something time-sensitive or requiring urgent attention. | Lets the notification system distinguish urgency. | A subset of Notification. | "Insurance policy expired yesterday" is an Alert; "Reminder set successfully" is a routine Notification, not an Alert. | Every Alert is a Notification; not every Notification is an Alert. |
| **Insight** | Not currently a defined LifeOS concept. Reserved for a possible future analytics/pattern-detection capability. | — | — | — | Explicitly out of scope per `02_Product_Requirements_Document.md` (no AI in MVP; Dashboard is assistant-style, not analytics). Term is reserved, not currently defined. |

---

## 10. Engineering Concepts (Product-Facing Only)

These definitions describe concepts at a product level only — no implementation, database, or API detail.

| Term | Definition | Purpose | Scope | Examples | Notes |
|---|---|---|---|---|---|
| **Platform Layer** | The conceptual layer of LifeOS containing every generic Capability, shared by all Domain Entities. | Names the "built once, reused everywhere" part of the system, without describing how it's implemented. | System-wide. | Attachments, Timeline, Reminders, Relationships. | See also *Domain Layer*. |
| **Domain Layer** | The conceptual layer containing what's unique to a specific Entity Type — its typed fields and domain-specific behavior. | Names the "thin, type-specific" part of the system, distinct from the Platform Layer. | Per Entity Type. | A Vehicle's Make/Model/VIN fields live in the Domain Layer; its Timeline does not. | — |
| **Configuration** | The product-level description of how a given Entity Type uses the Platform Layer — which Capabilities apply, which Custom Fields exist by default, its icon/label. | Names the mechanism by which a new Entity Type is "added" without new Platform work. | Per Entity Type. | Property's Configuration marks it as supporting Expenses and Relationships, with a default Custom Field for "Ownership Type." | — |
| **Reference Implementation** | The first Entity Type built to fully exercise the Platform Layer, validating it before reuse elsewhere. | Proves the platform is genuinely generic before it's relied upon. | Currently: Vehicle. | See `docs/decisions/DEC-001-vehicle-reference-implementation.md`. | — |
| **Reusable Component** | Any Capability, pattern, or Configuration convention designed from the outset to be used by more than one Entity Type. | The general principle underlying Platform Layer design decisions. | System-wide. | The Standard Entity Capability Set is a set of Reusable Components. | Product-level framing of reuse — not a statement about code structure. |
| **Package** | A code-level unit of organization (a Python or TypeScript directory) implementing either the Platform Layer or one Domain Layer Entity Type. | Names the actual code organization the Platform Layer / Domain Layer split is implemented as. | One package per Domain Entity Type, plus the Platform Layer's own packages. | `apps/api/app/domains/vehicles/`, `apps/api/app/platform/attachments/`. | **Not to be confused with the product-level Module** (Section 1, formally Product Module) — see `docs/architecture/01_System_Architecture.md`, Section 2, which introduced this distinction. A Product Module (e.g., "Assets") typically maps to *several* Packages (one per Entity Type it owns), never the reverse. |

---

## Cross-Reference Quick Index

| Term | See Also |
|---|---|
| Reminder | Task, Notification |
| Task | Goal, Reminder, Checklist |
| Attachment | Document, File, Media |
| Timeline | Activity, Event, Audit Log |
| Activity | Audit Log, Event, Operational Logging |
| Audit Log | Activity, Operational Logging |
| Operational Logging | Activity, Audit Log |
| Tag | Category, Label |
| Notification | Alert, Reminder |
| Capability | Generic Capability, Platform Layer |
| Domain Entity | Platform Entity, Reference Implementation |
| Relationship | System Relationship, Custom Relationship, Parent Entity, Child Entity |
| Module (Product Module) | Domain, Package |
| Package | Platform Layer, Domain Layer, Module |

---

## Quality Check — Ambiguities Identified and Resolved

While assembling this glossary, the following overlaps and ambiguities were identified and resolved so they don't drift into inconsistent usage later:

| Issue | Resolution |
|---|---|
| "Capability" (Section 1) and "Generic Capability" (Section 2) named the same thing | Standardized on **Capability**; "Generic Capability" is documented as a synonym, not a second concept. |
| "Tag" (Section 8) and "Label" (Section 8) named the same thing | Standardized on **Tag**; "Label" should not be used going forward. |
| "History" risked becoming a fourth, undefined concept alongside Timeline, Activity, and Audit Log | Defined as informal shorthand only, not a distinct data concept — use Timeline or Activity History formally. |
| "Change Log" could be mistaken for entity-level history | Scoped explicitly to software release notes, not product data, to prevent collision with Timeline/Activity/Audit Log. |
| "Project," "Budget," and "Insight" were requested as terms but have no corresponding Entity Type or capability in `01`–`03` | Documented as **reserved, not currently defined**, with a pointer to the relevant Product Boundary (Budget, Insight) or a note to define deliberately via Decision Log before use (Project) — rather than silently inventing scope that hasn't been approved. |
| "Insurance" (as requested) vs. the actual Entity Type name | Clarified that the formal Entity Type is **Insurance Policy**; "Insurance" is the general concept, not the record name. |
| "Module" (product-level, Section 1) risked colliding with **Package** (a code-level directory), once Engineering documents began referring to code organization | Introduced **Package** as a new, distinct term (Section 10) and clarified that "Module" is formally **Product Module** in Engineering contexts specifically to avoid the collision — resolved in `docs/architecture/01_System_Architecture.md`, Section 2, and canonicalized here. |
| **Operational Logging** (an engineering-only concept — request logs, stack traces, job logs) risked being conflated with **Activity** or **Audit Log** (both product-facing, both also "a log of things that happened") | Added **Operational Logging** as its own term (Section 4) with explicit "not to be confused with" notes on all three entries — resolved in `docs/architecture/01_System_Architecture.md`, Section 10, and canonicalized here. |

No further unresolved overlaps were identified. The `docs/decisions/` folder uses a `README.md` index plus one file per decision (`DEC-001` … `DEC-013`) — confirmed as the standing format; `README.md` serves as the Decision Log index referenced below.

---

## Document Status

**Version:** 1.1
**Status:** Draft
**Dependencies:**
- `docs/product/01_Product_Vision.md`
- `docs/product/02_Product_Requirements_Document.md`
- `docs/product/03_Feature_Catalogue.md`
- `docs/architecture/01_System_Architecture.md`

**Generated On:** 2026-07-02
**Revision Note:** v1.1 adds **Package** (Section 10) and **Operational Logging** (Section 4) as new canonical terms, and clarifies **Module** as formally **Product Module** in Engineering contexts — canonicalizing the two naming-collision resolutions first identified in `docs/architecture/01_System_Architecture.md`.

**Next Document:** `docs/architecture/02_Database_Architecture.md`
