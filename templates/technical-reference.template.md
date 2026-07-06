---
# ─── BẮT BUỘC ───────────────────────────────────────────
title: Tiêu Đề Kỹ Thuật
description: Mô tả vấn đề kỹ thuật và giải pháp
tags: [tag1, tag2, tag3]
category: tên-thư-mục
updated: YYYY-MM-DD

# ─── TÙY CHỌN ───────────────────────────────────────────
order: 1
---

<!--
======================================================================
  TEMPLATE: TECHNICAL REFERENCE (Tham khảo kỹ thuật)
  MỤC ĐÍCH:  Ghi lại vấn đề kỹ thuật, chẩn đoán và giải pháp
  PHÙ HỢP:   MySQL error, collation issues, troubleshooting
  CÁCH DÙNG: Copy → đổi tên → điền nội dung
======================================================================
-->

# {{TIÊU ĐỀ VẤN ĐỀ / GIẢI PHÁP}}

> {{Mô tả 1 câu: vấn đề này là gì, ảnh hưởng thế nào.}}

---

## Vấn đề

<!-- AI: Mô tả CHI TIẾT vấn đề.
     - Triệu chứng: lỗi gì xảy ra? (ghi nguyên văn error message)
     - Môi trường: OS, version, config liên quan
     - Khi nào xảy ra? -->

**Triệu chứng:**

```text
Error message đầy đủ (nếu có)
```

**Môi trường:** …

**Thời điểm xảy ra:** …

---

## Nguyên nhân

<!-- AI: Giải thích GỐC RỄ vấn đề.
     - Cơ chế: tại sao lỗi này xảy ra?
     - Link/tài liệu tham khảo nếu có. -->

{{Giải thích 1-3 đoạn.}}

---

## Cách chẩn đoán

<!-- AI: Các bước kiểm tra / xác nhận vấn đề.
     - Câu lệnh kiểm tra (SQL, command)
     - Kết quả mong đợi vs thực tế
     - Công cụ hỗ trợ -->

```sql
-- Câu lệnh kiểm tra
SELECT …
```

---

## Giải pháp

<!-- AI: Cách fix / workaround.
     - Các bước cụ thể (đánh số)
     - Lưu ý: ảnh hưởng, rủi ro, cần backup không? -->

### Cách 1: {{Tên cách xử lý}}

<!-- AI: Mô tả và các bước thực hiện. -->

```sql
-- Code / lệnh fix
```

### Cách 2: {{Tên cách xử lý khác}} (nếu có)

…

---

## Phòng ngừa

<!-- AI: Cách tránh lỗi tái diễn.
     - Config thay đổi
     - Monitoring
     - Best practice -->

- …

---

<!--
======================================================================
  METADATA CHO AGENT
  - Loại: technical-reference
  - Luôn ghi nguyên văn error message
  - Mỗi giải pháp ghi rõ ưu/nhược điểm
  - Code block dùng đúng language identifier
======================================================================
-->
