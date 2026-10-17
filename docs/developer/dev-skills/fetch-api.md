---
title: Polling API từ Console
description: Cách gọi fetch liên tục từ Chrome DevTools Console để kiểm tra health endpoint
tags: [fetch, console, devtools, debugging]
category: developer
updated: 2026-08-20
order: 1
---

# Polling API từ Console

> Gọi liên tục 1 request để kiểm tra health trực tiếp từ tab **Console** trong Chrome DevTools.

---

## Code

```javascript
const id = setInterval(() => {
  fetch('https://jsonplaceholder.typicode.com/posts/1')
    .then(r => console.log(r.status))
}, 1000)
```

```javascript
// lệnh ngắn gọn, gõ tay cũng được, sau đó sang tab Network để xem
setInterval(() => {
  fetch('https://jsonplaceholder.typicode.com/posts/1')
}, 500)
```

- `id` — cần lưu để có thể dừng bằng `clearInterval(id)`
- `1000` — mỗi 1 giây gọi 1 lần
- `.then(r => console.log(r.status))` — in status code để biết response thế nào

---

## Dừng poll

```javascript
clearInterval(id)
```
