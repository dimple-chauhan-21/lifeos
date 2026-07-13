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

---

## Phase 1.7 - Git Hooks & CI

**Scope, clarified before implementing:** repo already has a real GitHub remote (`dimple-chauhan-21/lifeos`), which shaped how this phase was verified — "does the CI pipeline actually run" can only be proven on GitHub's own infrastructure, not locally, so verification included pushing a branch and opening a PR (both confirmed with you first).

Completed:
- **Git hooks**: Husky 9.1.7 + lint-staged 17.0.8. Pre-commit hook (`.husky/pre-commit`) runs `lint-staged` only — staged-file-scoped ESLint+Prettier for `apps/web/**/*.{ts,tsx}`, Ruff check+format for `apps/api/**/*.py`. No typecheck, no tests in the hook, per the explicit instruction to keep it fast; those run in CI only.
- **CI** (`.github/workflows/ci.yml`): 4 parallel jobs — `lint-web`, `lint-api`, `test-web` (Vitest), `test-api` (pytest). `test-api` brings up Postgres/Redis/MinIO via `docker compose -f infra/docker-compose.yml` rather than GitHub Actions' native `services:` syntax, which can't express the password-protected Redis or MinIO's required command args — this reuses the exact same, already-verified service definitions instead of maintaining a second parallel definition.
- **Dependabot** (`.github/dependabot.yml`): `uv` (native ecosystem, not `pip` — verified from Astral's own docs) for `apps/api`, plus `github-actions`. `apps/web` deliberately excluded — see Technical Debt below.
- **README Getting Started section** — none existed before this phase; added since "verify on a clean clone" needs documented steps to follow, and Phase 1's own acceptance criteria requires this.

Versions verified via GitHub's API directly (not marketplace listing pages): `actions/checkout@v7`, `actions/setup-node@v6`, `pnpm/action-setup@v6` (floating major-version tags, standard convention for these three), `astral-sh/setup-uv@v8.3.2` (pinned to the exact patch version, per Astral's own supply-chain-security recommendation for this specific action).

**New Technical Debt entry** (classified per the standing rule): Dependabot does not yet support pnpm 11's new multi-document `pnpm-lock.yaml` format — confirmed via open upstream issues (dependabot-core#14794, #14919), not just assumed. Classified as **Temporary Ecosystem Gap**. `apps/web` is excluded from Dependabot scanning until this is fixed upstream; pnpm was **not** downgraded to v10 to work around it, per the standing rule against regressing a deliberately-chosen dependency to satisfy a scanning tool.

Real gaps found only by actually running things end to end, not by reading docs/code in isolation:
1. **README's `corepack enable` step failed outright**: this machine's active Node is v25.9.0 (not the project's pinned v24), and Node dropped bundling `corepack` starting v25 — confirmed via Node's own TSC announcement. The natural fallback, `npm install -g corepack`, then collided with an existing Homebrew-installed `pnpm` binary (`EEXIST`). Neither is a one-off fluke specific to this machine — both are realistic scenarios for any contributor using a newer Node or a Homebrew-installed pnpm. Fixed by not mandating corepack at all: the README now lists corepack, Homebrew, and `npm install -g pnpm@11.10.0` as equally valid options.
2. **The pushed branch alone didn't trigger CI** — `ci.yml` only fires on `pull_request` or a push to `main`, so a feature-branch push produces zero workflow runs. Not a bug, just a real discovery about the pipeline's own configured behavior; resolved by opening a PR (with your approval) rather than by changing the trigger.
3. **A real, previously-undetected bug**: `lint-api`'s `ruff format --check` failed on GitHub Actions — `app/core/config.py`'s `@field_validator(...)` decorator had been manually line-wrapped in Phase 1.6 on the (wrong) assumption it exceeded the 100-char limit. `ruff check` and `mypy` were run after that change, but `ruff format --check` was not, so it slipped through two full phases undetected until this CI pipeline actually exercised it. Fixed (`uv run ruff format .`), and this is exactly the kind of regression the CI pipeline exists to catch.
4. Also caught during clean-clone verification: the previously-documented Phase 1.2 environment note (root-owned `~/.local` on this machine, needing `UV_PYTHON_INSTALL_DIR`/`UV_CACHE_DIR` redirected) still applies and would block `uv sync` on a truly fresh clone too — not a new finding, but reconfirmed; not fixed at the system level, consistent with that standing note.

Verified, end to end, not assumed:
- **Pre-commit hook, both ecosystems, both outcomes**: staged a `.ts` file with an unfixable ESLint violation (unused var) → commit correctly blocked, working tree cleanly reverted, confirmed via `git log`. Staged a `.py` file with an auto-fixable Ruff violation (unused import, bad spacing) → hook auto-fixed and the commit succeeded. All test files and commits removed afterward — nothing left in history.
- **Full clean-clone verification**: fresh `git clone` into an isolated temp directory, followed only the new README steps — `pnpm install` (confirmed the Husky hook auto-installs via the `prepare` script), `uv sync`, `docker compose up --build`, confirmed `/health` and `/` both return real `200`s over HTTP, then ran every lint/typecheck/test command from the README (`lint:web`, `typecheck:web`, `test:web`, `lint:api`, `typecheck:api`) plus the full pytest suite inside the live container — all passing, from a directory that had never seen any of this session's prior state.
- **CI actually running on GitHub's infrastructure, not just locally**: pushed `phase-1.7-git-hooks-ci`, confirmed (with your approval) that a push alone doesn't trigger it, had you open a PR, then polled the Actions API directly (`gh` wasn't available; the repo being public allowed unauthenticated polling) — first run genuinely failed on `lint-api` (the real bug above), fixed and pushed again, second run: all 4 jobs `success`.

Commit:
```
feat(ci): add git hooks and GitHub Actions CI pipeline

Add Husky + lint-staged (9.1.7 / 17.0.8) for a fast, staged-file-scoped
pre-commit hook: ESLint+Prettier for apps/web, Ruff check+format for
apps/api. No typecheck or tests in the hook — those run in CI only.

Add .github/workflows/ci.yml: 4 parallel jobs (lint-web, lint-api,
test-web, test-api). test-api brings up Postgres/Redis/MinIO via the
existing infra/docker-compose.yml rather than redeclaring them in
GitHub Actions' native services: syntax.

Add .github/dependabot.yml: uv (apps/api) and github-actions
ecosystems. apps/web excluded — Dependabot doesn't yet support pnpm
11's lockfile format (Temporary Ecosystem Gap, logged in
TECHNICAL_DEBT.md, not worked around by downgrading pnpm).

Add README Getting Started section.

Fix: apps/api/app/core/config.py had a ruff-format violation from
Phase 1.6 that ruff check/mypy didn't catch — only found once this
CI pipeline actually ran the formatter check for real.

Verified: pre-commit hook blocks/auto-fixes correctly on both
ecosystems; full clean-clone bring-up passes every check; pushed a
branch and confirmed the pipeline actually passes on GitHub Actions
(not just locally), including a first real failure caught and fixed.
```

---

## Foundation Cleanup (post-Phase 1.7)

Documentation-only pass following the Foundation Review — no application code, dependencies, or architecture changed. Every item traces to a specific finding from that review.

Completed:
- `PROJECT_STATUS.md`: was still showing "Current Phase: Phase 4 — Implementation Planning" with Phase 5 as three unchecked "Sprint 1/2/3" placeholders, seven approved sub-phases out of date. Updated to reflect Phase 4 (Roadmap) complete and Phase 5's Foundation sub-phases (1.1–1.7) complete, linking to `CHANGELOG.md` and `TECHNICAL_DEBT.md`; current phase now correctly points at Roadmap Phase 3 (Database Foundation) as next.
- Fixed a broken cross-reference: `docs/architecture/01_System_Architecture.md`'s footer pointed to `docs/architecture/02_Database_Schema.md`, a file that has never existed — the real file is `02_Database_Architecture.md`.
- `docs/architecture/01_System_Architecture.md` and `05_Frontend_Architecture.md` were both still marked `Status: Draft`, despite `PROJECT_STATUS.md` itself already asserting "Phase 3 – Engineering (Architecture) — Complete" and both documents having been relied on as binding, approved architecture across all seven Foundation sub-phases. Checked both documents' own Quality Review sections for any legitimate open blocker first — found none — then updated `Status: Draft` → `Approved` in both the header table and footer of each. No content changed, no version bump (a status correction, not a revision).
- `docs/implementation/00_Implementation_Roadmap.md`: same reasoning — `Status: Draft` → `Approved`, since it has been the actively-executed source of truth for seven completed, individually-approved sub-phases. Its footer's "Next Document: None planned — upon approval, this roadmap becomes the source of truth for beginning Phase 1 implementation" was written for a future event that has since happened; reworded to state Phase 1–2 are complete and Phase 3 is next, pointing at `CHANGELOG.md`/`PROJECT_STATUS.md` for detail.
- `05_Frontend_Architecture.md`'s footer said "Next Document: To be determined" — filled in with `docs/implementation/00_Implementation_Roadmap.md`, now that it's known.
- `README.md` and this `CHANGELOG.md` were both re-verified against the current repository (scripts, ports, prerequisite versions, phase order) and found already accurate — no changes needed to either.
- Added five entries to `TECHNICAL_DEBT.md`, all classified **Our Design Decision**, for the Foundation Review's remaining findings that weren't yet tracked anywhere: Docker images running as root (+ `web`'s missing healthcheck), no CORS middleware yet, configuration not yet DI-injected, `asyncpg`/`redis`/`minio` shipping as runtime dependencies ahead of any runtime caller, and secrets not yet auto-generated on first run. None of these were fixed — per this cleanup's own scope, they're future-phase work, now just no longer undocumented future-phase work.

Explicitly not touched, per this cleanup's own scope: no Docker `USER` directives added, no CORS middleware written, no DI wiring changed, no dependencies added or removed, no application code modified.

Commit:
```
docs: Foundation cleanup — sync status docs with completed Phase 1

Update PROJECT_STATUS.md to reflect Phase 1 (Foundation, sub-phases
1.1-1.7) and Phase 4 (Roadmap) as complete, current phase now Phase 3
(Database Foundation). Fix a broken cross-reference in
01_System_Architecture.md (pointed at a file that never existed:
02_Database_Schema.md instead of 02_Database_Architecture.md).
Correct stale Status: Draft on 01_System_Architecture.md,
05_Frontend_Architecture.md, and 00_Implementation_Roadmap.md to
Approved, matching how they've actually been relied on across all
seven Foundation sub-phases (verified no open blocker in either
document's own Quality Review first). Fill in
05_Frontend_Architecture.md's "Next Document: To be determined".

Add 5 TECHNICAL_DEBT.md entries (Our Design Decision) for previously
undocumented, deliberately deferred items from the Foundation Review:
Docker root user, missing CORS, config not yet DI-injected, early
asyncpg/redis/minio dependencies, secrets not yet auto-generated.

No application code, dependencies, or architecture changed.
```

---

## Phase 3.1 - SQLAlchemy Engine & Session Foundation

Completed:
- `apps/api/app/db/base.py`: the declarative `Base`, nothing else
- `apps/api/app/db/session.py`: async engine + session factory only, reading `settings.database_url` and adapting its scheme (`postgresql://` → `postgresql+asyncpg://`) internally — the driver stays an infrastructure detail, never something written into `.env`
- Added `sqlalchemy[asyncio]==2.0.51`

Verified beyond static checks: a real `SELECT 1` through `AsyncSessionLocal` against live Postgres in Docker.

One real bug, caught only by running it: `sqlalchemy==2.0.51` alone doesn't install `greenlet`, which SQLAlchemy's async mode requires — confirmed via SQLAlchemy's own docs, which explicitly name this exact scenario (platforms without prebuilt `greenlet` wheels, e.g. Apple Silicon) and the fix (the `[asyncio]` extra). Not a new dependency — a correction to the extras spec on the one already approved.

A follow-up review (requested before starting 3.2) re-audited both files line by line against the same architecture docs plus a byte-level check of `db/__init__.py` against the project's other `__init__.py` files, a repo-wide grep for `postgresql+asyncpg` (found in exactly one place), and a check that `Base.metadata.tables` is genuinely empty. No changes were required — 3.1 was already correct as written.

Commit:
```
feat(api): add SQLAlchemy async engine and session foundation

Add app/db/base.py (declarative Base) and app/db/session.py (async
engine + session factory) — infrastructure only, no models yet.
Pin sqlalchemy[asyncio]==2.0.51 (the [asyncio] extra is required for
greenlet on platforms without prebuilt wheels, e.g. Apple Silicon —
caught by actually connecting, not assumed from the plain package
name). DATABASE_URL stays a generic postgresql:// URL; the asyncpg
driver scheme is an internal detail of session.py alone.

Verified: real SELECT 1 against live Postgres in Docker, full existing
test suite (4/4), ruff/ruff format/mypy all clean.
```

---

## Phase 3.2 - Alembic Wiring

Completed:
- Added `alembic==1.18.5` (verified current stable on PyPI, not a pre-release)
- Scaffolded via Alembic's own official **async template** (`alembic init -t async alembic`) rather than hand-converting the sync template — `apps/api/alembic.ini`, `apps/api/alembic/env.py`, `apps/api/alembic/script.py.mako`, `apps/api/alembic/README` (Alembic's own stock file, not authored here), `apps/api/alembic/versions/` (empty)
- `env.py` customized to reuse `target_metadata = Base.metadata` (imported from `app.db.base`) so autogenerate sees future models without a duplicate declaration
- `alembic.ini`'s stock `sqlalchemy.url = driver://user:pass@localhost/dbname` placeholder removed, replaced with a comment explaining the URL intentionally isn't set there

No migrations, tables, models, repositories, services, routers, DTOs, schemas, or seed scripts were created — infrastructure only, per this sub-phase's explicit scope.

**Corrected after initial implementation** (requested review before starting 3.3): the first version of `env.py` reused the application's live `engine` object from `app.db.session` directly for migrations. Re-checked against Alembic's own official async cookbook recipe, which builds an **independent** engine with `poolclass=pool.NullPool` — confirmed the "share a connection" alternative recipe is explicitly for programmatic/testing scenarios, not standard CLI usage, so reusing the app's live engine was a real deviation from the documented default, not a stylistic choice. Fixed: `run_async_migrations` now builds its own dedicated engine with `NullPool` (a one-shot CLI process has no use for the app's connection pool and shouldn't hold pooled connections open after it exits) — while still deriving the URL from the app's already-computed `engine.url` as a plain string, so `DATABASE_URL` keeps exactly one source of truth (`Settings`) without duplicating the `postgresql://` → `postgresql+asyncpg://` conversion logic a second time.

That fix surfaced a second real bug, caught only by actually reconnecting: `str(engine.url)` masks the password with `***` by default — a SQLAlchemy safety default against accidental credential leakage in logs, correct for display but silently unusable for an actual connection. First re-verification attempt failed with `asyncpg.exceptions.InvalidPasswordError`. Fixed by using `engine.url.render_as_string(hide_password=False)` instead.

Verified for real, against live Postgres in Docker, both before and after the correction above:
- `alembic current` / `alembic history` — both empty, correctly, since no migration files exist yet
- `alembic revision --autogenerate` — generated a genuinely empty (`pass`/`pass`) migration, correctly detecting zero difference between `Base.metadata` (empty) and the live database (empty); this file was a throwaway proof that the wiring works end-to-end and was deleted immediately after, per this sub-phase's scope
- Used that throwaway migration to prove `alembic upgrade head` and `alembic downgrade base` both work — applied cleanly, tracked correctly, reverted cleanly
- **A real, worth-documenting finding**: after `alembic upgrade head` — even with zero real migrations — Alembic creates its own `alembic_version` tracking table as a side effect of running `upgrade` at all (there's simply nothing recorded in it yet). This is expected, standard Alembic behavior, not a bug, and it's exactly what happens on a genuine fresh install too
- Re-ran with zero migration files present (after removing the throwaway one): `alembic current`/`history`/`upgrade head`/`downgrade base` all correctly no-op
- One real lint finding: `ruff check` flagged `env.py`'s import order (`I001`) on first run — auto-fixed, re-verified clean
- Ruff, Ruff format, mypy (10 source files), and the full existing test suite (4/4) all clean, no regressions, both before and after the correction

Commit:
```
feat(api): wire Alembic for async migrations

Add alembic==1.18.5 (verified current stable), scaffolded from
Alembic's own official async template. env.py reuses Base.metadata
for target_metadata, but builds its own independent engine with
NullPool for migrations (Alembic's own documented default — a
one-shot CLI process has no use for the app's connection pool),
deriving the URL from the app's already-computed engine.url as a
plain string so DATABASE_URL keeps exactly one source of truth
(Settings) without duplicating the asyncpg scheme conversion.

Two real bugs, both caught only by actually connecting: (1) an
earlier version reused the app's live engine directly, a real
deviation from Alembic's documented async recipe, corrected after
re-checking official docs; (2) str(engine.url) masks the password
with "***" by default, which silently broke the connection until
switched to render_as_string(hide_password=False).

Infrastructure only: no migrations, models, or tables. Verified
end-to-end against live Postgres in Docker — autogenerate, upgrade,
and downgrade all confirmed working via a throwaway no-op migration,
deleted after proving the wiring (a fresh install correctly has an
empty migration history until Phase 3.3's first real migration).
```

---

## Phase 3.3 - Users Table & First Migration

Completed:
- `apps/api/app/platform/users/models.py`: the minimal `User` model — `id` (UUID, DB-generated via `gen_random_uuid()`), `email`, `created_at` (DB-generated via `now()`). Pure ORM mapping only — no methods, no validation, no repository/service/router/schemas, per this sub-phase's explicit scope
- `apps/api/alembic/versions/0001_create_users.py`: creates `users` **and** seeds the mandatory V1 bootstrap user (`admin@lifeos.local`) in the same migration, so `alembic upgrade head` alone fully initializes a fresh install — no separate seed command, per your explicit refinement

**A real bug, caught immediately by hand-reviewing the autogenerated output, not by trusting it**: the first `alembic revision --autogenerate` produced a completely empty migration (`pass`/`pass`) — it failed to detect the new `User` model at all. Root cause: `env.py` imports `Base` for `target_metadata`, but nothing had ever imported the `User` model module itself, so it was never registered on `Base.metadata` by the time autogenerate ran its comparison (confirmed as a well-documented, expected Alembic requirement, not a defect in 3.2's design — this simply couldn't have surfaced before a real model existed). Initially fixed with a direct `from app.platform.users.models import User` in `env.py`.

**Revisited on request**: checked both Alembic's and SQLAlchemy's official docs directly for a prescribed pattern (individual per-model imports in `env.py` vs. a central aggregator) — neither document takes a position either way. Given the failure mode just hit is silent (a missing import produces an *empty* migration, not an error) and will only recur more as 28+ Entity Types get built, moved the import responsibility to `app/platform/__init__.py` (already existed as an empty marker, no new file) — it now imports every Platform-layer model, and `env.py` imports `app.platform` once instead of a growing, easy-to-forget per-model list. `app/domains/__init__.py` will need the same treatment once the first Domain package exists. Re-verified end-to-end: `Base.metadata.tables` correctly shows `users` from `import app.platform` alone, and a fresh `--autogenerate` against the already-migrated database correctly detects zero diff (proving the registration path works, not just that it doesn't error).

**Chose database-side generation for both `id` and `created_at`** (`server_default`, not Python-side SQLAlchemy defaults), verified `gen_random_uuid()` is core PostgreSQL (v13+, no extension) directly against the official docs. This matters concretely: the seed migration inserts via a raw `bulk_insert`, which bypasses the ORM's Python-side defaults entirely — database-side generation is what makes the seed insert work at all without the migration needing to supply its own UUID.

**Seed insert uses a self-contained `sa.table()`/`sa.column()` construct**, not the live `User` model import — confirmed as Alembic's own documented recommendation specifically so historical migrations stay stable if the model changes later (e.g., Phase 4 adding `password_hash`). This is also why `id`/`created_at` aren't specified in the insert — they're left to the column's own `server_default`.

**Migration filename**: generated with `--rev-id 0001` so Alembic's own tooling produces the literal `0001_create_users.py` filename, rather than hand-renaming a hash-named file after the fact.

**Fixed `alembic/script.py.mako`** (the migration template itself, a Phase 3.2 file): the stock async template generates `typing.Union`/`typing.Sequence` imports, which fail this project's own Ruff rules (`UP007`, `UP035`, `I001`). Rather than hand-fixing this same lint failure on every future migration, updated the template once to generate modern `X | Y` / `collections.abc.Sequence` syntax from the start — verified by confirming the fixed migration file's exact post-`ruff --fix` shape, then propagating that into the template.

Hand-reviewed the final migration against every point requested: column types, nullable flags, defaults, UUID generation mechanism, and downgrade correctness (a plain `drop_table` fully reverses both the schema and the seeded row, since dropping the table removes its data too — no separate `DELETE` needed).

Verified for real, against live Postgres in Docker:
- `alembic upgrade head` — `users` table created, primary key on `id` confirmed via `\d users`, `id` is genuinely `uuid` type defaulting to `gen_random_uuid()`, `created_at` is `timestamptz` defaulting to `now()`, exactly one seeded row present with a real generated UUID
- `alembic downgrade base` — `users` table genuinely gone (`\dt` confirms only `alembic_version` remains)
- `alembic upgrade head` again — table and seed row both correctly recreated (a fresh, different UUID each time, as expected from `gen_random_uuid()`)
- Inserted a real row through `AsyncSessionLocal`/the `User` ORM model (not raw SQL) — insert, `refresh()` (confirming server-side defaults populate back into the Python object), and a `select()` query-back all correct; both the seeded row and the ORM-inserted row coexisted correctly
- `alembic downgrade base` → `alembic upgrade head` again, **after** the manual ORM insert — confirmed a true clean reset: exactly one row (the reseeded bootstrap user) afterward, the manually-inserted test row correctly did not persist
- Ruff, Ruff format, mypy (14 source files), and the full existing test suite (4/4) all clean, no regressions

**New standing rule, adopted starting this phase**: every migration is immutable once committed — a schema change is always a new migration, never an edit to an existing committed one.

Commit:
```
feat(api): add users table with first migration

Add app/platform/users/models.py: minimal User model (id, email,
created_at only), pure ORM mapping, no business logic. Add
alembic/versions/0001_create_users.py: creates users and seeds the
mandatory V1 bootstrap user in the same migration, so a fresh install
is fully initialized after `alembic upgrade head` alone.

id and created_at use database-side defaults (gen_random_uuid(),
now()) rather than Python-side ones, verified gen_random_uuid() is
core Postgres 13+ (no extension) — required since the seed insert
bypasses the ORM's own defaults. The seed insert itself uses a
self-contained table()/column() construct rather than importing the
live model, per Alembic's own documented recommendation for keeping
historical migrations stable.

Fix: env.py needed a model import for autogenerate to see User at
all — the first autogenerate attempt silently produced an empty
migration, caught by hand-reviewing rather than trusting it. Checked
official Alembic/SQLAlchemy docs for a prescribed import pattern
(neither takes a position); centralized model registration in
app/platform/__init__.py rather than a growing per-model list in
env.py, since the failure mode is silent and will only recur more as
more Platform/Domain models are added.
Fix: script.py.mako updated to generate modern typing syntax (X | Y,
collections.abc.Sequence) so future migrations pass this project's
Ruff config without per-file patching.

Verified end-to-end against live Postgres in Docker: upgrade/downgrade
cycle (including after a manual ORM insert) all correct; table, PK,
UUID generation, and seed data all confirmed by direct inspection.

Adopted as a standing rule from this phase onward: migrations are
immutable once committed — a schema change is always a new migration.
```
