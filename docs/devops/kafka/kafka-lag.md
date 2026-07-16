---
title: Apache Kafka — Theo Dõi & Xử Lý Lag
description: Cách xem lag, nguyên nhân lag tăng cao và các biện pháp xử lý trong Kafka
tags: [kafka, lag, consumer-group, monitoring, devops]
category: 'devops/kafka'
updated: 2026-07-15
order: 3
---

# Apache Kafka — Theo Dõi & Xử Lý Lag

> Lag là số message chưa được consumer xử lý. LAG tăng liên tục là dấu hiệu hệ thống bị quá tải hoặc lỗi.

---

## 1. Lag là gì?

Kafka lưu message theo offset (vị trí). Consumer đọc đến offset `X`, trong khi offset cuối cùng trong partition là `Y`:

```text
LAG = Y - X
```

- **LAG = 0** → Consumer đang xử lý kịp.
- **LAG tăng dần** → Consumer chậm, cần xử lý.
- **LAG giảm dần** → Consumer đang catch up.

---

## 2. Xem Lag

### 2.1. CLI

```bash
# Xem lag tất cả consumer groups
bin/kafka-consumer-groups.sh --list --bootstrap-server localhost:9092

# Xem chi tiết lag theo group
bin/kafka-consumer-groups.sh --describe --group my-group \
  --bootstrap-server localhost:9092
```

Kết quả:

```text
GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
my-group        my-topic        0          1024            1050            26
my-group        my-topic        1          512             520             8
my-group        my-topic        2          256             260             4
```

### 2.2. GUI

Các tool như [Kafka UI](https://github.com/provectus/kafka-ui), [Kafkio](https://kafkio.com/), [Conduktor](https://www.conduktor.io/) đều hiển thị lag theo group + partition với giao diện trực quan.

---

## 3. Nguyên nhân lag tăng cao

| Nguyên nhân | Dấu hiệu |
|-------------|----------|
| Consumer xử lý chậm | LAG tăng đều, throughput thấp |
| Database query chậm | Consumer timeout, log lỗi DB |
| API call bên ngoài timeout | Log lỗi connection timeout |
| Số consumer ít hơn partition | Partition bị bỏ trống |
| Consumer crash | Consumer biến mất khỏi group |
| Partition tăng đột ngột | Rebalancing đang diễn ra |

---

## 4. Xử lý lag

### 4.1. Tăng số consumer trong group

```bash
# Số consumer tối đa = số partition
bin/kafka-topics.sh --describe --topic my-topic --bootstrap-server localhost:9092 | grep "Partition"
```

- Nếu topic có 3 partition → tối đa 3 consumer trong group.
- Thêm consumer sẽ idle (không có partition để xử lý).

### 4.2. Kiểm tra logic xử lý

- Xem log consumer: query DB có chậm không? API call có timeout không?
- Tối ưu batch processing thay vì xử lý từng message.

### 4.3. Tăng partition (nếu cần)

```bash
bin/kafka-topics.sh --alter --topic my-topic \
  --partitions 6 \
  --bootstrap-server localhost:9092
```

> **Lưu ý:** Chỉ tăng partition, không giảm. Tăng partition có thể ảnh hưởng đến key-based ordering.

### 4.4. Reset offset (khi cần xử lý lại)

```bash
# Reset về đầu
bin/kafka-consumer-groups.sh --topic my-topic --group my-group \
  --reset-offsets --to-earliest --execute \
  --bootstrap-server localhost:9092

# Reset về offset cụ thể
bin/kafka-consumer-groups.sh --topic my-topic --group my-group \
  --reset-offsets --to-offset 1000 --execute \
  --bootstrap-server localhost:9092
```

> **Cảnh báo:** Cần tắt consumer group trước khi reset offset.

---

## 5. Monitor lag dài hạn

| Phương pháp | Mô tả |
|-------------|-------|
| **JMX + Prometheus** | Export JMX metrics từ Kafka broker/consumer, query bằng Grafana |
| **Burrow** | Tool monitor lag tự động, gửi alert khi lag vượt ngưỡng |
| **Conduktor / Kafkio** | Dashboard GUI hiển thị lag real-time |

---

*Tài liệu được tạo ngày 15-07-2026 — Theo dõi và xử lý Lag trong Kafka.*
