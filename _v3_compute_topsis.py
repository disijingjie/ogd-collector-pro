import json
import sqlite3
import numpy as np
import pandas as pd

# 加载V3采集结果
with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
    v3_results = json.load(f)

# 获取成功的平台
dataset_counts = {}
for r in v3_results:
    if r['status'] == 'success' and r['dataset_count']:
        dataset_counts[r['code']] = r['dataset_count']

print('=== V3数据集数量 ===')
for code, count in sorted(dataset_counts.items(), key=lambda x: x[1], reverse=True):
    print(f'  {code}: {count:,}')

# 从数据库加载其他指标
conn = sqlite3.connect('data/ogd_database.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT p.code, p.name, p.province, 
           cr.has_api, cr.has_search, cr.has_download, cr.has_visualization, cr.response_time
    FROM platforms p
    JOIN collection_records cr ON p.id = cr.platform_id
    WHERE cr.status = 'available'
    AND cr.collected_at = (SELECT MAX(collected_at) FROM collection_records cr2 WHERE cr2.platform_id = p.id)
''')

rows = cursor.fetchall()
conn.close()

print(f'\n数据库记录: {len(rows)}个平台')

# 构建分析数据
data = []
for row in rows:
    code, name, province, has_api, has_search, has_download, has_vis, rt = row
    if code in dataset_counts:
        data.append({
            'code': code,
            'name': name,
            'province': province,
            'dataset_count': dataset_counts[code],
            'has_api': 1 if has_api else 0,
            'has_search': 1 if has_search else 0,
            'has_download': 1 if has_download else 0,
            'has_visualization': 1 if has_vis else 0,
            'response_time': rt or 3000
        })

print(f'合并后数据: {len(data)}个平台')

# TOPSIS计算（仅使用功能指标，dataset_count作为参考不纳入权重）
df = pd.DataFrame(data)

# 功能指标
indicators = ['has_api', 'has_search', 'has_download', 'has_visualization']

# 响应时间反转（越小越好）
df['response_time_inv'] = 1 / (df['response_time'] / 1000)
indicators.append('response_time_inv')

# 标准化
X = df[indicators].values
X_norm = X / np.sqrt((X**2).sum(axis=0))

# 等权重
w = np.ones(len(indicators)) / len(indicators)

# 加权标准化
V = X_norm * w

# 理想解
V_pos = V.max(axis=0)
V_neg = V.min(axis=0)

# 距离
d_pos = np.sqrt(((V - V_pos)**2).sum(axis=1))
d_neg = np.sqrt(((V - V_neg)**2).sum(axis=1))

# TOPSIS得分
df['topsis_score'] = d_neg / (d_pos + d_neg)
df['topsis_rank'] = df['topsis_score'].rank(ascending=False).astype(int)

# 排序
df = df.sort_values('topsis_score', ascending=False)

print()
print('=== TOPSIS排名（基于功能指标） ===')
print(f'{"排名":<4} {"平台":<10} {"得分":<8} {"数据集数":<10} {"功能总和":<8}')
print('-' * 50)
for _, row in df.iterrows():
    func_sum = row['has_api'] + row['has_search'] + row['has_download'] + row['has_visualization']
    rank = row['topsis_rank']
    name = row['name']
    score = row['topsis_score']
    dc = row['dataset_count']
    print(f'{rank:<4} {name:<10} {score:.4f}   {dc:<10,} {func_sum:<8}')

# 保存结果
df[['code', 'name', 'province', 'dataset_count', 'topsis_score', 'topsis_rank']].to_csv('data/v3_topsis_results.csv', index=False, encoding='utf-8-sig')
print()
print('结果已保存到: data/v3_topsis_results.csv')
