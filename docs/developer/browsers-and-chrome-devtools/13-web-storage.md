---
title: Web Storage
description: "Web Storage — Cookie, LocalStorage, SessionStorage, IndexedDB, Cache API: các cơ chế lưu trữ dữ liệu trong browser"
tags: [web-storage, cookie, localstorage, sessionstorage, indexeddb, cache-api]
category: developer
updated: 2026-07-26
order: 13
---

# Web Storage

So sánh tất cả storage mechanisms — khi nào dùng cái nào, quota, security tradeoff.

---

## Storage Comparison

| Storage | Scope | Capacity | Persistent | Server-visible | Async | Use case chính |
|---------|-------|----------|-----------|---------------|-------|----------------|
| **Cookie** | Origin | ~4KB | Có (expires) | **Có** (auto-sent) | — | Session, auth, tracking |
| **LocalStorage** | Origin | ~5-10MB | Có | Không | Không (blocking) | User prefs, form draft |
| **SessionStorage** | Tab | ~5-10MB | Không | Không | Không (blocking) | Temporary tab data |
| **IndexedDB** | Origin | ~vô hạn | Có | Không | **Có** | Offline data, large datasets |
| **Cache API** | Origin | ~vô hạn | Có | Không | **Có** | Network responses (SW) |

---

## Decision Tree: Chọn Storage

```text
Cần lưu dữ liệu?
│
├─ Server cần đọc? → Cookie (4KB, auto-sent)
│
├─ Dữ liệu > 5MB? → IndexedDB
│
├─ Cần sync giữa tabs? → LocalStorage
│  └─ Tab-isolated? → SessionStorage
│
├─ Cần cache HTTP responses? → Cache API (dùng với SW)
│
└─ Dữ liệu sensitive? → HttpOnly Cookie (KHÔNG dùng localStorage)
```

---

## Cookie

### Properties

| Property | Ví dụ | Ghi chú |
|----------|--------|---------|
| `domain` | `.example.com` | Scope domain |
| `path` | `/` | Scope path |
| `expires` / `max-age` | `3600` | Thời hạn |
| `secure` | `Secure` | HTTPS only |
| `HttpOnly` | `HttpOnly` | Không JS access |
| `SameSite` | `Strict` / `Lax` / `None` | CSRF protection |

### SameSite

| Value | Behavior |
|-------|----------|
| `Strict` | Không gửi trong cross-site requests |
| `Lax` | Gửi trong top-level GET navigation |
| `None` | Gửi tất cả (cần `Secure`) |

### Cookie vs LocalStorage

| | Cookie | LocalStorage |
|--|--------|-------------|
| Capacity | ~4KB | ~5-10MB |
| Auto-sent | **Có** | Không |
| Server-readable | **Có** | Không |
| Use case | Auth, session | Client settings |

---

## LocalStorage

```javascript
localStorage.setItem('key', JSON.stringify(data));
JSON.parse(localStorage.getItem('key'));
localStorage.removeItem('key');
localStorage.clear();
```

| Đặc điểm | Chi tiết |
|-----------|----------|
| Scope | Origin (protocol + domain + port) |
| Sync | **Blocking** — có thể gây lag trên main thread |
| Quota | Exceed → `QuotaExceededError` |

| Dùng | Không dùng |
|------|-----------|
| Theme, language prefs | Dữ liệu > 5MB |
| Form draft | Dữ liệu sensitive |
| Feature flags | Dữ liệu cần sync giữa tabs |

---

## SessionStorage

Tương tự LocalStorage nhưng **tab-scoped** — tab đóng = mất data, không share giữa tabs.

---

## IndexedDB

```text
IndexedDB Database
├── Object Store "users"
│   ├── { id: 1, name: "John" }
│   └── { id: 2, name: "Jane" }
└── Object Store "posts"
    └── { id: 1, title: "Hello", userId: 1 }
```

```javascript
const request = indexedDB.open('MyDB', 1);
request.onupgradeneeded = (e) => {
  const db = e.target.result;
  db.createObjectStore('users', { keyPath: 'id' });
};
request.onsuccess = (e) => {
  const db = e.target.result;
  const tx = db.transaction('users', 'readwrite');
  tx.objectStore('users').add({ id: 1, name: 'John' });
};
```

### IndexedDB vs LocalStorage

| | LocalStorage | IndexedDB |
|--|-------------|-----------|
| Capacity | ~5-10MB | **Vô hạn** |
| Data type | String only | **Bất kỳ** (Object, Blob, File) |
| Query | Key-value | **Index + range queries** |
| Transaction | Không | **ACID** |
| Async | Không | **Có** |

---

## Cache API

Dùng với Service Worker — lưu trữ network responses.

```javascript
const cache = await caches.open('v1');
await cache.put('/api/data', response);
const cached = await cache.match('/api/data');
await cache.delete('/api/data');
```

| | HTTP Cache | Cache API |
|--|-----------|----------|
| Control | Browser tự | **Developer kiểm soát** |
| Offline | Không | **Offline support** |
| Used by | Browser engine | **Service Worker** |

---

## Storage Quota

| Storage | Limit |
|---------|-------|
| Cookie | ~4KB per cookie |
| LocalStorage | ~5-10MB per origin |
| SessionStorage | ~5-10MB per tab |
| IndexedDB | ~60-80% disk |
| Cache API | ~60-80% disk |

```javascript
const { usage, quota } = await navigator.storage.estimate();
console.log(`Used: ${(usage/quota*100).toFixed(2)}%`);
await navigator.storage.persist(); // Request persistent storage
```

---

## Security Checklist

| # | Check | Priority |
|---|-------|---------|
| 1 | Không lưu sensitive data trong localStorage | Critical |
| 2 | Dùng `SameSite=Strict/Lax` cho session cookie | Critical |
| 3 | Dùng `HttpOnly + Secure` cho auth cookie | Critical |
| 4 | Validate data trước khi store vào IndexedDB | Medium |
| 5 | Monitor quota, cleanup old data | Low |

---

## DevTools

| Panel | Chức năng |
|-------|----------|
| Application → Cookies | Inspect/edit cookies |
| Application → Local Storage | Inspect/edit localStorage |
| Application → Session Storage | Inspect/edit sessionStorage |
| Application → IndexedDB | Inspect/edit IndexedDB |
| Application → Cache Storage | Inspect/edit Cache API |

---

**Xem thêm:** [Browser Cache](12-browser-cache.md) | [Service Worker & PWA](14-service-worker-pwa.md) | [Browser Security](17-browser-security.md)