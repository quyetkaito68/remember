---
title: About
description: Kiến trúc tổng thể và luồng hoạt động của website REMEMBER
tags: [about, architecture]
hideFromSidebar: true
order: 0
updated: 2026-07-05
---

# <span class="site-title">Về website này</span>

**REMEMBER** là personal knowledge base — lưu trữ kiến thức dưới dạng Markdown, build thành website tĩnh bằng VitePress, deploy lên GitHub Pages.

---

## Tech Stack

```text
┌────────────────────────────────────────────────────────────┐
│                     SOURCE (docs/)                         │
│  Markdown (.md) + Assets (.bat, .ps1, .sql, ...)           │
└────────────────────────────────────────────────────────────┘
                            │
                            v
┌────────────────────────────────────────────────────────────┐
│                   PRE-BUILD (scripts/)                     │
│  generate-assets.js                                        │
│  - Quét docs/, phát hiện page + asset                      │
│  - Sinh assets-manifest.json                               │
│  - Copy asset -> docs/public/                              │
│  - Sinh asset viewer pages -> docs/generated/assets/       │
└────────────────────────────────────────────────────────────┘
                            │
                            v
┌────────────────────────────────────────────────────────────┐
│               STATIC SITE GENERATOR (VitePress)            │
│  - Markdown Renderer                                       │
│  - Vue Components: AssetViewer, RelatedFiles, Breadcrumbs  │
│  - Theme config: Nav bar, Sidebar, Search                  │
└────────────────────────────────────────────────────────────┘
                            │
                            v
┌────────────────────────────────────────────────────────────┐
│                   STATIC OUTPUT (dist/)                    │
│  HTML + CSS + JS + Assets (hoàn toàn tĩnh)                 │
└────────────────────────────────────────────────────────────┘
```

## Kiến trúc triển khai

```text
┌────────────────────────────────────────────────────────────┐
│                       Developer                            │
│                   (Viết Markdown)                          │
└────────────────────────────────────────────────────────────┘
                            git push
                            │
                            v
┌────────────────────────────────────────────────────────────┐
│                 GitHub Repository                          │
│             (Source of Truth / main)                       │
└────────────────────────────────────────────────────────────┘
                            │
                            v
┌────────────────────────────────────────────────────────────┐
│                GitHub Actions (CI/CD)                      │
│  Workflow: deploy.yml                                      │
│  Steps: checkout -> npm ci -> npm run build                │
│         -> upload-pages-artifact                           │
└────────────────────────────────────────────────────────────┘
                            │
                            v
┌────────────────────────────────────────────────────────────┐
│                  GitHub Pages (CDN)                        │
│  Static hosting, HTTPS, cache edge global                  │
│  Tự động deploy mỗi lần push main                          │
└────────────────────────────────────────────────────────────┘
                            │
                            v
┌────────────────────────────────────────────────────────────┐
│                     Browser (User)                         │
│  - Trang content gốc (/topic/)                             │
│  - Asset viewer pages (/generated/assets/)                 │
│  - Search local (full-text)                                │
│  - Related files panel                                     │
└────────────────────────────────────────────────────────────┘
```

## Cấu trúc Thư mục

```text
┌────────────────────────────────────────────────────────────┐
│  docs/                        # Markdown (thượng nguồn)    │
│  ├── .vitepress/              # Config, theme, Vue         │
│  │   ├── config.js                                         │
│  │   ├── sidebar.js                                        │
│  │   └── theme/                                            │
│  │       ├── components/                                   │
│  │       └── utils/                                        │
│  ├── public/                  # Asset copy (gitignored)    │
│  ├── generated/               # Asset pages (gitignored)   │
│  ├── <topic>/                 # Content theo chủ đề        │
│  │   ├── *.md                                              │
│  │   └── *.bat, *.ps1, ...                                 │
│  ├── index.md                  # Trang chủ                 │
│  └── about.md                  # Trang giới thiệu          │
│                                                            │
│  scripts/                      # Build tooling             │
│  ├── generate-assets.js                                    │
│  └── generate-toc.js                                       │
│                                                            │
│  templates/                    # Markdown templates        │
│  ├── tutorial-guide.template.md                            │
│  ├── topic-overview.template.md                            │
│  ├── technical-reference.template.md                       │
│  └── script-documentation.template.md                      │
└────────────────────────────────────────────────────────────┘
```

## Công nghệ và Lý do chọn

### VitePress
- Markdown-first, build ra website tĩnh, không cần database hay server runtime
- Tích hợp sẵn full-text search, sidebar auto-generate, theme tùy biến qua Vue
- Cộng đồng lớn, tài liệu tốt, hỗ trợ Mermaid plugin

### Vue 3 (Components)
- Nhẹ, reactive, dễ nhúng component tương tác vào trang tĩnh
- AssetViewer + RelatedFilesPanel cho phép xem trước và tải assets ngay trong trang

### GitHub Pages + Actions
- Deploy zero-cost, HTTPS mặc định, CDN global
- CI/CD tự động: push main -> build -> deploy, không cần thao tác thủ công

### Markdown làm nguồn duy nhất
- AI-friendly: dễ đọc, dễ sinh nội dung
- Version control bằng Git, lưu trữ vĩnh viễn
- Không lock-in: có thể chuyển sang SSG khác bất cứ lúc nào

## Ưu điểm

| Ưu điểm | Mô tả |
|---------|-------|
| Không chi phí | Host trên GitHub Pages (free), build bằng GitHub Actions (free) |
| Tốc độ tối đa | Website tĩnh, load nhanh, cache tốt, không cần server |
| AI thân thiện | Markdown dễ đọc, dễ sinh, dễ xử lý bằng AI tool |
| Tự động hóa | Push code là deploy, không cần manual |
| Asset đi kèm | File .bat, .ps1, .sql đi kèm trang được preview và tải trực tiếp |
| Tìm kiếm | Full-text search local, không cần backend |
| Mở rộng được | Thêm content bằng cách tạo file .md mới, không cần config |
