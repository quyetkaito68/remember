---
title: JavaScript Engine (V8)
description: "JavaScript Engine — V8, SpiderMonkey, JavaScriptCore: kiến trúc, JIT compilation, và cách JS code được execute trong trình duyệt"
tags: [javascript-engine, v8, spidermonkey, javascriptcore, jit, turbolizer]
category: developer
updated: 2026-07-26
order: 3
---

# JavaScript Engine (V8)

JS Engine parse → compile → execute JavaScript. Chạy trong [Renderer Process](01-browser-architecture.md), không phải browser.

---

## V8 Pipeline

```text
┌─────────────────────── V8 Engine ───────────────────────────┐
│                                                             │
│  JavaScript Source Code                                     │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────┐                                       │
│  │  Parser          │ ──> Abstract Syntax Tree (AST)        │
│  └────────┬─────────┘                                       │
│           ▼                                                 │
│  ┌──────────────────┐                                       │
│  │  Ignition         │ ──> Bytecode (interpreter)           │
│  │  (Interpreter)    │     Chạy ngay, không cần compile     │
│  └────────┬─────────┘                                       │
│           │ (hot function detected)                         │
│           ▼                                                 │
│  ┌──────────────────┐                                       │
│  │  Sparkplug       │ ──> Native code (baseline compiler)   │
│  │  (Baseline)      │     Compile nhanh, optimization thấp  │
│  └────────┬─────────┘                                       │
│           │ (very hot function)                             │
│           ▼                                                 │
│  ┌──────────────────┐                                       │
│  │  TurboFan        │ ──> Highly optimized native code      │
│  │  (Optimizing)    │    Deoptimize nếu assumption sai      │
│  └──────────────────┘                                       │
│                                                             │
│  ┌──────────────────┐                                       │
│  │  Orinoco (GC)    │ ──> Concurrent, incremental,          │
│  │                  │     generational garbage collection   │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## JIT Tiers

```text
     Cold Function          Hot Function        Very Hot Function
          │                      │                      │
          ▼                      ▼                      ▼
     ┌──────────┐          ┌───────────┐          ┌──────────────┐
     │ Ignition │ ──────>  │ Sparkplug │ ──────>  │   TurboFan   │
     │(bytecode)│          │(native)   │          │(optimized)   │
     └──────────┘          └───────────┘          └──────────────┘
          │                      │                      │
          │                 Deoptimize ◄────────────────┘
          └──────────────────────┘
```

| Tier | Compile Speed | Optimization | Output |
|------|--------------|--------------|--------|
| **Ignition** | Ngay lập tức | Không | Bytecode |
| **Sparkplug** | ~microseconds | Thấp (bản dịch 1-1) | Native code |
| **TurboFan** | ~milliseconds | Cao (inline caching, constant folding) | Highly optimized native |

**Deoptimization:** TurboFan assume type → nếu type sai → revert về interpreter.

```javascript
// TurboFan optimize: a, b assumed number
add(1, 2); add(3, 4);
// → generate optimized integer add

// DEOPTIMIZE — type thay đổi
add("hello", "world");
```

---

## Inline Caching (IC)

| IC State | Ý nghĩa | Performance |
|----------|---------|-------------|
| **Uninitialized** | Chưa có cached data | Chậm |
| **Monomorphic** | Chỉ gặp 1 type | Rất nhanh |
| **Polymorphic** | Gặp 2-4 types | Nhanh |
| **Megamorphic** | Gặp nhiều hơn 4 types | Chậm (fallback) |

```javascript
// Monomorphic — rất nhanh
getWidth({ width: 100 });
getWidth({ width: 200 });

// Megamorphic — chậm
for (let i = 0; i < 100; i++) {
  getWidth({ width: i, type: `type${i}` });
}
```

---

## Garbage Collection (Generational)

```text
┌─────────────── V8 Heap ─────────────────────────┐
│                                                 │
│  ┌───────────────────┐  ┌───────────────────┐   │
│  │  Young Generation │  │  Old Generation   │   │
│  │  (~1-8 MB)        │  │  (~several GB)    │   │
│  │                   │  │                   │   │
│  │  - Scavenge GC    │  │  - Mark-Sweep     │   │
│  │  - Rất nhanh      │  │  - Mark-Compact   │   │
│  │  - Chạy thường    │  │  - Chạy ít hơn    │   │
│  │                   │  │                   │   │
│  │  New objects ──── │──│──> Promoted nếu   │   │
│  │                   │  │   survive GC      │   │
│  └───────────────────┘  └───────────────────┘   │
└─────────────────────────────────────────────────┘
```

| GC Type | Khi chạy | Thuật toán | Impact |
|---------|----------|------------|--------|
| **Scavenge** | Thường xuyên | Copy surviving objects | Rất thấp |
| **Mark-Sweep-Compact** | Khi old gen đầy | Mark live → Sweep dead → Compact | Có pause |

| Loại | Đặc điểm |
|------|-----------|
| **Main Thread GC** | Dừng JS execution → gây jank |
| **Parallel GC** | Nhiều worker threads cùng mark/sweep |
| **Concurrent GC** | GC chạy song song với JS → gần như không pause |

---

## So sánh Engines

| Tính năng | V8 | SpiderMonkey | JSC |
|-----------|-----|-------------|-----|
| Browser | Chrome, Edge, Brave | Firefox | Safari |
| Interpreter | Ignition | Baseline | LLInt |
| Baseline Compiler | Sparkplug | Baseline | Baseline JIT |
| Optimizing Compiler | TurboFan | Warp | DFG + FTL |
| JIT Tiers | 3 | 2 | 3 |
| Wasm | Tốt nhất | Tốt | Tốt |
| WeakRef | Có | Có | Có |

---

## Performance Tips

- **Tránh megamorphic IC:** Giữ type ổn định trong hot path
- **Tránh deoptimization:** Không thay đổi object shape trong loop
- **Memory leak:** Check detached DOM nodes trong DevTools Memory
- **Node.js:** V8 chạy cả server-side, kiến thức apply cả hai

```javascript
// BAD — thay đổi object shape → deoptimization
const obj = { x: 1 };
obj.y = 2;  // thêm property → V8 phải re-optimize

// GOOD — giữ shape ổn định
const obj = { x: 1, y: undefined };
obj.y = 2;
```

---

**Xem thêm:** [Rendering Engine](02-rendering-engine.md) | [Rendering Pipeline](04-rendering-pipeline.md) | [Event Loop](07-event-loop.md)