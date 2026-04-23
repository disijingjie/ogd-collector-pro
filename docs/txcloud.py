#!/usr/bin/env python3
"""
腾讯云轻量服务器管理脚本 - 一步到位版
基于腾讯云 Python SDK，无需 tccli，绕过 Windows 兼容性问题

用法:
    python txcloud.py status      # 查看服务器状态
    python txcloud.py reboot      # 重启服务器
    python txcloud.py firewall    # 查看防火墙规则
    python txcloud.py monitor     # 查看CPU/内存/流量监控
    python txcloud.py update      # 一键更新OGD应用 (SSH方式)
    python txcloud.py check       # 检查OGD应用状态 (SSH方式)
    python txcloud.py push        # 本地推送代码 + 服务器更新 (SSH方式)
    python txcloud.py logs [N]    # 查看OGD日志 (SSH方式)
    python txcloud.py run "命令"   # 在服务器执行任意命令 (SSH方式)
"""

import json
import sys
import time
from datetime import datetime, timedelta

import paramiko
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.lighthouse.v20200324 import lighthouse_client, models
from tencentcloud.monitor.v20180724 import monitor_client, models as monitor_models

# ===== 配置 =====
import os
SECRET_ID = os.environ.get("TENCENT_SECRET_ID", "YOUR_SECRET_ID")
SECRET_KEY = os.environ.get("TENCENT_SECRET_KEY", "YOUR_SECRET_KEY")
REGION = "ap-guangzhou"
INSTANCE_ID = "lhins-kyp9be3t"
SERVER_IP = "106.53.188.187"
SERVER_USER = "ubuntu"
SERVER_PASSWORD = os.environ.get("SERVER_PASSWORD", "wenming.890503")
APP_DIR = "/opt/ogd-collector-pro"


def get_lighthouse_client():
    """获取轻量服务器客户端"""
    cred = credential.Credential(SECRET_ID, SECRET_KEY)
    http = HttpProfile()
    http.endpoint = "lighthouse.tencentcloudapi.com"
    profile = ClientProfile()
    profile.httpProfile = http
    return lighthouse_client.LighthouseClient(cred, REGION, profile)


def get_monitor_client():
    """获取监控客户端"""
    cred = credential.Credential(SECRET_ID, SECRET_KEY)
    http = HttpProfile()
    http.endpoint = "monitor.tencentcloudapi.com"
    profile = ClientProfile()
    profile.httpProfile = http
    return monitor_client.MonitorClient(cred, REGION, profile)


_ssh_client = None

def get_ssh_client():
    """获取SSH连接（复用连接）"""
    global _ssh_client
    if _ssh_client is None or _ssh_client.get_transport() is None or not _ssh_client.get_transport().is_active():
        _ssh_client = paramiko.SSHClient()
        _ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 修复腾讯云服务器SSH兼容性问题
        transport = paramiko.Transport((SERVER_IP, 22))
        transport.connect(username=SERVER_USER, password=SERVER_PASSWORD)
        _ssh_client._transport = transport
    return _ssh_client


def ssh_run(command, timeout=120):
    """SSH执行命令（paramiko方式，自动密码认证）"""
    print(f">>> SSH: {command[:100]}{'...' if len(command) > 100 else ''}")
    try:
        client = get_ssh_client()
        stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
        out = stdout.read().decode('utf-8', errors='replace')
        err = stderr.read().decode('utf-8', errors='replace')
        exit_code = stdout.channel.recv_exit_status()
        if out:
            print(out)
        if err and "Warning" not in err:
            print("[stderr]", err.strip())
        return exit_code == 0
    except Exception as e:
        print(f"[SSH错误] {e}")
        _ssh_client = None
        return False


def cmd_status():
    """查看服务器状态"""
    client = get_lighthouse_client()
    req = models.DescribeInstancesRequest()
    req.InstanceIds = [INSTANCE_ID]
    resp = client.DescribeInstances(req)
    inst = resp.InstanceSet[0]

    print("=" * 60)
    print("腾讯云轻量服务器状态")
    print("=" * 60)
    print(f"实例ID:      {inst.InstanceId}")
    print(f"实例名称:    {inst.InstanceName}")
    print(f"运行状态:    {inst.InstanceState}")
    print(f"公网IP:      {inst.PublicAddresses[0] if inst.PublicAddresses else '无'}")
    print(f"内网IP:      {inst.PrivateAddresses[0] if inst.PrivateAddresses else '无'}")
    print(f"配置:        {inst.CPU}核 CPU / {inst.Memory}G 内存")
    print(f"系统盘:      {inst.SystemDisk.DiskSize}GB {inst.SystemDisk.DiskType}")
    print(f"带宽:        {inst.InternetAccessible.InternetMaxBandwidthOut}Mbps")
    print(f"计费方式:    {'包年包月' if inst.InstanceChargeType == 'PREPAID' else '按量计费'}")
    print(f"创建时间:    {inst.CreatedTime}")
    print(f"到期时间:    {inst.ExpiredTime}")
    print(f"操作系统:    {inst.OsName}")
    print(f"可用区:      {inst.Zone}")
    print(f"最新操作:    {inst.LatestOperation} ({inst.LatestOperationState})")
    print("=" * 60)


def cmd_reboot():
    """重启服务器"""
    print("=" * 60)
    print("重启服务器")
    print("=" * 60)
    client = get_lighthouse_client()
    req = models.RebootInstancesRequest()
    req.InstanceIds = [INSTANCE_ID]
    resp = client.RebootInstances(req)
    print(f"重启请求已发送: {resp.RequestId}")
    print("等待服务器恢复运行...")

    for i in range(60):
        time.sleep(5)
        try:
            req2 = models.DescribeInstancesRequest()
            req2.InstanceIds = [INSTANCE_ID]
            resp2 = client.DescribeInstances(req2)
            status = resp2.InstanceSet[0].InstanceState
            if status == "RUNNING":
                print(f"✅ 服务器已恢复运行 ({(i+1)*5}秒)")
                return
            print(f"  当前状态: {status} ({(i+1)*5}s)")
        except Exception as e:
            print(f"  等待中... ({(i+1)*5}s)")
    print("⚠️ 等待超时，请稍后手动检查")


def cmd_firewall():
    """查看防火墙规则"""
    print("=" * 60)
    print("防火墙规则")
    print("=" * 60)
    client = get_lighthouse_client()
    req = models.DescribeFirewallRulesRequest()
    req.InstanceId = INSTANCE_ID
    resp = client.DescribeFirewallRules(req)

    print(f"{'协议':<8} {'端口':<12} {'动作':<10} {'备注'}")
    print("-" * 60)
    for rule in resp.FirewallRuleSet:
        action = "允许" if rule.Action == "ACCEPT" else "拒绝"
        print(f"{rule.Protocol:<8} {rule.Port:<12} {action:<10} {rule.FirewallRuleDescription or ''}")
    print("=" * 60)


def cmd_monitor():
    """查看监控数据"""
    print("=" * 60)
    print("服务器监控数据 (最近1小时)")
    print("=" * 60)

    client = get_monitor_client()
    end_time = datetime.now().astimezone()
    start_time = end_time - timedelta(hours=1)

    metrics = [
        ("CPU利用率", "CPUUsage", "%"),
        ("内存利用率", "MemUsage", "%"),
        ("内网入带宽", "LanInTraffic", "Mbps"),
        ("内网出带宽", "LanOutTraffic", "Mbps"),
        ("外网入带宽", "WanInTraffic", "Mbps"),
        ("外网出带宽", "WanOutTraffic", "Mbps"),
        ("磁盘读流量", "DiskReadTraffic", "MB/s"),
        ("磁盘写流量", "DiskWriteTraffic", "MB/s"),
    ]

    for name, metric, unit in metrics:
        try:
            req = monitor_models.GetMonitorDataRequest()
            req.Namespace = "QCE/LIGHTHOUSE"
            req.MetricName = metric
            req.Instances = [{"Dimensions": [{"Name": "InstanceId", "Value": INSTANCE_ID}]}]
            req.Period = 300
            req.StartTime = start_time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
            req.EndTime = end_time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
            resp = client.GetMonitorData(req)

            if resp.DataPoints and len(resp.DataPoints) > 0 and resp.DataPoints[0].Values:
                values = resp.DataPoints[0].Values
                latest = values[-1]
                avg = sum(values) / len(values)
                print(f"  {name:<12} 最新: {latest:.2f}{unit}  平均: {avg:.2f}{unit}")
            else:
                print(f"  {name:<12} 无数据")
        except Exception as e:
            print(f"  {name:<12} 获取失败: {e}")
    print("=" * 60)


def cmd_update():
    """一键更新OGD应用"""
    print("=" * 60)
    print("更新 OGD-Collector Pro")
    print("=" * 60)
    success = ssh_run(f"cd {APP_DIR} && git pull origin main && systemctl restart ogd-collector")
    if success:
        print("\n✅ 更新完成 → http://106.53.188.187")
    else:
        print("\n❌ 更新失败")
    return success


def cmd_check():
    """检查OGD应用状态"""
    print("=" * 60)
    print("OGD-Collector Pro 运行状态")
    print("=" * 60)
    ssh_run(f"systemctl status ogd-collector --no-pager")
    print("-" * 60)
    ssh_run("curl -s http://127.0.0.1:5000 | head -5")


def cmd_logs():
    """查看OGD日志"""
    lines = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    print("=" * 60)
    print(f"OGD应用日志 (最近{lines}行)")
    print("=" * 60)
    ssh_run(f"journalctl -u ogd-collector --no-pager -n {lines}")


def cmd_push():
    """本地推送 + 服务器更新"""
    import os
    local_dir = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system"
    print("=" * 60)
    print("一键发布: 本地推送 → GitHub → 服务器更新")
    print("=" * 60)

    # 1. 本地推送
    print("\n[1/3] 本地推送代码...")
    subprocess.run(["git", "add", "."], cwd=local_dir, capture_output=True)
    r = subprocess.run(["git", "commit", "-m", f"auto update {datetime.now().strftime('%m-%d %H:%M')}"],
                       cwd=local_dir, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0:
        print("  提交信息:", (r.stderr or "").strip() or "无变更")
    r = subprocess.run(["git", "push", "origin", "main"], cwd=local_dir,
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    print("  ", (r.stdout or "").strip() or "推送完成")

    # 2. 服务器更新
    print("\n[2/3] 服务器拉取更新...")
    ssh_run(f"cd {APP_DIR} && git pull origin main")

    # 3. 重启服务
    print("\n[3/3] 重启服务...")
    ssh_run("systemctl restart ogd-collector")

    print("\n" + "=" * 60)
    print("✅ 发布完成！访问: http://106.53.188.187")
    print("=" * 60)


def cmd_run():
    """在服务器执行任意命令"""
    if len(sys.argv) < 3:
        print("请提供要执行的命令")
        print('示例: python txcloud.py run "df -h"')
        return
    ssh_run(sys.argv[2])


def show_help():
    print("""
腾讯云轻量服务器管理脚本 - 一步到位版
========================================

【腾讯云API操作】
  python txcloud.py status       查看服务器实例状态
  python txcloud.py reboot       重启服务器
  python txcloud.py firewall     查看防火墙规则
  python txcloud.py monitor      查看CPU/内存/流量监控

【SSH远程操作】
  python txcloud.py update       服务器拉取GitHub最新代码并重启
  python txcloud.py check        检查OGD应用运行状态
  python txcloud.py logs [N]     查看OGD日志，默认50行
  python txcloud.py push         ⭐ 一键发布 (本地推送 → GitHub → 服务器更新)
  python txcloud.py run "命令"    在服务器执行任意Shell命令

最常用:
  python txcloud.py push         ← 改完代码，一键发布
  python txcloud.py status       ← 查看服务器状态
  python txcloud.py monitor      ← 查看资源使用情况
    """)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()
    commands = {
        "status": cmd_status,
        "reboot": cmd_reboot,
        "firewall": cmd_firewall,
        "monitor": cmd_monitor,
        "update": cmd_update,
        "check": cmd_check,
        "logs": cmd_logs,
        "push": cmd_push,
        "run": cmd_run,
        "help": show_help,
    }

    if cmd in commands:
        try:
            commands[cmd]()
        except Exception as e:
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"未知命令: {cmd}")
        show_help()
