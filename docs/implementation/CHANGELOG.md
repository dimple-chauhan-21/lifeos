# LifeOS — Implementation Changelog

A running developer log of implementation progress, one entry per approved sub-phase, in order. Distinct from Git history (this explains *why* and ties back to the Roadmap/architecture) and from `PROJECT_STATUS.md` (which only tracks milestone-level acceptance, not per-sub-phase detail).

---

## Phase 1.1 - Repository Skeleton

Completed:
- Removed the pre-existing empty stub directories (`backend/`, `frontend/`, `infrastructure/`, `scripts/`) — untracked, no content, predated the approved architecture, and didn't match its naming (`apps/web`, `apps/api`, `infra/`)
- Created the approved monorepo skeleton: `apps/web/`, `apps/api/`, `infra/`, `.github/workflows/` (each currently a `.gitkeep` placeholder, populated in Phase 1.2 onward)
- Added `.editorconfig` (LF, UTF-8, 2-space indent default / 4-space for Python)
- Updated `README.md`: refreshed stack list (added Alembic), added a Repository Structure section, updated Current Status to point at the Roadmap and this changelog
- Extended `.gitignore`: added `.next/`, `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`
- **Deliberately not created**: `packages/api-types/` — deferred until a real API schema exists to generate types from, per the lazy-dependency-addition principle

Commit:
```
chore: initialize repository skeleton

Remove pre-architecture stub directories (backend/, frontend/,
infrastructure/, scripts/) and establish the approved monorepo
skeleton (apps/web, apps/api, infra, .github/workflows) per
docs/architecture/00_Engineering_Overview.md. Add .editorconfig,
refresh README, extend .gitignore for Next.js/Python tooling.
```
