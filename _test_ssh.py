import paramiko, sys, traceback
from pathlib import Path

try:
    key_path = Path.home() / ".ssh" / "id_ed25519"
    print("Key path:", key_path)
    print("Key exists:", key_path.exists())
    key = paramiko.Ed25519Key.from_private_key_file(str(key_path))
    print("Key loaded OK")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting...")
    client.connect('106.53.188.187', username='root', pkey=key, timeout=10, banner_timeout=10, auth_timeout=10)
    print("SSH connect OK")
    stdin, stdout, stderr = client.exec_command('echo hello-from-server')
    print("Output:", stdout.read().decode().strip())
    client.close()
    print("Closed OK")
except Exception as e:
    print("ERROR:", type(e).__name__, str(e))
    traceback.print_exc()
    sys.exit(1)
