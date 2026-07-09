---
title: Kiến Trúc Phần Mềm
description: Cách một phần mềm được tổ chức bên trong — từ mô hình-layered đến microservices.
tags: [software, architecture, design, pattern]
category: software
order: 3
updated: 2026-07-10
---

# Kiến Trúc Phần Mềm

> Một phần mềm không phải một cục code duy nhất. Nó được **chia lớp**, **chia module**, và **kết nối** theo kiến trúc cụ thể.

---

## 1. Tại sao cần kiến trúc?

```text
Không có kiến trúc:
┌──────────────────────────────────────┐
│  main.py (5000 dòng)                 │
│  - login                             │
│  - payment                           │
│  - notification                      │
│  - database                          │
│  - UI                                │
│  → Khó bảo trì, khó debug, khó scale │
└──────────────────────────────────────┘

Có kiến trúc:
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Auth     │  │ Payment  │  │ Notify   │
│ Module   │  │ Module   │  │ Module   │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     └─────────────┼─────────────┘
                   │
            Core / Shared Layer
```

---

## 2. Mô hình Layered Architecture (Phổ biến nhất)

```text
┌─────────────────────────────────────────────────┐
│          PRESENTATION LAYER                     │
│  (Giao diện: Web, Mobile, Desktop)              │
│                                                 │
│  HTML/CSS/JS  │  React  │  Flutter              │
└───────────────┬─────────────────────────────────┘
                │
                v
┌─────────────────────────────────────────────────┐
│          BUSINESS LOGIC LAYER                   │
│  (Quy tắc nghiệp vụ: tính tiền,                 │
│   xác thực, xử lý đơn hàng)                     │
│                                                 │
│  UserService  │  OrderService  │ ...            │
└───────────────┬─────────────────────────────────┘
                │
                v
┌─────────────────────────────────────────────────┐
│          DATA ACCESS LAYER                      │
│  (Đọc/ghi database, cache, file)                │
│                                                 │
│  Repository  │  ORM  │  Cache                   │
└───────────────┬─────────────────────────────────┘
                │
                v
┌─────────────────────────────────────────────────┐
│          DATABASE LAYER                         │
│  (Nơi dữ liệu được lưu trữ)                     │
│                                                 │
│  MySQL  │  PostgreSQL  │  MongoDB               │
└─────────────────────────────────────────────────┘
```

**Nguyên tắc:** Mỗi layer chỉ giao tiếp với layer liền kề bên dưới.

---

## 3. Mô hình Client-Server

```text
┌──────────┐         ┌──────────┐         ┌──────────┐
│  Client  │<───────>│  Server  │<───────>│ Database │
│ (Browser │  HTTP   │ (API,    │   SQL   │ (MySQL,  │
│  /App)   │  Request│  Logic)  │  Query  │  Redis)  │
└──────────┘         └──────────┘         └──────────┘
     │                     │
     v                     v
 Gửi request          Xử lý request
 Nhận response        Trả về data
```

### 3 loại Client-Server

| Loại | Mô tả | Ví dụ |
|------|-------|-------|
| 1-tier | Tất cả trong 1 máy | App desktop đơn giản |
| 2-tier | Client ↔ Server | MySQL + GUI tool |
| 3-tier | Client ↔ API ↔ DB | Web app hiện đại |

---

## 4. Mô hình Microservices

Thay vì 1 ứng dụng lớn, chia thành **nhiều service nhỏ**, mỗi service tự chạy riêng.

```text
┌──────────────────────────────────────────────────────┐
│                    API Gateway                       │
│              (auth, rate limit, route)               │
└──────┬──────────┬──────────┬──────────┬──────────────┘
       │          │          │          │
       v          v          v          v
┌──────────┐┌──────────┐┌──────────┐┌──────────┐
│   User   ││  Order   ││ Payment  ││ Notify   │
│ Service  ││ Service  ││ Service  ││ Service  │
│          ││          ││          ││          │
│ Port:3001││ Port:3002││ Port:3003││ Port:3004│
└────┬─────┘└────┬─────┘└────┬─────┘└────┬─────┘
     │           │           │           │
     v           v           v           v
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ UserDB │ │OrderDB │ │PayDB   │ │NotifDB │
└────────┘ └────────┘ └────────┘ └────────┘
```

### Monolith vs Microservices

| Tiêu chí | Monolith | Microservices |
|----------|----------|---------------|
| Cấu trúc | 1 codebase lớn | Nhiều service nhỏ |
| Deploy | Deploy cả ứng dụng | Deploy từng service |
| Scale | Scale cả app | Scale service cần |
| Debug | Dễ tìm bug | Phức tạp hơn |
| Phù hợp | Startup, dự án nhỏ | Hệ thống lớn, nhiều team |

---

## 5. Mô hình MVP (Model-View-Presenter)

Phổ biến trong ứng dụng **desktop** và **mobile**.

```text
┌──────────┐     ┌──────────┐     ┌──────────┐
│   VIEW   │────>│ PRESENTER│────>│  MODEL   │
│ (Giao    │     │ (Logic   │     │ (Data,   │
│  diện)   │<────│ điều     │<────│ Business)│
│          │     │ khiển)   │     │          │
└──────────┘     └──────────┘     └──────────┘
```

---

## 6. So sánh các mô hình kiến trúc

| Mô hình | Phù hợp | Độ phức tạp | Khả năng scale |
|---------|---------|-------------|----------------|
| Layered | Web app, CRUD | Thấp | Trung bình |
| Client-Server | App phân tán | Trung bình | Cao |
| Microservices | Hệ thống lớn | Cao | Rất cao |
| MVP/MVC | Desktop, Mobile | Trung bình | Trung bình |
| Event-Driven | Real-time, IoT | Cao | Rất cao |

---

## 7. Bức tranh tổng thể

```text
┌──────────────────────────────────────────────────┐
│              KIẾN TRÚC PHẦN MỀM                  │
│                                                  │
│   Layered ──────> Phổ biến nhất                  │
│       │                                          │
│       ├── Presentation (UI)                      │
│       ├── Business Logic (Nghiệp vụ)             │
│       ├── Data Access (Database)                 │
│       └── Infrastructure (Hạ tầng)               │
│                                                  │
│   Microservices ──> Phức tạp, scale tốt          │
│       │                                          │
│       ├── Service A (User)                       │
│       ├── Service B (Order)                      │
│       ├── Service C (Payment)                    │
│       └── API Gateway                            │
│                                                  │
│   Chọn mô hình phù hợp với:                      │
│       - Quy mô dự án                             │
│       - Số lượng team                            │
│       - Yêu cầu scale                            │
└──────────────────────────────────────────────────┘
```

---

## Tổng kết

```text
Kiến trúc phần mềm = Cách tổ chức code bên trong

    Layered     ── Đơn giản, phổ biến
    Microservices ── Phức tạp, scale tốt
    MVP/MVC     ── Phù hợp UI apps

Chọn đúng kiến trúc = Dễ bảo trì, dễ scale, dễ debug
Chọn sai kiến trúc = Dự án chết chậm
```

Đọc tiếp: [software-lifecycle.md](./software-lifecycle.md) — Phần mềm sinh ra, lớn lên, và già đi như thế nào?
