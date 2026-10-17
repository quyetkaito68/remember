---
title: Windows Startup App
description: 'Các cơ chế khởi động ứng dụng cùng Windows — Startup folder, Registry Run, Task Scheduler, Autoruns'
tags: [windows, startup, auto-start, task-scheduler, autoruns]
category: 'computer/windows'
updated: 2026-08-19
order: 2
---

# Windows Startup App

> Các cách để ứng dụng tự chạy khi đăng nhập Windows — từ đơn giản nhất (Startup folder) đến chuyên nghiệp nhất (Task Scheduler).

---

## Tổng quan

| Cơ chế | Độ phức tạp | Ủy quyền Admin | Chạy khi chưa login | Phù hợp |
|--------|:-----------:|:--------------:|:--------------------:|----------|
| **Startup folder** | ★☆☆ | Không | Không | App cá nhân, chạy nhanh |
| **Registry Run** | ★★☆ | Không (HKCU) / Có (HKLM) | Không | App cần registry-based startup |
| **Task Scheduler** | ★★★ | Tùy chọn | Có | Service-like, cần delay, restart, admin |
| **Autoruns** | ★★★★ | Có | — | Debug / audit toàn bộ startup |

---

## Cách 1: Startup Folder

Đơn giản nhất — copy shortcut vào thư mục Startup.

### Mở Startup folder

```text
Win + R → shell:startup → Enter
```

Đường dẫn thực tế:

```text
C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

### Thêm ứng dụng

1. Tạo Shortcut cho `.exe` (chuột phải → Send to → Desktop (create shortcut)).
2. Copy shortcut vào thư mục Startup.
3. Đăng nhập lại → Windows tự chạy.

> **Lưu ý:** Nên dùng Shortcut, không cần copy trực tiếp `.exe` vào thư mục.

### Startup folder cho tất cả user

```text
Win + R → shell:common startup → Enter
```

```text
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp
```

| Command | Phạm vi |
|---------|---------|
| `shell:startup` | Chỉ user hiện tại |
| `shell:common startup` | Tất cả user trên máy |

---

## Cách 2: Registry Run

Windows đọc key `Run` mỗi khi user đăng nhập.

### Hai vị trí quan trọng

| Key | Phạm vi | Quyền Admin |
|-----|---------|:-----------:|
| `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` | User hiện tại | Không |
| `HKLM\Software\Microsoft\Windows\CurrentVersion\Run` | Toàn hệ thống | Có |

### Thêm entry

Mở `regedit`, navigate đến một trong hai key trên, tạo **String Value (REG_SZ)**:

```
Tên: MyApp
Giá trị: "D:\MyApp\MyApp.exe"
```

Windows sẽ chạy `MyApp.exe` khi user đăng nhập.

### Xoá entry

Xoá String Value tương ứng trong Registry.

---

## Cách 3: Task Scheduler (Chuyên nghiệp)

Phù hợp khi ứng dụng cần:

- Chạy với quyền **Administrator**
- Chạy khi Windows khởi động (trước/sau login)
- **Delay** vài giây sau login
- Chạy dù **chưa đăng nhập**
- **Restart** khi crash
- Chạy theo điều kiện (triggers)

### Tạo task bằng GUI

```text
Win + R → taskschd.msc → Enter
```

```text
Task Scheduler
    └→ Create Task
        ├→ Triggers: At log on / At startup
        └→ Actions:  Start a program → D:\MyApp\myapp.exe
```

### Tạo task bằng command

```bash
schtasks /Create /SC ONLOGON /TN "MyApp" /TR "D:\MyApp\MyApp.exe" /RL HIGHEST /F
```

| Flag | Ý nghĩa |
|------|---------|
| `/SC ONLOGON` | Chạy khi user đăng nhập |
| `/TN` | Tên task |
| `/TR` | Đường dẫn chương trình |
| `/RL HIGHEST` | Quyền Administrator |
| `/F` | Ghi đè nếu đã tồn tại |

> Chi tiết tạo Scheduled Task → xem [Tạo Task Windows](/computer/windows/create-task).

---

## Cách 4: Autoruns (Debug / Audit)

**Autoruns** (Sysinternals) — công cụ của Microsoft để xem toàn bộ startup points trên Windows.

### Cài đặt

Tải từ: https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns

### Dùng

```text
autoruns.exe → tab "Everything"
```

Hiển thị tất cả vị trí Windows có thể tự chạy chương trình:

| Vị trí | Ghi chú |
|--------|---------|
| Startup folder | `shell:startup` |
| Registry Run | `HKCU/HKLM\...\Run` |
| Scheduled Tasks | Task Scheduler |
| Services | Windows Services |
| Drivers | Kernel drivers |
| Explorer extensions | Shell extensions |
| Winlogon | Login-related |
| AppInit | DLL load on app start |

> **Dùng Autoruns để:** audit ứng dụng nào đang tự khởi động, tìm malware, dọn startup thừa.

---

## So sánh nhanh

```text
Đơn giản ──────────────────────────────── Chuyên nghiệp

Startup Folder → Registry Run → Task Scheduler → Services
  (shortcut)     (REG_SZ)      (trigger/action)   (service)
```

### Khi nào dùng gì?

| Nhu cầu | Dùng |
|---------|------|
| App cá nhân, chạy khi login | Startup folder |
| App cần registry integration | Registry Run |
| App cần admin, delay, restart, chạy trước login | Task Scheduler |
| App chạy liên tục 24/7, start khi boot | Windows Services |

---

## Ghi chú

- **Startup folder**: nhanh nhất nhưng ít control nhất.
- **Registry Run**: phổ biến, dễ quản lý qua `regedit`.
- **Task Scheduler**: linh hoạt nhất cho ứng dụng tự viết, đặc biệt app chạy nền/service-like.
- **Autoruns**: không phải cơ chế startup, mà là công cụ audit/debug toàn bộ startup system.
- Đường dẫn sâu hơn về Windows startup: `Startup folder → Registry Run → Task Scheduler → Services → Winlogon → Autoruns → Windows Internals`.
