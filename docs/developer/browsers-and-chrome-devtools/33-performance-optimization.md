---
title: Performance Optimization
description: "Performance Optimization — Core Web Vitals, lazy loading, code splitting, image optimization, caching strategies"
tags: [performance-optimization, core-web-vitals, lazy-loading, code-splitting, image-optimization, web-performance]
category: developer
updated: 2026-07-26
order: 33
---

# Performance Optimization

> Core Web Vitals (LCP, CLS, INP) = metrics chính. Tối ưu theo thứ tự: loading → rendering → JS → images → cache.

---

## Core Web Vitals Targets

| Metric | Target | Đo gì | Cách tối ưu chính |
|--------|--------|-------|-------------------|
| **LCP** | ≤2.5s | Largest Contentful Paint | Optimize images, server response |
| **CLS** | ≤0.1 | Cumulative Layout Shift | Set dimensions, preload fonts |
| **INP** | ≤200ms | Interaction to Next Paint | Reduce main-thread work |
| **FCP** | ≤1.8s | First Contentful Paint | Inline critical CSS |
| **TTFB** | ≤800ms | Time to First Byte | Server/CDN optimization |

---

## Performance Audit Checklist

| # | Category | Check | Priority |
|---|----------|-------|----------|
| 1 | Loading | LCP ≤ 2.5s | Critical |
| 2 | Visual | CLS ≤ 0.1 | Critical |
| 3 | Interactivity | INP ≤ 200ms | Critical |
| 4 | Network | HTTP/2 enabled | High |
| 5 | Network | Brotli compression | High |
| 6 | Images | WebP/AVIF format | High |
| 7 | Images | Lazy loading (below fold) | High |
| 8 | JS | Code splitting | High |
| 9 | JS | Tree shaking | Medium |
| 10 | CSS | Critical CSS inline | Medium |
| 11 | CSS | Remove unused CSS | Medium |
| 12 | Cache | Immutable assets (hash in filename) | High |
| 13 | Cache | Cache-Control headers | High |
| 14 | Fonts | Preload critical fonts | Medium |
| 15 | Fonts | font-display: swap | Medium |

---

## Critical Rendering Path

```html
<!-- Inline critical CSS -->
<style>body { margin: 0; font-family: sans-serif; }</style>

<!-- Defer non-critical CSS -->
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">

<!-- Async JavaScript -->
<script src="app.js" defer></script>

<!-- Preload critical resources -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/hero.jpg" as="image">
<link rel="preconnect" href="https://api.example.com">
```

---

## Image Optimization

| Technique | Savings |
|-----------|---------|
| Format (WebP/AVIF vs JPEG) | 25-50% |
| Resize (appropriate dimensions) | 50-80% |
| Compression (quality 80) | 20-30% |
| Lazy loading | Perceived speed |
| Responsive images | Mobile optimization |

```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" loading="lazy" width="800" height="600">
</picture>
<img src="hero.jpg" fetchpriority="high" width="1920" height="1080">
```

---

## JS Optimization

```javascript
// Code splitting
const module = await import('./heavy-module.js');
const Home = React.lazy(() => import('./pages/Home'));

// Tree shaking — BAD vs GOOD
import _ from 'lodash';          // ❌ imports everything
import chunk from 'lodash/chunk'; // ✅ specific function
```

| Technique | Tool |
|-----------|------|
| Tree shaking | Webpack, Rollup |
| Code splitting | Dynamic import |
| Minification | Terser, CSSNano |
| Compression | Brotli (server config) |
| Analyze | webpack-bundle-analyzer |

---

## Caching Strategy

```text
Resource Type        → Cache Strategy
─────────────────────────────────────
HTML Pages           → no-cache (revalidate)
API Responses        → no-cache + ETag
Images (hash)        → max-age=31536000, immutable
CSS/JS (hash)        → max-age=31536000, immutable
Fonts                → max-age=31536000, immutable
```

---

## Network Optimization

| Technique | Impact |
|-----------|--------|
| HTTP/2+ | Multiplexing |
| Brotli > gzip | Better compression |
| CDN | Edge caching, low latency |
| DNS Prefetch |提前 resolve |
| Preconnect | TCP+TLS ahead |

---

## Server-Side Optimization

| Technique | When to use |
|-----------|-------------|
| **SSR** | Faster FCP, SEO |
| **SSG** | Fastest, static content |
| **Edge Rendering** | Low latency globally |
| **DB optimization** | Faster TTFB |

---

## Performance Budget

```json
{
  "budgets": [
    { "resourceType": "total", "budget": 300 },
    { "resourceType": "script", "budget": 100 },
    { "resourceType": "stylesheet", "budget": 50 },
    { "resourceType": "image", "budget": 100 }
  ]
}
```

---

## Tools

| Tool | Dùng để |
|------|--------|
| **Lighthouse** | Performance audit |
| **WebPageTest** | Detailed waterfall |
| **Chrome DevTools** | Performance panel |
| **webpack-bundle-analyzer** | Bundle analysis |
| **Core Web Vitals Extension** | Real-time metrics |

---

Xem thêm: [Rendering Pipeline](04-rendering-pipeline.md) | [Performance Panel](23-devtools-performance.md) | [Lighthouse](26-lighthouse.md)