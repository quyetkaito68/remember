---
title: Browser Rendering Pipeline
description: "Browser Rendering Pipeline — toàn bộ flow từ khi nhận HTML response đến khi pixel hiển thị trên màn hình: Parse → DOM → CSSOM → Render Tree → Layout → Paint → Composite"
tags: [rendering-pipeline, critical-rendering-path, dom, cssom, layout, paint, composite]
category: developer
updated: 2026-07-26
order: 4
---

# Browser Rendering Pipeline

HTML bytes → pixels on screen. Hiểu pipeline để tối ưu performance.

---

## Pipeline Tổng Quan

```text
┌─────────────────────────────────────────────────────────────┐
│                  RENDERING PIPELINE                         │
│                                                             │
│  HTML ──▶ [Parse] ──▶ DOM                                  │
│                            │                                │
│  CSS  ──▶ [Parse] ──▶ CSSOM                                │
│                            │                                │
│                            ▼                                │
│                     [Render Tree]                           │
│                            │                                │
│                            ▼                                │
│                     [Layout]                                │
│                  (vị trí, kích thước)                       │
│                            │                                │
│                            ▼                                │
│                     [Paint]                                 │
│                  (content, border, bg)                      │
│                            │                                │
│                            ▼                                │
│                     [Composite]                             │
│                  (ghép layers → screen)                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Timing Table

| Stage | Cost | DevTools Check |
|-------|------|----------------|
| Parse HTML/CSS | Medium | Performance → Parse HTML/CSS |
| Style Calculation | Medium | Performance → Recalculate Style |
| Layout | **HIGH** | Performance → Layout |
| Paint | Low-Medium | Performance → Paint |
| Composite | **LOWEST** | Performance → Composite Layers |

---

## Step 1: HTML Parsing

```text
Byte Stream → Characters (decode UTF-8) → Tokens → DOM Tree
```

| Blocking? | Tag | Behavior |
|-----------|-----|----------|
| **Yes** | `<script>` (classic) | Parser dừng chờ JS execute |
| No | `<script defer>` | Chạy sau khi parse xong |
| No | `<script async>` | Load xong là chạy ngay |

---

## Step 2: CSS Parsing → CSSOM

CSS là **render-blocking** — phải load và parse xong CSS mới render được.

```text
DOM Tree:                    CSSOM Tree:
html                         html { display: block }
├── head                     body { font-size: 16px }
│   └── title                div.container { color: red }
├── body                     p { margin: 10px }
│   └── div.container
│       ├── p "Hello"        Render Tree:
│       └── p "World"          div.container { color: red }
│                               p "Hello"
└── div.sidebar (hidden)       p "World"
                             // div.sidebar KHÔNG có (display: none)
```

---

## Step 3: Render Tree

Kết hợp DOM + CSSOM — chỉ chứa **visible elements**.

| DOM Node | Render Tree? | Lý do |
|----------|-------------|-------|
| `<div>` | Có | render normally |
| `display: none` | **Không** | removed from tree |
| `visibility: hidden` | Có | takes space, invisible |
| `<head>` | **Không** | not rendered |

---

## Step 4: Layout (Reflow)

Tính toán **vị trí** và **kích thước** của mỗi element.

```javascript
// Layout Thrashing — RẤT CHẬM
for (let i = 0; i < 100; i++) {
  element.style.width = `${i}px`;   // Force layout
  const w = element.offsetWidth;     // Force layout again
}

// Batch update — NHANH
element.style.width = '100px'; // Only 1 layout
const w = element.offsetWidth;
```

**Reflow triggers:**
- DOM node thêm/xóa/sửa
- CSS property: width, height, margin, padding, position, font-size
- Window resize
- Font loading

---

## Step 5: Paint

Vẽ pixels cho mỗi visible element.

| Property nhóm | Properties | Khi thay đổi |
|---------------|-----------|-------------|
| **Layout properties** | width, height, margin, padding, position, border | Reflow + Repaint |
| **Paint properties** | color, background, visibility, box-shadow, opacity | Repaint only |

---

## Step 6: Composite

```text
Layer 1 (z-index: 1):   Content layer ───────┐
Layer 2 (z-index: 2):   Fixed header ────────┤──▶ Composite ──▶ Screen
Layer 3 (z-index: 3):   Popup overlay ───────┘
```

**GPU-Accelerated Properties (chỉ composite, KHÔNG repaint):**

| Property | Tác dụng |
|----------|---------|
| `transform` | Di chuyển, xoay, scale |
| `opacity` | Thay đổi độ trong suốt |
| `will-change` | Báo hiệu browser chuẩn bị tách layer |

---

## Critical Rendering Path

```text
                    Critical Rendering Path
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    HTML (bytes)      CSS (bytes)     JS (bytes)
          │                │                │
          ▼                ▼                ▼
    HTML Parser       CSS Parser       JS Engine
          │                │                │
          ▼                ▼                │
         DOM            CSSOM               │
          │                │                │
          └────────┬───────┘                │
                   ▼                        │
              Render Tree ◄─────────────────┘
                   │
                   ▼
              First Paint
```

### Render-Blocking Resources

| Resource | Blocking? | Giải pháp |
|----------|-----------|-----------|
| `<link rel="stylesheet">` | **Yes** (CSS) | Inline critical CSS |
| `<script>` (classic) | **Yes** (HTML) | Dùng `defer` hoặc `async` |
| `<script defer>` | No | Run after HTML parse |
| `<script async>` | No | Run as soon as loaded |
| `<link rel="preload">` | No |提前 load, không render |

---

## Performance Bottlenecks

| Bottle Neck | Triệu chứng | Giải pháp |
|-------------|-------------|-----------|
| Slow HTML parse | Large document | Code split, lazy load |
| Slow CSS parse | Many rules, deep selectors | Simplify selectors |
| Layout thrashing | Janky scrolling | Batch DOM reads/writes |
| Excessive repaints | Flickering | Use `transform`, avoid `box-shadow` animation |
| Large layers | Memory pressure | Avoid large `will-change`, use `contain` |

---

## CLS (Cumulative Layout Shift)

| Nguyên nhân CLS | Giải pháp |
|-----------------|-----------|
| Image không có width/height | Always set explicit dimensions |
| Dynamic content chèn phía trên | Reserve space with skeleton/placeholder |
| Web font FOUT | Use `font-display: swap` + preload font |
| Ads/embed thay đổi size | Set min-height |

---

**Xem thêm:** [DOM & CSSOM](05-dom-cssom.md) | [Layout, Paint & Composite](06-layout-paint-composite.md) | [Performance Panel](23-devtools-performance.md)