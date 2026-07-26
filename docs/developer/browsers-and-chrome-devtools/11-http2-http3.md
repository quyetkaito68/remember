---
title: HTTP/2 & HTTP/3
description: "HTTP/2 và HTTP/3 — Multiplexing, Server Push, Header Compression, QUIC: các thế hệ giao thức HTTP mới giúp tăng tốc web"
tags: [http2, http3, quic, multiplexing, server-push, header-compression, spd]
category: developer
updated: 2026-07-26
order: 11
---

# HTTP/2 & HTTP/3

HTTP/2 multiplexing + HPACK giải quyết HTTP/1.1 HOL blocking ở application layer. HTTP/3 dùng QUIC (UDP) giải quyết TCP-level HOL blocking.

---

## Evolution

```text
HTTP/0.9 (1991)    ──▶  Simple GET, no headers
        │
HTTP/1.0 (1996)    ──▶  Headers, status codes, content types
        │
HTTP/1.1 (1997)    ──▶  Keep-Alive, chunked encoding, Host header
        │
HTTP/2 (2015)      ──▶  Multiplexing, HPACK, Server Push, Streams
        │
HTTP/3 (2022)      ──▶  QUIC (UDP), 0-RTT, no HOL blocking
```

---

## HTTP/1.1: Vấn đề

| Vấn đề | Giải thích |
|--------|-----------|
| **Head-of-Line Blocking** | Request 1 chờ xong mới gửi request 2 |
| **Single Connection** | Mỗi domain max 6 connections |
| **No Header Compression** | Headers gửi lại mỗi lần (~800 bytes) |
| **Redundant Headers** | Cookie, User-Agent gửi lại mỗi request |

```text
HTTP/1.1 (6 connections, sequential per connection):

Connection 1: [Request 1]──wait──[Request 7]──wait──[Request 13]
Connection 2: [Request 2]──wait──[Request 8]──wait──[Request 14]
Connection 3: [Request 3]──wait──[Request 9]──wait──[Request 15]
Connection 4: [Request 4]──wait──[Request 10]──wait──[Request 16]
Connection 5: [Request 5]──wait──[Request 11]
Connection 6: [Request 6]──wait──[Request 12]

⚠️ Mỗi request phải chờ request trước trên cùng connection
```

---

## HTTP/2

### Multiplexing

Nhiều **streams** chạy đồng thời trên **một TCP connection duy nhất**.

```text
HTTP/2 (1 connection, parallel):

Stream 1: [Request 1]──[Response 1]
Stream 2: [Request 2]──[Response 2]
Stream 3: [Request 3]──[Response 3]
Stream 4: [Request 4]──[Response 4]
Stream 5: [Request 5]──[Response 5]
Stream 6: [Request 6]──[Response 6]

✅ Không cần chờ, chạy song song hoàn toàn
```

### HPACK Header Compression

| Before HPACK | After HPACK |
|-------------|-------------|
| `:authority: api.example.com` | Index 1 |
| `:path: /api/users` | Index 3 |
| `cookie: session=abc123` | Literal + Index |
| ~800 bytes per request | ~100 bytes per request |

### Server Push

```text
Client Request:
  GET /index.html

Server Response (with push):
  200 OK: index.html
  PUSH_PROMISE: /style.css      ← Pushed before client asks
  PUSH_PROMISE: /app.js         ← Pushed before client asks
```

---

## HTTP/3 (QUIC)

HTTP/3 chạy trên **QUIC** (UDP) thay vì TCP.

### Head-of-Line Blocking: TCP vs QUIC

```text
TCP (Head-of-Line Blocking):
  Stream 1: [Request 1]──[Pkt 1]──[Pkt 2]──[Pkt 3]──[Pkt 4]  ✅
  Stream 2: [Request 2]──[Pkt 1]──[Pkt 2]──[Pkt 3]──[Pkt 4]
                                                 ↑
                                    Pkt 3 lost → ALL streams blocked

QUIC (No Head-of-Line Blocking):
  Stream 1: [Request 1]──[Pkt 1]──[Pkt 2]──[Pkt 3]──[Pkt 4]  ✅
  Stream 2: [Request 2]──[Pkt 1]──[Pkt 2]──[Pkt 3]──[Pkt 4]  ✅
                                                 ↑
                                    Pkt 3 lost → ONLY Stream 1 blocked
```

### 0-RTT Reconnection

```text
Client                           Server
  │── 0-RTT Data (cached key) ───▶│
  │── HTTP Request ───────────────▶│
  │◀── HTTP Response ──────────────│
  ✅ No handshake delay!
```

### Connection Migration

WiFi → 4G: TCP mất connection (mất 2-3 giây), QUIC tự migrate (không mất connection).

---

## So sánh Tổng hợp

| Tính năng | HTTP/1.1 | HTTP/2 | HTTP/3 |
|-----------|----------|--------|--------|
| Transport | TCP | TCP | **QUIC (UDP)** |
| Handshake | 3-RTT | 3-RTT | **1-RTT** (0-RTT) |
| Multiplexing | No | Yes | Yes |
| HOL Blocking | Yes | **Yes (TCP-level)** | **No** |
| Header Compression | No | HPACK | QPACK |
| Server Push | No | Yes | Yes |
| Encryption | Optional | Optional | **Built-in** |
| Connection Migration | No | No | **Yes** |
| Browser Support | All | 95%+ | 90%+ (2026) |

---

## Khi nào dùng gì

| Scenario | Recommendation |
|----------|---------------|
| Website thông thường | HTTP/2 (đủ tốt) |
| API calls nhiều, latency-sensitive | HTTP/3 (nếu server hỗ trợ) |
| CDN | HTTP/3 (Cloudflare, AWS CloudFront hỗ trợ) |
| Mobile apps | HTTP/3 (connection migration) |
| Real-time apps | HTTP/3 (no HOL blocking) |

---

## Kiểm tra Protocol

```bash
# Kiểm tra HTTP/2
curl -I https://example.com --http2

# Kiểm tra HTTP/3
curl -I https://example.com --http3

# Trong DevTools: Network Tab → Protocol column → h2 hoặc h3
```

```text
Name         Protocol  Status  Size     Time
──────────────────────────────────────────────
index.html   h3        200     14 KB    30ms
style.css    h3        200     8 KB     15ms
app.js       h3        200     50 KB    40ms
api/data     h2        200     2 KB     120ms
```

---

## Migration Checklist

- [ ] Verify server supports HTTP/2 (h2)
- [ ] Enable HTTP/3 on server/CDN (QUIC)
- [ ] Check CDN supports HTTP/3 (Cloudflare auto, AWS需 config)
- [ ] Test connection migration trên mobile
- [ ] Verify no regression trên older browsers
- [ ] Monitor HOL blocking improvements qua DevTools Protocol column
- [ ] Check Server Push usage (nếu dùng) — hiện đang deprecated ở một số browser

---

## Browser Support (2026)

| Browser | HTTP/2 | HTTP/3 |
|---------|--------|--------|
| Chrome 90+ | ✅ | ✅ |
| Firefox 90+ | ✅ | ✅ |
| Safari 14+ | ✅ | ✅ (macOS Ventura+) |
| Edge 90+ | ✅ | ✅ |

---

Xem thêm: [HTTP/HTTPS Lifecycle](10-http-lifecycle.md) | [Browser Cache](12-browser-cache.md) | [Networking](09-networking.md)