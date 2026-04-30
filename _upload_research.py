import paramiko

pkey = paramiko.Ed25519Key.from_private_key_file(r"C:\Users\MI\.ssh\id_ed25519")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("106.53.188.187", username="ubuntu", pkey=pkey, timeout=15)

sftp = client.open_sftp()
sftp.put(
    r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\templates\v3_research.html",
    "/opt/ogd-v8/templates/v3_research.html"
)
sftp.close()
client.close()
print("UPLOAD_OK")
