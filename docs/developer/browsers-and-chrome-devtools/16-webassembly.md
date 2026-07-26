---
title: WebAssembly
description: "WebAssembly (Wasm) — ngôn ngữ bytecode chạy trong browser với hiệu năng gần native, hỗ trợ đa ngôn ngữ (C, C++, Rust, Go)"
tags: [webassembly, wasm, wasm-modules, simd, multithreading]
category: developer
updated: 2026-07-26
order: 16
---

# WebAssembly

Wasm bổ sung JavaScript ở layer hiệu năng — bytecode compact chạy gần native speed, compile từ C/C++/Rust/Go.

---

## Architecture

```text
┌──────────────────────────────────────────────────────┐
│                  BROWSER                             │
│  ┌──────────────────┐    ┌─────────────────────────┐ │
│  │  JavaScript      │    │  WebAssembly            │ │
│  │  (V8 Engine)     │    │  (Wasm VM)              │ │
│  │  - DOM, Network  │    │  - Image/Video process  │ │
│  │  - UI, Business  │    │  - Physics, Crypto      │ │
│  └──────────────────┘    └─────────────────────────┘ │
│           JavaScript ◄═════════► WebAssembly         │
└──────────────────────────────────────────────────────┘
```

---

## JS vs Wasm

| | JavaScript | WebAssembly |
|--|-----------|-------------|
| Execution speed | ~30-50% native | **~85-95% native** |
| Startup time | Parse + JIT | **Instant** (bytecode) |
| Memory | GC (unpredictable) | **Manual** (predictable) |
| Multithreading | Single-threaded | **SharedArrayBuffer** |
| Type safety | Dynamic | **Static** (compile-time) |

---

## Decision Tree: Dùng Wasm hay JS?

```text
Performance-critical?
│
├─ Không → JavaScript
│
├─ Có, và thuộc loại nào?
│  ├─ Image/video processing → Wasm
│  ├─ Game engine / physics → Wasm
│  ├─ CAD/3D rendering → Wasm
│  ├─ Cryptography → Wasm
│  ├─ Audio processing → Wasm
│  ├─ Simple DOM manipulation → JS
│  ├─ CRUD apps → JS
│  └─ Form validation → JS
│
└─ Porting existing C/C++/Rust codebase → Wasm
```

---

## Module Structure

```text
WebAssembly Module (.wasm)
├── Types       (function signatures)
├── Imports     (from JS)
├── Exports     (to JS)
├── Functions   (compiled code)
├── Memories    (linear memory)
├── Tables      (function references)
└── Globals     (global variables)
```

```javascript
const { instance } = await WebAssembly.instantiate(
  await (await fetch('/module.wasm')).arrayBuffer()
);
const result = instance.exports.add(1, 2); // 3
```

---

## Compile Pipeline

```text
Source Code (C/Rust/Go)
        │
        ▼
┌──────────────────┐
│  LLVM / Compiler │ ──▶ .wasm (binary)
└──────────────────┘
        │
        ▼
  Browser loads + instantiates
```

| Source | Tool | Command |
|--------|------|---------|
| C/C++ | Emscripten | `emcc main.c -o main.js -s WASM=1` |
| Rust | wasm-pack | `wasm-pack build --target web` |

---

## Memory

```javascript
const memory = new WebAssembly.Memory({
  initial: 1,    // 64KB
  maximum: 100   // 6.4MB
});
const view = new Uint8Array(memory.buffer);
view[0] = 42;
```

## Multithreading

```javascript
const memory = new WebAssembly.Memory({
  initial: 1, maximum: 100, shared: true // SharedArrayBuffer
});
const worker1 = new Worker('worker.js');
worker1.postMessage({ memory, id: 1 });
```

---

## WASI (ngoài browser)

```text
Wasm in Browser          WASI
      │                   │
  DOM, Network         File System, Network
  Storage, GPU         Process, Environment
```

---

## Real-World Usage

| Application | Source → Wasm | Use Case |
|-------------|---------------|----------|
| Figma | C++ | Rendering engine |
| Google Earth | C++ | 3D rendering |
| AutoCAD Web | C++ | CAD engine |
| Photoshop Web | C++ | Image processing |
| Unity WebGL | C# | Game engine |
| Docker Wasm | Rust | Container runtime |

---

## Browser Support (2026)

Chrome ✅ | Firefox ✅ | Safari ✅ | Edge ✅ | Node.js ✅

## Debug

| Tool | Mô tả |
|------|--------|
| Chrome DevTools | Sources tab → Wasm |
| wasm-dwarfdump | Inspect debug info |
| WABT | WebAssembly Binary Toolkit |

---

**Xem thêm:** [WebSocket & SSE](15-websocket-sse.md) | [JavaScript Engine](03-javascript-engine.md) | [Browser Security](17-browser-security.md)