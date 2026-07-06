---
title: Apache Kafka — Thao Tác Trên Linux Server
description: 'Cài đặt, cấu hình, vận hành Kafka trên Linux — các lệnh cơ bản, xem log, xử lý sự cố'
tags: [kafka, apache-kafka, linux, message-queue, devops]
category: 'devops/kafka'
updated: 2026-07-06
order: 1
---

# Apache Kafka — Thao Tác Trên Linux Server

> Hướng dẫn cài đặt, cấu hình và các thao tác vận hành Kafka trên Linux. Dành cho sysadmin/DevOps quản lý cụm Kafka trong môi trường doanh nghiệp.

---

## 1. Cài đặt Kafka

### 1.1. Yêu cầu

- Java 8+ (khuyến nghị Java 11)
- Zookeeper (Kafka 2.x — 3.x vẫn cần; Kafka 3.x+ có thể dùng KRaft thay thế)

### 1.2. Tải và giải nén

```bash
cd /opt
wget https://downloads.apache.org/kafka/3.6.0/kafka_2.13-3.6.0.tgz
tar -xzf kafka_2.13-3.6.0.tgz
ln -s kafka_2.13-3.6.0 kafka
```

### 1.3. Cấu hình systemd service

**Zookeeper** (`/etc/systemd/system/zookeeper.service`):

```ini
[Unit]
Description=Apache Zookeeper
After=network.target

[Service]
Type=simple
User=kafka
ExecStart=/opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties
ExecStop=/opt/kafka/bin/zookeeper-server-stop.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

**Kafka** (`/etc/systemd/system/kafka.service`):

```ini
[Unit]
Description=Apache Kafka
After=zookeeper.service

[Service]
Type=simple
User=kafka
ExecStart=/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties
ExecStop=/opt/kafka/bin/kafka-server-stop.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable --now zookeeper kafka
```

---

## 2. Cấu hình Kafka

### 2.1. `server.properties` — Các tham số quan trọng

```properties
# --- Cơ bản ---
broker.id=1                                      # ID duy nhất trong cluster
listeners=PLAINTEXT://0.0.0.0:9092               # Lắng nghe tất cả interface
advertised.listeners=PLAINTEXT://192.168.41.43:9092  # IP mà client kết nối
log.dirs=/data/kafka/logs                        # Thư mục lưu dữ liệu

# --- Zookeeper ---
zookeeper.connect=192.168.41.43:2181,192.168.41.44:2181,192.168.41.45:2181

# --- Retention (thời gian giữ dữ liệu) ---
log.retention.hours=168                          # 7 ngày (mặc định)
log.retention.bytes=-1                           # Không giới hạn dung lượng

# --- Partition & Replication ---
num.partitions=3                                 # Mặc định 3 partition/topic
default.replication.factor=2                    # Replication mặc định

# --- Network ---
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600
```

### 2.2. Tuning JVM (`/opt/kafka/bin/kafka-server-start.sh`)

```bash
export KAFKA_HEAP_OPTS="-Xms4g -Xmx4g"
export KAFKA_GC_LOG_OPTS="-Xlog:gc*:file=/var/log/kafka/gc.log:time,tags:filecount=10,filesize=64M"
```

---

## 3. Các lệnh cơ bản

Tất cả lệnh đều nằm trong `/opt/kafka/bin/`. Thêm vào `PATH` hoặc gọi đường dẫn đầy đủ.

### 3.1. Quản lý Topic

```bash
# Liệt kê tất cả topics
bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Mô tả chi tiết một topic
bin/kafka-topics.sh --describe --topic QTSX_ReportQueue --bootstrap-server localhost:9092

# Tạo topic mới
bin/kafka-topics.sh --create --topic my-topic \
  --partitions 3 --replication-factor 2 \
  --bootstrap-server localhost:9092

# Tăng partition cho topic (chỉ được tăng, không giảm)
bin/kafka-topics.sh --alter --topic QTSX_ReportQueue_G2 \
  --partitions 5 \
  --bootstrap-server 192.168.41.43:9092,192.168.41.44:9092,192.168.41.45:9092

# Xoá topic
bin/kafka-topics.sh --delete --topic my-topic --bootstrap-server localhost:9092
```

### 3.2. Producer — Gửi message

```bash
# Gửi từ console (gõ từng dòng, Ctrl+C để thoát)
bin/kafka-console-producer.sh --topic my-topic --bootstrap-server localhost:9092
> hello world
> message 2

# Gửi từ file
bin/kafka-console-producer.sh --topic my-topic --bootstrap-server localhost:9092 < messages.txt
```

### 3.3. Consumer — Nhận message

```bash
# Consumer cơ bản (từ đầu)
bin/kafka-console-consumer.sh --topic my-topic \
  --from-beginning --bootstrap-server localhost:9092

# Consumer với group (quản lý offset)
bin/kafka-console-consumer.sh --topic my-topic \
  --group my-group --bootstrap-server localhost:9092
```

### 3.4. Consumer Group

```bash
# Liệt kê consumer groups
bin/kafka-consumer-groups.sh --list --bootstrap-server localhost:9092

# Mô tả group (Lag, Consumer, Partition)
bin/kafka-consumer-groups.sh --describe --group my-group \
  --bootstrap-server localhost:9092

# Reset offset về đầu (cần consumer group không hoạt động)
bin/kafka-consumer-groups.sh --topic my-topic --group my-group \
  --reset-offsets --to-earliest --execute \
  --bootstrap-server localhost:9092
```

Kết quả `--describe` trông như sau:

```text
GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
my-group        my-topic        0          1024            1050            26
my-group        my-topic        1          512             520             8
my-group        my-topic        2          256             260             4
```

> **LAG** = số message chưa được xử lý. Nếu LAG tăng liên tục → consumer đang chậm hoặc bị lỗi.

---

## 4. Xem log & giám sát

### 4.1. Log Kafka server

```bash
# Log chính
tail -f /opt/kafka/logs/server.log

# Log request (gỡ lỗi giao tiếp client)
tail -f /opt/kafka/logs/request.log

# Log controller (leader election, cluster changes)
tail -f /opt/kafka/logs/controller.log

# GC log
tail -f /var/log/kafka/gc.log
```

### 4.2. Log Zookeeper

```bash
tail -f /opt/kafka/logs/zookeeper.out
```

### 4.3. Kiểm tra trạng thái cluster

```bash
# Kiểm tra daemon
systemctl status kafka
systemctl status zookeeper

# Port listening
ss -tlnp | grep -E '9092|2181'

# Mô tả toàn bộ cluster
bin/kafka-broker-api-versions.sh --bootstrap-server localhost:9092

# Kiểm tra broker đang live
echo "dump" | nc localhost 2181
```

---

## 5. Lỗi thường gặp

### 5.1. Không kết nối được broker

```
[2026-07-06 10:00:00] WARN Connection to node 1 could not be established.
Broker may not be available.
```

**Nguyên nhân:** Firewall chặn port 9092 / 2181, hoặc `advertised.listeners` sai IP.

```bash
# Kiểm tra firewall
firewall-cmd --list-all
netsh advfirewall firewall show rule name=all | find "9092"

# Kiểm tra advertised.listeners
grep advertised.listeners /opt/kafka/config/server.properties
```

**Xử lý:** Mở port 9092 (Kafka) và 2181 (Zookeeper) trên firewall.

### 5.2. LAG tăng cao — Consumer chậm

```
GROUP           TOPIC           PARTITION  LAG
my-group        my-topic        0          15000
```

**Nguyên nhân:** Consumer xử lý không kịp throughput.

**Xử lý:**

- Tăng số consumer trong group (tối đa = số partition).
- Kiểm tra logic xử lý bên consumer (DB query chậm, API call timeout).
- Tăng partition nếu cần (xem mục 3.1).

### 5.3. Disk đầy

Kafka lưu message trong `log.dirs`. Nếu hết disk → broker crash.

```bash
df -h /data/kafka/logs
du -sh /data/kafka/logs/*

# Giảm retention hoặc xoá topic cũ
bin/kafka-configs.sh --alter --entity-type topics \
  --entity-name my-topic --add-config retention.ms=86400000 \
  --bootstrap-server localhost:9092
```

### 5.4. Leader không khả dụng

```
Topic: my-topic  Partition: 0  Leader: none  Replicas: 1,2  Isr: 1
```

**Nguyên nhân:** Broker chứa leader bị down, không đủ in-sync replicas để bầu leader mới.

**Xử lý:** Start broker bị down, hoặc set `unclean.leader.election.enable=true` (cẩn thận — mất dữ liệu).

---

## 6. Tham khảo nhanh

| Mục đích | Lệnh |
|----------|------|
| List topics | `kafka-topics.sh --list --bootstrap-server ...` |
| Mô tả topic | `kafka-topics.sh --describe --topic ... --bootstrap-server ...` |
| Tăng partition | `kafka-topics.sh --alter --topic ... --partitions N --bootstrap-server ...` |
| List consumer groups | `kafka-consumer-groups.sh --list --bootstrap-server ...` |
| Xem lag | `kafka-consumer-groups.sh --describe --group ... --bootstrap-server ...` |
| Reset offset | `kafka-consumer-groups.sh --reset-offsets ... --bootstrap-server ...` |
| Xem server log | `tail -f /opt/kafka/logs/server.log` |
| Kiểm tra trạng thái | `systemctl status kafka` |

---

*Tài liệu được tạo ngày 06-07-2026 — Thao tác Kafka trên Linux.*
