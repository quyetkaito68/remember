---
title: Performance Test — Kiến thức nền tảng & Các loại kiểm thử
description: 'Tổng hợp khái niệm CCU, Tenant, User, Request; công thức tính toán; mối liên hệ CCU-Thread trong JMeter; các kiểu kiểm thử performance và những điểm quan trọng thường bị bỏ sót'
tags: [jmeter, performance-test, ccu, tenant, load-test, stress-test]
category: 'developer/jmetter'
updated: 2026-07-06
order: 3
---

# Yêu Cầu Performance — Kiến thức nền tảng & Các loại kiểm thử

> **Tóm tắt**: Tài liệu tổng hợp các khái niệm cốt lõi (CCU, Tenant, User, Request), công thức tính toán, mối liên hệ giữa CCU và Thread trong JMeter, cũng như các kiểu kiểm thử performance và những điểm quan trọng thường bị bỏ sót.

## Mục lục

- [1. Khái niệm cốt lõi](#1-khái-niệm-cốt-lõi)
- [2. Công thức & Mối liên hệ](#2-công-thức--mối-liên-hệ)
- [3. CCU và Thread trong JMeter](#3-ccu-và-thread-trong-jmeter)
- [4. Các kiểu kiểm thử Performance](#4-các-kiểu-kiểm-thử-performance)
- [5. Những điểm quan trọng có thể bạn chưa biết](#5-những-điểm-quan-trọng-có-thể-bạn-chưa-biết)

---

## 1. Khái niệm cốt lõi

### 1.1. CCU (Concurrent Users / Concurrent Connections / Concurrent Calls)

```
CCU = Số lượng người dùng (hoặc kết nối) đồng thời
      tương tác với hệ thống tại cùng một thời điểm
```

- **CCU thực tế (Active CCU)**: Người dùng đang thực sự gửi request và chờ response.
- **CCU ước lượng (Estimated CCU)**: Dựa trên số lượng user đăng nhập, tỷ lệ concurrent (thường 10-20% tổng user active).
- **CCU tối đa (Peak CCU)**: Đỉnh cao nhất trong ngày/tháng, thường gấp 2-5x so với CCU trung bình.

### 1.2. Tenant

```
Tenant = Đơn vị thuê bao / tổ chức / khách hàng
         sử dụng hệ thống dạng SaaS (Multi-tenant)
```

- **Single-Tenant**: Mỗi khách hàng một instance riêng.
- **Multi-Tenant**: Nhiều khách hàng chung một instance, dữ liệu phân tách bằng `tenant_id`.
- **Common Tenant / System Tenant**: Tenant đặc biệt chứa cấu hình chung, không thuộc khách hàng nào.

### 1.3. User

```
User = Người dùng cụ thể trong hệ thống,
       thuộc về một Tenant nhất định
```

Phân loại theo mục đích test:
| Loại User | Mô tả |
|-----------|-------|
| **Anonymous User** | User chưa đăng nhập, chỉ truy cập public pages (login, landing page) |
| **Authenticated User** | User đã đăng nhập, có session/token |
| **Admin User** | User có quyền quản trị, thao tác nặng (CRUD users, config) |
| **End-User** | User thông thường, thao tác nghiệp vụ chính |
| **Service Account** | User máy (M2M), dùng API key, không có UI |

### 1.4. Request

```
Request = Một lời gọi HTTP (hoặc protocol khác) từ client đến server
```

- **Request đơn (Single Request)**: GET /api/users, POST /api/login...
- **Request chuỗi (Request Chain / Transaction)**: Nhiều request nối tiếp nhau theo một business flow.
- **Request đồng thời (Concurrent Requests)**: Nhiều request cùng lúc (có thể từ cùng một user).

---

## 2. Công thức & Mối liên hệ

### 2.1. Công thức cơ bản

```
Throughput (TPS) = CCU / Response Time (giây)

Ví dụ:
  CCU = 100, RT trung bình = 0.5s
  TPS = 100 / 0.5 = 200 request/giây
```

```
Response Time (RT) = Thời gian xử lý + Thời gian chờ (queue, network, I/O)

Các loại RT:
  - Avg RT: Trung bình cộng
  - Median RT (P50): 50% request nhanh hơn giá trị này
  - P95 / P99: 95%/99% request nhanh hơn (quan trọng nhất)
  - Max RT: Giá trị lớn nhất (thường bị nhiễu)
```

```
Số Thread JMeter cần = CCU × Hệ số an toàn (Safety Factor)

  Hệ số an toàn thường: 1.2 ~ 1.5
  (Dự phòng cho ramp-up, think time không đồng đều)

Ví dụ:
  CCU mục tiêu = 1000
  Hệ số = 1.3
  Thread = 1000 × 1.3 = 1300 threads
```

### 2.2. Mối liên hệ giữa các khái niệm

```
┌─────────────────────────────────────────────────────────────┐
│                         Hệ thống SaaS                        │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│  │ Tenant A │    │ Tenant B │    │ Tenant C │  ...          │
│  │ (100 usr)│    │ (50 usr) │    │ (200 usr)│               │
│  └─────┬────┘    └─────┬────┘    └─────┬────┘               │
│        │               │               │                     │
│        ▼               ▼               ▼                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Shared Service / API Layer              │    │
│  │  Mỗi user → Nhiều request (1 phiên = 5-20 request)  │    │
│  └─────────────────────────────────────────────────────┘    │
│        │               │               │                     │
│        ▼               ▼               ▼                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Database / Cache / Queue                │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

**Công thức tổng số request trên hệ thống (ước lượng):**

```
Tổng request/s = (Tổng CCU) × (Số request trung bình / user / giây)

hoặc

Tổng request/s = (Tổng CCU) / (Average Think Time + Average RT)
```

**Think Time (Thời gian suy nghĩ giữa các thao tác):**

```
- User thực tế: 3-10 giây giữa các thao tác
- JMeter có thể dùng Constant Timer / Uniform Random Timer
  để mô phỏng think time thực tế
```

### 2.3. Công thức phân bổ Tenant trong test

```
Threads cho Tenant X = (Số user của Tenant X / Tổng user) × Tổng Threads

Ví dụ:
  Tenant A có 500 user, Tenant B có 300 user, tổng 800 user
  Tổng Threads = 1000
  Tenant A = (500/800) × 1000 = 625 threads
  Tenant B = (300/800) × 1000 = 375 threads
```

### 2.4. Công thức Little's Law (Quan trọng)

```
L = λ × W

Trong đó:
  L = Số request đồng thời trong hệ thống (Concurrent Requests)
  λ = Throughput (request/giây)
  W = Response Time trung bình (giây)

Áp dụng:
  Nếu hệ thống xử lý 500 req/s và RT = 2s
  → Số request đang "ở trong" hệ thống = 500 × 2 = 1000 request
```

---

## 3. CCU và Thread trong JMeter

### 3.1. Quan hệ

```
CCU (mục tiêu) ───> Thread (JMeter)
                        │
                        ├── Mỗi thread = 1 user ảo (Virtual User)
                        ├── Mỗi thread chạy độc lập, loop theo kịch bản
                        └── Thread Pool = Tổng số CCU tối đa có thể mô phỏng
```

### 3.2. Thread Group: Các dạng

| Kiểu | Mô tả | Khi nào dùng |
|------|-------|--------------|
| **Thread Group** | Số thread cố định, chạy hết loop | Load test đơn giản |
| **Ultimate Thread Group** | Fine-tune ramp-up, hold, ramp-down | Endurance, Stress, Spike |
| **Concurrency Thread Group(*)** | Duy trì concurrency mục tiêu, tự động điều chỉnh | Khi cần CCU chính xác |
| **Arrivals Thread Group** | Duy trì throughput mục tiêu (arrivals/sec) | Khi cần TPS chính xác |

### 3.3. Cấu hình Thread Group cơ bản

```text
Number of Threads (users): 100         // = CCU mục tiêu
Ramp-Up Period (seconds):  60          // 1 thread/s, tăng dần
Loop Count:                10          // Mỗi user chạy 10 lần kịch bản
```

**Ramp-Up tối ưu:**

```
Ramp-Up = Số Thread × (Thời gian 1 kịch bản / Số lần lặp)

Ví dụ:
  100 threads, 1 kịch bản dài 30 giây, lặp 5 lần
  Ramp-Up = 100 × (30 / 5) = 600 giây (10 phút)
```

### 3.4. Lưu ý khi map CCU vào Thread

1. **Mỗi thread JMeter = 1 Virtual User** đang chạy kịch bản, KHÔNG phải 1 concurrent request.
2. **Thread không phải CCU tuyến tính**: Nếu 1 user có think time 5s, thì thread đó chỉ gửi request vài lần/phút.
3. **Số thread thực tế cần lớn hơn CCU** do think time và ramp-up không đồng đều.
4. **JMeter Distributed Testing** khi số thread > 1000 trên 1 máy (CPU/memory giới hạn).

### 3.5. Công thức tính Thread từ TPS mục tiêu (ngược)

```
Threads cần = TPS × (RT trung bình + Think Time trung bình)

Ví dụ:
  Mục tiêu TPS = 500
  RT trung bình = 0.5s
  Think Time = 3s
  Threads = 500 × (0.5 + 3) = 1750 threads
```

### 3.6. Giới hạn phần cứng của JMeter

| Tài nguyên | 1 máy thường | 1 máy cấu hình cao |
|------------|-------------|-------------------|
| Max threads ổn định | 300-500 threads | 1000-2000 threads |
| RAM cần thiết | 512MB - 1GB | 2GB - 4GB |
| Network (outbound) | ~100 Mbps | ~1 Gbps |
| **Khuyến nghị** | Dùng distributed (master + N slaves) nếu > 500 threads |

---

## 4. Các kiểu kiểm thử Performance(quan tâm 2 loại load test, stress test)

### 4.1. Load Testing (Kiểm thử tải)

```
Mục tiêu: Xác định hệ thống hoạt động ổn định dưới tải dự kiến
CCU = Tải dự kiến (ví dụ: 70-80% peak)
Duration: 30-60 phút
```

```text
Threads: 500            // CCU mục tiêu
Ramp-Up: 300s (5 phút)  // Tăng từ từ
Duration: 3600s (1 giờ) // Duy trì ổn định
```

### 4.2. Stress Testing (Kiểm thử quá tải)

```
Mục tiêu: Tìm điểm gãy (Breakpoint) của hệ thống
CCU = 150% - 300% tải dự kiến, tăng dần đến khi sập
```

```
Cách thực hiện:
  1. Bắt đầu từ 50% CCU mục tiêu
  2. Tăng 10-20% mỗi 5 phút
  3. Xác định điểm: RT tăng đột biến, Error rate > 5%, Throughput giảm
  4. Điểm gãy = Điểm cuối cùng trước khi sập
```

### 4.3. Feature Testing (Kiểm thử theo tính năng)

```
Mục tiêu: Đánh giá performance của một tính năng cụ thể,
          bao gồm tất cả API trong tính năng đó
```

**Ví dụ: Tính năng "Báo cáo"**

```text
Feature: Reporting Module
  APIs:
    - GET /reports/summary
    - GET /reports/detail
    - POST /reports/export (tạo file)
    - GET /reports/export/status
    - GET /reports/export/download

Kịch bản test: User vào báo cáo → xem summary → xem detail → export → download
Kết quả: Tổng thời gian hoàn thành luồng báo cáo
```


---

## 5. Những điểm quan trọng có thể bạn chưa biết

### 5.1. Pacing vs Think Time

```
Pacing = Khoảng thời gian cố định giữa các lần lặp (iteration)
Think Time = Khoảng thời gian giữa các request trong cùng iteration

Khác biệt:
  - Pacing kiểm soát throughput đầu ra (đều đặn)
  - Think Time mô phỏng hành vi người dùng thực (ngẫu nhiên)
```

### 5.2. Cache effect — Tác động của bộ nhớ đệm lên kết quả test

#### Bản chất cache effect

```
Cache effect = Hiện tượng lần chạy đầu (cold run) chậm hơn
              các lần chạy sau (warm run) vì dữ liệu đã được
              lưu vào bộ nhớ đệm ở các cấp khác nhau.
```

Nếu không hiểu cache effect, bạn sẽ:
- Đo sai baseline (cold run rất chậm → tưởng hệ thống yếu)
- Kết luận sai performance (warm run rất nhanh → tưởng hệ thống khoẻ)
- Benchmark sai giữa các phiên bản (version A chạy trước làm ấm cache cho version B chạy sau)

#### Các cấp độ cache trong hệ thống

```text
┌─────────────────────────────────────────────────┐
│ Cấp 1: Application Cache                         │
│   - In-memory cache (Redis, Memcached)           │
│   - Local cache (Caffeine, Ehcache, Guava)       │
│   - Cache tỉnh: danh mục, cấu hình, quyền        │
│   → Warm-up: cần 1-2 request để load cache       │
├─────────────────────────────────────────────────┤
│ Cấp 2: JVM / Runtime Cache                       │
│   - JIT Compilation (HotSpot: 10.000 lần gọi)    │
│   - Class loading, bytecode optimization          │
│   - Thread pool initialization                   │
│   → Warm-up: cần 1.000-10.000 request            │
├─────────────────────────────────────────────────┤
│ Cấp 3: Database Cache                            │
│   - Buffer pool / InnoDB Buffer (MySQL)          │
│   - Query cache, index cache                     │
│   - Connection pool (HikariCP, DBCP)             │
│   → Warm-up: cần vài phút để fill buffer pool    │
├─────────────────────────────────────────────────┤
│ Cấp 4: CDN / Reverse Proxy Cache                 │
│   - CloudFront, Cloudflare, Varnish, Nginx       │
│   - Cache static resources (css, js, ảnh)        │
│   → Warm-up: cần ít nhất 1 request/URL           │
├─────────────────────────────────────────────────┤
│ Cấp 5: OS / Kernel Cache                         │
│   - File system cache (page cache)               │
│   - DNS cache                                    │
│   - TCP connection reuse                         │
│   → Warm-up: tự nhiên theo thời gian             │
└─────────────────────────────────────────────────┘
```

#### Ví dụ thực tế — Cold Run vs Warm Run

```text
Test API GET /api/vouchers với 100 concurrent:

Lần chạy thứ    P95 RT    Ghi chú
────────────    ──────    ─────────────────────────────────
Cold (lần 1)    3.2s      DB chưa có cache, JIT chưa chạy
Lần 2           1.8s      Buffer pool đã nóng 1 phần
Lần 3           0.9s      Query cache hoạt động
Lần 4           0.5s      Cache ổn định (steady state)
Lần 5+          0.4-0.5s  Steady state

→ Nếu chỉ chạy lần 1 và kết luận "P95 = 3.2s" là SAI
→ Nếu chỉ chạy lần 4+ và kết luận "P95 = 0.5s" cũng SAI (bỏ qua cold start)
```

#### Hậu quả của cache effect nếu không xử lý

```text
1. Baseline sai → Kế hoạch capacity planning sai
2. So sánh A/B sai → Version mới chạy sau được hưởng cache của version cũ
3. Stress test sai → Tưởng hệ thống chịu được, nhưng vì đang cache
4. Endurance test sai → Kết luận "không memory leak" trong 2h nhưng thực ra
   cache chưa đầy, leak chỉ xuất hiện sau 4h+
```

### 5.2b. Cách Warm-up đúng

#### Nguyên tắc

```
Warm-up = Chạy một khoảng thời gian/request để đưa hệ thống
          về "trạng thái ổn định" (steady state) trước khi đo.
```

#### Các phương pháp warm-up

**Phương pháp 1 — Warm-up bằng JMeter iteration đầu (đơn giản nhất)**

```
Cấu hình:
  Loop Controller *2:
    Loop 1: Warm-up (không ghi metrics)
    Loop 2: Actual test (ghi metrics)

Hoặc dùng Thread Group với 2 giai đoạn:
  - 2-5 phút đầu là warm-up (bỏ qua trong phân tích)
  - Sau đó mới tính metrics
```

**Phương pháp 2 — Dùng Concurrent Thread Group với Schedule**

```text
bzm - Concurrency Thread Group:
  Hàng 1: 0 → target, ramp 120s, hold 300s ← 2p ramp + 5p warm-up
  Hàng 2: target → target, hold 1800s       ← 30p actual test

→ Kết quả: Bỏ qua 5 phút đầu (giai đoạn warm-up + ramp)
```

**Phương pháp 3 — Warm-up riêng trước test (recommended)**

```text
Bước 1: Chạy "warm-up script" riêng
  - Cùng số thread với test thật
  - Chạy 3-5 phút với tất cả các API/feature
  - Mục đích: load cache, kích hoạt JIT, fill connection pool

Bước 2: Chạy "test script" thật ngay sau warm-up
  - Không downtime giữa 2 bước
  - Metrics CHỈ lấy từ bước 2
```

**Phương pháp 4 — Warm-up bằng API call thủ công (cho môi trường mới)**

```batch
REM Script warm-up (dùng curl hoặc Postman)
curl -X POST https://api.kiemtoan.vn/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"warmup_user\",\"password\":\"xxx\"}"

curl https://api.kiemtoan.vn/api/vouchers?page=1&size=50
curl https://api.kiemtoan.vn/api/vouchers?page=2&size=50
curl https://api.kiemtoan.vn/api/dashboard
curl https://api.kiemtoan.vn/api/reports/summary
```

#### Dấu hiệu nhận biết warm-up đã hoàn thành

```text
Theo dõi real-time trong khi warm-up:

1. Response Time giảm dần và ổn định (không còn giảm nữa)
   ────
   \
    \──  Ổn định ở đây → warm-up xong
     \

2. Throughput tăng dần và ổn định
   ────────  Ổn định
   /
  /──  Tăng dần

3. Cache hit ratio (phía server) đạt đỉnh
   Ví dụ: Redis hit ratio từ 60% → 95%+ → warm-up xong

4. CPU / DB connection đạt steady state
   CPU: tăng → ổn định ở mức X%
   DB connections: tăng → ổn định ở mức Y
```

#### Warm-up time khuyến nghị theo từng loại test

```text
Loại test         Warm-up      Tổng thời gian   Ghi chú
───────────       ─────────    ───────────────  ──────────────────
Smoke             0 phút       2-3 phút         Không cần warm-up
Load (API)        2-5 phút     20-30 phút       Warm-up nhẹ
Load (Business)   3-5 phút     25-40 phút       JIT + DB cache
Stress            5 phút       20 phút          Warm-up đến steady state
Endurance         10 phút      8+ giờ           Warm-up bằng chính test
Spike             2 phút       10 phút          Warm-up với baseline
```

#### Lưu ý khi warm-up

```text
1. Không warm-up xong rồi đợi lâu mới test (cache sẽ hết hạn)
   → Nên chạy warm-up ngay trước test, tối đa cách 1-2 phút

2. Warm-up cần chạy đúng kịch bản (request, data) như test thật
   → Cache chỉ có tác dụng với các API đã gọi

3. Nếu test nhiều kịch bản liên tiếp, cần warm-up lại cho mỗi kịch bản
   → Kịch bản A dùng feature A, kịch bản B dùng feature B

4. Với endpoint mới chưa từng gọi, warm-up cần gọi qua endpoint đó
   → JIT chỉ compile code path nào đã được thực thi

5. Trong báo cáo, LUÔN ghi rõ đã warm-up chưa và warm-up bao lâu
   → Để người đọc hiểu context của kết quả
```

#### Cách xử lý trong JMeter — Cấu hình cụ thể

```text
Cách 1: Dùng 2 Thread Groups riêng
  Thread Group 1: Warm-up
    - Threads: 50% target
    - Loop: 2-5 lần
    - Không ghi file JTL
    - Không Assertion nặng

  Thread Group 2: Actual Test
    - Threads: target
    - Duration: 20-30 phút
    - Có ghi file JTL
    - Run Together (Run Thread Groups consecutively: ✓)

Cách 2: Dùng bzm - Concurrency Thread Group
  Hàng 1: Warm-up
    Start=0, End=target×0.5, Ramp=60s, Hold=120s
  Hàng 2: Actual Test
    Start=target×0.5, End=target, Ramp=60s, Hold=1800s

Cách 3: Dùng JSR223 để bỏ qua data warm-up
  Trong JSR223 Listener:
    if (vars.get("__iteration") < 5) {
      // Không ghi metrics cho 5 iteration đầu
      return
    }
    // Ghi metrics từ iteration thứ 6 trở đi
```

#### Checklist warm-up

- [ ] Cache server (Redis/Memcached) đã được warm trước khi test
- [ ] Database buffer pool đã đạt steady state
- [ ] JVM JIT compilation đã hoàn tất (theo dõi CPU giảm dần)
- [ ] Connection pools (DB, HTTP, gRPC) đã được khởi tạo đủ
- [ ] CDN cache đã được warm (nếu test qua CDN)
- [ ] Kết quả cold run và warm run được tách riêng trong báo cáo

### 5.4. Think Time tối ưu cho JMeter

```text
Không think time → Chỉ test khả năng xử lý "khô" của server
                   (saturate CPU/IO nhanh)

Có think time    → Mô phỏng sát thực tế, workload nhẹ nhàng hơn
                   (phù hợp test UX, capacity planning)

Khuyến nghị: Dùng Gaussian Random Timer (phân phối chuẩn)
             thay vì Uniform Random Timer (phân phối đều)
```



### 5.12. Kịch bản test mẫu

```text
Test 1: Smoke Test
  Threads: 5, Ramp-up: 10s, Duration: 5 phút
  Mục đích: Kiểm tra hệ thống còn sống

Test 2: Load Test (Business Flow)
  Threads: 500, Ramp-up: 300s, Duration: 1 giờ
  Mục đích: User Journey với 500 CCU

Test 3: Stress Test (API Component)
  Threads: 1000, Ramp-up: 600s, Duration: 30 phút
  Mục đích: Tìm breakpoint của API Login

Test 4: Endurance Test
  Threads: 300, Ramp-up: 300s, Duration: 8 giờ
  Mục đích: Phát hiện memory leak

Test 5: Spike Test
  Threads: 0 → 1000 trong 2s, Hold: 5 phút
  Mục đích: Kiểm tra auto-scaling
```

### 5.13. Checklist trước khi chạy Performance Test

- [ ] Dữ liệu test đã được prepare đầy đủ (CSV, DB records)
- [ ] Token/session hợp lệ, chưa expired
- [ ] Rate-limit / WAF đã được disable (nếu không test qua)
- [ ] CSV Data Config có đủ dữ liệu cho số threads tối đa
- [ ] Assertion chưa quá nặng (bỏ bớt assertion không cần thiết)
- [ ] Listeners (View Results Tree) đã tắt hoặc set ở chế độ ghi file
- [ ] Server monitoring tools đã sẵn sàng (Grafana, PerfMon)
- [ ] JMeter đã chạy ở chế độ Non-GUI (jmeter -n -t ...)
- [ ] Distributed agents (nếu có) đã đồng bộ thời gian (NTP)
- [ ] Đã warm-up hệ thống trước khi đo lường chính thức
- [ ] Kịch bản test có think time phù hợp (nếu test theo business flow)
- [ ] Đã backup dữ liệu test (tránh ảnh hưởng đến môi trường production)

---
