---
title: DOM, CSSOM & Render Tree
description: "DOM (Document Object Model), CSSOM (CSS Object Model) và Render Tree — cách trình duyệt biểu diễn và manipulated HTML/CSS thành cấu trúc tree"
tags: [dom, cssom, render-tree, document-object-model, dom-manipulation]
category: developer
updated: 2026-07-26
order: 5
---

# DOM, CSSOM & Render Tree

DOM = tree từ HTML. CSSOM = tree từ CSS. Kết hợp → Render Tree → feed vào [Layout, Paint & Composite](06-layout-paint-composite.md).

---

## DOM Tree

```text
Input HTML:
<div class="container">
  <h1>Title</h1>
  <p>Paragraph 1</p>
  <p>Paragraph 2</p>
</div>

DOM Tree:
Document
└── html (HTMLHtmlElement)
    ├── head (HTMLHeadElement)
    │   └── title (HTMLTitleElement)
    │       └── "Hello" (Text)
    └── body (HTMLBodyElement)
        └── div.container (HTMLDivElement)
            ├── h1 (HTMLHeadingElement)
            │   └── "Title" (Text)
            ├── p (HTMLParagraphElement)
            │   └── "Paragraph 1" (Text)
            └── p (HTMLParagraphElement)
                └── "Paragraph 2" (Text)
```

### Node Types

| Node Type | Ví dụ |
|-----------|-------|
| **Element Node** | `<div>`, `<p>`, `<span>` |
| **Text Node** | "Hello world" |
| **Comment Node** | `<!-- comment -->` |
| **Document Node** | `document` |
| **Document Fragment** | `document.createDocumentFragment()` |

---

## Reflow vs Repaint

| Thuật ngữ | Khi nào | Chi phí |
|-----------|---------|---------|
| **Reflow** | Thay đổi layout (size, position) | **Cao** — tính toán lại toàn bộ layout |
| **Repaint** | Thay đổi appearance (color, visibility) | **Thấp** — chỉ vẽ lại phần thay đổi |

---

## Reflow Triggers Checklist

- [ ] DOM node thêm/xóa/sửa (`appendChild`, `remove`, `innerHTML`)
- [ ] CSS layout property thay đổi (width, height, margin, padding, position, display)
- [ ] `offsetWidth`, `offsetHeight`, `getBoundingClientRect()` read
- [ ] Window resize
- [ ] Font loading hoàn thành
- [ ] Thay đổi `textContent` (có thể thay đổi size)
- [ ] Thay đổi className / classList

---

## Batch DOM Operations

```javascript
// RẤT CHẬM — forced layout thrashing
for (let i = 0; i < 100; i++) {
  const div = document.createElement('div');
  div.textContent = `Item ${i}`;
  document.body.appendChild(div);          // Reflow
  console.log(div.offsetWidth);            // Forced Reflow
}

// NHANH — batch read, then batch write
const fragment = document.createDocumentFragment();
for (let i = 0; i < 100; i++) {
  const div = document.createElement('div');
  div.textContent = `Item ${i}`;
  fragment.appendChild(div);               // No reflow yet
}
document.body.appendChild(fragment);       // Single reflow

const width = div.offsetWidth;             // Read after all writes
```

**Rule:** Separate reads from writes. Never read layout property between writes.

---

## Virtual DOM

```text
┌─────────────── Virtual DOM Flow ───────────────────┐
│                                                    │
│  State Change                                      │
│       │                                            │
│       ▼                                            │
│  Create new Virtual DOM tree                       │
│       │                                            │
│       ▼                                            │
│  Diff old vs new Virtual DOM                       │
│       │                                            │
│       ▼                                            │
│  Apply minimal patches to real DOM                 │
└────────────────────────────────────────────────────┘
```

| Framework | Virtual DOM? | Strategy |
|-----------|-------------|----------|
| React | Yes (Fiber) | Reconciliation |
| Vue 3 | Yes (Proxy-based) | Reactive dependency tracking |
| Svelte | No | Compile-time, surgical updates |
| Angular | No (Incremental DOM) | Ivy renderer |

---

## CSSOM

```text
Input CSS:
html { font-size: 16px; }
body { margin: 0; }
.container { max-width: 1200px; margin: auto; }
h1 { color: blue; }
p { color: gray; }

CSSOM Tree:
CSSStyleSheet
├── CSSRule: html { font-size: 16px; }
├── CSSRule: body { margin: 0; }
├── CSSRule: .container { max-width: 1200px; margin: auto; }
├── CSSRule: h1 { color: blue; }
└── CSSRule: p { color: gray; }
```

### Cascade & Specificity

```text
Specificity Calculation:
p           → (0, 0, 1) = 1
p.intro     → (0, 1, 1) = 11
#sidebar    → (1, 0, 0) = 100
#sidebar p  → (1, 0, 1) = 101
```

| Concept | Cách tính |
|---------|----------|
| **Cascade** | author > user > browser |
| **Specificity** | inline(1000) > id(100) > class(10) > element(1) |
| **Inheritance** | `color`, `font-family`, `line-height` inherit; `margin`, `padding` KHÔNG |

---

## Render Tree

```text
DOM Tree:                    CSSOM:
html                         html { }
├── head                     body { margin: 0 }
│   └── title                .container { padding: 20px }
├── body                     .hidden { display: none }
│   ├── div.container        p { color: blue }
│   │   ├── p "Hello"
│   │   └── p "World"
│   └── div.hidden           Render Tree:
                            └── body
                                └── div.container
                                    ├── p "Hello"  { color: blue }
                                    └── p "World"  { color: blue }
                                    // div.hidden KHÔNG có
```

| Element | DOM Tree | Render Tree |
|---------|----------|-------------|
| `<head>` | Có | **Không** |
| `display: none` | Có | **Không** |
| `visibility: hidden` | Có | **Có** (takes space) |
| `opacity: 0` | Có | **Có** (takes space, invisible) |
| Positioned off-screen | Có | **Có** (takes space) |

---

## DOM Performance Tips

```text
Lifecycle:
HTML Parser → DOM Tree ─┐
                        ├─▶ Render Tree → Layout → Paint → Composite
CSS Parser → CSSOM Tree ┘
```

| DevTools Panel | DOM-related功能 |
|----------------|----------------|
| **Elements** | Inspect, edit DOM tree real-time |
| **Performance** | Record layout/paint, identify reflow |
| **Memory** | Heap snapshot, detach DOM node detection |

```javascript
// Find detached DOM nodes (memory leak)
// DevTools → Memory → Heap Snapshot → "Detached" filter
```

---

**Xem thêm:** [Rendering Pipeline](04-rendering-pipeline.md) | [Layout, Paint & Composite](06-layout-paint-composite.md) | [Elements Panel](20-devtools-elements.md)