---
title: Bài toán Performance Test — AMIS Kiểm toán SaaS
description: 'Bài toán thực tế: xác định quy mô user/tenant, tính CCU, thiết kế kịch bản kiểm thử hiệu năng cho phần mềm kiểm toán SaaS với bzm - Concurrency Thread Group, cấu hình JMeter và thời gian chạy cụ thể'
tags: [jmeter, performance-test, amis, kiem-toan, ccu, tenant, concurrency-thread-group, bzm]
category: 'developer/jmetter'
updated: 2026-07-06
order: 4
---

# Bài toán Performance Test — AMIS Kiểm toán SaaS

> **Tóm tắt**: Bài toán thực tế xác định quy mô hệ thống SaaS kiểm toán tại Việt Nam, tính toán CCU dựa trên phân bổ tenant/user, thiết kế kịch bản kiểm thử với bzm - Concurrency Thread Group, cấu hình JMeter chi tiết và kế hoạch thời gian chạy test.

## Mục lục
- [1. Bài toán thực tế](#1-bài-toán-thực-tế)
- [2. Quy mô hệ thống](#2-quy-mô-hệ-thống)
- [3. Tính toán CCU](#3-tính-toán-ccu)
- [4. Các kịch bản kiểm thử](#4-các-kịch-bản-kiểm-thử)
- [5. bzm - Concurrency Thread Group](#5-bzm---concurrency-thread-group)
- [6. Cấu trúc Test Plan JMeter](#6-cấu-trúc-test-plan-jmeter)
- [7. Thời gian chạy test](#7-thời-gian-chạy-test)
- [8. Cấu hình JMeter & Distributed](#8-cấu-hình-jmeter--distributed)
- [9. Output & Metrics](#9-output--metrics)
- [10. Giải đáp: Test 10-15 phút có đánh giá được không?](#10-giải-đáp-test-10-15-phút-có-đánh-giá-được-không)

---

## 1. Bài toán thực tế

Dự án **AMIS Kiểm toán** — nền tảng SaaS phục vụ ngành kiểm toán tại Việt Nam.

### 1.1. Đối tượng khách hàng

| Nhóm khách hàng | Số lượng |
|----------------|---------|
| Doanh nghiệp kiểm toán (Việt Nam 2026) | ~220 |
| Trường học, bệnh viện, trung tâm (kiểm toán nội bộ) | ~580-780 |
| **Tổng tiềm năng** | **800-1.000** |

> Không bao gồm Big4 — phạm vi khách hàng từ nhỏ đến lớn.

### 1.2. Phân bổ khách hàng theo quy mô

```text
Loại KH      Tỷ lệ   Số KH    User/KH    Tổng user
──────────   ─────   ──────   ────────   ──────────
Rất nhỏ       45%     450      3-5        1.800
Nhỏ           35%     350      6-15       3.500
Trung bình    15%     150      16-40      3.750
Lớn            5%      50      41-120     3.500
                                         ───────
                              Tổng       12.500 user
```

---

## 2. Quy mô hệ thống

### 2.1. Các chỉ số cốt lõi

| Chỉ số | Giá trị |
|--------|---------|
| Tổng tenant | 1.000 |
| Tổng account | 12.000-15.000 |
| Tenant hoạt động mỗi ngày | 300-400 |
| Tenant đồng thời (peak) | 80-120 |
| CCU bình thường | 250-350 |
| CCU mùa cao điểm | 500-700 |
| Stress test | 1.000+ |

### 2.2. Đặc thù ngành kiểm toán

```
Mùa vụ rõ rệt:
  Tháng 3-4:   Quyết toán thuế (cao điểm)
  Tháng 10-12: Lập kế hoạch kiểm toán
  Cuối năm:    Hoàn thiện hồ sơ

→ CCU mùa cao điểm gấp 2-3 lần ngày thường
```

### 2.3. Từ tenant đến CCU

```
1.000 tenant
    │
    ▼
300-400 tenant có người đăng nhập trong ngày
    │
    ▼
 80-120 tenant đang online cùng thời điểm (peak)
    │
    ▼
250-350 user đang thao tác (bình thường)
500-700 user (cao điểm)

→ Database quan tâm: ~80-120 tenant đồng thời, không phải 1.000
```

---

## 3. Tính toán CCU

### 3.1. Từ account đến CCU

```text
12.500 account
    │ 10-20% active/ngày
    ▼
 2.000 DAU (Daily Active Users)
    │ 10-30% online cùng thời điểm
    ▼
 300-600 Concurrent Users (khoảng ước lượng)
```

### 3.2. Bộ số liệu cố định

| Chỉ số | Giá trị |
|--------|---------|
| Tổng tenant | 1.000 |
| Tổng account | 12.000 |
| Tenant hoạt động mỗi ngày | 300 |
| Tenant đồng thời (peak) | 80 |
| **CCU thực tế** | **400** |

Giả sử 9:30 sáng: 80 tenant, 400 người đang online và thao tác.

### 3.3. CCU ≠ Request concurrency

```
Một user kiểm toán viên trong 70 giây:
  0s     GET dashboard
  1-20s  đọc
  20s    GET audit
  21-40s đọc
  40s    POST save
  41-70s đọc

→ 3 request / 70 giây ≈ 0.04 req/s/user
→ Think Time trung bình: 30-60 giây giữa các thao tác
```

### 3.4. Tính throughput từ CCU

```text
Throughput (TPS) = CCU / (Think Time + Response Time)

Với:
  CCU = 400
  Think Time = 45s (trung bình)
  RT = 0.5s

TPS = 400 / (45 + 0.5) ≈ 8.8 request/giây

→ Hệ thống chỉ cần xử lý ~9 req/s ở mức 400 CCU
→ Điều này rất nhẹ so với các hệ thống realtime
```

---

## 4. Các kịch bản kiểm thử

### 4.1. Kịch bản theo mùa vụ

| Kịch bản | Mô tả | CCU | Duration |
|----------|-------|-----|----------|
| **Normal Load** | Ngày bình thường | 400 | 30 phút |
| **Peak Load** | Mùa cao điểm | 700 | 30 phút |
| **Stress** | Quá tải | 1.000-1.200 | 15 phút |
| **Spike** | Tăng đột biến đầu giờ | 0→700 trong 2s | 10 phút |
| **Endurance** | Chịu tải dài | 400 | 4-8 giờ |

### 4.2. Kịch bản chi tiết

#### Scénario A: Load Test — Ngày bình thường

| Tham số | Giá trị |
|---------|---------|
| Target Concurrency | 400 |
| Ramp-up | 5 phút (tăng đều 80 user/phút) |
| Hold | 20 phút |
| Ramp-down | 1 phút |

#### Scénario B: Load Test — Mùa cao điểm

| Tham số | Giá trị |
|---------|---------|
| Target Concurrency | 700 |
| Ramp-up | 5 phút |
| Hold | 20 phút |
| Ramp-down | 1 phút |

#### Scénario C: Stress Test

| Giai đoạn | Target | Thời gian |
|-----------|--------|-----------|
| Baseline | 400 | 5 phút |
| Tăng 1 | 600 | 3 phút |
| Tăng 2 | 800 | 3 phút |
| Tăng 3 | 1.000 | 3 phút |
| Peak | 1.200 | 5 phút |
| Giảm | 0 | 1 phút |

#### Scénario D: Spike Test

| Giai đoạn | Target | Thời gian |
|-----------|--------|-----------|
| Baseline | 50 | 2 phút |
| Spike | 700 (trong 2 giây) | 5 phút |
| Giảm | 0 | 30 giây |

---

## 5. bzm - Concurrency Thread Group

### 5.1. Giới thiệu

```
bzm - Concurrency Thread Group (Plugin: jp@gc)
  - Duy trì số concurrent users CHÍNH XÁC
  - Không phụ thuộc vào ramp-up như Thread Group thường
  - Tự động điều chỉnh thread để đạt target concurrency
  - Hỗ trợ: ramp-up → hold → ramp-down rõ ràng
```

> Plugin này nằm trong **JMeter Plugins Manager** → tab "Available Plugins" → `jpgc - Standard Set`.

### 5.2. Cấu hình cho từng kịch bản

**A — Normal Load (400 CCU):**

```text
Target Concurrency:  400
Ramp Up Time:       300 (5 phút)
Ramp-Up Steps Count: 20
Hold Target Rate:   1200 (20 phút)
Time Unit:          seconds
Thread Iterations Limit: forever
Log threads status: ✓
```

**B — Peak Load (700 CCU):**

```text
Target Concurrency:  700
Ramp Up Time:       300 (5 phút)
Ramp-Up Steps Count: 30
Hold Target Rate:   1200 (20 phút)
Time Unit:          seconds
```

**C — Stress (tăng dần 1.200):**

```text
Dùng 4 hàng (schedule) trong cùng 1 Concurrency Thread Group:

Hàng 1: Start=0, End=400,  Ramp=300s, Hold=300s
Hàng 2: Start=400, End=800,  Ramp=180s, Hold=180s
Hàng 3: Start=800, End=1200, Ramp=180s, Hold=300s
Hàng 4: Start=1200, End=0,   Ramp=60s,  Hold=0s
```

**D — Spike:**

```text
Hàng 1: Start=0,   End=50,   Ramp=120s, Hold=120s
Hàng 2: Start=50,  End=700,  Ramp=2s,   Hold=300s
Hàng 3: Start=700, End=0,    Ramp=30s,  Hold=0s
```

### 5.3. So sánh Thread Group thường vs bzm - Concurrency

| Tiêu chí | Thread Group (cổ điển) | bzm - Concurrency |
|----------|----------------------|-------------------|
| Số thread cố định? | Có (không đổi) | Tự động điều chỉnh |
| Giữ đúng concurrency? | Không (thread nhàn rỗi vẫn tính) | Có (chỉ tính thread đang chạy) |
| Ramp-down? | Không có | Có |
| Hỗ trợ schedule nhiều giai đoạn? | Không | Có (multi-row) |
| Dùng cho stress/spike? | Khó | Dễ |
| **Khuyến nghị** | Chỉ dùng cho smoke test | **Mặc định cho mọi kịch bản** |

---

## 6. Cấu trúc Test Plan JMeter

### 6.1. Test Plan tổng thể

```
Test Plan
  ├─ User Defined Variables
  │   ├─ BASE_URL     = https://kiemtoan.ami.vn
  │   ├─ THINK_TIME   = ${__P(thinktime,45)}
  │   └─ DEFAULT_USER = ${__P(user,test_user_01)}
  │
  ├─ HTTP Request Defaults
  │   ├─ Protocol: https
  │   ├─ Server: kiemtoan.ami.vn
  │   └─ Content-Type: application/json
  │
  ├─ CSV Data Set Config (x N thread groups)
  │   └─ users_400.csv (tenant_id, username, password, token)
  │
  └─ bzm - Concurrency Thread Group
      │
      ├─ setUp Thread Group (Login & lấy token)
      │
      ├─ Transaction Controller: "Xem danh sách chứng từ"
      │   ├─ HTTP GET /api/v1/vouchers
      │   ├─ HTTP GET /api/v1/vouchers/summary
      │   └─ JSON Assertion
      │
      ├─ Uniform Random Timer (5000-15000ms) ← Think Time sau feature
      │
      ├─ Transaction Controller: "Xem chi tiết chứng từ"
      │   ├─ HTTP GET /api/v1/vouchers/{id}
      │   ├─ HTTP GET /api/v1/vouchers/{id}/attachments
      │   ├─ HTTP GET /api/v1/vouchers/{id}/history
      │   └─ HTTP GET /api/v1/vouchers/{id}/permissions
      │
      ├─ Uniform Random Timer (10000-30000ms)
      │
      ├─ Transaction Controller: "Tạo/Lưu chứng từ"
      │   ├─ HTTP POST /api/v1/vouchers
      │   ├─ HTTP PUT /api/v1/vouchers/{id}
      │   └─ JSON Assertion
      │
      ├─ Uniform Random Timer (5000-15000ms)
      │
      ├─ Transaction Controller: "Tìm kiếm & Lọc"
      │   ├─ HTTP GET /api/v1/vouchers/search?q=...
      │   ├─ HTTP GET /api/v1/vouchers/filter?status=...
      │   └─ Response Assertion
      │
      └─ Listeners
          ├─ jp@gc - Response Times Over Time
          ├─ jp@gc - Active Threads Over Time
          ├─ jp@gc - Transactions per Second
          ├─ Summary Report (ghi file .jtl)
          └─ View Results Tree (TẮT khi chạy thật — chỉ bật debug)
```

### 6.2. Giải thích cấu trúc

```text
[Transaction Controller]    → Gom nhiều API thành 1 feature
    └─ API 1               → Không think time giữa các API
    └─ API 2               → (vì frontend gọi gần như đồng thời)
    └─ API 3

[Timer]                     → Think Time SAU feature
                            → Uniform Random Timer: 5-15s
                            → Gaussian Random Timer: phân phối chuẩn

[CSV Data Config]           → Mỗi virtual user dùng 1 user riêng
                            → Sharing mode: Current Thread Group
```

### 6.3. Transaction Controller — Cấu hình

```text
Generate Parent Sample: ✓ (để đo tổng thời gian feature)
Include Duration of Timer and Pre-Post Processors in generated sample: ✗
```

### 6.4. Think Time — Khuyến nghị cho kiểm toán

```text
Đặc thù kiểm toán viên:
  - Đọc chứng từ, giấy tờ: 15-30 giây
  - Xem Excel/PDF: 20-60 giây
  - Nhập liệu: 10-30 giây
  - Trao đổi, suy nghĩ: 10-20 giây

→ Think Time hiệu quả: 10-45 giây (Uniform Random)
→ Hoặc dùng Gaussian Random với deviation = 10s
```

---

## 7. Thời gian chạy test

### 7.1. Kế hoạch thời gian

| Kịch bản | Ramp-up | Hold | Ramp-down | Tổng |
|----------|---------|------|-----------|------|
| Smoke | 10s | 2 phút | 10s | **~3 phút** |
| Normal Load | 5 phút | 20 phút | 1 phút | **26 phút** |
| Peak Load | 5 phút | 20 phút | 1 phút | **26 phút** |
| Stress | 5 phút | 11 phút | 1 phút | **17 phút** |
| Endurance | 10 phút | 4-8 giờ | 2 phút | **~4-8 giờ** |
| Spike | 2 phút | 5 phút | 30s | **~7,5 phút** |

### 7.2. Tổng thời gian cho 1 đợt test đầy đủ

```text
Đợt test đầy đủ (Full Regression):
  ├─ Smoke:                   3 phút
  ├─ Normal Load:            26 phút
  ├─ Peak Load:              26 phút
  ├─ Stress:                 17 phút
  ├─ Spike:                   8 phút
  └─ Endurance (riêng):    4-8 giờ (chạy qua đêm)

Tổng (không endurance):   ~1.5 giờ
Tổng (cả endurance):      ~6-10 giờ
```

### 7.3. Lịch chạy gợi ý

```text
Buổi sáng (8:00-12:00):
  8:00 - 8:05   Smoke
  8:05 - 8:35   Normal Load (400 CCU)
  8:35 - 9:05   Peak Load (700 CCU)
  9:05 - 9:25   Stress
  9:25 - 9:35   Spike
  9:35 - 12:00  Phân tích kết quả, tuning

Qua đêm (chạy riêng):
  22:00 - 6:00  Endurance (400 CCU, 8 giờ)
```

---

## 8. Cấu hình JMeter & Distributed

### 8.1. Yêu cầu phần cứng

| Cấu hình | JMeter Master | JMeter Slave (x3) |
|----------|--------------|-------------------|
| RAM | 4GB | 2GB |
| CPU | 4 cores | 2 cores |
| Heap (JVM) | -Xmx3g | -Xmx1g |
| Network | 1Gbps | 1Gbps |

### 8.2. Tối ưu JMeter

```batch
REM Tăng heap cho JMeter
set HEAP="-Xms2g -Xmx3g -XX:MaxMetaspaceSize=512m"

REM Chạy non-GUI
jmeter -n -t "AMIS_KiemToan.jmx" ^
       -l "results/result_%date:~10,4%%date:~4,2%%date:~7,2%.jtl" ^
       -e -o "report/%date:~10,4%%date:~4,2%%date:~7,2%" ^
       -Jthreads=700 ^
       -Jthinktime=45 ^
       -f
```

### 8.3. Cấu hình user.properties

```properties
# Tại apache-jmeter-5.x/bin/user.properties

# Mode CLI
jmeter.save.saveservice.output_format=csv
jmeter.save.saveservice.response_data=false
jmeter.save.saveservice.samplerData=false
jmeter.save.saveservice.requestHeaders=false
jmeter.save.saveservice.url=false
jmeter.save.saveservice.assertionResults=false
jmeter.save.saveservice.bytes=true
jmeter.save.saveservice.thread_counts=true
jmeter.save.saveservice.thread_name=false
jmeter.save.saveservice.time=true
jmeter.save.saveservice.latency=true
jmeter.save.saveservice.connect_time=true
jmeter.save.saveservice.successful=true

# Strip batch
jmeter.save.saveservice.print_field_names=true
csvread.delimiter=,

# Summariser
summariser.interval=30
summariser.log=true
```

### 8.4. JMeter Distributed (nếu cần > 500 thread)

```text
Master (Windows):
  jmeter -n -t AMIS_KiemToan.jmx ^
         -R 192.168.1.101:1099,192.168.1.102:1099 ^
         -l results/result.jtl -e -o report -f

Mỗi Slave chạy:
  jmeter-server.bat (hoặc jmeter-server trên Linux)
```

### 8.5. Tỉ lệ phân bổ Thread/CPU

| Số threads | Cấu hình khuyến nghị |
|-----------|---------------------|
| 1-400 | 1 máy, 2-4GB RAM |
| 400-800 | 1 máy, 4-8GB RAM, HEAP=4g |
| 800-1.500 | 2 slaves × 400-800 thread/slave |
| 1.500-3.000 | 4 slaves × 400-800 thread/slave |

---

## 9. Output & Metrics

### 9.1. Báo cáo kết quả

#### Mẫu báo cáo Summary

```text
=====================================================================
KẾT QUẢ PERFORMANCE TEST — AMIS Kiểm toán
Ngày: 2026-07-06 | Kịch bản: Normal Load (400 CCU)
=====================================================================

Tổng quan:
  - Số request:          12,450
  - TPS trung bình:      8.3 req/s
  - Peak TPS:            12.1 req/s
  - Error rate:          0.02%
  - Thời gian test:      26 phút

Response Time (ms):
  - Min:    45
  - Avg:   320
  - P50:   180
  - P90:   650
  - P95:   890
  - P99:   2,100
  - Max:   5,400

Response Time theo Feature:
  Feature                    Avg    P95     P99    Error%
  ────────────────────────── ─────  ──────  ────── ──────
  Xem danh sách chứng từ      280    650   1,200   0.00
  Xem chi tiết chứng từ       450  1,200   2,500   0.01
  Tạo/Lưu chứng từ            650  1,800   3,200   0.05
  Tìm kiếm & Lọc              350    780   1,500   0.00

Server Metrics (peak):
  - CPU:         72%
  - RAM:         4.8/8GB (60%)
  - DB Connections: 45/100
  - DB Query time: 12ms avg
  - Disk I/O:    15 MB/s
```

### 9.2. Đồ thị cần lưu

```text
1. Response Times Over Time      → RT có ổn định không?
2. Active Threads Over Time      → Concurrency có đúng target không?
3. Transactions per Second       → Throughput theo thời gian
4. Response Times Percentiles    → Phân phối RT
5. Latency vs Response Time      → Mạng vs xử lý
6. Bytes Throughput Over Time    → Lưu lượng mạng
```

### 9.3. SLA mục tiêu cho AMIS Kiểm toán

| Metric | Mục tiêu | Cảnh báo | Ngưỡng tối đa |
|--------|---------|----------|--------------|
| P95 RT (API đơn) | < 1s | 1-2s | > 2s |
| P95 RT (Feature) | < 3s | 3-5s | > 5s |
| Error rate | < 0.1% | 0.1-1% | > 1% |
| TPS (400 CCU) | ≥ 8 req/s | 5-8 req/s | < 5 req/s |
| TPS (700 CCU) | ≥ 14 req/s | 10-14 req/s | < 10 req/s |
| CPU server | < 70% | 70-85% | > 85% |
| DB query time | < 50ms | 50-200ms | > 200ms |

---

## 10. Giải đáp: Test 10-15 phút có đánh giá được không?

### 10.1. Câu trả lời ngắn

```
CÓ — nếu bạn chọn đúng loại test.
KHÔNG — nếu bạn cần đánh giá memory leak hay độ ổn định dài hạn.
```

### 10.2. Khi nào 10-15 phút là đủ?

| Mục đích | Thời gian tối thiểu | Ghi chú |
|----------|-------------------|---------|
| Smoke test | 2-3 phút | Xác nhận hệ thống còn sống |
| Tìm bottleneck API | 5-10 phút | Với tải cố định, sau warm-up |
| Stress test (tìm breakpoint) | 10-15 phút | Tăng dần tải, tìm điểm gãy |
| Spike test | 5-8 phút | Tăng đột biến, hold ngắn |
| So sánh 2 phiên bản | 5-10 phút/kịch bản | A/B test |
| **Load test** | **20-30 phút** | **Cần tối thiểu 15 phút sau warm-up** |
| Endurance | 4-8 giờ | Phát hiện memory leak |

### 10.3. Tại sao load test cần > 15 phút?

```text
Lý do:
  1. Warm-up: 2-5 phút đầu hệ thống chưa ổn định (cache, connection pool)
  2. Garbage Collection: JVM cần vài chu kỳ GC để ổn định
  3. DB connection pool: Cần thời gian để đạt steady state
  4. Biến thiên RT: Cần đủ mẫu để có P95/P99 đáng tin cậy

Ví dụ:
  Test 5 phút với 400 CCU → 400 × 300s / 45s ≈ 2.666 request mẫu
  Test 20 phút            → 400 × 1200s / 45s ≈ 10.666 request mẫu

→ Càng nhiều mẫu, P99 càng đáng tin cậy
```

### 10.4. Giải pháp cho AMIS Kiểm toán (10-15 phút)

```text
Nếu bị giới hạn thời gian, làm như sau:

▸ Chạy Smoke (3 phút) → xác nhận hệ thống sống
▸ Chạy Stress (10 phút) → tăng từ 200 → 1.200 → tìm breakpoint

  Với bzm - Concurrency Thread Group:
    Hàng 1: 0→200,   ramp 60s,  hold 120s
    Hàng 2: 200→600,  ramp 120s, hold 120s
    Hàng 3: 600→1200, ramp 120s, hold 120s (hoặc đến khi sập)

▸ Chạy 1 Load test ngắn (10 phút) với 400 CCU
  → Chấp nhận P99 có thể chưa ổn định
  → Tập trung vào throughput và error rate

Total: ~23 phút — chấp nhận được.
```

### 10.5. Lưu đồ quyết định

```text
Chỉ có 10-15 phút?
        │
        ▼
Cần đánh giá độ ổn định dài hạn?
        │                   │
       YES                  NO
        │                   │
        ▼                   ▼
  Chạy endurance         Cần tìm bottleneck?
  riêng (qua đêm)             │
                        YES     NO
                         │       │
                         ▼       ▼
                    Stress Test  Smoke + Load
                    (~15 phút)   ngắn (~10 phút)
```

---

## Phụ lục: Kịch bản test cụ thể cho AMIS Kiểm toán

### P.1. Feature cần test

| STT | Feature | API | Tần suất (ước lượng) |
|-----|---------|-----|---------------------|
| 1 | Đăng nhập | POST /api/auth/login | 1 lần/phiên |
| 2 | Dashboard | GET /api/dashboard | 30% |
| 3 | Danh sách chứng từ | GET /api/vouchers | 40% |
| 4 | Chi tiết chứng từ | GET /api/vouchers/{id} + attachments + history | 35% |
| 5 | Tạo chứng từ | POST /api/vouchers | 10% |
| 6 | Sửa chứng từ | PUT /api/vouchers/{id} | 15% |
| 7 | Tìm kiếm | GET /api/vouchers/search | 20% |
| 8 | Báo cáo | GET /api/reports | 10% |
| 9 | Xuất Excel/PDF | POST /api/export | 5% |
| 10 | Đăng xuất | POST /api/auth/logout | 1 lần/phiên |

### P.2. Tỷ lệ phân bổ user theo tenant

Dùng `weighted switch` hoặc nhiều Thread Groups riêng:

```text
bzm - Concurrency Thread Group (400 CCU)
  ├─ 60% → User Journey: "Kiểm toán viên thông thường"
  │    Xem danh sách → Chi tiết → Tìm kiếm → Sửa
  │
  ├─ 25% → User Journey: "Kiểm toán viên nhập liệu"
  │    Xem danh sách → Tạo mới → Lưu → Xem lại
  │
  └─ 15% → User Journey: "Quản lý / Admin"
       Dashboard → Báo cáo → Xuất báo cáo → Duyệt
```

### P.3. Data test — Vì sao 1 user, 1 database (SILO) là KHÔNG ĐỦ?

#### Câu hỏi

> "Nếu tôi chỉ test bằng duy nhất 1 user, 1 database (SILO multi-tenant),
> chỉ gọi API thật nhiều request — dù không đa dạng dữ liệu — thì có vấn đề gì không?"

#### Câu trả lời ngắn

```
CÓ VẤN ĐỀ — và rất nghiêm trọng.

Test với 1 tenant + 1 user cho kết quả ẢO, KHÔNG phản ánh
thực tế khi có 80-120 tenant + 400 user đồng thời.
```

#### Phân tích chi tiết

**1. Database Connection Pool — Nút thắt cổ chai nguy hiểm nhất**

```text
SILO (mỗi tenant 1 database riêng):

  1 tenant → 1 database → 1 connection pool (ví dụ: 10 connections)
  80 tenant → 80 database → 80 connection pools × 10 = 800 connections

Nếu chỉ test 1 tenant:
  - Connection pool chỉ dùng 1 pool (10 conn) → ổn, không vấn đề
  - Nhưng thực tế 80 tenant → 800 connections → DB ngạt thở

Kết quả:
  Test 1 tenant: P95 = 200ms ✓ → Kết luận: hệ thống khoẻ
  Thực tế 80 tenant: P95 = 5s, timeout liên tục ✗ → Sập
```

**2. Query Plan — Cùng câu query, khác performance**

```
Database SILO: Mỗi tenant có data riêng, phân bố dữ liệu khác nhau.

Ví dụ:
  Tenant A (nhỏ):    50 chứng từ
  Tenant B (vừa):  1.200 chứng từ
  Tenant C (lớn):  15.000 chứng từ

  Query: SELECT * FROM vouchers WHERE status = 'pending'
          AND tenant_id = ?

  - Tenant A: full scan 50 dòng → 5ms (dùng index hay không cũng nhanh)
  - Tenant C: full scan 15.000 dòng → 800ms (cần index, có thể slow query)

Test chỉ với Tenant A: query nào cũng nhanh → Ảo tưởng
Test với Tenant C: phát hiện thiếu index, query chậm
```

**3. Lock Contention — Tranh chấp tài nguyên**

```text
1 user thao tác:             Không có tranh chấp lock nào
400 user cùng thao tác:
  - Row lock trên cùng bảng
  - Table lock nếu có DDL
  - Sequence/ID generation lock
  - Transaction isolation conflict

Ví dụ: Tạo chứng từ mới
  1 user: INSERT → 50ms ✓
  400 user cùng tạo:
    INSERT vào cùng bảng → hàng đợi lock
    Sequence lấy ID → contention
    → Thời gian tăng lên 500ms-2s
```

**4. Partition Pruning & Data Skew (SILO)**

```text
SILO model → Mỗi tenant có data riêng biệt
Nhưng data có thể bị lệch (skew):
  - Tenant "Tổng công ty X" có 50.000 chứng từ
  - Tenant "Cửa hàng Y" có 10 chứng từ

Nếu chỉ test 1 tenant với ít data:
  - Partition pruning không được kích hoạt (hoặc kích hoạt sai)
  - Index scan vs full table scan không được đánh giá đúng
  - Query plan tối ưu cho tenant nhỏ nhưng chậm cho tenant lớn
```

**5. Thread Pool & Resource Contention — Phía Application**

```text
Application Server:
  1 user → 1 thread trong thread pool → không contention
  400 user → 400 thread → thread pool có thể exhausted
    - Task queue dài ra
    - Context switching tăng
    - GC áp lực (nhiều object được tạo ra)

Chỉ test 1 user: không bao giờ phát hiện được vấn đề này.
```

**6. Token/Session Management**

```text
1 user:
  - 1 token trong memory cache → luôn hit
  - Cache tỉ lệ hit: 100%

400 user với 80 tenant:
  - Token phân tán, có thể cache miss
  - Session quản lý phức tạp hơn
  - Redis/Memcached có thể bị saturated
```

#### Bảng tổng hợp — Hậu quả của test 1 tenant

| Khía cạnh | Test 1 tenant | Thực tế 80 tenant | Kết luận sai? |
|-----------|--------------|-------------------|:---:|
| Connection pool | 10 conn ổn định | 800 conn quá tải | **SAI** |
| Query plan | Tối ưu cho ít data | Có thể full scan với tenant lớn | **SAI** |
| Lock contention | Không có | Row/table lock | **SAI** |
| Thread pool | 1 thread | 400 thread, queue dài | **SAI** |
| Cache hit | 100% (1 token) | Có thể miss | **SAI** |
| GC áp lực | Không đáng kể | Major GC thường xuyên | **SAI** |
| Network I/O | 1 conn | 400 conn | **SAI** |
| Disk I/O | 1 tenant data | 80 tenant data rải rác | **SAI** |

#### Vậy tôi cần chuẩn bị data thế nào cho đúng?

**Nguyên tắc: Data test phải phản ánh đúng phân bố thực tế của PRODUCTION.**

```text
┌─────────────────────────────────────────────────────────────┐
│ Data test cho SILO Multi-tenant                              │
├─────────────────────────────────────────────────────────────┤
│ 1. Nhiều tenant: tối thiểu 20-30 tenant (tỷ lệ với thực tế) │
│ 2. Mỗi tenant có volume data KHÁC NHAU (nhỏ, vừa, lớn)      │
│ 3. Dữ liệu trong mỗi tenant phải "thực" (không giống hệt)    │
│ 4. Tài khoản user riêng cho từng tenant                      │
│ 5. Think time khác nhau giữa các tenant                      │
└─────────────────────────────────────────────────────────────┘
```

**Cấu hình data tối thiểu cho AMIS Kiểm toán:**

```text
Loại tenant    Số lượng   Data volume    User/tenant
───────────    ─────────  ─────────────  ───────────
Rất nhỏ        10         50-100 bản ghi   1-2
Nhỏ            10         200-500 bản ghi  3-5
Trung bình     5          1.000-3.000      5-10
Lớn            3          5.000-15.000     10-20
                            ───────────
                28 tenant  (~3.5% tổng)

→ 28 tenant với đủ loại volume, phát hiện được:
  - Query plan khác nhau giữa tenant nhỏ và lớn
  - Connection pool stress
  - Lock contention khi nhiều tenant cùng thao tác
```

**Data files cần chuẩn bị:**

| File | Nội dung | Số dòng | Ghi chú |
|------|---------|---------|---------|
| `tenants.csv` | tenant_id, loại, db_name (SILO) | 30+ | Phân bổ theo tỷ lệ thực tế |
| `users.csv` | tenant_id, username, password, token | 100+ | Ít nhất 3-5 user/tenant |
| `voucher_ids.csv` | tenant_id, voucher_id | 5.000+ | Volume khác nhau theo tenant |
| `search_terms.csv` | tenant_id, keyword | 200+ | Từ khóa đặc thù từng tenant |
| `customer_data.csv` | tenant_id, customer data | 3.000+ | Data riêng cho từng tenant |

#### Khi nào test 1 tenant là chấp nhận được?

```text
Chấp nhận:
  - Smoke test (kiểm tra API còn sống)
  - Debug kịch bản JMeter
  - Warm-up trước khi chạy test thật
  - Benchmark API đơn thuần (không liên quan multi-tenant)

Không chấp nhận:
  - Load test để đánh giá năng lực hệ thống
  - Stress test
  - Endurance test
  - Capacity planning
  - Báo cáo performance chính thức
```

#### Kết luận

```
Test performance với 1 tenant + 1 user trong mô hình SILO
giống như "tập bơi trong chậu nước rồi kết luận mình
bơi được ở biển".

Nó đúng là có bơi — nhưng không phản ánh được sóng to,
gió lớn, dòng chảy, và cá mập.

Để đánh giá đúng, cần tối thiểu 20-30 tenant với volume
data thực tế (có nhỏ, có lớn), user thật, và concurrent
thực tế.
```

---

