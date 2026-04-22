# OGD-Collector Pro — Render 云部署指南

> Render 是一家美国云服务商，提供 **免费 Web Service** 托管。
> 优点：无需备案、注册简单、支持 GitHub 自动部署、有固定 HTTPS 域名。
> 缺点：免费版 15 分钟无访问会自动休眠，下次访问需 10-30 秒冷启动。

---

## 一、Render 是什么？适合我吗？

| 维度 | Render 免费版 | 腾讯云轻量 | cpolar |
|------|--------------|-----------|--------|
| **费用** | 免费 | ~90 元/年 | 免费 |
| **域名** | 自带 `xxx.onrender.com` | 需购买+备案 | 随机临时域名 |
| **备案** | ❌ 不需要 | ✅ 必须 | ❌ 不需要 |
| **访问速度** | 海外，国内一般 | 国内快 | 取决于你的带宽 |
| **稳定性** | 休眠机制，适合展示 | 长期稳定 | 你关机就断 |
| **HTTPS** | ✅ 自带 | 需配置证书 | ✅ cpolar 自带 |
| **推荐场景** | 给老师展示、论文附链接 | 正式长期运营 | 临时快速演示 |

**结论**：如果你需要给老师一个**长期可访问的 HTTPS 链接**，且**不想买服务器、不想备案**，Render 是最佳选择。

---

## 二、注册 Render 账号（2 分钟）

### 步骤 1：打开 Render 官网
访问 👉 **https://render.com**

### 步骤 2：点击右上角 "Get Started for Free"

### 步骤 3：选择 "Continue with GitHub"
> 强烈建议用 GitHub 登录，因为后续部署必须从 GitHub 仓库拉代码。

### 步骤 4：授权 Render 访问你的 GitHub
- 点击 "Authorize render"
- 默认授权即可，不需要改权限范围

### 步骤 5：完成注册
- 注册成功后进入 Dashboard（仪表盘）
- 右上角显示你的用户名，表示注册完成

---

## 三、将代码推送到 GitHub（5 分钟）

Render 只支持从 **GitHub/GitLab** 仓库部署，所以需要先把项目代码传上去。

### 步骤 1：在 GitHub 创建新仓库
1. 访问 👉 **https://github.com/new**
2. Repository name 填：`ogd-collector-pro`
3. Description 填：`三层架构政府数据开放平台采集与可视化系统`
4. 选择 **Public**（公开，免费；Private 需要付费计划）
5. 点击 **Create repository**

### 步骤 2：在本地初始化 Git 并推送

打开 PowerShell，进入项目目录：

```powershell
cd "c:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system"

# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: OGD-Collector Pro v2.0"

# 关联远程仓库（把下面的 YOUR_USERNAME 换成你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/ogd-collector-pro.git

# 推送代码
git push -u origin main
```

> 如果 `git push` 提示输入密码，需要输入 GitHub 的 **Personal Access Token**，不是你的登录密码。
> 获取方式：GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token

### 步骤 3：验证
打开 `https://github.com/YOUR_USERNAME/ogd-collector-pro`，应该能看到所有代码文件。

---

## 四、在 Render 上部署（3 分钟）

### 步骤 1：进入 Render Dashboard
访问 👉 **https://dashboard.render.com**

### 步骤 2：创建 Web Service
1. 点击蓝色按钮 **"New +"**
2. 选择 **"Web Service"**

### 步骤 3：连接 GitHub 仓库
1. 在列表中找到你的 `ogd-collector-pro` 仓库
2. 点击 **"Connect"**

### 步骤 4：配置部署参数
填写以下信息：

| 配置项 | 填写内容 |
|--------|----------|
| **Name** | `ogd-collector-pro`（或自定义） |
| **Region** | `Oregon (US West)`（默认即可） |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60` |

### 步骤 5：选择计划
- 选择 **Free**（免费）

### 步骤 6：添加环境变量（可选但建议）
点击 **"Advanced"** 展开，添加：
- `SECRET_KEY` → 点击 "Generate" 让 Render 自动生成
- `FLASK_ENV` → `production`

### 步骤 7：点击 "Create Web Service"
Render 会自动开始部署，大概需要 **2-3 分钟**。

---

## 五、部署完成后

### 查看状态
- 在 Render Dashboard 里，看到 
  - `Your service is live 🎉` → 部署成功
  - 下方会显示访问链接，如：`https://ogd-collector-pro.onrender.com`

### 访问你的系统
直接点击链接或用浏览器打开：
```
https://ogd-collector-pro.onrender.com
```

### 给老师发链接
直接复制这个 HTTPS 链接，微信发给导师即可，无需任何额外配置。

---

## 六、免费版限制须知

| 限制 | 说明 | 应对方法 |
|------|------|----------|
| **自动休眠** | 15 分钟无访问，实例休眠 | 首次访问慢（10-30秒），之后正常 |
| **每月时长** | 750 小时/月（足够） | 一个实例整月运行刚好 720 小时 |
| **磁盘不持久** | 实例重启后，上传/生成的文件丢失 | 数据库已配置自动重建，平台数据不会丢；采集记录会清空 |
| **带宽** | 100GB/月 | 展示用途完全够用 |

> **关于数据丢失**：免费版实例休眠后重启，SQLite 数据库文件会被重置。
> 但系统已配置自动初始化，平台基础数据（31省+13副省级+60地市）会自动重建。
> 如果希望保留采集记录作为演示，建议本地预先生成一份数据库快照，通过环境变量或外部存储恢复。

---

## 七、更新代码（后续迭代）

每次修改代码后，只需：

```powershell
cd "c:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system"
git add .
git commit -m "修复xxx问题"
git push origin main
```

Render 会自动检测到 GitHub 的更新并重新部署（约 1-2 分钟）。

---

## 八、常见问题

**Q1: 部署后页面报错 500？**
> 在 Render Dashboard → 你的 Service → Logs 里查看错误日志，通常是依赖包缺失或数据库初始化问题。

**Q2: 如何绑定自定义域名？**
> Dashboard → Settings → Custom Domains → 添加你的域名。国内域名仍需备案才能正常解析，海外域名（如 .com/.net）无需备案。

**Q3: 免费版够不够用？**
> 纯展示用途完全够用。如果需要 7×24 小时不间断采集、大流量访问、或数据持久化，再考虑升级付费计划（$7/月起）或迁移到腾讯云。

---

## 九、文件清单（已准备就绪）

以下文件已存在于项目中，确保推送时包含：

| 文件 | 作用 |
|------|------|
| `wsgi.py` | Gunicorn 入口文件 |
| `requirements.txt` | Python 依赖清单 |
| `render.yaml` | Render 部署配置文件（Blueprint） |
| `app.py` | Flask 主应用 |
| `models.py` | 数据库模型 |
| `collector_engine.py` | 采集引擎 |
| `data/` | SQLite 数据库目录 |
| `templates/` | HTML 模板 |
| `static/` | CSS/JS 静态资源 |

---

> 作者：文明（武汉大学信息管理学院博士生）
> 系统：OGD-Collector Pro v2.0
> 日期：2026-04-22
