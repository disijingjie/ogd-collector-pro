#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新数据库中省级平台的URL
基于实际验证结果和开放数林指数权威数据
"""
import sys
import io
import os
import sqlite3
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

DB_PATH = Path(__file__).parent / "data" / "ogd_database.db"

# 基于验证结果和权威数据的URL更新
URL_UPDATES = [
    # (code, old_url, new_url, status, notes)
    ('guangdong', 'https://data.gd.gov.cn', 'https://gddata.gd.gov.cn', 'active', '域名修正，已验证可用'),
    ('anhui', 'https://data.ah.gov.cn', 'http://data.ahzwfw.gov.cn:8000', 'active', '域名修正，已验证可用'),
    ('jiangsu', 'https://data.jiangsu.gov.cn', 'https://data.jszwfw.gov.cn:8118/extranet/openportal/pages/default/index.html', 'active', '域名变更，已验证可用'),
    ('sichuan', 'https://data.sc.gov.cn', 'https://scdata.net.cn', 'active', '域名变更，已验证可用'),
    ('henan', 'https://data.henan.gov.cn', 'https://data.hnzwfw.gov.cn', 'active', '域名变更，已验证可用'),
    ('shanxi', 'https://data.shanxi.gov.cn', 'http://data.shanxi.gov.cn', 'active', 'http可用，https超时'),
]

# 基于开放数林指数2025年数据的平台状态标注
PLATFORM_STATUS = {
    # 有独立平台且已开放数据（24个省/自治区 + 4个直辖市 = 28个）
    'beijing': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'tianjin': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'shanghai': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025', 'note': 'WAF拦截，需Playwright突破'},
    'chongqing': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'jiangsu': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'zhejiang': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'anhui': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'fujian': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'jiangxi': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'shandong': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'hebei': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025', 'note': '指数存在但域名无法解析，可能整合进政务服务网'},
    'shanxi': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'neimenggu': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'henan': {'has_platform': True, 'has_data': False, 'source': '开放数林指数2025', 'note': '平台存在但数据层为0，可能未实际开放数据'},
    'hubei': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'hunan': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'guangdong': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'guangxi': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'hainan': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'sichuan': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'guizhou': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'yunnan': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'xizang': {'has_platform': False, 'has_data': False, 'source': '开放数林指数2025', 'note': '数据层为0，无独立平台'},
    'shaanxi': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025', 'note': '指数极低(0.02)，域名无法解析'},
    'gansu': {'has_platform': False, 'has_data': False, 'source': '开放数林指数2025', 'note': '数据层为0，无独立平台'},
    'qinghai': {'has_platform': False, 'has_data': False, 'source': '开放数林指数2025', 'note': '所有维度为0，无平台'},
    'ningxia': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025', 'note': '指数存在但域名无法解析'},
    'xinjiang': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025', 'note': '指数极低(0.06)，域名无法解析'},
    'liaoning': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'jilin': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025'},
    'heilongjiang': {'has_platform': True, 'has_data': True, 'source': '开放数林指数2025', 'note': '平台维护中'},
}

def update_urls():
    """更新平台URL"""
    if not DB_PATH.exists():
        print(f"[ERROR] 数据库不存在: {DB_PATH}")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    updated_count = 0
    skipped_count = 0
    
    print("=" * 80)
    print("平台URL更新")
    print("=" * 80)
    
    for code, old_url, new_url, status, notes in URL_UPDATES:
        # 检查当前URL
        cursor.execute("SELECT url, name FROM platforms WHERE code=?", (code,))
        row = cursor.fetchone()
        
        if not row:
            print(f"[SKIP] {code}: 平台不存在于数据库")
            skipped_count += 1
            continue
        
        current_url, name = row
        
        # 更新URL
        cursor.execute("UPDATE platforms SET url=? WHERE code=?", (new_url, code))
        if cursor.rowcount > 0:
            print(f"[UPDATE] {name}({code}): {current_url} -> {new_url}")
            print(f"         状态: {status} | 备注: {notes}")
            updated_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n更新完成: {updated_count}个平台已更新, {skipped_count}个跳过")
    return updated_count

def generate_status_report():
    """生成平台最终状态报告"""
    print("\n" + "=" * 80)
    print("31个省级平台最终状态确认报告")
    print("数据来源: 开放数林指数2025 + 实际网络验证")
    print("=" * 80)
    
    has_platform = [k for k, v in PLATFORM_STATUS.items() if v['has_platform']]
    no_platform = [k for k, v in PLATFORM_STATUS.items() if not v['has_platform']]
    has_data = [k for k, v in PLATFORM_STATUS.items() if v['has_data']]
    no_data = [k for k, v in PLATFORM_STATUS.items() if not v['has_data']]
    
    print(f"\n一、平台存在性统计")
    print(f"  有独立平台: {len(has_platform)}个")
    print(f"  无独立平台: {len(no_platform)}个")
    
    print(f"\n二、数据开放统计")
    print(f"  已开放数据: {len(has_data)}个")
    print(f"  未开放数据: {len(no_data)}个")
    
    print(f"\n三、无独立平台（{len(no_platform)}个）")
    for code in no_platform:
        info = PLATFORM_STATUS[code]
        print(f"  {code}: {info['note']}")
    
    print(f"\n四、有平台但未开放数据（{len(no_data)}个）")
    for code in no_data:
        info = PLATFORM_STATUS[code]
        print(f"  {code}: {info['note']}")
    
    print(f"\n五、论文研究可用样本估算")
    print(f"  理想情况（突破上海WAF）: {len(has_data)}个省级平台")
    print(f"  保守情况（上海无法突破）: {len(has_data) - 1}个省级平台")
    print(f"  加上4个直辖市: +4个")
    print(f"  加上13个副省级: +13个")
    print(f"  总样本量（保守）: {len(has_data) - 1 + 4 + 13}个")
    print(f"  总样本量（理想）: {len(has_data) + 4 + 13}个")

if __name__ == '__main__':
    update_urls()
    generate_status_report()
