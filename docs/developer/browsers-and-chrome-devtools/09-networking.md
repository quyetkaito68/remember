---
title: Networking trong Browser
description: "Networking trong Browser — TCP, DNS, TLS, connection pooling, preconnect, DNS prefetch: cách trình duyệt thiết lập kết nối mạng"
tags: [networking, tcp, dns, tls, connection-pooling, preconnect, dns-prefetch]
category: developer
updated: 2026-07-26
order: 9
---

# Networking trong Browser

TCP, DNS, TLS, connection pooling — các tầng mạng browser dùng để giao tiếp với server.

---

## Networking Stack

```text
┌─────────────────────────────────────────────────────────┐
│                    BROWSER STACK                        │
│  ┌──────────────┐                                       │
│  │  JavaScript  │  fetch(), XMLHttpRequest              │
│  └──────┬───────┘                                       │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │  HTTP/HTTPS  │  Request/Response, Headers, Cookies   │
│  └──────┬───────┘                                       │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │  TLS/SSL     │  Encryption, Certificate              │
│  └──────┬───────┘                                       │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │  TCP         │  Reliable, ordered delivery           │
│  └──────┬───────┘                                       │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │  UDP (QUIC)  │  Fast, unreliable (HTTP/3)            │
│  └──────┬───────┘                                       │
│         ▼                                               │
│  ┌───────────────┐                                      │
│  │  IP → Physical│  WiFi, Ethernet, 4G/5G               │
│  └───────────────┘                                      │
└─────────────────────────────────────────────────────────┘
```

---

## DNS Resolution

```text
User nhập https://example.com

1. Browser Cache    → Có IP chưa? → Nếu có → Dùng
2. OS Cache         → Có IP chưa? → Nếu có → Dùng
3. Router Cache     → Có IP chưa? → Nếu có → Dùng
4. ISP DNS Server   → Query recursively → Nhận IP
5. Root DNS Server  → ".com" server
6. TLD DNS Server   → "example.com" authoritative server
7. Authoritative    → Trả về IP: 93.184.216.34
```

```text
DNS Hierarchy:

                    . (Root)
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      .com         .org         .net
        │            │            │
   ┌────┼────┐      │            │
   ▼    ▼    ▼      ▼            ▼
google apple example wikipedia github
```

| Hạng mục | Thời gian |
|----------|----------|
| Browser Cache | < 1ms |
| OS Cache | < 1ms |
| ISP DNS | 20-120ms |
| DNS over HTTPS | 50-200ms |

---

## TCP Connection

### Three-Way Handshake

```text
Client                    Server
  │                         │
  │──── SYN ──────────────▶│
  │◀── SYN-ACK ────────────│
  │──── ACK ──────────────▶│
  │     Connection Ready    │
```

### TCP & HTTP Version

| Phiên bản | Connection | Mô tả |
|-----------|------------|--------|
| HTTP/1.0 | 1 req/conn | Mỗi request mở kết nối mới |
| HTTP/1.1 | Keep-Alive | Mở 1 connection, nhiều requests |
| HTTP/2 | Multiplexing | Nhiều stream trên 1 connection |
| HTTP/3 | QUIC (UDP) | Không cần TCP handshake |

---

## TLS Handshake

### TLS 1.2 (2-RTT)

```text
Client                              Server
  │── ClientHello ──────────────────▶│  (ciphers, TLS version)
  │◀── ServerHello ─────────────────│  (cipher, certificate)
  │── Client verifies cert ────────▶│
  │── Key Exchange ────────────────▶│  (pre-master secret)
  │◀── Finished ───────────────────│
  │     Encrypted Communication     │
```

### TLS 1.3 (1-RTT, faster)

```text
Client                              Server
  │── ClientHello + key share ─────▶│
  │◀── ServerHello + Finished ─────│  (key share + cert)
  │── Finished ────────────────────▶│
  │     Encrypted Communication     │
  │     (1-RTT thay vì 2-RTT)       │
```

| Version | Handshake Time |
|---------|---------------|
| TLS 1.2 | 2-RTT (~100-300ms) |
| TLS 1.3 | 1-RTT (~50-150ms) |
| TLS 1.3 0-RTT | 0-RTT (reconnection) |

---

## Connection Pooling

Browser duy trì pool connections theo origin:

```text
Connection Pool:
  https://api.example.com  → [conn1, conn2, conn3]  (max 6)
  https://cdn.example.com  → [conn1, conn2]          (max 6)
  https://analytics.google → [conn1]                 (max 6)
```

| Browser | Max per origin | Total max |
|---------|---------------|-----------|
| Chrome | 6 | ~256 |
| Firefox | 6 | ~175 |
| Safari | 6 | ~200 |

---

## Preconnect, DNS Prefetch, Prefetch, Preload

| Technique | Kết nối | Tải resource | Dùng khi |
|-----------|---------|-------------|----------|
| `dns-prefetch` | Resolve DNS | Không | Domain không critical |
| `preconnect` | DNS + TCP + TLS | Không | Domain critical, chưa biết resource |
| `prefetch` | DNS + TCP + TLS + HTTP | Có (low priority) | Resource cho navigation tiếp |
| `preload` | DNS + TCP + TLS + HTTP | Có (high priority) | Resource cần ngay |

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://www.google-analytics.com">
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
<link rel="prefetch" href="/next-page.html">
```

---

## Network Timing trong DevTools

| Timing Phase | Ý nghĩa |
|-------------|----------|
| **Queued** | Request waiting in queue |
| **Stalled** | Waiting for available connection |
| **DNS Lookup** | Resolving domain name |
| **Initial Connection** | TCP handshake |
| **SSL** | TLS handshake |
| **TTFB** | Time To First Byte |
| **Content Download** | Receiving response body |

```text
Network Waterfall:

Name         Status  Size     Time   Waterfall
───────────────────────────────────────────────
index.html   200     14 KB    50ms   ████
style.css    200     8 KB     30ms   ▓▓▓▓▓▓
app.js       200     50 KB    120ms  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
api/data     200     2 KB     200ms  ░░░░░░░░░░░░░░░░░░░░░░░░
image.png    200     100 KB   80ms   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

|←─ Blocking ─→|←─ Blocking ─→|←───── Parallel ─────→|
```

---

## Network Optimization Checklist

| # | Technique | Impact |
|---|-----------|--------|
| 1 | Use HTTP/2+ | Multiplexing, header compression |
| 2 | Enable Keep-Alive | Avoid TCP handshake |
| 3 | DNS prefetch for third-party | Faster DNS resolution |
| 4 | Preconnect critical origins | Faster connection |
| 5 | Preload critical resources | Faster loading |
| 6 | Minimize third-party requests | Reduce DNS + TCP + TLS overhead |
| 7 | Use connection pooling | Reuse connections |
| 8 | Compress responses | Smaller payloads |

---

Xem thêm: [HTTP/HTTPS Lifecycle](10-http-lifecycle.md) | [HTTP/2 & HTTP/3](11-http2-http3.md) | [Network Panel](21-devtools-network.md)