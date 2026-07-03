# REMEMBER

A production-ready personal knowledge base powered by VitePress.

## Architecture

- `docs/` — Markdown source files and the single source of truth.
- `docs/.vitepress/` — site configuration, theme customizations, and build helpers.
- `docs/index.md` — the personal wiki homepage.
- `.github/workflows/deploy.yml` — GitHub Actions workflow for automatic GitHub Pages deployment.

## Features

- Markdown-first content model
- Automatic navigation and recursive sidebar generation from folder structure
- Breadcrumbs generated from current route segments
- Local full-text search powered by VitePress
- Light/dark mode with responsive layout
- Syntax highlighting and Mermaid diagrams
- Frontmatter support for title, description, tags, category, order, updated
- Previous/Next navigation via sidebar structure
- Zero backend, static site generation only

## Development

Install dependencies:

```bash
npm install
```

Run local development server:

```bash
npm run dev
```

Build the site:

```bash
npm run build
```

Serve the generated site locally:

```bash
npm run serve
```

## Deployment

Github Page - GithubActions