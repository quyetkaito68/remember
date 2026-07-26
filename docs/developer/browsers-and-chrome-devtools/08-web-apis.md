---
title: Web APIs
description: "Web APIs và Browser APIs — các API mà browser cung cấp cho JavaScript: DOM API, Fetch API, Storage, Animation, Observer, và nhiều hơn nữa"
tags: [web-api, browser-api, fetch-api, dom-api, observer, web-animation]
category: developer
updated: 2026-07-26
order: 8
---

# Web APIs

Các API browser cung cấp cho JS, không phải parte của ECMAScript spec. Chúng cho phép JS tương tác với DOM, network, storage, media.

---

## Web APIs vs JavaScript Core

| JavaScript Core (ECMAScript) | Web APIs (Browser) |
|-----------------------------|--------------------|
| `let`, `const`, `var` | `document.querySelector()` |
| `function`, `class` | `fetch()` |
| `Promise`, `async/await` | `setTimeout()`, `setInterval()` |
| `Array`, `Map`, `Set` | `localStorage`, `sessionStorage` |
| `JSON.parse/stringify` | `navigator.geolocation` |
| `RegExp` | `WebSocket` |

> **Lưu ý:** `fetch()`, `setTimeout()`, `Promise` là Web APIs, KHÔNG phải parte của JavaScript core. Node.js không có chúng (hoặc implement khác).

---

## Phân loại Web APIs

### DOM APIs

| API | Dùng khi |
|-----|---------|
| `querySelector/createElement` | Query/tạo element |
| `addEventListener` | Đăng ký event |
| `classList/dataset` | Thao tác class + data attributes |
| `IntersectionObserver` | Detect element visibility (lazy loading) |
| `MutationObserver` | Detect DOM changes |
| `ResizeObserver` | Detect element resize |
| `requestAnimationFrame` | Schedule animation frame |

### Network APIs

| API | Dùng khi |
|-----|---------|
| `fetch()` | HTTP request (thay XMLHttpRequest) |
| `XMLHttpRequest` | HTTP request (legacy) |
| `WebSocket` | Full-duplex real-time |
| `EventSource` | Server-Sent Events (SSE) |
| `navigator.onLine` | Check online/offline |

### Storage APIs

| API | Scope | Capacity |
|-----|-------|----------|
| `localStorage` | Persistent, origin-scoped | ~5-10MB |
| `sessionStorage` | Tab-scoped | ~5-10MB |
| `IndexedDB` | Persistent, structured DB | ~hundreds MB |
| `Cache API` | Service Worker only | configurable |

### Media APIs

| API | Dùng khi |
|-----|---------|
| `MediaRecorder` | Record audio/video |
| `HTMLVideoElement` | Control video playback |
| `Web Audio API` | Process audio |
| `WebRTC` | Peer-to-peer communication |

### Animation & Observer APIs

| API | Dùng khi |
|-----|---------|
| `requestAnimationFrame` | Animation 60fps |
| `Element.animate()` | Web Animations API |
| `IntersectionObserver` | Lazy loading, infinite scroll |
| `MutationObserver` | Watch DOM changes |
| `ResizeObserver` | Responsive layout |

### Security & Worker APIs

| API | Dùng khi |
|-----|---------|
| `crypto.subtle` | Cryptographic operations |
| `Trusted Types` | Prevent DOM XSS |
| `Worker` | Background thread (dedicated) |
| `SharedWorker` | Multi-tab shared thread |
| `Service Worker` | Offline, push notification, background sync |

---

## Fetch API

```javascript
// GET
const response = await fetch('https://api.example.com/data');
const data = await response.json();

// POST
const response = await fetch('https://api.example.com/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'John', age: 30 })
});

// Error handling
try {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = await response.json();
} catch (error) {
  console.error('Fetch failed:', error);
}
```

| Response Property | Mô tả |
|-------------------|--------|
| `response.ok` | `true` nếu status 200-299 |
| `response.status` | HTTP status code |
| `response.headers` | Response headers |
| `response.body` | ReadableStream |
| `response.json()` | Parse JSON |
| `response.text()` | Parse text |
| `response.blob()` | Parse binary |

---

## Observer APIs — Code Examples

```javascript
// IntersectionObserver — lazy loading
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      console.log('Element visible:', entry.target);
    }
  });
}, { threshold: 0.5 });
observer.observe(document.querySelector('.my-element'));
```

```javascript
// MutationObserver — watch DOM
const observer = new MutationObserver((mutations) => {
  mutations.forEach(mutation => console.log('DOM changed:', mutation.type));
});
observer.observe(document.body, { childList: true, subtree: true, attributes: true });
```

```javascript
// ResizeObserver — responsive layout
const observer = new ResizeObserver(entries => {
  entries.forEach(entry => {
    console.log('Size:', entry.contentRect.width, entry.contentRect.height);
  });
});
observer.observe(document.querySelector('.container'));
```

---

## Web Workers

```javascript
// main.js
const worker = new Worker('worker.js');
worker.postMessage({ data: largeArray });
worker.onmessage = (event) => console.log('Result:', event.data);

// worker.js
self.onmessage = (event) => {
  const result = heavyComputation(event.data);
  self.postMessage(result);
};
```

| Loại Worker | Dùng khi |
|-------------|---------|
| **Dedicated Worker** | `new Worker()` — 1 script dùng riêng |
| **Shared Worker** | Nhiều tab chung 1 worker |
| **Service Worker** | Offline, push notification, background sync |

---

## Performance APIs

| API | Mô tả |
|-----|--------|
| `performance.now()` | High-resolution timestamp |
| `PerformanceObserver` | Monitor performance entries |
| `LargestContentfulPaint` | Measure LCP |
| `FirstInputDelay` | Measure FID |
| `NavigationTiming` | Page load timing |

```javascript
window.addEventListener('load', () => {
  const timing = performance.getEntriesByType('navigation')[0];
  console.log('DNS:', timing.domainLookupEnd - timing.domainLookupStart);
  console.log('TCP:', timing.connectEnd - timing.connectStart);
  console.log('TTFB:', timing.responseStart - timing.requestStart);
  console.log('Load:', timing.loadEventEnd - timing.startTime);
});
```

---

## Quick Reference by Use Case

| Use Case | API cần dùng |
|----------|-------------|
| Lazy loading images | `IntersectionObserver` |
| Infinite scroll | `IntersectionObserver` + `fetch` |
| Real-time updates | `WebSocket` hoặc `EventSource` |
| Background computation | `Worker` |
| Offline-first app | `Service Worker` + `Cache API` |
| Copy/paste | `navigator.clipboard` |
| User location | `navigator.geolocation` |
| Push notifications | `Service Worker` + `Notification API` |
| Local data | `localStorage` / `IndexedDB` |
| Animation | `requestAnimationFrame` / `Element.animate()` |
| DOM change detection | `MutationObserver` |
| Element size tracking | `ResizeObserver` |

---

Xem thêm: [Event Loop](07-event-loop.md) | [Networking](09-networking.md) | [Web Storage](13-web-storage.md)