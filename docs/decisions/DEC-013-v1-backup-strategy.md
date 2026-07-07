# DEC-013: V1 Backup Strategy — Automated Daily Postgres Backups to a Local Docker-Mounted Directory

# Document Information

| Field | Value |
|---|---|
| Document | DEC-013 |
| File | `docs/decisions/DEC-013-v1-backup-strategy.md` |
| Version | 1.0 |
| Status | Approved |
| Owner | Engineering Team |
| Last Updated | 2026-07-02 |
| Depends On | `docs/architecture/00_Engineering_Overview.md` |
| Used By | `docs/architecture/00_Engineering_Overview.md`, future backup/restore implementation |

---

## Context
`docs/architecture/00_Engineering_Overview.md`, Section 16 flagged backup destination and mechanism as an open question dating back to the original Phase 0 discussion — the architecture needed *a* concrete default for V1 without prematurely committing to a specific cloud provider before one was ever decided.

## Decision
V1 backups are **automated, daily PostgreSQL dumps** (`pg_dump`, encrypted at rest), written to a **local Docker-mounted backup directory** on the same self-hosted host — a named volume or bind mount separate from the primary Postgres data volume. The backup job (a Celery Beat scheduled task, per `docs/architecture/00_Engineering_Overview.md`, Section 10) is implemented so the destination is a configurable target, not hardcoded to the local filesystem — this keeps the mechanism provider-agnostic for future cloud storage (e.g., an S3-compatible remote, or syncing the same backup directory to MinIO or an external object store) without a rewrite.

## Reason
A local, Docker-mounted directory requires no external account, no additional cost, and no new third-party dependency — consistent with the self-hosted, own-your-infrastructure ethos already established for the deployed product. Keeping the destination abstracted behind configuration (rather than hardcoding local-filesystem paths throughout the backup job) means adding a cloud destination later is a configuration change, not an architecture change.

## Alternatives Considered
- **Defer backups entirely until a cloud target is chosen** — rejected: leaves V1 with no recovery story at all, which is unacceptable given the sensitivity and irreplaceability of the data LifeOS holds (`docs/product/02_Product_Requirements_Document.md`, Section 10 success metrics explicitly require a verified backup/restore test).
- **Commit to a specific cloud provider now** (e.g., S3, Backblaze) — rejected: no cloud provider has been chosen for deployment yet (`docs/architecture/00_Engineering_Overview.md`, Section 16), and hardcoding one would need to be undone later; the provider-agnostic configuration approach avoids this without sacrificing a working V1 default.
