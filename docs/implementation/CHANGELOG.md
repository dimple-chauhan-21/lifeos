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

---

## Phase 1.3 - Backend Bootstrap

Completed:
- Removed `apps/api/app/example.py` (the Phase 1.2 placeholder — cleaned up at the start of this phase, per the refined rule to not let placeholders outlive the phase that created them)
- Added FastAPI 0.139.0 + `uvicorn[standard]` 0.50.2 as runtime dependencies; Pydantic 2.13.4 and Starlette 1.3.1 resolved transitively by FastAPI (not pinned directly, per FastAPI's own guidance to let it manage those)
- Added pytest 9.1.1 as a dev dependency
- Created `app/main.py`: a FastAPI instance with a single `/health` endpoint — nothing else (no routers, no DB, no auth yet)
- Created `tests/test_health.py`: one passing test
- Added `pythonpath = ["."]` to `[tool.pytest.ini_options]` so `tests/` can import `app` without a package install step

Two things caught only by actually running verification, not assumed from documentation:
1. `from app.main import app` failed in pytest with `ModuleNotFoundError` until `pythonpath = ["."]` was added — the project has no build-system/packaging step yet, so pytest didn't know to put the project root on `sys.path`.
2. Starlette's `TestClient` emits a deprecation warning for `httpx`, pointing at `httpx2`. **Initially swapped to `httpx2`, then reverted after deeper verification requested during review** (see Correction below) — kept on `httpx` 0.28.1, accepting the (cosmetic, non-functional) warning.

**Correction, made before approval:** the initial swap to `httpx2` was based on the warning's own wording and `httpx2`'s self-description, not on official documentation. Checked against primary sources on request:
- FastAPI's official testing docs (fastapi.tiangolo.com) still explicitly instruct `pip install httpx` — no mention of `httpx2`.
- `httpx` (`encode/httpx`) is not deprecated as a project — only its use as Starlette's `TestClient` backend specifically is warned against.
- `httpx2` support in Starlette's `TestClient` traces to one merged PR plus a single terse maintainer reply in a GitHub discussion — no migration guide, rationale, or stability/timeline commitment published anywhere found.
- Conclusion: not an officially documented ecosystem recommendation yet. Reverted to `httpx` 0.28.1 per the standing preference for ecosystem stability over early adoption of a newer package. The warning is harmless and can be revisited once (if) FastAPI's own documentation adopts `httpx2`.

Verified beyond the test suite: booted a real `uvicorn` process and confirmed `GET /health` returns `200 {"status": "ok"}` over actual HTTP, not just via `TestClient`.

Commit:
```
feat(api): bootstrap FastAPI application with health endpoint

Add FastAPI 0.139.0 + uvicorn[standard] 0.50.2 as the first runtime
dependencies. app/main.py exposes a single /health endpoint — no
routing, database, or auth yet (later phases). Add pytest 9.1.1 and
httpx 0.28.1 (per FastAPI's official docs, despite Starlette's
TestClient httpx2 deprecation warning — not yet an officially
documented ecosystem recommendation, see CHANGELOG for verification).
Fix pytest module resolution via pythonpath.
```
