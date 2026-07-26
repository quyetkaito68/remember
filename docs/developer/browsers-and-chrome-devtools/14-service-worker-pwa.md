---
title: Service Worker & PWA
description: "Service Worker và Progressive Web App — offline-first, background sync, push notification: cách biến web app thành ứng dụng native-like"
tags: [service-worker, pwa, progressive-web-app, offline-first, push-notification, web-app-manifest]
category: developer
updated: 2026-07-26
order: 14
---

# Service Worker & PWA

SW là network proxy chạy nền — intercept requests, cache, offline. PWA = SW + Manifest → installable, offline-capable.

---

## SW Architecture

```text
┌───────────────────────────────────────────────────────┐
│                  BROWSER                              │
│  ┌──────────────────┐    ┌──────────────────────────┐ │
│  │   Main Thread    │    │   Service Worker Thread  │ │
│  │  fetch() ────────│───>│  intercept fetch event   │ │
│  │                  │<───│  return cached / network │ │
│  └──────────────────┘    └──────────────────────────┘ │
│                    ┌─────────────────────────┐        │
│                    │   Cache API             │        │
│                    └─────────────────────────┘        │
└───────────────────────────────────────────────────────┘
```

### SW vs Web Worker

| | Service Worker | Web Worker |
|--|---------------|------------|
| Scope | **Origin-wide** | Chỉ trong page |
| Network | **Intercept requests** | Không |
| Cache | Cache API | Không |
| Use case | Offline, push, sync | Heavy computation |

---

## SW Lifecycle

```text
Register ──▶ Install ──▶ Activate ──▶ Running (Fetch/Events)
                │            │
                ▼            ▼
           Cache static   Cleanup old
           assets         caches
```

| Phase | Chức năng |
|-------|----------|
| **Register** | `navigator.serviceWorker.register('/sw.js')` |
| **Install** | `caches.open('v1')` + `addAll()` — cache static assets |
| **Activate** | Delete old caches, `clients.claim()` |
| **Fetch** | Intercept → cache or network |

### Registration Flow

```text
main.js                        sw.js
  │                              │
  │── register('/sw.js') ──────▶│
  │                              │── install event
  │                              │   caches.addAll(STATIC_ASSETS)
  │                              │   skipWaiting()
  │                              │
  │◀── controlled ──────────────│── activate event
  │                              │   delete old caches
  │                              │   clients.claim()
  │                              │
  │── fetch() ─────────────────▶│── fetch event
  │◀── response ────────────────│   cache-first / network-first
```

### Code

```javascript
// main.js
navigator.serviceWorker.register('/sw.js', { scope: '/' });

// sw.js
const CACHE_NAME = 'v1';
const STATIC_ASSETS = ['/', '/index.html', '/style.css', '/app.js', '/offline.html'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(STATIC_ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
  ));
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request)
      .then(r => { if (r.ok) caches.open(CACHE_NAME).then(c => c.put(e.request, r.clone())); return r; })
      .catch(() => caches.match('/offline.html'))
    )
  );
});
```

---

## Offline Strategy Table

| Strategy | Khi dùng | Ví dụ |
|----------|----------|--------|
| **Cache-First** | Static assets, fonts, images | `style.css`, `font.woff2` |
| **Network-First** | API calls, dynamic content | `/api/data` |
| **Stale-While-Revalidate** | Fresh + cached cần cả hai | News feed |
| **Cache-Only** | Pre-cached offline resources | `offline.html` |
| **Network-Only** | Non-cacheable | Analytics |

---

## PWA

### Requirements

| Yêu cầu | Bắt buộc |
|---------|---------|
| HTTPS | Có (trừ localhost) |
| Web App Manifest | name, icons, start_url |
| Service Worker | Cache + offline |
| Installable | "Add to Home Screen" |

### Manifest

```json
{
  "name": "My PWA",
  "short_name": "MyApp",
  "start_url": "/",
  "display": "standalone",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

### PWA vs Native

| | PWA | Native |
|--|-----|--------|
| Install | From browser | App store |
| Offline | Có | Có |
| Push Notification | Có | Có |
| File System | Hạn chế | Full access |
| Update | Tự động | Cần approve |
| Dev cost | **Thấp hơn** | Cao hơn |

---

## Push Notification

```javascript
// Request permission
await Notification.requestPermission();

// Subscribe
const reg = await navigator.serviceWorker.ready;
const sub = await reg.pushManager.subscribe({
  userVisibleOnly: true,
  applicationServerKey: vapidPublicKey
});

// sw.js
self.addEventListener('push', (e) => {
  const data = e.data.json();
  e.waitUntil(self.registration.showNotification(data.title, {
    body: data.body, icon: '/icon.png'
  }));
});
```

---

## Background Sync

```javascript
// Register sync
await reg.sync.register('sync-new-posts');

// sw.js
self.addEventListener('sync', (e) => {
  if (e.tag === 'sync-new-posts') e.waitUntil(syncPendingPosts());
});
```

---

## Debug SW

| Tool | Cách dùng |
|------|-----------|
| Application Tab | SW section → inspect, update, unregister |
| Network Tab | "from Service Worker" trong Size column |
| Lighthouse | PWA audit |

```javascript
// Update: increment version
const CACHE_NAME = 'v2'; // Browser check SW file mỗi 24h hoặc khi reload
```

---

**Xem thêm:** [Web Storage](13-web-storage.md) | [Browser Cache](12-browser-cache.md) | [WebSocket & SSE](15-websocket-sse.md)