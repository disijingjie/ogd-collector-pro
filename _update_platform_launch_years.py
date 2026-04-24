#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新省级平台上线年份数据
数据来源：用户提供的各省级政府数据开放平台上线时间
"""
import sys
import io
import os
import sqlite3
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

DB_PATH = Path(__file__).parent / "data" / "ogd_database.db"

# 用户提供的省级平台上线年份数据
# 格式: (省份编码, 上线年份)
LAUNCH_YEARS = [
    # 2015年
    ('zhejiang', 2015),
    # 2016年
    ('guangdong', 2016),
    ('guizhou', 2016),
    # 2018年
    ('henan', 2018),
    ('jiangxi', 2018),
    ('ningxia', 2018),
    ('shandong', 2018),
    ('shaanxi', 2018),
    # 2019年
    ('fujian', 2019),
    ('hainan', 2019),
    ('jiangsu', 2019),
    ('sichuan', 2019),
    ('xinjiang', 2019),
    # 2020年
    ('guangxi', 2020),
    ('hubei', 2020),
    ('hunan', 2020),
    ('qinghai', 2020),
    # 2023年
    ('anhui', 2023),
    ('gansu', 2023),
    ('hebei', 2023),
    # 2024年
    ('liaoning', 2024),
    # 2025年
    ('shanxi', 2025),
    # 未标注年份（根据开放数林指数推断为早期或近年）
    # 黑龙江、内蒙古、吉林、云南 - 未标注具体年份
]

# 直辖市上线年份（公开资料）
MUNICIPALITY_YEARS = [
    ('beijing', 2016),    # 北京政务数据资源网
    ('shanghai', 2015),   # 上海公共数据开放平台（2015年5月上线）
    ('tianjin', 2017),    # 天津信息资源统一开放平台
    ('chongqing', 2017),  # 重庆市政府数据开放平台
]

def update_launch_years():
    """更新平台上线年份到数据库"""
    if not DB_PATH.exists():
        print(f"[ERROR] 数据库不存在: {DB_PATH}")
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # 检查platforms表是否有launch_year字段，没有则添加
    cursor.execute("PRAGMA table_info(platforms)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'launch_year' not in columns:
        cursor.execute("ALTER TABLE platforms ADD COLUMN launch_year INTEGER")
        print("[INFO] 已添加 launch_year 字段到 platforms 表")
    
    # 更新所有上线年份
    all_updates = LAUNCH_YEARS + MUNICIPALITY_YEARS
    updated = 0
    not_found = []
    
    print("=" * 60)
    print("更新省级平台上线年份")
    print("=" * 60)
    
    for code, year in all_updates:
        cursor.execute("UPDATE platforms SET launch_year=? WHERE code=?", (year, code))
        if cursor.rowcount > 0:
            # 获取名称
            cursor.execute("SELECT name FROM platforms WHERE code=?", (code,))
            row = cursor.fetchone()
            name = row[0] if row else code
            print(f"  {name}({code}): {year}年")
            updated += 1
        else:
            not_found.append(code)
    
    conn.commit()
    conn.close()
    
    print(f"\n更新完成: {updated}个平台已更新")
    if not_found:
        print(f"未找到: {', '.join(not_found)}")
    
    return updated

def generate_timeline_analysis():
    """生成平台发展历程时序分析"""
    print("\n" + "=" * 60)
    print("省级政府数据开放平台发展历程分析")
    print("=" * 60)
    
    all_data = LAUNCH_YEARS + MUNICIPALITY_YEARS
    
    # 按年份分组
    from collections import defaultdict
    year_map = defaultdict(list)
    for code, year in all_data:
        year_map[year].append(code)
    
    # 累计统计
    cumulative = 0
    print("\n一、逐年上线平台数量")
    print("-" * 40)
    for year in sorted(year_map.keys()):
        count = len(year_map[year])
        cumulative += count
        provinces = ', '.join(year_map[year])
        print(f"  {year}年: {count}个 ({provinces})")
    
    print(f"\n总计: {len(all_data)}个省级平台有明确上线年份")
    
    # 阶段划分（基于上线时间）
    print("\n二、发展阶段划分")
    print("-" * 40)
    
    stages = [
        ("萌芽期", 2015, 2016, "首批平台上线，浙江、广东、贵州先行探索"),
        ("扩散期", 2017, 2019, "平台数量快速增长，华东、华南、西南集中上线"),
        ("规范期", 2020, 2022, "国家层面政策推动，中西部地区跟进"),
        ("深化期", 2023, 2025, "平台整合与质量提升，部分地区调整域名或并入政务服务网"),
    ]
    
    for stage_name, start, end, desc in stages:
        stage_codes = [c for c, y in all_data if start <= y <= end]
        print(f"  {stage_name} ({start}-{end}): {len(stage_codes)}个")
        print(f"    {desc}")
        if stage_codes:
            print(f"    包含: {', '.join(stage_codes)}")
    
    # 未标注年份的平台
    no_year = ['heilongjiang', 'neimenggu', 'jilin', 'yunnan']
    print(f"\n三、未明确标注上线年份的平台")
    print("-" * 40)
    print(f"  黑龙江、内蒙古、吉林、云南")
    print(f"  （根据开放数林指数，这些平台存在但具体上线时间待确认）")
    
    # 论文可用数据
    print("\n四、论文时序分析数据")
    print("-" * 40)
    print("  可用于：")
    print("  1. 平台发展历程描述（第一章背景/第三章现状）")
    print("  2. 阶段性特征与政策节点关联分析")
    print("  3. 上线早晚与平台质量相关性分析")

if __name__ == '__main__':
    update_launch_years()
    generate_timeline_analysis()
