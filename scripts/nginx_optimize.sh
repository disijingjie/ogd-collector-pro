#!/bin/bash
# OGD-Collector Pro Nginx优化脚本
# 1. 静态资源长期缓存 2. Gzip压缩 3. PDF等大文件缓存策略

NGINX_CONF="/etc/nginx/sites-available/ogd-collector"

# 检查当前Nginx配置
echo "=== 当前Nginx配置 ==="
cat $NGINX_CONF

# 更新Nginx配置（在server块中添加）
echo ""
echo "=== 建议在server块中添加的配置 ==="
cat << 'EOF'

    # 静态资源长期缓存
    location ~* ^/static/(thesis_charts|data|css|js|img)/ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # PDF文件单独缓存（7天）
    location ~* ^/static/fulltext/.*\.pdf$ {
        expires 7d;
        add_header Cache-Control "public";
        access_log off;
    }

    # 模板相关静态（短期缓存）
    location ~* ^/static/ {
        expires 7d;
        add_header Cache-Control "public";
    }

EOF

echo ""
echo "如需应用，请手动编辑 $NGINX_CONF 并执行 sudo nginx -t && sudo systemctl reload nginx"
