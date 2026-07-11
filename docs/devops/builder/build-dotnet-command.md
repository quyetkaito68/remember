---
title: Build C# Backend Solution — 3 Lệnh Dotnet Cốt Lõi
description: 'Ba lệnh dotnet clean, restore, build dùng để build project/solution C# backend trong CI/CD hoặc local'
tags: [dotnet, csharp, build, backend, ci-cd]
category: 'devops/builder'
updated: 2026-07-06
order: 1
---

# Build C# Backend Solution — 3 Lệnh Dotnet Cốt Lõi

> Ba lệnh chạy tuần tự để build một `.sln` hoặc project C# backend. Dùng cho local build và CI/CD pipeline.

```text
      dotnet clean
           │
           ▼
    dotnet restore
           │
           ▼
      dotnet build
```

## Flags chung — dùng cho cả 3 lệnh

| Flag | Ý nghĩa |
|------|---------|
| `-nologo` | Ẩn banner .NET |
| `-maxcpucount:5` | Dùng tối đa 5 CPU song song (chỉnh theo số core thật) |
| `-clp:ErrorsOnly` | Chỉ in lỗi ra console |

Các ví dụ bên dưới **không lặp lại** 3 flag này để giữ gọn.

---

## 1. Clean — Dọn dẹp output cũ

```bash
dotnet clean <flags chung> -c Release <solution.sln>
```

| Flag riêng | Ý nghĩa |
|------------|---------|
| `-c Release` | Xóa output của configuration Release |

Xóa thư mục `bin/Release/` và `obj/` để build sạch, tránh cache cũ.

---

## 2. Restore — Khôi phục package NuGet

```bash
dotnet restore <flags chung> <solution.sln>
```

Không có flag riêng — chỉ cần flags chung.

Tải dependency từ NuGet.org / private feed. Cần internet hoặc VPN vào NuGet feed nội bộ.

---

## 3. Build — Biên dịch mã nguồn

```bash
dotnet build <flags chung> --no-restore -c Release /p:Version=0.2.0.12 <project.csproj>
```

| Flag riêng | Ý nghĩa |
|------------|---------|
| `--no-restore` | Bỏ qua restore (đã chạy ở bước 2, tiết kiệm thời gian) |
| `-c Release` | Build ở chế độ Release (optimized) |
| `/p:Version=0.2.0.12` | Ghi đè version assembly (tùy chọn, không bắt buộc) |

**Lưu ý**: Lệnh này build theo `.csproj` (1 project). Muốn build cả solution, thay bằng đường dẫn `.sln`.

---

## Ví dụ chạy cả 3 lệnh

```bash
# Flags chung: -nologo -maxcpucount:5 -clp:ErrorsOnly
dotnet clean    -nologo -maxcpucount:5 -clp:ErrorsOnly -c Release D:\Project\Backend\MyApp.sln
dotnet restore  -nologo -maxcpucount:5 -clp:ErrorsOnly D:\Project\Backend\MyApp.sln
dotnet build    -nologo -maxcpucount:5 -clp:ErrorsOnly --no-restore -c Release /p:Version=1.0.0.0 D:\Project\Backend\MyApp\MyApp.csproj
```

---

## Ghi chú

- Đường dẫn `.sln` build cả solution; `.csproj` build 1 project.
- Nếu chạy `dotnet build` không có `--no-restore`, nó tự động restore lại → chậm hơn.
- `/p:Version=...` chỉ cần khi gắn version cụ thể cho artifact.

---

*Tài liệu được tạo ngày 06-07-2026 — 3 lệnh dotnet build C# backend.*
