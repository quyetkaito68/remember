---
title: Sources Panel & Debugging
description: "Sources Panel trong Chrome DevTools — breakpoint, conditional breakpoint, logpoint, call stack, scope, watch expressions, debugger"
tags: [sources-panel, devtools, breakpoint, debugger, call-stack, step-through]
category: developer
updated: 2026-07-26
order: 22
---

# Sources Panel & Debugging

Debug JavaScript — set breakpoints, step through code, inspect variables, analyze call stack.

---

## Giao diện

```text
┌─────────────────────┐ ┌─────────────────────────────────────────────┐
│  Sources Panel      │ │  app.js:42                                  │
│                     │ │  ┌────────────────────────────────────────┐ │
│  ┌───────────────┐  │ │  │ 40  function processData(data) {       │ │
│  │ File Tree     │  │ │  │ 41    const results = [];              │ │
│  │ > src         │  │ │  |>42    data.forEach(item => {           │ │
│  │   app.js      │  │ │  │ 43      results.push(transform);       │ │
│  │   utils.js    │  │ │  │ 44    });                              │ │
│  └───────────────┘  │ │  │ 45    return results;                  │ │
│                     │ │  └────────────────────────────────────────┘ │
│  ┌───────────────┐  │ │  Call Stack:                                │
│  │ Watch         │  │ │  > processData (app.js:42) < Current        │
│  │ + data        │  │ │    handleSubmit (app.js:128)                │
│  │  = [...]      │  │ │    onClick (app.js:95)                      │
│  └───────────────┘  │ │  Scope:                                     │
│                     │ │  > Local: data=[...], results=[]            │
│  Breakpoints:       │ │  > Closure: transform=function() {}         │
│  [x] app.js:42      │ │                                             │
└─────────────────────┘ └─────────────────────────────────────────────┘
```

## Breakpoint Types

| Type | Khi nào | Cách thêm |
|------|---------|-----------|
| **Line** | Mỗi lần chạy đến line | Click line number |
| **Conditional** | Condition = true | Right-click → Add conditional breakpoint |
| **Logpoint** | Log mà không pause | Right-click → Add logpoint |
| **DOM** | DOM thay đổi | Elements → Right-click → Break on |
| **XHR** | Request matching pattern | Sources → XHR Breakpoints |
| **Event Listener** | Event trigger | Sources → Event Listener Breakpoints |

---

## Debugger Controls

| Action | Shortcut |
|--------|----------|
| Continue | `F8` |
| Step Over | `F10` |
| Step Into | `F11` |
| Step Out | `Shift+F11` |
| Run to line | `Ctrl+F8` |
| Restart | `Ctrl+Shift+F5` |

```javascript
function add(a, b) {
  return a + b;      // Step Into enters here
}

function calculate() {
  const x = 10;     // Step Over: executes, stays in calculate
  const result = add(x, y);  // Step Into: enters add()
  return result;     // Step Out: back to calculate
}
```

---

## Scope Panel

| Scope | Content |
|-------|---------|
| Local | Variables trong function hiện tại |
| Closure | Variables từ parent scope |
| Global | Window/document variables |

---

## Source Maps

```text
Original source:     Source map:          Minified bundle:
app.ts      ──────>  app.js.map    ─────>  bundle.min.js
src/utils.ts ──────>                  (DevTools tu map)
```

DevTools hiển thị original TypeScript code ngay cả khi load bundle.min.js.

---

## Blackboxing

Ẩn third-party scripts khỏi debugging:

```text
Settings → Blackboxing → Add pattern
  node_modules/
  jquery.min.js
  analytics.js
```

---

## Debugging Workflow Checklist

```text
JS bug?
|
+-- 1. Set breakpoint tai error location
|     +-- Hoac dung `debugger;` statement
|
+-- 2. Reproduce -> breakpoint trigger
|
+-- 3. Kiem tra Scope panel
|     +-- Local variables gia tri dung?
|     +-- Closure variables bi stale?
|     +-- Watch expression de track
|
+-- 4. Step through (F10/F11/Shift+F11)
|     +-- Line nao gay sai logic?
|
+-- 5. Check Call Stack
|     +-- Function nao goi function nay?
|
+-- 6. Console durante pause
|     +-- Access variables
|     +-- Execute code test
|     +-- copy(data) de debug
|
+-- 7. Fix -> test -> remove breakpoint
```

---

## Tips

| Tip | Mô tả |
|-----|--------|
| `debugger;` | Manual breakpoint trong code |
| `console.trace()` | Log call stack |
| `console.time('label')` | Measure execution time |
| `monitor(fn)` | Log every function call |
| `copy(object)` | Copy to clipboard |

---

## Remote Debugging

```javascript
node --inspect app.js
// Chrome → chrome://inspect → Remote Target
```

---

Xem thêm: [Chrome DevTools Tổng Quan](19-chrome-devtools.md) | [Event Loop](07-event-loop.md) | [Performance Panel](23-devtools-performance.md)