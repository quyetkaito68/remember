@echo off

:: xin quyền admin
NET SESSION >nul 2>&1
if %errorLevel% neq 0 (
    echo Dang xin quyen admin...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit
)

echo ==== Don dep file tam (Temp) ====

echo Dang xoa %TEMP% ...
del /s /f /q "%TEMP%\*.*" >nul 2>&1
for /d %%p in ("%TEMP%\*") do rmdir /s /q "%%p" >nul 2>&1

echo Dang xoa C:\Windows\Temp ...
del /s /f /q "C:\Windows\Temp\*.*" >nul 2>&1
for /d %%p in ("C:\Windows\Temp\*") do rmdir /s /q "%%p" >nul 2>&1

echo Dang don dep Recycle Bin...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"

rd /s /q C:\$Recycle.Bin >nul 2>&1

echo ==== Hoan thanh ====
@REM pause