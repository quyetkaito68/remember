---
title: Tạo Scheduled Task Trên Windows
description: 'Hướng dẫn tạo task chạy định kỳ bằng Task Scheduler — ví dụ với script clean-temp.bat dọn dẹp temp hàng ngày'
tags: [windows, task-scheduler, scheduled-task, automation, batch]
category: 'computer/windows'
updated: 2026-07-06
order: 1
---

# Tạo Scheduled Task Trên Windows

> Dùng **Task Scheduler** để chạy script / chương trình tự động vào thời gian định kỳ. Ví dụ: chạy `clean-temp.bat` mỗi ngày lúc 12h trưa.

---

## Trước khi bắt đầu

- Quyền **Administrator** trên máy.
- Script đã hoạt động đúng (test manual trước).
- Script cần chạy với quyền Admin? Nếu có, tích **Run with highest privileges** trong task.

---

## Cách 1: Tạo Task Bằng GUI (Task Scheduler)

### Bước 1: Mở Task Scheduler

```text
Win + R → taskschd.msc → Enter
```

### Bước 2: Tạo task mới

- Click **Create Task** (panel bên phải).
- Tab **General**:
  - **Name**: `Clean Temp Daily`
  - **Description**: (tuỳ chọn) `Dọn dẹp file tạm hàng ngày`
  - **Run whether user is logged on or not**: ✅
  - **Run with highest privileges**: ✅ (vì clean-temp.bat cần Admin)

### Bước 3: Tab Triggers — Lịch chạy

Click **New…**:

| Field | Giá trị |
|-------|---------|
| Begin the task | On a schedule |
| Daily | ✅ |
| Start | `07/07/2026 12:00:00` |
| Recur every | `1` days |
| Enabled | ✅ |

### Bước 4: Tab Actions — Hành động

Click **New…**:

| Field | Giá trị |
|-------|---------|
| Action | Start a program |
| Program/script | `C:\path\to\clean-temp.bat` |
| Start in | `C:\path\to\` |

### Bước 5: Tab Conditions & Settings

- **Conditions**: Bỏ tick **Stop if running for…** (nếu script chạy lâu).
  Bỏ **Start only if on AC power** nếu là laptop.
- **Settings**: Để mặc định.

### Bước 6: OK → Nhập password tài khoản → Done.

---

## Cách 2: Tạo Task Bằng Command Line (schtasks)

```bash
schtasks /Create /SC DAILY /TN "Clean Temp Daily" /TR "C:\path\to\clean-temp.bat" /ST 12:00 /RL HIGHEST /F
```

| Flag | Ý nghĩa |
|------|---------|
| `/SC DAILY` | Lặp lại hàng ngày |
| `/TN` | Tên task (hiển thị trong Task Scheduler) |
| `/TR` | Đường dẫn script / chương trình |
| `/ST 12:00` | Giờ chạy (HH:mm) |
| `/RL HIGHEST` | Run with highest privileges |
| `/F` | Ghi đè nếu task đã tồn tại |

Ví dụ với `clean-temp.bat`:

```bash
schtasks /Create /SC DAILY /TN "Clean Temp Daily" /TR "D:\scripts\clean-temp.bat" /ST 12:00 /RL HIGHEST /F
```

### Các tuỳ chọn lịch khác

```bash
# Mỗi giờ
schtasks /Create /SC HOURLY /TN "Task Name" /TR "script.bat" /RL HIGHEST /F

# Mỗi 30 phút
schtasks /Create /SC MINUTE /MO 30 /TN "Task Name" /TR "script.bat" /RL HIGHEST /F

# Mỗi thứ Hai hàng tuần lúc 8:00
schtasks /Create /SC WEEKLY /D MON /TN "Task Name" /TR "script.bat" /ST 08:00 /RL HIGHEST /F

# Khi máy tính khởi động
schtasks /Create /SC ONSTART /TN "Task Name" /TR "script.bat" /RL HIGHEST /F
```

---

## Quản lý Task

```bash
# Liệt kê tasks
schtasks /Query /FO TABLE

# Chạy task ngay lập tức
schtasks /Run /TN "Clean Temp Daily"

# Dừng task đang chạy
schtasks /End /TN "Clean Temp Daily"

# Xoá task
schtasks /Delete /TN "Clean Temp Daily" /F

# Export task ra XML (backup / deploy)
schtasks /Query /TN "Clean Temp Daily" /XML > clean-temp-task.xml

# Import task từ XML
schtasks /Create /XML clean-temp-task.xml /TN "Clean Temp Daily"
```

---

## Kiểm tra & Gỡ lỗi

### Task đã chạy chưa?

```
Task Scheduler → Task Scheduler Library → chọn task → tab History
```

### Lịch sử bằng command

```bash
# Xem log task trong 24h qua
wevtutil qe Microsoft-Windows-TaskScheduler/Operational /c:10 /rd:true /f:text
```

### Script chạy thủ công OK nhưng task không chạy?

| Nguyên nhân | Kiểm tra |
|-------------|----------|
| **Task không có quyền Admin** | Tab General → Run with highest privileges |
| **Path sai** | Tab Actions → kiểm tra Program/script và Start in |
| **Script cần thư mục làm việc** | Start in phải trỏ đúng thư mục chứa script |
| **User không có quyền log on as batch job** | Local Security Policy → Local Policies → User Rights → Adjust memory quotas… |

---

## Ghi chú

- **Task chạy kể cả khi user chưa login** nếu bạn chọn **Run whether user is logged on or not**.
- Nếu script có `pause` ở cuối → task sẽ treo vô hạn. Bỏ `pause` hoặc dùng `timeout /t 3 >nul`.
- Dùng **Export XML** để backup task, deploy sang máy khác.
- **clean-temp.bat** tham khảo tại `docs/utilities-script/clean-temp.bat` — script dọn `%TEMP%`, `C:\Windows\Temp` và Recycle Bin.

---

*Tài liệu được tạo ngày 06-07-2026 — Scheduled Task Windows.*
