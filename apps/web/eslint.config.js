import js from "@eslint/js";
import tseslint from "typescript-eslint";

// eslint-config-next is not yet compatible with ESLint 10 (its transitive
// plugins only declare peer support up to ESLint 9, and fail at runtime
// with ESLint 10 — see docs/implementation/CHANGELOG.md, Phase 1.4).
// Revisit once Next.js's own ESLint config catches up.
export default tseslint.config(
  { ignores: ["dist/**", ".next/**", "node_modules/**"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
);
