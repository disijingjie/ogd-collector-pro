"""
检查论文计算与数据的一致性
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sqlite3
import numpy as np
import pandas as pd
from scipy.optimize import linprog
from pathlib import Path

DB_PATH = Path('data/ogd_database.db')
BINARY_INDICATORS = [
    'has_https', 'has_search', 'has_download', 'has_api',
    'has_visualization', 'has_update_info', 'has_metadata',
    'has_feedback', 'has_register', 'has_preview', 'has_bulk_download'
]

def load_data():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.code, p.name, p.region, p.launch_year,
               cr.has_https, cr.has_search, cr.has_download, cr.has_api,
               cr.has_visualization, cr.has_update_info, cr.has_metadata,
               cr.has_feedback, cr.has_register, cr.has_preview, cr.has_bulk_download,
               cr.dataset_count, cr.response_time, cr.collected_at
        FROM platforms p
        JOIN (
            SELECT platform_code, MAX(id) as max_id
            FROM collection_records
            WHERE status='available'
            GROUP BY platform_code
        ) latest ON p.code = latest.platform_code
        JOIN collection_records cr ON latest.max_id = cr.id
        WHERE p.tier = '省级'
        ORDER BY p.code
    """)
    rows = cursor.fetchall()
    data = []
    for r in rows:
        d = dict(r)
        for ind in BINARY_INDICATORS:
            d[ind] = int(d.get(ind, 0) or 0)
        d['dataset_count'] = int(d.get('dataset_count', 0) or 0)
        d['response_time'] = float(d.get('response_time', 0) or 0)
        d['launch_year'] = int(d.get('launch_year', 2018) or 2018)
        data.append(d)
    conn.close()
    return data

def topsis_binary_only(data):
    df = pd.DataFrame(data)
    n = len(df)
    X = df[BINARY_INDICATORS].values.astype(float)
    X_entropy = X + 0.001
    p = X_entropy / X_entropy.sum(axis=0)
    e = -np.sum(p * np.log(p), axis=0) / np.log(n)
    g = 1 - e
    w = g / g.sum()
    X_weighted = X * w
    V_plus = X_weighted.max(axis=0)
    V_minus = X_weighted.min(axis=0)
    D_plus = np.sqrt(((X_weighted - V_plus) ** 2).sum(axis=1))
    D_minus = np.sqrt(((X_weighted - V_minus) ** 2).sum(axis=1))
    C = D_minus / (D_plus + D_minus + 1e-10)
    df['topsis_score'] = C
    df['topsis_rank'] = df['topsis_score'].rank(ascending=False).astype(int)
    return df, w

def topsis_with_dataset_count(data):
    """包含dataset_count的TOPSIS（论文中描述的版本）"""
    df = pd.DataFrame(data)
    n = len(df)
    # 11个二值指标 + dataset_count + response_time
    indicators = BINARY_INDICATORS + ['dataset_count', 'response_time']
    X = df[indicators].copy()
    # 对dataset_count取对数（量纲差异太大）
    X['dataset_count'] = np.log1p(X['dataset_count'])
    # response_time取倒数（越小越好）
    X['response_time'] = 1.0 / (X['response_time'] + 0.1)
    X = X.values.astype(float)
    # 标准化
    X_norm = X / np.sqrt((X**2).sum(axis=0))
    # 熵权
    X_entropy = X_norm + 0.001
    p = X_entropy / X_entropy.sum(axis=0)
    e = -np.sum(p * np.log(p), axis=0) / np.log(n)
    g = 1 - e
    w = g / g.sum()
    X_weighted = X_norm * w
    V_plus = X_weighted.max(axis=0)
    V_minus = X_weighted.min(axis=0)
    D_plus = np.sqrt(((X_weighted - V_plus) ** 2).sum(axis=1))
    D_minus = np.sqrt(((X_weighted - V_minus) ** 2).sum(axis=1))
    C = D_minus / (D_plus + D_minus + 1e-10)
    df['topsis_score'] = C
    df['topsis_rank'] = df['topsis_score'].rank(ascending=False).astype(int)
    return df, w, indicators

data = load_data()
print("=" * 70)
print("加载了 %d 个省级平台" % len(data))
print("=" * 70)

# 统计dataset_count
non_zero = [d for d in data if d['dataset_count'] > 0]
zero = [d for d in data if d['dataset_count'] == 0]
print("\n=== dataset_count 分布 ===")
print("非零平台: %d 个" % len(non_zero))
for d in non_zero:
    print("  %s: %d" % (d['name'], d['dataset_count']))
print("为零平台: %d 个" % len(zero))
for d in zero:
    print("  %s: 0" % d['name'])

# 方案1: 仅用11个二值指标
print("\n" + "=" * 70)
print("方案1: 仅用11个二值指标计算TOPSIS")
print("=" * 70)
df1, w1 = topsis_binary_only(data)
print("\n权重分布:")
for ind, weight in zip(BINARY_INDICATORS, w1):
    print("  %-25s: %.4f" % (ind, weight))
print("\n排名:")
for _, row in df1.sort_values('topsis_score', ascending=False).iterrows():
    func = sum(row[k] for k in BINARY_INDICATORS)
    print("  %-8s | score=%.4f | rank=%2d | dc=%5d | func=%2d" % (
        row['name'], row['topsis_score'], int(row['topsis_rank']),
        row['dataset_count'], func))

# 方案2: 包含dataset_count
print("\n" + "=" * 70)
print("方案2: 11个二值指标 + dataset_count + response_time")
print("=" * 70)
df2, w2, inds2 = topsis_with_dataset_count(data)
print("\n权重分布:")
for ind, weight in zip(inds2, w2):
    print("  %-25s: %.4f" % (ind, weight))
print("\n排名:")
for _, row in df2.sort_values('topsis_score', ascending=False).iterrows():
    func = sum(row[k] for k in BINARY_INDICATORS)
    print("  %-8s | score=%.4f | rank=%2d | dc=%5d | func=%2d" % (
        row['name'], row['topsis_score'], int(row['topsis_rank']),
        row['dataset_count'], func))

# 排名对比
print("\n" + "=" * 70)
print("排名对比（方案1 vs 方案2）")
print("=" * 70)
merged = df1[['name', 'topsis_rank']].merge(
    df2[['name', 'topsis_score', 'topsis_rank']], on='name',
    suffixes=('_binary', '_with_dc'))
merged = merged.sort_values('topsis_rank_binary')
for _, row in merged.iterrows():
    diff = int(row['topsis_rank_with_dc']) - int(row['topsis_rank_binary'])
    arrow = "UP" if diff < 0 else ("DOWN" if diff > 0 else "SAME")
    print("  %-8s | 纯二值排名=%2d | 含DC排名=%2d | 变化=%+3d %s" % (
        row['name'], int(row['topsis_rank_binary']),
        int(row['topsis_rank_with_dc']), diff, arrow))

print("\n" + "=" * 70)
print("结论:")
print("=" * 70)
print("1. 实际计算脚本 topsis_binary_only 已经排除了 dataset_count")
print("2. 但论文正文中仍然引用了'dataset_count权重0.3605'等描述")
print("3. 论文中的排名数据需要与脚本计算结果核对一致性")
