@echo off
setlocal
title Network Quick Check
set "PS=powershell -NoProfile -ExecutionPolicy Bypass -Command"

%PS% "Write-Host '==========================================' -ForegroundColor Cyan; Write-Host '       NETWORK QUICK CHECK (REMEMBER)' -ForegroundColor Cyan; Write-Host '==========================================' -ForegroundColor Cyan"
echo.

%PS% "Write-Host '===== 1. THONG TIN IP =====' -ForegroundColor Cyan"
ipconfig | findstr /i "IPv4 Default"
echo.

%PS% "Write-Host '===== 2. KIEM TRA ROUTER (192.168.0.1) =====' -ForegroundColor Cyan"
ping -n 1 192.168.0.1 >nul 2>&1
if errorlevel 1 (
    %PS% "Write-Host '[LOI] Khong ping duoc router.' -ForegroundColor Red; Write-Host '   Kiem tra: cap mang / Wifi da ket noi chua, router da bat nguon chua, card mang da bat chua.' -ForegroundColor DarkGray"
    set "ROUTER_OK=0"
) else (
    %PS% "Write-Host '[OK] Router truy cap duoc.' -ForegroundColor Green"
    set "ROUTER_OK=1"
)
echo.

%PS% "Write-Host '===== 3. KIEM TRA INTERNET (8.8.8.8) =====' -ForegroundColor Cyan"
ping -n 1 8.8.8.8 >nul 2>&1
if errorlevel 1 (
    %PS% "Write-Host '[LOI] Khong co ket noi Internet.' -ForegroundColor Red; Write-Host '   Nguyen nhan co the: modem/router loi duong WAN, ISP gap su co, hoac firewall chan ping ICMP.' -ForegroundColor DarkGray"
    set "NET_OK=0"
) else (
    %PS% "Write-Host '[OK] Co ket noi Internet.' -ForegroundColor Green"
    set "NET_OK=1"
)
echo.

%PS% "Write-Host '===== 4. KIEM TRA DNS (google.com) =====' -ForegroundColor Cyan"
ping -n 1 google.com >nul 2>&1
if errorlevel 1 (
    if "%NET_OK%"=="1" (
        %PS% "Write-Host '[LOI] Khong truy cap duoc google.com.' -ForegroundColor Red; Write-Host '   Nguyen nhan: Internet OK nhung DNS loi. Xu ly: ipconfig /flushdns, doi DNS ve 8.8.8.8 hoac 1.1.1.1.' -ForegroundColor DarkGray"
    ) else (
        %PS% "Write-Host '[LOI] Khong truy cap duoc google.com.' -ForegroundColor Red; Write-Host '   Nguyen nhan: mat Internet nen khong phan giai duoc ten mien - hoac DNS cung loi.' -ForegroundColor DarkGray"
    )
) else (
    %PS% "Write-Host '[OK] DNS phan giai tot.' -ForegroundColor Green"
)
echo.

%PS% "Write-Host '===== KET QUA TONG HOP =====' -ForegroundColor Cyan"
if "%NET_OK%"=="1" (
    %PS% "Write-Host '[OK] CO MANG - Internet dang hoat dong tot.' -ForegroundColor Green"
) else (
    %PS% "Write-Host '[LOI] KHONG CO MANG.' -ForegroundColor Red; Write-Host '   Nguyen nhan: mat ket noi voi router - kiem tra Wifi/cap mang/nguon router.' -ForegroundColor DarkGray"
)

if "%NET_OK%"=="1" (
    echo.
    %PS% "Write-Host '===== TOC DO MANG - BANDWIDTH =====' -ForegroundColor Cyan"
    powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='SilentlyContinue'; $idx=(Get-NetIPConfiguration|Where-Object{$_.IPv4DefaultGateway}|Select-Object -First 1).InterfaceIndex; if($idx){$ad=Get-NetAdapter -InterfaceIndex $idx; Write-Output ('Card dang dung: {0} - Bandwidth: {1}' -f $ad.Name,$ad.LinkSpeed)}"
)

echo.
pause
endlocal
