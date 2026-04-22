#!/bin/bash
# =============================================================================
# OGD-Collector Pro — 腾讯云轻量服务器一键部署脚本
# 作者：文明（武汉大学信息管理学院博士生）
# 用法：以 root 身份执行  bash deploy.sh
# =============================================================================

set -e  # 遇到错误立即退出

echo "=========================================="
echo "OGD-Collector Pro 一键部署开始"
echo "=========================================="

# ---------------------------------------------------------------------------
# 1. 系统更新与基础依赖
# ---------------------------------------------------------------------------
echo "[1/8] 更新系统并安装基础依赖..."
apt-get update -y
apt-get upgrade -y
apt-get install -y \
    python3 python3-pip python3-venv \
    git nginx curl wget unzip \
    build-essential libssl-dev

# ---------------------------------------------------------------------------
# 2. 安装 Python 依赖（系统级，备用）
# ---------------------------------------------------------------------------
echo "[2/8] 升级 pip..."
pip3 install --upgrade pip setuptools wheel

# ---------------------------------------------------------------------------
# 3. 创建应用目录并拉取代码
# ---------------------------------------------------------------------------
echo "[3/8] 拉取项目代码..."
APP_DIR="/opt/ogd-collector-pro"
mkdir -p "$APP_DIR"

# 如果目录已存在且有代码，先备份
cd "$APP_DIR"
if [ -d ".git" ]; then
    echo "[INFO] 检测到已有代码，执行 git pull 更新..."
    git pull origin main
else
    # 用户需要替换为自己的 GitHub 仓库地址
    echo "[INFO] 首次克隆代码..."
    # 默认使用示例仓库，部署时请替换为实际地址
    git clone https://github.com/YOUR_USERNAME/ogd-collector-pro.git /tmp/ogd-temp
    cp -r /tmp/ogd-temp/* "$APP_DIR/"
    rm -rf /tmp/ogd-temp
fi

# ---------------------------------------------------------------------------
# 4. 创建 Python 虚拟环境并安装依赖
# ---------------------------------------------------------------------------
echo "[4/8] 创建虚拟环境并安装 Python 依赖..."
cd "$APP_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

# ---------------------------------------------------------------------------
# 5. 初始化数据库
# ---------------------------------------------------------------------------
echo "[5/8] 初始化 SQLite 数据库..."
python3 -c "from models import init_db, init_platforms_data; init_db(); init_platforms_data()"

# ---------------------------------------------------------------------------
# 6. 配置 systemd 服务（开机自启 + 崩溃重启）
# ---------------------------------------------------------------------------
echo "[6/8] 配置 systemd 服务..."

# 生成随机 SECRET_KEY
SECRET_KEY=$(openssl rand -hex 32)

cat > /etc/systemd/system/ogd-collector.service << EOF
[Unit]
Description=OGD-Collector Pro 三层架构采集系统
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
Environment="SECRET_KEY=$SECRET_KEY"
Environment="FLASK_ENV=production"
ExecStart=$APP_DIR/venv/bin/gunicorn wsgi:app \
    --bind 0.0.0.0:5000 \
    --workers 2 \
    --timeout 60 \
    --access-logfile $APP_DIR/logs/access.log \
    --error-logfile $APP_DIR/logs/error.log
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 创建日志目录
mkdir -p "$APP_DIR/logs"

# 重载 systemd
systemctl daemon-reload
systemctl enable ogd-collector

# ---------------------------------------------------------------------------
# 7. 配置 Nginx 反向代理
# ---------------------------------------------------------------------------
echo "[7/8] 配置 Nginx 反向代理..."

# 获取本机公网 IP（用于配置）
PUBLIC_IP=$(curl -s http://metadata.tencentyun.com/latest/meta-data/public-ipv4 || echo "YOUR_SERVER_IP")

cat > /etc/nginx/sites-available/ogd-collector << EOF
server {
    listen 80;
    server_name _;  # 使用 IP 访问，后续可改为域名

    client_max_body_size 64M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static {
        alias $APP_DIR/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 健康检查端点
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
}
EOF

# 启用站点
ln -sf /etc/nginx/sites-available/ogd-collector /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 测试并重载 Nginx
nginx -t
systemctl restart nginx
systemctl enable nginx

# ---------------------------------------------------------------------------
# 8. 启动应用
# ---------------------------------------------------------------------------
echo "[8/8] 启动 OGD-Collector Pro..."
systemctl start ogd-collector

sleep 3

# 检查服务状态
if systemctl is-active --quiet ogd-collector; then
    echo ""
    echo "=========================================="
    echo "✅ 部署成功！"
    echo "=========================================="
    echo ""
    echo "访问地址：http://$PUBLIC_IP"
    echo ""
    echo "常用命令："
    echo "  查看状态：systemctl status ogd-collector"
    echo "  查看日志：journalctl -u ogd-collector -f"
    echo "  重启服务：systemctl restart ogd-collector"
    echo "  停止服务：systemctl stop ogd-collector"
    echo ""
    echo "日志文件："
    echo "  访问日志：$APP_DIR/logs/access.log"
    echo "  错误日志：$APP_DIR/logs/error.log"
    echo "=========================================="
else
    echo ""
    echo "❌ 服务启动失败，请检查日志："
    echo "  journalctl -u ogd-collector -n 50"
    exit 1
fi
