import paramiko

pkey = paramiko.Ed25519Key.from_private_key_file(r"C:\Users\MI\.ssh\id_ed25519")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("106.53.188.187", username="ubuntu", pkey=pkey, timeout=15)

commands = [
    "ps aux | grep gunicorn | grep -v grep",
    "netstat -tlnp 2>/dev/null | grep 5008 || ss -tlnp | grep 5008",
    "ls -la /opt/ogd-v8/templates/v3_thesis.html | awk '{print $5}'",
    "cd /opt/ogd-v8 && PYTHONPATH=/opt/ogd-v8 /home/ubuntu/.local/bin/gunicorn v8_wsgi:app --bind 0.0.0.0:5008 --workers 2 --daemon 2>&1; echo 'GUNICORN_EXIT=$?'",
]

for cmd in commands:
    print(f">>> {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out: print("OUT:", out)
    if err: print("ERR:", err)
    print()

client.close()
