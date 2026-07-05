---
# ─── BẮT BUỘC ───────────────────────────────────────────
title: 'Tiêu Đề Hướng Dẫn'
description: 'Mô tả ngắn gọn nội dung (1-2 câu)'
tags: [tag1, tag2, tag3]
category: 'tên-thư-mục'       # Tên thư mục chứa file
updated: YYYY-MM-DD            # Ngày cập nhật gần nhất

# ─── TÙY CHỌN ───────────────────────────────────────────
order: 1                       # Vị trí sidebar (mặc định 999)
---

<!--
======================================================================
  TEMPLATE: TUTORIAL / GUIDE (Hướng dẫn từng bước)
  MỤC ĐÍCH:  Hướng dẫn step-by-step, ai cũng làm theo được
  PHÙ HỢP:   Git guide, Windows maintenance, Network basics, v.v.
  CÁCH DÙNG: Copy file này, đổi tên, điền nội dung theo hướng dẫn
  GIỮ NGUYÊN: comment <!-- AI: … --> để agent đọc được instruction
======================================================================
-->

# {{TIÊU ĐỀ BÀI VIẾT}}

> {{Mô tả ngắn gọn (1-2 câu) về mục tiêu và đối tượng của bài hướng dẫn này.}}

---

## Tổng quan

<!-- AI: Giới thiệu chủ đề. Giải thích:
     - Tại sao nội dung này hữu ích?
     - Vấn đề gì được giải quyết?
     - Đối tượng nào nên đọc?
     Viết 1-2 đoạn ngắn. -->

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque ut lectus vel urna facilisis tincidunt.

---

## Yêu cầu

<!-- AI: Liệt kê ĐIỀU KIỆN CẦN CÓ trước khi bắt đầu.
     - Phần mềm / công cụ đã cài: ghi rõ version tối thiểu
     - Kiến thức nền tảng
     - Quyền truy cập (admin, network, v.v.) -->

- **Phần mềm:** …
- **Kiến thức:** …
- **Quyền:** …

---

## Các bước thực hiện

<!-- AI: Chia thành các bước ĐÁNH SỐ. Mỗi bước gồm:
     - Mô tả NGẮN (1-3 câu)
     - Code block (nếu có) với language identifier
     - Kết quả mong đợi (nếu cần)
     KHÔNG gộp nhiều thao tác vào một bước. -->

### Bước 1: {{Mô tả bước 1}}

<!-- AI: Giải thích bước này làm gì, tại sao cần làm. -->

```bash
# Lệnh thực hiện
command --option value
```

Kết quả: {{mô tả kết quả mong đợi}}

### Bước 2: {{Mô tả bước 2}}

…

---

## Xử lý lỗi thường gặp

<!-- AI: Table 2 cột: Lỗi | Nguyên nhân & Cách xử lý.
     Chỉ thêm mục này nếu có lỗi phổ biến, không bắt buộc. -->

| Lỗi / Hiện tượng | Nguyên nhân & Cách xử lý |
|------------------|--------------------------|
| …                | …                        |

---

## Ghi chú

<!-- AI: Các lưu ý quan trọng, best practice, cảnh báo.
     Sử dụng định dạng: > Ghi chú, > Cảnh báo, ✅ Khuyến nghị -->

> **Lưu ý:** …

> **Cảnh báo:** …

✅ **Khuyến nghị:** …

---

## Tham khảo

<!-- AI: Link tham khảo, bài viết gốc, tài liệu chính thức. -->

- {{Tiêu đề link}} — {{mô tả ngắn}}

---

<!--
======================================================================
  METADATA CHO AGENT
  - Loại: tutorial-guide
  - Bắt buộc: title, description, tags, category, updated
  - Không bắt buộc: order
  - Sử dụng tiếng Việt có dấu trong toàn bộ nội dung
  - Code block luôn có ngôn ngữ identifier
  - Heading hierarchy: # → ## → ### (không nhảy cấp)
======================================================================
-->
