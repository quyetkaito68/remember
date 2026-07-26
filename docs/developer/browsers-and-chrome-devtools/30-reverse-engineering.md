---
title: Reverse Engineering Website
description: "Reverse Engineering Website — phân tích tech stack, xác định framework, tìm API endpoints, reverse engineer luồng hoạt động của ứng dụng web"
tags: [reverse-engineering, tech-stack, framework-detection, api-analysis, web-reverse-engineering]
category: developer
updated: 2026-07-26
order: 30
---

# Reverse Engineering Website

Phân tích trang web để hiểu kiến trúc, technology, API và data flow.

---

## RE Workflow

```text
Detect Framework ──▶ Map API Endpoints ──▶ Trace Data Flow ──▶ Document Architecture
```

---

## Framework Detection

### DOM + Network Signatures

| Framework | DOM Identifiers | Static Files |
|-----------|----------------|--------------|
| React | `data-reactroot`, `__reactFiber$...` | `/static/js/bundle.js` |
| Vue | `data-v-xxxx`, `__vue_app__` | — |
| Angular | `ng-version="X"`, `_nghost-xxxx` | `/main.*.js` |
| Next.js | `<div id="__next">`, `__NEXT_DATA__` | `/_next/static/chunks/...` |
| Nuxt.js | `<div id="__nuxt">`, `__NUXT_DATA__` | `/_nuxt/...` |
| Svelte | — | `/_app/...` |

### Window Object

```javascript
window.__NEXT_DATA__                    // Next.js
window.__NUXT__                         // Nuxt.js
window.__REACT_DEVTOOLS_GLOBAL_HOOK__   // React
window.ng                              // Angular
window.__VUE__                          // Vue
```

### Extensions

| Extension | Use |
|-----------|-----|
| **Wappalyzer** | Full tech stack detection |
| **BuiltWith** | Technology profiler |
| **React/Vue/Angular DevTools** | Component tree inspection |

---

## API Discovery

### 5 Methods

| # | Method | How |
|---|--------|-----|
| 1 | Network Tab | Filter Fetch/XHR, watch requests |
| 2 | Source Search | `fetch("`, `axios.`, `$.ajax` |
| 3 | Bundle Analysis | Search bundle.js for API URLs |
| 4 | Service Worker | Check SW for cached API patterns |
| 5 | Console | Global API config objects |

### Network Tab Analysis

```text
DevTools → Network → Filter: Fetch/XHR
├─ URL patterns: /api/v1/, /graphql, /rest/
├─ Headers: Content-Type, Authorization
├─ Response: JSON, XML
└─ Static: CDN domain, X-Powered-By
```

### GraphQL Indicators

```text
POST /graphql
Request body: {"query":"..."}
Source: gql`...`, graphql`...`
```

---

## Reverse Engineer Flow

### API Endpoint Map

```text
GET    /api/v1/users           → List users
GET    /api/v1/users/:id       → Get user
POST   /api/v1/users           → Create user
POST   /api/v1/auth/login      → Login
POST   /api/v1/auth/refresh    → Refresh token
```

### Auth Flow

```text
Login:  POST /auth/login {email,password} → {token, refreshToken}
Use:    Header: Authorization: Bearer <token>
Refresh: POST /auth/refresh {refreshToken} → {token}
```

### Data Flow

```text
User Action → JS Handler → API Call → Server → DB → Response → State → DOM → UI
```

---

## JavaScript Bundle Analysis

### Source Maps

```text
Available → DevTools → Sources → original .ts/.tsx files
None     → Format minified code → search strings/URLs
```

### Search in Bundle

| Search | Tìm gì |
|--------|--------|
| `http://`, `https://` | API URLs |
| `fetch(`, `axios.` | HTTP calls |
| `localStorage` | Storage usage |
| `WebSocket` | WS connections |
| `graphql` | GraphQL queries |
| `Bearer` | Auth tokens |

---

## Common Tech Stack Patterns

| Frontend | Backend | Database | CDN |
|----------|---------|----------|-----|
| React + Next.js | Node.js + Express | PostgreSQL | Vercel |
| Vue + Nuxt | Node.js + Fastify | MongoDB | Netlify |
| Angular | .NET Core | SQL Server | Azure |
| React | Django | PostgreSQL | AWS |
| Vue | Laravel | MySQL | Cloudflare |

---

## RE Checklist

| # | Check | Tool |
|---|-------|------|
| 1 | Frontend framework | DOM, window, Wappalyzer |
| 2 | Backend technology | `X-Powered-By` header |
| 3 | API endpoints | Network tab, source search |
| 4 | Auth method | Login request analysis |
| 5 | Data format | Request/Response body |
| 6 | Caching strategy | `Cache-Control` headers |
| 7 | Third-party services | Network tab domain filter |
| 8 | Build tool | Bundle file patterns |
| 9 | CDN provider | Asset URLs |
| 10 | Rate limiting | 429 error responses |

---

## Tool Reference

| Tool | Use |
|------|-----|
| **Chrome DevTools** | Network, Sources, Elements |
| **Wappalyzer** | Tech stack detection |
| **Postman** | API testing |
| **curl** | Quick HTTP requests |
| **Wireshark** | Network traffic analysis |
| **mitmproxy** | HTTP proxy intercept |

---

Xem thêm: [Web Scraping](31-web-scraping.md) | [Network Panel](21-devtools-network.md) | [Anti-bot](32-anti-bot.md)