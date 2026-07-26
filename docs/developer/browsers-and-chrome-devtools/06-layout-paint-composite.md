---
title: Layout, Paint & Composite
description: "Layout, Paint và Composite — ba giai đoạn cuối của rendering pipeline: tính toán vị trí, vẽ pixels và ghép layers để hiển thị lên màn hình"
tags: [layout, paint, composite, gpu-acceleration, layer, reflow, repaint]
category: developer
updated: 2026-07-26
order: 6
---

# Layout, Paint & Composite

Render Tree → Layout (tính vị trí) → Paint (vẽ pixels) → Composite (ghép layers → screen).

---

## Pipeline Cost Summary

```text
Complete Pipeline:

  HTML ──▶ Parse ──▶ DOM ──┐
                           ├─▶ Render Tree ──▶ Layout ──▶ Paint ──▶ Composite ──▶ Screen
  CSS  ──▶ Parse ──▶ CSSOM ┘

  Cost:     Low    Medium     HIGH    Low       Low      LOWEST
```

| Stage | Cost | DevTools Check |
|-------|------|----------------|
| Layout | **HIGH** | Performance → Layout |
| Paint | Low-Medium | Performance → Paint |
| Composite | **LOWEST** | Performance → Composite Layers |

---

## Layout (Reflow)

### Reflow Cascade

```text
Thay đổi width của div.container:

div.container (reflow)
├── div.header (reflow — vì width thay đổi)
│   ├── h1 (reflow)
│   └── nav (reflow)
├── div.content (reflow — vì width thay đổi)
│   ├── p (reflow)
│   └── img (reflow)
└── div.footer (reflow — vì width thay đổi)
```

### Layout Cost

| Hạng mục | Chi phí |
|----------|---------|
| Thêm 1 element đơn giản | Thấp |
| Thay đổi 1 text node | Thấp (nếu không thay đổi size) |
| Thay đổi width/height element gốc | **Cao** (reflow cascade) |
| Thay đổi position (absolute/fixed) | **Cao** |
| Thay đổi font-size | **Cao** (text reflow toàn bộ) |
| Thay đổi CSS property không ảnh hưởng layout | **Không có layout** |

### Properties gây Reflow

| Gây Reflow | Không gây Reflow |
|-----------|-------------------|
| width, height | color |
| margin, padding | visibility |
| border-width | background |
| position, float | box-shadow |
| display | opacity |
| font-size | **transform** |
| overflow | transition |

---

## Paint

### Paint Order (back to front)

```text
1. Background color / image
2. Border
3. Content (text, images)
4. Outline
5. Pseudo-elements (::before, ::after)
6. Overlay (scrollbar, selection)
```

### Paint vs Layout Properties

| Paint Property (chỉ repaint) | Layout Property (reflow + repaint) |
|------------------------------|-----------------------------------|
| color | width, height |
| background-color | margin, padding |
| visibility | border-width |
| box-shadow | position, float |
| opacity | display |
| outline | overflow |
| text-decoration | font-size |

---

## Composite — Layer & GPU

### Layer Diagram

```text
Layer 1 (z-index: 1):   Page content
Layer 2 (z-index: 2):   Fixed navigation bar
Layer 3 (z-index: 3):   Modal overlay
Layer 4 (z-index: 4):   Popup tooltip

GPU Composite:
  Draw Layer 1 → Screen buffer
  Draw Layer 2 → Screen buffer (trên Layer 1)
  Draw Layer 3 → Screen buffer (trên Layer 2)
  Draw Layer 4 → Screen buffer (trên Layer 3)
```

### Layer Promotion Rules

| Trigger | Ví dụ | Tách layer? |
|---------|-------|------------|
| `position: fixed` | Fixed header, modal | **Yes** |
| `will-change: transform` | Animation transform | **Yes** |
| `transform` (non-none) | `translateX()`, `rotate()` | **Yes** |
| `opacity` (animation) | Fade in/out | **Yes** |
| `<video>`, `<canvas>`, `<iframe>` | Media elements | **Yes** |
| CSS filter (animation) | Blur, brightness animation | **Yes** |
| 3D transform | `perspective`, `rotateZ()` | **Yes** |

### GPU-Accelerated Properties

| GPU-Accelerated | NOT GPU-Accelerated |
|----------------|---------------------|
| transform | width, height |
| opacity | margin, padding |
| filter | top, left, right, bottom |
| clip-path | font-size |
| will-change | color, background |

### CPU vs GPU Animation Cost

```text
animation bằng top/left (CPU):
  top: 0px → top: 100px
  → Trigger layout → repaint → composite
  → Chi phí CAO

animation bằng transform (GPU):
  transform: translateY(0) → translateY(100px)
  → KHÔNG trigger layout → KHÔNG repaint → chỉ composite
  → Chi phí THẤP
```

### GPU Compositing Flow

```text
┌──────────────────────────────────────────────┐
│                CPU (Main Thread)             │
│                                              │
│  Layout → Paint → Create Display Lists       │
│                           │                  │
│                           ▼                  │
│              Send Display Lists to GPU       │
└───────────────────────────┼──────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────┐
│                GPU Process                   │
│                                              │
│  Receive layers from all Renderer Processes  │
│                           │                  │
│                           ▼                  │
│  Composite layers (transforms, blend modes)  │
│                           │                  │
│                           ▼                  │
│  Output pixels to screen                     │
└──────────────────────────────────────────────┘
```

---

## Performance Pitfalls

### Forced Synchronous Layout

```javascript
// BAD — Forced synchronous layout
element.style.width = '100px';
console.log(element.offsetWidth); // Forces layout!

// GOOD — Batch reads first, then writes
const width = element.offsetWidth;   // Read
element.style.width = `${width + 10}px`; // Write
```

### Layout Thrashing

```javascript
// BAD — Layout thrashing
const elements = document.querySelectorAll('div');
elements.forEach(el => {
  el.style.height = `${el.offsetWidth + 10}px`; // Layout per element!
});

// GOOD — Single layout
const heights = Array.from(elements).map(el => el.offsetWidth + 10);
elements.forEach((el, i) => {
  el.style.height = `${heights[i]}px`;
});
```

### Paint Storm

```javascript
// BAD — Paint every frame
function animate() {
  element.style.boxShadow = `0 0 ${random}px red`;
  requestAnimationFrame(animate);
}

// GOOD — Use transform (GPU-accelerated)
function animate() {
  element.style.transform = `translateX(${random}px)`;
  requestAnimationFrame(animate);
}
```

---

**Xem thêm:** [Rendering Pipeline](04-rendering-pipeline.md) | [DOM & CSSOM](05-dom-cssom.md) | [Performance Panel](23-devtools-performance.md)