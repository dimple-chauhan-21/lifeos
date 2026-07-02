# LifeOS — Product Vision

# Document Information

| Field | Value |
|---|---|
| Document | Product Vision |
| File | `docs/product/01_Product_Vision.md` |
| Version | 1.0 |
| Status | Draft |
| Owner | Product Team |
| Last Updated | 2026-07-02 |
| Depends On | None (foundational document) |
| Used By | All Product, Design & Engineering Documents |

---

## 1. Vision Statement

> **LifeOS is the operating system for a person's life administration — a single, secure, self-hosted place where every important document, asset, record, and commitment lives, connects, and can be found again in seconds.**

Where today a person's important information is scattered across email attachments, photo galleries, glove-box folders, note apps, and a dozen single-purpose services, LifeOS unifies it around the things that actually make up a life — a vehicle, a property, a policy, a person, a document — instead of forcing that life into someone else's app boundaries.

---

## 2. The Problem We're Solving

Modern life generates a constant stream of records that matter: insurance policies, vehicle registrations, medical reports, warranties, contracts, identity documents, subscriptions, loans. None of these are individually complex to store — but collectively, they end up nowhere in particular. People solve this today with a patchwork of email search, cloud drive folders, note apps, and physical paper, and the patchwork fails exactly when it matters most: at renewal time, during an emergency, or when someone else needs to step in.

This is explored in depth in the Product Requirements Document (`docs/product/02_Product_Requirements_Document.md`); this document defines the vision that PRD is built on.

---

## 3. What LifeOS Is

LifeOS is a **self-hosted personal operating system** built around a **generic Entity Platform**: every meaningful thing in a person's life — a vehicle, a property, a policy, a device, a pet, a document — is modeled as an entity that automatically gains the same core capabilities: attachments, timeline, reminders, relationships, expenses, notes, custom fields, and activity history.

Rather than being built as a collection of independent modules (a "finance app" bolted to a "document app" bolted to a "vehicle tracker"), LifeOS is built **platform-first**: one consistent entity engine powers every domain, so that adding a new domain — Property, Health, Devices, Pets — means configuring the platform, not building a new app from scratch. **Vehicle is the reference implementation** that proves this platform out end-to-end before it is reused elsewhere.

---

## 4. Our Guiding Philosophy

LifeOS is not judged by how many features it has. It is judged by whether it can answer the questions a person actually asks themselves:

- *"Where did I keep that?"*
- *"When did this happen?"*
- *"How much did I spend on this?"*
- *"What else is related to this?"*
- *"What do I need to do next?"*

If a feature doesn't help answer one of these questions, it doesn't belong in LifeOS. This is the product's north star and the filter every future feature is measured against.

---

## 5. Who LifeOS Is For

LifeOS V1 is built for **a single individual** who wants one trustworthy place to manage the administrative surface of their life — someone currently juggling that information across email, cloud drives, note apps, and paper. The architecture is deliberately **SaaS-ready**, so the same platform can later extend to shared household use and, eventually, a hosted multi-tenant product — without requiring a rebuild. Detailed personas and audience segmentation are defined in the PRD.

---

## 6. What Makes LifeOS Different

| Existing approach | Why it falls short | LifeOS's approach |
|---|---|---|
| Single-purpose apps (finance tracker, document scanner, vehicle log) | Each captures one slice of life; nothing connects across them | One entity platform, every domain interconnected |
| General note-taking / cloud drive apps | Unstructured; no reminders, no relationships, no domain-specific fields | Structured entities with typed fields, reminders, and relationships built in |
| Cloud SaaS life-management apps | Sensitive personal/financial/medical data held by a third party | Self-hosted by default; you own your infrastructure and your data |
| Module-driven "all-in-one" apps | Every module looks and behaves differently; each domain is built from scratch | Platform-first — every domain reuses the same capabilities and interface pattern |

---

## 7. Long-Term Aspiration

Over the next several years, LifeOS aims to become the default answer to "where do I keep track of my life" — starting as a single-user, self-hosted tool, extending naturally to shared household use, and eventually to a hosted product usable by many independent users or families, without ever compromising on data ownership or the entity-first architecture that makes it extensible. AI is deliberately excluded from the MVP, but the platform is designed so that intelligence (smart reminders, document extraction, natural-language search) can be layered on later without architectural rework.

---

## 8. Foundational Product Decisions

The following decisions are approved and treated as fixed inputs to all subsequent product and architecture documents. They are elaborated on throughout the PRD and later architecture documents, not repeated here in full:

- Single-user application for V1; SaaS-ready architecture
- Self-hosted, deployed via Docker
- Web-first; a Flutter mobile application is planned for a later phase
- Email/password authentication for V1
- No AI in the MVP; architecture must not preclude AI later
- Generic Entity Platform, built platform-first
- Vehicle as the reference implementation of the Entity Platform
- Platform capabilities: Global Search, Assistant-style Dashboard, Custom Fields, Attachments, Timeline, Relationships, Expenses, Notes, Activity Log, Audit Log

---

## Document Status

**Version:** 1.0
**Status:** Draft
**Dependencies:** None (foundational document)
**Generated On:** 2026-07-02

## Next Documents

The next document to generate is `docs/product/02_Product_Requirements_Document.md`, which translates this vision into a concrete product definition: mission, goals, principles, target audience, user personas, product boundaries, and measurable success criteria.
