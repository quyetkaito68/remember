# AGENTS.md — Project Guide for AI Agents

## Overview

**REMEMBER** — Personal knowledge base built with VitePress (SSG), hosted on GitHub Pages. Markdown files are the single source of truth; the build pipeline generates asset manifests and viewer pages automatically.

## Key Directories

| Path | Purpose |
|------|---------|
| `docs/` | All Markdown content + assets. **Only user-authored files.** |
| `docs/.vitepress/` | VitePress config, theme (Vue components), sidebars, styles. |
| `docs/.vitepress/theme/components/` | Vue components: `AssetViewer.vue`, `RelatedFilesPanel.vue`, `Breadcrumbs.vue`. |
| `docs/.vitepress/theme/utils/` | `assetRegistry.js` — fetches manifest, resolves assets. |
| `docs/.vitepress/generated/` | Auto-generated `assets-manifest.json` (gitignored). |
| `docs/public/` | Copied assets at build time (gitignored). |
| `docs/generated/` | Auto-generated asset viewer pages (gitignored). |
| `scripts/` | `generate-assets.js` — scans `docs/`, builds manifest, copies assets, generates pages. |
| `.github/workflows/` | `deploy.yml` — CI/CD to GitHub Pages. |

## Architecture

```
Markdown (.md) + Assets (bat, ps1, ...)
        │
        ▼
generate-assets.js (pre-build)
  - scans docs/ folders
  - builds assets-manifest.json
  - copies assets → docs/public/
  - generates asset pages → docs/generated/assets/
        │
        ▼
VitePress build → dist/ → GitHub Pages
        │
        ▼
Browser:
  - fetch assets-manifest.json
  - RelatedFilesPanel shows downloadable assets per page
  - AssetViewer renders image/pdf/video/audio/text preview
```

## Content Rules

- Each topic folder under `docs/` contains `.md` file(s) + related asset files (`.bat`, `.ps1`, `.sql`, etc.).
- Asset files (non-md) are automatically detected by `generate-assets.js`.
- All markdown files use frontmatter: `title`, `description`, `tags`, `category`, `updated`, `order`.
- `order` in frontmatter controls sidebar sort position.
- Create `index.md` in a folder to make it appear in the top nav bar.

## Build Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Generate assets + start VitePress dev server |
| `npm run build` | Generate assets + build for production |
| `npm run generate-assets` | Run asset scan only |

## Vue Components

- **RelatedFilesPanel.vue** — Shows download/raw links for assets in the same folder as current page.
- **AssetViewer.vue** — Full preview of a single asset (image, pdf, video, audio, text code block with copy button, or download fallback).
- **Breadcrumbs.vue** — Auto-generated breadcrumbs from route path.

## Key Behaviors

- `a.url` = link to the generated viewer page (`/generated/assets/.../`).
- `a.rawUrl` = link to the actual raw asset file (`/public/...`).
- Download links should use `a.rawUrl || a.url`.
- Text file types: `.ps1`, `.bat`, `.cmd`, `.sh`, `.sql`, `.json`, `.xml`, `.yml`, `.yaml`, `.ini`, `.reg`, `.env`, `.txt`, `.js`, `.ts`, `.py`, `.java`, `.c`, `.cpp`, `.css`, `.html`, `.md`.

## Git Conventions

- Branch: `main`
- Standard commit messages (English or Vietnamese).
- Avoid committing secrets or generated files (public/, generated/ are gitignored).

## Coding Style

- Vue: `<script setup>`, no comments in code, concise.
- CSS: single-line rules, flat, no preprocessors.
- JS: ES modules (`type: "module"`), no TypeScript.
- Prefer editing existing files, avoid creating new files unless necessary.
