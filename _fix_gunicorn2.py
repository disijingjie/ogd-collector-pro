import paramiko, time

pkey = paramiko.Ed25519Key.from_private_key_file(r"C:\Users\MI\.ssh\id_ed25519")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("106.53.188.187", username="ubuntu", pkey=pkey, timeout=15)

# Check and restart
for cmd in [
    "ps aux | grep 'gunicorn.*5008' | grep -v grep",
    "ss -tlnp | grep 5008",
    "cat /opt/ogd-v8/templates/v3_thesis.html | wc -c",
    "pkill -f 'gunicorn.*5008'; sleep 2; cd /opt/ogd-v8 && PYTHONPATH=/opt/ogd-v8 /home/ubuntu/.local/bin/gunicorn v8_wsgi:app --bind 0.0.0.0:5008 --workers 2 --daemon; sleep 2; ps aux | grep 'gunicorn.*5008' | grep -v grep",
]:
    print(f">>> {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd)
    time.sleep(1)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out: print("OUT:", out[:500])
    if err: print("ERR:", err[:500])
    print()

client.close()
