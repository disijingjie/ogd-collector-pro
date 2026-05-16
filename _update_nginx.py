#!/usr/bin/env python3
"""更新服务器Nginx配置 - 添加Gzip压缩和静态资源缓存策略"""
import subprocess
import os

SSH = r'C:\Program Files\Git\usr\bin\ssh.exe'
KEY = r'C:\Users\MI\.ssh\id_ed25519'
HOST = 'ubuntu@106.53.188.187'

CONF_FILE = os.path.join(os.path.dirname(__file__), 'nginx_ogd_collector.conf')

with open(CONF_FILE, 'rb') as f:
    content = f.read()

print(f"上传Nginx配置文件 ({len(content)} bytes)...")

# Upload to server
cmd = [SSH, '-o', 'StrictHostKeyChecking=no', '-i', KEY, HOST,
       'cat > /tmp/ogd_nginx.conf && echo OK']
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = proc.communicate(input=content)

if proc.returncode != 0:
    print(f"上传失败: {stderr.decode()}")
    exit(1)

print("✓ 配置文件已上传到 /tmp/ogd_nginx.conf")

# Copy to nginx config and test
print("测试Nginx配置...")
cmd2 = [SSH, '-o', 'StrictHostKeyChecking=no', '-i', KEY, HOST,
        'sudo cp /tmp/ogd_nginx.conf /etc/nginx/sites-available/ogd-collector && sudo nginx -t 2>&1']
proc2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout2, stderr2 = proc2.communicate(timeout=15)
print(stdout2.decode().strip())

if proc2.returncode == 0:
    print("✓ Nginx配置测试通过！")
    # Reload nginx
    cmd3 = [SSH, '-o', 'StrictHostKeyChecking=no', '-i', KEY, HOST,
            'sudo systemctl reload nginx && echo "✓ Nginx已重新加载"']
    proc3 = subprocess.Popen(cmd3, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout3, _ = proc3.communicate(timeout=15)
    print(stdout3.decode().strip())
else:
    print("✗ Nginx配置测试失败，未重新加载")
    print(f"错误: {stderr2.decode().strip()}")
