#!/usr/bin/env python3
"""直接通过SSH/SCP部署文件到服务器（绕过GitHub）"""
import subprocess
import sys
from pathlib import Path

SERVER = "ubuntu@106.53.188.187"
APP_DIR = "/opt/ogd-collector-pro"
ROOT_PW = "Wenming.890328"

files_to_deploy = [
    ("../app.py", f"{APP_DIR}/app.py"),
    ("../models.py", f"{APP_DIR}/models.py"),
    ("../auto_collect.py", f"{APP_DIR}/auto_collect.py"),
    ("../setup_cron.sh", f"{APP_DIR}/setup_cron.sh"),
    ("../templates/login.html", f"{APP_DIR}/templates/login.html"),
    ("../templates/base.html", f"{APP_DIR}/templates/base.html"),
    ("../templates/thesis.html", f"{APP_DIR}/templates/thesis.html"),
]

def scp_file(local, remote):
    cmd = [
        "scp", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=15",
        str(local), f"{SERVER}:{remote}"
    ]
    print(f">>> SCP: {local} -> {remote}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"[ERROR] {result.stderr}")
        return False
    return True

print("=" * 60)
print("直接部署到服务器 (绕过GitHub)")
print("=" * 60)

success_count = 0
for local, remote in files_to_deploy:
    local_path = Path(__file__).parent.parent / local.replace("../", "")
    if local_path.exists():
        if scp_file(local_path, remote):
            success_count += 1
    else:
        print(f"[WARN] 本地文件不存在: {local_path}")

print(f"\n部署完成: {success_count}/{len(files_to_deploy)} 个文件")

# 重启服务
print("\n>>> 重启服务...")
restart_cmd = [
    "ssh", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=15",
    SERVER, f"echo '{ROOT_PW}' | sudo -S systemctl restart ogd-collector"
]
result = subprocess.run(restart_cmd, capture_output=True, text=True, timeout=30)
if result.returncode == 0:
    print("✅ 服务重启成功")
else:
    print(f"[WARN] 重启输出: {result.stderr}")

print("\n" + "=" * 60)
print("访问: http://106.53.188.187")
print("=" * 60)
