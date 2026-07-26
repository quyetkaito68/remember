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
│  Name          Method  Status  Size     Time   Waterfall     │
│  ─────────────────────────────────────────────────────────── │
│  index.html    GET     200     14.2 KB  85ms   ████████      │
│  style.css     GET     304     0 B      23ms   ██            │
│  app.js        GET     200     52.1 KB  142ms  ████████████  │
│  api/user      GET     200     1.2 KB   245ms  ████████████  │
├──────────────────────────────────────────────────────────────┤
│  8 requests  |  260 KB transferred  |  1.2 MB resources      │
│  Finish: 1.2s  |  DOMContentLoaded: 850ms  |  Load: 1.2s     │
└──────────────────────────────────────────────────────────────┘
```

---

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
