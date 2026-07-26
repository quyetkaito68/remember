---
title: Kiến Trúc Trình Duyệt Hiện Đại
description: "Kiến trúc multi-process của browser hiện đại — Browser Process, Renderer Process, GPU Process, Network Process và cách chúng giao tiếp"
tags: [browser-architecture, multi-process, chromium, browser-process, renderer-process]
category: developer
updated: 2026-07-26
order: 1
---

# Kiến Trúc Trình Duyệt Hiện Đại

Multi-process architecture: mỗi tab/iframe chạy trong process riêng → ổn định, bảo mật, hiệu năng.

---

## Kiến trúc tổng quan

```text
┌──────────────────────────────────────────────────────────────────┐
│                        BROWSER PROCESS                           │
│                   (Process chính, 1 duy nhất)                    │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │    UI Thread │  │   Network    │  │   Storage Manager      │  │
│  │  (Chrome UI) │  │   Service    │  │                        │  │
│  └──────────────┘  └──────────────┘  └────────────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │  Browser     │  │   Drawing    │  │   Process Launcher     │  │
│  │  Thread      │  │   Manager    │  │                        │  │
│  └──────────────┘  └──────────────┘  └────────────────────────┘  │
└──────────────────────────────┬───────────────────────────────────┘
                               │ IPC
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐
│  RENDERER PROCESS  │ │  RENDERER PROCESS  │ │    GPU PROCESS     │
│     (Tab 1)        │ │     (Tab 2)        │ │                    │
│    Blink + V8      │ │    Blink + V8      │ │    WebGL, Canvas   │
└────────────────────┘ └────────────────────┘ └────────────────────┘
              │                                          ▲
              └──────── IPC ─────────────────────────────┘
```

---

## Các Process chính

### Browser Process (1 duy nhất)

| Thành phần | Chức năng |
|------------|-----------|
| **UI Thread** | Vẽ title bar, thanh địa chỉ, nút back/forward, quản lý tab |
| **Network Thread** | Xử lý tất cả network request (fetch, XHR, image) |
| **Storage Thread** | Quản lý cookie, cache, IndexedDB |
| **Process Launcher** | Tạo và quản lý Renderer Process |
| **Drawing Manager** | Điều phối Renderer Process vẽ lên GPU |

> Network Thread **không chạy JavaScript**. JS chỉ chạy trong Renderer Process.

### Renderer Process (mỗi tab 1 process)

```text
┌─────────────── RENDERER PROCESS ───────────────┐
│                                                │
│  ┌─────────────── Main Thread ───────────────┐ │
│  │  HTML Parser → DOM                        │ │
│  │  CSS Parser → CSSOM                       │ │
│  │  JavaScript (V8)                          │ │
│  │  Style Calculation                        │ │
│  │  Layout → Paint                           │ │
│  └───────────────────────────────────────────┘ │
│                                                │
│  ┌─────────── Compositor Thread ─────────────┐ │
│  │  Tách layer, handle input (scroll, click) │ │
│  └───────────────────────────────────────────┘ │
│                                                │
│  ┌─────────── Raster Worker Pool ────────────┐ │
│  │  Vẽ tile → bitmap pixels                  │ │
│  └───────────────────────────────────────────┘ │
└────────────────────────────────────────────────┘
```

### GPU Process (1 duy nhất)

| Chức năng | Chi tiết |
|-----------|----------|
| WebGL rendering | Canvas 2D, WebGL, WebGPU |
| Composite layers | Ghép các layer từ Renderer Process |
| Hardware acceleration | Tận dụng GPU để tăng tốc vẽ |

### Network Process (từ Chrome 99)

Trước Chrome 99, Network Thread chạy trong Browser Process. Từ Chrome 99 → tách riêng vì lý do security/stability.

---

## Site Isolation

Mỗi **origin** (protocol + domain + port) chạy trong Renderer Process riêng.

```text
┌─────────────── MAIN TAB ──────────────────┐
│  Renderer Process (https://example.com)   │
│                                           │
│  <iframe src="https://ads.tracker.com">   │
│         │                                 │
│         ▼ (tách process riêng)            │
│  ┌─────────────────────────────────┐      │
│  │ Renderer Process (ads.tracker)  │      │
│  └─────────────────────────────────┘      │
│                                           │
│  <iframe src="https://payment.bank.com">  │
│         │                                 │
│         ▼ (tách process riêng)            │
│  ┌─────────────────────────────────┐      │
│  │ Renderer Process (payment.bank) │      │
│  └─────────────────────────────────┘      │
└───────────────────────────────────────────┘
```

| Tính năng | Giải thích |
|-----------|-----------|
| Cross-origin iframes | iframe từ domain khác → process riêng |
| Spectre mitigation | Ngăn side-channel attack đọc memory cross-origin |
| Performance trade-off | Nhiều process hơn → tốn RAM hơn → nhưng bảo mật hơn |

---

## IPC (Inter-Process Communication)

```text
Browser Process ◄──── Mojo (IPC) ────► Renderer Process
                          │
                          ▼
                     GPU Process
```

| Cặp giao tiếp | Ví dụ |
|---------------|--------|
| Browser → Renderer | Navigate URL, resize window, focus tab |
| Renderer → Browser | Title changed, URL changed, request permission |
| Renderer → GPU | Draw commands, composite layers |
| Browser → Network | Start fetch, abort request, set cookie |

---

## Memory

| Hạng mục | Giá trị |
|----------|---------|
| Browser Process | ~50-100 MB |
| Renderer Process (tab trống) | ~30-50 MB |
| Renderer Process (tab nặng) | ~200-500 MB |
| GPU Process | ~50-100 MB |
| Tổng (10 tab bình thường) | ~500 MB - 1 GB |

---

## Multi-Process Tradeoff

|  | Single-Process | Multi-Process |
|--|---------------|---------------|
| Tab crash | Crash toàn bộ browser | Chỉ crash tab đó |
| Security | Tab đọc được memory tab khác | Sandbox cô lập |
| Performance | Một tab busy làm chậm hết | Tab khác vẫn mượt |
| Memory | Chia sẻ, tiết kiệm RAM | Mỗi process riêng, tốn hơn |
| Complexity | Đơn giản | Phức tạp hơn, cần IPC |

---

## Renderer Process Lifecycle

```text
1. User nhập URL → Browser Process
2. Browser Process kiểm tra process đã tồn tại chưa?
   ├── Có → Gửi IPC "navigate" đến Renderer Process hiện tại
   └── Không → Tạo Renderer Process mới
3. Renderer Process mới bắt đầu parse HTML
4. Khi user chuyển tab → Renderer Process pause render
5. Khi user tắt tab → Browser Process terminates Renderer Process
6. Khi browser tắt → Tất cả Renderer Process bị kill
```

---

## Chromium vs Firefox vs Safari

| Tính năng | Chromium | Firefox | Safari |
|-----------|----------|---------|--------|
| Rendering Engine | Blink | Gecko | WebKit |
| JS Engine | V8 | SpiderMonkey | JavaScriptCore |
| Kiến trúc | Multi-process (site isolation) | Multi-process (Fission) | Multi-process |
| Site Isolation | Mặc định từ Chrome 67 | Mặc định từ Firefox 97 | Có |
| IPC | Mojo | ContentProcess IPC | XPC |

---

**Xem thêm:** [Rendering Engine](02-rendering-engine.md) | [JavaScript Engine](03-javascript-engine.md) | [Rendering Pipeline](04-rendering-pipeline.md) | [Event Loop](07-event-loop.md)