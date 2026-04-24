"""
全面核对论文数据与实际计算的一致性
"""
import os, sys, re
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

def dea_bcc(topsis_df):
    df = topsis_df.copy()
    df['operating_years'] = 2026 - df['launch_year'] + 1
    df['function_score'] = df[BINARY_INDICATORS].sum(axis=1)
    n = len(df)
    efficiencies = []
    for i in range(n):
        x1 = df.iloc[i]['operating_years']
        x2 = df.iloc[i]['function_score']
        x3 = max(df.iloc[i]['dataset_count'], 1)
        y1 = df.iloc[i]['topsis_score']
        c = [1.0] + [0.0] * n
        A_ub = []
        b_ub = []
        A_ub.append([-x1] + df['operating_years'].tolist())
        b_ub.append(0)
        A_ub.append([-x2] + df['function_score'].tolist())
        b_ub.append(0)
        A_ub.append([-x3] + [max(v, 1) for v in df['dataset_count'].tolist()])
        b_ub.append(0)
        A_ub.append([0] + [-v for v in df['topsis_score'].tolist()])
        b_ub.append(-y1)
        A_eq = [[0] + [1.0] * n]
        b_eq = [1.0]
        bounds = [(0, None)] + [(0, None)] * n
        try:
            result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                           bounds=bounds, method='highs')
            theta = result.x[0] if result.success else 1.0
        except Exception:
            theta = 1.0
        efficiencies.append(theta)
    df['dea_efficiency'] = efficiencies
    return df

data = load_data()
print("=" * 80)
print("数据核实报告")
print("=" * 80)

# 1. dataset_count分布
print("\n【1】dataset_count分布（22个省级平台）")
non_zero = [d for d in data if d['dataset_count'] > 0]
zero = [d for d in data if d['dataset_count'] == 0]
print("  非零平台: %d个" % len(non_zero))
for d in non_zero:
    print("    %s: %d" % (d['name'], d['dataset_count']))
print("  为零平台: %d个" % len(zero))

# 2. TOPSIS计算
print("\n【2】TOPSIS实际计算结果（11项二值指标）")
df, w = topsis_binary_only(data)
for _, row in df.sort_values('topsis_score', ascending=False).iterrows():
    func = sum(row[k] for k in BINARY_INDICATORS)
    print("  排名%2d | %-8s | score=%.4f | func=%2d/11 | dc=%5d" % (
        int(row['topsis_rank']), row['name'], row['topsis_score'], func, row['dataset_count']))

# 3. 论文中声称的数据 vs 实际数据
print("\n【3】论文数据 vs 实际数据对比")
print("  %-8s | 论文得分 | 实际得分 | 论文排名 | 实际排名 | 差异" % "平台")
print("  " + "-" * 70)

# 论文中的数据（从表5-3提取）
thesis_data = {
    '北京市': (1.0000, 2), '辽宁省': (1.0000, 2), '内蒙古自治区': (1.0000, 2), '山东省': (1.0000, 2),
    '四川省': (0.7553, 5), '广西壮族自治区': (0.7553, 5),
    '海南省': (0.5463, 7), '湖南省': (0.5344, 8), '山西省': (0.5332, 9),
    '云南省': (0.4804, 10), '江苏省': (0.4297, 11), '天津市': (0.3905, 12),
    '河南省': (0.3767, 13), '重庆市': (0.3606, 14), '湖北省': (0.3464, 15),
    '浙江省': (0.3305, 16), '吉林省': (0.3284, 17), '广东省': (0.2509, 18),
    '江西省': (0.2479, 19), '福建省': (0.0514, 20), '贵州省': (0.0514, 20),
    '安徽省': (0.0232, 22),
}

for _, row in df.sort_values('topsis_score', ascending=False).iterrows():
    name = row['name']
    actual_score = row['topsis_score']
    actual_rank = int(row['topsis_rank'])
    if name in thesis_data:
        t_score, t_rank = thesis_data[name]
        score_diff = actual_score - t_score
        rank_diff = actual_rank - t_rank
        print("  %-8s | %8.4f | %8.4f | %8d | %8d | 得分%+7.4f 排名%+3d" % (
            name, t_score, actual_score, t_rank, actual_rank, score_diff, rank_diff))
    else:
        print("  %-8s | (论文未列) | %8.4f | (论文未列) | %8d |" % (name, actual_score, actual_rank))

# 4. 功能完善度核对
print("\n【4】各平台功能完善度（11项指标之和）")
for _, row in df.sort_values('topsis_score', ascending=False).iterrows():
    func = sum(row[k] for k in BINARY_INDICATORS)
    print("  %-8s: %2d/11" % (row['name'], int(func)))

# 5. DEA计算
print("\n【5】DEA效率计算结果")
df_dea = dea_bcc(df)
for _, row in df_dea.sort_values('dea_efficiency', ascending=False).iterrows():
    print("  %-8s | efficiency=%.4f | func=%2d | dc=%5d" % (
        row['name'], row['dea_efficiency'],
        sum(row[k] for k in BINARY_INDICATORS), row['dataset_count']))

print("\n" + "=" * 80)
print("核心问题总结：")
print("=" * 80)
print("1. 论文表5-3中的得分/排名与实际脚本计算结果完全不同")
print("2. 论文中'dataset_count权重0.3605'的描述与实际计算不符")
print("3. 论文中'四川44558'与实际数据库中四川dc=0不符")
print("4. 论文中'7个满分平台'与实际计算没有任何满分平台不符")
print("5. 需要基于实际计算结果重写论文中的数据表格和结论")
