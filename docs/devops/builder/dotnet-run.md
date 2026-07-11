---
title: Run ASP.NET Core — Chạy Project Sau Khi Build
description: 'Hướng dẫn chạy file .dll của ASP.NET Core bằng CLI, thiết lập môi trường Development/Production'
tags: [dotnet, aspnetcore, run, cli, development]
category: 'devops/builder'
updated: 2026-07-11
order: 2
---

# Run ASP.NET Core — Chạy Project Sau Khi Build

> Sau khi build thành công, chạy trực tiếp file `.dll` bằng CLI để test local hoặc debug.

---

## Chạy cơ bản

```bash
dotnet <ten-project>.dll
```

Ví dụ:

```bash
dotnet MyApp.dll
```

---

## Chạy với môi trường cụ thể

Thiết lập biến môi trường trước khi chạy:

```powershell
$env:ASPNETCORE_ENVIRONMENT = "Development"
dotnet <ten-project>.dll
```

Hoặc dùng `set` (cmd):

```cmd
set ASPNETCORE_ENVIRONMENT=Development
dotnet <ten-project>.dll
```

### Các môi trường hợp lệ

| Menv | Mô tả |
|------|-------|
| `Development` | Phát triển local, bật debug, verbose log |
| `Staging` | Môi trường kiểm thử, gần production |
| `Production` | Môi trường vận hành thật |

---

## Ví dụ thực tế

```powershell
$env:ASPNETCORE_ENVIRONMENT = "Staging"
dotnet MyApp.dll
```

Log console sẽ hiển thị chi tiết, tương tự khi chạy trên Docker/Kubernetes.

---

## Lưu ý

- **Tên biến môi trường chuẩn**: `ASPNETCORE_ENVIRONMENT`.
- Nếu không set biến môi trường, ASP.NET Core mặc định dùng `Production`.
- Log output giống hệt khi image chạy trên container Docker/Kubernetes.

---

*Tài liệu được cập nhật ngày 11-07-2026 — chạy ASP.NET Core project sau build.*
