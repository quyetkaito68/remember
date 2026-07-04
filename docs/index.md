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

## Flow bằng text:
1. Viết nội dung Markdown ở trong docs và đặt asset kèm theo cùng thư mục.
2. Khi chạy build, script trong generate-assets.js sẽ quét thư mục này.
3. Script sẽ:
    - phát hiện page Markdown,
    - phát hiện asset liên quan,
    - sinh manifest JSON,
    - tạo route cho asset page,
    - publish asset vào output tĩnh để browser có thể truy cập.
4. VitePress đọc Markdown và render thành HTML.
5. Theme trong index.js chèn giao diện như panel liên quan và viewer.
6. Khi người dùng mở trang, browser sẽ fetch manifest rồi render UI.

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

## Tính năng preview cả file script đính kèm file markdown chính

Lý do hiện tại phải copy assets file vào docs/public là vì build của VitePress tạo ra một output tĩnh riêng, chủ yếu là HTML/CSS/JS. Các file gốc nằm trong thư mục markdown ban đầu không tự động “được expose” như một URL có thể tải trực tiếp từ browser sau khi deploy.

```
+------------------------------+
|  Source content (docs/)      |
|  - page.md                   |
|  - asset files (.bat, .ps1) |
+--------------+---------------+
               |
               v
+------------------------------+
|  Generate step               |
|  - scan folders              |
|  - detect page + asset       |
|  - create manifest           |
|  - create asset routes       |
|  - copy/publish assets       |
+--------------+---------------+
               |
               v
+------------------------------+
|  VitePress build             |
|  - Markdown -> HTML          |
|  - inject theme components  |
+--------------+---------------+
               |
               v
+------------------------------+
|  Static output (dist/)       |
|  - html/css/js/assets        |
+--------------+---------------+
               |
               v
+------------------------------+
|  Browser                     |
|  - load page                 |
|  - fetch manifest           |
|  - show Related Files/UI    |
+------------------------------+
```

## 1. Repository Layout
```
docs/

├── computer/
│
│   ├── windows/
│   │
│   │   ├── clean-temp/
│   │   │
│   │   │   clean-temp.md        <-- Main Document
│   │   │   clean-temp.bat       <-- Asset Document
│   │   │   clean-temp.ps1
│   │   │   clean-temp.sql
│   │   │   clean-temp.png
│   │   │
│   │   └── firewall/
│   │
│   └── linux/
│
└── .vitepress/
```

## 2. Build Flow
```
                   npm run docs:build

                           │

                           ▼

             Asset Manifest Generator

                           │

        Scan every folder inside docs/

                           │

                           ▼

        Detect Main Document (.md)

                           │

                           ▼

      Detect Related Asset Documents

                           │

                           ▼

      Build assets-manifest.json

                           │

                           ▼

        Generate Static Website
```

## 3. Manifest

Ví dụ:
```
clean-temp/

    clean-temp.md
    clean-temp.ps1
    clean-temp.bat
    clean-temp.sql
```
Sinh ra

```
assets-manifest.json

│

├── page
│      /computer/windows/clean-temp
│
│      markdown
│          clean-temp.md
│
│      assets
│
│      ├── clean-temp.ps1
│      ├── clean-temp.bat
│      └── clean-temp.sql
│
└── ...
```


## 4. Runtime Flow

Khi user mở
```
/clean-temp/
```

flow sẽ là 
```
Browser

     │

     ▼

VitePress Router

     │

     ▼

Markdown Renderer

     │

     ▼

Load Page Metadata

     │

     ▼

Asset Manager

     │

     ▼

Read assets-manifest.json

     │

     ▼

Find Related Assets

     │

     ▼

Render Asset Panel
```

## 5. Asset Manager

Đây là trung tâm của toàn bộ tính năng.

```
                 Asset Manager

                       │

      ┌────────────────┼─────────────────┐

      │                │                 │

 Asset Registry   Asset Resolver   Asset Viewer

      │                │                 │

      │                │                 │

 Manifest       Current Page      Render UI

      │                │

      └──────────┬─────┘

                 ▼

          Related Assets
```

## 6. Khi click vào Asset

Ví dụ click  clean-temp.ps1

flow


```
User

    │

Click

    │

    ▼

Asset Router

    │

    ▼

Asset Resolver

    │

    ▼

Read Manifest

    │

    ▼

Locate File

    │

    ▼

Asset Viewer

    │

    ▼

Preview Renderer

    │

    ▼

Browser

```

