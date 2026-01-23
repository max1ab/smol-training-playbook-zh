# Repository Guidelines

## Project Structure & Module Organization
- `app/` houses the Astro site and all runtime code.
  - `app/src/pages/` contains page entry points (notably `index.astro`).
  - `app/src/components/` holds Astro/Svelte UI components.
  - `app/src/content/` stores MDX chapters, embeds, and bibliographic data.
  - `app/src/content/assets/` contains images, data files, and other media.
  - `app/public/` provides static public assets.
- `app/scripts/` includes export, import, and data generation utilities.
- `scripts/` contains repo-level tooling (release automation).
- Root files like `Dockerfile`, `nginx.conf`, and `entrypoint.sh` support deployment.

## Build, Test, and Development Commands
Run commands from `app/` unless noted.
- `npm install`: install dependencies.
- `npm run dev`: start the Astro dev server (default `http://localhost:4321`).
- `npm run build`: production build; also used as the primary automated check.
- `npm run preview`: serve the production build on port 8080.
- `npm run export:pdf`: generate PDF output.
- `npm run export:latex`: generate LaTeX output.
- `npm run latex:convert`: run the LaTeX importer (`app/scripts/latex-importer`).
- `npm run notion:import`: run the Notion importer (`app/scripts/notion-importer`).

## Coding Style & Naming Conventions
- Use Prettier and follow existing patterns in the codebase.
- Keep code self-documenting; add comments only for complex logic.
- Match existing naming: PascalCase for components (e.g., `Hero.astro`), kebab or snake case for data/asset files, and descriptive MDX filenames in `app/src/content/`.
- Target Node.js `>=20` as specified in `app/package.json`.

## Testing Guidelines
- There is no dedicated unit-test runner; treat `npm run build` as the main automated check.
- Manual verification matters: test responsive layouts, light/dark themes, and major browsers (Chrome/Firefox/Safari) per `CONTRIBUTING.md`.
- Export paths should be validated when you change rendering or content (`npm run export:pdf`, `npm run export:latex`).

## Commit & Pull Request Guidelines
- Use Conventional Commits: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`.
- PRs should include a clear description, link related issues, and provide screenshots for UI changes.
- Include test instructions in the PR (e.g., `npm run build`, `npm run export:pdf`).

## Agent-Specific Notes
- Keep edits concise and aligned with the existing Astro/MDX structure.
- Avoid large asset changes unless required; prefer updating content in `app/src/content/`.

## 翻译要求
- 面向技术书籍读者，保持原文结构与逻辑，术语前后一致，必要时对英文长句进行合理拆分，但不得改变原意；代码、符号、专有名词保持不变。
