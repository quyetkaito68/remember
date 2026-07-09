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

## Yêu cầu hệ thống

### 1. Cài đặt Java (JRE/JDK)

JMeter chạy trên nền Java, yêu cầu **Java 8+** (khuyến nghị Java 11 hoặc 17).

**Tải Java:**
- **JDK (khuyến nghị)**: https://adoptium.net/ (Temurin JDK 11/17)
- **JRE**: https://www.java.com/download/

**Kiểm tra sau khi cài:**
```bash
java -version
```
Output mẫu:
```
java version "17.0.12" 2024-07-16 LTS
Java(TM) SE Runtime Environment (build 17.0.12+8)
```

### 2. Tải & Giải nén JMeter

**Tải tại:** https://jmeter.apache.org/download_jmeter.cgi

Chọn bản **Binaries** (`.zip`), ví dụ: `apache-jmeter-5.6.3.zip`. Giải nén vào thư mục bất kỳ, không cần cài đặt.

```
Ví dụ:
  D:\0_FullShare\Jmeter\apache-jmeter-5.4.3\
    ├── bin/
    ├── lib/
    ├── docs/
    └── ...
```

### 3. Chạy JMeter GUI (Kiểm tra)

```bash
# Windows
D:\0_FullShare\Jmeter\apache-jmeter-5.4.3\bin\jmeter.bat

# hoặc dùng jmeter.bat (double-click)
```

JMeter GUI sẽ mở ra → Kiểm tra version ở menu **Help > About Apache JMeter**.

> **Lưu ý:** Trong tài liệu này, `%JMETER_HOME%` là thư mục cài JMeter (ví dụ: `D:\0_FullShare\Jmeter\apache-jmeter-5.4.3`).

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

## Lỗi có thể gặp

### 1. `'java' is not recognized as an internal or external command`

**Nguyên nhân:** Java chưa được cài hoặc chưa set PATH.

**Xử lý:**
- Cài Java (xem [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)).
- Hoặc set thủ công trong `jmeter-run.bat`:
  ```batch
  set "JAVA_HOME=C:\Program Files\Java\jdk-17"
  set "PATH=%JAVA_HOME%\bin;%PATH%"
  ```

### 2. `Error: Unable to access jarfile ...\ApacheJMeter.jar`

**Nguyên nhân:** `JMETER_HOME` trỏ sai thư mục.

**Xử lý:**
- Kiểm tra lại `JMETER_HOME` trong `jmeter-run.bat` — phải trỏ đến thư mục gốc của JMeter (thư mục chứa `bin/jmeter.bat`).
- Đảm bảo đường dẫn không có khoảng trắng, hoặc nếu có phải dùng `""`.

### 3. `java.lang.OutOfMemoryError: Java heap space`

**Nguyên nhân:** JMeter không đủ bộ nhớ heap.

**Xử lý:**
- Tăng heap trong `jmeter.bat` hoặc file `setenv.bat`:
  ```batch
  set HEAP="-Xms1g -Xmx4g"
  ```
- Hoặc set trong `jmeter-run.bat` trước lệnh gọi JMeter:
  ```batch
  set "JVM_ARGS=-Xms1g -Xmx4g"
  ```

### 4. `Engine is busy, please try later` / Không chạy được test plan từ menu

**Nguyên nhân:** File `.jmx` bị lỗi syntax hoặc thiếu thư viện.

**Xử lý:**
- Mở file `.jmx` bằng JMeter GUI kiểm tra trước.
- Đảm bảo có đủ plugin (ví dụ: jp@gc, bzm) nếu test plan dùng plugin mở rộng.
- Tải plugin thiếu qua **JMeter Plugin Manager** (`Options > Plugins Manager`).

### 5. `CannotResolveClassException: com.blazemeter.jmeter.threads.concurrency.ConcurrencyThreadGroup`

**Nguyên nhân:** Test plan dùng plugin **bzm - Concurrency Thread Group** nhưng chưa cài.

**Xử lý:**
- Cài **Plugins Manager** (nếu chưa có):
  - Tải `plugins-manager.jar` từ https://jmeter-plugins.org/install/Install/
  - Copy vào `%JMETER_HOME%/lib/ext/`
- Mở JMeter GUI → **Options > Plugins Manager** → tab **Available Plugins**
- Tìm `bzm - Concurrency Thread Group` → check **Install** → restart JMeter.
- Nếu chạy non-GUI, plugin đã tự động được load — không cần cấu hình thêm.

### 6. **Non-GUI mode:**
```
jmeter -n -t ...
```
Lỗi: `errorlevel=1` hoặc không sinh được file JTL.

**Xử lý:**
- Đảm bảo thư mục output (`testresult`, `testreport`) đã được tạo trước hoặc lệnh JMeter dùng flag `-f`.
- Kiểm tra dung lượng ổ đĩa — nếu hết disk, JMeter không thể ghi file.

---

## Ghi chú

- Script dùng **PowerShell** để sắp xếp danh sách `.jmx` theo thứ tự tự nhiên (natural sort) như Windows Explorer — `Test2` đứng trước `Test10`.
- Cần **Java** (JRE/JDK) để chạy JMeter.
- Nếu thư mục `TESTPLAN_DIR` không có `.jmx` nào → báo lỗi và thoát.
- Có thể sửa script để thêm tùy chọn JMeter khác (thread count, ramp-up, v.v.).

---

*Tài liệu được tạo ngày 06-07-2026 — JMeter run script.*


Lỗi có thể gặp: Problem loading XML from:'C:\Users\quyet\Downloads\mauperformancetest\testplan\1-audit-period-management.jmx'. 
Cause:
CannotResolveClassException: com.blazemeter.jmeter.threads.concurrency.ConcurrencyThreadGroup

 Detail:com.thoughtworks.xstream.converters.ConversionException: 
---- Debugging information ----
cause-exception     : com.thoughtworks.xstream.converters.ConversionException
cause-message       : 
first-jmeter-class  : org.apache.jmeter.save.converters.HashTreeConverter.unmarshal(HashTreeConverter.java:66)
class               : org.apache.jmeter.save.ScriptWrapper
required-type       : org.apache.jmeter.save.ScriptWrapper
converter-type      : org.apache.jmeter.save.ScriptWrapperConverter
path                : /jmeterTestPlan/hashTree/hashTree/com.blazemeter.jmeter.threads.concurrency.ConcurrencyThreadGroup
line number         : 209
version             : 5.6.3
-------------------------------

 => do chưa cài plugin bzm
