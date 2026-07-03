---
title: REMEMBER
description: A personal knowledge base with Markdown as the only source of truth.
tags: [home, wiki]
updated: 2026-07-03
---

# <span class="site-title">HOMEPAGE</span>

Đây là website của QuyetKaito lưu trữ lại các kiến thức.

Đưa vào một thư mục Markdown, công cụ sẽ build thành một website hoàn chỉnh.

```
Markdown (.md)
       │
       │
Static Site Generator
(VitePress / Docusaurus / ...)
       │
       ▼
HTML + CSS + JS
       │
       ▼
Website tĩnh
```

## Kiến trúc tổng thể

```
                              +----------------------+
                              |      GitHub Repo     |
                              |  (Source of Truth)   |
                              +----------+-----------+
                                         |
                                         |
                                 Markdown (.md)
                                         |
                                         |
                          +--------------v---------------+
                          |         VitePress            |
                          | Static Site Generator (SSG)  |
                          +--------------+---------------+
                                         |
                            Build HTML/CSS/JS
                                         |
                      +------------------v------------------+
                      |              dist/                  |
                      |       Static Website Output         |
                      +------------------+------------------+
                                         |
                            GitHub Actions (CI/CD)
                                         |
                                         |
                          +--------------v---------------+
                          |         GitHub Pages         |
                          |      Static File Hosting     |
                          +--------------+---------------+
                                         |
                                         |
                                 Browser (Desktop/Mobile)
```

## Kiến trúc runtime
```
Browser

    │

    ├────────────── Request /network/tcp

    │

GitHub Pages (CDN)

    │

    ├── index.html

    ├── assets/

    ├── search-index

    ├── css

    └── js

    │

Browser Render

    │

Markdown -> HTML

    │

User
```

## Flow phát triển
```
Viết Markdown

        │

git add

        │

git commit

        │

git push

        │

GitHub Actions

        │

npm install

        │

vitepress build

        │

Generate Static Website

        │

Deploy GitHub Pages

        │

Website Online
```


