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

---

## Phase 1.4 - Frontend Bootstrap

Completed:
- Removed `apps/web/src/example.ts` (the Phase 1.2 placeholder — cleaned up at the start of this phase)
- Added Next.js 16.2.10 + React/React DOM 19.2.7 as runtime dependencies
- Added Vitest 4.1.10, `@vitejs/plugin-react` 6.0.3, Testing Library (`@testing-library/react` 16.3.2, `@testing-library/jest-dom` 6.9.1), `jsdom` 29.1.1, and matching `@types/*` as dev dependencies
- Created `app/layout.tsx` + `app/page.tsx`: one placeholder page rendering "LifeOS" — no routing, styling, or state yet
- Created `vitest.config.ts` + `vitest.setup.ts`, and one smoke test (`app/page.test.tsx`) rendering the page
- Scope held to the lazy-dependency principle: no Tailwind, shadcn/ui, Zustand, TanStack Query, React Hook Form, or Zod — none needed for a single placeholder page

Versions verified directly against the npm registry, not search summaries — two corrections this surfaced:
1. A blog post referenced "Next.js 16.3", but `16.3.0` doesn't exist as a stable release — only `16.3.0-preview.x`/`-canary.x`. Used `16.2.10` (the registry's actual `latest` tag).
2. `@types/node`'s "latest" resolved to `26.x`, matching Node 26 — but Phase 1.2 deliberately pinned Node 24 LTS. Used `@types/node` `24.13.2` to match the runtime actually in use, not the newest major.

**Dropped mid-implementation, after verification:** initially added `eslint-config-next` 16.2.10 for Next.js-specific lint rules. Its own peer range (`eslint: ">=9.0.0"`) technically allows ESLint 10, but its transitive plugins (`eslint-plugin-import`, `eslint-plugin-jsx-a11y`, `eslint-plugin-react`) only declare support up to ESLint `^9`, and running it crashed with `TypeError: scopeManager.addGlobals is not a function` — a real internal-API break, not a benign warning. Rather than downgrade the ESLint 10.6.0 already verified in Phase 1.2, removed `eslint-config-next` (it wasn't required for this phase's actual goal) and kept the existing typescript-eslint-only config, which lints the new `.tsx` files cleanly. Revisit once Next.js's own ESLint config supports ESLint 10.

Two gaps only caught by actually running the tooling, not assumed:
1. Prettier had no `.prettierignore` and started formatting-checking `.next/` build output (148 files) the moment a real build existed. Added `apps/web/.prettierignore` (`.next/`, `node_modules/`, `dist/`).
2. Adding `"incremental": true` to `tsconfig.json` (required by Next.js) produces `tsconfig.tsbuildinfo`, which wasn't gitignored. Added `*.tsbuildinfo` to the root `.gitignore`.

`tsconfig.json` was also auto-updated by Next.js itself on first build (mandatory: `jsx` → `react-jsx`; suggested: `allowJs: true`, additional `include` entries) — expected, standard first-build behavior, not reverted.

Verified beyond the test suite: ran both `next build && next start` and `next dev` as real processes and confirmed `GET /` returns `200` with the actual rendered page (`<title>LifeOS</title>`, `<main>LifeOS</main>`) over real HTTP, not just via the component test.

Commit:
```
feat(web): bootstrap Next.js application with placeholder page

Add Next.js 16.2.10 + React 19.2.7 as the first runtime dependencies.
app/page.tsx renders a single placeholder page — no routing, styling,
or state yet (later phases). Add Vitest 4.1.10 + Testing Library for
component testing, with one smoke test. Drop eslint-config-next after
finding it crashes on ESLint 10 (transitive plugins cap at ESLint 9);
revisit once it catches up. Add .prettierignore and *.tsbuildinfo to
.gitignore, both gaps only surfaced by actually running the tooling.
```
