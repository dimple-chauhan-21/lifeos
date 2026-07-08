# Build context is the repository root (this is a pnpm workspace).
FROM node:24-slim

RUN corepack enable

WORKDIR /workspace

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/web/package.json apps/web/package.json

RUN pnpm install --frozen-lockfile

COPY . .

WORKDIR /workspace/apps/web

EXPOSE 3000

CMD ["pnpm", "dev"]
