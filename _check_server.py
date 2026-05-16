#!/usr/bin/env python3
"""远程服务器状态检查脚本 - 通过SSH执行"""
import subprocess
import sys

SSH = r'C:\Program Files\Git\usr\bin\ssh.exe'
KEY = r'C:\Users\MI\.ssh\id_ed25519'
HOST = 'ubuntu@106.53.188.187'

def ssh_cmd(cmd):
    full_cmd = [SSH, '-o', 'StrictHostKeyChecking=no', '-i', KEY, HOST, cmd]
    r = subprocess.run(full_cmd, capture_output=True, text=True, timeout=30)
    return r.stdout.strip(), r.returncode

# 1. Check DB tables
print("=== DB Tables ===")
out, rc = ssh_cmd("cd /opt/ogd-collector-pro && python3 -c \"import sqlite3; conn=sqlite3.connect('data/ogd_database.db'); c=conn.cursor(); c.execute(\\\"SELECT name FROM sqlite_master WHERE type='table'\\\"); tables=[r[0] for r in c.fetchall()]; print('\\n'.join(tables))\"")
print(out)

# 2. Check recent collection tasks
print("\n=== Recent Collection Tasks ===")
out, rc = ssh_cmd("cd /opt/ogd-collector-pro && python3 -c \"import sqlite3; conn=sqlite3.connect('data/ogd_database.db'); c=conn.cursor(); c.execute('SELECT id,task_name,status,created_at,completed_at FROM collection_tasks ORDER BY id DESC LIMIT 5'); [print(r) for r in c.fetchall()]\"")
print(out)

# 3. Check platform health
print("\n=== Platform Health (latest 5) ===")
out, rc = ssh_cmd("cd /opt/ogd-collector-pro && python3 -c \"import sqlite3; conn=sqlite3.connect('data/ogd_database.db'); c=conn.cursor(); try: c.execute('SELECT platform_code,status,checked_at FROM platform_health_checks ORDER BY id DESC LIMIT 5'); [print(r) for r in c.fetchall()]; except: print('table not found')\"")
print(out)

# 4. Check collection_stats
print("\n=== Collection Stats (latest 5) ===")
out, rc = ssh_cmd("cd /opt/ogd-collector-pro && python3 -c \"import sqlite3; conn=sqlite3.connect('data/ogd_database.db'); c=conn.cursor(); try: c.execute('SELECT stat_date,tier,total_platforms,available_count,avg_score FROM collection_stats ORDER BY id DESC LIMIT 5'); [print(r) for r in c.fetchall()]; except: print('table not found')\"")
print(out)

# 5. Check v6_app.py routes for collection status
print("\n=== Collection Results JSON ===")
out, rc = ssh_cmd("cd /opt/ogd-collector-pro && python3 -c \"import json; data=json.load(open('data/v3_collection_results.json')); print(f'Platforms: {len(data)}'); statuses={}; [statuses.__setitem__(r.get('status','unknown'), statuses.get(r.get('status','unknown'),0)+1) for r in data]; print(f'Statuses: {statuses}')\"")
print(out)
