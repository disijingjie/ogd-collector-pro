import os
import paramiko

SERVER_IP = "106.53.188.187"
SERVER_USER = "ubuntu"
SERVER_PASSWORD = "wenming890503"
LOCAL_DIR = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\static\thesis_charts"
REMOTE_DIR = "/opt/ogd-collector-pro/static/thesis_charts"

print("连接服务器...")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
transport = paramiko.Transport((SERVER_IP, 22))
transport.connect(username=SERVER_USER, password=SERVER_PASSWORD)
client._transport = transport
sftp = client.open_sftp()

# 创建远程目录
sftp.mkdir(REMOTE_DIR) if not REMOTE_DIR else None

files = [f for f in os.listdir(LOCAL_DIR) if f.endswith('.png')]
print(f"开始上传 {len(files)} 张图片...")

for i, filename in enumerate(files, 1):
    local_path = os.path.join(LOCAL_DIR, filename)
    remote_path = f"{REMOTE_DIR}/{filename}"
    sftp.put(local_path, remote_path)
    print(f"  [{i}/{len(files)}] {filename}")

sftp.close()
transport.close()
print(f"✅ 全部上传完成！共 {len(files)} 张图片")
