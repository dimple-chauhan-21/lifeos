# LifeOS — Technical Debt / Future Improvements Log

A running log of known gaps, deferred work, and things deliberately left unresolved during implementation — each with the reason and the condition under which it should be revisited. Distinct from `docs/implementation/CHANGELOG.md` (which records what was done, phase by phase) and from `PROJECT_STATUS.md` (milestone acceptance only).

---

## apps/web — `eslint-config-next` not adopted (ESLint 10 incompatibility)

**Logged:** Phase 1.4 - Frontend Bootstrap (2026-07-08)

**Classification:** Temporary Ecosystem Gap — not a bug in this project's code, not an inherent architectural limitation of Next.js itself, and not a choice we made. `eslint-config-next`'s transitive plugins simply haven't published ESLint 10 support yet; expected to close as the plugin maintainers catch up.

**Issue:** `eslint-config-next` 16.2.10 is not usable with ESLint 10.6.0 (the version this project runs). Its own peer range (`eslint: ">=9.0.0"`) technically allows it, but its transitive plugins (`eslint-plugin-import`, `eslint-plugin-jsx-a11y`, `eslint-plugin-react`) only declare support up to ESLint `^9`. Running it crashes with `TypeError: scopeManager.addGlobals is not a function` — a real internal ESLint API break, not a benign peer-dependency warning.

**Current state:** `apps/web/eslint.config.js` uses `@eslint/js` + `typescript-eslint` only. This lints TypeScript/JSX correctly but does not include Next.js-specific rules (e.g., `next/image` usage warnings, Next-aware React Hooks rules, routing conventions).

**Resolution condition:** Adopt `eslint-config-next` once the Next.js ecosystem officially supports ESLint 10 (i.e., its transitive plugins declare and are verified to work with ESLint 10, not just an open-ended peer range on the top-level package).

**Constraint:** Do not downgrade ESLint 10.6.0 to work around this. The ESLint version was deliberately chosen and verified in Phase 1.2; compatibility should be resolved by the Next.js/ESLint ecosystem catching up, not by this project regressing its tooling.

---

## infra — MinIO pinned to last community release (upstream repo unmaintained)

**Logged:** Phase 1.5 - Docker & Docker Compose (2026-07-08)

**Classification:** Upstream Framework Limitation — not a bug in this project, not expected to resolve on its own (it's a permanent business/product shift by the vendor, not a version-lag gap), and not itself a choice we made — the choice we made (pinning the last release) was our *response* to this limitation.

**Issue:** `docs/architecture/00_Engineering_Overview.md` (Section 1/9) specifies self-hosted MinIO as the fixed-stack S3-compatible object store. MinIO Inc. has moved its self-hosted product to a commercial-first offering ("AIStor", with a Free single-node tier and a paid Enterprise tier).

**Verification, across both official and secondary sources (checked on request, not GitHub alone):**
- **Official — Docker Hub** (`minio/minio`, MinIO's own publishing channel): no new tags published after `RELEASE.2025-09-07T16-13-09Z`, confirmed directly by paging the repository's own tag API (`hub.docker.com/v2/repositories/minio/minio/tags`).
- **Official — [docs.min.io](https://docs.min.io)**: the documentation site is now structured around AIStor as the primary product, including a dedicated official guide, ["Upgrade from open-source MinIO"](https://docs.min.io/enterprise/aistor-object-store/upgrade-aistor-server/community-edition/) — its existence signals an intended migration path away from the open-source edition, though neither this page nor `docs.min.io/community/minio-object-store/` uses the words "deprecated" or "end-of-life" explicitly.
- **Official — GitHub** (`github.com/minio/minio`): repository banner states **"THIS REPOSITORY IS NO LONGER MAINTAINED."**
- **Secondary (trade press, not MinIO's own words)** fills in the explicit timeline the official channels don't spell out directly: community edition entered "maintenance mode" (no new features, security fixes only "as appropriate") on 2025-12-03, and the GitHub repo was formally archived on 2026-04-25 ([LinuxIac](https://linuxiac.com/minio-ends-active-development/), [It's FOSS](https://itsfoss.com/news/minio-moves-away-from-open-source/)).

**Current state:** `infra/docker-compose.yml` pins `minio/minio:RELEASE.2025-09-07T16-13-09Z` — the last tag the project published (Sept 2025) before archival. Fully functional, AGPLv3-licensed, verified working end-to-end in this phase (bucket listing, connectivity). It will not receive further security or bug fixes from upstream.

**Resolution condition:** Revisit if either (a) a real security issue is found in this pinned MinIO release with no patched community version available, or (b) AIStor's Free tier's terms are verified in detail and found suitable (its account/registration requirements and exact feature parity with legacy MinIO were not fully verifiable from public docs at the time of this decision). Until then, the pinned release is the deliberate choice — do not silently swap to AIStor or a different object store (e.g., SeaweedFS, Garage) without flagging it, since that would revisit an architecture decision, not just a version bump.

---

## .github/dependabot.yml — apps/web excluded from dependency scanning (pnpm 11 lockfile format)

**Logged:** Phase 1.7 - Git Hooks & CI (2026-07-08)

**Classification:** Temporary Ecosystem Gap — Dependabot's parser hasn't caught up to pnpm 11's new lockfile format yet; actively tracked upstream with open issues, not a permanent limitation, and not something in our own control to fix.

**Issue:** pnpm 11 changed `pnpm-lock.yaml` to a multi-document YAML file (an "env lockfile" document plus the regular project lockfile). Dependabot's `npm`-ecosystem parser (the value used for pnpm per [GitHub's own ecosystem support docs](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-repositories), which lists supported pnpm versions as only v7–v10) does not yet handle this format — confirmed via open upstream issues [dependabot-core#14794](https://github.com/dependabot/dependabot-core/issues/14794) and [#14919](https://github.com/dependabot/dependabot-core/issues/14919) ("multi-document pnpm-lock.yaml reported as dependency_file_not_parseable").

**Current state:** `.github/dependabot.yml` configures `uv` (native ecosystem, `apps/api`) and `github-actions` scanning, but deliberately excludes `apps/web`'s npm/pnpm dependencies. Per the standing rule against regressing a deliberately-chosen dependency version to satisfy a scanning tool, pnpm was **not** downgraded to v10 to work around this.

**Resolution condition:** Add an `npm`-ecosystem entry for `apps/web` once Dependabot ships support for pnpm 11's lockfile format (tracked in the linked upstream issues) — check periodically, or when either issue closes.
