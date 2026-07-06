---
title: 'Build C# Backend Solution — 3 Lệnh Dotnet Cốt Lõi'
description: 'Ba lệnh dotnet clean, restore, build dùng để build project/solution C# backend trong CI/CD hoặc local'
tags: [dotnet, csharp, build, backend, ci-cd]
category: 'devops/builder'
updated: 2026-07-06
order: 1
---

# Build C# Backend Solution — 3 Lệnh Dotnet Cốt Lõi

> Ba lệnh chạy tuần tự để build một `.sln` hoặc project C# backend. Dùng cho local build và CI/CD pipeline.

---

## Thứ tự thực hiện

```text
      dotnet clean
           │
           ▼
    dotnet restore
           │
           ▼
     dotnet build
```

---

## 1. Clean — Dọn dẹp output cũ

```bash
dotnet clean -nologo -maxcpucount:5 -clp:ErrorsOnly -c Release <solution.sln>
```

| Flag | Ý nghĩa |
|------|---------|
| `-nologo` | Ẩn banner .NET |
| `-maxcpucount:5` | Dùng tối đa 5 CPU song song |
| `-clp:ErrorsOnly` | Chỉ in lỗi ra console |
| `-c Release` | Xóa output của configuration Release |

Xóa thư mục `bin/Release/` và `obj/` để build sạch, tránh cache cũ.

---

## 2. Restore — Khôi phục package NuGet

```bash
dotnet restore -nologo -maxcpucount:5 -clp:ErrorsOnly <solution.sln>
```

| Flag | Ý nghĩa |
|------|---------|
| `-nologo` | Ẩn banner .NET |
| `-maxcpucount:5` | Dùng tối đa 5 CPU song song |
| `-clp:ErrorsOnly` | Chỉ in lỗi ra console |

Tải các dependency từ NuGet.org / private feed về máy. Cần internet / VPN access vào NuGet feed nội bộ.

---

## 3. Build — Biên dịch mã nguồn

```bash
dotnet build -nologo --no-restore -maxcpucount:5 -clp:ErrorsOnly -c Release /p:Version=0.2.0.12 <project.csproj>
```

| Flag | Ý nghĩa |
|------|---------|
| `-nologo` | Ẩn banner .NET |
| `--no-restore` | Không chạy restore lại (đã chạy ở bước 2) |
| `-maxcpucount:5` | Dùng tối đa 5 CPU song song |
| `-clp:ErrorsOnly` | Chỉ in lỗi ra console |
| `-c Release` | Build ở chế độ Release (optimized) |
| `/p:Version=0.2.0.12` | Ghi đè version cho assembly |

**Lưu ý**: Lệnh này build theo `.csproj` (project), không build theo `.sln` (solution). Nếu build cả solution, dùng đường dẫn đến `.sln`.

---

## Ví dụ chạy cả 3 lệnh

```bash
dotnet clean -nologo -maxcpucount:5 -clp:ErrorsOnly -c Release D:\Project\Backend\MyApp.sln
dotnet restore -nologo -maxcpucount:5 -clp:ErrorsOnly D:\Project\Backend\MyApp.sln
dotnet build -nologo --no-restore -maxcpucount:5 -clp:ErrorsOnly -c Release /p:Version=1.0.0.0 D:\Project\Backend\MyApp\MyApp.csproj
```

---

## Ghi chú

- **`--no-restore` ở lệnh build** giúp tiết kiệm thời gian vì restore đã chạy riêng. Nếu chạy `dotnet build` không có flag này, nó sẽ tự động restore lại.
- **`-maxcpucount:5`** nên chỉnh theo số core CPU thật (ví dụ máy 8 core thì để 6-7).
- **`/p:Version=...`** chỉ cần khi muốn gắn version cụ thể cho artifact, không bắt buộc trong local dev.
- Đường dẫn có thể là `.sln` (solution) hoặc `.csproj` (project). `.sln` build cả solution; `.csproj` build một project.

---

*Tài liệu được tạo ngày 06-07-2026 — 3 lệnh dotnet build C# backend.*
