---
title: Restore MySQL Database
description: Khôi phục database MySQL từ file dump .sql bằng command mysql.
tags: [mysql, restore, database, backup]
category: database
updated: 2026-07-05
---

## Requirement

- MySQL Client (`mysql`) đã được cài đặt và có trong PATH.
- User có quyền `CREATE`, `ALTER`, `INSERT`, `DROP` trên database đích.
- File dump `.sql` (được tạo từ `mysqldump` hoặc tương tự).

## Script: `restore-database.bat`

Script cơ bản dùng để restore database từ file `.sql`.

## Cách sử dụng

```bat
REM Cơ bản
mysql -u username -p database_name < backup_file.sql

REM Với verbose output
mysql -u username -p -v database_name < backup_file.sql
```

Trong đó:

| Tham số | Ý nghĩa |
|---------|---------|
| `-u` | Username kết nối |
| `-p` | Nhắc nhập password (có thể viết liền `-pPass` nhưng không an toàn) |
| `-v` | Verbose mode — hiển thị chi tiết các câu lệnh đang chạy |
| `database_name` | Tên database cần restore (phải tồn tại trước) |
| `<` | Redirect file `.sql` vào stdin của mysql |

## Các option thường dùng

```bat
REM Nếu file dump có CREATE DATABASE, có thể bỏ qua bước tạo DB
mysql -u username -p < backup_file.sql

REM Tạo database trước rồi restore
mysql -u username -p -e "CREATE DATABASE IF NOT EXISTS db_name"
mysql -u username -p db_name < backup_file.sql

REM Restore với force (tiếp tục nếu gặp lỗi)
mysql -u username -p --force db_name < backup_file.sql

REM Restore file nén
gunzip -c backup.sql.gz | mysql -u username -p db_name

REM Restore từ xa qua SSH
ssh user@server "cat backup.sql" | mysql -u username -p db_name

REM Restore và xem tiến trình với pv (pipe viewer)
pv backup.sql.gz | gunzip | mysql -u username -p db_name
```

## Quy trình restore chuẩn

```bat
@echo off
set "MYSQL_USER=apu"
set "MYSQL_PASSWORD=12345678@Abc"
set "HOST=192.168.11.149"
set "DATABASE=db_t03c01_2023"
set "BACKUP_FILE=db_t03c01_2023.sql"

REM Tạo database nếu chưa tồn tại
mysql -h %HOST% -u %MYSQL_USER% -p%MYSQL_PASSWORD% -e "CREATE DATABASE IF NOT EXISTS %DATABASE%"

REM Restore
mysql -h %HOST% -u %MYSQL_USER% -p%MYSQL_PASSWORD% %DATABASE% < "%BACKUP_FILE%"

if %errorlevel% equ 0 (
    echo Restore completed successfully
) else (
    echo Restore failed!
)
```

## Lưu ý

- File dump không chứa `CREATE DATABASE` thì cần tạo database thủ công trước khi restore.
- Khi restore trên server khác, kiểm tra lại collation và charset cho khớp.
- Nên dùng `--force` để bỏ qua các lỗi không nghiêm trọng (ví dụ trigger đã tồn tại).
- File dump lớn nên nén `.sql.gz` để tiết kiệm dung lượng và thời gian truyền.
