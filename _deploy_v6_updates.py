#!/usr/bin/env python3
"""V6批量部署脚本 - 部署全部6项更新"""
import subprocess
import os
import time

SSH = r'C:\Program Files\Git\usr\bin\ssh.exe'
KEY = r'C:\Users\MI\.ssh\id_ed25519'
HOST = 'ubuntu@106.53.188.187'
SERVER_PATH = '/opt/ogd-collector-pro'
PROJECT = r'C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system'

def ssh_exec(cmd):
    proc = subprocess.Popen([SSH, '-o', 'StrictHostKeyChecking=no', '-i', KEY, HOST, cmd],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(timeout=30)
    return stdout.decode('utf-8', errors='replace'), proc.returncode

def upload_file(local, server):
    if not os.path.exists(local):
        print(f"  SKIP (not found): {local}")
        return False
    with open(local, 'rb') as f:
        content = f.read()
    cmd = [SSH, '-o', 'StrictHostKeyChecking=no', '-i', KEY, HOST,
           f'cat > {server} && echo "OK: $(wc -c < {server}) bytes"']
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(input=content)
    ok = proc.returncode == 0
    status = "✓" if ok else "✗"
    print(f"  {status} {os.path.basename(local)} ({len(content):,} bytes)")
    return ok

# 文件列表
FILES = [
    # 1. P0: 实时采集看板 - v6_app.py新增3个API
    ('v6_app.py', f'{SERVER_PATH}/v6_app.py'),
    # 2. P0: 互锁映射数据
    ('data/data_thesis_interlock.json', f'{SERVER_PATH}/data/data_thesis_interlock.json'),
]

# 模板文件
TEMPLATES = [
    'v6_collection.html',   # P0: 实时看板
    'v6_caliber.html',      # P0: 互锁追踪
    'v6_literature_db.html',# P1: 文献去重
    'base_v6.html',         # P2: 移动端响应式
]

print("=" * 60)
print("V6 全量部署 - 6项更新")
print("=" * 60)

# Step 1: 上传核心Python文件和数据
print("\n=== 1. 上传核心文件 ===")
for local_rel, server_path in FILES:
    local = os.path.join(PROJECT, local_rel)
    upload_file(local, server_path)

# Step 2: 上传模板文件
print("\n=== 2. 上传模板文件 ===")
for t in TEMPLATES:
    local = os.path.join(PROJECT, 'templates', t)
    server = f'{SERVER_PATH}/templates/{t}'
    upload_file(local, server)

# Step 3: 重启服务
print("\n=== 3. 重启服务 ===")
stdout, rc = ssh_exec("sudo systemctl restart ogd-collector && sleep 3 && sudo systemctl is-active ogd-collector")
if 'active' in stdout:
    print("✓ 服务已重启并运行中")
else:
    print(f"⚠ 服务状态: {stdout}")

# Step 4: 校验关键页面
print("\n=== 4. 部署校验 ===")
pages = ['/', '/collection', '/caliber', '/literature', '/map',
         '/api/collection/status', '/api/collection/health', '/api/collection/timeline',
         '/api/interlock/check', '/api/literature/dedup']
errors = []
for page in pages:
    stdout, rc = ssh_exec(f"curl -s -o /dev/null -w '%{{http_code}}' http://127.0.0.1:5000{page}")
    status = stdout.strip().replace('\n', '')
    ok = '200' in status
    mark = "✓" if ok else "✗"
    print(f"  {mark} {page}: {status}")
    if not ok:
        errors.append(page)

# Step 5: 模板数校验
print("\n=== 5. 模板数校验 ===")
stdout, rc = ssh_exec(f"ls {SERVER_PATH}/templates/v6_*.html | wc -l")
server_count = stdout.strip()
local_count = str(len([f for f in os.listdir(os.path.join(PROJECT, 'templates')) if f.startswith('v6_') and f.endswith('.html')]))
if server_count == local_count:
    print(f"  ✓ 模板数一致: {local_count}")
else:
    print(f"  ⚠ 模板数: 本地{local_count} vs 服务器{server_count}")

print("\n" + "=" * 60)
if errors:
    print(f"⚠ 部署完成，但有 {len(errors)} 个页面返回异常: {errors}")
else:
    print("✓ 全部6项更新部署完成！所有页面/API正常")
print(f"访问: http://{HOST.split('@')[1]}")
print("=" * 60)
