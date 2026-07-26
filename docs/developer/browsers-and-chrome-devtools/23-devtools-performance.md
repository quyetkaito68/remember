---
title: Performance Panel
description: "Performance Panel trong Chrome DevTools — record, analyze và optimize rendering performance: FPS, CPU, memory, frame timeline"
tags: [performance-panel, devtools, performance-profiling, flame-chart, fps, rendering-performance]
category: developer
updated: 2026-07-26
order: 23
---

# Performance Panel

Record rendering performance — FPS, CPU, memory — tìm chính xác bottleneck gây lag.

---

## Recording

| Action | Shortcut |
|--------|----------|
| Start/Stop | `Ctrl+E` |
| Reload & Record | Ctrl + Click reload icon |

```text
Recording workflow:
1. ☑ Screenshots, ☑ JavaScript, ☑ Memory
2. Ctrl+E hoặc click record
3. Thực hiện thao tác test (scroll, click, animation)
4. Stop recording
5. Phân tích kết quả
```

---

## Panel Layout

```text
┌──────────────────────────────────────────────────────────────┐
│  Performance Panel                                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Screenshots (thumbnail strip)                        │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FPS  ▏██████████▏██████████▏████████▏               │   │
│  │       0s        1s         2s        3s              │   │
│  │  (Red bar = dropped frame)                            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  CPU ▏▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░▓▓▓▓▓▓▓           │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FLAME CHART (Main Thread)                            │   │
│  │  ├── Recalculate Style (25ms)                        │   │
│  │  │   ├── Parse CSS (8ms)                             │   │
│  │  │   └── Compute Style (17ms)                        │   │
│  │  ├── Layout (12ms)                                   │   │
│  │  └── Paint (8ms)                                     │   │
│  └──────────────────────────────────────────────────────┘   │
│  Summary: Loading 15% | Scripting 45% | Rendering 25% |     │
│           Painting 15%                                       │
└──────────────────────────────────────────────────────────────┘
```

---

## Flame Chart

```text
Flame Chart:
┌─────────────────────────────────────────────────┐
│  Event (click)                                  │
│  ┌─────────────────────────────────────────────┐│
│  │  Function A (50ms)                          ││
│  │  ┌──────────────┐  ┌──────────────────────┐ ││
│  │  │ Function B   │  │  Function C          │ ││
│  │  │ (20ms)       │  │  (30ms)              │ ││
│  │  ┌────────┐     │  │  ┌────────────────┐  │ ││
│  │  │ Func D │     │  │  │  Func E        │  │ ││
│  │  │ (8ms)  │     │  │  │  (15ms)        │  │ ││
│  │  └────────┘     │  │  └────────────────┘  │ ││
│  └─────────────────┘  └──────────────────────┘ ││
└─────────────────────────────────────────────────┘

Wider bar = longer execution = potential bottleneck
```

| Observation | Meaning |
|-------------|---------|
| Wider bar | Function chạy lâu |
| Deep nesting | Recursive/nested calls |
| Same-width bars lặp | Identical work repeated |
| Gap between bars | Idle/waiting time |

---

## Performance Metrics

| Metric | Target | Ý nghĩa |
|--------|--------|---------|
| FPS | ≥60fps | Smooth animation |
| CPU | <30% | Không quá tải |
| Memory | Stable | Không tăng liên tục |
| Layout | <16ms | Per frame |
| Paint | <16ms | Per frame |

---

## Summary Pie Chart

```text
Scripting cao → optimize JS (debounce, reduce DOM manipulation)
Rendering cao → optimize CSS (simplify selectors, reduce complexity)
Painting cao → reduce paint work (use transform, reduce elements)
Loading cao → optimize loading (lazy load, preload, CDN)
```

---

## Common Performance Issues

| Issue | Flame Chart Pattern | Solution |
|-------|-------------------|----------|
| Long script | Wide yellow bars | Optimize algorithm, debounce |
| Layout thrashing | Multiple purple bars | Batch DOM reads/writes |
| Expensive paint | Wide green bars | Use transform, reduce elements |
| Forced reflow | Frequent layout calls | Avoid reading layout after style change |
| Long task | Single wide bar >50ms | Break into smaller tasks (`requestIdleCallback`) |

---

## Performance Analysis Checklist

```text
UI lag / slow?
│
├── 1. Record 5-10s interaction
│
├── 2. Check Summary pie chart
│     ├── Scripting > 40% → JS bottleneck
│     ├── Rendering > 30% → CSS/layout bottleneck
│     └── Painting > 20% → paint bottleneck
│
├── 3. Check FPS chart
│     └── Red bars = dropped frames
│
├── 4. Zoom vào Main Thread flame chart
│     └── Tìm widest bars → function nào chạy lâu?
│
├── 5. Bottom-up tab
│     └── Sort by Self time → function nào tốn nhiều nhất?
│
└── 6. Fix → Record lại → So sánh
```

---

## Recording Tips

| Tip | Mô tả |
|-----|--------|
| Record ngắn | 5-10s, focused analysis |
| Disable cache | Thấy real loading time |
| Incognito | Clean profile, no extensions |
| CPU throttle | Test trên simulated slow device |

---

## Summary View

```text
Bottom-up tab:
┌───────────────────────────────────────────────────┐
│  Total  Self  Category  Function                  │
│  50ms   30ms  Scripting  processArray             │
│  30ms   25ms  Scripting  calculateTotal           │
│  20ms   20ms  Rendering  recalculateStyles        │
│  15ms   15ms  Painting   paintLayer               │
└───────────────────────────────────────────────────┘
```

---

Xem thêm: [Chrome DevTools Tổng Quan](19-chrome-devtools.md) | [Memory Panel](24-devtools-memory.md) | [Rendering Pipeline](04-rendering-pipeline.md)