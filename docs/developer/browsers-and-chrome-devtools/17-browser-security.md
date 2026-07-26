---
title: Browser Security
description: "Browser Security — Same-Origin Policy, CORS, CSP, Permissions Policy: các cơ chế bảo mật built-in của trình duyệt hiện đại"
tags: [browser-security, same-origin-policy, cors, csp, permissions-policy, content-security-policy]
category: developer
updated: 2026-07-26
order: 17
---

# Browser Security

SOP cô lập origins → CORS cho phép cross-origin có kiểm soát → CSP chống XSS → Permissions Policy kiểm soát features.

---

## Security Model

```text
┌────────────────────────────────────────────────────────────┐
│                    BROWSER SECURITY                        │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │  Same-Origin  │  │    CORS      │  │      CSP         │ │
│  │  Policy       │  │  (Explicit)  │  │  (Policy-based)  │ │
│  └───────────────┘  └──────────────┘  └──────────────────┘ │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │ Permissions   │  │  Secure      │  │  Sandbox         │ │
│  │ Policy        │  │  Contexts    │  │  (iframe)        │ │
│  └───────────────┘  └──────────────┘  └──────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

---

## Same-Origin Policy (SOP)

Origin = `protocol + domain + port`

```text
https://example.com:443/path
│         │          │
protocol  domain     port

https://example.com  == https://example.com:443  ✅
http://example.com   != https://example.com      ❌
https://api.example.com != https://example.com   ❌
```

### SOP Rules

| Action | Same Origin | Cross Origin |
|--------|------------|-------------|
| Read DOM / cookies / localStorage | ✅ | ❌ |
| AJAX request | ✅ | ❌ (cần CORS) |
| Execute script | ✅ | ❌ |
| Load image / CSS | ✅ | ✅ (but can't read) |
| Load script | ✅ | ✅ (can execute) |
| Form submit | ✅ | ✅ |

```text
https://bank.com (logged in)
  reads DOM of
  ▼
https://evil.com
  ❌ BLOCKED by SOP
```

---

## CORS

### Flow

```text
Browser                    Server (api.example.com)
  │── OPTIONS /api/data ──▶│  (Preflight)
  │   Origin: app.test.com │
  │◀── 204 + CORS headers ─│
  │── POST /api/data ─────▶│  (Actual Request)
  │◀── 200 + CORS headers ─│
```

### Headers

| Header | Ví dụ |
|--------|--------|
| `Access-Control-Allow-Origin` | `*` hoặc `https://app.com` |
| `Access-Control-Allow-Methods` | `GET, POST, PUT` |
| `Access-Control-Allow-Headers` | `Content-Type, Authorization` |
| `Access-Control-Allow-Credentials` | `true` |
| `Access-Control-Max-Age` | `86400` |

### Simple vs Preflight

| Simple Request | Preflight Required |
|----------------|-------------------|
| GET, POST, HEAD | PUT, DELETE, PATCH |
| Limited headers | Custom headers |

### CORS Troubleshooting

| Error | Nguyên nhân | Giải pháp |
|-------|------------|-----------|
| `No 'Access-Control-Allow-Origin'` | Server thiếu CORS header | Configure server CORS |
| `Method not allowed` | Method không trong Allow-Methods | Add method |
| `Header not allowed` | Header không trong Allow-Headers | Add header |
| `Credentials not supported` | `withCredentials` nhưng thiếu `Allow-Credentials` | Set `Access-Control-Allow-Credentials: true` |

---

## CSP

### Directives

| Directive | Kiểm soát |
|-----------|----------|
| `default-src` | Fallback cho tất cả |
| `script-src` | JavaScript sources |
| `style-src` | CSS sources |
| `img-src` | Image sources |
| `connect-src` | AJAX, WebSocket, EventSource |
| `frame-src` | iframe sources |
| `object-src` | Plugin sources |
| `frame-ancestors` | Ai embed được page này |
| `base-uri` | Base tag URL |
| `form-action` | Form submission targets |

### Values

| Value | Mô tả |
|-------|--------|
| `'none'` | Không cho phép |
| `'self'` | Chỉ cùng origin |
| `'unsafe-inline'` | Inline script/style |
| `'unsafe-eval'` | eval() |
| `'nonce-abc123'` | Script với nonce |
| `'sha256-...'` | Script với hash |

### Example

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-abc123' https://cdn.example.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://api.example.com;
  frame-src 'none';
  object-src 'none';
  frame-ancestors 'none';
```

---

## Permissions Policy

```text
Permissions-Policy:
  camera=(),
  microphone=(),
  geolocation=(self),
  payment=(),
  fullscreen=(self)
```

| Feature | Values |
|---------|--------|
| `camera`, `microphone` | `()`, `(self)`, `(...)` |
| `geolocation` | `()`, `(self)`, `(...)` |
| `payment` | `()`, `(self)`, `(...)` |
| `fullscreen` | `()`, `(self)`, `(...)` |

---

## Secure Contexts (HTTPS Required)

| API | HTTPS Required |
|-----|---------------|
| Service Worker | ✅ |
| Push Notification | ✅ |
| Geolocation | ✅ |
| Camera/Microphone | ✅ |
| Crypto.subtle | ✅ |
| Clipboard API | ✅ |

### HSTS

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

---

## Security Headers Checklist

| # | Header | Protection |
|---|--------|-----------|
| 1 | `Content-Security-Policy` | XSS, data injection |
| 2 | `Strict-Transport-Security` | Protocol downgrade |
| 3 | `X-Content-Type-Options: nosniff` | MIME sniffing |
| 4 | `X-Frame-Options: DENY` | Clickjacking |
| 5 | `Referrer-Policy: no-referrer` | Referrer leakage |
| 6 | `Permissions-Policy` | Feature abuse |

---

**Xem thêm:** [XSS & CSRF](18-xss-csrf.md) | [Web Storage](13-web-storage.md) | [Chrome DevTools](19-chrome-devtools.md)