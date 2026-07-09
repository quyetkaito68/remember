---
title: Chu Kỳ Sống Phần Mềm
description: Phần mềm đi qua các giai đoạn — từ ý tưởng đến bảo trì, retirement. Quy trình SDLC và DevOps.
tags: [software, lifecycle, sdlc, devops, maintenance]
category: software
order: 4
updated: 2026-07-10
---

# Chu Kỳ Sống Phần Mềm

> Phần mềm không tồn tại mãi mãi. Nó **sinh ra**, **lớn lên**, **hoạt động**, và **chết đi**. Hiểu chu kỳ sống giúp bạn xây dựng phần mềm bền vững.

---

## 1. Tổng quan chu kỳ sống

```text
┌─────────────────────────────────────────────────────────────┐
│                CHU KỲ SỐNG PHẦN MỀM (SDLC)                  │
│                                                             │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│   │1. Phân   │───>│2. Thiết  │───>│3. Phát   │              │
│   │ tích     │    │ kế       │    │ triển    │              │
│   └──────────┘    └──────────┘    └──────────┘              │
│        │                                │                   │
│        │              ┌──────────┐      │                   │
│        │              │6. Bảo    │<─────┤                   │
│        │              │ trì      │      │                   │
│        │              └──────────┘      │                   │
│        │                  │             v                   │
│        │                  │      ┌──────────┐               │
│        │                  │      │4. Kiểm   │               │
│        │                  │      │ thử     │                │
│        │                  │      └──────────┘               │
│        │                  │             │                   │
│        │                  │             v                   │
│        │                  │      ┌──────────┐               │
│        └──────────────────┘      │5. Triển  │               │
│                                  │ khai     │               │
│                                  └──────────┘               │
│                                                             │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─           │
│   Giai đoạn 7: Retirement (Ngừng hoạt động)                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Chi tiết từng giai đoạn

### Giai đoạn 1: Phân tích nhu cầu

```text
┌─────────────────────────────────────┐
│     PHÂN TÍCH NHU CẦU               │
│                                     │
│   User: "Muốn đặt xe nhanh hơn"     │
│              │                      │
│              v                      │
│   ┌─────────────────────┐           │
│   │ Yêu cầu chức năng:  │           │
│   │ - Đặt xe            │           │
│   │ - Theo dõi xe       │           │
│   │ - Thanh toán online │           │
│   │ - Đánh giá tài xế   │           │
│   └─────────────────────┘           │
└─────────────────────────────────────┘
```

**Output:** Software Requirements Specification (SRS)

---

### Giai đoạn 2: Thiết kế

```text
┌─────────────────────────────────────┐
│        THIẾT KẾ                     │
│                                     │
│   Kiến trúc: Microservices          │
│                                     │
│   ┌──────┐ ┌──────┐ ┌──────┐        │
│   │ User │ │Ride  │ │Pay   │        │
│   │Svc   │ │Svc   │ │Svc   │        │
│   └──────┘ └──────┘ └──────┘        │
│                                     │
│   Database: PostgreSQL              │
│   Cache: Redis                      │
│   Message Queue: RabbitMQ           │
└─────────────────────────────────────┘
```

**Output:** Architecture Document, Database Schema, API Design

---

### Giai đoạn 3: Phát triển (Coding)

```text
┌─────────────────────────────────────┐
│        PHÁT TRIỂN                   │
│                                     │
│   Sprint 1: User Service            │
│   Sprint 2: Ride Service            │
│   Sprint 3: Payment Service         │
│   Sprint 4: Integration             │
│                                     │
│   ┌─────────────────────────┐       │
│   │  Git Workflow            │      │
│   │                          │      │
│   │  main ──> develop ──> PR │      │
│   │            │             │      │
│   │         feature/*        │      │
│   └─────────────────────────┘       │
└─────────────────────────────────────┘
```

**Output:** Source Code, Unit Tests

---

### Giai đoạn 4: Kiểm thử

```text
┌─────────────────────────────────────┐
│        KIỂM THỬ                     │
│                                     │
│   ┌──────────┐                      │
│   │ Unit Test│  Test từng function  │
│   └────┬─────┘                      │
│        │                            │
│   ┌────v─────┐                      │
│   │Integration│ Test kết nối        │
│   │ Test     │  giữa các module     │
│   └────┬─────┘                      │
│        │                            │
│   ┌────v─────┐                      │
│   │  E2E     │  Test toàn bộ flow   │
│   │  Test    │  như người dùng      │
│   └──────────┘                      │
└─────────────────────────────────────┘
```

**Output:** Test Report, Bug Fixes

---

### Giai đoạn 5: Triển khai (Deploy)

```text
┌─────────────────────────────────────┐
│        TRIỂN KHAI                   │
│                                     │
│   CI/CD Pipeline:                   │
│                                     │
│   Code ──> Build ──> Test ──> Deploy│
│     │        │        │        │    │
│     Git    Docker   Test    AWS/    │
│            Image   Suite   Vercel   │
│                                     │
│   Deployment Strategies:            │
│   ├── Blue-Green                    │
│   ├── Canary                        │
│   └── Rolling Update                │
└─────────────────────────────────────┘
```

**Output:** Production Environment, Monitoring Setup

---

### Giai đoạn 6: Bảo trì

```text
┌─────────────────────────────────────┐
│        BẢO TRÌ                      │
│                                     │
│   ┌──────────┐  ┌──────────┐        │
│   │ Corrective│  │ Adaptive │       │
│   │ Fix bug   │  │ Nâng cấp │       │
│   │           │  │ version  │       │
│   └──────────┘  └──────────┘        │
│                                     │
│   ┌──────────┐  ┌──────────┐        │
│   │ Perfective│  │Preventive│       │
│   │ Tối ưu   │  │ Refactor │        │
│   │ performance│ │预防bug  │          │
│   └──────────┘  └──────────┘        │
└─────────────────────────────────────┘
```

---

## 3. DevOps — Đưa Development và Operations lại gần nhau

```text
Trước DevOps:
┌──────────┐              ┌──────────┐
│  Dev     │── "Xong rồi"──>│  Ops    │
│ (Viết    │              │ (Deploy,  │
│  code)   │<── "Bug!"────│  chạy)    │
└──────────┘              └──────────┘
    ↓                           ↓
  Silo                       Silo

Sau DevOps:
┌─────────────────────────────────────┐
│           DevOps Loop               │
│                                     │
│   Plan ──> Code ──> Build           │
│     ▲                   │           │
│     │                   v           │
│   Monitor <── Deploy <── Test       │
│                                     │
│   Continuous Integration            │
│   Continuous Delivery               │
└─────────────────────────────────────┘
```

---

## 4. So sánh mô hình phát triển

| Mô hình | Đặc điểm | Phù hợp |
|---------|-----------|----------|
| Waterfall | Tuần tự, không quay lại | Dự án rõ ràng, ít thay đổi |
| Agile | Iterative, linh hoạt | Hầu hết dự án hiện đại |
| Scrum | Agile với Sprint 2 tuần | Team 5-9 người |
| Kanban | Không Sprint, liên tục | Support,运维 |
| DevOps | Dev + Ops liên tục | Hệ thống production |

---

## 5. Tuổi thọ phần mềm

```text
┌──────────────────────────────────────────────────┐
│                                                  │
│   Năng suất                                      │
│      │                                           │
│      │    ╱╲        Maintenance                  │
│      │   ╱  ╲       Phase                        │
│      │  ╱    ╲─────────────────────╲             │
│      │ ╱  Dev ╲                     ╲            │
│      │╱        ╲                     ╲           │
│      ┼──────────╲─────────────────────╲───> Time │
│      │ Start     Peak               Decline      │
│      │                                   │       │
│      │                    Retirement     │       │
│      │                    (Ngừng hỗ trợ) │       │
└──────────────────────────────────────────────────┘
```

---

## 6. Tổng kết

```text
Chu kỳ sống phần mềm:

    Phân tích ──> Thiết kế ──> Phát triển ──> Kiểm thử
         │                                        │
         │                                        v
         │                                   Triển khai
         │                                        │
         └────────────── <──── Bảo trì <──────────┘

Mỗi giai đoạn có output riêng:
    SRS → Architecture → Code → Test → Deploy → Maintenance
```

Đọc thêm:
- [software-overview.md](./software-overview.md) — Quay lại bản đồ thế giới phần mềm
- [software-types.md](./software-types.md) — Phân loại phần mềm
- [software-architecture.md](./software-architecture.md) — Kiến trúc bên trong phần mềm
