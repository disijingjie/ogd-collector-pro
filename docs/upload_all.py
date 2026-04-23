import os
import subprocess

LOCAL_DIR = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\static\thesis_charts"
SERVER = "ubuntu@106.53.188.187"
REMOTE_DIR = "/opt/ogd-collector-pro/static/thesis_charts"

files = sorted([f for f in os.listdir(LOCAL_DIR) if f.endswith('.png')])
print(f"开始上传 {len(files)} 张图片...")

success = 0
for i, filename in enumerate(files, 1):
    local = os.path.join(LOCAL_DIR, filename)
    remote = f"{REMOTE_DIR}/{filename}"
    cmd = [
        "scp", "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=15",
        local, f"{SERVER}:{remote}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, encoding='utf-8', errors='replace')
    if result.returncode == 0:
        print(f"  [{i}/{len(files)}] ✅ {filename}")
        success += 1
    else:
        print(f"  [{i}/{len(files)}] ❌ {filename} - {result.stderr[:100]}")

print(f"\n上传完成: {success}/{len(files)} 张成功")
