---
title: Application Panel
description: "Application Panel trong Chrome DevTools — inspect và quản lý LocalStorage, SessionStorage, IndexedDB, Cookies, Cache Storage, Service Worker"
tags: [application-panel, devtools, storage-inspector, service-worker, cache-storage]
category: developer
updated: 2026-07-26
order: 25
---

# Application Panel

Inspect + quản lý tất cả storage và Service Worker trong browser.

---

## Panel Layout

```text
┌──────────────────────────────────────────────────────────────┐
│  Application Panel                                           │
│                                                              │
│  ┌─────────────────┐ ┌────────────────────────────────────┐  │
│  │  Storage Tree   │ │  Content View                      │  │
│  │  v Manifest     │ │  Key | Value                       │  │
│  │  v Service      │ │  theme| dark                       │  │
│  │    Workers      │ │  lang | vi                         │  │
│  │  v Storage      │ │  token| eyJhbGci...                │  │
│  │    Local Storage│ │                                    │  │
│  │    Session Stor.│ │  [+ Add] [Delete] [Clear]          │  │
│  │    IndexedDB    │ │                                    │  │
│  │    Cookies      │ │                                    │  │
│  │  v Cache Storage│ │                                    │  │
│  │  v Frames       │ │                                    │  │
│  └─────────────────┘ └────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## Storage Overview

| Type | Scope | Capacity | Persistent |
|------|-------|----------|------------|
| LocalStorage | Origin | ~5-10MB | Yes |
| SessionStorage | Tab | ~5-10MB | No (tab) |
| IndexedDB | Origin | ~50%+ disk | Yes |
| Cookies | Domain | ~4KB/cookie | Configurable |
| Cache Storage | Origin | Dynamic | Yes |

---

## Service Worker Debugging

```text
SW Lifecycle:
  Register → Install → Activate → Running (intercept fetch)
```

| Action | Mô tả |
|--------|--------|
| **Unregister** | Xóa service worker |
| **Update** | Force update SW |
| **Start/fetch** | Trigger fetch event |
| **Push Messaging** | Simulate push notification |

---

## Manifest (PWA)

```text
Name, Short Name, Display: standalone, Theme Color, Icons (192px, 512px)
```

---

## Debugging Checklist

| # | Check | Location |
|---|-------|----------|
| 1 | LocalStorage keys/values | Storage → Local Storage |
| 2 | Cookies (domain, Secure, HttpOnly) | Storage → Cookies |
| 3 | IndexedDB data | Storage → IndexedDB |
| 4 | Cache Storage entries | Cache Storage |
| 5 | SW status + update | Service Workers |
| 6 | PWA manifest validity | Manifest |
| 7 | Frame tree (iframes) | Frames |

---

## Clear Storage

```text
☑ Service Workers    ☑ Local Storage    ☑ Cache Storage
☑ Session Storage    ☑ IndexedDB        ☑ Cookies
[Clear site data]
```

---

Xem thêm: [Chrome DevTools Tổng Quan](19-chrome-devtools.md) | [Web Storage](13-web-storage.md) | [Service Worker & PWA](14-service-worker-pwa.md)