---
title: WebSocket & Server-Sent Events
description: "WebSocket và Server-Sent Events (SSE) — hai cơ chế real-time communication trong browser: full-duplex và one-way streaming"
tags: [websocket, server-sent-events, sse, real-time, full-duplex, streaming]
category: developer
updated: 2026-07-26
order: 15
---

# WebSocket & SSE

WebSocket = full-duplex (cả hai phía). SSE = one-way server push. Cả hai dùng cho real-time.

---

## Protocol Comparison

```text
HTTP:     Client ──Request──▶ Server
          Client ◀──Response── Server  (kết thúc)

WebSocket: Client ◀═══════════▶ Server  (full-duplex, persistent)

SSE:       Client ◀─────────── Server  (server push, auto-reconnect)
```

---

## Decision Tree: Chọn Real-Time

```text
Cần real-time?
│
├─ Client cần gửi data lên server?
│  ├─ Có, liên tục (chat, gaming, collab) → WebSocket
│  └─ Không (chỉ server push) → SSE
│
├─ Cần auto-reconnect?
│  ├─ Có → SSE (built-in)
│  └─ Không → WebSocket (tự implement)
│
├─ Đằng sau proxy/CDN?
│  ├─ Có, restricted → SSE (HTTP, tương thích tốt)
│  └─ Không → WebSocket
│
├─ Cần binary data?
│  ├─ Có → WebSocket
│  └─ Không → SSE (text only)
│
└─ CRUD operations? → HTTP REST
```

---

## SSE vs WebSocket

| Tính năng | SSE | WebSocket |
|-----------|-----|-----------|
| Direction | **Server → Client** (one-way) | **Both ways** |
| Protocol | **HTTP** | **ws://** (upgrade) |
| Auto-reconnect | **Có** (built-in) | Không |
| Event ID / resume | **Có** | Không |
| Binary data | Không | **Có** |
| Max connections (HTTP/1.1) | ~6/domain | **Không giới hạn** |
| Proxy/CDN | **Tương thích tốt** | Có thể bị block |

---

## WebSocket

### Handshake

```text
Client ──GET /chat HTTP/1.1──────▶ Server
       Upgrade: websocket
       Sec-WebSocket-Key: dGhl...
       Sec-WebSocket-Version: 13

Server ──101 Switching Protocols──▶ Client
       Upgrade: websocket
       Sec-WebSocket-Accept: s3pP...
```

### API

```javascript
const socket = new WebSocket('wss://example.com/socket');

socket.onopen = () => socket.send(JSON.stringify({ type: 'join', room: 'general' }));
socket.onmessage = (e) => { const data = JSON.parse(e.data); };
socket.onclose = (e) => { console.log(e.code, e.reason); };
socket.onerror = (e) => { console.error(e); };
```

### Chat Example (Node.js)

```javascript
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    wss.clients.forEach(c => {
      if (c.readyState === WebSocket.OPEN) c.send(JSON.stringify(msg));
    });
  });
});
```

---

## SSE

### API

```javascript
const es = new EventSource('/api/events');
es.onmessage = (e) => { console.log(JSON.parse(e.data)); };
es.addEventListener('price-update', (e) => { console.log(JSON.parse(e.data)); });
es.onerror = () => { /* auto reconnect */ };
```

### Server (Node.js)

```javascript
http.createServer((req, res) => {
  if (req.url === '/api/events') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    });
    const interval = setInterval(() => {
      res.write(`data: ${JSON.stringify({ time: new Date() })}\n\n`);
    }, 5000);
    req.on('close', () => clearInterval(interval));
  }
}).listen(3000);
```

### Event Format

```text
data: {"price": 100.50}

event: price-update
data: {"price": 101.20}

id: 12345
retry: 5000
data: {"message": "Connected"}

(Events separated by \n\n)
```

---

## Use Cases

| Scenario | Recommendation |
|----------|---------------|
| Chat, messaging | **WebSocket** |
| Live stock price | **SSE** |
| Multiplayer game | **WebSocket** |
| Live notifications | **SSE** (auto-reconnect) |
| Collaboration (Google Docs) | **WebSocket** |
| Live sports score | **SSE** |
| Dashboard real-time | SSE hoặc WebSocket |
| CRUD operations | **HTTP REST** |

---

## Connection Management

### Heartbeat (WebSocket)

```javascript
setInterval(() => {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ type: 'ping' }));
  }
}, 30000);
```

### Reconnection (WebSocket)

```javascript
function connect() {
  const socket = new WebSocket('wss://example.com/socket');
  socket.onclose = (e) => {
    if (!e.wasClean) setTimeout(connect, 3000);
  };
  socket.onerror = () => socket.close();
}
```

---

## Real-World Usage

| Application | Technology |
|-------------|-----------|
| Slack, Discord | WebSocket |
| GitHub Notifications | SSE |
| Trading platforms | WebSocket |
| Twitter Live | SSE |

---

**Xem thêm:** [Service Worker & PWA](14-service-worker-pwa.md) | [Networking](09-networking.md) | [WebAssembly](16-webassembly.md)