#!/usr/bin/env python3
"""
OGD-Collector Pro Paramiko 部署脚本
解决 PowerShell SSH 命令卡住问题
"""
import os
import sys
from pathlib import Path

import paramiko

SERVER_IP = "106.53.188.187"
SERVER_USER = "root"
SERVER_PATH = "/opt/ogd-collector-pro"
KEY_PATH = Path.home() / ".ssh" / "id_ed25519"

FILES_TO_DEPLOY = [
    ("app.py", f"{SERVER_PATH}/app.py"),
    ("models.py", f"{SERVER_PATH}/models.py"),
    ("templates/collector.html", f"{SERVER_PATH}/templates/collector.html"),
    ("templates/dashboard.html", f"{SERVER_PATH}/templates/dashboard.html"),
]


def main():
    project_root = Path(__file__).parent

    print("=" * 50)
    print("OGD-Collector Pro Paramiko 部署")
    print("=" * 50)

    if not KEY_PATH.exists():
        print(f"[ERROR] 密钥文件不存在: {KEY_PATH}")
        sys.exit(1)

    # 加载私钥
    try:
        private_key = paramiko.Ed25519Key.from_private_key_file(str(KEY_PATH))
        print(f"[OK] 已加载密钥: {KEY_PATH.name}")
    except paramiko.ssh_exception.PasswordRequiredException:
        print("[ERROR] 密钥需要密码，请在本地终端手动执行部署")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 加载密钥失败: {e}")
        sys.exit(1)

    # 连接服务器
    print(f"[INFO] 连接服务器 {SERVER_IP} ...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=SERVER_IP,
            username=SERVER_USER,
            pkey=private_key,
            timeout=15,
            banner_timeout=15,
            auth_timeout=15,
        )
        print("[OK] SSH 连接成功")
    except Exception as e:
        print(f"[ERROR] SSH 连接失败: {e}")
        sys.exit(1)

    # 上传文件
    sftp = client.open_sftp()
    for local_rel, remote_path in FILES_TO_DEPLOY:
        local_path = project_root / local_rel
        if not local_path.exists():
            print(f"[WARN] 本地文件不存在，跳过: {local_path}")
            continue
        print(f"[INFO] 上传 {local_rel} -> {remote_path}")
        try:
            sftp.put(str(local_path), remote_path)
            print(f"[OK]   上传成功")
        except Exception as e:
            print(f"[ERROR] 上传失败: {e}")
    sftp.close()

    # 重启服务
    print("[INFO] 重启服务 ogd-collector ...")
    stdin, stdout, stderr = client.exec_command(
        "sudo systemctl restart ogd-collector && sleep 2 && sudo systemctl is-active ogd-collector"
    )
    status = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if status == "active":
        print("[OK] 服务重启成功，运行状态: active")
    else:
        print(f"[WARN] 服务状态: {status}")
        if err:
            print(f"[WARN] stderr: {err}")

    # 获取服务状态详情
    stdin, stdout, stderr = client.exec_command(
        "sudo systemctl status ogd-collector --no-pager | head -n 6"
    )
    print("\n[服务状态摘要]")
    for line in stdout.read().decode().strip().split("\n"):
        print("  ", line)

    client.close()
    print("\n" + "=" * 50)
    print("部署完成！访问: http://106.53.188.187/collector")
    print("=" * 50)


if __name__ == "__main__":
    main()
