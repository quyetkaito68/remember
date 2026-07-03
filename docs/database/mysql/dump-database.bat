@echo off

REM Thiet lap thong tin tai khoan
set "MYSQL_USER=apu"
set "MYSQL_PASSWORD=12345678@Abc"
set "DATABASE=db_t03c01_2023"
set "HOST=192.168.11.149"

REM Set the backup directory and filename
set "BACKUP_DIR=."
set "BACKUP_FILE=%BACKUP_DIR%\%DATABASE%.sql"

REM tao file backup db distribute 
REM chi lay cau truc va proceduce, data ngam dinh chay sau
mysqldump -h %HOST% -u %MYSQL_USER% -p%MYSQL_PASSWORD% --routines --triggers %DATABASE% > "%BACKUP_FILE%"

REM Check if the backup was successful
if %errorlevel% equ 0 (
    echo Backup completed successfully: %BACKUP_FILE%
) else (
    echo Backup failed!
)

pause

