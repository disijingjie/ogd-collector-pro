# OGD-Collector Pro — GitHub 自动同步方案（推荐）

> 最佳实践：本地 → GitHub → 服务器自动拉取
> 优点：有版本历史、无需手动上传、多设备协作、回滚方便

---

## 架构图

```
┌─────────────┐     git push      ┌─────────────┐     git pull      ┌─────────────┐
│  本地开发    │ ───────────────→ │   GitHub    │ ───────────────→ │  腾讯云服务器 │
│  (Windows)   │                  │   仓库       │   (webhook/手动)  │  (Ubuntu)    │
└─────────────┘                  └─────────────┘                  └─────────────┘
     ↑                                                                 │
     └──────────────────────── 浏览器访问 http://服务器IP ──────────────┘
```

---

## 方案一：手动 Git 同步（最稳妥，推荐先用这个）

### 每次更新只需两步：

**Step 1：本地提交并推送**
```powershell
cd "C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system"

git add .
git commit -m "修复采集管理页面bug / 添加新功能xxx"
git push origin main
```

**Step 2：服务器拉取并重启**
```bash
ssh root@你的服务器IP

cd /opt/ogd-collector-pro
git pull origin main
systemctl restart ogd-collector
```

> 整个过程约 30 秒。

---

## 方案二：配置 SSH 密钥（免密码）

### 1. 本地生成密钥（只需一次）

```powershell
# 打开 PowerShell
ssh-keygen -t ed25519 -C "ambit@qq.com" -f "$env:USERPROFILE\.ssh\id_ed25519" -N '""'
```

### 2. 将公钥复制到服务器

```powershell
# 方法A：使用 ssh-copy-id（如果安装了）
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@你的服务器IP

# 方法B：手动复制
cat ~/.ssh/id_ed25519.pub
# 然后 SSH 登录服务器，粘贴到 ~/.ssh/authorized_keys
```

### 3. 配置 SSH 别名（方便使用）

编辑 `C:\Users\MI\.ssh\config`，添加：

```
Host ogd-server
    HostName 你的服务器IP
    User root
    IdentityFile ~/.ssh/id_ed25519
    StrictHostKeyChecking no
```

之后就可以用 `ssh ogd-server` 直接登录，无需密码。

### 4. 服务器端配置 GitHub 免密

```bash
ssh root@你的服务器IP

# 生成服务器端的密钥
ssh-keygen -t ed25519 -C "server@ogd-collector" -f ~/.ssh/id_ed25519 -N ""

# 查看公钥
cat ~/.ssh/id_ed25519.pub
```

将输出的公钥添加到 GitHub：
- 打开 https://github.com/settings/keys
- 点击 **New SSH key**
- Title 填：`OGD-Server`
- Key 粘贴刚才的公钥
- 点击 **Add SSH key**

---

## 方案三：GitHub Actions 自动部署（高级）

每次 `git push` 后，GitHub 自动部署到服务器。

### 1. 在 GitHub 仓库添加 Secrets

进入仓库 → Settings → Secrets and variables → Actions → New repository secret

添加以下 secrets：

| Secret 名称 | 值 |
|------------|-----|
| `SERVER_HOST` | 你的服务器公网IP |
| `SERVER_USER` | root |
| `SERVER_KEY` | 服务器私钥（~/.ssh/id_ed25519 的内容） |

### 2. 创建 GitHub Actions 工作流

在项目中创建文件：`.github/workflows/deploy.yml`

```yaml
name: Deploy to Tencent Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_KEY }}
        script: |
          cd /opt/ogd-collector-pro
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          systemctl restart ogd-collector
          echo "Deployed at $(date)"
```

### 3. 效果

以后每次本地执行 `git push`，GitHub 会自动：
1. 拉取最新代码到服务器
2. 安装新依赖
3. 重启服务

你什么都不用做，等 1 分钟就行。

---

## 方案对比

| 方案 | 操作复杂度 | 每次更新时间 | 是否需要配置 | 推荐度 |
|------|-----------|------------|------------|--------|
| 手动 Git 同步 | ⭐ 简单 | 30 秒 | 无 | ⭐⭐⭐⭐⭐ |
| SSH 密钥免密 | ⭐⭐ 中等 | 20 秒 | 一次 | ⭐⭐⭐⭐⭐ |
| GitHub Actions | ⭐⭐⭐ 复杂 | 0 秒（全自动） | 一次 | ⭐⭐⭐⭐ |
| SCP 手动上传 | ⭐⭐ 中等 | 1-2 分钟 | 无 | ⭐⭐ |

---

## 快速开始建议

**今天（第一次部署）：**
1. 买腾讯云服务器
2. 运行一键部署脚本
3. 配置 SSH 密钥（本地 + 服务器各一次）

**以后（每次更新）：**
```powershell
# 本地修改代码...
git add .
git commit -m "xxx"
git push origin main

# SSH 到服务器拉取
ssh ogd-server "cd /opt/ogd-collector-pro && git pull && systemctl restart ogd-collector"
```

或者更懒一点，配置好 GitHub Actions 后，只需：
```powershell
git push origin main
# 等 1 分钟，自动部署完成
```

---

## 安全建议

1. **不要用密码登录**：配置好 SSH 密钥后，关闭服务器的密码登录
   ```bash
   # 在服务器上执行
   sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
   systemctl restart sshd
   ```

2. **修改默认 SSH 端口**（可选）：
   ```bash
   sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config
   systemctl restart sshd
   ```

3. **定期备份数据库**：
   ```bash
   # 在服务器上添加定时任务
   crontab -e
   # 添加：每天凌晨3点备份
   0 3 * * * cp /opt/ogd-collector-pro/data/ogd_database.db /opt/ogd-collector-pro/backups/ogd_database_$(date +\%Y\%m\%d).db
   ```

---

> 作者：文明（武汉大学信息管理学院博士生）
> 日期：2026-04-22
