---
title: Bản Đồ Thế Giới Phần Mềm
description: Tổng quan toàn cảnh thế giới phần mềm — từ nhu cầu người dùng đến cách phần mềm đến tay người dùng.
tags: [software, overview, architecture, lifecycle]
category: software
order: 1
updated: 2026-07-10
---

# Bản Đồ Thế Giới Phần Mềm

> Thế giới phần mềm gồm những gì.
> Một phần mềm được tạo ra như thế nào.
> Người dùng truy cập phần mềm ra sao.
> Những giai đoạn nào sẽ được học ở các tài liệu tiếp theo.

---

## 1. Bức tranh toàn cảnh

Mọi phần mềm đều bắt đầu từ **1 nhu cầu nào đó của con người** 

```text
┌─────────────────────────────────────────────────────────────────────┐
│                          THẾ GIỚI PHẦN MỀM                          │
│                                                                     │
│   ┌──────────┐                                                      │
│   │  NGƯỜI   │  có nhu cầu                                          │
│   │  DÙNG    │───> "Tôi muốn ..."                                   │
│   └────┬─────┘                                                      │
│        │                                                            │
│        v                                                            │
│   ┌──────────┐                                                      │
│   │ NHU CẦU  │  Ví dụ: đặt xe, xem phim, quản lý tài chính          │
│   └────┬─────┘                                                      │
│        │                                                            │
│        v                                                            │
│   ┌───────────────────────────────────────────────────┐             │
│   │             PHẦN MỀM ĐƯỢC TẠO RA                  │             │
│   │                                                   │             │
│   │  Thiết kế → Code → Kiến trúc → Kiểm thử → Deploy  │             │
│   └─────────────────────────┬─────────────────────────┘             │
│                             │                                       │
│                             v                                       │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐                      │
│   │ Web App  │    │ Mobile   │    │ Desktop  │                      │
│   │          │    │ App      │    │ App      │                      │
│   └────┬─────┘    └────┬─────┘    └────┬─────┘                      │
│        │               │               │                            │
│        └───────────────┼───────────────┘                            │
│                        │                                            │
│                        v                                            │
│   ┌─────────────────────────────────────────────┐                   │
│   │           NGƯỜI DÙNG TRUY CẬP               │                   │
│   │     Browser / App Store / Cài đặt trực tiếp │                   │
│   └─────────────────────────────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Hai câu hỏi lớn

Thế giới phần mềm xoay quanh hai câu hỏi:

| Câu hỏi | Ý nghĩa | Tài liệu trả lời |
|----------|---------|------------------|
| Phần mềm **là gì** và **gồm mấy loại**? | Phân loại thế giới phần mềm | [software-types.md](./software-types.md) |
| Phần mềm **được xây dựng** như thế nào? | Kiến trúc & quy trình | [software-architecture.md](./software-architecture.md) |

---

## 3. Lộ trình học

Đây là bản đồ — mỗi file là một vùng đất:

```text
                    software-overview.md
                          │
              ┌───────────┼───────────┐
              v           v           v
        software-     software-    software-
        types.md      architecture  lifecycle.md
                      .md
              │           │           │
              v           v           v
         Phần mềm    Cách phần    Chu kỳ sống
         gồm những   mềm được     từ sinh ra
         gì?         tổ chức?     đến bảo trì
```

### File tiếp theo nên đọc

| Thứ tự | File | Nội dung chính |
|--------|------|----------------|
| 1 | [software-types.md](./software-types.md) | Hệ thống phân loại phần mềm |
| 2 | [software-architecture.md](./software-architecture.md) | Kiến trúc bên trong một phần mềm |
| 3 | [software-lifecycle.md](./software-lifecycle.md) | Chu kỳ sống từ ý tưởng đến bảo trì |

---

## 4. Từ nhu cầu người dùng đến phần mềm

Đây là luồng cơ bản nhất:

```text
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Nhu cầu  │────>│ Thiết kế │────>│ Xây dựng │────>│ Sử dụng  │
│người dùng│     │ phần mềm │     │ phần mềm │     │ phần mềm │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
     │                │                │                │
     v                v                v                v
 "Tôi muốn        "Phần mềm       "Lập trình viên   "Người dùng
  đặt taxi         sẽ có giao      viết code,        mở app,
  nhanh hơn"       diện như         test, deploy"     đặt xe"
                    thế nào?"
```

**Mỗi bước tương ứng với một giai đoạn:**

| Bước | Giai đoạn | Chi tiết |
|------|-----------|----------|
| Nhu cầu | Phân tích | Hiểu người dùng muốn gì |
| Thiết kế | Kiến trúc | Chọn công nghệ, vẽ sơ đồ |
| Xây dựng | Phát triển | Code, test, build |
| Sử dụng | Vận hành | Deploy, monitor, bảo trì |

---

## 5. Phần mềm — Định nghĩa đơn giản

```text
┌─────────────────────────────────────────────┐
│                  PHẦN MỀM                   │
│                                             │
│  ┌────────────┐  ┌───────────┐              │
│  │Instructions│  │   Data    │              │
│  │  (Code)    │  │ (Cấu hình │              │
│  │            │  │ database) │              │
│  └────────────┘  └───────────┘              │
│                                             │
│  ┌─────────────────────────────┐            │
│  │      Documentation          │            │
│  │   (Hướng dẫn, API docs)     │            │
│  └─────────────────────────────┘            │
└─────────────────────────────────────────────┘
```

Phần mềm **không phải phần cứng**. Phần mềm là **tập hợp các chỉ dẫn** telling máy tính phải làm gì.

---

## 6. Ví dụ thực tế

```text
Người dùng: "Muốn đặt xe từ Hà Nội đến Nội Bài"

    │
    v

Phần mềm: Ứng dụng Grab

    │
    ├── Mobile App (iOS/Android)
    ├── Web Dashboard (quản trị)
    ├── Backend Server (xử lý đơn hàng)
    ├── Database (lưu trữ dữ liệu)
    └── Payment Gateway (thanh toán)

    │
    v

Người dùng: Mở app → Nhập địa điểm → Đặt xe → Thanh toán
```

---

## Tổng kết

```text
Thế giới phần mềm:

    Nhu cầu ──> Phân loại ──> Kiến trúc ──> Xây dựng ──> Vận hành
        │            │             │              │             │
        v            v             v              v             v
     software-   software-    software-       software-     software-
     overview     types      architecture    lifecycle     operations
                 (loại PM)   (cách tổ chức)  (chu kỳ sống) (vận hành)
```

đọc tiếp:

- [software-types.md](./software-types.md) — Phần mềm gồm những loại nào?
- [software-architecture.md](./software-architecture.md) — Một phần mềm được tổ chức ra sao?
- [software-lifecycle.md](./software-lifecycle.md) — Phần mềm sinh ra, lớn lên, và già đi như thế nào?
