---
title: Get database size
description: Truy vấn lấy kích thước dữ liệu, index và tổng dung lượng của từng bảng trong database MySQL.
tags: [mysql, sql, database, size, information-schema]
category: database
order: 9
updated: 2026-07-07
---

# Lấy kích thước các bảng trong MySQL

Truy vấn giúp xem dung lượng từng bảng trong một database MySQL — hữu ích khi cần kiểm tra dung lượng, tối ưu lưu trữ hoặc xác định bảng nào tốn nhiều tài nguyên nhất.

## Truy vấn

```sql
SELECT
    table_name,
    ROUND(data_length / 1024 / 1024, 2) AS data_mb,
    ROUND(index_length / 1024 / 1024, 2) AS index_mb,
    ROUND((data_length + index_length) / 1024 / 1024, 2) AS total_mb,
    table_rows
FROM information_schema.tables
WHERE table_schema = 'db_nmk2ab_2025'
ORDER BY (data_length + index_length) DESC;
```

## Giải thích cột

| Cột | Ý nghĩa |
|-----|---------|
| `table_name` | Tên bảng |
| `data_mb` | Kích thước dữ liệu (MB) — từ `data_length` |
| `index_mb` | Kích thước index (MB) — từ `index_length` |
| `total_mb` | Tổng dung lượng = data + index (MB) |
| `table_rows` | Số dòng ước tính (ước lượng của InnoDB, không chính xác tuyệt đối) |

## Cách dùng

1. Thay `'db_nmk2ab_2025'` bằng tên database thực tế của bạn.
2. Chạy truy vấn trong MySQL client, MySQL Workbench, hoặc phpMyAdmin.
3. Kết quả được sắp xếp từ bảng lớn nhất đến nhỏ nhất.

## Biến thể

### Lấy size cho database hiện tại

```sql
SELECT
    table_name,
    ROUND(data_length / 1024 / 1024, 2) AS data_mb,
    ROUND(index_length / 1024 / 1024, 2) AS index_mb,
    ROUND((data_length + index_length) / 1024 / 1024, 2) AS total_mb,
    table_rows
FROM information_schema.tables
WHERE table_schema = database()
ORDER BY total_mb DESC;
```

### Lấy tổng dung lượng toàn database

```sql
SELECT
    table_schema AS database_name,
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS total_mb,
    ROUND(SUM(data_length) / 1024 / 1024, 2) AS data_mb,
    ROUND(SUM(index_length) / 1024 / 1024, 2) AS index_mb
FROM information_schema.tables
WHERE table_schema = 'db_nmk2ab_2025'
GROUP BY table_schema;
```

### Hiển thị bằng GB

Thay `1024 / 1024` bằng `1024 / 1024 / 1024` và đổi tên cột từ `_mb` sang `_gb`.

## Ghi chú

- `data_length` và `index_length` trả về byte. Công thức chia cho `1024^2` để ra MB.
- Với InnoDB, `table_rows` là ước lượng dựa trên sampling, không chính xác như MyISAM.
- Để có số liệu chính xác nhất, chạy `ANALYZE TABLE` trước khi truy vấn.
