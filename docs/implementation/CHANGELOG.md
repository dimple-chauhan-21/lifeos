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

---

## Phase 1.5 - Docker & Docker Compose

Completed:
- `infra/docker-compose.yml`: 5 services — `postgres`, `redis`, `minio`, `api`, `web` — with healthcheck-based `depends_on` throughout (no sleep delays). `worker`/`beat` deliberately deferred: no Celery code exists anywhere yet, and adding the services now would mean adding a stub task module just to give them something to run, violating the lazy-dependency principle. Revisit when a real background job is actually built.
- `infra/.env.example` documenting every required variable
- `apps/api/Dockerfile` + `.dockerignore` (uv-based, dev-oriented, live-reload via bind mount with `UV_PROJECT_ENVIRONMENT` kept outside the mounted path so installed deps aren't shadowed)
- `apps/web/Dockerfile` + root `.dockerignore` (pnpm-based; build context is the repo root since `apps/web` is part of the pnpm workspace, not a standalone package)
- `apps/api/app/core/config.py`: typed `Settings` (pydantic-settings 2.14.2) covering `database_url`, `redis_url`, and MinIO endpoint/credentials/bucket — fails fast if any is missing. Session-secret/cookie settings (also mentioned in `04_Backend_Architecture.md` §21) deliberately excluded — no consumer exists until the Auth phase.
- `apps/api/tests/test_connectivity.py`: real smoke test connecting to actual Postgres (`asyncpg` 0.31.0), Redis (`redis` 8.0.1), and MinIO (`minio` 7.2.20) — no mocks, consistent with the project's own stated integration-test philosophy (`00_Engineering_Overview.md` §17)

Versions verified against official/primary sources, not assumed from the architecture doc's "16+"/generic naming:
- PostgreSQL: `postgres:18` (Docker Hub's actual latest stable)
- Redis: `redis:8.8` — verified its licensing history first: reverted to a tri-license (RSALv2/SSPLv1/**AGPLv3**) as of Redis 8.0, AGPLv3 being OSI-approved open source again. Safe to use as the actively-maintained current stable.
- MinIO: **found the `minio/minio` GitHub repo now says "THIS REPOSITORY IS NO LONGER MAINTAINED"** — the vendor pivoted to a commercial "AIStor" product. Flagged to you directly rather than silently picking a replacement; you chose to pin the last published community tag (`RELEASE.2025-09-07T16-13-09Z`). Logged as technical debt with classification **Upstream Framework Limitation** — see `TECHNICAL_DEBT.md`.

Two scope judgment calls, confirmed with you before implementing:
1. `worker`/`beat` deferred (see above).
2. `apps/api/app/core/config.py` included in this same phase rather than split out, since it's needed to actually satisfy this phase's own smoke-test requirement.

Two real bugs caught only by actually running things, not by reading docs/config in advance:
1. Postgres exited on first start with `postgres-1 | Error: in 18+, these Docker images are configured to store database data in a format which is compatible with "pg_ctlcluster"...`. PostgreSQL 18 changed its expected volume mount point from `/var/lib/postgresql/data` to `/var/lib/postgresql`. References: [official `postgres` image docs, Docker Hub](https://hub.docker.com/_/postgres) ("The defined `VOLUME` was changed in 18 and above to `/var/lib/postgresql`. Mounts and volumes should be targeted at the updated location.") and [docker-library/postgres#1259](https://github.com/docker-library/postgres/pull/1259), the PR the container's own error message pointed to. Fixed and re-verified clean.
2. The root `.gitignore`'s `.env.*` pattern was also silently matching `infra/.env.example` — the one `.env*` file that's *supposed* to be committed as a template. Added `!.env.example` to un-ignore it; confirmed via `git check-ignore` before and after.

Verified beyond `docker compose up` succeeding: `postgres`, `redis`, `minio`, and `api` all report `healthy` via their own healthchecks; `GET /health` (API), `GET /` (web, rendering the real page), and MinIO's console all returned `200` over real HTTP from the host; the connectivity smoke test plus the full existing test suite (4 tests) both passed running *inside* the live `api` container against the real `postgres`/`redis`/`minio` containers, not mocks. Docker itself wasn't installed on this machine at the start of this phase — paused and waited for it to be installed before running any of the above, rather than claiming success without testing.

Commit:
```
feat(infra): add Docker Compose stack (postgres, redis, minio, api, web)

Add infra/docker-compose.yml with healthcheck-gated startup ordering
and infra/.env.example. Add dev Dockerfiles for apps/api (uv-based)
and apps/web (pnpm-based, root build context). Add apps/api/app/core/
config.py: typed, fail-fast Settings for DB/Redis/MinIO. Add a real
connectivity smoke test (asyncpg, redis, minio clients — no mocks).

Pin postgres:18, redis:8.8 (verified AGPLv3 post-license-reversal),
and minio RELEASE.2025-09-07T16-13-09Z (last community release before
the minio/minio repo was marked unmaintained in favor of the vendor's
commercial AIStor product — logged in TECHNICAL_DEBT.md). Defer
worker/beat services until real Celery task code exists.

Fix: Postgres 18 moved its expected volume mount point from
/var/lib/postgresql/data to /var/lib/postgresql — caught only by
actually running docker compose up, not from reading docs in advance.
Fix: root .gitignore's .env.* pattern was silently ignoring
infra/.env.example too; added a !.env.example negation.
```

---

## Phase 1.6 - Environment & Configuration

**Scope, clarified before implementing:** Phase 1.5 already built `apps/api/app/core/config.py` (typed `Settings`) and proved it *could* connect via an isolated smoke test — but `app/main.py` never actually called it. The FastAPI app itself didn't consume `Settings` at all, so the architecture's "fails fast on missing configuration" requirement (`04_Backend_Architecture.md` §21) wasn't actually true for the running application, only for a test that happened to import `get_settings()` directly. Confirmed with you that closing this specific gap — not something broader like frontend env vars or auto-generated secrets — was this phase's scope.

Completed:
- Wired `get_settings()` into a FastAPI `lifespan` handler (`app/main.py`) — configuration is now loaded and validated at application startup, not lazily on first use.
- Added real validation to `Settings` beyond mere presence (`app/core/config.py`): `database_url` must parse as a `postgresql://` URL, `redis_url` must parse as `redis://`, and the MinIO fields must not be blank. A required variable that's *set but empty or malformed* now fails just as loudly as one that's missing entirely.

Verified, not assumed:
- **A bare `TestClient(app)` (as `tests/test_health.py` already used, not as a context manager) does not trigger FastAPI's lifespan at all** — confirmed by running that test with every DB/Redis/MinIO env var unset and watching it still pass. This means the existing test's green status was never actually proof the app was configured correctly; the lifespan only fires for a real ASGI server (uvicorn) or a `with TestClient(app) as client:` context-manager usage. Documented here since it's a non-obvious gap between "test passes" and "app actually validates config."
- Ran `uv run uvicorn app.main:app` locally with **zero** environment variables set: real crash — `pydantic_core.ValidationError: 6 validation errors for Settings` naming every missing field, `ERROR: Application startup failed. Exiting.`, connection refused on the port.
- Ran the same with a syntactically-invalid `DATABASE_URL` (present but not a real Postgres URL): rejected with `Value error, database_url must be a postgresql:// URL` — proving "invalid," not just "missing," is caught.
- **Inside real Docker** (per this phase's explicit instruction, not just locally): brought the full stack up clean first (all healthy, `/health` returns `200`), then ran `docker compose run --rm -e DATABASE_URL="" api` — the container's own logs showed the identical `ValidationError` and `Application startup failed. Exiting.`, and its healthcheck immediately reported `unhealthy`. One nuance worth recording: because the dev Dockerfile runs `uvicorn --reload`, the outer reloader-supervisor process doesn't itself exit non-zero on a startup crash (it stays "Up (unhealthy)" rather than "Exited") — the operator-visible signal in this dev setup is the healthcheck status and crash traceback in logs, not the container's exit code. This is expected `--reload` behavior, not a bug; noted so it isn't surprising later.
- Ran the full existing test suite (4 tests) inside the live, correctly-configured container afterward — all still passing, no regressions.
- No temporary verification code left behind: the broken-config checks above were ad hoc CLI invocations and a disposable `docker compose run` container, never committed to the repo.

No new ecosystem incompatibility or architectural concern surfaced this phase requiring a `TECHNICAL_DEBT.md` entry.

Commit:
```
feat(api): fail fast on missing or invalid configuration at startup

Wire the existing Settings class into a FastAPI lifespan handler so
app/main.py actually validates configuration at startup, instead of
only being reachable through an isolated test. Add real validation
beyond presence checks: database_url/redis_url must parse as
postgresql:// and redis:// URLs; MinIO fields must not be blank.

Verified with zero and with invalid env vars, both locally (uvicorn)
and inside a real Docker container (docker compose run --rm -e
DATABASE_URL="") — confirmed an actual startup crash naming the
problem, not just a passing isolated test.
```
