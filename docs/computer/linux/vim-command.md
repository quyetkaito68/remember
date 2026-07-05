---
title: Vim — Các lệnh cơ bản để chỉnh sửa file
description: 'Các thao tác Vim cơ bản nhất: mở file, edit, save, delete, select, exit, và các mode.'
tags: [vim, linux, terminal, editor]
category: linux
updated: 2026-07-05
order: 1
---

# Vim — Các lệnh cơ bản

> Các thao tác Vim cần biết để chỉnh sửa file nhanh. Xem [tài liệu đầy đủ](https://vimhelp.org/) để biết thêm.

---

## Các mode trong Vim

| Mode | Gõ để vào | Mô tả |
|------|-----------|-------|
| **Normal** | `Esc` | Mode mặc định — di chuyển, xoá, copy, paste |
| **Insert** | `i` | Soạn thảo nội dung |
| **Visual** | `v` | Chọn (select) văn bản |
| **Command** | `:` | Gõ lệnh (save, quit, search, replace) |

---

## Mở file

```bash
vim ten-file.txt       # Mở file (tạo mới nếu chưa tồn tại)
vim -R ten-file.txt    # Mở ở chế độ read-only

# Mở ở dòng số cụ thể
vim +10 ten-file.txt   # Mở và nhảy tới dòng 10
```

---

## Soạn thảo (Insert mode)

Từ Normal mode, gõ:

| Phím | Chức năng |
|------|-----------|
| `i` | Insert tại vị trí con trỏ |
| `I` | Insert đầu dòng |
| `a` | Append — chèn sau con trỏ |
| `A` | Append cuối dòng |
| `o` | Mở dòng mới bên dưới |
| `O` | Mở dòng mới bên trên |
| `Esc` | Thoát Insert mode → về Normal |

---

## Lưu file & Thoát (Command mode)

Từ Normal mode, gõ `:` rồi một trong các lệnh sau:

| Lệnh | Chức năng |
|------|-----------|
| `:w` | Save |
| `:q` | Thoát (không cho thoát nếu chưa save) |
| `:wq` | Save + thoát |
| `:q!` | Thoát không save |
| `:w !sudo tee %` | Save khi quên `sudo` (Linux/macOS) |
| `:x` | Save + thoát (giống `:wq`) |

---

## Xoá dòng / ký tự (Normal mode)

| Phím | Chức năng |
|------|-----------|
| `x` | Xoá ký tự tại con trỏ |
| `dd` | Xoá dòng hiện tại |
| `3dd` | Xoá 3 dòng từ con trỏ trở xuống |
| `dw` | Xoá từ con trỏ đến cuối từ |
| `d$` hoặc `D` | Xoá từ con trỏ đến cuối dòng |
| `d0` | Xoá từ con trỏ đến đầu dòng |
| `di{` | Xoá nội dung bên trong `{ }` (hữu ích với code) |

---

## Chọn nội dung — Visual mode

| Phím | Chức năng |
|------|-----------|
| `v` | Chọn từng ký tự (dùng mũi tên để mở rộng) |
| `V` | Chọn từng dòng |
| `Ctrl+v` | Chọn theo cột (chọn khối chữ nhật) |
| Sau khi chọn: | `y` = copy, `d` = xoá, `>` = tăng indent, `<` = giảm indent |

---

## Undo / Redo

| Phím | Chức năng |
|------|-----------|
| `u` | Undo |
| `Ctrl+r` | Redo |

---

## Tài liệu tham khảo

- [Vim Help — toàn bộ lệnh](https://vimhelp.org/)
- [Vim Adventures](https://vim-adventures.com/) — học Vim qua game
- `vimtutor` — gõ lệnh này trong terminal để có bài hướng dẫn tương tác sẵn (dùng thử ngay: `vimtutor`)
- [Open Vim](https://www.openvim.com/) — interactive tutorial
