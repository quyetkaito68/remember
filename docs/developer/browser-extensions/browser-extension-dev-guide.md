---
title: Hướng Dẫn Phát Triển & Publish Browser Extension
description: Cách cấu trúc project, test tại local, và publish extension lên Chrome Web Store, Firefox Add-ons, Edge Add-ons
tags: [browser-extension, chrome-extension, publish, development]
category: developer
updated: 2026-07-12
order: 2
---

# Hướng Dẫn Phát Triển & Publish Browser Extension

> Bài viết hướng dẫn practical: cấu trúc project, test local trên các browser, và publish extension để người khác có thể cài đặt sử dụng.

---

## Cấu Trúc Project

Dùng WXT hoặc Plasmo sẽ generate cấu trúc tự nhiên, nhưng đây là cấu trúc cơ bản để hiểu:

```
my-extension/
├── src/
│   ├── background/
│   │   └── index.ts          Service Worker
│   ├── content/
│   │   └── index.ts          Content Script
│   ├── popup/
│   │   ├── index.html
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── sidepanel/
│   │   ├── index.html
│   │   └── App.tsx
│   ├── options/
│   │   ├── index.html
│   │   └── App.tsx
│   ├── services/
│   │   ├── storage.ts        chrome.storage wrapper
│   │   ├── tab.ts            chrome.tabs wrapper
│   │   └── message.ts        Message Passing wrapper
│   └── utils/
│       └── index.ts
├── public/
│   └── icon.png              Extension icon
├── manifest.json             Manifest V3 config
├── package.json
└── wxt.config.ts             hoặc plasmo.config.ts
```

**Quy tắc tách business logic khỏi Chrome API:** Tạo wrapper services (`storage.ts`, `tab.ts`, `message.ts`) để tách biệt code business logic khỏi Chrome API. Điều này giúp unit test dễ dàng hơn và có thể reuse logic nếu port sang web app.

---

## Test Tại Local

### Chrome (Chromium-based)

```text
┌────────────────────────────────────────────────┐
│           Chrome Extension Testing             │
├────────────────────────────────────────────────┤
│                                                │
│  1. chrome://extensions                        │
│     - Bật "Developer mode"                     │
│     - Click "Load unpacked"                    │
│     - Chọn thư mục build/dist                  │
│                                                │
│  2. Verify                                     │
│     - Icon hiện trên toolbar                   │
│     - Click popup hiển thị đúng                │
│     - Content script chạy trên trang           │
│                                                │
│  3. DevTools                                   │
│     - F12 trên popup                           │
│     - Service Worker: inspect trong            │
│       chrome://extensions > Service            │
│       Worker > "inspect"                       │
│     - Content Script: F12 trên trang           │
│       web, tab Console                         │
│                                                │
└────────────────────────────────────────────────┘
```

**Hot reload:** Nếu dùng WXT hoặc Plasmo, save file sẽ tự động reload extension. Nếu dev thủ công, phải click nút reload trên `chrome://extensions` mỗi lần thay đổi.

### Firefox

```
1. about:debugging#/runtime/this-firefox
2. Click "Load Temporary Add-on..."
3. Chọn manifest.json trong thư mục build
4. Verify tương tự Chrome
```

**Lưu ý:** Firefox không hỗ trợ hot reload. Mỗi lần thay đổi phải unload rồi load lại.

### Edge

```
1. edge://extensions
2. Bật "Developer mode"
3. Click "Load unpacked"
4. Chọn thư mục build
```

Edge dùng chung Chromium nên quy trình giống hệt Chrome.

### Safari

Safari yêu cầu thêm bước convert sang Safari Web Extension bằng Xcode. Không thể test trực tiếp từ thư mục build như Chrome/Firefox.

---

## Publish Extension

### Chrome Web Store

**Chi phí:** $5 one-time fee (đăng ký developer account).

```text
┌──────────────────────────────────────────────────┐
│          Chrome Web Store Publishing             │
├──────────────────────────────────────────────────┤
│                                                  │
│  1. Build production                             │
│     npm run build                                │
│                                                  │
│  2. Zip thư mục build                            │
│     Compress dist/ thành extension.zip           │
│                                                  │
│  3. Đăng nhập Chrome Web Store Dashboard         │
│     https://chrome.google.com/webstore/          │
│     developer/dashboard                          │
│                                                  │
│  4. Click "New Item"                             │
│     - Upload extension.zip                       │
│     - Điền listing: title, description,          │
│       icon, screenshots                          │
│     - Chọn category và visibility                │
│                                                  │
│  5. Submit for review                            │
│     - Review thường mất 1-7 ngày                 │
│     - Nếu reject sẽ có feedback cụ thể           │
│     - Có thể appeal nếu không đồng ý             │
│                                                  │
│  6. Sau khi approve                              │
│     - Extension xuất hiện trên store             │
│     - Auto-update khi publish bản mới            │
│     - Version phải lớn hơn bản trước             │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Lưu ý khi submit:**
- Extension phải có privacy policy nếu collects user data
- Screenshots phải rõ ràng, minh họa functionality
- Description phải accurate, không misleading
- Nên test kỹ trên latest stable Chrome trước khi submit

### Firefox Add-ons (AMO)

**Chi phí:** Miễn phí.

```
1. Build production
2. Zip thư mục build
3. Đăng nhập https://addons.mozilla.org/developer/
4. Submit a New Add-on
   - Upload zip
   - Điền listing info
   - Chọn license
5. Manual review (thường nhanh hơn Chrome, 1-3 ngày)
6. Sau khi approve -> xuất hiện trên addons.mozilla.org
```

### Edge Add-ons

**Chi phí:** Miễn phí.

```
1. Build production
2. Zip thư mục build
3. Đăng nhập https://partner.microsoft.com/dashboard/edge/submit
4. Submit extension
   - Upload zip
   - Điền listing info
5. Review (thường 1-3 ngày)
6. Sau khi approve -> xuất hiện trên Microsoft Edge Add-ons
```

---

## Checklist Trước Khi Publish

| # | Mục | Kiểm tra |
|---|------|----------|
| 1 | Manifest | Version number tăng đúng, permissions chỉ lấy cần thiết |
| 2 | Icon | Có đủ size: 16x16, 48x48, 128x128 |
| 3 | Description | Rõ ràng, không spam keyword |
| 4 | Privacy | Có privacy policy nếu collect data |
| 5 | Test | Đã test trên latest stable browser |
| 6 | Error handling | Không có unhandled error trong console |
| 7 | Performance | Không gây lag, không memory leak |
| 8 | Security | Không hardcode API key, không eval() |

---

## Native Messaging (Bonus)

Nếu extension cần chạy code native trên máy tính (đọc file, chạy script), dùng **Native Messaging** — giao tiếp giữa extension và một native app (Python, Node.js, Go...).

```text
┌────────────┐    JSON     ┌────────────┐   stdin/stdout  ┌────────────┐
│  Content   │------------>|  Service   |---------------->|   Native   │
│  Script    |<------------|  Worker    |<----------------|    App     │
└────────────┘   Message   └────────────┘      JSON       └────────────┘
```

Native app phải được register trên máy client. Phù hợp cho extension cần truy cập file system hoặc chạy algorithm phức tạp.

---

## Tổng kết

Test tại local đơn giản với `Load unpacked`. Publish cần zip extension, submit lên store tương ứng, đợi review. Chrome Web Store tốn $5, còn Firefox và Edge miễn phí. Luôn luôn test kỹ và tuân thủ security best practices trước khi submit.
