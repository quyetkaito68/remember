---
title: Network Panel
description: "Network Panel trong Chrome DevTools — monitor, filter, analyze network requests: waterfall, timing, headers, response, caching"
tags: [network-panel, devtools, network-analysis, waterfall, request-response]
category: developer
updated: 2026-07-26
order: 21
---

# Network Panel

Monitor tất cả network requests — filter, analyze waterfall, debug API calls, caching.

---

## Giao diện

```text
┌──────────────────────────────────────────────────────────────┐
│  [Disable cache] ☑  Throttle: [No throttling ▼]  [Clear] 🔍 │
├──────────────────────────────────────────────────────────────┤
│  Filters:                                                    │
│  [All] [Fetch/XHR] [JS] [CSS] [Img] [Media] [Font] [WS]      │
├──────────────────────────────────────────────────────────────┤
│  Name          Method  Status  Size       Time   Waterfall   │
│  ─────────────────────────────────────────────────────────── │
│  index.html    GET     200     14.5 KB    85ms   ████████    │
│  style.css     GET     304     0 B        23ms   ██          │
│  app.js        GET     200     52.1 KB    142ms  ████████████│
│  api/user      GET     200     1.2 KB     245ms  ████████████│
├──────────────────────────────────────────────────────────────┤
│  8 requests  |  260 KB transferred  |  1.2 MB resources      │
│  Finish: 1.2s  |  DOMContentLoaded: 850ms  |  Load: 1.2s     │
└──────────────────────────────────────────────────────────────┘

Hover vào Size → tooltip: "Served from disk cache, resource size: 14.5 KB"
```

---

## Disable Cache

Checkbox `Disable cache` ở thanh toolbar — **chỉ có hiệu lực khi DevTools đang mở**.

### Cách hoạt động

```text
Disable cache ☑ (DevTools mở)
─────────────────────────────────
Browser request → BỎ QUA disk/memory cache
                → Luôn gửi request mới đến server
                → Server trả 200 OK + body đầy đủ

Disable cache ☐ (hoặc DevTools đóng)
─────────────────────────────────
Browser request → Check cache trước
                ├── Có cache hợp lệ → 304 Not Modified (0 KB)
                └── Không có cache → 200 OK + body mới
```

### Size column — cách đọc

Mỗi dòng request hiển thị **1 giá trị** trong cột Size:

```text
  Name          Size
  ─────────────────────
  index.html    14.5 KB          ← từ network hoặc cache
  style.css     0 B              ← từ cache
  app.js        52.1 KB          ← từ network
```

**Hover vào Size** → tooltip hiện chi tiết:

```text
┌───────────────────────────────────────────────────────────────────────┐
│  Serve from disk cache, resource size: 14.5 KB                        │
│              ↑ từ đâu                  ↑ kích thước file gốc (decoded)│
└───────────────────────────────────────────────────────────────────────┘
```

| Tooltip format | Ý nghĩa |
|----------------|----------|
| `Served from disk cache, resource size: X KB` | Không có request mạng, dùng cache disk |
| `Served from memory cache, resource size: X KB` | Không có request mạng, dùng cache RAM |
| `Transferred: X KB, resource size: Y KB` | Có request mạng — X = nén (gzip), Y = file gốc |

```text
Ví dụ hover:
─────────────────────────────────────────────────
Case 1 — Cached:
  "Served from disk cache, resource size: 14.5 KB"
   → Không request, browser dùng file cũ từ disk
   → Size column hiển thị: 0 B (from disk cache)

Case 2 — Network, có gzip:
  "Transferred: 42 KB, resource size: 150 KB"
   → Browser nhận 42 KB (nén), giải nén thành 150 KB
   → Size column hiển thị: 42 KB

Case 3 — Network, không gzip:
  "Transferred: 150 KB, resource size: 150 KB"
   → Browser nhận 150 KB (không nén)
   → Size column hiển thị: 150 KB
```

**Status bar** (dòng cuối) tổng hợp tất cả requests:

```text
8 requests  |  260 KB transferred  |  1.2 MB resources
             ↑ tổng từ network      ↑ tổng decoded (file gốc)
```

### Các trường hợp đặc biệt

| Hiển thị trong cột | Hover tooltip | Ý nghĩa |
|---------------------|---------------|----------|
| `52.1 KB` | `Transferred: 52.1 KB, resource size: 52.1 KB` | Network, không gzip |
| `42 KB` | `Transferred: 42 KB, resource size: 150 KB` | Network, có gzip |
| `0 B (from disk cache)` | `Served from disk cache, resource size: 14.5 KB` | Cached disk |
| `0 B (from memory cache)` | `Served from memory cache, resource size: 8.2 KB` | Cached RAM |
| `Pending...` | — | Request đang xử lý |

Khi `Disable cache` bật → Size column **luôn hiển thị kích thước thực** (transferred), không bao giờ `from cache`.

### Khi nào dùng

| Use Case | Giải thích |
|----------|-----------|
| Dev/Coding | Thấy ngay file CSS/JS mới sau khi save, không cần hard refresh |
| Debug caching | So sánh response khi có/không có cache |
| Test fresh load | Mô phỏng user lần đầu visit trang |
| Verify Cache-Control | Xem header caching có đúng logic không |

## Filter

| Filter | Mô tả | Ví dụ |
|--------|--------|-------|
| `type:` | Loại resource | `type:script`, `type:css`, `type:fetch` |
| `status-code:` | HTTP status | `status-code:404`, `status-code:5xx` |
| `method:` | HTTP method | `method:POST` |
| `domain:` | Domain | `domain:api.example.com` |
| `larger-than:` | Kích thước | `larger-than:100KB` |
| `is:` | Trạng thái | `is:from-cache`, `is:running` |
| `-domain:` | Exclude domain | `-domain:cdn.example.com` |

```text
Combo filters:
type:fetch status-code:200 mime-type:application/json
→ JSON API responses thành công

-type:script -type:stylesheet
→ Bỏ qua static assets
```

---

## Waterfall

```text
Waterfall Columns:

Queued     Stalled    DNS Lookup  Initial    TTFB       Content
                            Connection  (Server)   Download
─────────────────────────────────────────────────────────────────
│░░░░░░░│▓▓▓▓▓▓│████│▓▓▓▓▓▓▓▓▓▓▓▓▓▓│░░░░░░│▓▓▓▓│
         Queuing    DNS+TCP+TLS   Waiting   Download

Colors:
  ░░░ Waiting/Queued
  ▓▓▓ DNS+TCP+TLS (Connection)
  ███ Content Download
  ▓▓▓ TTFB (Time to First Byte)
```

| Phase | Optimization |
|-------|-------------|
| Queued | HTTP/2 multiplexing |
| Stalled | Preconnect |
| DNS Lookup | DNS prefetch |
| Initial Connection | Keep-Alive |
| SSL | TLS 1.3 |
| TTFB | Server optimization |
| Content Download | Compression, CDN |

---

## Request Details

| Tab | Xem gì |
|-----|--------|
| Headers | Request/response headers, cookies |
| Preview | JSON tree, HTML render, image preview |
| Response | Raw response body |
| Initiator | Gì trigger request này (Parser/Script/Other) |
| Timing | Chi tiết từng phase: Stalled → DNS → SSL → TTFB → Download |

---

## Copy as cURL

Right-click request → Copy → Copy as cURL:

```bash
curl 'https://api.example.com/users' \
  -H 'authorization: Bearer eyJhbGciOi...' \
  -H 'accept: application/json' \
  --compressed
```

**Ứng dụng:** Debug API, share request với team, replay trong terminal.

---

## Throttling

| Preset | Download | Upload | Latency |
|--------|----------|--------|---------|
| Fast 3G | 1.5 Mbps | 750 Kbps | 100ms |
| Slow 3G | 500 Kbps | 500 Kbps | 2000ms |
| Offline | 0 | 0 | ∞ |

---

## Network Debugging Checklist

```text
Request có vấn đề?
│
├── 1. Status code sai?
│     ├── 4xx → client error (auth, payload, endpoint)
│     └── 5xx → server error (check server logs)
│
├── 2. Request chậm?
│     ├── Timing tab → phase nào chiếm nhiều?
│     ├── TTFB cao → server processing
│     └── Download cao → payload lớn → compress/CDN
│
├── 3. CORS error?
│     └── Headers tab → check Access-Control-Allow-Origin
│
├── 4. Cache miss?
│     └── Headers → Cache-Control, ETag, If-None-Match
│
└── 5. Too many requests?
      └── Waterfall overlap → combine, lazy load, HTTP/2
```

---

## Tips

| Tip | Mô tả |
|-----|--------|
| Preserve log | Giữ requests khi page reload |
| Capture screenshots | Frame-by-frame |
| Hide data URLs | Ẩn base64 resources |
