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
| `templates/` | **New.** Markdown templates per content type — pick the right one for each new file. |
| `scripts/` | `generate-assets.js` — scans `docs/`, builds manifest, copies assets, generates pages. `read-document.py` — reads .docx/.pdf files and outputs markdown. `verify-diagram.ps1` — checks ASCII diagram alignment. |
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

## Markdown Templates

Standard templates for writing content are at `templates/`. Pick the right template for your content type:

| Template | Use Case |
|----------|----------|
| `templates/tutorial-guide.template.md` | Step-by-step guides (Git, Windows, Network) |
| `templates/topic-overview.template.md` | Broad topic overviews, architecture (AI ecosystem) |
| `templates/technical-reference.template.md` | Technical problems, diagnosis, fixes (MySQL errors) |
| `templates/script-documentation.template.md` | Scripts, tools, config files (backup, clean-temp) |

**How to use:** Copy the `.template.md` to your target folder, rename to `<slug>.md`, fill in content following the `<!-- AI: … -->` comments, then remove those comments.

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

## Reading Documents

Use `python scripts/read-document.py <file-path>` to read `.docx` and `.pdf` files. Output is markdown text printed to stdout.

Dependencies: `python-docx`, `pypdf` (installed globally).

## Git Conventions

- Branch: `main`
- Standard commit messages (English or Vietnamese).
- Avoid committing secrets or generated files (public/, generated/ are gitignored).

## Coding Style

- Vue: `<script setup>`, no comments in code, concise.
- CSS: single-line rules, flat, no preprocessors.
- JS: ES modules (`type: "module"`), no TypeScript.
- Prefer editing existing files, avoid creating new files unless necessary.

## ASCII Diagram Rules

Xem skill `ascii-diagram` (.claude/skills/ascii-diagram/SKILL.md) cho quy tắc đầy đủ. Chạy `powershell -File scripts/verify-diagram.ps1 -File <path-to-md>` để verify diagram.
