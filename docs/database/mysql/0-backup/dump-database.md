---
title: Backup MySQL Database với mysqldump
description: Script dump database MySQL tự động backup cấu trúc, procedures và triggers.
tags: [mysql, backup, mysqldump, database]
category: database
updated: 2026-07-05
---

## Requirement

- MySQL Client Tools (`mysqldump`) đã được cài đặt và có trong PATH.
- Quyền truy cập tới database (user có quyền `SELECT`, `SHOW VIEW`, `TRIGGER`, `LOCK TABLES`).

## Script: `dump-database.bat`

Script kết nối tới MySQL server và tạo file `.sql` backup tại thư mục hiện tại.

## Các tham số trong mysqldump

| Tham số | Ý nghĩa |
|---------|---------|
| `-h` | Hostname hoặc IP của MySQL server |
| `-u` | Username kết nối |
| `-p` | Password (viết liền sau `-p`, không space) |
| `--routines` | Backup stored procedures và functions |
| `--triggers` | Backup triggers |
| `<database>` | Tên database cần dump |
| `>` | Redirect output vào file `.sql` |

## Cách sử dụng

Chạy trực tiếp file `dump-database.bat`:

```bat
dump-database.bat
```

Kết quả: file `db_t03c01_2023.sql` được tạo trong cùng thư mục.

## Các option mysqldump thường dùng khác

```bat
REM Backup toàn bộ (dữ liệu + cấu trúc)
mysqldump -h HOST -u USER -pPASS --routines --triggers DB > backup.sql

REM Chỉ backup cấu trúc (không data)
mysqldump -h HOST -u USER -pPASS --no-data --routines --triggers DB > struct.sql

REM Chỉ backup dữ liệu (không cấu trúc)
mysqldump -h HOST -u USER -pPASS --no-create-info DB > data.sql

REM Backup nhiều database
mysqldump -h HOST -u USER -pPASS --databases DB1 DB2 DB3 > multi.sql

REM Backup tất cả database
mysqldump -h HOST -u USER -pPASS --all-databases > all.sql

REM Nén output để tiết kiệm dung lượng
mysqldump -h HOST -u USER -pPASS DB | gzip > backup.sql.gz
```

## Lưu ý bảo mật

- Password được hardcode trong file `.bat` — không nên commit lên git repository public.
- Nên sử dụng file config `.my.cnf` với permission hạn chế thay vì password trong script.
- Hoặc dùng environment variables để truyền password an toàn hơn.

Ví dụ dùng `.my.cnf`:

```ini
[mysqldump]
user=apu
password=12345678@Abc
host=192.168.11.149
```

Sau đó script chỉ cần:

```bat
mysqldump --routines --triggers db_t03c01_2023 > backup.sql
```
