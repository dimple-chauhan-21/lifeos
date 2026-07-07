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

## Current Status

🚧 Implementation in progress — see [`docs/implementation/00_Implementation_Roadmap.md`](docs/implementation/00_Implementation_Roadmap.md) and [`docs/implementation/CHANGELOG.md`](docs/implementation/CHANGELOG.md) for build progress.
