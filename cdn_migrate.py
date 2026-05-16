#!/usr/bin/env python3
"""
OGD-Collector Pro 静态资源CDN迁移脚本
将大文件（PDF/图片）迁移到腾讯云COS，Nginx反向代理

前置条件：
1. 安装cos-python-sdk-v5: pip install cos-python-sdk-v5
2. 配置腾讯云COS密钥（SecretId/SecretKey）
3. 创建COS Bucket

用法:
  python cdn_migrate.py --check        # 检查哪些文件需要迁移
  python cdn_migrate.py --migrate      # 执行迁移
  python cdn_migrate.py --nginx-config  # 生成Nginx反向代理配置
"""

import os
import sys
import json
from pathlib import Path

# 配置
PROJECT_PATH = Path(r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system")
STATIC_PATH = PROJECT_PATH / "static"
CDN_CONFIG_FILE = PROJECT_PATH / "data" / "cdn_config.json"

# 腾讯云COS配置（需要填写）
COS_SECRET_ID = os.environ.get('COS_SECRET_ID', '')
COS_SECRET_KEY = os.environ.get('COS_SECRET_KEY', '')
COS_REGION = 'ap-guangzhou'
COS_BUCKET = 'ogd-collector-pro-1250000000'  # 需替换为实际Bucket
CDN_DOMAIN = f'{COS_BUCKET}.cos.{COS_REGION}.myqcloud.com'

# 需要迁移的文件类型和大小阈值
MIGRATE_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.gif', '.svg'}
MIGRATE_SIZE_THRESHOLD = 500 * 1024  # 500KB以上才迁移

def check_files():
    """检查需要迁移的文件"""
    files = []
    total_size = 0

    for root, dirs, filenames in os.walk(STATIC_PATH):
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext in MIGRATE_EXTENSIONS:
                fpath = os.path.join(root, fname)
                fsize = os.path.getsize(fpath)
                if fsize > MIGRATE_SIZE_THRESHOLD:
                    rel_path = os.path.relpath(fpath, PROJECT_PATH).replace('\\', '/')
                    files.append({
                        'path': rel_path,
                        'size': fsize,
                        'size_mb': round(fsize / 1024 / 1024, 1),
                        'cdn_url': f'https://{CDN_DOMAIN}/{rel_path}'
                    })
                    total_size += fsize

    print(f"需要迁移的文件: {len(files)} 个")
    print(f"总大小: {total_size / 1024 / 1024:.1f} MB")
    print()

    for f in sorted(files, key=lambda x: -x['size'])[:20]:
        print(f"  {f['size_mb']:>6.1f} MB  {f['path']}")

    return files

def generate_nginx_config(files):
    """生成Nginx反向代理配置"""
    print("\n=== Nginx CDN反向代理配置 ===")
    print("在 /etc/nginx/sites-available/ogd-collector 的 server 块中添加：\n")

    # PDF文件走CDN
    print(f"    # PDF文件走COS CDN")
    print(f"    location /static/fulltext/ {{")
    print(f"        proxy_pass https://{CDN_DOMAIN}/static/fulltext/;")
    print(f"        proxy_set_header Host {CDN_DOMAIN};")
    print(f"        expires 30d;")
    print(f"    }}")
    print()

    # 大图片走CDN
    print(f"    # 大图片走COS CDN")
    print(f"    location /static/thesis_charts_v7/ {{")
    print(f"        proxy_pass https://{CDN_DOMAIN}/static/thesis_charts_v7/;")
    print(f"        proxy_set_header Host {CDN_DOMAIN};")
    print(f"        expires 30d;")
    print(f"    }}")

def migrate_to_cos(files):
    """迁移文件到COS"""
    if not COS_SECRET_ID or not COS_SECRET_KEY:
        print("❌ 缺少腾讯云COS密钥！")
        print("请设置环境变量 COS_SECRET_ID 和 COS_SECRET_KEY")
        return

    try:
        from qcloud_cos import CosConfig, CosS3Client
    except ImportError:
        print("❌ 请先安装COS SDK: pip install cos-python-sdk-v5")
        return

    config = CosConfig(Region=COS_REGION, SecretId=COS_SECRET_ID, SecretKey=COS_SECRET_KEY)
    client = CosS3Client(config)

    success = 0
    for f in files:
        local_path = os.path.join(PROJECT_PATH, f['path'])
        cos_key = f['path']
        try:
            client.upload_file(Bucket=COS_BUCKET, Key=cos_key, LocalFilePath=local_path)
            print(f"✓ 上传: {f['path']}")
            success += 1
        except Exception as e:
            print(f"✗ 失败: {f['path']} - {e}")

    print(f"\n迁移完成: {success}/{len(files)}")

    # 保存CDN配置
    cdn_config = {
        'cdn_domain': CDN_DOMAIN,
        'migrated_files': [f['path'] for f in files],
        'migrated_at': str(Path.cwd()),
        'total_size_mb': sum(f['size'] for f in files) / 1024 / 1024
    }
    with open(CDN_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(cdn_config, f, ensure_ascii=False, indent=2)
    print(f"CDN配置已保存到: {CDN_CONFIG_FILE}")

def main():
    if len(sys.argv) < 2:
        print("用法: python cdn_migrate.py --check|--migrate|--nginx-config")
        return

    files = check_files()

    arg = sys.argv[1]
    if arg == '--check':
        pass  # already checked above
    elif arg == '--migrate':
        migrate_to_cos(files)
    elif arg == '--nginx-config':
        generate_nginx_config(files)
    else:
        print(f"未知参数: {arg}")

if __name__ == '__main__':
    main()
