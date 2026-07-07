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

---

## Phase 1.2 - Workspace & Development Tooling

Completed:
- Configured the pnpm workspace (`pnpm-workspace.yaml`, root `package.json` pinning `pnpm@11.10.0`, `.nvmrc` pinning Node 24 LTS)
- Bootstrapped `apps/web` tooling only (no framework yet): TypeScript 6.0 (strict), ESLint 10.6.0 (flat config) + typescript-eslint 8.62.1, Prettier 3.9.4
- Bootstrapped `apps/api` tooling only (no framework yet), managed via `uv`: Python 3.13 pinned, Ruff 0.15.20, mypy 2.1.0 (strict)
- Added one throwaway file per app (`apps/web/src/example.ts`, `apps/api/app/example.py`) to prove the full lint/format/typecheck pipeline works end-to-end — both to be removed when Phases 1.3/1.4 bootstrap the real applications
- Verified all six root workspace scripts (`lint:web`, `lint:api`, `format:web`, `format:api`, `typecheck:web`, `typecheck:api`) run correctly

Versions chosen and why: see the version table presented for review before implementation (Node 24 LTS over 25/26; Python 3.13 over 3.14 for upcoming backend library maturity; TypeScript 6.0 stable over the 7.0 Go-rewrite still in RC; `@eslint/js` corrected to 10.0.1 after the registry rejected the assumed 10.6.0 — versions don't track 1:1 with the main `eslint` package).

Environment notes (not project config, specific to this machine):
- `~/.local` is owned by `root`, not the user — broke both the `uv` official installer and `uv`'s default Python-install directory. Worked around by installing `uv` via Homebrew and redirecting `UV_PYTHON_INSTALL_DIR`/`UV_CACHE_DIR` to `~/.cache/uv/*`. Not fixed at the system level (out of this project's scope) — flagged here so it isn't a mystery later.
- This machine's local Node (25.9.0) and system Python (3.9.6, macOS-bundled) are both older/different from the project's targets (Node 24 LTS, Python 3.13) — `uv` manages its own Python independently, so this only really matters for Node; installing Node 24 via `nvm` (already pinned in `.nvmrc`) is recommended locally.

Commit:
```
chore: configure workspace tooling (TypeScript, ESLint, Prettier, Ruff, mypy)

Set up pnpm workspace (Node 24, pnpm 11.10.0) and per-app dev
tooling only — no application frameworks yet. apps/web: TypeScript
6.0 (strict), ESLint 10.6.0 (flat config), Prettier 3.9.4. apps/api:
Python 3.13 via uv, Ruff 0.15.20, mypy 2.1.0 (strict). Throwaway
example files validate the full pipeline; removed in Phases 1.3/1.4.
```
