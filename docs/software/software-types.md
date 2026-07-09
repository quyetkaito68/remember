---
title: Các Loại Phần Mềm
description: Hệ thống phân loại phần mềm — System, Application, Embedded, và mối quan hệ giữa chúng.
tags: [software, types, classification]
category: software
order: 2
updated: 2026-07-10
---

# Các Loại Phần Mềm

> Phần mềm không phải là một khối đồng nhất. Chúng được chia thành nhiều loại dựa trên **vai trò** và **cách chúng hoạt động**.

---

## 1. Phân loại tổng quan

```text
                                    PHẦN MỀM
                                        │
          +─────────────────────────────┼──────────────────────────────+
          v                             v                              v
    System Software               Application Software               Embedded Software
    (Phần mềm hệ thống)           (Phần mềm ứng dụng)               (Phần mềm nhúng)
          │                             │                              │
    +─────+─────+                 +─────+─────+                  +─────+─────+
    v           v                 v           v                  v           v
    OS      Driver              Desktop    Mobile               IoT        Firmware
            Utility             Web App    App
```

---

## 2. System Software

Phần mềm **máy tính cần để hoạt động**. Không có nó, phần mềm khác không chạy được.

```text
┌───────────────────────────────────────────────┐
│           SYSTEM SOFTWARE                     │
│                                               │
│   ┌──────────┐    ┌──────────┐                │
│   │    OS    │    │  Driver  │                │
│   │ Windows  │    │ GPU      │                │
│   │ Linux    │    │ Printer  │                │
│   │ macOS    │    │ Network  │                │
│   └──────────┘    └──────────┘                │
│                                               │
│   ┌──────────┐    ┌──────────┐                │
│   │ Utility  │    │ Runtime  │                │
│   │ Antivirus│    │ .NET     │                │
│   │ Zip      │    │ JVM      │                │
│   │ Backup   │    │ Node.js  │                │
│   └──────────┘    └──────────┘                │
└───────────────────────────────────────────────┘
```

| Loại | Ví dụ | Vai trò |
|------|-------|---------|
| OS | Windows, Linux, macOS | Quản lý phần cứng, chạy ứng dụng |
| Driver | GPU Driver, Printer Driver | Kết nối OS với phần cứng |
| Utility | 7-Zip, Antivirus | Hỗ trợ bảo trì, tối ưu |
| Runtime | JVM, .NET, Node.js | Chạy chương trình ngôn ngữ cao |

---

## 3. Application Software

Phần mềm **con người dùng trực tiếp** để thực hiện công việc.

```text
┌──────────────────────────────────────────────┐
│        APPLICATION SOFTWARE                  │
│                                              │
│   ┌──────────┐    ┌──────────┐               │
│   │  Desktop │    │   Web    │               │
│   │   App    │    │   App    │               │
│   │ VS Code  │    │ Gmail    │               │
│   │ Excel    │    │ Netflix  │               │
│   │ Photoshop│    │ Facebook │               │
│   └──────────┘    └──────────┘               │
│                                              │
│   ┌──────────┐    ┌──────────┐               │
│   │  Mobile  │    │   CLI    │               │
│   │   App    │    │   Tool   │               │
│   │ Grab     │    │ git      │               │
│   │ Shopee   │    │ docker   │               │
│   │ Zalo     │    │ npm      │               │
│   └──────────┘    └──────────┘               │
└──────────────────────────────────────────────┘
```

| Loại | Ví dụ | Đặc điểm |
|------|-------|-----------|
| Desktop App | VS Code, Excel | Cài trên máy, chạy offline |
| Web App | Gmail, Netflix | Truy cập qua browser |
| Mobile App | Grab, Shopee | Cài trên điện thoại |
| CLI Tool | git, docker | Chạy trên terminal |

---

## 4. Embedded Software

Phần mềm **cắm sẵn trong thiết bị phần cứng**. Người dùng không thấy, không cài, không gỡ.

```text
┌───────────────────────────────────────────────┐
│        EMBEDDED SOFTWARE                      │
│                                               │
│   ┌──────────┐    ┌──────────┐                │
│   │   IoT    │    │ Firmware │                │
│   │ Smart    │    │ BIOS     │                │
│   │ Home     │    │ Router   │                │
│   │ Sensor   │    │ Printer  │                │
│   └──────────┘    └──────────┘                │
│                                               │
│   ┌──────────┐    ┌──────────┐                │
│   │   MCU    │    │  RTOS    │                │
│   │ Arduino  │    │ FreeRTOS │                │
│   │ ESP32    │    │ Zephyr   │                │
│   └──────────┘    └──────────┘                │
└───────────────────────────────────────────────┘
```

---

## 5. So sánh 3 loại chính

| Tiêu chí | System | Application | Embedded |
|----------|--------|-------------|----------|
| Ai dùng? | Máy tính | Con người | Thiết bị |
| Thay đổi được? | Khó | Dễ | Rất khó |
| Ảnh hưởng nếu lỗi | Máy tính chết | Mất chức năng | Thiết bị hỏng |
| Ví dụ | Windows | Grab | BIOS |

---

## 6. Mối quan hệ giữa các loại

```text
┌───────────────────────────────────────────────────┐
│                  NGƯỜI DÙNG                       │
│                                                   │
│           Dùng Application Software               │
│              (Grab, Gmail, VS Code)               │
│                      │                            │
│                      v                            │
│          ┌───────────────────────┐                │
│          │   Application chạy    │                │
│          │   trên System Software│                │
│          └───────────┬───────────┘                │
│                      │                            │
│                      v                            │
│          ┌───────────────────────┐                │
│          │   OS quản lý          │                │
│          │   Hardware + Driver   │                │
│          └───────────────────────┘                │
│                                                   │
│   Embedded Software chạy trong thiết bị:          │
│   Smart TV, Router, IoT Sensor                    │
└───────────────────────────────────────────────────┘
```

---

## 7. Theo mô hình phân phối

```text
┌───────────────────────────────────────────────────┐
│                                                   │
│   SaaS ──┐                                        │
│          │  Cloud-based                           │
│   PaaS ──┤  Không cài đặt                         │
│          │  Truy cập qua Internet                 │
│   IaaS ──┘                                        │
│                                                   │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─         │
│                                                   │
│   On-Premise ──  Cài trên máy local               │
│                   Quản lý by user                 │
│                                                   │
└───────────────────────────────────────────────────┘
```

| Mô hình | Ví dụ | Ai quản lý server? |
|---------|-------|---------------------|
| SaaS | Gmail, Salesforce | Nhà cung cấp |
| PaaS | Heroku, Vercel | Nhà cung cấp |
| IaaS | AWS, Azure | Bạn quản lý OS+App |
| On-Premise | ERP tại công ty | Bạn quản lý mọi thứ |

---

## Tổng kết

```text
Phần mềm gồm 3 loại chính:

    System Software ── Cho máy tính hoạt động
    Application Software ── Con người dùng trực tiếp
    Embedded Software ── Ẩn trong thiết bị

Mỗi loại có vai trò riêng, nhưng đều phục vụ 1 mục đích:
Đáp ứng nhu cầu của con người.
```

Đọc tiếp: [software-architecture.md](./software-architecture.md) — Một phần mềm bên trong được tổ chức ra sao?
