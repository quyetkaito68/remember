---
title: Debugging Thực Tế
description: "Debugging thực tế — techniques, patterns, strategies để debug hiệu quả với DevTools"
tags: [debugging, debugging-techniques, error-handling, devtools-debugging, real-world-debugging]
category: developer
updated: 2026-07-26
order: 34
---

# Debugging Thực Tế

> Reproduce → Isolate → Identify root cause → Fix → Prevent. DevTools > console.log.

---

## Debugging Process

```text
1. REPRODUCE       → Trigger bug nhất quán
2. ISOLATE          → Thu hẹp: page → component → code
3. IDENTIFY         → Root cause, không chỉ symptom
4. FIX              → Fix + test case
5. PREVENT          → Test, code review, logging
```

---

## Issue → Tool Mapping

| Issue | Tool | How |
|-------|------|-----|
| JS error | Console tab | Error message + stack trace |
| Broken layout | Elements tab | Inspect CSS, box model |
| API failing | Network tab | Check request/response/status |
| Slow page | Performance tab | Record → flame chart |
| Memory leak | Memory tab | Heap snapshot comparison |
| React state bug | React DevTools | Component tree + props/state |
| Vue reactivity bug | Vue DevTools | Component inspection |
| Redux flow bug | Redux DevTools | State timeline + actions |

---

## Debugging Checklist

| # | Check | Tool |
|---|-------|------|
| 1 | Reproduce consistently | Manual testing |
| 2 | Check console errors | Console tab |
| 3 | Check network requests | Network tab |
| 4 | Check DOM changes | Elements tab |
| 5 | Set breakpoints | Sources tab |
| 6 | Check variable values | Watch/Scope panel |
| 7 | Check call stack | Sources tab |
| 8 | Profile performance | Performance tab |
| 9 | Check memory | Memory tab |
| 10 | Read error message carefully | Console |

---

## Console Techniques

```javascript
console.table([{ name: 'John', age: 30 }, { name: 'Jane', age: 25 }]);
console.group('Step 1'); console.log('msg'); console.groupEnd();
console.time('fetch'); await fetchData(); console.timeEnd('fetch');
console.trace('Called from:');

// Intercept all fetch
const originalFetch = window.fetch;
window.fetch = async (...args) => {
  console.log('Fetch:', args[0]);
  const response = await originalFetch(...args);
  console.log('Response:', response.status, args[0]);
  return response;
};
```

---

## Common Bug Patterns

### Async/Await Missing

```javascript
// ❌ Returns Promise, not data
function getUser() {
  fetch('/api/user').then(r => r.json()).then(user => user);
}
// ✅
async function getUser() {
  return await (await fetch('/api/user')).json();
}
```

### Closure in Loop

```javascript
// ❌ Always logs 5
for (var i = 0; i < 5; i++) buttons[i].addEventListener('click', () => console.log(i));
// ✅ Correct index
for (let i = 0; i < 5; i++) buttons[i].addEventListener('click', () => console.log(i));
```

### Stale State (React)

```javascript
// ❌ count always 0
setCount(count + 1);
// ✅ Uses latest state
setCount(prev => prev + 1);
```

### Memory Leak

```javascript
// ❌ Listener never removed
useEffect(() => { window.addEventListener('resize', handleResize); }, []);
// ✅
useEffect(() => {
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
```

---

## Systematic Debugging Strategies

| Strategy | How |
|----------|-----|
| **Binary Search** | Log at midpoint → narrow half → repeat |
| **Elimination** | Comment half → check → narrow |
| **Rubber Duck** | Explain problem out loud → find bug during explanation |
| **Rubber Duck** | Explain problem step by step → bug reveals itself |

---

## Debugging Tools

| Tool | Dùng để |
|------|--------|
| **Console** | Basic logging |
| **Sources Panel** | Breakpoints, step through |
| **Network Panel** | Request/response debugging |
| **React DevTools** | Component tree, props, state |
| **Vue DevTools** | Component inspection |
| **Redux DevTools** | State management debugging |

---

Xem thêm: [Sources Panel](22-devtools-sources.md) | [Performance Panel](23-devtools-performance.md) | [Memory Panel](24-devtools-memory.md)