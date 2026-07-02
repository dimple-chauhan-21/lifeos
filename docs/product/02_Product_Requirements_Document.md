# LifeOS — Product Requirements Document (PRD)

# Document Information

| Field | Value |
|---|---|
| Document | Product Requirements Document |
| File | `docs/product/02_Product_Requirements_Document.md` |
| Version | 1.0 |
| Status | Draft |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | `01_Product_Vision.md` |
| Used By | `03_Feature_Catalogue.md` and all subsequent Product, Design & Engineering Documents |

---

## 1. Executive Summary

LifeOS is a self-hosted, entity-driven personal operating system that gives an individual one secure place to store, connect, and retrieve every important record of their life — vehicles, properties, documents, finances, health records, and more. Rather than being built as a set of disconnected modules, LifeOS is built on a single **generic Entity Platform**, with **Vehicle as its reference implementation**, so that every future domain (Property, Health, Documents, Devices, Pets) reuses the same capabilities — attachments, timeline, reminders, relationships, expenses, notes, custom fields, and audit history — instead of being rebuilt from scratch.

Version 1.0 targets a **single user**, **self-hosted via Docker**, accessed **web-first**, with a Flutter mobile client planned for a later phase. Authentication is email/password. No AI capability ships in the MVP, though the architecture is deliberately kept AI-ready. This document defines what LifeOS is, who it is for, and how success will be measured — it intentionally excludes all technical and implementation detail, which is covered in the `docs/architecture/` series.

---

## 2. Product Vision

The full product vision is defined in [`01_Product_Vision.md`](./01_Product_Vision.md) and is treated as fixed input to this document. In summary: LifeOS exists to answer five questions a person routinely asks about their own life — *where did I keep that, when did this happen, how much did I spend, what's related, and what do I need to do next* — through a single, self-hosted, entity-driven platform rather than a collection of single-purpose apps.

This PRD translates that vision into concrete product requirements: mission, goals, principles, audience, personas, boundaries, and success metrics.

---

## 3. Mission Statement

> **To give every person a private, structured, and permanent home for the information their life depends on — built on a platform, not a pile of features.**

LifeOS's mission is not to be the most feature-rich app in any single category (it will not out-budget YNAB or out-organize a dedicated EHR). Its mission is to be the **one place that connects all of them**, owned entirely by the person whose life it represents.

---

## 4. Problem Statement

### 4.1 Current Problems

| Problem | Impact |
|---|---|
| Important documents are scattered across email, cloud drives, messaging apps, and physical paper | No single source of truth; things get lost |
| Renewal dates (insurance, registration, subscriptions) are tracked inconsistently or not at all | Missed renewals, lapsed coverage, late fees |
| No structural link between related records (a vehicle, its insurance policy, its service history, its documents) | Manually reconstructing context every time something needs attention |
| Sensitive data (medical, financial, identity) is handed to third-party cloud services by default | Privacy risk, and discomfort with the loss of control over highly personal data |
| If something happens to the person managing this information, no one else can find or understand it | High-stakes failure mode during emergencies, illness, or death |

### 4.2 Existing Solutions

| Category | Examples | What it solves |
|---|---|---|
| Budgeting/finance apps | YNAB, Mint-alikes | Transactions and budgets only |
| Cloud storage / note apps | Google Drive, Evernote, Notion | Generic file/note storage, no domain structure |
| Password managers | 1Password, Bitwarden | Credentials only |
| Vehicle-specific apps | Carfax-adjacent apps, dealer apps | Vehicle history only, not integrated with anything else |
| Document scanners | Genius Scan, Adobe Scan | Capture only, no ongoing management |
| Physical folders / spreadsheets | — | Familiar but manual, unsearchable, single point of failure |

### 4.3 Why Existing Solutions Fail

- **They are module-driven, not entity-driven.** Each tool owns one slice of life and has no concept of how a vehicle relates to its insurance, or a property relates to its utility bills and maintenance history.
- **They fragment context.** Retrieving the full picture of "everything about my car" means checking four different apps.
- **They require trusting a third party with the most sensitive categories of personal data**, often bundled with ad-supported or data-monetized business models.
- **None of them are built to be a system of record for someone else** in an emergency — they are built for the original user only, in the moment, not for long-term continuity.

### 4.4 Why LifeOS Is Different

LifeOS is built **platform-first, entity-driven, and self-hosted**: one consistent engine gives every domain the same capabilities (attachments, timeline, reminders, relationships, expenses, notes, custom fields), so information about a vehicle, a property, or a policy is never siloed from the things it's actually connected to — and the whole system remains under the user's own control rather than a third party's.

---

## 5. Product Goals

### 5.1 Short-Term Goals (V1 / MVP)
- Deliver a working, self-hosted single-user application covering the Assets category, with Vehicle as a fully realized reference implementation of the Entity Platform.
- Prove that the Entity Platform's core capabilities (Attachments, Timeline, Reminders, Relationships, Expenses, Notes, Custom Fields, Activity Log, Audit Log) are genuinely generic and reusable, not Vehicle-specific.
- Deliver Global Search and an assistant-style Dashboard that surface what needs attention today, not analytics.

### 5.2 Long-Term Goals
- Extend the same platform across all defined life categories (Assets, People, Finance, Health, Documents, Planning, Home, Knowledge) without rebuilding core infrastructure per domain.
- Support shared household use and, eventually, a hosted multi-tenant product — without a platform rewrite.
- Introduce AI-assisted capabilities (document extraction, smart reminders, natural-language search) once the platform and data model are proven, without retrofitting architecture.

### 5.3 User Goals
- "I want to find any important document or record about my life in seconds, not minutes."
- "I want to never miss a renewal, expiry, or payment again."
- "I want to understand, at a glance, everything connected to a given vehicle, property, or policy."
- "I want to trust that my most sensitive personal data is not being handed to a third party."

### 5.4 Product Goals
- Every new domain added to LifeOS should cost materially less engineering effort than the one before it, because it reuses the platform rather than reinventing it.
- Every entity in the system, regardless of domain, should look, feel, and behave consistently.
- The system should degrade gracefully with incomplete data — a record with only a name and a photo is still useful, not broken.

---

## 6. Product Principles

These principles are binding on every future feature decision:

1. **Entity-first, not module-first.** New functionality is expressed as entity types and capabilities on the platform, not as a bolted-on standalone module.
2. **Platform before features.** A capability is built once, generically, and reused — not duplicated per domain.
3. **Consistency over novelty.** Every entity type follows the same interaction pattern (Overview, Timeline, Attachments, Notes, Expenses, Reminders, Relationships, Activity, Settings). A domain does not get a bespoke UI just because it's new.
4. **Privacy and ownership by default.** The user's data belongs to the user. Self-hosting is the default deployment model; no feature may require handing data to a third party without explicit, informed consent.
5. **Progressive disclosure.** The product is simple by default (create an entity, attach a file, set a reminder) and powerful when needed (custom fields, relationships) — complexity is opt-in, never mandatory.
6. **Data portability is non-negotiable.** A user must always be able to get their complete data and files back out of the system in a usable form.
7. **AI must earn its place.** No AI capability ships until it demonstrably serves the product's guiding questions (*where, when, how much, what's related, what's next*) better than a non-AI solution — and the MVP ships with none.
8. **Secure by default.** Sensible, secure configuration is the out-of-the-box experience; the user should never need security expertise to be safe.

---

## 7. Target Audience

### 7.1 Primary
Individuals who currently manage their own life administration across a fragmented mix of email, cloud storage, note apps, and paper, and who are motivated enough by the pain of that fragmentation to adopt a dedicated system. Comfortable enough with technology to self-host via Docker, or willing to have it hosted for them once that option exists.

### 7.2 Secondary
Households and families who want to extend a single individual's LifeOS setup to shared use — once household/family sharing ships. Early adopters who value data ownership and self-hosting as a matter of principle (a natural audience overlap with the self-hosting/open-source community).

### 7.3 Future
Non-technical users who want the benefits of LifeOS without operating their own infrastructure, served by a future hosted multi-tenant offering. Small households needing "emergency access" / legacy-planning style sharing with a trusted contact.

---

## 8. User Personas

### Persona 1 — Rohan Mehta, "The Overwhelmed Household Manager"
- **Age / Role:** 38, Marketing Manager, married with two children
- **Context:** Manages nearly all administrative matters for his household — insurance renewals, school documents, medical records for the kids, home maintenance.
- **Goals:** One place to track every renewal and document so nothing is missed; ability to eventually let his spouse access the same information.
- **Frustrations today:** Insurance policies are in email; his car's service history is in a mechanic's notebook; he once missed a policy renewal because the reminder email went to spam.
- **How LifeOS helps:** Centralized reminders across every policy and document, regardless of category, surfaced on one dashboard.
- **Quote:** *"I don't need ten apps. I need one place that remembers what I'd forget."*

### Persona 2 — Ananya Verma, "The Multi-Asset Owner"
- **Age / Role:** 45, small business owner, owns two vehicles, a home, and rental property
- **Context:** Tracks vehicle registrations, insurance, maintenance schedules, and property-related bills across multiple assets.
- **Goals:** See, per asset, everything related to it — insurance, service history, expenses, documents — without cross-referencing four different tools.
- **Frustrations today:** Vehicle service records live in a garage app; property documents live in a shared drive; there's no link between an asset and its associated costs over time.
- **How LifeOS helps:** Vehicle and Property entities with full relationship, timeline, and expense tracking built in from day one, since Vehicle is the platform's reference implementation.
- **Quote:** *"I want to click on my car and see everything about it — not go looking in five places."*

### Persona 3 — Karan Shah, "The Digital-Native Solo Professional"
- **Age / Role:** 27, software engineer, single, minimalist approach to tools
- **Context:** Deliberately avoids app sprawl; currently uses a single note app for everything, which has become an unstructured dumping ground.
- **Goals:** Replace ten single-purpose apps with one structured system; values self-hosting and data ownership on principle.
- **Frustrations today:** His note app has no structure — searching for "car insurance" returns three years of unrelated notes.
- **How LifeOS helps:** Structured entities with typed fields and custom fields give him organization without sacrificing flexibility; self-hosted deployment matches his values.
- **Quote:** *"I don't want another app. I want infrastructure I control."*

### Persona 4 — Priya Nair, "The Health & Records-Conscious User"
- **Age / Role:** 52, manages a chronic health condition, tracks medical records for herself and an aging parent
- **Context:** Deeply uncomfortable with medical and identity data living in third-party cloud apps; keeps paper copies of everything as a fallback.
- **Goals:** A private, self-hosted place for medical records, prescriptions, and vaccination history that she fully controls.
- **Frustrations today:** Patient portals are fragmented across providers; nothing connects her own records to her parent's.
- **How LifeOS helps:** Self-hosted-by-default architecture and field-level encryption for sensitive data address her core trust concern; Relationships let her link her own records to a family member's (once household sharing ships).
- **Quote:** *"I'll use this the day I stop worrying about where my data actually lives."*

### Persona 5 — Vikram Desai, "The Homeowner Planning Ahead"
- **Age / Role:** 61, recently retired, homeowner
- **Context:** Increasingly thinking about what happens to his affairs — insurance, property documents, financial records — if he's incapacitated, and who would even know where to look.
- **Goals:** A single, organized system his family could understand and access in an emergency, even though he manages it alone today.
- **Frustrations today:** His important documents are in a mix of a home safe, email, and a filing cabinet; his family has no idea what exists or where.
- **How LifeOS helps:** Represents the future "family sharing" and emergency-access audience — validates why SaaS-ready, shareable architecture matters even though V1 is single-user.
- **Quote:** *"Right now, if something happened to me, my family would have no idea where to start."*

---

## 9. Product Boundaries

### LifeOS IS
- A self-hosted, entity-driven personal operating system for life administration
- A single source of truth for documents, assets, records, and their relationships to one another
- A platform where every domain (Vehicle, Property, Health, Documents, Devices, Pets, …) shares the same core capabilities
- A system designed for data ownership, portability, and long-term durability

### LifeOS IS NOT
- A full double-entry accounting or budgeting engine (not a YNAB/Quicken replacement)
- An Electronic Health Record (EHR) system or a substitute for provider medical records
- A general-purpose document editor or note-taking tool
- A social network or sharing platform
- An AI assistant or chatbot, in the MVP or near term
- A bank-integrated financial transaction platform

### Out of Scope (for now)
- Bank/financial account integrations (e.g., Plaid-style aggregation)
- AI-powered features of any kind
- Native mobile apps (a Flutter app is planned for a later phase, not V1)
- Multi-user / household sharing (planned, not in V1)
- User-defined custom modules (custom *fields* are supported; user-defined new entity *types* are not)
- Any plugin, marketplace, or third-party extension system

---

## 10. Success Metrics

Because V1 is a single-user, self-hosted product, success is measured primarily by **completeness, reliability, and platform reuse efficiency** rather than by growth metrics. Growth/business metrics become relevant once a hosted, multi-user offering exists.

| Category | Metric | Target for V1 |
|---|---|---|
| Platform reuse | Engineering effort to add a new entity domain after Vehicle (e.g., Property) | Materially lower than Vehicle's build effort; no new platform-level infrastructure required |
| Data completeness | % of created entities with at least one attachment, reminder, or custom field populated | Indicates the platform is being used as intended, not just as a flat list |
| Reliability | Data loss incidents | Zero |
| Reliability | Successful backup/restore test | Verified at least once before V1 is considered production-ready |
| Usability | Time to locate a specific record via Global Search | Under 5 seconds for a user familiar with the system |
| Engagement (single-user context) | Weekly active use of the Dashboard | Regular use, since the Dashboard is the "what needs attention" entry point |
| Consistency | New entity types visually/behaviorally indistinguishable in structure from Vehicle | 100% adherence to the 9-capability entity contract |
| Trust / Security | Sensitive fields (identity numbers, financial account numbers) encrypted at the application layer | 100% of defined sensitive fields |

---

## Document Status

**Version:** 1.0
**Status:** Draft
**Dependencies:**
- `docs/product/01_Product_Vision.md`

**Generated On:** 2026-07-02

---

## Next Documents

The next document to generate is `docs/product/03_Feature_Catalogue.md`, which will enumerate the concrete features of LifeOS — organized by platform capability (Entity Platform, Attachments, Timeline, Reminders, Relationships, Expenses, Notes, Custom Fields, Global Search, Dashboard, Activity/Audit Log) and by domain (starting with Vehicle as the reference implementation) — describing what each feature does at a product level, without technical implementation detail.
