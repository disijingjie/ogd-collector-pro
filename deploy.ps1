# OGD-Collector Pro 一键部署脚本 (PowerShell)
# 用法: 右键 → 使用 PowerShell 运行

$ErrorActionPreference = "Stop"
$serverIP = "106.53.188.187"
$serverUser = "ubuntu"
$remotePath = "/opt/ogd-collector-pro"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  OGD-Collector Pro 一键部署" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Git提交
Write-Host "[1/4] 提交本地代码..." -ForegroundColor Yellow
Set-Location "C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system"
git add .
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
git commit -m "自动更新 $timestamp" 2>$null
git push origin main
Write-Host "[OK] Git推送成功" -ForegroundColor Green
Write-Host ""

# Step 2: 同步到服务器（用rsync或scp，比git pull更可靠）
Write-Host "[2/4] 同步代码到服务器..." -ForegroundColor Yellow
# 先ssh过去做git pull（如果GitHub能连的话）
$pullResult = ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 "$serverUser@$serverIP" "cd $remotePath && git pull origin main 2>&1" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[警告] GitHub连接慢，改用scp直接同步..." -ForegroundColor Yellow
    # 用scp同步templates和data目录
    scp -o StrictHostKeyChecking=no -r "templates" "$serverUser@${serverIP}:$remotePath/"
    scp -o StrictHostKeyChecking=no -r "data" "$serverUser@${serverIP}:$remotePath/"
    scp -o StrictHostKeyChecking=no "app.py" "$serverUser@${serverIP}:$remotePath/"
}
Write-Host "[OK] 服务器代码已更新" -ForegroundColor Green
Write-Host ""

# Step 3: 重启服务
Write-Host "[3/4] 重启服务..." -ForegroundColor Yellow
ssh -o StrictHostKeyChecking=no "$serverUser@$serverIP" "sudo systemctl restart ogd-collector && echo 'RESTART_OK'"
Write-Host "[OK] 服务已重启" -ForegroundColor Green
Write-Host ""

# Step 4: 验证
Write-Host "[4/4] 验证服务状态..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
$status = ssh -o StrictHostKeyChecking=no "$serverUser@$serverIP" "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:5000/v3/"
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
if ($status -eq "200") {
    Write-Host "  部署成功！✓" -ForegroundColor Green
} else {
    Write-Host "  服务返回状态: $status" -ForegroundColor Red
}
Write-Host "  http://$serverIP/v3/" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

pause