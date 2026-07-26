---
title: Browser & Chrome DevTools — Tổng Quan
description: "Lộ trình 36 files: kiến trúc trình duyệt, rendering pipeline, DevTools, automation, reverse engineering"
tags: [browser, chrome-devtools, rendering-engine, event-loop, web-security, web-performance]
category: developer
updated: 2026-07-26
order: 0
---

# Browser & Chrome DevTools — Tổng Quan

---

## Bản chất

Browser = **multi-process OS mini**. Mỗi tab = 1 renderer process. Rendering pipeline biến HTML/CSS/JS thành pixels. DevTools là interface trực tiếp vào mọi layer bên trong.

---

## Lộ trình

```text
Phần 1: NỀN TẢNG (01-07)
  Architecture → Rendering Engine → JS Engine (V8)
  → Rendering Pipeline → DOM/CSSOM → Layout/Paint/Composite → Event Loop

Phần 2: MẠNG & LƯU TRỮ (08-16)
  Web APIs → Networking → HTTP → HTTP/2 & 3
  → Cache → Storage → Service Worker/PWA → WebSocket/SSE → Wasm

Phần 3: BẢO MẬT (17-18)
  SOP/CORS/CSP → XSS/CSRF

Phần 4: DEVTOOLS (19-27)
  Elements → Network → Sources → Performance
  → Memory → Application → Lighthouse → CDP

Phần 5: AUTOMATION & RE (28-32)
  Puppeteer/Playwright → Browser Automation
  → Reverse Engineering → Scraping → Anti-bot

Phần 6: THỰC HÀNH (33-35)
  Performance Optimization → Debugging → Case Studies
```

---

## Đọc theo thứ tự nào

| Nhu cầu | Đọc bắt đầu từ |
|---------|----------------|
| Hiểu browser hoạt động thế nào | 01 → 07 |
| Debug frontend | 19 → 22 → 34 |
| Phân tích API website | 21 → 30 → 31 |
| Tối ưu performance | 23 → 26 → 33 |
| Automation/scraping | 28 → 29 → 31 → 32 |
| Browser security | 17 → 18 |
| Chrome Extension | 01 → 17 → 19 → [browser-extensions](/developer/browser-extensions/browser-extension-overview) |

---

## Files nhanh

| # | File | Ngắn gọn |
|---|------|----------|
| 01 | [Architecture](01-browser-architecture) | Multi-process: Browser, Renderer, GPU, Network |
| 02 | [Rendering Engine](02-rendering-engine) | Blink/WebKit/Gecko — parse HTML/CSS |
| 03 | [JS Engine](03-javascript-engine) | V8: Ignition → Sparkplug → TurboFan + GC |
| 04 | [Rendering Pipeline](04-rendering-pipeline) | Parse → DOM → CSSOM → RenderTree → Layout → Paint → Composite |
| 05 | [DOM/CSSOM](05-dom-cssom) | Tree structure, reflow vs repaint |
| 06 | [Layout/Paint/Composite](06-layout-paint-composite) | GPU-accelerated properties, layer splitting |
| 07 | [Event Loop](07-event-loop) | Call stack, microtask > macrotask, rAF |
| 08 | [Web APIs](08-web-apis) | Fetch, Observer, Worker, Clipboard, Geolocation |
| 09 | [Networking](09-networking) | DNS → TCP → TLS → HTTP, connection pooling |
| 10 | [HTTP Lifecycle](10-http-lifecycle) | URL enter → render, HSTS, cache check |
| 11 | [HTTP/2 & 3](11-http2-http3) | Multiplexing, QUIC, 0-RTT, no HOL blocking |
| 12 | [Browser Cache](12-browser-cache) | HTTP cache, memory cache, stale-while-revalidate |
| 13 | [Web Storage](13-web-storage) | Cookie vs localStorage vs IndexedDB vs Cache API |
| 14 | [SW & PWA](14-service-worker-pwa) | Offline-first, push, manifest, installable |
| 15 | [WebSocket & SSE](15-websocket-sse) | Full-duplex vs one-way streaming |
| 16 | [WebAssembly](16-webassembly) | Wasm bytecode, near-native speed, WASI |
| 17 | [Browser Security](17-browser-security) | SOP, CORS, CSP, Permissions Policy |
| 18 | [XSS & CSRF](18-xss-csrf) | Stored/DOM/Reflected XSS, CSRF token, SameSite |
| 19 | [DevTools Overview](19-chrome-devtools) | All panels, shortcuts, command menu |
| 20 | [Elements Panel](20-devtools-elements) | DOM inspector, CSS editor, box model |
| 21 | [Network Panel](21-devtools-network) | Waterfall, timing, filter, copy as cURL |
| 22 | [Sources Panel](22-devtools-sources) | Breakpoint, step-through, call stack, scope |
| 23 | [Performance Panel](23-devtools-performance) | Flame chart, FPS, CPU, long tasks |
| 24 | [Memory Panel](24-devtools-memory) | Heap snapshot, detached nodes, leak detection |
| 25 | [Application Panel](25-devtools-application) | Storage, SW, cache, manifest |
| 26 | [Lighthouse](26-lighthouse) | Core Web Vitals, audit categories, budget |
| 27 | [CDP](27-cdp) | Chrome DevTools Protocol, WebSocket JSON-RPC |
| 28 | [Puppeteer/Playwright](28-puppeteer-playwright) | Headless browser, auto-wait, multi-browser |
| 29 | [Browser Automation](29-browser-automation) | Patterns: POM, retry, anti-detection, parallel |
| 30 | [Reverse Engineering](30-reverse-engineering) | Detect framework, find API, auth flow |
| 31 | [Web Scraping](31-web-scraping) | HTTP vs headless vs API, crawl strategy |
| 32 | [Anti-bot](32-anti-bot) | Fingerprinting, CAPTCHA, rate limit, behavioral |
| 33 | [Performance Opt](33-performance-optimization) | Core Web Vitals, lazy load, code split, cache |
| 34 | [Debugging Guide](34-debugging-guide) | Reproduce → isolate → fix, common patterns |
| 35 | [Case Studies](35-case-studies) | E-commerce, SPA, SaaS analysis framework |

---

## Liên kết

| Topic liên quan | Liên kết |
|----------------|---------|
| Browser Extension | [browser-extensions](/developer/browser-extensions/browser-extension-overview) |
| Performance Frontend | [performance-front-end](/developer/performance/performance-front-end) |
| Network cơ bản | [network-internet](/computer/network-internet/network-internet-co-ban) |