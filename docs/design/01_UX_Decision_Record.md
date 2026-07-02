# LifeOS — UX Decision Record

# Document Information

| Field | Value |
|---|---|
| Document | UX Decision Record |
| File | `docs/design/01_UX_Decision_Record.md` |
| Version | 1.1 |
| Status | Draft |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `00_Design_Handoff.md`, `06_Screen_Inventory.md`, `05_User_Journeys.md`, `04_Information_Architecture.md`, `00_Glossary.md` |
| Used By | Sitemap, User Flows, Low-Fidelity Wireframes, Design System |

---

## Purpose

This is the UX equivalent of `docs/decisions/` (ADRs) — every major UX decision that must be settled before wireframing begins, recorded with options, a recommendation, and its future cost of change. It does not duplicate `00_Design_Handoff.md`; it resolves the open questions that document raised (its Section 11) and expands them into a full decision set covering every UX-relevant surface of the product.

Each decision uses a fixed structure: **Description · Why This Decision Matters · Options Considered · Recommendation · Trade-offs · Future Impact · Status.** All decisions start as **Pending Approval** unless a prior document has already settled the matter, in which case that's stated explicitly rather than re-litigated.

---

## Navigation

### UX-001: Primary Navigation Pattern

**Description:** Whether LifeOS's Global Navigation (`04_Information_Architecture.md`, Section 3) is presented as a persistent sidebar or a top navigation bar.

**Why This Decision Matters:** This is the single most-seen UI element in the product — it's present on every screen and directly expresses the 12-module Product Hierarchy (`04_Information_Architecture.md`, Section 1). Getting it wrong makes every other screen feel cramped or disorganized.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Persistent left sidebar | Scales well to 12 modules without crowding; supports icon + label; standard for data-dense, multi-domain apps | Consumes horizontal space on smaller desktop viewports; needs a distinct mobile treatment |
| Top navigation bar | Preserves full width for content; familiar from consumer web apps | 12 modules will not fit horizontally without an overflow menu, defeating the "everything visible" benefit |
| Hybrid (top bar for Global actions, sidebar for Modules) | Separates "always there" actions (Search, Notifications, Settings) from Module browsing | Two navigation surfaces to design consistently; higher initial complexity |

**Recommendation:** Persistent left sidebar for Modules, with Search, Notifications, and Settings anchored in a slim top bar. This directly mirrors the Global Navigation vs. the rest of the layer model in `04_Information_Architecture.md`, Section 3, rather than forcing all of Global Navigation into one visual pattern.

**Trade-offs:** Requires a defined collapse/hide behavior for narrow viewports (see UX-039); a full sidebar is not viable on mobile.

**Future Impact:** High — the primary navigation shell is the hardest thing to change once every screen is built against it.

**Status:** Pending Approval

---

### UX-002: Breadcrumbs & Wayfinding

**Description:** Whether LifeOS shows breadcrumbs (e.g., `Assets > Vehicle > Honda City`) to indicate location within the hierarchy.

**Why This Decision Matters:** The Product Hierarchy is only two levels deep by design (`04_Information_Architecture.md`, Principle 2) — this bounds how much wayfinding is actually needed, and over-building breadcrumbs would misrepresent a hierarchy that's intentionally shallow.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Full breadcrumb trail on every screen | Familiar pattern, always shows location | Implies a deep hierarchy that doesn't exist; wasted space given only 2 levels |
| No breadcrumbs — rely on the persistent sidebar + page title | Matches the actual shallow hierarchy; less visual noise | Slightly less explicit when arriving via Cross-Entity Navigation or Search from an unrelated context |
| Contextual "back to" link only (e.g., "← Back to Vehicles") | Lightweight, reinforces the one Module the entity belongs to | Doesn't help when a user arrived via a Relationship link from a different Module |

**Recommendation:** Contextual "back to [owning Module]" link on Entity Overview, combined with the persistent sidebar highlighting the active Module. No full breadcrumb trail — it would overstate a hierarchy that's deliberately flat.

**Trade-offs:** A user who jumped in via Cross-Entity Navigation from a different Module won't see a trail back through where they came from — only where the current Entity natively lives. This is an intentional simplification given IA Principle 2, not an oversight.

**Future Impact:** Low — easy to add later if user testing shows a real need.

**Status:** Pending Approval

---

### UX-003: Global Search Access Point

**Description:** Where and how Global Search is invoked — an always-visible search bar vs. a keyboard-shortcut/icon-triggered overlay.

**Why This Decision Matters:** Global Search is how LifeOS answers "where did I keep that" (`01_Product_Vision.md`) — it needs to be reachable in effectively zero friction from anywhere, per Global Navigation (`04_Information_Architecture.md`, Section 3).

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Always-visible search bar in the top nav | Zero discovery cost, always available | Consumes persistent top-bar space on every screen |
| Icon-triggered overlay/command palette | Keeps chrome minimal; can support a fast keyboard shortcut | Requires the user to discover/learn the trigger first |
| Both — persistent bar that also supports a keyboard shortcut | Best of both: discoverable and fast for repeat users | Slightly more to design and keep consistent |

**Recommendation:** Persistent, always-visible search bar in the top navigation, with a keyboard shortcut as a fast-path for repeat users. Given Search is one of only 12 top-level Modules and central to the product's core value proposition, it should not be hidden behind a discovery step.

**Trade-offs:** Permanently allocates top-bar space to Search on every screen, including ones where it's not the primary task.

**Future Impact:** Medium — changeable, but every screen's top bar would need to be touched.

**Status:** Pending Approval

---

## Dashboard

### UX-004: Dashboard Layout Structure

**Description:** How the Dashboard's widgets (Today's Agenda, Expiring Soon, Pending Bills, Recent Activity, Favorites, Upcoming Trips — `03_Feature_Catalogue.md`, Section 2.2) are spatially arranged.

**Why This Decision Matters:** The Dashboard is the first screen most sessions begin on (`05_User_Journeys.md`, J2.1) and is explicitly assistant-style, not analytics (`02_Product_Requirements_Document.md`, Section 6) — its layout has to read as "here's what matters," not a grid of equal-weight report tiles.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Uniform grid of equal-sized widget cards | Simple to build and scan | Implies every widget carries equal importance, which contradicts the assistant framing (urgent items should dominate) |
| Single-column priority feed (most urgent item first, regardless of widget) | Matches the "assistant" framing directly; naturally handles the escalation model in J9.1 | Loses the at-a-glance grouping by widget type (harder to jump straight to "Upcoming Trips" specifically) |
| Hybrid — a prioritized top strip (Today's Agenda / overdue items) above a widget grid for the rest | Urgent items get top billing without losing the scannable grouping of the remaining widgets | Two layout patterns to maintain on one screen |

**Recommendation:** Hybrid — an urgency-first top strip surfacing anything due/overdue today, with the remaining widgets (Expiring Soon, Recent Activity, Favorites, Upcoming Trips) below in a scannable grid. This satisfies both the assistant framing and the practical need to browse by category.

**Trade-offs:** Slightly more layout complexity than a uniform grid; needs a clear rule for what qualifies for the top strip vs. the grid.

**Future Impact:** Medium — the Dashboard is high-visibility but not structurally load-bearing for the rest of the product the way navigation is.

**Status:** Pending Approval

---

### UX-005: Widget Interactivity

**Description:** Whether Dashboard widgets support inline actions (e.g., marking a Reminder done directly from Today's Agenda) or are read-only summaries that link out to the full context.

**Why This Decision Matters:** `05_User_Journeys.md` J2.2 explicitly describes marking Reminders done/snoozed/dismissed "directly from the list" — this is already a product decision, not fully open; this entry formalizes the UX pattern for it.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Read-only widgets, all actions require opening the Entity | Simpler, fewer interactive states on the Dashboard | Contradicts J2.2's already-specified behavior; adds friction to a high-frequency action |
| Inline actions on widget items (mark done, snooze, dismiss, favorite) | Matches J2.2; reduces clicks for the most common daily action | More interactive surface area to design and test (hover/focus states, confirmation for destructive-adjacent actions) |

**Recommendation:** Inline actions, per J2.2. This is largely already decided by `05_User_Journeys.md` — this entry exists to make the UX pattern explicit (which actions are inline vs. require opening the entity) rather than to re-open the question.

**Trade-offs:** Every widget type needs its own defined set of inline actions, which is more design surface than a purely read-only Dashboard.

**Future Impact:** Low — additive; inline actions can be expanded over time without breaking the pattern.

**Status:** Pending Approval

---

### UX-006: Dashboard Customization

**Description:** Whether the user can reorder, hide, or add widgets to the Dashboard, or whether its composition is fixed.

**Why This Decision Matters:** Customization adds real UX value for power users but also real complexity — an empty or misconfigured Dashboard undermines the "assistant that watches your life for you" premise (`05_User_Journeys.md`, J9.1) if a widget was accidentally hidden.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Fully fixed Dashboard composition | Simple, guarantees no user ever "loses" a widget by accident | No flexibility for users who don't care about a given widget (e.g., no Trips yet) |
| Fully customizable (reorder, hide, add) | Maximum flexibility | Meaningful design and engineering surface for a v1; risk of a user hiding something important |
| Fixed composition, but empty/irrelevant widgets auto-collapse | No manual configuration needed; naturally adapts to what a user actually has | Less user control than true customization |

**Recommendation:** Fixed composition with auto-collapsing empty widgets for MVP. This delivers most of the practical benefit of customization (a Dashboard that reflects what's actually relevant to this user) without the design and engineering cost of a full customization system, and it removes the risk of a user accidentally hiding something important.

**Trade-offs:** A user with a strong preference (e.g., "I never want to see Upcoming Trips") has no way to permanently opt out in MVP.

**Future Impact:** Medium — true customization can be added later without breaking the fixed layout's structure, but it's more work to retrofit than to decide up front.

**Status:** Pending Approval

---

### UX-007: Assistant Card Pattern & Priority Ordering

**Description:** How individual Assistant Cards (`00_Glossary.md`, Section 9 — proactive, "you should do something" widgets) are visually differentiated from passive Widgets, and how multiple simultaneous items are ordered.

**Why This Decision Matters:** `05_User_Journeys.md` J9.1 defines an urgency escalation model (invisible → Expiring Soon → Today's Agenda → Overdue/Alert) — the Dashboard needs a consistent way to represent that escalation without relying on color alone (Section 8 of `00_Design_Handoff.md`).

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Sort strictly by due date | Simple, predictable | Doesn't account for severity (an overdue item and a due-today item might both be "soonest" but aren't equally urgent) |
| Sort by urgency tier first (Overdue > Due Today > Expiring Soon), then by date within tier | Matches the escalation model directly; most urgent always surfaces first | Requires a defined tiering rule up front |
| User-defined manual priority | Maximum user control | Contradicts the "assistant does this for you" premise — reintroduces the manual-checking burden LifeOS exists to remove |

**Recommendation:** Sort by urgency tier first, then by date within tier — directly implementing the J9.1 escalation model. Each tier gets a distinct, non-color-reliant visual treatment (icon + label), consistent with the accessibility guidance already established (`00_Design_Handoff.md`, Section 8).

**Trade-offs:** Requires the urgency-tiering logic to be well-defined and consistent across every Domain (a Document expiring in 5 days and an overdue Loan payment must be comparably ranked).

**Future Impact:** Medium — the ordering rule is changeable, but user trust in "the assistant shows me what matters most first" depends on getting it right early.

**Status:** Pending Approval

---

## Entity Experience

### UX-008: Generic Entity Layout

**Description:** The overall page structure used for every Entity Overview, regardless of Entity Type — this is the single highest-leverage decision in this document, per `00_Design_Handoff.md`, Section 5.

**Why This Decision Matters:** This layout is reused across all 28 Entity Types. A flaw here is not a one-screen problem — it's a whole-product problem, repeated 28 times.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Single scrollable page (fields, then tabs' content, all stacked) | Simple, no navigation within the page | Becomes very long for entities with many Attachments/Timeline entries; hard to scan |
| Fields at top, capability tabs below (tabbed navigation within the page) | Keeps each capability's content focused; matches Context Navigation (`04_Information_Architecture.md`, Section 3) directly | Requires a tab-switching interaction to design and make accessible |
| Sidebar-within-page (fields on the left permanently visible, capability content on the right, tab-switched) | Overview fields always visible even while browsing Timeline/Attachments | More complex responsive behavior; competes for space with the primary Global Navigation sidebar |

**Recommendation:** Fields at top (the Overview itself), capability tabs below — this is the option already implied by every prior document's language ("Entity Overview," "capability tabs") and matches Context Navigation directly. It also degrades gracefully to mobile (tabs collapse per UX-039) in a way the sidebar-within-page option does not.

**Trade-offs:** On a long Timeline or Attachments tab, the entity's own identifying fields scroll out of view — mitigate with a persistent, minimal header (entity name + type icon) that stays visible while a tab is scrolled.

**Future Impact:** High — every one of the ~13 generic screens and every Entity Type depends on this pattern.

**Status:** Pending Approval

---

### UX-009: Overview Field Layout

**Description:** How an Entity's typed fields and Custom Field values are arranged and visually distinguished (or not) from each other on the Overview.

**Why This Decision Matters:** `00_Design_Handoff.md` Section 5 flags this directly: Custom Fields must render inline without looking bolted-on, and the layout must not break regardless of how many extra fields exist.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Fixed two-column label/value grid, Custom Fields appended at the end in the same style | Predictable, simple to implement generically | A visual seam between "built-in" and "custom" if not styled identically; long field lists get visually monotonous |
| Grouped sections (e.g., "Details," "Additional Fields") | Some structure for entities with many fields | Introduces an artificial grouping that doesn't exist in the data model — risks looking like Custom Fields are second-class |
| Single continuous field list, no visual distinction between built-in and custom fields at all | Fully honors "Custom Fields should feel native" (`00_Design_Handoff.md`) | Loses a subtle wayfinding cue that could help a returning user recognize their own customizations |

**Recommendation:** Single continuous field list with no structural distinction between built-in and Custom Fields — directly satisfying the Design Handoff's explicit instruction that Custom Fields should not be visually called out as second-class (this resolves Open UX Decision #4 from `00_Design_Handoff.md`, Section 11).

**Trade-offs:** A user with many Custom Fields on one Entity Type may find it harder to distinguish "what LifeOS defines" from "what I added" — acceptable, since the product's own principle is that both should feel equally first-class.

**Future Impact:** Medium — the field-rendering component is reused everywhere, but the visual treatment can be adjusted later without restructuring data.

**Status:** Pending Approval

---

### UX-010: Tab Interaction Pattern

**Description:** How a user switches between an Entity's capability tabs (Timeline, Attachments, Notes, Expenses, Reminders, Relationships, Activity History), and specifically how this collapses on mobile. Settings is no longer part of this tab set — see `docs/decisions/DEC-012-remove-entity-settings-tab.md`; Archive/Delete are reached via a `⋮` overflow menu on the Entity Overview header instead.

**Why This Decision Matters:** This is the Capability Tab Shell (`06_Screen_Inventory.md`, Section 4/Quality Review) — one of the highest-reuse templates in the product, and Open UX Decision #2 from `00_Design_Handoff.md`.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Horizontal tab bar (desktop), unchanged on mobile with horizontal scroll | One pattern across breakpoints, simplest to build | Horizontal-scroll tabs are a known-poor mobile pattern — easy to miss tabs that scroll off-screen |
| Horizontal tab bar (desktop) → accordion (mobile) | Each breakpoint gets its natively best pattern | Two distinct interaction patterns to design and keep behaviorally equivalent |
| Horizontal tab bar (desktop) → bottom sheet / dropdown selector (mobile) | Compact on mobile, avoids the scroll-tabs problem | A dropdown hides all other tabs' content entirely, which may hide relevant context (e.g., a Reminders badge) more than an accordion would |

**Recommendation:** Horizontal tab bar on desktop/tablet; accordion on mobile (tabs stack vertically, each expandable, with the most contextually relevant tab open by default — typically Overview or Timeline). This resolves Open UX Decision #2 and keeps all tabs discoverable at every breakpoint, which matters given several tabs can carry unread/urgent state (e.g., an overdue Reminder).

**Trade-offs:** The accordion pattern takes more vertical scroll on mobile than a dropdown would; acceptable given the discoverability benefit.

**Future Impact:** High — this pattern is reused across all Entity Types and both major breakpoint classes; changing it later touches the entire Entity Overview experience.

**Status:** Pending Approval

---

### UX-011: Related Entity Presentation

**Description:** How linked Entities appear within the Relationships tab — as a flat list, grouped by Relationship Type, or as a visual graph.

**Why This Decision Matters:** This is the UI expression of Cross-Entity Navigation (`04_Information_Architecture.md`, Section 3), the single most important navigational pattern in the product per `00_Design_Handoff.md`, Section 3.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Flat list of linked entities, each showing its Relationship Type as a label | Simple, fast to scan, consistent with the Filterable List Shell already established | Doesn't visually convey a longer chain (e.g., Vehicle → Insurance → Contact) in one view |
| Grouped by Relationship Type (e.g., a section for "Insured By," another for "Incurs") | Clarifies the nature of each connection at a glance | More vertical space for entities with many varied relationship types |
| Interactive node graph | Visually compelling for exploring a whole connected chain at once | High design/engineering cost for a pattern most users will use briefly per entity, not as a primary daily tool; risks becoming a novelty rather than a utility (see also UX-024) |

**Recommendation:** Grouped by Relationship Type. It's the clearest expression of "what is this entity connected to and how," without the cost and discoverability risk of a full graph visualization (see UX-024 for the dedicated graph-view decision, which this entry defers to).

**Trade-offs:** For an Entity with many relationships of the same type (e.g., a Property with a dozen linked Inventory Items), the group can get long — acceptable, paginated/scrollable within the group.

**Future Impact:** Medium — this is a well-contained component; a future graph view (UX-024) can be added as an alternate view without replacing this default.

**Status:** Pending Approval

---

### UX-012: Empty State Strategy

**Description:** The tone and content of empty states across the product (`06_Screen_Inventory.md`, Section 8 lists 15 of them).

**Why This Decision Matters:** A new user's very first experience with most of LifeOS's modules is an empty state (`05_User_Journeys.md`, J1.4) — this materially shapes first impressions, and ties directly to Open UX Decision #6 from `00_Design_Handoff.md` (tone: friendly/encouraging vs. minimal/neutral).

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Minimal, neutral text only ("No attachments yet") | Fast to build, consistent, matches a "quiet, trustworthy" tone (`00_Design_Handoff.md`, Section 10) | Can feel cold or unfinished if overused across 15+ distinct empty states |
| Friendly, illustrated empty states with encouraging copy | Warmer, more engaging first-run experience | Risks clashing with the product's handling of sensitive financial/medical/identity data — illustration-heavy UI can read as less serious than the content warrants |
| Minimal text + a single clear action (e.g., "No Attachments — Add one"), no illustration | Actionable and calm; consistent with "quiet, trustworthy" | Less visually distinctive than illustrated states — acceptable trade for this product's tone |

**Recommendation:** Minimal text plus a single clear call-to-action, no illustration — consistent with the "quiet, trustworthy" tone direction already flagged in `00_Design_Handoff.md`, Section 10, and appropriate given the sensitivity of the data categories involved. This resolves Open UX Decision #6.

**Trade-offs:** Less visually engaging on true first-use (an entirely empty Dashboard) than an illustrated approach would be — mitigate with slightly warmer copy specifically on the very first empty Dashboard (J1.4/J2.1), while keeping every other empty state minimal.

**Future Impact:** Low — copy and minor visual treatment, easy to adjust later without structural change.

**Status:** Pending Approval

---

## Forms

### UX-013: Form Structure (Single-Page vs. Multi-Step)

**Description:** Whether Add Entity / Entity Form (`06_Screen_Inventory.md`, Section 6) is a single page or a multi-step wizard.

**Why This Decision Matters:** This form is used for every one of the 28 Entity Types (via the merged Entity Form template) — its structure needs to scale from an Entity Type with 4 fields to one with many, without becoming a different experience each time.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Single-page form for all Entity Types | One consistent pattern regardless of field count; fastest for entities with few fields | Can feel long for Entity Types with many fields plus Custom Fields |
| Multi-step wizard for all Entity Types | Breaks complexity into digestible steps | Adds unnecessary friction for simple Entity Types (e.g., a Bookmark with 2 fields); inconsistent step count per type is itself a design burden |
| Single-page form, with only required fields shown initially and an explicit "add more fields" expansion | Fast for the common case; scales to complex entities without a rigid step sequence | Requires a clear, consistent affordance for "there's more here" so optional fields aren't missed |

**Recommendation:** Single-page form with required fields shown by default and an explicit expansion for optional/Custom Fields. This matches `05_User_Journeys.md` J1.4's principle that an entity is created successfully even with only minimum fields filled, and avoids forcing every Entity Type through an artificial multi-step sequence regardless of actual complexity.

**Trade-offs:** Entity Types with genuinely many required fields (uncommon, but possible) will still produce a longer single page — acceptable, since required-field count is a Configuration decision made per Entity Type, not a UX limitation.

**Future Impact:** High — this is the Entity Form template, used everywhere Entities are created.

**Status:** Pending Approval

---

### UX-014: Validation Strategy

**Description:** When field validation errors are shown — on blur (leaving a field), on submit, or live as the user types.

**Why This Decision Matters:** Poor validation timing is one of the most common sources of form frustration; this pattern is reused across every Entity Form and every modal (Add Attachment, Add Relationship, Add Reminder, Add Expense).

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Validate only on submit | Simple, doesn't interrupt typing | User discovers all errors at once, at the end — frustrating for longer forms |
| Live validation (as the user types) | Immediate feedback | Can flag errors on a field the user hasn't finished typing yet (e.g., marking an email invalid before the domain is typed), which reads as broken |
| Validate on blur (when the user leaves a field), plus a final check on submit | Feedback arrives right when relevant, not prematurely or all at once | Slightly more implementation states (untouched / valid / invalid) to design for |

**Recommendation:** Validate on blur, with a final full-form check on submit. This is the standard, well-tested pattern that avoids both premature error flagging and end-of-form surprise.

**Trade-offs:** None significant — this is a low-risk, well-established pattern.

**Future Impact:** Low — a well-contained, swappable behavior within the form component.

**Status:** Pending Approval

---

### UX-015: Save Behavior (Autosave vs. Explicit Save)

**Description:** Whether Entity Forms autosave as the user types, or require an explicit Save action.

**Why This Decision Matters:** `05_User_Journeys.md` J1.4 already established that **no draft/incomplete state exists** — an Entity is either created or it isn't; this decision must respect that existing constraint rather than reopening it.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Autosave on every field change, even before all required fields are filled | Never lose typed input | Directly contradicts the "no draft state" decision already made in `05_User_Journeys.md` — would create partial Entities that shouldn't exist |
| Explicit Save only, entity created in one atomic action once required fields are valid | Consistent with the existing "no draft" decision; a created Entity is always complete enough to be real | If a user's session is interrupted before saving, unsaved input is lost |
| Explicit Save for entity **creation**; autosave for **edits** to an already-created Entity | Respects the no-draft rule at creation while reducing risk of losing edits to entities that already exist | Two different save behaviors (create vs. edit) to keep mentally distinct — acceptable since they are already conceptually distinct actions |

**Recommendation:** Explicit Save for entity creation (no drafts, per the existing decision); autosave for edits to fields on an already-created Entity, consistent with `05_User_Journeys.md` J3.2's description of edits being reflected "immediately" and logged to Activity History. This is not a new decision so much as the correct UX expression of one already made.

**Trade-offs:** Autosave-on-edit needs a clear, unobtrusive "saved" indicator so the user trusts the change went through without requiring a manual Save click.

**Future Impact:** Medium — changing "no drafts" later would be a product decision (out of scope here), not just a UX one; the UX pattern itself is moderately reusable.

**Status:** Pending Approval

---

### UX-016: Required Field Indication

**Description:** How required fields are marked on any form.

**Why This Decision Matters:** A small, high-frequency pattern reused on every form in the product — worth deciding once, consistently, rather than per-form.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Asterisk (`*`) on required fields | Extremely familiar convention | Asterisk alone can be missed or unclear to some screen reader configurations if not paired with text |
| Label text "(required)" on every required field | Fully explicit, no symbol interpretation needed | More visually noisy across forms with many required fields |
| Mark optional fields instead ("(optional)"), leaving unmarked fields implicitly required | Reduces marks when most fields are required (the common case for LifeOS's minimum-fields-first forms per UX-013) | Less universally familiar than marking required fields directly |

**Recommendation:** Asterisk on required fields, always paired with an accessible text equivalent (e.g., `aria-required`, and "required" in the field's accessible label) — satisfying both familiarity and the accessibility requirements in Section titled Accessibility below (UX-036–038).

**Trade-offs:** None significant.

**Future Impact:** Low.

**Status:** Pending Approval

---

## Lists & Tables

### UX-017: Default View Type (Card vs. Table)

**Description:** Whether the Entity List / Filterable List Shell (`06_Screen_Inventory.md`, Section 6) defaults to a card grid or a table/row layout.

**Why This Decision Matters:** This is one of the most-used generic templates in the product — it's how a user browses every Entity Type's collection.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Table/row layout for all Entity Types | Data-dense, scales well to hundreds of entities, easy to scan multiple fields at once | Less visually distinctive per entity; weaker for entity types where an Attachment thumbnail (e.g., a Vehicle's photo) is a meaningful identifier |
| Card grid for all Entity Types | Visually richer, foregrounds a thumbnail/image where one exists | Far less data-dense — poor fit for long-term data volume (`00_Design_Handoff.md`, Section 7: "design for real data volume") |
| Table by default, with an optional card view toggle | Data-dense default that scales, while still offering the richer view where useful | Two view implementations per list, doubling the design/build surface of the most-reused template in the product |

**Recommendation:** Table/row layout as the single default for all Entity Types, with no per-Domain toggle in MVP. Given the explicit design constraint to plan for real, long-term data volume (`00_Design_Handoff.md`, Section 10), density should win over visual richness as the default; a card toggle can be considered post-MVP (see Future UX Considerations) once real usage data shows it's needed.

**Trade-offs:** Entity Types with a strong visual identifier (Vehicle photos, Contact avatars) lose some of that richness in list view — mitigate with a small thumbnail column within the table row rather than a full card.

**Future Impact:** Medium — changeable later, but the Filterable List Shell is reused everywhere, so a later change touches many screens.

**Status:** Pending Approval

---

### UX-018: Sort & Filter Pattern

**Description:** How sorting and filtering controls are presented on any list (Entity List, Search Results, Archive & Trash List).

**Why This Decision Matters:** Filtering is required functionality per `03_Feature_Catalogue.md`, Section 5 (Global Search must support module/entity type/date filters) — this decision defines the shared interaction pattern.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Persistent filter/sort bar always visible above the list | Filters always discoverable, no extra click to access | Consumes vertical space on every list, even when unused |
| Filters hidden behind a "Filter" button that opens a panel/drawer | Keeps the list clean by default | Adds one click before filtering; less discoverable for new users |
| Sort always visible (simple dropdown), filters behind a button | Balances the two — sort is used more casually/frequently than multi-criteria filtering | Slight inconsistency in how the two related controls are exposed |

**Recommendation:** Sort control always visible (simple dropdown near the list header); filters behind a "Filter" button that opens a panel showing active filter count as a badge. This matches typical usage patterns (sort changes are frequent and low-commitment; filtering is a more deliberate action) and keeps the default list view clean, which matters more as data volume grows.

**Trade-offs:** A new user may not immediately notice filtering is available — mitigate with a clearly labeled, always-visible "Filter" button (not an icon-only affordance).

**Future Impact:** Medium.

**Status:** Pending Approval

---

### UX-019: Bulk Actions

**Description:** Whether Entity Lists support selecting multiple entities at once for a shared action (e.g., bulk archive, bulk tag).

**Why This Decision Matters:** Not previously specified in any prior document — this is a genuinely new UX surface, and one with real complexity (selection state, confirmation, partial-failure handling) relative to its MVP value.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Full bulk actions (multi-select, batch archive/tag/delete) in MVP | Real efficiency gain for users with many entities | Meaningful design and engineering surface for a capability not requested or validated by any User Journey to date |
| No bulk actions in MVP; single-entity actions only | Matches every journey already documented (all describe one-entity-at-a-time flows); keeps MVP scope disciplined | Users with many similar entities (e.g., many Expenses) must act on them one at a time |
| Deferred, but list rows are designed with a selection-checkbox affordance reserved from the start | Avoids retrofitting the list layout later if bulk actions are added | Slightly more visual complexity in the row design now, for a feature not shipping yet |

**Recommendation:** No bulk actions in MVP, and no reserved selection-checkbox affordance either — none of the User Journeys in `05_User_Journeys.md` describe a bulk-action need, and introducing the UI surface without a validated use case adds complexity the product doesn't yet need. Revisit post-MVP if usage patterns show real demand (see Future UX Considerations).

**Trade-offs:** If bulk actions are added later, the list row layout may need adjustment to accommodate a selection checkbox.

**Future Impact:** Low — deferring costs nothing now; adding it later is a contained, additive change to the Filterable List Shell.

**Status:** Pending Approval

---

### UX-020: Pagination Strategy

**Description:** Whether long lists use traditional pagination (page numbers) or infinite scroll.

**Why This Decision Matters:** Directly tied to the "design for real data volume" constraint (`00_Design_Handoff.md`, Section 7) — a user's Expense list, for example, will grow into the hundreds over a few years.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---| 
| Traditional pagination (page numbers / next-prev) | Predictable position, easy to reference "page 3," works well with sort/filter combinations | Slightly more clicks to browse sequentially |
| Infinite scroll | Feels faster for casual browsing | Loses position on navigating away and back; awkward to combine with in-page anchors like "jump to a specific date range" |
| Infinite scroll with a "load more" button (no auto-loading) | Reduces the "losing your place" problem somewhat vs. true infinite scroll | Still not as precise as page numbers for returning to a specific spot |

**Recommendation:** Traditional pagination. Given LifeOS is a records-and-retrieval product (not a social feed), predictable position and precise navigation matter more than the casual-browsing feel infinite scroll optimizes for — and it composes more cleanly with the sort/filter pattern (UX-018) and date-range review flows like `05_User_Journeys.md` J5.2.

**Trade-offs:** Slightly more clicks than infinite scroll for a user paging through many results sequentially.

**Future Impact:** Low — a contained behavior within the Filterable List Shell.

**Status:** Pending Approval

---

## Search

### UX-021: Search Interaction Model

**Description:** Whether Global Search returns results instantly as the user types, or only after explicit submission — and how search suggestions/recent searches factor in.

**Why This Decision Matters:** Search is core to the product's value proposition (`01_Product_Vision.md`) and the primary mechanism for "where did I keep that" — response feel matters as much as result accuracy.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Instant results as the user types (with debounce) | Fastest perceived response; matches modern search UX expectations | Requires careful handling of rapidly-changing queries and loading states |
| Submit-to-search only (press Enter) | Simpler technically; avoids showing noisy partial-query results | Feels slower and dated relative to user expectations set by other tools |
| Instant results, with recent searches shown before any query is typed | Combines fast search with a zero-effort re-entry point for repeat lookups | Requires storing and surfacing recent-search history, a small additional UX surface |

**Recommendation:** Instant results with debounce, and recent searches shown as soon as the search field is focused (before typing). This is the modern baseline users expect and directly supports the product's "find it in seconds" success metric (`02_Product_Requirements_Document.md`, Section 10).

**Trade-offs:** Needs a clear, calm loading state for the brief moment between keystroke and results (see Loading States, `06_Screen_Inventory.md` Section 10) so instant search doesn't feel flickery.

**Future Impact:** Medium.

**Status:** Pending Approval

---

### UX-022: Advanced Filters Presentation

**Description:** How Search Results filtering (by Module, Entity Type, date range — `03_Feature_Catalogue.md`, Section 5) is presented within Search specifically, as distinct from list filtering (UX-018).

**Why This Decision Matters:** Search Results is one instance of the Filterable List Shell, but arrives from a different entry point (a query) and may benefit from filter options tailored to search specifically (e.g., "search within Attachments only").

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Reuse the exact same filter panel pattern as UX-018, with Search-relevant filter options | Full UI consistency with every other list in the product | Slightly less tailored to search-specific needs |
| A distinct, search-specific filter bar (e.g., filter chips directly below the search field) | Can be more tightly integrated with the query itself | A second filtering pattern to maintain alongside UX-018's |

**Recommendation:** Reuse the UX-018 filter panel pattern exactly, populated with Search-relevant filter dimensions (Module, Entity Type, date range). Consistency across every list in the product outweighs the marginal benefit of a search-specific variant.

**Trade-offs:** None significant — this is a direct application of an already-decided pattern.

**Future Impact:** Low.

**Status:** Pending Approval

---

### UX-023: Saved Searches

**Description:** Whether users can save a search query + filter combination for quick reuse (e.g., "This Year's Vehicle Expenses").

**Why This Decision Matters:** A real convenience for recurring lookups like `05_User_Journeys.md` J5.2 (Reviewing Yearly Expenses), but adds a persistence and management surface (naming, editing, deleting saved searches) not validated as necessary by any journey to date.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Full Saved Searches feature (name, save, manage, re-run) in MVP | Real recurring-task value | Unvalidated scope addition; no journey in `05_User_Journeys.md` describes this need explicitly |
| No Saved Searches in MVP; rely on Filtering (UX-018/022) each time | Matches documented journeys exactly; no new persistence surface | Recurring lookups (like yearly expense review) require re-applying filters each time |
| Defer Saved Searches, but ensure the filter-state is reflected in the URL/shareable so a "save" can later just mean "bookmark this URL" | Low-cost future path without building a dedicated feature now | Still requires future design work when actually built |

**Recommendation:** Defer to post-MVP (see Future UX Considerations). This mirrors the same reasoning as Bulk Actions (UX-019): a real, plausible feature, but not one any current journey requires, and better validated with real usage before design investment.

**Trade-offs:** Recurring lookups like J5.2 require manually reapplying filters each time in MVP.

**Future Impact:** Low — cleanly additive later.

**Status:** Pending Approval

---

## Relationships

### UX-024: Relationship Visualization — Graph View vs. List View

**Description:** Whether LifeOS ever offers an interactive node-graph visualization of an Entity's connections, in addition to the grouped list decided in UX-011.

**Why This Decision Matters:** `05_User_Journeys.md` J7.1 (Connecting Entities Across Domains) uses a graph diagram to *illustrate* the concept in documentation — this decision is about whether that becomes an actual product surface.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Build a real interactive graph view for MVP | Visually compelling; could differentiate the product | High design/engineering cost; graph UIs are notoriously hard to keep usable past a handful of nodes; not requested by any journey as a working requirement (J7.1 uses the diagram as illustration, not spec) |
| No graph view — grouped list only (UX-011) | Matches actual documented need; avoids a high-cost, high-risk UI pattern for MVP | Loses the "see the whole connected picture at once" experience for power users |
| Defer — revisit only if user research shows the list view is insufficient for understanding multi-hop connections | Keeps the door open without committing scope now | Requires a future decision point rather than resolving it now |

**Recommendation:** No graph view for MVP or the near term; the grouped list (UX-011) plus one-click Cross-Entity Navigation already lets a user traverse a chain like Vehicle → Insurance → Expense → Contact → Property one hop at a time, which satisfies the underlying need. Revisit only with real evidence the list pattern is insufficient (Future UX Considerations).

**Trade-offs:** No single-screen view of an entity's full connection web — a user must navigate hop by hop to explore a chain.

**Future Impact:** Low — this is a purely additive future option, not something the rest of the product depends on.

**Status:** Pending Approval

---

### UX-025: Cross-Entity Navigation Affordance

**Description:** The specific interaction/visual cue that tells a user "clicking this takes you to a different Entity," distinct from an in-page tab switch.

**Why This Decision Matters:** Cross-Entity Navigation is called out repeatedly across `04_Information_Architecture.md` and `00_Design_Handoff.md` as the single most important navigational pattern in the product — it needs a clear, consistent, recognizable affordance so users always know when a click will leave the current Entity.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Linked entities styled identically to any other clickable text/list item | Minimal visual overhead | Risks ambiguity — a user may not realize clicking navigates to an entirely different Entity's Overview rather than expanding inline |
| A distinct "entity chip/card" style used everywhere a Relationship link appears (consistent icon + entity type label + name) | Immediately recognizable as "this is a link to another Entity," reused identically across Relationships tabs, Timeline references, and Search results | Requires one more reusable component to design, on top of the Filterable List Shell and Capability Tab Shell |

**Recommendation:** A distinct, consistent "entity chip" component — Entity Type icon + name — used everywhere a link points to another Entity Instance (Relationships tab, inline Timeline references, Expense's linked entity, Search results). This becomes instantly recognizable after the first few uses and directly reinforces the product's "everything is connected" premise.

**Trade-offs:** One more core reusable component to design and maintain, alongside the templates already listed in `00_Design_Handoff.md`, Section 6.

**Future Impact:** Medium-High — used pervasively; worth getting right early, but is a self-contained component rather than a page-level structural decision.

**Status:** Pending Approval

---

## Timeline & Activity

### UX-026: Timeline Visualization Style

**Description:** How an Entity's Timeline (`00_Glossary.md`, Section 4) is visually presented — a vertical chronological list, or a more graphical timeline (horizontal axis, milestones).

**Why This Decision Matters:** Timeline is one of the highest-value capability tabs — it's how a user answers "when did this happen" for any Entity (`01_Product_Vision.md`).

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Vertical chronological list (most recent first), each Event as a compact row | Simple, scales to long histories, consistent with the Capability Tab Shell pattern used elsewhere | Less visually distinctive than a graphical timeline |
| Horizontal graphical timeline with a visual axis | Visually engaging for a small number of events | Does not scale well to entities with many events (a Vehicle serviced 40 times over 10 years); harder to make accessible and responsive |

**Recommendation:** Vertical chronological list, most recent first, consistent with the Capability Tab Shell used by every other tab. This scales to real data volume and stays consistent with the rest of the Entity Overview, rather than introducing a one-off visual pattern for a single tab.

**Trade-offs:** Less visually distinctive than a graphical timeline — acceptable given the product's calm, data-dense tone (Visual Language, below).

**Future Impact:** Low — a well-contained, swappable rendering choice within the shared shell.

**Status:** Pending Approval

---

### UX-027: Activity Grouping Strategy

**Description:** Whether Timeline/Activity entries are grouped by day, or shown as an ungrouped continuous list.

**Why This Decision Matters:** Affects scannability of both the per-Entity Timeline and the Dashboard's Recent Activity widget (`04_Information_Architecture.md`, Section 9).

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Ungrouped, each entry shows its own full timestamp | Simple | Repetitive, harder to scan a busy history at a glance |
| Grouped by day ("Today," "Yesterday," "March 10, 2026"), entries listed under each | Much easier to scan; matches familiar patterns from activity feeds elsewhere | Slightly more structure to implement in the shared shell |

**Recommendation:** Grouped by day, with relative labels for the last 2 days ("Today," "Yesterday") and absolute dates beyond that — directly informs the date formatting decision below (UX-028).

**Trade-offs:** None significant.

**Future Impact:** Low.

**Status:** Pending Approval

---

### UX-028: Date & Time Formatting Convention

**Description:** The consistent format for displaying dates and times across the product (Timeline, Reminders, Expiring Soon, Expense dates, etc.).

**Why This Decision Matters:** A small decision with outsized consistency impact — dates appear on nearly every screen, and inconsistent formatting (e.g., `03/07/2026` vs. `March 7, 2026` vs. `3 days ago`) undermines the "quiet, trustworthy" tone.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Absolute dates everywhere (e.g., "March 7, 2026") | Unambiguous, no locale confusion | Less immediately meaningful for very recent events ("2 hours ago" is often more useful than a full date) |
| Relative dates everywhere (e.g., "3 days ago") | Immediately meaningful for recent activity | Becomes vague and less useful for anything more than a few weeks old; ambiguous for future dates (a Reminder "in 3 days" reads oddly as pure relative time) |
| Relative for recent (within ~7 days), absolute beyond that — with the exact timestamp always available on hover/tap | Best of both: meaningful for recent activity, precise for anything older | Requires a defined cutoff and a secondary "exact time" affordance |

**Recommendation:** Relative formatting within 7 days ("Today," "Yesterday," "3 days ago"), absolute dates beyond that, with the full exact timestamp always available via hover (desktop) or tap (mobile) — consistent with the accessibility requirement to never rely on a single, potentially ambiguous presentation (Section Accessibility, below).

**Trade-offs:** Requires consistent handling of the exact-timestamp fallback across both desktop and touch interfaces.

**Future Impact:** Low — a formatting rule, easy to adjust centrally if needed.

**Status:** Pending Approval

---

## Attachments

### UX-029: Upload Interaction

**Description:** How files are added to the Attachments capability — click-to-browse, drag-and-drop, or both.

**Why This Decision Matters:** Attachments is one of the most-used capabilities across the product (`00_Design_Handoff.md`, Section 5) and directly supports the "everything important, stored" premise (`01_Product_Vision.md`).

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Click-to-browse only (standard file picker) | Simple, fully accessible and keyboard-operable by default | Slower for users with a file already visible on their desktop |
| Drag-and-drop only | Fast for desktop users with the file at hand | Not usable on touch devices without a fallback; not natively keyboard-accessible |
| Both — drag-and-drop zone with a visible, always-available "Browse" button as the accessible fallback | Fast where useful, fully accessible everywhere | Slightly more surface to design (drop-zone states: idle, hover, dropping, uploading) |

**Recommendation:** Both, with click-to-browse as the guaranteed accessible path and drag-and-drop as a progressive enhancement. This directly satisfies the accessibility requirement against hover/drag-only interactions (`00_Design_Handoff.md`, Section 8).

**Trade-offs:** More interaction states to design for the upload zone.

**Future Impact:** Low — a contained component.

**Status:** Pending Approval

---

### UX-030: Preview Behavior

**Description:** Whether Attachments preview inline (within the Attachments tab) or require opening the Attachment/File Viewer for any preview.

**Why This Decision Matters:** Affects how quickly a user can confirm "yes, this is the right file" without leaving the Entity context.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Thumbnail-only in the tab; full preview always requires opening the Viewer | Simple, keeps the tab lightweight | An extra click even to confirm a file's identity |
| Full inline preview for every Attachment directly in the tab | Fastest recognition, no extra click | Heavy for tabs with many Attachments (multiple embedded PDFs/videos rendering at once); performance and layout risk |
| Thumbnail with filename/type in the tab; single click opens the full Attachment/File Viewer for any real preview | Lightweight list, one click to full context — consistent with the generic List → Viewer dependency already defined in `06_Screen_Inventory.md`, Section 7 | Marginally slower than full inline preview for a single-file case |

**Recommendation:** Thumbnail + filename in the Attachments tab, full preview in the Attachment/File Viewer — this matches the dependency chain already documented in `06_Screen_Inventory.md`, Section 7 (Entity Overview → Attachments tab → Viewer) and avoids the performance risk of multiple embedded previews.

**Trade-offs:** One extra click to see a full preview versus a hypothetical fully-inline approach.

**Future Impact:** Low.

**Status:** Pending Approval

---

### UX-031: File Organization Within Attachments

**Description:** Whether Attachments on a single Entity can be organized into folders/categories, or remain a flat, chronological list.

**Why This Decision Matters:** An Entity with many Attachments (e.g., a Vehicle with years of service receipts) could benefit from organization, but this adds real complexity not requested by any journey.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Flat, chronological list (matches upload order / Timeline order) | Simple, consistent with the Capability Tab Shell, no new concepts to design | Can get long for high-Attachment-count entities over years |
| User-defined folders within an Entity's Attachments | More organization for power users | A new hierarchy concept that doesn't exist anywhere else in the IA (`04_Information_Architecture.md`, Principle 2: no nesting below Entity Type) — would be a meaningful architectural exception |
| Flat list, but sortable/filterable by upload date or file type | Some organization without introducing a new hierarchy concept | Less structure than true folders for a very high-Attachment-count entity |

**Recommendation:** Flat list, sortable/filterable by date and file type — consistent with IA Principle 2 (no nesting below Entity Type) and avoiding a genuinely new organizational concept for a need not yet validated by any journey.

**Trade-offs:** No folder-level organization for entities with very large numbers of Attachments.

**Future Impact:** Low — sort/filter is additive; true folders, if ever needed, would be a bigger future decision requiring its own DEC entry given the IA implication.

**Status:** Pending Approval

---

### UX-032: Version History for Attachments

**Description:** Whether re-uploading a file to an existing Attachment slot creates a version history, or simply creates a new, separate Attachment.

**Why This Decision Matters:** This is **already resolved**, not open — included here for completeness and traceability rather than as a live decision.

**Options Considered:** *(not applicable — already decided)*

**Recommendation:** N/A — per `00_Glossary.md`, Section 6: *"Version: Not currently a supported concept — each Attachment is a single, standalone file; re-uploading creates a new Attachment, not a new version of an existing one."* The UX implication: there is no "replace and version" affordance in MVP — "Upload a new file" always creates an additional Attachment alongside any existing ones, and the old one is only removed if the user explicitly deletes it.

**Trade-offs:** N/A.

**Future Impact:** N/A — flagged in `00_Glossary.md` as a plausible future capability, not part of the current model.

**Status:** Resolved (see `docs/product/00_Glossary.md`, Section 6)

---

## Notifications

### UX-033: Notification Center Pattern

**Description:** The interaction pattern for the Notification Center (`03_Feature_Catalogue.md`, Section 2.2) — a dropdown panel vs. a dedicated full page.

**Why This Decision Matters:** Notifications is one of the 12 top-level Modules and a Global Navigation entry point (`04_Information_Architecture.md`, Section 1).

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Dropdown panel from the top nav icon | Fast access without leaving current context | Limited space for filtering/managing a large notification history |
| Dedicated full page | Room for filtering, grouping, and managing notification history properly | One extra step (navigation) for the common "just glance and dismiss" case |
| Dropdown panel for a quick recent view, with a "View All" link to a full page for full history/management | Fast for the common case, complete for the occasional deep-dive | Two related surfaces to keep consistent |

**Recommendation:** Dropdown panel (recent, unread-prioritized) with a "View All" link to a full Notification Center page — mirroring the same reasoning as UX-004's Dashboard hybrid approach (fast access to what's urgent, full context available on demand).

**Trade-offs:** Two surfaces to maintain, though they share the same underlying Filterable List Shell.

**Future Impact:** Medium.

**Status:** Pending Approval

---

### UX-034: Toast vs. Inline Notification Usage

**Description:** When to use a transient toast (e.g., "Saved") vs. an inline message within the page (e.g., a validation error, or "Reminder created" confirmation shown in context).

**Why This Decision Matters:** Establishes a consistent rule so designers and, later, engineers don't decide this ad hoc per screen.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Toasts for everything (success and error) | One consistent pattern | Errors that need the user to actually fix something (e.g., a form validation issue) are poorly served by a transient toast that can disappear before it's read |
| Inline messages for everything | Errors stay visible until resolved | Overkill for simple, low-stakes confirmations like "Saved" — inline success messages add clutter |
| Toasts for transient confirmations (Saved, Archived, Reminder created); inline messages for anything requiring user action (validation errors, failed uploads) | Matches the message to its urgency and required response | Two patterns to apply consistently — mitigated by a clear rule (does this require the user to act? if yes, inline; if no, toast) |

**Recommendation:** Toasts for transient, no-action-needed confirmations; inline messages for anything the user must read and act on. This is a standard, well-understood split that avoids both toast-fatigue and error messages disappearing before they're addressed.

**Trade-offs:** Requires discipline in applying the rule consistently across every form and action in the product.

**Future Impact:** Low — a rule, not a structural dependency.

**Status:** Pending Approval

---

### UX-035: Reminder Interaction Pattern

**Description:** The specific UI actions available on a Reminder — mark done, snooze, dismiss — and how snooze duration is chosen.

**Why This Decision Matters:** `05_User_Journeys.md` J2.2 already specifies these three actions exist; this decision defines snooze specifically, which J2.2 left open.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Fixed snooze options (e.g., "1 day," "1 week") | Fast, no date picker needed for the common case | Less precise than a custom date |
| Custom date picker only | Full precision | Slower for the common "just push it a day" case |
| Fixed common options plus a "custom date" fallback | Fast for the common case, precise when needed | One more UI state (the custom picker) to design |

**Recommendation:** Fixed common snooze options (e.g., Tomorrow, Next Week) plus a "Custom date" fallback — balancing speed for the frequent case against precision when genuinely needed.

**Trade-offs:** None significant.

**Future Impact:** Low.

**Status:** Pending Approval

---

## Accessibility

### UX-036: Accessibility Conformance Target

**Description:** The formal accessibility standard LifeOS commits to.

**Why This Decision Matters:** `00_Design_Handoff.md`, Section 8 already recommends WCAG 2.1 AA but flags it as unratified — this entry exists to formally decide it, since every subsequent accessibility decision depends on a target being fixed.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| WCAG 2.1 Level A (minimum) | Lowest implementation cost | Insufficient for a product holding sensitive medical/financial/identity data used by a broad range of people, potentially including users with disabilities managing their own care |
| WCAG 2.1 Level AA | Industry-standard target for serious products; covers contrast, keyboard access, focus, text alternatives comprehensively | More design and engineering discipline required than Level A |
| WCAG 2.1 Level AAA | Highest standard | Some AAA criteria are impractical for general-purpose products (e.g., strict contrast on all UI, not just text) and can conflict with visual design flexibility, without proportionate benefit for this product's context |

**Recommendation:** WCAG 2.1 Level AA, as already recommended in `00_Design_Handoff.md`. This is the recognized professional baseline for a serious product, appropriately rigorous given the sensitivity of the data LifeOS holds, without the impractical constraints of full AAA conformance.

**Trade-offs:** Requires accessibility to be a first-class design and QA concern throughout, not a post-launch pass.

**Future Impact:** High — retrofitting accessibility after components are built is far more expensive than designing to the target from the start.

**Status:** Pending Approval

---

### UX-037: Keyboard Navigation & Focus Management

**Description:** The baseline keyboard-operability standard for every interactive surface — forms, tabs, modals, the Capability Tab Shell, drag-and-drop.

**Why This Decision Matters:** Directly required by the WCAG 2.1 AA target (UX-036); also a practical necessity for power users who prefer keyboard navigation for a data-entry-heavy product like this one.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Keyboard support only where trivial (native HTML controls) | Least effort | Fails WCAG AA on custom components (tabs, modals, the entity chip from UX-025) unless deliberately built |
| Full keyboard operability for every custom component, with visible focus indicators throughout | Meets WCAG AA; supports real power-user workflows | Requires every custom component (tab shell, modal, filter panel, upload zone) to be designed with keyboard interaction and focus order in mind from the start |

**Recommendation:** Full keyboard operability for every interactive surface, including custom components, with a visible focus indicator at every step and a logical, predictable focus order (especially critical for modals — focus must move into the modal on open and return to the triggering element on close).

**Trade-offs:** Meaningfully more design specification work per component (documenting focus order and keyboard shortcuts, not just visual states).

**Future Impact:** High — same reasoning as UX-036.

**Status:** Pending Approval

---

### UX-038: Screen Reader, Contrast, and Motion Sensitivity

**Description:** Baseline requirements for screen reader support, color contrast, and reduced-motion preference — grouped here since all three are cross-cutting WCAG AA requirements rather than screen-specific decisions.

**Why This Decision Matters:** These three requirements touch every component in the design system and need to be decided once, centrally, rather than negotiated per screen.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Handle each requirement ad hoc per component as it's designed | Flexible | Inconsistent results, easy to miss requirements on less-visible screens (e.g., Settings) |
| Establish fixed baseline rules up front: text alternatives on all non-text content; minimum 4.5:1 contrast for text (3:1 for large text/icons); full support for `prefers-reduced-motion` | Consistent, auditable, matches WCAG AA directly | Requires the rules to be actually enforced during design and review, not just stated |

**Recommendation:** Fixed baseline rules, applied to every component without exception: all Attachments/icons/non-text content get text alternatives; all text meets 4.5:1 contrast minimum (3:1 for large text and meaningful icons); all animation/transition respects `prefers-reduced-motion` by reducing to instant or minimal-motion equivalents. This is the direct, practical expression of the WCAG AA target (UX-036).

**Trade-offs:** Constrains color and motion choices in the eventual visual/motion design (see Visual Language and Motion sections below) — an intentional, accepted constraint given the product's data sensitivity.

**Future Impact:** High.

**Status:** Pending Approval

---

## Responsive Behaviour

### UX-039: Responsive Strategy Across Breakpoints

**Description:** How the core layout (Global Navigation, Entity Overview, Capability Tab Shell) adapts across desktop, tablet, and mobile — resolving Open UX Decision #2 from `00_Design_Handoff.md` in full, alongside the mobile-web requirement from that document's Section 9.

**Why This Decision Matters:** `00_Design_Handoff.md`, Section 9 already establishes that full responsive support is in scope for MVP (not deferred to the native app) — this decision defines exactly what changes at each breakpoint.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Minimal adaptation — same layout, scaled down | Least design effort | Sidebar navigation (UX-001) and multi-column Overview layouts genuinely don't work on a phone-width viewport; would produce a poor mobile experience despite Section 9's requirement that mobile be first-class |
| Distinct layouts per breakpoint, designed intentionally for each | Each breakpoint gets a layout that actually works for its constraints | More design surface — three layout states per template instead of one |

**Recommendation:** Distinct, intentional layouts per breakpoint:
- **Desktop:** Persistent sidebar (UX-001), horizontal Capability Tabs (UX-010), table-based lists (UX-017).
- **Tablet:** Collapsible sidebar (icon-only by default, expandable), horizontal tabs retained if width allows, table lists retained.
- **Mobile:** Sidebar becomes a bottom nav bar or slide-out drawer (not a persistent rail), Capability Tabs collapse to an accordion (UX-010), lists remain table-like but with reduced columns (prioritizing the entity name and its single most important status field).

**Trade-offs:** Three layout states per major template to design, review, and keep behaviorally equivalent — a real but necessary cost given Section 9's mobile-web requirement.

**Future Impact:** High — this, combined with UX-001, is foundational to every screen in the product.

**Status:** Pending Approval

---

## Visual Language

### UX-040: Visual Tone & Information Density

**Description:** The product's overall tone, personality, information density, spacing philosophy, and minimalism level — deliberately not including any color decisions.

**Why This Decision Matters:** LifeOS holds financial, medical, and identity data for years of a person's life — its visual language needs to earn and hold trust, not just look modern. This also resolves the tone question flagged as a constraint-not-yet-confirmed in `00_Design_Handoff.md`, Section 10.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Warm, friendly, consumer-app personality (rounded, playful, illustration-forward) | Approachable, lowers the intimidation factor of "life admin" | Risks undermining trust for a product handling identity documents, medical records, and bank details — can read as not serious enough |
| Premium, minimal, high-density personality (precise, restrained, utilitarian) | Matches the seriousness of the data; scales well to real data volume (`00_Design_Handoff.md`, Section 7) | Can feel cold or clinical if taken too far, especially for first-time/empty-state moments |
| Calm and trustworthy, moderately dense, restrained but not cold — precise typography and generous-but-not-wasteful spacing, minimal ornamentation, warmth expressed through clarity and helpfulness rather than decoration | Balances trust and approachability; supports the assistant framing (calm, helpful, not alarmist) without reading clinical | Requires more design discipline to keep "calm" from drifting into "boring" over time |

**Recommendation:** Calm and trustworthy, moderately information-dense, restrained ornamentation — warmth comes from clarity, helpful copy, and the assistant framing (`02_Product_Requirements_Document.md`, Section 6), not from illustration or playful visual devices. Spacing should favor legibility and scanability for data-dense screens (lists, Overview field grids) over generous "consumer app" whitespace. This directly resolves the tone question from `00_Design_Handoff.md`, Section 10.

**Trade-offs:** Less immediately "delightful" on first impression than a warmer, more illustrated style — an accepted trade given the product's actual content.

**Future Impact:** High — the tone established now shapes every future visual decision, including the eventual Design System.

**Status:** Pending Approval

---

## Motion & Animation

### UX-041: Motion & Animation Philosophy

**Description:** The product's approach to motion — purely functional (state changes only) vs. expressive/decorative animation.

**Why This Decision Matters:** Motion choices affect perceived performance and polish, but also directly interact with the reduced-motion accessibility requirement (UX-038) and the calm tone established in UX-040.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| No motion beyond native browser defaults | Simplest, fewest accessibility considerations | Can feel abrupt; misses the chance to use motion to clarify state changes (e.g., an item moving from Today's Agenda to Recent Activity) |
| Rich, expressive animation throughout (page transitions, decorative micro-interactions) | Visually polished, memorable | Works against the calm, restrained tone (UX-040); higher risk of motion-sickness triggers if `prefers-reduced-motion` isn't rigorously respected; more engineering cost |
| Functional motion only — used to clarify state changes and spatial relationships (e.g., a tab switching, a toast appearing/dismissing, a modal opening), never purely decorative | Reinforces understanding without adding visual noise; naturally aligns with reduced-motion fallbacks (functional motion can simplify to an instant state change with no loss of meaning) | Less visually distinctive than an expressive-animation approach |

**Recommendation:** Functional motion only — every animation must exist to clarify a state change or spatial relationship (a tab activating, a toast entering/leaving, a modal opening/closing, an item's urgency tier changing on the Dashboard). No purely decorative animation. This is consistent with the calm tone (UX-040) and makes reduced-motion support straightforward, since every functional animation has an obvious instant-transition equivalent.

**Trade-offs:** The product will read as less "flashy" than competitors that lean on decorative motion — an accepted trade given the tone direction.

**Future Impact:** Medium — a philosophy that guides many small decisions, but each individual animation is low-cost to adjust.

**Status:** Pending Approval

---

## Error Handling

### UX-042: Error Presentation & Recovery Pattern

**Description:** How errors (`06_Screen_Inventory.md`, Section 9) are presented, and what recovery path is offered.

**Why This Decision Matters:** A calm, trustworthy product (UX-040) needs errors to feel handled, not alarming — especially given the product's data sensitivity, where an unclear error during a save could make a user genuinely worried about losing important records.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Generic error messages ("Something went wrong") | Simple to implement everywhere | Unhelpful; increases user anxiety precisely when reassurance is needed most |
| Specific, plain-language error messages with a clear next step (e.g., "This file is too large — try a file under 25MB" rather than a raw error code) | Reduces anxiety, tells the user exactly what to do | Requires each error condition (`06_Screen_Inventory.md`, Section 9) to have dedicated, considered copy rather than a generic fallback |

**Recommendation:** Specific, plain-language messages with an explicit next step for every error condition in `06_Screen_Inventory.md`, Section 9, following the inline-vs-toast split already decided in UX-034 (errors requiring action are inline, near the point of failure). Never surface a raw technical error to the user.

**Trade-offs:** Requires dedicated copywriting effort per error condition rather than one generic fallback message.

**Future Impact:** Medium.

**Status:** Pending Approval

---

### UX-043: Confirmation & Undo Strategy

**Description:** When LifeOS asks for confirmation before an action, versus performing the action immediately with an Undo option.

**Why This Decision Matters:** Directly relevant to the Confirm Action modal already recommended for merging in `06_Screen_Inventory.md` (Confirm Archive / Delete / Permanent Delete) — this decision defines which actions actually need that modal at all.

**Options Considered:**

| Option | Pros | Cons |
|---|---|---|
| Confirm-before for every non-trivial action (archive, delete, remove relationship) | Prevents all accidental actions | Adds a click to very low-risk, easily-reversible actions (e.g., Archive, which is already fully reversible) — friction without proportionate benefit |
| Immediate action + Undo toast for everything, no confirmation modals at all | Fastest interaction for all actions | Genuinely destructive actions (Permanent Delete) shouldn't rely on a toast the user might miss or dismiss |
| Tiered: reversible actions (Archive, remove a Relationship, Soft Delete) use immediate action + Undo toast; irreversible actions (Permanent Delete, "delete forever" from Trash) use an explicit Confirm Action modal | Matches friction to actual consequence — fast for safe actions, deliberate for unsafe ones | Requires a clear, consistently-applied rule for which tier an action belongs to |

**Recommendation:** Tiered approach. Archive, Soft Delete (to Trash), and removing a Relationship are all reversible by design (`04_Information_Architecture.md`, Section 5) — these use immediate action plus an Undo toast (UX-034), not a confirmation modal, since the safety net already exists structurally. Permanent Delete alone uses the Confirm Action modal, since it is the one genuinely irreversible action in the product (`docs/decisions/DEC-007`).

**Trade-offs:** Users accustomed to "everything asks first" may be briefly surprised that Archive/Soft Delete happen immediately — mitigated by the Undo toast appearing right away and the fact that both are non-destructive by design.

**Future Impact:** Medium — this rule, once set, should apply consistently to every future destructive-adjacent action added to the product, not just the three current ones.

**Status:** Pending Approval

---

## Design System Principles

Every future component must follow these principles — expanded from the Product Principles (`02_Product_Requirements_Document.md`, Section 6) and IA Principles (`04_Information_Architecture.md`, Section 10), translated specifically for the design system:

1. **Platform-first.** A component is designed once, generically, and reused across Entity Types — never duplicated per Domain (directly enables the ~40-screen inventory in `06_Screen_Inventory.md` instead of ~336).
2. **Consistency over novelty.** No Entity Type or Domain earns a bespoke visual treatment without a documented, approved reason (see UX-008, Section 5).
3. **Progressive disclosure.** Required, common actions are always immediate and low-friction (viewing an Overview, adding an Attachment); powerful but less-common capabilities (Custom Fields, Custom Relationships, Advanced Filters) are present but never in the way of the common case.
4. **Recognition over recall.** Interface elements should be self-explanatory in context (the entity chip from UX-025, the urgency tiers from UX-007) rather than requiring the user to remember what an icon or color means from having read documentation.
5. **Reduce cognitive load.** Every screen answers one of the five guiding questions (`01_Product_Vision.md`) as directly as possible — if a component doesn't serve *where, when, how much, what's related,* or *what's next,* question whether it belongs.
6. **Accessibility by default, not by exception.** Every component meets WCAG 2.1 AA (UX-036–038) from its first design draft, not as a later remediation pass.
7. **Calm over urgent, by default.** Visual urgency (color, iconography, motion) is reserved for genuinely time-sensitive states (Overdue/Alert, per J9.1) — never used for routine information, so that when it does appear, it's meaningful.
8. **Design for longevity of data, not just the demo state.** Every list, table, and Dashboard widget must remain usable with hundreds of entities and years of history, not just the first few records a new user creates.
9. **Every component has a defined empty, loading, and error state.** No component ships with only its "happy path" designed (directly operationalizes `06_Screen_Inventory.md`, Sections 8–10).

---

## Future UX Considerations

Decisions deliberately postponed until after MVP, with the reasoning already stated in their respective entries above:

| Deferred Decision | Why It Can Wait |
|---|---|
| Card-view toggle for Entity Lists (UX-017) | Table view alone satisfies MVP; revisit only if real usage shows demand for a visual/gallery browsing mode |
| Bulk actions on Entity Lists (UX-019) | No current User Journey requires it; needs real usage evidence first |
| Saved Searches (UX-023) | Same reasoning as bulk actions — a plausible, unvalidated feature |
| Interactive relationship graph view (UX-024) | The grouped-list + Cross-Entity Navigation pattern already satisfies the underlying need; graph UIs are high-cost and hard to keep usable |
| Attachment folders/organization (UX-031) | Would introduce a new hierarchy concept not otherwise present in the IA; flat + filterable is sufficient for MVP data volumes |
| Attachment version history (UX-032) | Already deferred at the product level (`00_Glossary.md`) |
| Dashboard customization beyond auto-collapse (UX-006) | Fixed composition with auto-collapse delivers most of the value without the design/engineering cost of full customization |
| Dark mode (`00_Design_Handoff.md`, Open Decision #7) | Not yet resolved even as a decision to make — recommend deciding before the Design System is built, since it affects every color token, but the visual execution itself can follow after MVP ships |

---

## Quality Review

**A genuine simplification found while writing this document, not previously identified — since approved as `docs/decisions/DEC-012-remove-entity-settings-tab.md`:** the **Entity Settings** tab (part of the Standard Entity Capability Set, `03_Feature_Catalogue.md` Section 2.1) had no defined content beyond Archive/Delete actions (`06_Screen_Inventory.md` described it as "minimal in V1"). Given UX-043 already establishes that Archive is an immediate action with an Undo toast (not a page you navigate to), a full seventh Capability Tab wasn't justified for content that amounted to two menu items. **Applied:** the Entity Settings tab is replaced with a small overflow (⋮) menu on the Entity Overview header, containing Archive and Delete. This removes one tab from the Capability Tab Shell (UX-010) everywhere it's used and removes one entry from the Screen Catalogue — `06_Screen_Inventory.md` (now v1.1) reflects the updated ~39-screen estimate.

**Inconsistency identified:** `05_User_Journeys.md` (J1.4, edge case) states an Entity is created successfully "regardless of how sparse its data is," which UX-013 and UX-015 both build on directly — no conflict found, but it's worth noting explicitly that this document's form-related decisions (UX-013, UX-015, UX-016) are all downstream of, and constrained by, that existing product decision rather than independently derived. Design should not treat form UX as fully open; the "no draft state" rule is fixed.

**Open question not yet resolved by any prior document:** the "Expiring Soon" window is stated as a "default 30 days" and configurable (`03_Feature_Catalogue.md`, Section 2.2) but it's not decided whether that window is uniform across every expiry-bearing Entity Type, or whether it should vary (e.g., a Document might reasonably warrant a longer lead time than a Subscription renewal). This affects UX-007's tiering logic directly and should be settled as a product decision, not a UX one — flagged here rather than answered, since it's outside this document's scope.

**Reusable interaction patterns worth formalizing first in the Design System**, because they recur across the largest number of decisions in this record: the **entity chip** (UX-025), the **Confirm Action modal** (UX-043), the **filter panel + always-visible sort** pattern (UX-018), and the **urgency-tier treatment** (UX-007, reused by UX-035 and the Notification Center). Building these four first will unblock the largest share of subsequent screen design.

**Where the Entity Platform most reduces UI complexity:** every decision tagged "High" Future Impact in this document — UX-008 (Generic Entity Layout), UX-009 (Overview field layout), UX-010 (Tab interaction) — is decided exactly **once** and applies to all 28 Entity Types simultaneously, which is the entire reason `06_Screen_Inventory.md` arrives at ~40 screens instead of ~336. This document adds no exceptions to that model; every entity-specific UX question considered (e.g., UX-011, relationship presentation) resolved to a generic pattern rather than a bespoke one.

**Hardest decisions to change after implementation** (all decisions rated Future Impact: High above, gathered here for quick reference): UX-001 (Primary Navigation), UX-008 (Generic Entity Layout), UX-010 (Tab Interaction Pattern), UX-013 (Form Structure), UX-036/037/038 (Accessibility baseline), UX-039 (Responsive Strategy), UX-040 (Visual Tone). These should be prioritized for approval and validated with a real prototype before any other design work proceeds.

---

## UX Decisions Requiring Product Owner Approval

Only decisions that would materially change the product if decided differently, or that resolve a previously-open question from `00_Design_Handoff.md`:

1. **UX-001 — Primary Navigation Pattern** (sidebar + top bar hybrid). Foundational; touches every screen.
2. **UX-008 — Generic Entity Layout**. The single highest-leverage decision in the document; every Entity Type depends on it.
3. **UX-010 — Tab Interaction Pattern**, including the mobile accordion approach. Resolves Open UX Decision #2 from `00_Design_Handoff.md`.
4. **UX-013 — Form Structure** (single-page, expandable, vs. multi-step wizard).
5. **UX-036 — Accessibility Conformance Target** (WCAG 2.1 AA). Sets a binding standard for all future design and engineering work.
6. **UX-039 — Responsive Strategy**, specifically the mobile navigation change (sidebar → bottom nav/drawer). Confirms mobile-web is genuinely first-class, not a scaled-down afterthought.
7. **UX-040 — Visual Tone & Information Density**. Resolves the tone question left open in `00_Design_Handoff.md`, Section 10, and shapes every later visual decision.
8. **Scope deferrals: UX-019 (Bulk Actions), UX-023 (Saved Searches), UX-024 (No Graph View).** These are decisions to *not* build something plausible — confirm the reasoning (no validated journey requires them yet) is acceptable before Design commits to simpler MVP surfaces.
9. ~~The Entity Settings tab elimination~~ — **Approved as `docs/decisions/DEC-012-remove-entity-settings-tab.md`.** `06_Screen_Inventory.md` and `04_Information_Architecture.md` have been updated accordingly.
10. **Dark mode** (`00_Design_Handoff.md`, Open Decision #7) — still entirely undecided even as a yes/no; needs a decision (not necessarily execution) before the Design System's color tokens are built.

---

## Document Status

**Version:** 1.1
**Status:** Draft
**Dependencies:**
- `docs/design/00_Design_Handoff.md`
- `docs/product/06_Screen_Inventory.md`
- `docs/product/05_User_Journeys.md`
- `docs/product/04_Information_Architecture.md`
- `docs/product/03_Feature_Catalogue.md`
- `docs/product/00_Glossary.md`
- `docs/decisions/DEC-012-remove-entity-settings-tab.md`

**Generated On:** 2026-07-02
**Revision Note:** v1.1 applies `DEC-012` (Entity Settings tab removed, item 9 of the Final Section resolved) and confirms items 1–2 of the Final Section as approved per the Product Owner's response.

**Next Document:** Sitemap (per `PROJECT_STATUS.md`, Phase 2 — Design), once the remaining decisions in the Final Section above are approved.
