---
title: Memory Panel
description: "Memory Panel trong Chrome DevTools — heap snapshot, allocation profiling, memory leak detection, detached DOM nodes"
tags: [memory-panel, devtools, memory-leak, heap-snapshot, garbage-collection]
category: developer
updated: 2026-07-26
order: 24
---

# Memory Panel

Phát hiện memory leak — tìm objects giữ reference không cần thiết.

---

## Profiling Methods

| Method | When Use | Impact |
|--------|----------|--------|
| **Heap Snapshot** | Find what's in memory | Low |
| **Allocation Timeline** | See allocations over time | Medium |
| **Allocation Sampling** | Lightweight profiling | Low |

---

## Heap Snapshot

Snapshot mọi objects trong JS heap, so sánh giữa 2 thời điểm.

### Cách dùng

```text
1. Click [Take Snapshot]
2. Thực hiện action lặp (thêm/xóa items)
3. Click [Take Snapshot] lần nữa
4. Compare snapshot 1 vs snapshot 2
5. Xem objects #Delta tăng → potential leak
```

### Heap Snapshot View

```text
┌──────────────────────────────────────────────────────────┐
│  Heap Snapshot Comparison                                │
│  Summary  ▼  Comparison  │  Containment  │  Statistics   │
│                                                          │
│  Class            #Delta  Size Delta  Retained Size      │
│  ──────────────────────────────────────────────────────  │
│  (string)         +150    +12.5 KB    +12.5 KB           │
│  (array)          +50     +8.2 KB     +8.2 KB            │
│  HTMLDivElement   +30     +2.1 KB     +15.3 KB           │
│  EventListener    +25     +1.8 KB     +1.8 KB            │
│  (closure)        +20     +1.2 KB     +4.5 KB            │
└──────────────────────────────────────────────────────────┘
```

### Retained Size vs Size

| Thuật ngữ | Ý nghĩa |
|-----------|---------|
| **Size** | Direct memory của object |
| **Retained Size** | Memory freed nếu object bị GC |

---

## Memory Leak Patterns

### 1. Forgotten Event Listeners

```javascript
// LEAK
button.addEventListener('click', () => { console.log('clicked'); });

// FIX
button.removeEventListener('click', handler);
```

### 2. Detached DOM Nodes

```javascript
// LEAK — giữ reference sau khi remove
let detached = div;
document.body.removeChild(div);

// FIX
document.body.removeChild(div);
detached = null;
```

### 3. Closures giữ large data

```javascript
// LEAK
function processData() {
  const hugeData = new Array(1000000).fill('x');
  return () => console.log(hugeData.length);
}

// FIX — chỉ giữ cần thiết
function processData() {
  const hugeData = new Array(1000000).fill('x');
  const length = hugeData.length;
  return () => console.log(length);
}
```

### 4. setInterval never cleared

```javascript
// FIX
const interval = setInterval(() => { ... }, 1000);
clearInterval(interval); // khi không cần
```

---

## Allocation Timeline

```text
Memory ▏██████████████████████████████████
       ▏████████████████████████████████████████████
       ▏██████████████████████████████████████████████
       0s        5s        10s       15s       20s

Memory tăng liên tục = leak
Memory tăng rồi drop = normal GC
```

---

## Detached DOM Nodes

DOM nodes bị remove khỏi document nhưng vẫn có reference.

```text
1. Take heap snapshot
2. Summary view → filter: "Detached"
3. Click detached element
4. Retainers panel → ai giữ reference?
5. Clear reference
```

---

## Memory Leak Detection Checklist

```text
Memory tăng liên tục?
│
├── 1. Take heap snapshot → Compare
│     └── Object nào #Delta tăng đều?
│
├── 2. Allocation Timeline
│     ├── Memory curve linear up → leak
│     └── Memory curve sawtooth → normal GC
│
├── 3. Filter "Detached" trong heap snapshot
│     └── Detached DOM nodes → check retainer
│
├── 4. Kiểm tra common leak sources
│     ├── Event listeners chưa remove?
│     ├── Detached DOM nodes?
│     ├── Closures giữ large data?
│     ├── setInterval chưa clear?
│     ├── Global variables tích lũy?
│     └── Cache growing unbounded?
│
└── 5. Fix → Snapshot lại → Verify #Delta = 0
```

---

## Retainer Analysis

| Retainer | Action |
|----------|--------|
| Event listener → DOM element | Remove listener khi destroy |
| Closure → large array | Clear closure reference |
| Global variable → DOM node | Set to null |
| Detached HTMLDivElement | Nullify reference |
| Cache object growing | Implement max size / eviction |

---

## Tips

| Tip | Mô tả |
|-----|--------|
| Record ngắn | So sánh dễ hơn |
| Repeat actions | 10x add/remove để thấy pattern |
| Compare snapshots | Tìm growing objects |
| Check retainer chain | Tìm ai giữ leak |
| Allocation sampling | Dùng trong production |

---

Xem thêm: [Chrome DevTools Tổng Quan](19-chrome-devtools.md) | [Performance Panel](23-devtools-performance.md) | [Application Panel](25-devtools-application.md)