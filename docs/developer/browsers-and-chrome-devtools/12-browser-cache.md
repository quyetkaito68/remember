---
title: Browser Cache
description: "Browser Cache — HTTP Cache, Memory Cache, Service Worker Cache: các loại cache trong browser, caching strategies và cách tối ưu"
tags: [browser-cache, http-cache, memory-cache, cache-control, etag, service-worker-cache]
category: developer
updated: 2026-07-26
order: 12
---

# Browser Cache

HTTP Cache, Memory Cache, Service Worker Cache — mỗi loại phục vụ mục đích khác nhau, kiểm soát bởi HTTP headers.

---

## Các loại Browser Cache

```text
┌────────────────────────────────────────────────────────┐
│                    BROWSER CACHE                       │
│                                                        │
│  ┌──────────────────────┐                              │
│  │   Service Worker     │  Offline-first, PWA          │
│  │   Cache              │  Kiểm soát hoàn toàn         │
│  └──────────┬───────────┘                              │
│             │                                          │
│  ┌──────────▼───────────┐                              │
│  │   HTTP Cache         │  Cache-Control, ETag         │
│  │   (Disk Cache)       │  Persistent trên disk        │
│  └──────────┬───────────┘                              │
│             │                                          │
│  ┌──────────▼───────────┐                              │
│  │   Memory Cache       │  Session-scoped              │
│  │   (RAM)              │  Nhanh nhất                  │
│  └──────────────────────┘                              │
└────────────────────────────────────────────────────────┘
```

---

## HTTP Cache (Disk Cache)

### Cache Flow

```text
Request → Check Cache
              │
              ├── Fresh (max-age chưa hết) → Serve from cache
              │
              └── Stale (max-age hết hạn) → Conditional Request
                                                │
                                                ├── 304 Not Modified → Serve from cache
                                                │
                                                └── 200 OK → Serve new + update cache
```

### Cache-Control Directives

| Directive | Mô tả | Ví dụ |
|-----------|--------|--------|
| `no-store` | Không cache任何 | `Cache-Control: no-store` |
| `no-cache` | Cache nhưng phải revalidate | `Cache-Control: no-cache` |
| `max-age` | Thời gian cache (giây) | `Cache-Control: max-age=3600` |
| `s-maxage` | max-age cho CDN/proxy | `Cache-Control: s-maxage=86400` |
| `public` | Cache bởi browser + CDN | `Cache-Control: public` |
| `private` | Chỉ cache bởi browser | `Cache-Control: private` |
| `immutable` | Không bao giờ thay đổi | `Cache-Control: immutable` |
| `must-revalidate` | Phải revalidate khi stale | `Cache-Control: must-revalidate` |

### ETag / Last-Modified

```text
First Request:
  GET /style.css
  Response: 200 OK, ETag: "abc123", Cache-Control: max-age=3600

Cache Expired → Conditional Request:
  GET /style.css
  If-None-Match: "abc123"
  Response: 304 Not Modified (không gửi lại body)
```

### Cache Strategy by Resource Type

| Priority | Resource Type | Strategy |
|----------|-------------|----------|
| **High** | CSS, JS (critical) | `max-age=31536000, immutable` + filename hash |
| **High** | Fonts | `max-age=31536000, immutable` |
| **Medium** | Images | `max-age=86400, stale-while-revalidate=604800` |
| **Medium** | API responses | `no-cache` + ETag |
| **Low** | HTML pages | `no-cache` hoặc `max-age=0, must-revalidate` |
| **Never** | Sensitive data | `no-store` |

---

## Memory Cache vs HTTP Cache

| Tính năng | HTTP Cache (Disk) | Memory Cache |
|-----------|-------------------|-------------|
| Storage | Disk | RAM |
| Speed | Nhanh | Rất nhanh |
| Persistence | Persistent (qua session) | Session-scoped |
| Scope | Theo origin + URL | Theo tab |
| Capacity | Lớn (hàng GB) | Nhỏ (hàng MB) |
| Control | HTTP headers | Browser tự quyết định |

---

## Caching Strategies

```text
Cache-First (Stale-While-Revalidate):
  Request → Cache → Found → Serve + background revalidate
                        → Not found → Fetch → Save to cache

Network-First:
  Request → Network → Success → Serve + save to cache
                     → Failure → Serve from cache (fallback)

Cache-Only:
  Request → Cache → Found → Serve | Not found → Error

Network-Only:
  Request → Network → Success → Serve | Failure → Error
```

| Strategy | Dùng khi |
|----------|---------|
| **Cache-First** | Images, fonts, static assets |
| **Network-First** | API calls, dynamic content |
| **Cache-Only** | Offline mode, pre-cached resources |
| **Network-Only** | Analytics, tracking, non-cacheable |

---

## Cache Strategy Code

```javascript
// Cache-First with Stale-While-Revalidate
async function cacheFirst(request) {
  const cache = await caches.open('v1');
  const cached = await cache.match(request);
  if (cached) {
    event.waitUntil(
      fetch(request).then(response => cache.put(request, response.clone()))
    );
    return cached;
  }
  const response = await fetch(request);
  cache.put(request, response.clone());
  return response;
}

// Network-First with Cache Fallback
async function networkFirst(request) {
  try {
    const response = await fetch(request);
    const cache = await caches.open('v1');
    cache.put(request, response.clone());
    return response;
  } catch (error) {
    const cache = await caches.open('v1');
    const cached = await cache.match(request);
    if (cached) return cached;
    throw error;
  }
}
```

---

## Cache Busting

| Method | Mô tả | Vấn đề |
|--------|--------|--------|
| **Filename hashing** | `style.a1b2c3d4.css` — browser thấy hash mới → tải lại | Best practice |
| **Query string** | `style.css?v=2.0` — browser thấy query mới → tải lại | CDN có thể ignore |
| **CDN config** | Dùng `immutable` + hash để tránh revalidation trên CDN | Cần CDN config đúng |

---

## Developer Tools & Cache

| Tool | Mô tả |
|------|--------|
| **Network Tab** | Xem "from cache" / "from disk cache" |
| **Application Tab** | Inspect Cache Storage, Service Worker |
| **Disable Cache** | Network Tab → Disable cache |
| **Hard Reload** | Ctrl+Shift+R (clear cache cho tab) |
| **Clear Storage** | Application → Clear storage |

```text
Name          Status  Size      From Cache
───────────────────────────────────────────
index.html    200     14 KB     ❌ (no-cache)
style.css     200     8 KB      ✅ (from disk cache)
app.js        200     50 KB     ✅ (from memory cache)
image.png     200     100 KB    ❌ (from network)
```

---

## Common Caching Mistakes

| Sai lầm | Giải pháp |
|---------|-----------|
| `Cache-Control: max-age=31536000` trên HTML | HTML là entry point, phải revalidate |
| Không dùng filename hash | Dùng hash để cache bust |
| Cache sensitive data | Dùng `no-store` cho auth tokens |
| `no-cache` thay `no-store` | `no-cache` vẫn cache được (phải revalidate) |
| Không có stale-while-revalidate | Thêm để serve stale trong khi revalidate |

---

## Cache Debugging Checklist

- [ ] Check `Cache-Control` header trong Network Tab → Headers
- [ ] Verify ETag/Last-Modified đã set đúng
- [ ] Test conditional request: xem response 304 hay 200
- [ ] Kiểm tra "from cache" column trong Network Tab
- [ ] Disable cache trong DevTools để test fresh load
- [ ] Hard reload (Ctrl+Shift+R) để clear cache cho tab
- [ ] Verify filename hash thay đổi khi deploy version mới
- [ ] Check Service Worker cache trong Application → Cache Storage
- [ ] Verify `no-store` cho sensitive data (auth tokens, PII)
- [ ] Test stale-while-revalidate:serve stale trong khi revalidate

---

## Cache Strategy Decision Tree

```text
Resource thay đổi?
  │
  ├── Không bao giờ → immutable + max-age=31536000 + hash filename
  │
  ├── Rất ít (fonts, images) → max-age=86400, stale-while-revalidate
  │
  ├── Thỉnh thoảng (API data) → no-cache + ETag
  │
  ├── Thường xuyên (HTML) → no-cache hoặc max-age=0, must-revalidate
  │
  └── Mỗi request (auth, PII) → no-store
```

---

Xem thêm: [HTTP/HTTPS Lifecycle](10-http-lifecycle.md) | [Web Storage](13-web-storage.md) | [Service Worker & PWA](14-service-worker-pwa.md)