---
title: JMeter — Tạo Test Plan Cơ Bản
description: 'Hướng dẫn tạo test plan JMeter từ A-Z: record request, xử lý dữ liệu, trích xuất kết quả và sinh data'
tags: [jmeter, performance-test, test-plan, recording, csv, json-extractor, jsr223]
category: 'developer/jmetter'
updated: 2026-07-06
order: 2
---

# JMeter — Tạo Test Plan Cơ Bản

> Hướng dẫn từ record request → xử lý dữ liệu đầu vào/ra → chạy test plan. Dành cho người mới bắt đầu với JMeter.

---

## 1. Record Request

### 1.1. Cấu hình HTTP(S) Test Script Recorder

```
Test Plan
 └─ Non-Test Elements
     └─ HTTP(S) Test Script Recorder
```

**Cấu hình Recorder:**

| Field | Giá trị |
|-------|---------|
| Port | `8888` (mặc định) |
| Target Controller | Chọn Thread Group muốn lưu request |
| Grouping | Put each group in a new controller |

### 1.2. Cấu hình Browser Proxy

```
Windows: Settings → Network & Internet → Proxy
  - Use proxy: 127.0.0.1:8888
  - Bỏ qua: localhost, 127.*, 10.*, 192.168.* (tuỳ mạng)

Hoặc dùng extension: FoxyProxy (Chrome/Firefox)
```

### 1.3. Cài HTTPS certificate

```
Recorder → Options → Manager Certificates → Install
→ Import vào browser (Trusted Root Certification Authorities)
```

### 1.4. Record

- Click **Start** trên Recorder.
- Thao tác trên web như bình thường.
- Request sẽ tự động ghi vào Thread Group.

---

## 2. Request Filtering

Sau khi record, loại bỏ request không cần thiết.

### 2.1. Dùng URL Patterns to Include/Exclude

```
HTTP(S) Test Script Recorder → Requests Filtering
  - URL Patterns to Include: .*api.*, .*/rest/.*
  - URL Patterns to Exclude: .*\.css, .*\.js, .*\.png, .*\.ico, .*\.woff
```

### 2.2. Thủ công sau record

- Xoá request static resource (css, js, ảnh, font).
- Gom request cùng luồng vào **Transaction Controller**.
- Parameter hoá URL path, header, body.

---

## 3. CSV Data Set Config

Dùng để đọc dữ liệu đầu vào từ file `.csv` — ví dụ danh sách user, token, ID.

### 3.1. Chuẩn bị file CSV

```csv
username,password,token
user01,Pass@123,tok_abc_01
user02,Pass@123,tok_abc_02
user03,Pass@123,tok_abc_03
```

### 3.2. Thêm vào Thread Group

```
Thread Group
 └─ Config Element
     └─ CSV Data Set Config
```

| Field | Giá trị |
|-------|---------|
| Filename | `D:\data\users.csv` |
| Variable Names | `username,password,token` |
| Delimiter | `,` |
| Recycle on EOF | `False` |
| Stop thread on EOF | `True` (nếu số user = số thread) |
| Sharing mode | `All threads` |

### 3.3. Sử dụng biến

Trong request: `${username}`, `${password}`, `${token}`.

---

## 4. Hàm sinh dữ liệu

Dùng trong **User Parameters** hoặc trực tiếp trong request body.

### 4.1. UUID

```text
${__UUID()}
```
→ `550e8400-e29b-41d4-a716-446655440000`

### 4.2. Random number

```text
${__Random(1000,9999)}             → 7421
${__Random(0,100)}                 → 57
```

### 4.3. Random string

```text
${__RandomString(8,abcdefghijklmnopqrstuvwxyz)}    → hkfqapwx
${__RandomString(10,0123456789)}                   → 0485172396
```

### 4.4. Timestamp

```text
${__time(yyyy-MM-dd)}              → 2026-07-06
${__time(HH:mm:ss)}                → 14:30:00
${__time(yyyy-MM-dd HH:mm:ss)}     → 2026-07-06 14:30:00
${__time()}                        → 1817752200000 (millis)
```

### 4.5. Kết hợp trong User Parameters

```
Thread Group
 └─ Pre Processors
     └─ User Parameters
```

| Parameter | Value |
|-----------|-------|
| `requestId` | `REQ_${__time()}` |
| `uuid` | `${__UUID()}` |
| `userId` | `${__Random(10000,99999)}` |
| `timestamp` | `${__time(yyyy-MM-dd'T'HH:mm:ss)}` |

---

## 5. JSON Extractor

Trích xuất giá trị từ JSON response — dùng cho request sau (token, ID).

### 5.1. Thêm vào HTTP Request

```
HTTP Request
 └─ Post Processors
     └─ JSON Extractor
```

| Field | Giá trị | Ghi chú |
|-------|---------|---------|
| Name of created variables | `accessToken` | Tên biến để dùng lại |
| JSON Path expressions | `$.accessToken` | JSONPath đến field cần lấy |
| Match No. | `0` (Random) | 0=random, 1=đầu, -1=tất cả |
| Default Value | `NOT_FOUND` | Giá trị nếu không match |

### 5.2. Ví dụ JSONPath

```json
{
  "code": 200,
  "data": {
    "id": 12345,
    "name": "Nguyen Van A"
  },
  "items": [
    {"id": 1, "value": "a"},
    {"id": 2, "value": "b"}
  ]
}
```

| JSONPath | Kết quả |
|----------|---------|
| `$.data.id` | `12345` |
| `$.data.name` | `Nguyen Van A` |
| `$.items[0].id` | `1` |
| `$.items[*].value` | `["a","b"]` |

### 5.3. Sử dụng biến trích xuất

Request sau: `Authorization: Bearer ${accessToken}`

---

## 6. JSR223 PreProcessor

Chạy script Groovy trước khi request — dùng khi cần logic phức tạp hơn hàm built-in.

### 6.1. Thêm vào HTTP Request

```
HTTP Request
 └─ Pre Processors
     └─ JSR223 PreProcessor
```

| Field | Giá trị |
|-------|---------|
| Language | `groovy` |
| Script | (code Groovy) |

### 6.2. Các biến có sẵn trong script

| Biến | Ý nghĩa |
|------|---------|
| `vars` | Đọc/ghi biến JMeter (`vars.get()`, `vars.put()`) |
| `prev` | Truy cập kết quả sample trước đó |
| `props` | JMeter properties (global) |
| `log` | Logger |
| `sampler` | HTTP Sampler hiện tại |

### 6.3. Ví dụ — Tạo chữ ký SHA256

```groovy
import java.security.MessageDigest

def input = vars.get("rawData")
def digest = MessageDigest.getInstance("SHA-256")
def hash = digest.digest(input.getBytes("UTF-8")).encodeHex().toString()

vars.put("signature", hash)
```

Dùng trong request: `X-Signature: ${signature}`

### 6.4. Ví dụ — Format timestamp

```groovy
import java.time.*

def now = Instant.now().toString()
vars.put("isoTime", now)

// Date arithmetic: +7 ngày
def future = Instant.now().plus(Duration.ofDays(7))
vars.put("expireDate", future.toString())
```

---

## 7. Cấu trúc Test Plan hoàn chỉnh

```
Test Plan
 ├─ HTTP Request Defaults (base URL, content-type)
 ├─ HTTP Cookie Manager
 │
 └─ Thread Group (10 users, ramp-up 5s, loop 2)
     │
     ├─ Config Elements
     │   ├─ CSV Data Set Config → username,password
     │   └─ User Parameters → uuid, timestamp
     │
     ├─ Pre Processors
     │   └─ JSR223 PreProcessor → tạo signature
     │
     ├─ HTTP Request: POST /api/login
     │   └─ Post Processors
     │       └─ JSON Extractor → accessToken
     │
     ├─ HTTP Request: GET /api/users (Authorization: Bearer ${accessToken})
     │
     ├─ HTTP Request: POST /api/orders (body có UUID, timestamp)
     │
     └─ Listeners
         ├─ View Results Tree (debug)
         ├─ Summary Report
         └─ Aggregate Report
```

---

## Ghi chú

- **Record chỉ là bước đầu**: Luôn parameter hoá (URL, header, body) sau khi record.
- **Dùng Transaction Controller** để gom nhiều request thành một giao dịch.
- **JSON Extractor vs Regular Expression Extractor**: JSON Extractor nhanh hơn, dễ đọc hơn.
- **JSR223 dùng Groovy, không dùng BeanShell**: Groovy nhanh hơn, hỗ trợ đầy đủ Java syntax.
- **CSV nên đặt cùng thư mục với .jmx** và dùng relative path để dễ move.

---

*Tài liệu được tạo ngày 06-07-2026 — JMeter Test Plan.*
