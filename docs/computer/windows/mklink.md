---
title: 'Mklink — Symbolic Link Trên Windows'
description: 'Cách tạo symbolic link (symlink) trên Windows bằng lệnh mklink — trỏ folder/file ảo đến vị trí thật'
tags: [windows, mklink, symlink, symbolic-link, cmd]
category: 'computer/windows'
updated: 2026-07-06
order: 1
---

# Mklink — Symbolic Link Trên Windows

> `mklink` tạo symbolic link — một "con trỏ" xuất hiện như folder/file thật nhưng thực chất trỏ đến một đường dẫn khác. Giống shortcut nhưng trong suốt với ứng dụng.

---

## Cú pháp

```bash
mklink <Link> <Target>
mklink /D <Link> <Target>   # Directory symlink
mklink /H <Link> <Target>   # Hard link (file only)
mklink /J <Link> <Target>   # Junction (directory only)
```

| Flag | Loại | Ghi chú |
|------|------|---------|
| (none) | File symlink | Link đến file |
| `/D` | Directory symlink | Link đến thư mục |
| `/H` | Hard link | Cùng file vật lý, không phải con trỏ |
| `/J` | Junction | Giống `/D` nhưng chỉ local, không hỗ trợ UNC path |

---

## Cách dùng

### Symbolic link cho thư mục

```bash
#   Link                  Target
mklink /D "C:\MySymLink" "D:\TargetFolder"
```

Kết quả: Xuất hiện folder `C:\MySymLink` có icon folder kèm mũi tên nhỏ — trỏ đến `D:\TargetFolder`.

### Symbolic link cho file

```bash
mklink "C:\MyFileLink.txt" "D:\TargetFile.txt"
```

### Junction — trỏ đến UNC path

```bash
mklink /J "D:\DevelopProduction\AMISBASE" "D:\AMISBASE"
mklink /J "\\nvquyet-vdi\AMISBASE" "D:\AMISBASE"
mklink /J "D:\DevelopKiemToanMAU\AMISBASE" "D:\AMISBASE_net8\AMISBASE"
```

> **Lưu ý:** `/J` (Junction) hỗ trợ UNC path (`\\server\share`); `/D` thì không.

---

## Xoá symbolic link

Chỉ xoá link, **không ảnh hưởng** đến target.

```bash
# Directory symlink
rmdir "C:\MySymLink"

# File symlink
del "C:\MyFileLink.txt"
```

> Không dùng `rmdir /s` — sẽ xoá luôn dữ liệu target nếu link hỏng hoặc hard link.

---

## Yêu cầu quyền

- File symlink (`mklink` không flag) cần quyền **Developer Mode** (Windows 10+).
- Directory symlink (`mklink /D`) và Junction (`mklink /J`) cần **Run as Administrator**.

```
# Chạy cmd với quyền Administrator
mklink /D "D:\DevelopProduction\AMISBASE" "D:\AMISBASE"
```

---

## Ghi chú

- **Không nhầm với shortcut**: Shortcut (`.lnk`) là file riêng, ứng dụng không tự động follow. Symlink trong suốt — ứng dụng nghĩ đó là folder/file thật.
- **Xoá link KHÔNG xoá target**: Chỉ xoá con trỏ, dữ liệu gốc vẫn còn.
- **Coi chừng xoá nhầm**: Nếu dùng `rmdir /s` trên symlink và target không tồn tại → có thể tạo folder rỗng thay vì báo lỗi.
- **Relative path**: Link có thể dùng relative path, không nhất thiết là absolute.

---

*Tài liệu được tạo ngày 06-07-2026 — Mklink Windows.*
