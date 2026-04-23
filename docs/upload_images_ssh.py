import os
import subprocess
import base64

LOCAL_DIR = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\static\thesis_charts"
SERVER_IP = "106.53.188.187"
SERVER_USER = "ubuntu"
SERVER_PASSWORD = "wenming890503"
REMOTE_DIR = "/opt/ogd-collector-pro/static/thesis_charts"

files = [f for f in os.listdir(LOCAL_DIR) if f.endswith('.png')]
print(f"开始上传 {len(files)} 张图片到服务器...")

# 先创建远程目录
subprocess.run([
    "python", "txcloud.py", "run",
    f"mkdir -p {REMOTE_DIR}"
], cwd=os.path.dirname(__file__), check=False)

for i, filename in enumerate(files, 1):
    local_path = os.path.join(LOCAL_DIR, filename)
    with open(local_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('ascii')
    
    # 分批传输，避免命令过长
    chunk_size = 50000
    remote_path = f"{REMOTE_DIR}/{filename}"
    
    # 先清空目标文件
    subprocess.run([
        "python", "txcloud.py", "run",
        f"> {remote_path}"
    ], cwd=os.path.dirname(__file__), check=False)
    
    # 分块追加
    for j in range(0, len(b64), chunk_size):
        chunk = b64[j:j+chunk_size]
        cmd = f'echo "{chunk}" >> {remote_path}'
        subprocess.run([
            "python", "txcloud.py", "run", cmd
        ], cwd=os.path.dirname(__file__), check=False)
    
    # base64解码
    subprocess.run([
        "python", "txcloud.py", "run",
        f"base64 -d {remote_path} > {remote_path}.tmp && mv {remote_path}.tmp {remote_path}"
    ], cwd=os.path.dirname(__file__), check=False)
    
    print(f"  [{i}/{len(files)}] {filename} ({len(data)//1024}KB)")

print(f"✅ 全部上传完成！共 {len(files)} 张图片")
