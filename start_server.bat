@echo off
chcp 65001 >nul
echo ============================================
echo   OGD-Collector Pro 三层架构采集系统
echo   政府数据开放平台采集与可视化系统
echo   作者：文明（武汉大学信息管理学院博士生）
echo ============================================
echo.
echo 正在初始化数据库...
C:\Users\MI\AppData\Local\Programs\Python\Python315\python.exe -c "from models import init_db, init_platforms_data; init_db(); init_platforms_data()"
echo 数据库初始化完成
echo.
echo 启动Web服务...
echo 访问地址: http://127.0.0.1:5000
echo.
C:\Users\MI\AppData\Local\Programs\Python\Python315\python.exe app.py
pause
