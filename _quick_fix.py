import paramiko

pkey = paramiko.Ed25519Key.from_private_key_file(r"C:\Users\MI\.ssh\id_ed25519")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("106.53.188.187", username="ubuntu", pkey=pkey, timeout=15)

# Kill any existing
client.exec_command("pkill -f 'gunicorn.*5008' 2>/dev/null")

# Start new one
stdin, stdout, stderr = client.exec_command("cd /opt/ogd-v8 && PYTHONPATH=/opt/ogd-v8 /home/ubuntu/.local/bin/gunicorn v8_wsgi:app --bind 0.0.0.0:5008 --workers 2 --daemon 2>&1; echo 'EXIT_CODE=$?'")
out = stdout.read().decode().strip()
print("START:", out)

# Check
stdin, stdout, stderr = client.exec_command("sleep 2 && ps aux | grep 'gunicorn.*5008' | grep -v grep && ss -tlnp | grep 5008")
out = stdout.read().decode().strip()
print("CHECK:", out if out else "NO PROCESS")

client.close()
