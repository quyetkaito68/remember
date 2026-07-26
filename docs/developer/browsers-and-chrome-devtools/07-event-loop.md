---
title: Event Loop & Task Queue
description: "Event Loop, Task Queue và Microtask Queue — cách JavaScript single-threaded xử lý bất đồng bộ, render, và event trong trình duyệt"
tags: [event-loop, task-queue, microtask, macrotask, call-stack, asynchronous, callback]
category: developer
updated: 2026-07-26
order: 7
---

# Event Loop & Task Queue

Single-threaded nhưng xử lý được bất đồng bộ nhờ Event Loop điều phối giữa Call Stack, Task Queue và Microtask Queue.

---

## Main Thread Architecture

```text
┌───────────────────────────────────────────────────────┐
│                    MAIN THREAD                        │
│                                                       │
│  ┌─────────────┐    ┌───────────────────────────────┐ │
│  │  Call Stack │    │       Web APIs / Browser      │ │
│  │  frame()    │◄───│  setTimeout, fetch, DOM event │ │
│  │  frame()    │    │  Worker, WebSocket            │ │
│  │  frame()    │    └───────────────────────────────┘ │
│  └──────┬──────┘                                      │
│         ▼                                             │
│  ┌─────────────────────────────────────────────────┐  │
│  │              EVENT LOOP                         │  │
│  │  1. Check Microtask Queue (all tasks)           │  │
│  │  2. Check Task Queue (one task)                 │  │
│  │  3. Render if needed (16.7ms frame budget)      │  │
│  └─────────────────────────────────────────────────┘  │
│                                                       │
│  ┌───────────────┐    ┌──────────────────────────┐    │
│  │ Microtask     │    │     Task Queue           │    │
│  │ Queue         │    │     (Macrotask Queue)    │    │
│  │ Promise.then  │    │ setTimeout callback      │    │
│  │ queueMicrotask│    │ setInterval callback     │    │
│  │ MutationObs.  │    │ I/O, rAF                 │    │
│  └───────────────┘    └──────────────────────────┘    │
└───────────────────────────────────────────────────────┘
```

---

## Microtask vs Macrotask — Quick Reference

| | Microtask | Macrotask |
|---|---|---|
| **Ưu tiên** | Cao hơn | Thấp hơn |
| **Khi chạy** | Tất cả trước khi task tiếp theo | Một task mỗi lần loop |
| **Timing** | Sau task hiện tại, trước render | Sau microtasks |
| **Sources** | `Promise.then/catch/finally`, `queueMicrotask()`, `MutationObserver`, `async/await` | `setTimeout`, `setInterval`, `I/O`, `requestAnimationFrame`, `MessageChannel`, `postMessage` |

---

## Event Loop Algorithm

```text
while (true) {
  // 1. Run ALL microtasks
  while (microtaskQueue.isNotEmpty()) {
    task = microtaskQueue.dequeue();
    execute(task);
  }

  // 2. Run ONE macrotask
  if (taskQueue.isNotEmpty()) {
    task = taskQueue.dequeue();
    execute(task);

    // 3. Render if needed
    if (shouldRender()) {
      render();
    }
  }

  // 4. Yield to browser (idle)
  yieldToBrowser();
}
```

**Quan trọng:** Mỗi lần loop chỉ lấy **một task** từ Task Queue, chạy xong, kiểm tra **tất cả** microtasks, rồi mới lấy task tiếp.

---

## Ví dụ: setTimeout vs Promise

```javascript
console.log('1');
setTimeout(() => console.log('2'), 0);
Promise.resolve().then(() => console.log('3'));
console.log('4');
```

```text
Output: 1, 4, 3, 2

1. console.log('1')        → Output: 1
2. setTimeout(cb, 0)       → Push cb to Task Queue
3. Promise.resolve().then  → Push cb to Microtask Queue
4. console.log('4')        → Output: 4
5. Call Stack empty → Microtask Queue → run Promise cb → Output: 3
6. Task Queue → run setTimeout cb → Output: 2
```

---

## Rendering & rAF

Browser render khi: microtask queue rỗng + đủ 16.7ms từ lần render trước.

```text
Timeline (60fps budget = 16.7ms):

  Task 1 (5ms) → Microtasks (2ms) → Render (3ms) → Task 2 (8ms) → Microtasks (1ms) → Render (3ms)
  |←──────── 16.7ms ────────→|←────────── 16.7ms ────────→|
```

**rAF chạy trước render, không phải trong task queue:**

```text
Event Loop Order:
  1. Run all microtasks
  2. Run one macrotask
  3. Run all requestAnimationFrame callbacks
  4. Render
  5. Repeat
```

```javascript
function animate() {
  element.style.transform = `translateX(${x}px)`;
  x += 1;
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

---

## Web Workers — Event Loop riêng

```text
┌───────────────── Main Thread ────────────────────┐
│  Event Loop → Call Stack → Microtask Queue       │
│                                                  │
│  postMessage(worker, data) ────────────────────┐ │
└────────────────────────────────────────────────┼─┘
                                                 │
┌─────────────────▼──────────── Worker Thread ───┤
│  Event Loop → Call Stack → Microtask Queue     │
│                                                │
│  postMessage(mainThread, result) ────────────┐ │
└──────────────────────────────────────────────┼─┘
                                               │
Main Thread receives message → push to Task Queue
```

---

## Performance Checklist

| Vấn đề | Nguyên nhân | Giải pháp |
|--------|------------|-----------|
| Janky animation | Task quá dài block render | Break task nhỏ hơn |
| Click không responsive | Long task đang chạy | `requestIdleCallback` |
| UI đơ | Infinite loop main thread | Move to Web Worker |
| Frame drop | Microtask quá nhiều | Limit microtask per frame |

```javascript
// BAD — Long task blocks rendering
function processLargeData(data) {
  data.forEach(item => heavyComputation(item)); // 50ms
}

// GOOD — Break into smaller tasks
function processLargeData(data, index = 0) {
  const chunk = data.slice(index, index + 1000);
  chunk.forEach(item => heavyComputation(item));
  if (index + 1000 < data.length) {
    setTimeout(() => processLargeData(data, index + 1000), 0);
  }
}
```

---

## Common Gotchas

- [ ] `setTimeout(fn, 0)` ≠ chạy ngay — phải chờ Call Stack rỗng + tất cả microtasks xong
- [ ] Promise chain chạy hết trước khi vào macrotask tiếp theo
- [ ] Microtask quá nhiều → block render → janky UI
- [ ] `queueMicrotask()` bên trong Promise callback → chạy trong cùng microtask checkpoint
- [ ] rAF callback chạy **trước** render, không phải trong task queue
- [ ] Web Worker có event loop riêng — postMessage là cách giao tiếp duy nhất

---

Xem thêm: [JavaScript Engine](03-javascript-engine.md) | [Web APIs](08-web-apis.md) | [Performance Panel](23-devtools-performance.md)