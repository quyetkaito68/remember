---
title: JMeter — Chạy Test Plan Với jmeter-run.bat
description: 'Sử dụng file jmeter-run.bat để chạy JMeter non-GUI với test plan có sẵn, tự động sinh HTML report'
tags: [jmeter, performance-test, load-test, batch, windows]
category: 'developer/jmetter'
updated: 2026-07-06
order: 1
---

# JMeter — Chạy Test Plan Với jmeter-run.bat

> `jmetter-run.bat` là script batch chạy JMeter ở chế độ **non-GUI** (command line). Liệt kê các file `.jmx` trong thư mục test plan, cho phép chọn và chạy, tự động sinh JTL result + HTML report.

---

## Cấu hình

Mở `jmeter-run.bat` và sửa 2 đường dẫn đầu file:

```batch
set "JMETER_HOME=D:\0_FullShare\Jmeter\apache-jmeter-5.4.3"
set "TESTPLAN_DIR=D:\0_FullShare\Jmeter\PerformanceTestQTSX\testplan"
```

| Biến | Ý nghĩa |
|------|---------|
| `JMETER_HOME` | Thư mục cài JMeter (chứa `bin/jmeter.bat`) |
| `TESTPLAN_DIR` | Thư mục chứa các file `.jmx` (test plan) |

---

## Cách chạy

```bash
# Mở cmd / double-click file
jmetter-run.bat
```

Màn hình menu:

```
==========================================
       JMeter Test Plan Selection
==========================================
Directory: "D:\...\testplan"
dateStr: "20260706"

  1. Login_100Users
  2. Search_API_50Users
  3. CreateOrder_20Users

  0. Exit
==========================================
Select test (0-3):
```

Chọn số → xác nhận `y` → script chạy JMeter.

---

## Luồng xử lý

```
User chọn test plan
        │
        ▼
Kiểm tra file .jmx tồn tại
        │
        ▼
Tạo thư mục:
  testresult/<TestName>_YYYYMMDD/
  testreport/<TestName>_YYYYMMDD/
        │
        ▼
Chạy JMeter:
  jmeter -n -t <plan.jmx> -l <result.jtl> -e -o <report_dir> -f
        │
        ▼
Hỏi: Open HTML report?
  └─ y → mở browser
  └─ n → quay lại menu
```

### Giải thích lệnh JMeter

```bash
jmeter -n -t "<plan.jmx>" -l "<result.jtl>" -e -o "<report_dir>" -f
```

| Flag | Ý nghĩa |
|------|---------|
| `-n` | Non-GUI mode (chạy ngầm) |
| `-t` | Path đến file `.jmx` test plan |
| `-l` | Path ghi file kết quả `.jtl` |
| `-e` | Sinh HTML report sau khi chạy xong |
| `-o` | Thư mục xuất HTML report |
| `-f` | Ghi đè nếu file/thư mục đã tồn tại |

---

## Output

Sau khi chạy, cấu trúc thư mục:

```
testresult/
  Login_100Users_20260706/
    Login_100Users_20260706.jtl    <-- raw results
testreport/
  Login_100Users_20260706/
    index.html                     <-- HTML dashboard (mở browser)
    content/
    statistics.json
    ...
```

File `.jtl` dùng để import lại vào JMeter GUI sau này.

---

## Ghi chú

- Script dùng **PowerShell** để sắp xếp danh sách `.jmx` theo thứ tự tự nhiên (natural sort) như Windows Explorer — `Test2` đứng trước `Test10`.
- Cần **Java** (JRE/JDK) để chạy JMeter.
- Nếu thư mục `TESTPLAN_DIR` không có `.jmx` nào → báo lỗi và thoát.
- Có thể sửa script để thêm tùy chọn JMeter khác (thread count, ramp-up, v.v.).

---

*Tài liệu được tạo ngày 06-07-2026 — JMeter run script.*
