import path from "node:path";

const apiDir = path.join(process.cwd(), "apps/api");

function toApiRelative(files) {
  return files.map((file) => path.relative(apiDir, file));
}

export default {
  "apps/web/**/*.{ts,tsx}": (files) => [
    `pnpm --filter web exec eslint --fix ${files.join(" ")}`,
    `pnpm --filter web exec prettier --write ${files.join(" ")}`,
  ],
  "apps/api/**/*.py": (files) => {
    const relative = toApiRelative(files).join(" ");
    return [
      `sh -c 'cd apps/api && uv run ruff check --fix ${relative}'`,
      `sh -c 'cd apps/api && uv run ruff format ${relative}'`,
    ];
  },
};
