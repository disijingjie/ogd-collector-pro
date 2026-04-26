#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复22个省级平台数据质量维度得分（score_c3）
"""

import sqlite3
import json
import pandas as pd

DB_PATH = 'data/ogd_database.db'
V3_PATH = 'data/v3_collection_results.json'

# 连接数据库
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 1. 查询所有省级平台（tier='省级'）的最新记录
print("=" * 110)
print("【1】所有省级平台最新维度得分现状")
print("=" * 110)
cursor.execute("""
    SELECT cr.platform_code, cr.platform_name, cr.dataset_count, 
           cr.score_c1, cr.score_c2, cr.score_c3, cr.score_c4,
           cr.has_api, cr.has_bulk_download, cr.has_metadata, cr.has_update_info,
           cr.has_feedback, cr.app_count,
           cr.has_search, cr.has_download, cr.has_visualization, cr.has_preview, cr.has_register,
           cr.collected_at
    FROM collection_records cr
    INNER JOIN platforms p ON cr.platform_code = p.code
    WHERE p.tier = '省级'
    ORDER BY cr.platform_code, cr.collected_at DESC
""")
rows = cursor.fetchall()

# 取每个平台的最新记录
latest = {}
for r in rows:
    code = r['platform_code']
    if code not in latest:
        latest[code] = r

print(f"{'平台':<12} {'名称':<14} {'数据集':>8} {'C1':>6} {'C2':>6} {'C3':>6} {'C4':>6} {'API':>4} {'批量':>4} {'元数据':>6} {'更新':>6} {'反馈':>6} {'app数':>6}")
print("-" * 105)
for code in sorted(latest.keys()):
    r = latest[code]
    print(f"{r['platform_code']:<12} {r['platform_name']:<14} {str(r['dataset_count']):>8} {str(r['score_c1']):>6} {str(r['score_c2']):>6} {str(r['score_c3']):>6} {str(r['score_c4']):>6} {str(r['has_api']):>4} {str(r['has_bulk_download']):>4} {str(r['has_metadata']):>6} {str(r['has_update_info']):>6} {str(r['has_feedback']):>6} {str(r['app_count']):>6}")

# 2. 统计缺失和为0的情况
print("\n" + "=" * 60)
print("【2】省级平台缺失统计")
print("=" * 60)
provincial_codes = set(latest.keys())
print(f"省级平台总数: {len(provincial_codes)}")

c3_zero_codes = [c for c, r in latest.items() if r['score_c3'] == 0]
print(f"score_c3为0的平台数: {len(c3_zero_codes)}")
print(f"score_c3为0的平台: {', '.join(sorted(c3_zero_codes))}")

missing_scores = [c for c, r in latest.items() if r['score_c1'] is None or r['score_c2'] is None or r['score_c3'] is None or r['score_c4'] is None]
print(f"缺失任一维度得分: {len(missing_scores)}")
if missing_scores:
    print(f"缺失平台: {', '.join(sorted(missing_scores))}")

# 3. 查看score_c3=0的平台功能字段详情
print("\n" + "=" * 60)
print("【3】score_c3=0的平台功能字段详情")
print("=" * 60)
for code in sorted(c3_zero_codes):
    r = latest[code]
    print(f"\n  {code} ({r['platform_name']}):")
    print(f"    数据集: {r['dataset_count']}, 元数据: {r['has_metadata']}, 更新信息: {r['has_update_info']}, API: {r['has_api']}, 批量下载: {r['has_bulk_download']}")
    print(f"    搜索: {r['has_search']}, 下载: {r['has_download']}, 可视化: {r['has_visualization']}, 预览: {r['has_preview']}, 注册: {r['has_register']}")
    print(f"    得分: C1={r['score_c1']}, C2={r['score_c2']}, C3={r['score_c3']}, C4={r['score_c4']}")

# 4. 读取v3_collection_results.json
print("\n" + "=" * 60)
print("【4】v3采集结果数据")
print("=" * 60)
with open(V3_PATH, 'r', encoding='utf-8') as f:
    v3_data = json.load(f)

v3_by_code = {item['code']: item for item in v3_data}
print(f"v3数据中的平台数: {len(v3_by_code)}")
for code in sorted(v3_by_code.keys()):
    item = v3_by_code[code]
    print(f"  {code:<12} {item['name']:<14} 数据集: {str(item['dataset_count']):>8} 类型: {item['type']} 置信度: {item['confidence']}")

# 5. 对比：哪些省级平台在v3中有数据但在数据库最新记录中score_c3=0
print("\n" + "=" * 60)
print("【5】对比分析：v3有数据但score_c3=0的平台")
print("=" * 60)
for code in sorted(c3_zero_codes):
    if code in v3_by_code:
        v3 = v3_by_code[code]
        r = latest[code]
        print(f"  {code:<12} v3数据集: {str(v3['dataset_count']):>8} | DB数据集: {str(r['dataset_count']):>8} | 元数据: {r['has_metadata']} | 更新: {r['has_update_info']}")

# 6. 列出所有省级平台（从platforms表）
print("\n" + "=" * 60)
print("【6】platforms表中所有省级平台")
print("=" * 60)
cursor.execute("SELECT code, name, province, region FROM platforms WHERE tier = '省级' ORDER BY code")
rows = cursor.fetchall()
for r in rows:
    print(f"  {r['code']:<12} {r['name']:<14} {r['province']:<10} {r['region']}")

# 7. 列出不在latest中的省级平台（即没有collection_records的）
print("\n" + "=" * 60)
print("【7】没有collection_records的省级平台")
print("=" * 60)
cursor.execute("SELECT code, name, province, region FROM platforms WHERE tier = '省级' ORDER BY code")
all_provincial = {r['code']: r for r in cursor.fetchall()}
missing_records = [c for c in all_provincial if c not in latest]
print(f"缺失记录的平台数: {len(missing_records)}")
for code in missing_records:
    r = all_provincial[code]
    print(f"  {code:<12} {r['name']:<14} {r['province']:<10} {r['region']}")

# 8. 核心问题分析：score_c3=0但has_metadata=1或has_update_info=1的平台
print("\n" + "=" * 60)
print("【8】核心问题：score_c3=0但has_metadata=1或has_update_info=1的平台")
print("=" * 60)
for code in sorted(c3_zero_codes):
    r = latest[code]
    if r['has_metadata'] == 1 or r['has_update_info'] == 1:
        print(f"  {code:<12} {r['platform_name']:<14} 元数据={r['has_metadata']} 更新={r['has_update_info']} score_c3={r['score_c3']}")

conn.close()
print("\n分析完成。")
