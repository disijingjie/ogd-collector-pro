@echo off
chcp 65001 >nul
echo ========================================
echo  OGD-Collector Pro 一键部署脚本
echo ========================================
echo.

echo [1/4] 提交本地代码...
cd /d C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system
git add .
git commit -m "自动更新 %date% %time%"
git push origin main
if errorlevel 1 (
    echo [错误] Git推送失败
    pause
    exit /b 1
)
echo [OK] Git推送成功
echo.

echo [2/4] 连接服务器并拉取代码...
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 ubuntu@106.53.188.187 "cd /opt/ogd-collector-pro && git pull origin main" 2>&1
if errorlevel 1 (
    echo [错误] 服务器代码拉取失败
    pause
    exit /b 1
)
echo [OK] 服务器代码已更新
echo.

echo [3/4] 重启服务...
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 ubuntu@106.53.188.187 "sudo systemctl restart ogd-collector && echo 'RESTART_OK'" 2>&1
if errorlevel 1 (
    echo [错误] 服务重启失败
    pause
    exit /b 1
)
echo [OK] 服务已重启
echo.

echo [4/4] 验证服务状态...
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 ubuntu@106.53.188.187 "sleep 2 && curl -s -o /dev/null -w '%%{http_code}' http://127.0.0.1:5000/v3/ && echo ''" 2>&1
echo.

echo ========================================
echo  部署完成！访问地址：
echo  http://106.53.188.187/v3/
echo ========================================
pause