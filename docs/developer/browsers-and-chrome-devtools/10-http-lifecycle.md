---
title: HTTP/HTTPS Lifecycle
description: "HTTP/HTTPS Lifecycle — toàn bộ quá trình từ URL enter đến response render: DNS, TCP, TLS, Request, Response, Parse, Render"
tags: [http, https, http-request, http-response, http-method, http-status, http-headers]
category: developer
updated: 2026-07-26
order: 10
---

# HTTP/HTTPS Lifecycle

Từ URL enter đến response render — toàn bộ quá trình HTTP/HTTPS.

---

## Lifecycle Flow

```text
┌─────────────────────────────────────────────────────────────┐
│  1. URL PARSING                                             │
│  https://example.com:443/path?query=value#hash              │
│  protocol: https | hostname: example.com | port: 443        │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│  2. HSTS CHECK → Force HTTPS nếu domain trong HSTS list     │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│  3. SERVICE WORKER CHECK → Check cache hoặc fetch network   │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│  4. CACHE CHECK                                             │
│  Fresh → Serve from cache                                   │
│  Stale → Conditional request (If-None-Match)                │
│  Miss → Continue to network                                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│  5. DNS RESOLUTION → example.com → 93.184.216.34            │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│  6. TCP CONNECTION → SYN → SYN-ACK → ACK                    │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│  7. TLS HANDSHAKE (nếu HTTPS) → 1-RTT hoặc 2-RTT            │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│  8. HTTP REQUEST → GET /path HTTP/2 + Headers + Cookie      │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│  9. SERVER PROCESSING → Route → Auth → DB → Template        │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│  10. HTTP RESPONSE → 200 OK + Headers + Body                │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│  11. BROWSER RENDER → Parse HTML → Fetch CSS/JS → Render    │
└─────────────────────────────────────────────────────────────┘
```

---

## HTTP Request Structure

```text
GET /api/users?page=1&limit=10 HTTP/2
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Accept: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept-Language: vi-VN,vi;q=0.9,en-US;q=0.8
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
```

| Phần | Mô tả |
|------|--------|
| **Request Line** | Method + Path + HTTP Version |
| **Headers** | Metadata (auth, content type, cache) |
| **Body** | Data (POST/PUT only) |

---

## HTTP Methods

| Method | Purpose | Idempotent | Body |
|--------|---------|-----------|------|
| **GET** | Retrieve resource | Yes | No |
| **POST** | Create resource | No | Yes |
| **PUT** | Replace resource | Yes | Yes |
| **PATCH** | Partial update | No | Yes |
| **DELETE** | Delete resource | Yes | Optional |
| **HEAD** | Same as GET, no body | Yes | No |
| **OPTIONS** | CORS preflight | Yes | No |

---

## HTTP Status Codes

| Range | Category | Ví dụ |
|-------|----------|--------|
| **1xx** | Informational | 100 Continue, 101 Switching Protocols |
| **2xx** | Success | 200 OK, 201 Created, 204 No Content |
| **3xx** | Redirection | 301 Moved Permanently, 304 Not Modified |
| **4xx** | Client Error | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests |
| **5xx** | Server Error | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable |

---

## HTTP Headers quan trọng

### Request Headers

| Header | Mô tả |
|--------|--------|
| `Authorization` | Authentication token |
| `Content-Type` | Body format (JSON, form, etc.) |
| `Accept` | Expected response format |
| `Cache-Control` | Cache behavior |
| `If-None-Match` | ETag conditional request |
| `If-Modified-Since` | Last-Modified conditional request |
| `Cookie` | Cookies |

### Response Headers

| Header | Mô tả |
|--------|--------|
| `Content-Type` | Response body format |
| `Content-Length` | Response body size |
| `Cache-Control` | Cache policy |
| `ETag` | Resource version hash |
| `Set-Cookie` | Set browser cookie |
| `Access-Control-Allow-Origin` | CORS policy |
| `Location` | Redirect URL |

---

## HTTPS: HTTP + TLS

| HTTP | HTTPS |
|------|-------|
| Port 80 | Port 443 |
| Plaintext | Encrypted |
| No certificate | Certificate required |
| Browser show "Not Secure" | Padlock icon |
| HTTP/1.1, HTTP/2 | HTTP/1.1, HTTP/2, HTTP/3 |

---

## Caching & HTTP Response

### Cache-Control Directives

| Directive | Mô tả |
|-----------|--------|
| `no-store` | Không cache任何 response |
| `no-cache` | Cache nhưng phải revalidate mỗi lần |
| `max-age=3600` | Cache trong 3600 giây |
| `public` | Cache bởi CDN, proxy, browser |
| `private` | Chỉ cache bởi browser |
| `immutable` | Response không bao giờ thay đổi |

### Conditional Requests

```text
First Request:
  GET /image.png
  Response: 200 OK, ETag: "abc123", Cache-Control: max-age=3600

Cache Expired → Conditional Request:
  GET /image.png
  If-None-Match: "abc123"
  Response: 304 Not Modified (không gửi lại body)
```

---

## HTTP/2 Features trong Lifecycle

| Feature | Mô tả | Ảnh hưởng |
|---------|--------|-----------|
| **Multiplexing** | Nhiều requests trên 1 connection | Không block nhau |
| **Header Compression** | HPACK compression | Giảm header size |
| **Server Push** | Server push resources trước khi client request | Giảm round trips |
| **Stream Priority** | Request priority | Critical resources first |

---

## RESTful API Pattern

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/users` | List users |
| GET | `/api/users/123` | Get user 123 |
| POST | `/api/users` | Create user |
| PUT | `/api/users/123` | Update user 123 |
| DELETE | `/api/users/123` | Delete user 123 |

---

## HTTP Debug trong DevTools

| DevTools Feature | Cách dùng |
|-----------------|-----------|
| **Network Tab** | Xem tất cả requests |
| **Filter** | `status-code:404`, `method:POST`, `type:json` |
| **Waterfall** | Xem thứ tự và thời gian load |
| **Headers tab** | Inspect request/response headers |
| **Preview tab** | Xem response body |
| **Timing tab** | Phân tích từng phase |

---

## Quick Troubleshooting

| Symptom | Kiểm tra | Giải pháp |
|---------|---------|-----------|
| Slow TTFB | Server processing time | Optimize DB query, caching |
| 304 responses | ETag/Last-Modified match | Cache working correctly, verify max-age |
| CORS errors | `Access-Control-Allow-Origin` header | Fix server CORS config |
| 502 Bad Gateway | Upstream server down | Check load balancer, backend health |
| 429 Too Many Requests | Rate limiting | Add retry logic, backoff |
| Mixed content | HTTP resources on HTTPS page | Update all URLs to HTTPS |
| Slow DNS | DNS Lookup phase | Use dns-prefetch, preconnect |
| SSL errors | Certificate issues | Check cert validity, intermediate certs |

---

Xem thêm: [Networking](09-networking.md) | [HTTP/2 & HTTP/3](11-http2-http3.md) | [Browser Cache](12-browser-cache.md)