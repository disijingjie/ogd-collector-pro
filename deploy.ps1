# OGD-Collector Pro 一键部署脚本 (纯 PowerShell)
# 包含 Git 操作和 SFTP 上传

$ErrorActionPreference = "Stop"

# ========== 配置 ==========
$git = "C:\Program Files\Git\bin\git.exe"
$projectDir = "C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system"
$keyPath = "C:\Users\MI\.ssh\id_ed25519"

$host_ip = "106.53.188.187"
$username = "ubuntu"
$serviceName = "ogd-collector"

# 要上传的文件
$filesToUpload = @(
    @{ Local = "$projectDir\templates\v3_thesis.html"; Remote = "/opt/ogd-collector-pro/templates/v3_thesis.html" },
    @{ Local = "$projectDir\templates\v3_research.html"; Remote = "/opt/ogd-collector-pro/templates/v3_research.html" },
    @{ Local = "$projectDir\templates\v3_collection.html"; Remote = "/opt/ogd-collector-pro/templates/v3_collection.html" },
    @{ Local = "$projectDir\templates\v3_literature.html"; Remote = "/opt/ogd-collector-pro/templates/v3_literature.html" },
    @{ Local = "$projectDir\templates\v3_papers.html"; Remote = "/opt/ogd-collector-pro/templates/v3_papers.html" },
    @{ Local = "$projectDir\templates\v3_chen_chuanfu.html"; Remote = "/opt/ogd-collector-pro/templates/v3_chen_chuanfu.html" },
    @{ Local = "$projectDir\v3_app.py"; Remote = "/opt/ogd-collector-pro/v3_app.py" }
)

# ========== 函数 ==========

function Invoke-GitCommand {
    param([string[]]$Args)
    
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $git
    $psi.Arguments = $Args -join " "
    $psi.WorkingDirectory = $projectDir
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    
    $proc = [System.Diagnostics.Process]::Start($psi)
    $stdout = $proc.StandardOutput.ReadToEnd()
    $stderr = $proc.StandardError.ReadToEnd()
    $proc.WaitForExit()
    
    return @{
        ExitCode = $proc.ExitCode
        Stdout = $stdout
        Stderr = $stderr
    }
}

function Write-Step {
    param([string]$Text, [string]$Color = "White")
    Write-Host ("  " + $Text) -ForegroundColor $Color
}

function Connect-SSH {
    try {
        Add-Type -Path "$env:USERPROFILE\.pip\paramiko\paramiko.py" -ErrorAction SilentlyContinue
    } catch { }
    
    $assemblyPath = [System.Reflection.Assembly]::LoadWithPartialName("System.Management.Automation").Location
    $dllDir = Split-Path $assemblyPath -Parent
    
    # 使用 Python 执行 SFTP
    $pythonCmd = @"
import paramiko
import os

host = '$host_ip'
username = '$username'
key_path = r'$keyPath'

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.Ed25519Key.from_private_key_file(key_path)
    ssh.connect(host, username=username, pkey=key, timeout=30)
    print("SSH_CONNECT_OK")
    ssh.close()
except Exception as e:
    print(f"SSH_CONNECT_ERROR: {e}")
"@
    
    $result = python -c $pythonCmd 2>&1
    if ($result -match "SSH_CONNECT_OK") {
        return $true
    } else {
        Write-Host "SSH 连接失败: $result" -ForegroundColor Red
        return $false
    }
}

function Upload-File {
    param($localPath, $remotePath)
    
    $uploadCmd = @"
import paramiko
import os

host = '$host_ip'
username = '$username'
key_path = r'$keyPath'

local = r'$localPath'
remote = '$remotePath'

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.Ed25519Key.from_private_key_file(key_path)
    ssh.connect(host, username=username, pkey=key, timeout=30)
    
    sftp = ssh.open_sftp()
    
    # 创建目录
    remote_dir = os.path.dirname(remote)
    try:
        sftp.stat(remote_dir)
    except:
        try:
            sftp.mkdir(remote_dir)
        except:
            pass
    
    # 上传
    sftp.put(local, remote)
    sftp.close()
    ssh.close()
    print("UPLOAD_OK")
except Exception as e:
    print(f"UPLOAD_ERROR: {e}")
"@
    
    $result = python -c $uploadCmd 2>&1
    if ($result -match "UPLOAD_OK") {
        return $true
    } else {
        return $false
    }
}

function Restart-Service {
    $cmd = @"
import paramiko

host = '$host_ip'
username = '$username'
key_path = r'$keyPath'
service = '$serviceName'

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.Ed25519Key.from_private_key_file(key_path)
    ssh.connect(host, username=username, pkey=key, timeout=30)
    
    stdin, stdout, stderr = ssh.exec_command(f'sudo systemctl restart {service}')
    exit_code = stdout.channel.recv_exit_status()
    
    ssh.close()
    
    if exit_code == 0:
        print("RESTART_OK")
    else:
        print(f"RESTART_ERROR: exit {exit_code}")
except Exception as e:
    print(f"RESTART_ERROR: {e}")
"@
    
    $result = python -c $cmd 2>&1
    if ($result -match "RESTART_OK") {
        return $true
    } else {
        return $false
    }
}

function Verify-Deployment {
    $cmd = @"
import paramiko

host = '$host_ip'
username = '$username'
key_path = r'$keyPath'

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.Ed25519Key.from_private_key_file(key_path)
    ssh.connect(host, username=username, pkey=key, timeout=30)
    
    # 首页
    stdin, stdout, stderr = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/')
    home = stdout.read().strip()
    
    # 论文页
    stdin, stdout, stderr = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5001/v3/thesis')
    thesis = stdout.read().strip()
    
    ssh.close()
    
    print(f"HOME:{home}|THESIS:{thesis}")
except Exception as e:
    print(f"VERIFY_ERROR: {e}")
"@
    
    $result = python -c $cmd 2>&1
    return $result
}

# ========== 主程序 ==========

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "OGD-Collector Pro 一键部署" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Git 状态
Write-Host "[1/4] 检查 Git 状态..." -ForegroundColor Yellow
$result = Invoke-GitCommand -Args @("status", "--short")
if ($result.Stdout) {
    Write-Host "发现变更文件:"
    $result.Stdout -split "`n" | ForEach-Object {
        Write-Host "  $_" -ForegroundColor Gray
    }
} else {
    Write-Host "  没有变更文件" -ForegroundColor Gray
}

# Step 2: Git Add 和 Commit
Write-Host ""
Write-Host "[2/4] Git Commit..." -ForegroundColor Yellow
Invoke-GitCommand -Args @("add", ".") | Out-Null

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
$result = Invoke-GitCommand -Args @("commit", "-m", "自动更新 $timestamp")

if ($result.ExitCode -eq 0) {
    Write-Host "  Commit 成功 ✓" -ForegroundColor Green
    if ($result.Stdout -match "files? changed") {
        Write-Host "  $($result.Stdout)" -ForegroundColor Gray
    }
} else {
    Write-Host "  Commit 失败" -ForegroundColor Red
    if ($result.Stderr) {
        Write-Host "  $($result.Stderr)" -ForegroundColor Red
    }
}

# Step 3: Git Push
Write-Host ""
Write-Host "[3/4] Git Push (最多重试3次)..." -ForegroundColor Yellow
$pushSuccess = $false

for ($i = 1; $i -le 3; $i++) {
    Write-Host "  尝试 $i/3..." -NoNewline
    $result = Invoke-GitCommand -Args @("push", "origin", "main")
    
    if ($result.ExitCode -eq 0) {
        Write-Host " 成功 ✓" -ForegroundColor Green
        $pushSuccess = $true
        break
    } else {
        Write-Host " 失败" -ForegroundColor Red
        if ($i -lt 3) {
            Write-Host "    等待 3 秒后重试..." -ForegroundColor Gray
            Start-Sleep -Seconds 3
        }
    }
}

if (-not $pushSuccess) {
    Write-Host "  Git Push 失败，将使用 SFTP 上传" -ForegroundColor DarkYellow
}

# Step 4: SFTP 上传
Write-Host ""
Write-Host "[4/4] SFTP 上传到服务器..." -ForegroundColor Yellow

# 检查 paramiko
$checkParamiko = python -c "import paramiko; print('OK')" 2>&1
if ($checkParamiko -notmatch "OK") {
    Write-Host "  安装 paramiko..." -ForegroundColor Gray
    pip install paramiko --quiet
}

# 上传文件
$uploadSuccess = 0
foreach ($file in $filesToUpload) {
    if (Test-Path $file.Local) {
        Write-Host "  上传: $([System.IO.Path]::GetFileName($file.Local))..." -NoNewline
        if (Upload-File -localPath $file.Local -remotePath $file.Remote) {
            Write-Host " ✓" -ForegroundColor Green
            $uploadSuccess++
        } else {
            Write-Host " ✗" -ForegroundColor Red
        }
    } else {
        Write-Host "  跳过: $([System.IO.Path]::GetFileName($file.Local)) (不存在)" -ForegroundColor DarkGray
    }
}

# 重启服务
Write-Host ""
Write-Host "  重启服务..." -NoNewline
if (Restart-Service) {
    Write-Host " ✓" -ForegroundColor Green
} else {
    Write-Host " ✗" -ForegroundColor Red
}

# 验证
Start-Sleep -Seconds 3
Write-Host ""
Write-Host "  验证部署..." -ForegroundColor Gray
$verifyResult = Verify-Deployment

if ($verifyResult -match "HOME:(\d+)") {
    $homeCode = $Matches[1]
    if ($homeCode -eq "200") {
        Write-Host "    首页: $homeCode ✓" -ForegroundColor Green
    } else {
        Write-Host "    首页: $homeCode" -ForegroundColor Yellow
    }
}

if ($verifyResult -match "THESIS:(\d+)") {
    $thesisCode = $Matches[1]
    if ($thesisCode -eq "200") {
        Write-Host "    论文页: $thesisCode ✓" -ForegroundColor Green
    } else {
        Write-Host "    论文页: $thesisCode" -ForegroundColor Yellow
    }
}

# 完成
Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "部署完成！" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "访问地址: http://$host_ip/v3/thesis" -ForegroundColor Cyan
Write-Host "密码: 123" -ForegroundColor Cyan
Write-Host ""
