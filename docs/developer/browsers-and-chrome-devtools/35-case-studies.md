---
title: Case Study Thực Tế
description: "Case Study thực tế — phân tích website: e-commerce, SPA, social media, SaaS với browser & DevTools"
tags: [case-study, real-world, ecommerce, spa, saas, practical-analysis]
category: developer
updated: 2026-07-26
order: 35
---

# Case Study Thực Tế

> Phân tích website thực tế với DevTools: tech stack, performance, API, scraping.

---

## Tech Stack Detection Checklist

| Check | Location | Result |
|-------|----------|--------|
| `#root` | Elements tab | React |
| `#__next` | Elements tab | Next.js |
| `#app` | Elements tab | Vue |
| `window.__NEXT_DATA__` | Console | Next.js data |
| `window.__NUXT__` | Console | Nuxt.js data |
| Meta generator | Elements tab | Framework name |
| Script src patterns | Network tab | Build tool, CDN |

---

## Quick Analysis Template

```text
Website: _______________

Tech Stack:
  Frontend: _______________
  Backend:  _______________
  CDN:      _______________

Performance:
  Lighthouse: ___/100
  LCP: ___s  CLS: ___  INP: ___ms
  Requests: ___  Total Size: ___MB

API:
  Pattern: REST / GraphQL
  Auth: Bearer / Cookie / Session

Scrapability:
  Static HTML: Yes / No
  Has API: Yes / No
  Anti-bot: None / Cloudflare / Custom
```

---

## Case Study 1: E-Commerce Website

### Phân tích

```text
Bước 1: Tech Stack → Elements tab → #__next → Next.js
Bước 2: Network → Filter XHR → API calls:
         GET  /api/products?page=1&limit=20
         GET  /api/products/:id
         POST /api/cart
Bước 3: Performance → Flame chart: Scripting 45%, Rendering 25%
Bước 4: Images → 50 images, 3MB total, no lazy load
```

### Kết quả

| Finding | Detail | Optimization |
|---------|--------|-------------|
| Framework | Next.js (React SSR) | — |
| Bundle | vendor.js 1.2MB | Code split, tree shake |
| Images | 3MB, no lazy load | Lazy load, WebP |
| Fonts | 4 custom fonts | Reduce to 2 |
| Third-party | 15 scripts | Reduce, async |

---

## Case Study 2: SPA Dashboard

### Phân tích

```text
Lighthouse: 45/100 → LCP 6.2s, CLS 0.35, TBT 2500ms
Performance Profile → Main thread blocked 60% by JS
  Long tasks: processLargeDataset (800ms), renderChart (400ms)
Memory → Heap keeps growing, 500+ detached nodes
Network → 50 requests on load, some payloads 5MB+
```

### Solutions

| Issue | Fix | Result |
|-------|-----|--------|
| Bundle 2.5MB | Code split + lazy load | -40% size |
| Memory leak | Remove listeners on unmount | Stable 150MB |
| 50 API calls | Pagination + cache | -70% payload |
| CLS 0.35 | Explicit dimensions + skeleton | CLS 0.05 |

---

## Case Study 3: Social Media Infinite Scroll

### Phân tích

```text
Network → GET /api/feed?cursor=abc123&limit=20
  Response: data[], nextCursor (base64 timestamp)
DOM → New posts appended, old NOT removed
  Virtual scrolling? Only ~50 DOM nodes visible
Performance → 60fps scroll, images lazy loaded
  Videos: autoplay muted, pause on viewport exit
```

**Key insight:** Cursor = base64 timestamp → dùng cho pagination trong scraping.

---

## Case Study 4: SaaS Auth Flow

### Phân tích

```text
Login:    POST /api/auth/login → { token, refreshToken, user }
Refresh:  POST /api/auth/refresh (every 15 min)
Session:  30 min inactivity timeout, heartbeat every 5 min
```

### Security Check

| Check | Status |
|-------|--------|
| HttpOnly cookie | ✅ XSS protection |
| SameSite=Lax | ✅ CSRF protection |
| HTTPS only | ✅ |
| Token in localStorage | ⚠️ XSS risk (backup) |
| CSP header | ✅ |

---

## Case Study 5: API-Heavy SPA

### Before vs After

```text
BEFORE:                        AFTER:
JS Bundle: 2.5MB               JS Bundle: 800KB (split)
API calls: 15 (parallel)       API calls: 3 (critical only)
Time to interactive: 8s        Time to interactive: 2s
Lighthouse: 35/100             Lighthouse: 85/100
```

| Change | Impact |
|--------|--------|
| Code split: main + vendor + charts | -68% bundle |
| Lazy load non-critical widgets | Faster initial |
| API: summary first, details on demand | -80% requests |
| WebP + lazy load images | -50% image size |
| System fonts + preload 1 font | Faster FCP |
| Service Worker cache | Offline + speed |

---

## Analysis Framework

```text
┌──────────────────────────────────────────────┐
│  WEBSITE ANALYSIS FRAMEWORK                  │
│                                              │
│  1. TECH STACK                               │
│     Frontend / Backend / Database / CDN      │
│                                              │
│  2. ARCHITECTURE                             │
│     SSR/CSR/SSG / API pattern / State mgmt   │
│                                              │
│  3. PERFORMANCE                              │
│     CWV / Bundle size / Requests / Cache     │
│                                              │
│  4. SECURITY                                 │
│     HTTPS / CSP / Auth method / CORS         │
│                                              │
│  5. SCRAPABILITY                             │
│     Static? / API? / Anti-bot? / Rate limit? │
└──────────────────────────────────────────────┘
```

---

Xem thêm: [Reverse Engineering](30-reverse-engineering.md) | [Performance Optimization](33-performance-optimization.md) | [Debugging Guide](34-debugging-guide.md)