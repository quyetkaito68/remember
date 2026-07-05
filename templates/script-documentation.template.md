---
# ─── BẮT BUỘC ───────────────────────────────────────────
title: 'Tên Công Cụ / Script'
description: 'Mô tả chức năng và cách dùng script'
tags: [tag1, tag2, tag3]
category: 'tên-thư-mục'
updated: YYYY-MM-DD

# ─── TÙY CHỌN ───────────────────────────────────────────
order: 1
---

<!--
======================================================================
  TEMPLATE: SCRIPT DOCUMENTATION (Tài liệu công cụ / script)
  MỤC ĐÍCH:  Document script, công cụ, file config - ngắn gọn, đủ dùng
  PHÙ HỢP:   .bat, .ps1, .sql scripts, file config .json
  CÁCH DÙNG: Copy → đổi tên → điền nội dung
======================================================================
-->

# {{TÊN SCRIPT / CÔNG CỤ}}

> {{Mô tả 1-2 câu: công cụ này làm gì, khi nào cần dùng.}}

---

## Yêu cầu

<!-- AI: Liệt kê điều kiện để chạy được script này.
     - OS / phiên bản
     - Dependencies / phần mềm cần cài
     - Quyền (admin, user, v.v.) -->

- **Hệ điều hành:** …
- **Phần mềm:** …
- **Quyền:** …

---

## Cách sử dụng

<!-- AI: Hướng dẫn chạy script. Có thể gồm:
     - Dòng lệnh mẫu
     - Các bước chuẩn bị (nếu cần) -->

```bash
./script-name.bat [arguments]
```

hoặc

```powershell
.\script-name.ps1 [arguments]
```

---

## Tham số

<!-- AI: Nếu script nhận tham số, liệt kê trong table. -->

| Tham số | Kiểu   | Bắt buộc | Mô tả                      |
|---------|--------|----------|----------------------------|
| …       | string | Có       | …                          |
| …       | number | Không    | … (mặc định: …)            |

---

## Ví dụ

<!-- AI: Các tình huống sử dụng thực tế, kèm giải thích. -->

### Ví dụ 1: {{Mô tả tình huống}}

```bash
script-name.bat param1
```

{{Giải thích output / kết quả.}}

### Ví dụ 2: {{Mô tả tình huống khác}}

…

---

## Cấu hình (nếu có)

<!-- AI: Nếu script dùng file config, mô tả cấu trúc. -->

```json
{
  "key": "value"
}
```

---

## Ghi chú

<!-- AI: Cảnh báo, best practice, troubleshooting ngắn. -->

> **Lưu ý:** …

---

## Liên kết

- {{File script gốc: link đến file .bat/.ps1 cùng thư mục}}
- {{Tài liệu liên quan (nếu có)}}

---

<!--
======================================================================
  METADATA CHO AGENT
  - Loại: script-documentation
  - Luôn format code block với đúng language identifier
  - Table tham số đầy đủ: tên, kiểu, bắt buộc, mô tả
  - Có ít nhất 1 ví dụ cụ thể
======================================================================
-->
