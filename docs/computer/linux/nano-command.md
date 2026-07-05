---
title: Nano — Các lệnh cơ bản để chỉnh sửa file
description: 'Các thao tác Nano cơ bản nhất: mở file, edit, save, search, cut, exit.'
tags: [nano, linux, terminal, editor]
category: linux
updated: 2026-07-05
order: 2
---

# Nano — Các lệnh cơ bản

> Nano là text editor trong terminal, đơn giản hơn Vim — không có mode, gõ là được. Xem [tài liệu đầy đủ](https://www.nano-editor.org/docs.php) để biết thêm.

---

## Mở file

```bash
nano ten-file.txt        # Mở file (tạo mới nếu chưa tồn tại)
nano -m ten-file.txt     # Bật hỗ trợ mouse (click để di chuyển)
sudo nano /etc/hosts     # Mở file cần quyền root
```

---

## Các lệnh trong Nano

Tổ hợp phím dùng `Ctrl` (ký hiệu `^`) hoặc `Meta`/`Alt` (ký hiệu `M-`).

| Phím | Chức năng |
|------|-----------|
| `Ctrl+O` | Lưu file (WriteOut) — rồi Enter để xác nhận |
| `Ctrl+X` | Thoát — nếu chưa lưu sẽ hỏi |
| `Ctrl+S` | Lưu nhanh (không hỏi tên file) |
| `Ctrl+K` | Cut (cắt) dòng hiện tại |
| `Ctrl+U` | Paste (dán) |
| `Alt+6` hoặc `M+6` | Copy dòng hiện tại |
| `Ctrl+W` | Tìm kiếm (Search) — gõ từ khoá rồi Enter |
| `Ctrl+\` | Tìm và thay thế (Search & Replace) |
| `Ctrl+A` | Về đầu dòng |
| `Ctrl+E` | Về cuối dòng |
| `Ctrl+Y` | Lùi trang (Page Up) |
| `Ctrl+V` | Tiến trang (Page Down) |
| `Ctrl+G` | Xem help (danh sách đầy đủ các lệnh) |
| `Ctrl+C` | Hiển thị vị trí con trỏ (dòng, cột) |
| `Ctrl+_` | Nhảy tới dòng số cụ thể |
| `Alt+U` | Undo |
| `Alt+E` | Redo |
| `Ctrl+T` | Kiểm tra chính tả (nếu có hunspell/aspell) |
| `Ctrl+J` | Justify — căn chỉnh đoạn văn |

---

## Chọn nội dung (Select)

1. Đặt con trỏ tại vị trí bắt đầu
2. `Alt+A` hoặc `M+A` — bắt đầu chọn (mark)
3. Di chuyển con trỏ để mở rộng vùng chọn
4. `Ctrl+K` — cut vùng chọn, `Alt+6` — copy vùng chọn

---

## Tìm kiếm & Thay thế

```text
Ctrl+W  → gõ từ khoá → Enter → tìm tiếp bằng Alt+W
Ctrl+\  → gõ từ cần thay → Enter → gõ từ thay thế → chọn:
           Y = replace tại đây, A = replace tất cả, N = bỏ qua
```

---

## Giao diện Nano

Khi mở file, hai dòng dưới cùng hiển thị các lệnh phổ biến:

```text
^G Get Help  ^O WriteOut  ^W Where Is  ^K Cut Text  ^J Justify
^X Exit      ^R Read File  ^\ Replace   ^U Uncut     ^C Cur Pos
```

`^` nghĩa là phím `Ctrl` — `^G` = `Ctrl+G`.

---

## Tài liệu tham khảo

- [Nano Documentation](https://www.nano-editor.org/docs.php)
- [Nano Manual](https://www.nano-editor.org/dist/latest/nano.html)
- Gõ `Ctrl+G` trong Nano để xem help tích hợp sẵn
