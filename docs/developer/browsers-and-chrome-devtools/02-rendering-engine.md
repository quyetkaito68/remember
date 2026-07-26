---
title: Rendering Engine (Blink, WebKit, Gecko)
description: "Rendering Engine — Blink, WebKit, Gecko: kiến trúc parser, flow từ HTML bytes đến DOM/CSSOM, quirks mode vs standards mode"
tags: [rendering-engine, blink, webkit, gecko, html-parser, css-parser]
category: developer
updated: 2026-07-26
order: 2
---

# Rendering Engine (Blink, WebKit, Gecko)

Rendering Engine parse HTML/CSS → tạo DOM/CSSOM → feed vào [Rendering Pipeline](04-rendering-pipeline.md).

---

## Engine Flow

```text
┌───────────────────────────────────────────────────────────┐
│                   RENDERING ENGINE                        │
│                                                           │
│  HTML Bytes ──▶ [Tokenize] ──▶ [Tree Builder] ──▶ DOM   │
│                                                           │
│  CSS  Bytes ──▶ [Tokenize] ──▶ [Tree Builder] ──▶ CSSOM │
│                                                           │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Parser Stages:                                       │ │
│  │                                                      │ │
│  │ 1. Byte Stream → Characters (decode encoding)        │ │
│  │ 2. Characters → Tokens (tokenization)                │ │
│  │ 3. Tokens → Nodes (tree construction)                │ │
│  │ 4. Nodes → DOM/CSSOM Tree                            │ │
│  └──────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

---

## HTML Parser — Preload Scanner & Speculative Parsing

```text
HTML Parser chạy 2 luồng:
┌─────────────────────┬───────────────────────────────┐
│  Main Parser Thread │  Preload Scanner (background) │
│                     │                               │
│  Parse HTML chi tiết│  Quét nhanh tìm resource:     │
│  Xây DOM tree       │  - <script src="...">         │
│  Chạy JS nếu có     │  - <link rel="stylesheet">    │
│                     │  - <img src="...">            │
│                     │  → Preload trước khi parser   │
│                     │    bị chặn bởi JS             │
└─────────────────────┴───────────────────────────────┘
```

**Script blocking behavior:**

| Tag | Blocking? | Behavior |
|-----|-----------|----------|
| `<script>` (classic) | **Yes** | Parser dừng, chờ JS execute xong |
| `<script defer>` | No | Chạy sau khi parse xong, giữ thứ tự |
| `<script async>` | No | Load xong là chạy ngay, không giữ thứ tự |
| `<link rel="stylesheet">` | **Yes** (render) | CSS must load trước khi render |

---

## Quirks Mode vs Standards Mode

Browser cần biết cách render khi HTML không có `<!DOCTYPE>`.

```text
┌──────────────────────────────────────────────────────┐
│ DOCTYPE detection:                                   │
│                                                      │
│ <!DOCTYPE html>                                      │
│     → Standards Mode (quirks: off)                   │
│                                                      │
│ <!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 ...">   │
│     → Almost Standards Mode                          │
│                                                      │
│ Không có DOCTYPE hoặc sai                            │
│     → Quirks Mode (render giống IE5.5)               │
└──────────────────────────────────────────────────────┘
```

| Mode | Hành vi | Ví dụ khác biệt |
|------|---------|-----------------|
| **Standards Mode** | Render theo spec hiện tại |盒模型 tính đúng (width = content width) |
| **Almost Standards Mode** | Gần standards, vài exception | table layout slightly khác |
| **Quirks Mode** | Backward-compatible với IE5.5 |盒模型 sai (width bao gồm padding + border) |

```css
/* Quirks vs Standards —盒模型 */
/* Standards: width = content width only */
box { width: 100px; padding: 10px; }
/* → Total width: 100px (content) + 20px (padding) = 120px */

/* Quirks: width includes padding */
box { width: 100px; padding: 10px; }
/* → Total width: 100px (content shrinks to 80px) */
```

---

## CSS Parser — Cascade & Specificity

```text
Specificity Calculation:
p           → (0, 0, 1) = 1
p.intro     → (0, 1, 1) = 11
#sidebar    → (1, 0, 0) = 100
#sidebar p  → (1, 0, 1) = 101
```

| Concept | Ý nghĩa |
|---------|---------|
| **Cascade** | author > user > browser (inline > external) |
| **Specificity** | inline(1000) > id(100) > class(10) > element(1) |
| **Inheritance** | `color`, `font-family`, `line-height` inherit; `margin`, `padding` KHÔNG |

---

## Blink vs WebKit vs Gecko

| Tính năng | Blink | WebKit | Gecko |
|-----------|-------|--------|-------|
| Dùng bởi | Chrome, Edge, Brave, Opera | Safari | Firefox |
| Fork từ | WebKit (2013) | KHTML (2001) | Original |
| HTML Parser | Blink (riêng) | WebKit parser | Gecko parser (nsHTMLContentSink) |
| CSS Parser | Blink | WebKit | Gecko (Servo components) |
| Layout Engine | LayoutNG (2019+) | Legacy layout | WebRender (partial) |
| Multi-process | Yes (site isolation) | Yes | Yes (Fission) |
| Jank-free rendering | LayoutNG (parallel) | Limited | WebRender (GPU-first) |
| DevTools Protocol | CDP | CDP (ported) | Firefox DevTools Protocol |
| Network Stack | Chromium Network Stack | NSURLSession | Necko |

---

## Parser Performance

| Vấn đề | Nguyên nhân | Giải pháp |
|--------|-------------|-----------|
| Slow HTML parse | HTML quá lớn | Code split, lazy loading |
| Slow CSS parse | Selector quá sâu, quá nhiều rule | Simplify selectors |
| Render-blocking script | `<script>` không defer/async | Dùng `defer` hoặc `async` |
| FOUC/FOUT | CSS load chậm | Inline critical CSS |
| Layout shift | Font/image load late | `font-display: swap`, set dimensions |

---

**Xem thêm:** [Browser Architecture](01-browser-architecture.md) | [Rendering Pipeline](04-rendering-pipeline.md) | [DOM & CSSOM](05-dom-cssom.md)