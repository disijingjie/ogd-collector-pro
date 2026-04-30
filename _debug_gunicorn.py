import paramiko, time

pkey = paramiko.Ed25519Key.from_private_key_file(r"C:\Users\MI\.ssh\id_ed25519")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("106.53.188.187", username="ubuntu", pkey=pkey, timeout=15)

# Test import
cmds = [
    "cd /opt/ogd-v8 && python3 -c 'import v8_wsgi; print(\"import ok\")' 2>&1",
    "cd /opt/ogd-v8 && python3 -c 'import v8_app; print(\"app ok\")' 2>&1",
    "which gunicorn; which python3",
    "ls -la /home/ubuntu/.local/bin/gunicorn",
]

for cmd in cmds:
    print(f">>> {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out: print("OUT:", out)
    if err: print("ERR:", err)
    print()

# Try starting in background with nohup
print(">>> Starting with nohup...")
stdin, stdout, stderr = client.exec_command("cd /opt/ogd-v8 && nohup bash -c 'PYTHONPATH=/opt/ogd-v8 /home/ubuntu/.local/bin/gunicorn v8_wsgi:app --bind 0.0.0.0:5008 --workers 2' > /tmp/guni.log 2>&1 & sleep 3 && ps aux | grep gunicorn | grep -v grep")
time.sleep(5)
out = stdout.read().decode().strip()
err = stderr.read().decode().strip()
print("OUT:", out)
if err: print("ERR:", err)

# Check log
stdin, stdout, stderr = client.exec_command("cat /tmp/guni.log 2>/dev/null | tail -20")
print("LOG:", stdout.read().decode().strip())

client.close()
