import paramiko, time

pkey = paramiko.Ed25519Key.from_private_key_file(r"C:\Users\MI\.ssh\id_ed25519")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("106.53.188.187", username="ubuntu", pkey=pkey, timeout=15)

# Check v8 files exist and syntax
for cmd in [
    "ls -la /opt/ogd-v8/v8_wsgi.py /opt/ogd-v8/v8_app.py",
    "cd /opt/ogd-v8 && python3 -c 'import v8_app; print(\"import OK\")' 2>&1",
    "cd /opt/ogd-v8 && python3 -c 'import v8_wsgi; print(\"wsgi import OK\")' 2>&1",
    "pkill -f 'gunicorn.*5008' 2>/dev/null; sleep 1; echo 'killed'",
]:
    print(f">>> {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out: print("OUT:", out)
    if err: print("ERR:", err)
    print()

# Start gunicorn with explicit output
print(">>> Starting gunicorn on 5008...")
cmd = "cd /opt/ogd-v8 && PYTHONPATH=/opt/ogd-v8 /home/ubuntu/.local/bin/gunicorn v8_wsgi:app --bind 0.0.0.0:5008 --workers 2 --daemon"
stdin, stdout, stderr = client.exec_command(cmd)
time.sleep(2)

# Check if it started
cmd2 = "ps aux | grep 'gunicorn.*5008' | grep -v grep; ss -tlnp | grep 5008"
stdin, stdout, stderr = client.exec_command(cmd2)
out = stdout.read().decode().strip()
if out:
    print("GUNICORN RUNNING:", out)
else:
    print("GUNICORN NOT RUNNING!")
    # Try foreground to see error
    print(">>> Trying foreground run for 3 seconds...")
    stdin, stdout, stderr = client.exec_command("cd /opt/ogd-v8 && PYTHONPATH=/opt/ogd-v8 timeout 3 /home/ubuntu/.local/bin/gunicorn v8_wsgi:app --bind 0.0.0.0:5008 --workers 1 2>&1")
    time.sleep(4)
    err_out = stderr.read().decode().strip()
    std_out = stdout.read().decode().strip()
    print("FG STDOUT:", std_out[-500:] if len(std_out) > 500 else std_out)
    print("FG STDERR:", err_out[-500:] if len(err_out) > 500 else err_out)

client.close()
