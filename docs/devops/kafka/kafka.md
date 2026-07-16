---
title: Apache Kafka — Tổng Quan
description: 'Kafka là gì, mô hình pub-sub, kiến trúc và các công cụ GUI quản lý Kafka'
tags: [kafka, apache-kafka, pub-sub, message-queue, devops]
category: 'devops/kafka'
updated: 2026-07-15
order: 1
---

# Apache Kafka — Tổng Quan

> Apache Kafka là nền tảng streaming phân tán mã nguồn mở, dùng để truyền tải sự kiện (event) thời gian thực giữa các hệ thống trong kiến trúc microservices.

---

## 1. Kafka là gì?

Kafka hoạt động như một **hệ thống message broker phân tán** — lưu trữ và chuyển tiếp message giữa producer (người gửi) và consumer (người nhận) theo mô hình pub-sub.

**Đặc điểm chính:**

- **Throughput cao:** Hàng triệu message/giây, độ trệmillisecond.
- **Lưu trữ bền vững:** Message ghi disk theo thứ tự, hỗ trợ replay lại dữ liệu.
- **Scale ngang:** Thêm broker vào cluster để mở rộng.
- **Fault-tolerant:** Dữ liệu replicate tự động giữa các broker.

---

## 2. Mô hình Pub/Sub

```text
┌──────────┐          ┌─────────────────────────────┐           ┌──────────────┐
│          │  publish │         Kafka Cluster       │  subscribe│              │
│ Producer │ ───────► │  Topic A: [P0] [P1] [P2]    │ ───────►  │   Consumer   │
│          │          │                             │           │   Group A    │
└──────────┘          │  Topic B: [P0] [P1]         │           └──────────────┘
                      │                             │
                      │  Broker 1    Broker 2       │          ┌──────────────┐
                      │  (leader)    (follower)     │ ───────► │   Consumer   │
                      │                             │          │   Group B    │
                      └─────────────────────────────┘          └──────────────┘
```

- **Producer** gửi message vào **Topic** (kênh dữ liệu).
- **Consumer** đăng ký Topic và nhận message.
- Nhiều consumer group đọc cùng topic độc lập với nhau.
- Message lưu theo thứ tự, consumer tự quản lý offset (vị trí đọc).

---

## 3. Kiến trúc cơ bản

| Khái niệm | Vai trò |
|-----------|---------|
| **Broker** | Node trong cluster, lưu trữ và phục vụ dữ liệu |
| **Topic** | Kênh logic phân loại message (ví dụ: `order-events`, `user-clicks`) |
| **Partition** | Topic chia thành nhiều partition để phân tán tải |
| **Replica** | Mỗi partition có nhiều bản sao trên các broker khác nhau |
| **Producer** | Ứng dụng gửi message vào topic |
| **Consumer** | Ứng dụng đọc message từ topic |
| **Consumer Group** | Nhóm consumer chia nhau xử lý partition |
| **Zookeeper / KRaft** | Quản lý metadata cluster, leader election |

---

## 4. Ứng dụng trong hệ thống

| Use case | Mô tả |
|-----------|-------|
| **Event-driven microservices** | Service giao tiếp qua sự kiện thay vì REST API trực tiếp |
| **Log aggregation** | Tập trung log từ nhiều server để xử lý và phân tích |
| **Stream processing** | Xử lý dữ liệu real-time (tính toán, filter, transform) |
| **Data integration** | Kết nối các hệ thống khác nhau (DB, cache, search engine) |
| **Activity tracking** | Theo dõi hành vi user, clickstream analysis |
| **IoT data ingestion** | Thu thập dữ liệu từ thiết bị IoT hàng loạt |

---

## 5. Công cụ GUI quản lý Kafka

Thay vì dùng CLI, có nhiều công cụ giao diện đồ họa giúp thao tác Kafka dễ dàng hơn:

### 5.1. Kafka UI (opensource)

| Tool | Link | Đặc điểm |
|------|------|-----------|
| **Kafka UI** | [https://github.com/provectus/kafka-ui](https://github.com/provectus/kafka-ui) | Web UI miễn phí, docker deploy đơn giản, xem topic/consumer/lag |
| **AKHQ** | [https://github.com/tchiotludo/akhq](https://github.com/tchiotludo/akhq) | Kotlin-based, hỗ trợ Kafka + Schema Registry + Connect |
| **UI for Apache Kafka** | [https://github.com/Blizzard/ui-for-kafka](https://github.com/Blizzard/ui-for-kafka) | Desktop app, cross-platform |

### 5.2. Managed / Cloud tools

| Tool | Link | Đặc điểm |
|------|------|-----------|
| **Kafkio** | [https://kafkio.com/](https://kafkio.com/) | Web-based, connect trực tiếp cluster, xem topic/message/consumer group |
| **Conduktor** | [https://www.conduktor.io/](https://www.conduktor.io/) | Desktop + web, GUI đầy đủ, hỗ trợ schema registry |
| **Lenses.io** | [https://lenses.io/](https://lenses.io/) | Enterprise, stream processing GUI |

### 5.3. Các chức năng phổ biến trên GUI

Tất cả các tool trên đều hỗ trợ:

- **Xem danh sách Topic** — tên, partition, replication factor, config
- **Xem/Send message** — browse message theo offset, search theo key
- **Xem Consumer Group** — danh sách group, lag per partition
- **Xem Cluster** — broker status, partition leader, ISR
- **Tạo/Xoá Topic** — trực tiếp từ giao diện
- **Reset offset** — consumer group offset management

---

## 6. Tài liệu liên quan

| File | Nội dung |
|------|----------|
| [`kafka-setup.md`](./kafka-setup.md) | Cài đặt, cấu hình, các lệnh CLI, xử lý sự cố |
| [`kafka-lag.md`](./kafka-lag.md) | Theo dõi và xử lý Lag trong Kafka |

---

*Tài liệu được cập nhật ngày 15-07-2026.*
