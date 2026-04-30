import sys
print("Python:", sys.version)
try:
    import paramiko
    print("paramiko OK")
except ImportError:
    print("paramiko NOT installed")
    sys.exit(1)

# Upload v3_thesis.html to server
try:
    pkey = paramiko.Ed25519Key.from_private_key_file(r"C:\Users\MI\.ssh\id_ed25519")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("106.53.188.187", username="ubuntu", pkey=pkey, timeout=15)

    sftp = client.open_sftp()
    sftp.put(
        r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\templates\v3_thesis.html",
        "/opt/ogd-v8/templates/v3_thesis.html"
    )
    sftp.close()

    # Restart gunicorn
    stdin, stdout, stderr = client.exec_command("pkill -f gunicorn.*5008; sleep 2; cd /opt/ogd-v8 && PYTHONPATH=/opt/ogd-v8 /home/ubuntu/.local/bin/gunicorn v8_wsgi:app --bind 0.0.0.0:5008 --workers 2 --daemon")
    print("STDOUT:", stdout.read().decode().strip())
    print("STDERR:", stderr.read().decode().strip())

    client.close()
    print("UPLOAD_OK")
except Exception as e:
    print("ERROR:", e)
    sys.exit(1)
