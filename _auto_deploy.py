#!/usr/bin/env python3
"""
自动部署脚本：将本地代码推送到GitHub并更新腾讯云服务器
"""
import subprocess
import sys
import os
from datetime import datetime

REPO_DIR = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system"
GIT_EXE = r"C:\Program Files\Git\cmd\git.exe"
SERVER_IP = "106.53.188.187"
SERVER_USER = "ubuntu"

def run_cmd(cmd, cwd=None, retries=0, retry_delay=5):
    """执行命令，支持重试"""
    for attempt in range(retries + 1):
        try:
            print(f"[执行] {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=cwd or REPO_DIR,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            print(f"  退出码: {result.returncode}")
            if result.stdout:
                print(f"  输出:\n{result.stdout}")
            if result.stderr:
                print(f"  错误:\n{result.stderr}")
            if result.returncode == 0:
                return result
            if attempt < retries:
                print(f"  重试 {attempt + 1}/{retries}...")
                import time
                time.sleep(retry_delay)
        except Exception as e:
            print(f"  异常: {e}")
            if attempt < retries:
                print(f"  重试 {attempt + 1}/{retries}...")
                import time
                time.sleep(retry_delay)
    return None

def main():
    results = {
        "git_add": None,
        "git_commit": None,
        "git_push": None,
        "ssh_update": None
    }

    # 1. git add
    print("=" * 60)
    print("步骤1: git add .")
    print("=" * 60)
    results["git_add"] = run_cmd([GIT_EXE, "add", "."])
    if not results["git_add"]:
        print("[错误] git add 失败")
        return results

    # 检查是否有变更需要提交
    print("=" * 60)
    print("检查是否有变更需要提交...")
    print("=" * 60)
    diff_result = run_cmd([GIT_EXE, "diff", "--cached", "--stat"])
    if diff_result and not diff_result.stdout.strip():
        print("[信息] 没有需要提交的变更，跳过commit和push")
        results["git_commit"] = "skipped"
        results["git_push"] = "skipped"
        results["ssh_update"] = "skipped"
        return results

    # 2. git commit
    print("=" * 60)
    print("步骤2: git commit")
    print("=" * 60)
    commit_msg = f"自动更新 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    results["git_commit"] = run_cmd([GIT_EXE, "commit", "-m", commit_msg])
    if not results["git_commit"]:
        print("[错误] git commit 失败")
        return results

    # 3. git push (重试3次)
    print("=" * 60)
    print("步骤3: git push origin main")
    print("=" * 60)
    results["git_push"] = run_cmd([GIT_EXE, "push", "origin", "main"], retries=3, retry_delay=10)
    if not results["git_push"]:
        print("[错误] git push 失败（3次重试后）")
        return results

    # 4. SSH 更新服务器
    print("=" * 60)
    print("步骤4: SSH更新服务器")
    print("=" * 60)
    ssh_cmd = (
        f"ssh {SERVER_USER}@{SERVER_IP} "
        f'"cd /opt/ogd-collector-pro && git pull origin main && sudo systemctl restart ogd-collector"'
    )
    print(f"[执行] {ssh_cmd}")
    try:
        ssh_result = subprocess.run(
            ssh_cmd,
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=True
        )
        print(f"  退出码: {ssh_result.returncode}")
        if ssh_result.stdout:
            print(f"  输出:\n{ssh_result.stdout}")
        if ssh_result.stderr:
            print(f"  错误:\n{ssh_result.stderr}")
        if ssh_result.returncode == 0:
            results["ssh_update"] = ssh_result
        else:
            print("[错误] SSH 连接/执行失败")
            results["ssh_update"] = None
    except Exception as e:
        print(f"[错误] SSH 异常: {e}")
        results["ssh_update"] = None

    return results

if __name__ == "__main__":
    results = main()
    print("\n" + "=" * 60)
    print("部署结果汇总")
    print("=" * 60)
    for step, result in results.items():
        if result == "skipped":
            status = "跳过（无变更）"
        elif result is None:
            status = "失败"
        else:
            status = "成功"
        print(f"  {step}: {status}")
    print("=" * 60)
