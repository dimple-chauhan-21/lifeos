# LifeOS — Design Handoff

# Document Information

| Field | Value |
|---|---|
| Document | Design Handoff |
| File | `docs/design/00_Design_Handoff.md` |
| Version | 1.0 |
| Status | Draft |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `00_Glossary.md`, `01_Product_Vision.md`, `02_Product_Requirements_Document.md`, `03_Feature_Catalogue.md`, `04_Information_Architecture.md`, `05_User_Journeys.md`, `06_Screen_Inventory.md` |
| Used By | UX/UI Design, all future `docs/design/` documents |

---

## Welcome

This is the single handoff artifact from Product to Design. It assumes no prior context — everything a Product Designer needs before opening a design tool is either stated here or linked to its source of truth in `docs/product/`. It does not contain wireframes, UI, or implementation detail; those come next, and this document exists specifically to make sure they're built on the right foundation.

Read this once, fully, before designing anything. The single most important idea in it is in Section 5: **LifeOS is platform-first, so you are not designing ~40 individual screens — you are designing a small number of generic templates that render differently per Entity Type.** Nearly everything else in this document exists in service of that idea.

---

## 1. Product Vision Summary

LifeOS is a self-hosted, entity-driven personal operating system — one secure place for a person's vehicles, properties, documents, finances, health records, and more, replacing the fragmented mix of email, cloud drives, note apps, and paper most people currently rely on.

Every design decision should be measurable against the five questions LifeOS exists to answer (`01_Product_Vision.md`):
- *Where did I keep that?*
- *When did this happen?*
- *How much did I spend?*
- *What else is related to this?*
- *What do I need to do next?*

Key product facts that shape design:
- **Single-user in V1**, but the architecture is SaaS-ready — don't design multi-account UI now, but don't design anything that assumes only one person will ever use an instance either (e.g., avoid hardcoding "you" everywhere a more neutral label would age better).
- **Self-hosted**, deployed via Docker — no "sign up with Google" style flows; auth is email/password for V1.
- **No AI in the MVP.** Do not design AI-flavored affordances (chat interfaces, "ask AI" buttons, auto-suggestions framed as intelligent) in this phase.
- **Vehicle is the reference implementation** of the entire platform (`docs/decisions/DEC-001`) — design against Vehicle first.

Full detail: `01_Product_Vision.md`, `02_Product_Requirements_Document.md`.

---

## 2. Information Architecture Summary

The product hierarchy is exactly two levels deep: **Module → Entity Type.** Nothing nests deeper than that — a Vehicle's Insurance Policy is not "inside" the Vehicle, it's a separate Entity connected by a Relationship. Design should never imply a deeper hierarchy than this (e.g., no breadcrumb trail longer than Module → Entity Type → Entity Instance).

**12 top-level Modules:** Dashboard, Assets, Documents, Finance, Health, Planning, Home, Knowledge, People, Global Search, Notifications, Settings. (An earlier `Activity & Audit` module was folded into Dashboard + Settings — `docs/decisions/DEC-011`.)

**8 Domains own 28 Entity Types between them** (Assets, Documents, Finance, Health, Planning, Home, Knowledge, People) — full list in `04_Information_Architecture.md`, Section 2. Every Entity Type belongs to exactly one Domain; cross-domain relevance is always expressed as a Relationship, never as an entity belonging to two places.

**Information ownership** (`04_Information_Architecture.md`, Section 7) — design should reflect this structure directly: Global data lives in Settings, Domain-level data is structural (categories, not user content), and almost everything a user actually sees is owned by one specific Entity Instance. There is no "orphaned" data in this product — every list, card, or file shown should be traceable to the Entity that owns it.

---

## 3. Navigation Principles

Four distinct navigation layers exist conceptually (`04_Information_Architecture.md`, Section 3) and should remain visually distinguishable in the design system:

| Layer | What it is | Design implication |
|---|---|---|
| **Global Navigation** | Always-available entry points: Dashboard, each Module, Search, Notifications, Settings | Should be reachable from literally anywhere — a persistent nav shell, not a per-screen element |
| **Local Navigation** | Moving between Entity Types/lists within one Module | Secondary-level nav, scoped to the Module currently open |
| **Context Navigation** | Moving between an Entity Instance's own capability tabs | Tab-level UI on the Entity Overview |
| **Cross-Entity Navigation** | Jumping from one Entity to a *different, related* Entity | This is the most important pattern in the product — every Relationship, every Search result, and every Dashboard item should lead here in exactly one click |

**Design priority:** Cross-Entity Navigation is what makes LifeOS feel like one connected system rather than a folder of separate apps. If a design pattern makes it harder to jump from a Vehicle to its Insurance Policy than it is to navigate there via the Finance module from scratch, that pattern has failed the product's core premise.

---

## 4. Screen Inventory Summary

The full inventory is in `06_Screen_Inventory.md`. Headline numbers:

- **~40 unique screens total** (37 after two recommended merges — see Section 6 below), covering the entire product.
- For comparison: a naive, one-screen-per-entity-type approach across 28 Entity Types would require roughly **336 screens.** The actual count is ~12% of that, because almost everything is a generic, reusable template.
- **MVP scope** = nearly the entire generic screen set (13 generic templates + Global/Settings/Modals), applied to just 5 Entity Types (Vehicle, Insurance Policy, Expense, Document, Contact). The only screens excluded from MVP are the two genuinely entity-specific ones (Checklist Items, Trip Itinerary), both belonging to post-MVP Domains.
- Two examples from the original screen-inventory brief — "Insurance Details" and "Health Record" — turned out, on inspection, to **not** be unique screens at all; both are the generic Entity Overview template, parameterized. Treat any instinct to design something "specific to an entity" with real suspicion until you've confirmed it can't be expressed as fields, Custom Fields, or a generic capability tab.

---

## 5. Entity Platform Principles

This is the most important section in this document for how you should actually work.

Every Entity Instance in LifeOS — a Vehicle, a Contact, an Insurance Policy, a Medical Record — is built on the same underlying platform and, by default, supports the same **Standard Entity Capability Set**: Create, View/Overview, Edit, Archive/Unarchive, Soft Delete/Restore, Favorite, Tag, Timeline, Notes, Attachments, Expenses, Reminders, Relationships, Custom Fields, Activity History (`03_Feature_Catalogue.md`, Section 2.1).

What this means for design:

1. **Design one Entity Overview template, not one per Entity Type.** It must gracefully render very different field sets (a Vehicle's VIN and odometer vs. a Contact's phone number and Roles) without looking hand-built for either.
2. **Design one Capability Tab shell**, reused for Timeline, Attachments, Notes, Expenses, Reminders, Relationships, and Activity History — each supplies its own item renderer, but the surrounding shell (header, empty state, add action, list) should be a single pattern.
3. **Not every Entity Type supports every capability.** Consult the applicability matrix in `03_Feature_Catalogue.md`, Section 6 before assuming a tab always appears — a Knowledge Note, for example, does not have a Notes tab (it *is* the note). Design must hide inapplicable tabs entirely, never show them disabled/greyed-out.
4. **Custom Fields are unpredictable by design** — any number of extra fields, of type text/number/date/boolean/single-select, can appear on any Entity Type's Overview. The Overview layout must not break, and should not visually "call out" Custom Fields as second-class — they're meant to feel native.
5. **Validate every generic template against at least two structurally different Entity Types** before considering it finished — Vehicle (Assets) and Contact (People) are a good pair, since they differ enough to expose template assumptions (e.g., a template that quietly assumes every entity has a photo, or a numeric identifier, will break on one or the other).
6. **Entity lifecycle state (Active / Archived / Trashed) needs one consistent visual language** across every Entity Type — not a per-Domain treatment. See `04_Information_Architecture.md`, Section 5 for the full state model.

---

## 6. Reusable Screen Templates

These are the templates to actually design, in priority order — build the templates before any specific screen instance:

| Template | Replaces / Covers |
|---|---|
| **Entity Form** | Add Entity + Edit Entity, merged into one form with create/edit modes (recommended merge, `06_Screen_Inventory.md` Quality Review) |
| **Entity Overview** | Every Entity Type's detail view |
| **Capability Tab Shell** | Timeline, Attachments, Notes, Expenses, Reminders, Relationships, Activity History (7 tabs, 1 shell) |
| **Filterable List Shell** | Entity List, Search Results, Archive & Trash List, Notification Center, Custom Field Definitions list |
| **Confirm Action** | Confirm Archive, Confirm Delete, Confirm Permanent Delete, merged into one parameterized modal (recommended merge) |
| **Attachment / File Viewer** | Previewing any image, PDF, video, or audio file, from any Entity |

Everything else in the Screen Catalogue (Dashboard Home, Settings screens, Auth screens) is genuinely a one-off and can be designed individually — but confirm against `06_Screen_Inventory.md`, Section 1 before assuming a screen is one-off; several things that look unique (like "Insurance Details") turned out not to be.

---

## 7. UX Principles

Translated for design from the binding Product Principles (`02_Product_Requirements_Document.md`, Section 6) and Information Architecture Principles (`04_Information_Architecture.md`, Section 10):

- **Consistency over novelty.** A new Entity Type or Domain does not earn a bespoke UI. If a design idea only works for one Entity Type, it's probably a Custom Field or a Domain-specific label, not a new template.
- **Progressive disclosure.** The default experience (create an entity, attach a file, set a reminder) should feel simple; power (Custom Fields, Relationships, Custom Relationship types) should be available without being in the way for a user who never touches it.
- **Assistant, not analytics.** The Dashboard surfaces what needs attention — it is explicitly not a BI/reporting surface. Avoid chart-heavy, metrics-dashboard visual language; favor a calm, task-oriented, "here's what's next" tone.
- **Design for the five guiding questions.** Every screen should make it faster to answer *where, when, how much, what's related,* or *what's next* — if a design element doesn't serve one of these, question whether it belongs.
- **Calm, trustworthy tone over urgency-by-default.** This product holds financial, medical, and identity data. Reserve visually urgent treatment (strong red, exclamation iconography) genuinely for overdue/Alert-level items (per the escalation model in `05_User_Journeys.md`, J9.1) — not for routine information.
- **Design for real data volume.** A user's data grows for years. Lists, Search, and Dashboard widgets should be designed assuming hundreds of entities over time, not just an empty-state demo.

---

## 8. Accessibility Guidelines

No accessibility standard has been formally ratified yet for LifeOS — the following is the recommended baseline, and should be confirmed as a Product decision (see Section 11):

- Target **WCAG 2.1 AA** conformance.
- **Never use color as the sole indicator of state** — this matters especially for the Expiring Soon / Overdue / Alert escalation model (`05_User_Journeys.md`, J9.1), which must remain legible to colorblind users via icon and text, not color alone.
- All interactive elements (forms, tabs, modals, the Capability Tab shell) must be fully keyboard-navigable with visible focus states.
- All non-text content (Attachments, icons, entity-type imagery) needs text alternatives for screen readers.
- Sufficient contrast ratios for text and icons in both light and (if built) dark mode.
- Avoid hover-only or tooltip-only interactions — they fail on touch devices and for screen-reader users, and this product will be used on mobile browsers (Section 9).
- Given the sensitivity of the data (identity, medical, financial documents), accessibility here is not just compliance — it's part of the product's trust proposition.

---

## 9. Responsive Design Requirements

LifeOS is **web-first**, with a Flutter mobile app planned for a later phase (`01_Product_Vision.md`) — but web-first does not mean desktop-only. Until the native app exists, mobile browser usage should be assumed as a first-class, everyday access pattern (checking today's reminders, quickly logging an expense, searching for a document while out).

Requirements:
- Full responsive support across desktop, tablet, and mobile browser widths is **in scope for MVP**, not deferred alongside the native app.
- Core flows — Dashboard review, Quick Add, Global Search, viewing a Reminder or Entity Overview — must work well on a phone-sized browser viewport, not just "not be broken."
- The Capability Tab Shell and Entity Overview need a defined mobile layout strategy (tabs collapsing to an accordion or bottom sheet, for example) — this is not yet decided; see Section 11.
- The Attachment/File Viewer must account for mobile constraints — large PDFs/videos, potentially slower connections back to a self-hosted instance accessed remotely.

---

## 10. Design Constraints

- **Fixed frontend stack:** Next.js, React, TypeScript, Tailwind CSS, shadcn/ui, Zustand, TanStack Query, React Hook Form, Zod. Design within shadcn/ui's component vocabulary where reasonable — it keeps design-to-build friction low, though it is not a hard requirement to use only existing shadcn components unmodified.
- **No AI-flavored UI in this phase** — no chat interfaces, no "ask AI" affordances, no AI-styled suggestion patterns. Revisit only once AI is actually scoped as a feature.
- **No native mobile screens** — only responsive web, per Section 9.
- **Single-user in V1** — no account-switching, no multi-tenant chrome, no "invite a household member" UI yet, even though the underlying data model supports it later.
- **Data sensitivity demands a "quiet," trustworthy visual tone** rather than a playful consumer-app aesthetic — this is a recommendation, not yet a ratified constraint; confirm with Product (Section 11).
- **Design for real longevity of data**, not just demo/empty states — this is a product meant to hold years of records.

---

## 11. Open UX Decisions

These need a decision — from Design, from Product, or jointly — before high-fidelity design work should be considered final. Several affect the component library's structure, not just visual polish, so resolve them early:

1. **Visual language for entity lifecycle state** (Active / Archived / Trashed) — badge, color, label, or combination?
2. **Mobile collapse strategy for the Capability Tab Shell** — accordion, bottom sheet, horizontal scroll tabs, or something else?
3. **Visual distinction (if any) between System Relationships and Custom Relationships** on the Relationships tab.
4. **How Custom Fields are visually distinguished, if at all,** from an Entity Type's built-in typed fields on Overview.
5. **Dashboard widget visual hierarchy** when multiple things need attention at once — how does Today's Agenda read differently from Expiring Soon, from an Overdue/Alert item?
6. **Empty-state tone** — friendly/encouraging illustration vs. minimal/neutral text — ties directly to the "quiet, trustworthy" tone question in Section 10.
7. **Dark mode** — in scope for V1 or deferred to a later release?
8. **Iconography system** for 12 Modules and 28 Entity Types — no icon language exists yet.
9. **Confirmation of the two recommended screen merges** (Entity Form; Confirm Action modal) from `06_Screen_Inventory.md` — Design should sign off before these become the basis of the component library.
10. **Whether an expiry field (Document, Insurance Policy) auto-generates a Reminder**, is manual only, or prompts the user — still open from `05_User_Journeys.md`'s Quality Review, and it directly affects whether "Creating a Reminder" needs a manual UI step in the expiry-driven case.

---

## 12. Recommendations for Claude Design

Practical guidance for how to approach this phase, whether working solo or directing a design-focused agent:

1. **Start with the reference implementation, not the whole product.** Design the Entity Overview and one Capability Tab (Attachments is a good first choice — it's used everywhere and has real visual complexity) for **Vehicle** first. Get that right before touching any other Entity Type.
2. **Design templates before instances.** Entity Form, Capability Tab Shell, and Filterable List Shell (Section 6) should exist as real, documented components before any Domain-specific screen is drawn — this mirrors the platform-first build order already used in engineering, and for the same reason: it's the highest-leverage, hardest-to-change work.
3. **Stress-test every template against two different Entity Types** before calling it done — Vehicle and Contact are recommended, since they differ enough (physical asset with a VIN vs. a person with Roles) to expose assumptions that don't generalize.
4. **Resolve Open UX Decisions (Section 11) before high-fidelity work**, not after — several of them determine component structure, and retrofitting them later is expensive.
5. **Organize design files using the existing Screen Classification** (`06_Screen_Inventory.md`, Section 2: Global / Module / Entity / Modal / Wizard / Settings) so design artifacts map 1:1 to the documentation already in place — this keeps Product and Design traceable to each other as both evolve.
6. **Keep design outputs inside `docs/design/`**, numbered and versioned using the same Document Information header standard already established across `docs/product/` and `docs/decisions/` — treat design documentation with the same rigor as product documentation, since Engineering will eventually depend on both.
7. **Log any new decision made during design** (a resolved Open UX Decision, a rejected direction, a new constraint discovered) in `docs/decisions/` as a new `DEC-XXX` entry, exactly as Product has been doing — this is what has kept this documentation set coherent so far, and Design should extend the same discipline rather than starting a separate, parallel decision trail.

---

## Document Status

**Version:** 1.0
**Status:** Draft
**Dependencies:**
- `docs/product/00_Glossary.md`
- `docs/product/01_Product_Vision.md`
- `docs/product/02_Product_Requirements_Document.md`
- `docs/product/03_Feature_Catalogue.md`
- `docs/product/04_Information_Architecture.md`
- `docs/product/05_User_Journeys.md`
- `docs/product/06_Screen_Inventory.md`

**Generated On:** 2026-07-02

**Next Document:** First wireframe/design artifact under `docs/design/`, scoped to the Vehicle Entity Overview + Attachments tab per Section 12, Recommendation 1.
