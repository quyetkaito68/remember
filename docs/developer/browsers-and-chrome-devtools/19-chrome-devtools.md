---
title: Chrome DevTools Tổng Quan
description: "Chrome DevTools — tổng quan các panel, keyboard shortcuts, và cách sử dụng DevTools để debug, phân tích và tối ưu ứng dụng web"
tags: [chrome-devtools, devtools, debugging, developer-tools, chrome]
category: developer
updated: 2026-07-26
order: 19
---

# Chrome DevTools Tổng Quan

Chọn panel nào tùy vấn đề cần debug — Elements cho DOM/CSS, Network cho request, Sources cho JS debugging.

---

## Chọn Panel

```text
Vấn đề?
│
├── DOM/CSS sai? ──────────▶ Elements
├── API chậm/lỗi? ─────────▶ Network
├── JS bug? ───────────────▶ Sources
├── UI lag? ───────────────▶ Performance
├── Memory tăng? ──────────▶ Memory
├── Storage/SW/PWA? ───────▶ Application
└── Audit toàn diện? ──────▶ Lighthouse
```

---

## Mở DevTools

| Shortcut | Action |
|----------|--------|
| `F12` | Toggle DevTools |
| `Ctrl+Shift+I` | Toggle DevTools |
| `Ctrl+Shift+J` | Console trực tiếp |
| `Ctrl+Shift+C` | Inspect element mode |

---

## Các Panel chính

| Panel | Dùng cho | Link |
|-------|---------|------|
| **Elements** | Inspect/edit DOM, CSS real-time, box model | [→](20-devtools-elements.md) |
| **Network** | Monitor request, waterfall, timing, filter, copy as cURL | [→](21-devtools-network.md) |
| **Sources** | Debug JS: breakpoint, step-through, call stack, scope | [→](22-devtools-sources.md) |
| **Performance** | Record CPU, FPS, rendering pipeline, long tasks | [→](23-devtools-performance.md) |
| **Memory** | Heap snapshot, memory leak, detached nodes | [→](24-devtools-memory.md) |
| **Application** | Storage, Service Worker, cache, PWA manifest | [→](25-devtools-application.md) |
| **Lighthouse** | Audit performance, SEO, accessibility | [→](26-lighthouse.md) |
| **Console** | Execute JS, log, debug, `$0`, `$$()` | — |

---

## Console Commands

```text
$0                              // Selected element
$$('a')                         // querySelectorAll('a')
$0.style.color = 'red'          // Change style
copy($0.outerHTML)             // Copy to clipboard
monitorEvents($0, 'click')     // Log events
```

| Shortcut | Action |
|----------|--------|
| `Ctrl+L` | Clear console |
| `Shift+Enter` | Multi-line input |

---

## Command Menu

`Ctrl+Shift+P` — search và execute bất kỳ command nào.

```text
Command Menu:
┌───────────────────────────────────────────┐
│  > Capture screenshot                     │
│  > Run performance audit                  │
│  > Show Rendering                         │
│  > Emulate CSS media feature: prefers-    │
│    dark-color-scheme                      │
│  > Disable JavaScript                     │
│  > Network conditions                     │
└───────────────────────────────────────────┘
```

---

## Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+M` | Device mode (responsive) |
| `Ctrl+Shift+P` | Command menu |
| `Ctrl+Shift+F` | Search across all files |
| `Ctrl+O` | Open file |
| `Ctrl+G` | Go to line |

---

## Remote Debugging

```bash
chrome://inspect/#devices
chrome --remote-debugging-port=9222
```

---

## Automation

| Tool | Use |
|------|-----|
| **Puppeteer** | Node.js, dùng CDP |
| **Playwright** | Multi-browser automation |

Xem thêm: [CDP](27-cdp.md) | [Puppeteer & Playwright](28-puppeteer-playwright.md)