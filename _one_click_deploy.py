#!/usr/bin/env python3
"""
OGD-Collector-Pro V6 一键部署脚本（增强版）
用法:
  python _one_click_deploy.py              # 完整部署：git push + 服务器pull + 校验
  python _one_click_deploy.py file.html    # 上传单个文件
  python _one_click_deploy.py --check      # 只做部署后校验
  python _one_click_deploy.py --all        # 上传全部V6模板+app+data+校验

前置条件：
1. SSH免密已配置 (C:\\Users\\MI\\.ssh\\id_ed25519)
2. 服务器路径: /opt/ogd-collector-pro
3. Git已commit（不会自动commit！）
"""

import subprocess
import sys
import os
import time
import json
from datetime import datetime

# 配置
SSH_KEY = r"C:\Users\MI\.ssh\id_ed25519"
SERVER_IP = "106.53.188.187"
SERVER_USER = "ubuntu"
SERVER_PATH = "/opt/ogd-collector-pro"
PROJECT_PATH = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system"

GIT_SSH = r"C:\Program Files\Git\usr\bin\ssh.exe"
PYTHON = r"C:\Users\MI\AppData\Local\Programs\Python\Python315\python.exe"

# 部署日志
DEPLOY_LOG = os.path.join(PROJECT_PATH, "deploy_log.txt")

# V6关键文件清单
V6_KEY_FILES = [
    "v6_app.py",
    "v3_platform_rules.json",
    "data/v3_collection_results.json",
    "data/data_thesis_interlock.json",
]

def log(msg):
    """记录部署日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    try:
        with open(DEPLOY_LOG, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except:
        pass

def run_cmd(cmd, timeout=30):
    """执行命令并返回输出"""
    log(f"执行: {cmd[:80]}...")
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

def ssh_exec(cmd):
    """在服务器执行命令"""
    full_cmd = [GIT_SSH, "-o", "StrictHostKeyChecking=no", "-i", SSH_KEY,
                f"{SERVER_USER}@{SERVER_IP}", cmd]
    proc = subprocess.Popen(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(timeout=30)
    return stdout.decode('utf-8', errors='replace'), stderr.decode('utf-8', errors='replace'), proc.returncode

def upload_file(local_path, server_path=None):
    """上传单个文件到服务器"""
    if not os.path.exists(local_path):
        log(f"✗ 文件不存在: {local_path}")
        return False

    if server_path is None:
        rel_path = os.path.relpath(local_path, PROJECT_PATH)
        server_path = f"{SERVER_PATH}/{rel_path}".replace("\\", "/")

    with open(local_path, 'rb') as f:
        content = f.read()

    log(f"上传: {os.path.basename(local_path)} ({len(content)} bytes) → {server_path}")

    ssh_cmd = [GIT_SSH, "-o", "StrictHostKeyChecking=no", "-i", SSH_KEY,
               f"{SERVER_USER}@{SERVER_IP}",
               f"cat > {server_path} && echo 'OK: $(wc -c < {server_path}) bytes'"]

    proc = subprocess.Popen(ssh_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(input=content)

    if proc.returncode == 0:
        log(f"✓ 上传成功: {stdout.strip()}")
        return True
    else:
        log(f"✗ 上传失败: {stderr.decode('utf-8', errors='replace')[:200]}")
        return False

def git_push():
    """推送到GitHub"""
    log("\n=== 1. Git Push ===")
    cmd = f'cd /d "{PROJECT_PATH}" && "{GIT_SSH}" push origin main'
    stdout, stderr, code = run_cmd(cmd, 60)
    if code == 0:
        log("✓ Git push 成功")
        return True
    elif "up to date" in stdout.lower() or "Everything up-to-date" in stdout:
        log("✓ 代码已是最新")
        return True
    else:
        log(f"⚠ Git push 结果: {stderr[:200]}")
        return True  # 继续部署

def server_pull_and_restart():
    """服务器pull + 重启"""
    log("\n=== 2. 服务器 Pull & 重启 ===")

    stdout, stderr, code = ssh_exec(f"cd {SERVER_PATH} && git pull origin main 2>&1")
    if "up to date" in stdout.lower() or "Already up" in stdout:
        log("✓ 服务器代码已是最新")
    elif code == 0:
        log("✓ Git pull 成功")
    else:
        log(f"⚠ Pull结果: {stdout[:200]}")

    log("\n=== 3. 重启服务 ===")
    stdout, stderr, code = ssh_exec("sudo systemctl restart ogd-collector && sleep 3 && sudo systemctl is-active ogd-collector")
    if "active" in stdout:
        log("✓ 服务已重启并运行中")
        return True
    else:
        log(f"⚠ 服务状态: {stdout}")
        return False

def deploy_check():
    """部署后校验"""
    log("\n=== 4. 部署后校验 ===")
    errors = []

    # 检查关键页面HTTP状态
    pages = ['/', '/caliber', '/map', '/collection', '/analysis', '/thesis', '/literature',
             '/api/collection/status', '/api/collection/health', '/api/interlock/check', '/api/literature/dedup']

    for page in pages:
        stdout, stderr, code = ssh_exec(f"curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:5000{page}")
        status = stdout.strip().replace('\\n', '').replace(':', '')
        if '200' in status:
            log(f"✓ {page}: 200")
        else:
            log(f"✗ {page}: {status}")
            errors.append(page)

    # 检查模板数量
    stdout, _, _ = ssh_exec(f"ls {SERVER_PATH}/templates/v6_*.html | wc -l")
    template_count = stdout.strip()
    local_count = len([f for f in os.listdir(os.path.join(PROJECT_PATH, 'templates')) if f.startswith('v6_') and f.endswith('.html')])
    if template_count == str(local_count):
        log(f"✓ 模板数一致: {local_count}")
    else:
        log(f"⚠ 模板数不一致: 本地{local_count} vs 服务器{template_count}")
        errors.append('template_count')

    # 检查数据文件
    for data_file in ['data/v3_collection_results.json', 'data/data_thesis_interlock.json']:
        stdout, _, code = ssh_exec(f"test -f {SERVER_PATH}/{data_file} && echo 'exists' || echo 'missing'")
        if 'exists' in stdout:
            log(f"✓ {data_file}: 存在")
        else:
            log(f"✗ {data_file}: 缺失")
            errors.append(data_file)

    if errors:
        log(f"\n⚠ 校验发现 {len(errors)} 个问题: {errors}")
        return False
    else:
        log("\n✓ 全部校验通过！")
        return True

def upload_all_v6():
    """上传全部V6文件"""
    log("\n=== 上传全部V6文件 ===")

    # 1. 上传所有v6模板
    templates_dir = os.path.join(PROJECT_PATH, 'templates')
    v6_templates = [f for f in os.listdir(templates_dir) if f.startswith('v6_') and f.endswith('.html')]
    log(f"发现 {len(v6_templates)} 个V6模板")

    for t in v6_templates:
        local = os.path.join(templates_dir, t)
        server = f"{SERVER_PATH}/templates/{t}"
        upload_file(local, server)

    # 2. 上传v6_app.py
    upload_file(os.path.join(PROJECT_PATH, 'v6_app.py'), f"{SERVER_PATH}/v6_app.py")

    # 3. 上传关键数据文件
    for df in V6_KEY_FILES:
        local = os.path.join(PROJECT_PATH, df)
        if os.path.exists(local):
            server = f"{SERVER_PATH}/{df}"
            upload_file(local, server)

    # 4. 重启
    log("\n=== 重启服务 ===")
    stdout, stderr, code = ssh_exec("sudo systemctl restart ogd-collector && sleep 3 && sudo systemctl is-active ogd-collector")
    if "active" in stdout:
        log("✓ 服务已重启并运行中")
    else:
        log(f"⚠ 服务状态: {stdout}")

def main():
    print("=" * 60)
    print("OGD-Collector-Pro V6 一键部署（增强版）")
    print("=" * 60)

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == '--check':
            deploy_check()
        elif arg == '--all':
            upload_all_v6()
            deploy_check()
        else:
            # 单文件上传
            file_path = arg
            if not os.path.isabs(file_path):
                file_path = os.path.join(PROJECT_PATH, file_path)
            upload_file(file_path)
            # 自动重启
            ssh_exec("sudo systemctl restart ogd-collector && sleep 1")
            log("✓ 服务已重启")
    else:
        # 完整部署
        git_push()
        server_pull_and_restart()
        deploy_check()

    print(f"\n访问: http://{SERVER_IP}")

if __name__ == "__main__":
    main()
