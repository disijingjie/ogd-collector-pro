#!/usr/bin/env python3
"""
腾讯云服务器管理脚本 - 通过 Python SDK 管理轻量服务器
无需打开腾讯云终端，直接在 WorkBuddy 中执行
"""

import json
import sys
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.lighthouse.v20200324 import lighthouse_client, models
from tencentcloud.tat.v20201028 import tat_client, models as tat_models

# ===== 配置信息 =====
import os
SECRET_ID = os.environ.get("TENCENT_SECRET_ID", "YOUR_SECRET_ID")
SECRET_KEY = os.environ.get("TENCENT_SECRET_KEY", "YOUR_SECRET_KEY")
REGION = "ap-guangzhou"
INSTANCE_ID = "lhins-kyp9be3t"


def get_client(service="lighthouse"):
    """获取腾讯云客户端"""
    cred = credential.Credential(SECRET_ID, SECRET_KEY)
    httpProfile = HttpProfile()
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile

    if service == "lighthouse":
        httpProfile.endpoint = "lighthouse.tencentcloudapi.com"
        return lighthouse_client.LighthouseClient(cred, REGION, clientProfile)
    elif service == "tat":
        httpProfile.endpoint = "tat.tencentcloudapi.com"
        return tat_client.TatClient(cred, REGION, clientProfile)
    else:
        raise ValueError(f"未知服务: {service}")


def get_instance_status():
    """获取服务器状态"""
    client = get_client("lighthouse")
    req = models.DescribeInstancesRequest()
    req.InstanceIds = [INSTANCE_ID]
    resp = client.DescribeInstances(req)

    instance = resp.InstanceSet[0]
    print("=" * 50)
    print("服务器状态")
    print("=" * 50)
    print(f"实例ID:     {instance.InstanceId}")
    print(f"名称:       {instance.InstanceName}")
    print(f"状态:       {instance.InstanceState}")
    print(f"公网IP:     {instance.PublicAddresses[0] if instance.PublicAddresses else '无'}")
    print(f"配置:       {instance.CPU}核 {instance.Memory}G")
    print(f"系统盘:     {instance.SystemDisk.DiskSize}GB {instance.SystemDisk.DiskType}")
    print(f"创建时间:   {instance.CreatedTime}")
    print(f"到期时间:   {instance.ExpiredTime}")
    print(f"最新操作:   {instance.LatestOperation} ({instance.LatestOperationState})")
    print("=" * 50)
    return instance.InstanceState


def reboot_instance():
    """重启服务器"""
    client = get_client("lighthouse")
    req = models.RebootInstancesRequest()
    req.InstanceIds = [INSTANCE_ID]
    resp = client.RebootInstances(req)
    print(f"重启请求已发送: {resp.RequestId}")
    print("等待服务器重启中...")

    # 等待重启完成
    for i in range(30):
        time.sleep(5)
        try:
            status = get_instance_status()
            if status == "RUNNING":
                print("✅ 服务器已重启完成")
                return True
        except Exception:
            print(f"  等待中... ({i+1}/30)")
    print("⚠️ 等待超时，请稍后手动检查")
    return False


def run_command(command, timeout=300):
    """
    在服务器上执行命令（通过腾讯云自动化助手 TAT）
    无需SSH，直接在服务器上执行Shell命令
    """
    client = get_client("tat")

    # 创建命令
    req = tat_models.CreateCommandRequest()
    req.CommandName = f"ogd-task-{int(time.time())}"
    req.Content = command
    req.CommandType = "SHELL"
    req.WorkingDirectory = "/root"
    req.Timeout = timeout
    resp = client.CreateCommand(req)
    command_id = resp.CommandId
    print(f"命令已创建: {command_id}")

    # 执行命令
    invoke_req = tat_models.InvokeCommandRequest()
    invoke_req.CommandId = command_id
    invoke_req.InstanceIds = [INSTANCE_ID]
    invoke_resp = client.InvokeCommand(invoke_req)
    invocation_id = invoke_resp.InvocationId
    print(f"命令已下发: {invocation_id}")

    # 等待执行结果
    print("等待执行结果...")
    for i in range(60):
        time.sleep(3)
        try:
            result_req = tat_models.DescribeInvocationTasksRequest()
            result_req.InvocationTaskIds = [f"{invocation_id}-{INSTANCE_ID}"]
            result_resp = client.DescribeInvocationTasks(result_req)

            if result_resp.InvocationTaskSet:
                task = result_resp.InvocationTaskSet[0]
                if task.TaskStatus == "SUCCESS":
                    print("✅ 命令执行成功")
                    if task.TaskResult and task.TaskResult.Output:
                        output = task.TaskResult.Output
                        try:
                            import base64
                            decoded = base64.b64decode(output).decode('utf-8', errors='replace')
                            print("输出:")
                            print("-" * 50)
                            print(decoded)
                            print("-" * 50)
                        except Exception:
                            print(f"输出: {output}")
                    return True
                elif task.TaskStatus == "FAILED":
                    print(f"❌ 命令执行失败: {task.TaskStatus}")
                    return False
                else:
                    print(f"  状态: {task.TaskStatus} ({i+1}/60)")
        except Exception as e:
            print(f"  查询中... ({i+1}/60) - {e}")

    print("⚠️ 等待超时")
    return False


def update_ogd_app():
    """一键更新OGD-Collector Pro应用"""
    print("=" * 50)
    print("开始更新 OGD-Collector Pro")
    print("=" * 50)

    command = """cd /opt/ogd-collector-pro && git pull origin main && systemctl restart ogd-collector && echo "更新完成" && systemctl status ogd-collector --no-pager"""

    success = run_command(command, timeout=120)
    if success:
        print("✅ OGD-Collector Pro 更新成功")
        print("访问: http://106.53.188.187")
    else:
        print("❌ 更新失败，请检查服务器状态")
    return success


def check_app_status():
    """检查OGD应用运行状态"""
    print("=" * 50)
    print("检查 OGD-Collector Pro 运行状态")
    print("=" * 50)

    command = """systemctl status ogd-collector --no-pager && echo "---" && curl -s http://127.0.0.1:5000 | head -5 && echo "---Nginx---" && systemctl status nginx --no-pager"""
    return run_command(command, timeout=60)


def show_help():
    """显示帮助信息"""
    help_text = """
腾讯云服务器管理脚本
====================

用法: python server_manager.py [命令]

命令列表:
  status      查看服务器实例状态
  reboot      重启服务器
  update      一键更新OGD-Collector Pro应用
  check       检查OGD应用运行状态
  run "命令"   在服务器上执行任意Shell命令

示例:
  python server_manager.py status
  python server_manager.py update
  python server_manager.py run "df -h"
  python server_manager.py run "cat /opt/ogd-collector-pro/app.py | head -20"
    """
    print(help_text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    try:
        if cmd == "status":
            get_instance_status()
        elif cmd == "reboot":
            reboot_instance()
        elif cmd == "update":
            update_ogd_app()
        elif cmd == "check":
            check_app_status()
        elif cmd == "run":
            if len(sys.argv) < 3:
                print("请提供要执行的命令")
                print('示例: python server_manager.py run "ls -la"')
                sys.exit(1)
            run_command(sys.argv[2])
        else:
            print(f"未知命令: {cmd}")
            show_help()
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
