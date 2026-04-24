# OGD-Collector Pro 本地启动脚本
# 作者：文明

$projectPath = "C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system"
$pythonPath = "$projectPath\venv\Scripts\python.exe"

Set-Location $projectPath

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "OGD-Collector Pro 本地启动中..." -ForegroundColor Cyan
Write-Host "三层架构数据开放平台采集系统" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "访问地址: http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

& $pythonPath app.py
