@echo off
title Network Quick Check

echo ===== THONG TIN IP =====
ipconfig | findstr /i "IPv4 Default"

echo.
echo ===== KIEM TRA ROUTER =====
ping -n 1 192.168.0.1

echo.
echo ===== KIEM TRA INTERNET =====
ping -n 1 8.8.8.8

echo.
echo ===== KIEM TRA DNS =====
ping -n 1 google.com

echo.
pause