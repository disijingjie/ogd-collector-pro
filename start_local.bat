@echo off
chcp 65001 >nul
cd /d C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system

REM 激活虚拟环境并启动服务
venv\Scripts\python.exe app.py

pause
