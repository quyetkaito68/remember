---
title: Elements Panel
description: "Elements Panel trong Chrome DevTools — inspect, edit DOM tree, CSS styles, box model, computed styles và DOM breakpoints"
tags: [elements-panel, devtools, dom-inspector, css-editor, box-model]
category: developer
updated: 2026-07-26
order: 20
---

# Elements Panel

Inspect/edit DOM tree và CSS real-time — panel dùng nhiều nhất cho layout/styling issues.

---

## Open

| Cách | Shortcut |
|------|----------|
| DevTools → Elements tab | `F12` → click Elements |
| Inspect element | `Ctrl+Shift+C` → click element |
| Console reference | `$0` |

---

## DOM Tree View

```text
DOM Tree View:
┌──────────────────────────────────────────┐
│  ▼ <html lang="vi">                      │
│    ▼ <head>                              │
│      <meta charset="UTF-8">              │
│    ▼ </head>                             │
│    ▼ <body>                              │
│      ▼ <div id="app" class="container">  │
│        ▼ <header class="header">         │
│          <h1>Hello World</h1>            │
│        ▼ </header>                       │
│        ▼ <main>                          │
│          <p>Content</p>                  │
│        ▼ </main>                         │
│      ▼ </div>                            │
│    ▼ </body>                             │
│  ▼ </html>                               │
└──────────────────────────────────────────┘
```

### DOM Editing

| Action | Cách |
|--------|------|
| Edit text | Double-click text node |
| Edit HTML | Double-click element tag |
| Add/Delete element | Right-click → Add/Delete |
| Copy outerHTML | Right-click → Copy |

---

## Styles Panel

```text
Styles Panel:
┌──────────────────────────────────────────────┐
│  .element-styles                             │
│  ┌──────────────────────────────────────┐    │
│  │ element.style {                      │    │
│  │   color: blue;  ◄─ inline style      │    │
│  │ }                                    │    │
│  ├──────────────────────────────────────┤    │
│  │ .container {                         │    │
│  │   max-width: 1200px;                 │    │
│  │ }  ◄─ from style.css:42              │    │
│  └──────────────────────────────────────┘    │
│                                              │
│  Inherited from <div>:                       │
│  ┌──────────────────────────────────────┐    │
│  │ font-size: 16px;                     │    │
│  └──────────────────────────────────────┘    │
└──────────────────────────────────────────────┘
```

### CSS Editing

| Action | Cách |
|--------|------|
| Edit value | Click giá trị → edit |
| Add property | Click trong rule → type |
| Toggle property | Click checkbox |
| Add rule | Click `+` |
| Disable rule | Uncheck checkbox |

---

## Box Model

```text
Box Model:
┌───────────────────────────────────────┐
│              Margin                   │
│  ┌─────────────────────────────────┐  │
│  │           Border                │  │
│  │  ┌───────────────────────────┐  │  │
│  │  │        Padding            │  │  │
│  │  │  ┌─────────────────────┐  │  │  │
│  │  │  │     Content         │  │  │  │
│  │  │  │   500 x 200         │  │  │  │
│  │  │  └─────────────────────┘  │  │  │
│  │  │     20  20  20  20        │  │  │
│  │  └───────────────────────────┘  │  │
│  │     10  10  10  10              │  │
│  └─────────────────────────────────┘  │
│     0   0   0   0                     │
└───────────────────────────────────────┘
```

| Thuật ngữ | Ý nghĩa |
|-----------|---------|
| Content | width x height |
| Padding | content → border |
| Border | đường viền |
| Margin | border → element khác |

---

## DOM Breakpoints

Right-click element → Break on:

| Loại | Khi nào break |
|------|--------------|
| Subtree modifications | Element con thay đổi |
| Attributes modifications | Attribute thay đổi |
| Node removal | Element bị xóa |

---

## Search trong Elements

`Ctrl+F` trong Elements panel: selector (`.class`, `#id`), text, XPath.

---

## CSS Debugging Checklist

```text
CSS không đúng?
│
├── 1. Inspect element → Styles panel
│     ├── Có rule bị override? → Xem specificity
│     ├── Có rule bị strikethrough? → Bị overridden
│     └── Check !important
│
├── 2. Box model đúng?
│     └── Content + Padding + Border + Margin
│
├── 3. Layout sai?
│     ├── Computed tab → check final values
│     ├── Float/clear issues?
│     └── Flexbox/Grid alignment?
│
└── 4. Responsive sai?
      └── Ctrl+Shift+M → test từng breakpoint
```

---

## Tips

| Tip | Mô tả |
|-----|--------|
| `$0` | Element đang selected |
| `$0.classList.add('active')` | Thêm class |
| `$0.style.display = 'none'` | Ẩn element |
| `$0.scrollIntoView()` | Scroll đến element |
| `Ctrl+Z` / `Ctrl+Shift+Z` | Undo/Redo |

---

Xem thêm: [Chrome DevTools Tổng Quan](19-chrome-devtools.md) | [DOM & CSSOM](05-dom-cssom.md) | [Layout, Paint & Composite](06-layout-paint-composite.md)