from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.tat.v20201028 import tat_client, models
import time
import base64

import os
cred = credential.Credential(
    os.environ.get('TENCENT_SECRET_ID', 'YOUR_SECRET_ID'),
    os.environ.get('TENCENT_SECRET_KEY', 'YOUR_SECRET_KEY')
)
http = HttpProfile()
http.endpoint = 'tat.tencentcloudapi.com'
profile = ClientProfile()
profile.httpProfile = http
client = tat_client.TatClient(cred, 'ap-guangzhou', profile)

# 创建命令
req = models.CreateCommandRequest()
req.CommandName = 'ogd-check-status'
req.Content = 'systemctl status ogd-collector --no-pager && echo "---OK---" && curl -s http://127.0.0.1:5000 | head -5'
req.CommandType = 'SHELL'
req.WorkingDirectory = '/root'
req.Timeout = 60
resp = client.CreateCommand(req)
cmd_id = resp.CommandId
print('命令ID:', cmd_id)

# 执行命令
invoke_req = models.InvokeCommandRequest()
invoke_req.CommandId = cmd_id
invoke_req.InstanceIds = ['lhins-kyp9be3t']
invoke_resp = client.InvokeCommand(invoke_req)
inv_id = invoke_resp.InvocationId
print('执行ID:', inv_id)

# 等待结果
for i in range(30):
    time.sleep(3)
    try:
        result_req = models.DescribeInvocationTasksRequest()
        result_req.InvocationTaskIds = [f'{inv_id}-lhins-kyp9be3t']
        result_resp = client.DescribeInvocationTasks(result_req)
        if result_resp.InvocationTaskSet:
            task = result_resp.InvocationTaskSet[0]
            if task.TaskStatus == 'SUCCESS':
                print('执行成功!')
                if task.TaskResult and task.TaskResult.Output:
                    try:
                        out = base64.b64decode(task.TaskResult.Output).decode('utf-8', errors='replace')
                        print(out)
                    except Exception as e:
                        print('解码输出失败:', e)
                        print(task.TaskResult.Output)
                break
            elif task.TaskStatus == 'FAILED':
                print('执行失败:', task.TaskStatus)
                if task.TaskResult and task.TaskResult.Output:
                    try:
                        out = base64.b64decode(task.TaskResult.Output).decode('utf-8', errors='replace')
                        print(out)
                    except:
                        pass
                break
            else:
                print(f'状态: {task.TaskStatus} ({i+1}/30)')
    except Exception as e:
        print(f'查询中... ({i+1}/30) - {e}')
