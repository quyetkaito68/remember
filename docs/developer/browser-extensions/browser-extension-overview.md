---
title: Tổng Quan Browser Extension
description: Giới thiệu toàn diện về browser extension — kiến trúc, khả năng, hạn chế, framework và stack phát triển năm 2026
tags: [browser-extension, chrome-extension, manifest-v3, web-extension]
category: developer
updated: 2026-07-12
order: 1
---

# Tổng Quan Browser Extension

> Browser extension là chương trình nhỏ chạy trong trình duyệt, mở rộng khả năng của trình duyệt mà không cần chỉnh sửa code gốc.

---

## Browser Extension là gì

Browser extension là một gói ứng dụng nhỏ (HTML, CSS, JavaScript) được cài vào trình duyệt web. Nó có quyền truy cập vào các API mà web page thông thường không có — đọc/sửa nội dung trang, giao tiếp với background service, thao tác storage, hiển thị popup, v.v.

Tất cả các trình duyệt hiện đại đều hỗ trợ chuẩn **WebExtensions API** — một API chung dựa trên tiêu chuẩn W3C. Chrome, Edge, Brave, Opera, Vivaldi dùng chung nền tảng Chromium nên extension viết cho Chrome gần như chạy được trên tất cả các browser này.

---

## Browser Extension có thể làm gì

| Khả năng | Ví dụ cụ thể |
|----------|---------------|
| Đọc và sửa nội dung trang web | Ẩn quảng cáo, đổi font chữ, dịch trang |
| Thêm UI vào trang web | Nút floating, panel bên cạnh, tooltip |
| Giao tiếp với API bên ngoài | Gọi OpenAI API để tóm tắt trang, gọi API thời tiết |
| Lưu dữ liệu locally | Ghi nhớ cài đặt người dùng, cache dữ liệu |
| Chạy background task | Kiểm tra email mỗi 5 phút, đồng bộ dữ liệu |
| Chụp và phân tích màn hình | Screenshot trang, OCR văn bản từ ảnh |
| Tự động hóa thao tác | Auto-fill form, tự động điền thông tin |
| Kiểm soát tab và window | Mở tab mới, group tab, quản lý nhiều window |
| Chèn sidebar/panel | Translator panel, note-taking panel, CRM assistant |
| Hook vào network request | Modify headers, proxy request, debug API call |

---

## Browser Extension không thể làm gì

| Hạn chế | Giải thích |
|---------|-----------|
| Chạy background vĩnh viễn | Service Worker bị kill sau ~30s idle, phải dùng alarms API |
| Truy cập file system | Không đọc được file trên ổ cứng, chỉ truy cập được downloads/ |
| Thực thi code ngoài sandbox | Không chạy được binary, native code (trừ Native Messaging) |
| Modify trang `chrome://` | Bị chặn security |
| Bypass CORS | Extension vẫn phải tuân thủ CORS khi fetch từ content script |
| Access cookies domain khác | Bị giới hạn theo `host_permissions` trong manifest |
| Publish không cần review | Chrome Web Store duyệt thủ công, có thể mất 1-7 ngày |
| Chạy trên mọi nền tảng mobile | iOS không hỗ trợ extension thực sự (trừ Safari extension iOS 15+) |
| Lưu trữ dữ liệu lớn | `chrome.storage` giới hạn ~10MB (sync) / ~5MB (local) |
| Direct access database | Không chạy được MySQL/PostgreSQL trực tiếp, phải dùng API |

---

## Kiến trúc Browser Extension

```text
┌─────────────────────────────────────────────────────────┐
│                    BROWSER EXTENSION                    │
│                                                         │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐│
│  │    Popup      │  │   Options     │  │  Side Panel   ││
│  │    Page       │  │    Page       │  │               ││
│  └──────┬────────┘  └──────┬────────┘  └──────┬────────┘│
│         │                  │                  │         │
│         └──────────────────┼──────────────────┘         │
│                            │                            │
│                 Message Passing                         │
│                            │                            │
│  ┌─────────────────────────┼─────────────────────────┐  │
│  │                         │                         │  │
│  v                         v                         v  │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐│
│  │  Service      │  │   Content     │  │   Storage     ││
│  │  Worker       │  │   Script      │  │               ││
│  │(Background)   │  │  (per tab)    │  │ chrome.       ││
│  │               │  │               │  │ storage       ││
│  └───────────────┘  └───────────────┘  └───────────────┘│
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Service Worker (Background)

Service Worker chạy ẩn, không có UI. Đây là "trung tâm điều phối" của extension — xử lý sự kiện từ content script, popup, và các browser events (alarm, tab change, install). Manifest V3 yêu cầu dùng Service Worker thay thế cho Background Page (V2).

**Đặc điểm quan trọng:** Service Worker bị browser kill sau khoảng 30 giây không hoạt động. Phải thiết kế lại stateless hoặc persist state vào `chrome.storage`.

### Content Script

Content Script chạy trong ngữ cảnh của trang web (không phải extension context). Nó có thể đọc và sửa DOM của trang. Mỗi tab có thể có nhiều content script riêng biệt. Content Script giao tiếp với Service Worker qua Message Passing.

### Popup

Popup là cửa sổ nhỏ hiện ra khi click vào icon extension. Thường dùng để toggle trạng thái, hiển thị thông tin tóm tắt, hoặc truy cập nhanh tính năng.

### Options Page

Trang cài đặt mở trong tab mới. Dùng để cấu hình extension chi tiết — API key, theme, whitelist, v.v.

### Side Panel

Xu hướng mới từ Chrome 114+. Panel hiển thị bên cạnh trang web, luôn luôn visible. Phù hợp cho translator, note-taking, CRM — những chức năng cần tương tác liên tục.

### Storage

`chrome.storage` lưu dữ liệu extension. Có 3 loại: `local` (không sync, ~5MB), `sync` (sync qua tài khoản, ~100KB), `session` (chỉ trong phiên, ~10MB). Không phù hợp lưu trữ dữ liệu lớn — nên dùng IndexedDB nếu cần.

### Message Passing

Cơ chế giao tiếp giữa các thành phần. Content Script không thể gọi trực tiếp Service Worker — phải dùng `chrome.runtime.sendMessage` hoặc `chrome.tabs.sendMessage`. Phía nhận dùng `chrome.runtime.onMessage` listener.

---

## Ecosystem Browser

```text
                    Browser Extension
                           |
          ┌────────────────┼────────────────┐
          |                |                |
     Chromium          Firefox           Safari
          |                |                |
   ┌──────┼──────┐         |                |
   |      |      |         |                |
 Chrome Edge Brave    Firefox            Safari
       Opera Vivaldi
```

Chrome, Edge, Brave, Opera, Vivaldi đều dựa trên Chromium — extension gần như compatibility 100%. Firefox dùng engine riêng (Gecko) nhưng hỗ trợ WebExtensions API nên code gần như tương thích. Safari dùngWebKit và yêu cầu format riêng (Swift/ObjC wrapper).

---

## So sánh Framework

| Tiêu chí | Plasmo | WXT |
|----------|--------|-----|
| Maintainer | Plasmo Labs (commercial) | Community-driven |
| TypeScript | Built-in, rất mượt | Built-in, mượt |
| React support | Tốt (default) | Tốt |
| Vue support | Có (plugin) | Tốt (plugin) |
| Hot reload | Content Script + Popup + Background | Content Script + Popup + Background |
| Manifest V3 | Hỗ trợ đầy đủ | Hỗ trợ đầy đủ |
| Cross-browser | Chrome, Firefox, Safari | Chrome, Firefox, Edge, Safari |
| DevTools panel | Có | Có |
| Documentation | Khá tốt, có examples | Tốt, có migration guide từ Plasmo |
| Bundle size | Nhỏ | Nhỏ hơn một chút |
| Community | Lớn hơn | Đang phát triển |

### Khi nào chọn Plasmo

- Đã quen với Plasmo hoặc đang migrate từ extension cũ
- Cần ecosystem plugin phong phú
- Team lớn, cần stability từ commercial maintainer

### Khi nào chọn WXT

- Bắt đầu project mới từ đầu
- Muốn lightweight hơn, ít abstraction hơn
- Cần hỗ trợ nhiều browser hơn (đặc biệt Safari)

---

## Stack Khuyến Nghị 2026

```text
┌───────────────────────────┐
│       Manifest V3         │
└─────────────┬─────────────┘
              v
┌───────────────────────────┐
│       TypeScript          │
└─────────────┬─────────────┘
              v
┌───────────────────────────┐
│         React             │
└─────────────┬─────────────┘
              v
┌───────────────────────────┐
│          Vite             │
└─────────────┬─────────────┘
              v
┌───────────────────────────┐
│     WXT hoặc Plasmo       │
└───────────────────────────┘
```

- **Manifest V3** — Bắt buộc. Manifest V2 đã bị Chrome loại bỏ.
- **TypeScript** — Gần như tiêu chuẩn industry. Type safety giúp tránh bug khi code interacts với Chrome API.
- **React** — Đang thắng thế trong ecosystem extension. Vue cũng khả thi nhưng resource hỗ trợ ít hơn.
- **Vite** — Dev server siêu nhanh, hot reload mượt.
- **WXT hoặc Plasmo** — Framework đóng gói, handle build pipeline, cross-browser compatibility.

---

## Xu Hướng 2026

- **AI Extension** — Mảng phát triển mạnh nhất: tóm tắt YouTube, dịch trang web real-time, AI assistant tích hợp vào mọi trang, email assistant, CRM assistant.
- **Side Panel** — Xu hướng UI mới, thay thế popup cho nhiều use case.
- **Message Bus pattern** — Thay vì gọi trực tiếp, dùng event-driven architecture.
- **Không lưu dữ liệu lớn trong chrome.storage** — Dùng IndexedDB hoặc API server-side.
- **Không nhét API key trực tiếp vào extension** — Dùng proxy server hoặc OAuth flow.

---

## Tổng kết

Browser extension là một mảng phát triển hấp dẫn với barrier to entry thấp. Năm 2026, với Manifest V3, TypeScript, và framework như WXT/Plasmo, việc build một extension chuyên nghiệp trở nên dễ dàng hơn bao giờ hết. AI integration đang tạo ra wave mới với nhiều cơ hội sản phẩm sáng tạo.

Xem thêm: [Hướng Dẫn Phát Triển & Publish](browser-extension-dev-guide.md)
