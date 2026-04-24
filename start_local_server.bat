@echo off
chcp 65001 >nul
cd /d C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system
echo ========================================
echo OGD-Collector Pro 本地调试服务器
echo ========================================
echo 访问地址: http://127.0.0.1:5000
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.
C:\Users\MI\AppData\Local\Programs\Python\Python315\python.exe app.py
pause
