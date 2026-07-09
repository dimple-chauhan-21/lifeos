# LifeOS

LifeOS is a modern, self-hosted Personal Life Operating System.

The goal of LifeOS is to provide a single platform to manage every important aspect of personal life, including:

- Vehicles
- Properties
- Documents
- Health
- Finance
- Goals
- Tasks
- Travel
- Digital Assets
- Relationships

---

## Technology Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui

### Backend

- FastAPI
- Python
- SQLAlchemy
- Alembic

### Database

- PostgreSQL

### Infrastructure

- Docker / Docker Compose
- Redis
- MinIO

---

## Repository Structure

```
apps/
  web/        Next.js frontend
  api/        FastAPI backend
infra/        Docker Compose, Nginx, deployment config
docs/         Product, design, and architecture documentation
design/       UX/UI design workspace (sprints, decisions, assets)
```

Full architecture: [`docs/architecture/`](docs/architecture/). Product and design documentation: [`docs/product/`](docs/product/), [`docs/design/`](docs/design/). Project status: [`PROJECT_STATUS.md`](PROJECT_STATUS.md).

---

## Getting Started

**Prerequisites:**

- [Node.js 24](https://nodejs.org/) (pinned in `.nvmrc`)
- [pnpm 11.10.0](https://pnpm.io/) (pinned in `package.json`'s `packageManager` field — run via `corepack enable` to get the exact version automatically)
- [Python 3.13](https://www.python.org/) via [uv](https://docs.astral.sh/uv/) (uv manages the Python install itself — no separate Python install needed)
- [Docker](https://www.docker.com/) with Docker Compose

**Setup:**

```bash
git clone https://github.com/dimple-chauhan-21/lifeos.git
cd lifeos

# Install JS/TS dependencies (also installs the pre-commit git hook)
corepack enable
pnpm install

# Install Python dependencies
cd apps/api && uv sync && cd ../..

# Configure environment variables
cp infra/.env.example infra/.env
# edit infra/.env if you want non-default local credentials

# Start the full stack (Postgres, Redis, MinIO, API, web)
cd infra && docker compose up --build
```

Once running:

- Frontend: [http://localhost:3000](http://localhost:3000)
- API health check: [http://localhost:8000/health](http://localhost:8000/health)
- MinIO console: [http://localhost:9001](http://localhost:9001)

**Running checks locally** (outside Docker):

```bash
pnpm run lint:web && pnpm run typecheck:web && pnpm run test:web
pnpm run lint:api && pnpm run typecheck:api
```

The backend's integration tests (`pnpm run test:api`) require the Docker services above to be running first.

---

## Current Status

🚧 Implementation in progress — see [`docs/implementation/00_Implementation_Roadmap.md`](docs/implementation/00_Implementation_Roadmap.md) and [`docs/implementation/CHANGELOG.md`](docs/implementation/CHANGELOG.md) for build progress.
