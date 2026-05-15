@echo off
chcp 65001 >nul
echo ============================================
echo   OGD-Collector Pro V6 - 本地开发服务器
echo ============================================

set PYTHON="C:\Users\MI\AppData\Local\Programs\Python\Python315\python.exe"
set PROJECT_DIR=C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system

cd /d %PROJECT_DIR%

echo [1/3] 检查 Flask 是否安装...
%PYTHON% -c "import flask" 2>nul
if errorlevel 1 (
    echo [INFO] Flask 未安装，正在安装依赖...
    %PYTHON% -m pip install flask werkzeug jinja2
    if errorlevel 1 (
        echo [ERROR] Flask 安装失败，请检查网络连接
        pause
        exit /b 1
    )
    echo [OK] Flask 安装完成
) else (
    echo [OK] Flask 已安装
)

echo [2/3] 启动本地服务器...
echo [INFO] 访问地址: http://127.0.0.1:5000/
echo [INFO] 按 Ctrl+C 停止服务器
echo ============================================

%PYTHON% run_local.py

pause
