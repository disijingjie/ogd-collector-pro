# OGD-Collector Pro 部署运维手册

> 本文档记录服务器架构、部署流程、常见问题及解决方案。
> 最后更新：2026-04-28

---

## 1. 服务器架构

```
用户浏览器
    |
    v
Nginx (端口 80)
    |-- /v3/  --> 127.0.0.1:5001 (v3_app.py / v3_wsgi:app)
    |-- /     --> 127.0.0.1:5002 (v4_app.py / v4_wsgi:app)
    |-- /v2/  --> 127.0.0.1:5000 (app.py / wsgi:app)
    |-- /static --> /opt/ogd-collector-pro/static
```

### 三个Flask应用

| 应用 | 端口 | WSGI文件 | 路由前缀 | 用途 |
|:---|:---|:---|:---|:---|
| 旧版 | 5000 | wsgi.py | `/` | 旧版OGD系统（systemd管理） |
| V3 | 5001 | v3_wsgi.py | `/v3/` | 博士论文展示系统（独立gunicorn） |
| V4 | 5002 | v4_wsgi.py | `/` | 论文全章展示系统（独立gunicorn） |

**关键认知**：
- `/v3/` 路由到端口5001，不是端口5000
- v3_app.py 和 app.py 是两个独立的应用
- 修改 `/v3/` 页面必须改 **v3_app.py** 和 **v3_*.html** 模板

---

## 2. 文件位置

### 服务器
```
/opt/ogd-collector-pro/
    ├── app.py              # 旧版Flask应用（端口5000）
    ├── wsgi.py             # 旧版WSGI入口
    ├── v3_app.py           # V3 Flask应用（端口5001）
    ├── v3_wsgi.py          # V3 WSGI入口
    ├── v4_app.py           # V4 Flask应用（端口5002）
    ├── v4_wsgi.py          # V4 WSGI入口
    ├── templates/
    │   ├── v3_index.html       # V3旧首页（已废弃）
    │   ├── v3_dashboard.html   # V3新首页（系统概览）
    │   ├── v3_collection.html  # V3采集中心
    │   ├── v3_platforms.html   # V3平台列表
    │   ├── v3_analysis.html    # V3分析看板
    │   ├── v3_thesis.html      # V3论文成果
    │   ├── v3_research.html    # V3研究拓展
    │   ├── v3_reproduce.html   # V3数据复现
    │   ├── v3_rules.html       # V3规则说明
    │   ├── v3_collection_mechanism.html
    │   └── base_v3.html        # V3基础模板
    └── static/             # 静态文件（CSS/JS/图片）
```

### 本地开发
```
C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\
    ├── app.py
    ├── v3_app.py
    ├── templates\           # 修改HTML模板
    └── static\              # 修改CSS/JS/图片
```

---

## 3. 部署流程（本地修改 → 服务器同步）

### 推荐方式：一键同步脚本

**文件位置**：`C:\Users\MI\Desktop\ogd-sync.py`

**使用步骤**：
1. 在本地修改代码（HTML/CSS/JS/Python）
2. 保存文件
3. 双击运行 `ogd-sync.py`
4. 等待30-60秒完成

**脚本功能**：
- Git提交并推送到GitHub（备份）
- tar打包（排除venv/__pycache__/.git等）
- SCP上传到服务器
- 服务器解压并备份旧代码
- 重启V3 gunicorn（端口5001）
- 验证HTTP 200

### 手动方式

```powershell
cd C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system

# 1. Git备份
git add .
git commit -m "update: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin main

# 2. 打包
tar -czf deploy.tar.gz --exclude=venv --exclude=__pycache__ --exclude=.git .

# 3. 上传
scp deploy.tar.gz ubuntu@106.53.188.187:/tmp/

# 4. 服务器部署
ssh ubuntu@106.53.188.187 "cd /opt/ogd-collector-pro && sudo tar -xzf /tmp/deploy.tar.gz --overwrite"

# 5. 重启V3服务
ssh ubuntu@106.53.188.187 "sudo pkill -f v3_wsgi; sleep 1; bash -c 'cd /opt/ogd-collector-pro && export PYTHONPATH=/home/ubuntu/.local/lib/python3.10/site-packages && /home/ubuntu/.local/bin/gunicorn v3_wsgi:app --bind 0.0.0.0:5001 --workers 2 --daemon'"
```

---

## 4. 服务管理命令

### 查看状态
```bash
# 查看所有gunicorn进程
ps aux | grep gunicorn | grep -v grep

# 查看端口占用
sudo lsof -i :5001

# 测试V3服务
curl -s http://127.0.0.1:5001/ | head -5
```

### 重启V3服务（端口5001）
```bash
# 杀死旧进程
sudo pkill -f "v3_wsgi"

# 启动新进程（必须用bash -c，PYTHONPATH不能和timeout混用）
bash -c "cd /opt/ogd-collector-pro && \
export PYTHONPATH=/home/ubuntu/.local/lib/python3.10/site-packages && \
/home/ubuntu/.local/bin/gunicorn v3_wsgi:app --bind 0.0.0.0:5001 --workers 2 --daemon"
```

**注意**：`PYTHONPATH=... timeout 5 cmd` 语法错误！timeout会把PYTHONPATH当命令。必须用 `bash -c "export PYTHONPATH=... && cmd"`。

### 重启旧版服务（端口5000，systemd管理）
```bash
sudo systemctl restart ogd-collector
sudo systemctl status ogd-collector --no-pager
```

### 重启Nginx
```bash
sudo systemctl reload nginx
```

---

## 5. 常见问题

### Q1: 同步成功但页面显示旧版
**原因**：浏览器缓存  
**解决**：按 `Ctrl+F5` 强制刷新

### Q2: 页面返回404
**原因**：v3_app.py缺少对应路由  
**解决**：在v3_app.py中添加 `@app.route('/xxx')` 路由

### Q3: 页面返回502 Bad Gateway
**原因**：端口5001的gunicorn未启动  
**解决**：按上方"重启V3服务"命令执行

### Q4: gunicorn启动失败（无输出）
**原因**：命令语法错误  
**解决**：使用 `bash -c "export PYTHONPATH=... && gunicorn ..."` 格式

### Q5: 本地修改后同步脚本不生效
**原因**：修改了app.py但Nginx路由到v3_app.py  
**解决**：修改 `/v3/` 页面必须改 **v3_app.py** 和 **v3_*.html**

---

## 6. 服务器信息

| 项目 | 值 |
|:---|:---|
| IP | 106.53.188.187 |
| 用户名 | ubuntu |
| 密码 | wenming.890503 |
| 部署路径 | /opt/ogd-collector-pro |
| Nginx配置 | /etc/nginx/sites-enabled/ogd-collector |
| systemd服务 | /etc/systemd/system/ogd-collector.service |
| gunicorn路径 | /home/ubuntu/.local/bin/gunicorn |
| Python site-packages | /home/ubuntu/.local/lib/python3.10/site-packages |

---

## 7. 修改页面指南

### 修改V3页面（/v3/xxx）
1. 修改 `templates/v3_xxx.html`
2. 如需新路由，修改 `v3_app.py` 添加 `@app.route('/xxx')`
3. 保存后运行 `ogd-sync.py`

### 修改旧版页面（/xxx）
1. 修改 `templates/xxx.html`
2. 如需新路由，修改 `app.py`
3. 保存后运行 `ogd-sync.py`（脚本会重启systemd服务）

### 修改静态文件（CSS/JS/图片）
1. 修改 `static/` 目录下文件
2. 保存后运行 `ogd-sync.py`
3. 强制刷新浏览器（Ctrl+F5）

---

## 8. 关键教训（2026-04-28排查总结）

1. **文件部署成功 ≠ 页面生效**：必须确保路由正确指向模板
2. **v3_app.py 和 app.py 是独立应用**：修改一个不影响另一个
3. **gunicorn重启命令语法敏感**：PYTHONPATH必须用bash -c export
4. **Nginx缓存30天**：static文件修改后可能需强制刷新
5. **三个端口独立管理**：5000(systemd)、5001(手动gunicorn)、5002(手动gunicorn)
