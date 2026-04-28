#!/usr/bin/env pwsh
# OGD-Collector Pro 一键同步脚本
# 功能：本地代码直接同步到服务器 + GitHub备份
# 用法：右键 → 使用 PowerShell 运行

$ErrorActionPreference = "Stop"

# 配置
$ServerIP    = "106.53.188.187"
$ServerUser  = "ubuntu"
$RemotePath  = "/opt/ogd-collector-pro"
$LocalPath   = "C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system"
$ServiceName = "ogd-collector"

function Write-Color($text, $color) { Write-Host $text -ForegroundColor $color }

Write-Color "========================================" Cyan
Write-Color "  OGD-Collector Pro 一键同步" Cyan
Write-Color "========================================" Cyan
Write-Color "" White

# Step 0: 检测免密登录
Write-Color "[0/5] 检测SSH免密登录..." Yellow
$test = & ssh -o BatchMode=yes -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$ServerUser@$ServerIP" "echo OK" 2>&1
if ($test -notmatch "OK") {
    Write-Color "      SSH免密登录未配置！" Red
    Write-Color "      请先运行桌面的 fix-ssh-once.ps1 配置免密" Yellow
    Write-Color "      按任意键退出..." DarkGray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}
Write-Color "      SSH免密正常" Green

# Step 1: Git 提交（仅备份，不阻塞）
Write-Color "[1/5] Git 提交（备份到GitHub）..." Yellow
try {
    Set-Location $LocalPath
    git add -A 2>$null
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "sync: $timestamp" 2>$null | Out-Null
    git push origin main 2>$null | Out-Null
    Write-Color "      GitHub备份完成" Green
} catch {
    Write-Color "      GitHub备份跳过（无网络或无需提交）" DarkGray
}

# Step 2: 直接同步文件到服务器
Write-Color "[2/5] 同步文件到服务器..." Yellow
Set-Location $LocalPath

# 用tar打包排除不需要的文件
$tarFile = "$env:TEMP\ogd-sync-$(Get-Date -Format 'yyyyMMdd-HHmmss').tar.gz"
try {
    Write-Color "      打包本地文件..." DarkGray
    & tar -czf $tarFile --exclude="venv" --exclude="__pycache__" --exclude=".git" --exclude=".workbuddy" --exclude="*.pyc" --exclude="*.log" --exclude="*.err" --exclude="_*.json" --exclude="_*.zip" --exclude="sync-to-server.ps1" --exclude="deploy.ps1" --exclude="deploy.bat" .
    if ($LASTEXITCODE -ne 0) { throw "tar打包失败" }
    $sizeKB = [math]::Round((Get-Item $tarFile).Length/1KB,1)
    Write-Color "      打包完成: ${sizeKB} KB" DarkGray

    # scp传输到服务器
    Write-Color "      传输到服务器..." DarkGray
    & scp -o StrictHostKeyChecking=no -o ConnectTimeout=10 $tarFile "$ServerUser@${ServerIP}:/tmp/ogd-sync.tar.gz"
    if ($LASTEXITCODE -ne 0) { throw "scp传输失败" }
    Write-Color "      传输完成" Green

    # 服务器端解压部署
    Write-Color "[3/5] 服务器端部署..." Yellow
    $deployScript = @"
set -e
cd $RemotePath
# 备份当前代码
BACKUP_DIR="/opt/backups/ogd-\$(date +%Y%m%d-%H%M%S)"
mkdir -p \$BACKUP_DIR /opt/backups
cp -r . \$BACKUP_DIR/ 2>/dev/null || true
ls -td /opt/backups/ogd-* 2>/dev/null | tail -n +4 | xargs rm -rf 2>/dev/null || true
# 解压新代码
cd /tmp
tar -xzf ogd-sync.tar.gz -C $RemotePath --overwrite
rm -f ogd-sync.tar.gz
# 确保权限
chown -R ubuntu:ubuntu $RemotePath 2>/dev/null || true
echo "DEPLOY_OK"
"@
    $result = $deployScript | ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 "$ServerUser@$ServerIP" "bash -s"
    if ($result -notmatch "DEPLOY_OK") { throw "服务器部署失败: $result" }
    Write-Color "      服务器文件更新完成" Green
} finally {
    if (Test-Path $tarFile) { Remove-Item $tarFile -Force }
}

# Step 4: 重启服务
Write-Color "[4/5] 重启服务..." Yellow
$restartResult = ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 "$ServerUser@$ServerIP" "sudo systemctl restart $ServiceName && sleep 2 && systemctl is-active $ServiceName"
if ($restartResult -match "active") {
    Write-Color "      服务重启成功" Green
} else {
    Write-Color "      服务状态: $restartResult" Red
}

# Step 5: 验证
Write-Color "[5/5] 验证服务..." Yellow
Start-Sleep -Seconds 2
$verify = ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 "$ServerUser@$ServerIP" "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:5000/v3/"
if ($verify -eq "200") {
    Write-Color "      验证通过 (HTTP 200)" Green
} else {
    Write-Color "      验证失败 (HTTP $verify)" Red
}

Write-Color "" White
Write-Color "========================================" Cyan
Write-Color "  同步完成！" Green
Write-Color "  访问: http://$ServerIP/v3/" Cyan
Write-Color "========================================" Cyan
Write-Color ""
Write-Color "按任意键退出..." DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
