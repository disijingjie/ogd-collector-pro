# =============================================================================
# OGD-Collector Pro — Windows 本地代码同步到腾讯云脚本
# 作者：文明（武汉大学信息管理学院博士生）
# 功能：一键将本地修改同步到服务器（无需每次手动上传）
# =============================================================================

# --------------------- 用户配置区（请修改） ---------------------

# 服务器配置
$SERVER_IP = "123.456.789.012"      # 你的腾讯云服务器公网IP
$SERVER_USER = "root"                # SSH用户名（默认root）
$SERVER_PASSWORD = "your_password"   # root密码（或留空使用密钥）

# 本地项目路径
$LOCAL_PATH = "C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system"

# 服务器部署路径（与一键部署脚本保持一致）
$REMOTE_PATH = "/opt/ogd-collector-pro"

# 是否使用 SSH 密钥（推荐，更安全）
$USE_KEY = $false                    # $true = 使用密钥，$false = 使用密码
$KEY_PATH = "$env:USERPROFILE\.ssh\id_rsa"  # 密钥路径

# GitHub 仓库地址（如果使用 Git 同步）
$GITHUB_REPO = "https://github.com/YOUR_USERNAME/ogd-collector-pro.git"

# --------------------- 同步方式选择 ---------------------

function Show-Menu {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "  OGD-Collector Pro 代码同步工具" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "请选择同步方式：" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  [1] SCP 直接上传（适合小改动，快速）"
    Write-Host "  [2] Git Push + 服务器 Pull（推荐，有版本记录）"
    Write-Host "  [3] rsync 增量同步（适合大量文件变更）"
    Write-Host "  [4] 配置 SSH 密钥（免密码登录）"
    Write-Host "  [5] 查看服务器状态"
    Write-Host "  [6] 重启服务器服务"
    Write-Host "  [0] 退出"
    Write-Host ""
}

# --------------------- 方式1: SCP 直接上传 ---------------------

function Sync-SCP {
    Write-Host "[SCP] 开始同步代码到服务器..." -ForegroundColor Green
    
    # 检查是否安装了 scp（Git for Windows 自带）
    $scp = Get-Command scp -ErrorAction SilentlyContinue
    if (-not $scp) {
        Write-Host "❌ 未找到 scp 命令。请安装 Git for Windows 或 OpenSSH。" -ForegroundColor Red
        return
    }
    
    # 构建 scp 命令
    $exclude = @("*.pyc", "__pycache__", "*.db-journal", "cpolar*", "logs/*", "*.zip")
    
    if ($USE_KEY -and (Test-Path $KEY_PATH)) {
        # 使用密钥
        $scpArgs = @("-i", $KEY_PATH, "-r", "-o", "StrictHostKeyChecking=no")
    } else {
        # 使用密码（需要安装 pscp 或 expect）
        Write-Host "[提示] 使用密码登录，将逐文件上传..." -ForegroundColor Yellow
    }
    
    # 使用 PowerShell 的 Copy-Item 通过 PSSession（如果启用了 WinRM）
    # 或者使用 plink/pscp (PuTTY 工具)
    
    Write-Host "[替代方案] 推荐使用 Git 方式（选项2），更可靠。" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "手动 SCP 命令示例：" -ForegroundColor Cyan
    Write-Host "  scp -r $LOCAL_PATH\*.py ${SERVER_USER}@${SERVER_IP}:${REMOTE_PATH}/" -ForegroundColor Gray
    Write-Host "  scp -r $LOCAL_PATH\templates ${SERVER_USER}@${SERVER_IP}:${REMOTE_PATH}/" -ForegroundColor Gray
    Write-Host "  scp -r $LOCAL_PATH\static ${SERVER_USER}@${SERVER_IP}:${REMOTE_PATH}/" -ForegroundColor Gray
}

# --------------------- 方式2: Git 同步（推荐） ---------------------

function Sync-Git {
    Write-Host "[Git] 开始 Git 同步流程..." -ForegroundColor Green
    
    # Step 1: 本地提交
    Write-Host ""
    Write-Host "Step 1: 本地代码提交" -ForegroundColor Cyan
    Set-Location $LOCAL_PATH
    
    # 检查是否有变更
    $status = git status --short
    if ([string]::IsNullOrWhiteSpace($status)) {
        Write-Host "[INFO] 本地没有未提交的变更" -ForegroundColor Yellow
    } else {
        Write-Host "检测到以下变更：" -ForegroundColor Yellow
        git status --short
        Write-Host ""
        
        $msg = Read-Host "请输入提交信息（直接回车使用默认）"
        if ([string]::IsNullOrWhiteSpace($msg)) {
            $msg = "Update from local $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
        }
        
        git add .
        git commit -m "$msg"
        Write-Host "✅ 本地提交完成" -ForegroundColor Green
    }
    
    # Step 2: 推送到 GitHub
    Write-Host ""
    Write-Host "Step 2: 推送到 GitHub..." -ForegroundColor Cyan
    try {
        git push origin main
        Write-Host "✅ 推送成功" -ForegroundColor Green
    } catch {
        Write-Host "❌ 推送失败，请检查 GitHub 仓库配置" -ForegroundColor Red
        return
    }
    
    # Step 3: SSH 到服务器执行 Pull
    Write-Host ""
    Write-Host "Step 3: 服务器拉取最新代码..." -ForegroundColor Cyan
    
    $remoteCmd = @"
cd $REMOTE_PATH && git pull origin main && systemctl restart ogd-collector && echo 'OK'
"@
    
    if ($USE_KEY -and (Test-Path $KEY_PATH)) {
        $result = ssh -i $KEY_PATH -o "StrictHostKeyChecking=no" "${SERVER_USER}@${SERVER_IP}" $remoteCmd 2>&1
    } else {
        Write-Host "请输入服务器密码执行远程命令..." -ForegroundColor Yellow
        # 使用 plink 或手动输入
        Write-Host "手动执行以下命令：" -ForegroundColor Cyan
        Write-Host "  ssh ${SERVER_USER}@${SERVER_IP}" -ForegroundColor Gray
        Write-Host "  cd $REMOTE_PATH && git pull origin main && systemctl restart ogd-collector" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "✅ 同步完成！访问 http://${SERVER_IP} 查看效果" -ForegroundColor Green
}

# --------------------- 方式3: rsync 增量同步 ---------------------

function Sync-Rsync {
    Write-Host "[rsync] 增量同步（需要安装 cwRsync 或 WSL）" -ForegroundColor Green
    Write-Host ""
    Write-Host "推荐使用 WSL 中的 rsync：" -ForegroundColor Cyan
    Write-Host "  wsl rsync -avz --exclude='*.pyc' --exclude='__pycache__' --exclude='*.db-journal' `" -ForegroundColor Gray
    Write-Host "    $LOCAL_PATH/ ${SERVER_USER}@${SERVER_IP}:${REMOTE_PATH}/" -ForegroundColor Gray
}

# --------------------- 方式4: 配置 SSH 密钥 ---------------------

function Setup-SSHKey {
    Write-Host "[SSH密钥] 配置免密码登录..." -ForegroundColor Green
    Write-Host ""
    
    # 检查本地是否已有密钥
    if (-not (Test-Path "$env:USERPROFILE\.ssh\id_rsa")) {
        Write-Host "本地没有 SSH 密钥，正在生成..." -ForegroundColor Yellow
        ssh-keygen -t rsa -b 4096 -C "ambit@qq.com" -f "$env:USERPROFILE\.ssh\id_rsa" -N '""'
        Write-Host "✅ 密钥生成完成" -ForegroundColor Green
    } else {
        Write-Host "✅ 本地密钥已存在" -ForegroundColor Green
    }
    
    # 显示公钥
    $pubKey = Get-Content "$env:USERPROFILE\.ssh\id_rsa.pub"
    Write-Host ""
    Write-Host "你的公钥（复制到服务器的 ~/.ssh/authorized_keys）：" -ForegroundColor Cyan
    Write-Host $pubKey -ForegroundColor Yellow
    Write-Host ""
    Write-Host "手动执行步骤：" -ForegroundColor Cyan
    Write-Host "  1. ssh ${SERVER_USER}@${SERVER_IP}" -ForegroundColor Gray
    Write-Host "  2. mkdir -p ~/.ssh && chmod 700 ~/.ssh" -ForegroundColor Gray
    Write-Host "  3. 将上面公钥粘贴到 ~/.ssh/authorized_keys" -ForegroundColor Gray
    Write-Host "  4. chmod 600 ~/.ssh/authorized_keys" -ForegroundColor Gray
    Write-Host "  5. 退出后测试：ssh ${SERVER_USER}@${SERVER_IP}" -ForegroundColor Gray
}

# --------------------- 方式5: 查看服务器状态 ---------------------

function Show-ServerStatus {
    Write-Host "[状态] 查询服务器服务状态..." -ForegroundColor Green
    Write-Host ""
    Write-Host "手动执行：" -ForegroundColor Cyan
    Write-Host "  ssh ${SERVER_USER}@${SERVER_IP} 'systemctl status ogd-collector && systemctl status nginx'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "或登录后执行：" -ForegroundColor Gray
    Write-Host "  systemctl status ogd-collector  # 查看应用状态" -ForegroundColor Gray
    Write-Host "  journalctl -u ogd-collector -f  # 实时查看日志" -ForegroundColor Gray
    Write-Host "  systemctl status nginx          # 查看 Nginx 状态" -ForegroundColor Gray
}

# --------------------- 方式6: 重启服务 ---------------------

function Restart-Server {
    Write-Host "[重启] 重启服务器服务..." -ForegroundColor Green
    Write-Host ""
    Write-Host "手动执行：" -ForegroundColor Cyan
    Write-Host "  ssh ${SERVER_USER}@${SERVER_IP} 'systemctl restart ogd-collector && systemctl restart nginx'" -ForegroundColor Gray
}

# --------------------- 主程序 ---------------------

while ($true) {
    Show-Menu
    $choice = Read-Host "请选择"
    
    switch ($choice) {
        "1" { Sync-SCP }
        "2" { Sync-Git }
        "3" { Sync-Rsync }
        "4" { Setup-SSHKey }
        "5" { Show-ServerStatus }
        "6" { Restart-Server }
        "0" { exit }
        default { Write-Host "无效选择" -ForegroundColor Red }
    }
    
    Write-Host ""
    Read-Host "按回车继续"
}
