#!/usr/bin/env python3
"""
OGD-Collector-Pro 一键部署脚本
使用方法: python _one_click_deploy.py [可选：文件路径]
不传参数 = git push + 服务器pull
传参数 = 只上传指定文件到服务器

前置条件：
1. SSH免密已配置 (C:\\Users\\MI\\.ssh\\id_ed25519)
2. 服务器路径: /opt/ogd-collector-pro
3. Git已commit（不会自动commit！）
"""

import subprocess
import sys
import os
import time

# 配置
SSH_KEY = r"C:\Users\MI\.ssh\id_ed25519"
SERVER_IP = "106.53.188.187"
SERVER_USER = "ubuntu"
SERVER_PATH = "/opt/ogd-collector-pro"
PROJECT_PATH = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system"

GIT_SSH = r"C:\Program Files\Git\usr\bin\ssh.exe"
PYTHON = r"C:\Users\MI\AppData\Local\Programs\Python\Python315\python.exe"

def run_cmd(cmd, timeout=30):
    """执行命令并返回输出"""
    print(f"执行: {cmd[:80]}...")
    proc = subprocess.Popen(
        cmd, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        return stdout.decode('utf-8', errors='replace'), stderr.decode('utf-8', errors='replace'), proc.returncode
    except subprocess.TimeoutExpired:
        proc.kill()
        return "", "Timeout", -1

def git_push():
    """推送到GitHub"""
    print("\n=== 1. Git Push ===")
    cmd = f'"{GIT_SSH}" push origin main'
    stdout, stderr, code = run_cmd(cmd, 60)
    if code == 0 and "Everything up-to-date" not in stdout and "up to date" not in stdout.lower():
        print("✓ Git push 成功")
        return True
    elif "Everything up-to-date" in stdout or "up to date" in stdout.lower():
        print("✓ 代码已是最新（无需push）")
        return True
    else:
        print(f"✗ Git push 失败: {stderr[:200]}")
        return False

def ssh_exec(cmd):
    """在服务器执行命令"""
    full_cmd = f'"{GIT_SSH}" -o StrictHostKeyChecking=no -i "{SSH_KEY}" {SERVER_USER}@{SERVER_IP} "{cmd}"'
    proc = subprocess.Popen(
        full_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate(timeout=30)
    return stdout.decode('utf-8', errors='replace'), stderr.decode('utf-8', errors='replace'), proc.returncode

def server_pull():
    """服务器执行git pull"""
    print("\n=== 2. 服务器 Pull & 重启 ===")
    
    # git pull
    stdout, stderr, code = ssh_exec(f"cd {SERVER_PATH} && git pull origin main")
    if code == 0:
        print("✓ Git pull 成功")
    else:
        print(f"⚠ Git pull 结果: {stdout[:200]}")
        if "up to date" in stdout.lower() or "already" in stdout.lower():
            print("✓ 代码已是最新")
        else:
            print(f"⚠ Pull可能有警告: {stderr[:100]}")
    
    # 重启服务
    print("\n=== 3. 重启服务 ===")
    stdout, stderr, code = ssh_exec("sudo systemctl restart ogd-collector && sleep 2 && systemctl is-active ogd-collector")
    if "active" in stdout:
        print("✓ 服务已重启并运行中")
    else:
        print(f"⚠ 服务状态: {stdout}")
    
    return True

def upload_single_file(file_path):
    """上传单个文件到服务器（绕过Git）"""
    print(f"\n=== 上传单个文件: {file_path} ===")
    
    if not os.path.exists(file_path):
        print(f"✗ 文件不存在: {file_path}")
        return False
    
    # 确定服务器目标路径
    rel_path = os.path.relpath(file_path, PROJECT_PATH)
    server_dest = f"{SERVER_PATH}/{rel_path}".replace("\\", "/")
    
    # 读取文件内容
    with open(file_path, 'rb') as f:
        content = f.read()
    
    print(f"文件大小: {len(content)} bytes")
    print(f"目标路径: {server_dest}")
    
    # 通过SSH stdin上传
    ssh_cmd = [
        GIT_SSH,
        "-o", "StrictHostKeyChecking=no",
        "-i", SSH_KEY,
        f"{SERVER_USER}@{SERVER_IP}",
        f"cat > {server_dest} && echo 'Upload OK: $(wc -c < {server_dest}) bytes'"
    ]
    
    proc = subprocess.Popen(ssh_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(input=content)
    
    if proc.returncode == 0:
        print(f"✓ 上传成功: {stdout.strip()}")
        
        # 如果是templates文件，需要重启服务
        if 'templates' in server_dest:
            print("\n=== 重启服务 ===")
            ssh_exec("sudo systemctl restart ogd-collector && sleep 1")
            print("✓ 服务已重启")
        return True
    else:
        print(f"✗ 上传失败: {stderr}")
        return False

def main():
    print("=" * 50)
    print("OGD-Collector-Pro 一键部署")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # 单文件模式
        file_path = sys.argv[1]
        if not os.path.isabs(file_path):
            file_path = os.path.join(PROJECT_PATH, file_path)
        upload_single_file(file_path)
    else:
        # 完整部署模式
        git_push()
        server_pull()
    
    print("\n" + "=" * 50)
    print("部署完成!")
    print(f"访问: http://{SERVER_IP}")
    print("=" * 50)

if __name__ == "__main__":
    main()
