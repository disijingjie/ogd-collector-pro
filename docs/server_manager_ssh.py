#!/usr/bin/env python3
"""
服务器管理脚本 (SSH方式)
通过本地SSH密钥直接管理服务器，无需打开腾讯云终端
"""

import subprocess
import sys

SERVER_IP = "106.53.188.187"
SERVER_USER = "root"
APP_DIR = "/opt/ogd-collector-pro"


def ssh_run(command, timeout=60):
    """通过SSH在服务器上执行命令"""
    ssh_cmd = [
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "ConnectTimeout=10",
        f"{SERVER_USER}@{SERVER_IP}",
        command
    ]
    print(f"执行: ssh {SERVER_USER}@{SERVER_IP} '{command[:80]}...'")
    result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=timeout, encoding='utf-8', errors='replace')
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr, file=sys.stderr)
    return result.returncode == 0


def status():
    """查看服务器状态"""
    print("=" * 50)
    print("服务器系统状态")
    print("=" * 50)
    ssh_run("uptime && free -h && df -h /")


def check_app():
    """检查OGD应用状态"""
    print("=" * 50)
    print("OGD-Collector Pro 运行状态")
    print("=" * 50)
    ssh_run(f"systemctl status ogd-collector --no-pager && echo '---本地测试---' && curl -s http://127.0.0.1:5000 | head -10")


def update_app():
    """更新OGD应用"""
    print("=" * 50)
    print("更新 OGD-Collector Pro")
    print("=" * 50)
    success = ssh_run(f"cd {APP_DIR} && git pull origin main && systemctl restart ogd-collector && echo '更新成功'")
    if success:
        print("\n✅ 更新完成，访问: http://106.53.188.187")
    else:
        print("\n❌ 更新失败")
    return success


def restart_app():
    """重启OGD应用"""
    print("=" * 50)
    print("重启 OGD-Collector Pro")
    print("=" * 50)
    ssh_run(f"systemctl restart ogd-collector && systemctl status ogd-collector --no-pager")


def restart_nginx():
    """重启Nginx"""
    print("=" * 50)
    print("重启 Nginx")
    print("=" * 50)
    ssh_run("systemctl restart nginx && systemctl status nginx --no-pager")


def view_logs(lines=50):
    """查看应用日志"""
    print("=" * 50)
    print(f"OGD应用日志 (最近{lines}行)")
    print("=" * 50)
    ssh_run(f"journalctl -u ogd-collector --no-pager -n {lines}")


def push_local():
    """本地推送代码到GitHub并更新服务器"""
    import os
    local_dir = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system"
    print("=" * 50)
    print("本地推送 + 服务器更新")
    print("=" * 50)

    # 1. 本地git推送
    print("\n[1/3] 本地推送代码到GitHub...")
    result = subprocess.run(
        ["git", "add", "."],
        cwd=local_dir, capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    result = subprocess.run(
        ["git", "commit", "-m", "auto update"],
        cwd=local_dir, capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        print("提交信息:", result.stderr.strip() if result.stderr else "无变更或已提交")
    result = subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=local_dir, capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    print(result.stdout if result.stdout else "推送完成")
    if result.stderr:
        print(result.stderr)

    # 2. 服务器拉取更新
    print("\n[2/3] 服务器拉取更新...")
    success = ssh_run(f"cd {APP_DIR} && git pull origin main")

    # 3. 重启服务
    print("\n[3/3] 重启服务...")
    ssh_run("systemctl restart ogd-collector")

    print("\n✅ 全部完成！访问: http://106.53.188.187")


def show_help():
    print("""
服务器管理脚本 (SSH方式)
========================

用法: python server_manager_ssh.py [命令]

命令列表:
  status      查看服务器系统状态 (uptime, 内存, 磁盘)
  check       检查OGD应用运行状态
  update      服务器端拉取GitHub最新代码并重启
  restart     重启OGD应用服务
  restart-nginx  重启Nginx
  logs [N]    查看应用日志，默认50行
  push        本地推送代码到GitHub + 服务器更新 (一键全流程)
  run "命令"   在服务器上执行任意命令

示例:
  python server_manager_ssh.py status
  python server_manager_ssh.py push          ← 最常用，一键发布
  python server_manager_ssh.py logs 100
  python server_manager_ssh.py run "ls -la /opt/ogd-collector-pro"
    """)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    try:
        if cmd == "status":
            status()
        elif cmd == "check":
            check_app()
        elif cmd == "update":
            update_app()
        elif cmd == "restart":
            restart_app()
        elif cmd == "restart-nginx":
            restart_nginx()
        elif cmd == "logs":
            lines = int(sys.argv[2]) if len(sys.argv) > 2 else 50
            view_logs(lines)
        elif cmd == "push":
            push_local()
        elif cmd == "run":
            if len(sys.argv) < 3:
                print("请提供命令")
                sys.exit(1)
            ssh_run(sys.argv[2])
        else:
            print(f"未知命令: {cmd}")
            show_help()
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
