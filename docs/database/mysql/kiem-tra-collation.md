---
title: Kiểm tra Collation MySQL
description: Hướng dẫn xác định các bảng và cột trong MySQL không dùng collation utf8mb4_0900_as_ci.
tags: [mysql, collation, sql, database]
category: database
order: 10
updated: 2026-07-04
---

# Kiểm tra Collation MySQL

Trang này chứa truy vấn để tìm tất cả bảng (`TABLE`) và cột (`COLUMN`) trong cơ sở dữ liệu hiện tại có `COLLATION` khác `utf8mb4_0900_as_ci`.

## Mục đích

- Xác định bảng/cột đang dùng collation không đồng nhất.
- Hỗ trợ việc chuẩn hóa dữ liệu về `utf8mb4_0900_as_ci`.
- Giảm lỗi so sánh chuỗi khi nối hoặc join giữa các bảng khác collation.

## Truy vấn

```sql
-- Liệt kê tất cả tables và columns có collation khác utf8mb4_0900_as_ci
SELECT 
    'TABLE' AS TYPE,
    T.TABLE_SCHEMA,
    T.TABLE_NAME,
    NULL AS COLUMN_NAME,
    T.TABLE_COLLATION AS COLLATION_NAME,
    CCSA.CHARACTER_SET_NAME
FROM information_schema.TABLES T
LEFT JOIN information_schema.COLLATION_CHARACTER_SET_APPLICABILITY CCSA 
    ON T.TABLE_COLLATION = CCSA.COLLATION_NAME
WHERE T.TABLE_SCHEMA = database()
    AND T.TABLE_COLLATION != 'utf8mb4_0900_as_ci'
    AND T.TABLE_TYPE = 'BASE TABLE'

UNION ALL

SELECT 
    'COLUMN' AS TYPE,
    TABLE_SCHEMA,
    TABLE_NAME,
    COLUMN_NAME,
    COLLATION_NAME,
    CHARACTER_SET_NAME
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = database()
    AND COLLATION_NAME IS NOT NULL
    AND COLLATION_NAME != 'utf8mb4_0900_as_ci'

ORDER BY TABLE_NAME, TYPE DESC, COLUMN_NAME;
```

## Giải thích

- `information_schema.TABLES`: kiểm tra collation của bảng.
- `information_schema.COLUMNS`: kiểm tra collation của từng cột.
- `TABLE_SCHEMA = database()`: chỉ xét cơ sở dữ liệu hiện tại.
- `COLLATION_NAME != 'utf8mb4_0900_as_ci'`: lọc ra các đối tượng có collation khác chuẩn.

## Cách dùng

1. Mở MySQL client hoặc MySQL Workbench.
2. Chạy truy vấn trong cơ sở dữ liệu cần kiểm tra.
3. Dựa vào kết quả để sửa các bảng hoặc cột về `utf8mb4_0900_as_ci`.

## Gợi ý chuẩn hóa

- Với bảng: `ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;`
- Với cột: `ALTER TABLE table_name MODIFY column_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;`

> Lưu ý: trước khi thay đổi collation, nên sao lưu dữ liệu và kiểm tra tương thích với ứng dụng.



