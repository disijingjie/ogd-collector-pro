# OGD-Collector Pro 项目记忆

## 服务器信息
- **IP**: 106.53.188.187
- **实例ID**: lhins-kyp9be3t
- **区域**: ap-guangzhou
- **系统**: Ubuntu 22.04
- **部署路径**: /opt/ogd-collector-pro
- **GitHub**: https://github.com/disijingjie/ogd-collector-pro

## SSH 配置
- **用户名**: ubuntu
- **密码**: wenming.890503（已配置免密登录）
- **公钥**: 已添加到服务器 ~/.ssh/authorized_keys
- **本地私钥**: C:\Users\MI\.ssh\id_ed25519

## 一键更新流程
当本地代码有变更时，执行以下步骤：

### 方式1：桌面脚本（推荐）
双击运行 `C:\Users\MI\Desktop\ogd-update.bat`

### 方式2：手动命令
```powershell
cd C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system
git add .
git commit -m "自动更新 $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin main
ssh ubuntu@106.53.188.187 "cd /opt/ogd-collector-pro && git pull origin main && sudo systemctl restart ogd-collector"
```

### 方式3：腾讯云控制台（备用）
1. 登录 https://console.cloud.tencent.com/lighthouse/instance
2. 找到实例 lhins-kyp9be3t → 一键登录
3. 执行：
```bash
cd /opt/ogd-collector-pro
git pull origin main
sudo systemctl restart ogd-collector
systemctl status ogd-collector --no-pager
```

## 服务管理命令
```bash
# 查看状态
sudo systemctl status ogd-collector --no-pager

# 重启服务
sudo systemctl restart ogd-collector

# 查看日志
sudo journalctl -u ogd-collector --no-pager -n 50

# 测试访问
curl -s http://127.0.0.1:5000 | head -5
```

## 已知问题
- 腾讯云API密钥已失效（SecretId不存在），无法使用TAT自动化助手
- SSH免密登录已配置成功，是主要连接方式

## 更新记录
- 2026-04-23: 配置SSH免密登录，创建一键更新脚本
