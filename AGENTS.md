# Repository Guidelines

## Project Structure & Module Organization
The workspace root only holds high-level docs (`CLAUDE.md`, `skeleton-ui.md`, `prompt.json`) plus the `monitor_front/` Svelte application. Inside `monitor_front/src`, `main.ts` wires Vite to `App.svelte`, `lib/` holds reusable widgets (e.g., `Counter.svelte`), and `assets/` stores component-local media. Static files that must be served verbatim (favicons, SEO assets) belong in `monitor_front/public/`. Keep environment-specific settings in the various `tsconfig*.json` and `vite.config.ts` files; update them instead of scattering inline overrides.

## Build, Test, and Development Commands
Install dependencies with `bun install` (preferred because `bun.lock` is tracked) or `npm install` if Bun is unavailable. Run `npm run dev` (or `bun run dev`) from `monitor_front/` for a hot-reload preview. `npm run build` emits the production bundle to `monitor_front/dist/`. Use `npm run preview` to smoke-test that bundle with Vite’s static server. `npm run check` runs `svelte-check` followed by `tsc` to ensure templates and tooling configs stay type-safe.

## Coding Style & Naming Conventions
Follow the default Svelte + TypeScript style: two-space indentation, single quotes inside scripts, and PascalCase component files (`MyWidget.svelte`). State shared logic in `src/lib` and import using relative paths; keep collocated styles within each `.svelte` block unless a style is reused broadly, in which case promote it to `app.css`. Avoid implicit `any`; prefer typed `export let` props and Svelte stores for shared state. Run `npm run check` before submitting to catch formatting or typing drift.

## Testing Guidelines
There is no automated test suite yet, so rely on `npm run check` plus manual verification in `npm run preview`. When adding Vitest or Playwright, co-locate tests under `src` using the `.test.ts` suffix and aim for meaningful DOM assertions (accessibility roles, text content) rather than brittle selectors. Document any new test commands in `package.json` scripts and ensure CI can run them headlessly.

## Commit & Pull Request Guidelines
Existing history uses short, imperative titles (see `Initial commit`), so keep subject lines under ~60 characters and describe the intent, not the mechanics. Reference issues using `Fixes #id` in the body when relevant. Pull requests must summarize user-facing changes, list notable screenshots or clips for UI updates, and mention any configuration migrations (e.g., Vite, tsconfig). Include reproduction steps for bug fixes and rerun `npm run build && npm run check` before requesting review.
