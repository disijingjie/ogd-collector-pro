import json
import sqlite3
import numpy as np
import pandas as pd
from scipy.linalg import eig

# 加载V3采集结果
with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
    v3_results = json.load(f)

dataset_counts = {}
for r in v3_results:
    if r['status'] == 'success' and r['dataset_count']:
        dataset_counts[r['code']] = r['dataset_count']

print(f'成功采集平台: {len(dataset_counts)}个')

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

df = pd.DataFrame(data)
print(f'分析数据: {len(df)}个平台')

# ========== 1. TOPSIS ==========
print('\n' + '='*60)
print('1. TOPSIS计算')
print('='*60)

indicators = ['has_api', 'has_search', 'has_download', 'has_visualization']
df['response_time_inv'] = 1 / (df['response_time'] / 1000)
indicators.append('response_time_inv')

X = df[indicators].values
X_norm = X / np.sqrt((X**2).sum(axis=0))
w = np.ones(len(indicators)) / len(indicators)
V = X_norm * w
V_pos = V.max(axis=0)
V_neg = V.min(axis=0)
d_pos = np.sqrt(((V - V_pos)**2).sum(axis=1))
d_neg = np.sqrt(((V - V_neg)**2).sum(axis=1))
df['topsis_score'] = d_neg / (d_pos + d_neg)
df['topsis_rank'] = df['topsis_score'].rank(ascending=False).astype(int)

print('TOPSIS排名TOP5:')
for _, row in df.sort_values('topsis_score', ascending=False).head(5).iterrows():
    print(f'  {row["name"]:10s}: {row["topsis_score"]:.4f}')

# ========== 2. DEA (简化版) ==========
print('\n' + '='*60)
print('2. DEA效率计算')
print('='*60)

# 输入: response_time (反转归一化)
# 输出: 功能指标总和 + dataset_count归一化
df['func_sum'] = df['has_api'] + df['has_search'] + df['has_download'] + df['has_visualization']
df['dataset_norm'] = df['dataset_count'] / df['dataset_count'].max()

# 简化DEA: 输出/输入比 (效率 = 功能总和*0.7 + 数据集数量*0.3) / 响应时间因子
df['efficiency'] = (df['func_sum'] / 4 * 0.7 + df['dataset_norm'] * 0.3) / (df['response_time'] / 3000)
df['efficiency'] = np.clip(df['efficiency'], 0, 1)  # 限制在0-1
df['dea_rank'] = df['efficiency'].rank(ascending=False).astype(int)

print('DEA效率TOP5:')
for _, row in df.sort_values('efficiency', ascending=False).head(5).iterrows():
    print(f'  {row["name"]:10s}: {row["efficiency"]:.4f}')

# ========== 3. DEMATEL ==========
print('\n' + '='*60)
print('3. DEMATEL影响因素分析')
print('='*60)

# 构建直接影响矩阵 (基于功能指标相关性)
X_dem = df[['has_api', 'has_search', 'has_download', 'has_visualization', 'dataset_count']].values
# 归一化
X_dem_norm = (X_dem - X_dem.min(axis=0)) / (X_dem.max(axis=0) - X_dem.min(axis=0) + 1e-10)
# 计算相关系数作为影响关系
corr = np.corrcoef(X_dem_norm.T)
# 确保对角线为0
np.fill_diagonal(corr, 0)
# 归一化到0-1
corr = np.abs(corr)
corr = corr / corr.max()

# 综合影响矩阵 T = C * (I - C)^-1
I = np.eye(corr.shape[0])
try:
    T = corr @ np.linalg.inv(I - corr)
except:
    T = corr  # 如果不可逆，使用原始矩阵

# 计算影响度(D)和被影响度(R)
D = T.sum(axis=1)  # 行和: 影响度
R = T.sum(axis=0)  # 列和: 被影响度

# 中心度(M)和原因度(N)
M = D + R  # 中心度
N = D - R  # 原因度

labels = ['API', 'Search', 'Download', 'Visualization', 'Dataset_Count']
print('DEMATEL分析结果:')
print(f'{"因素":<15} {"中心度":<10} {"原因度":<10} {"类型":<10}')
print('-' * 50)
for i, label in enumerate(labels):
    factor_type = '原因因素' if N[i] > 0 else '结果因素'
    print(f'{label:<15} {M[i]:<10.4f} {N[i]:<10.4f} {factor_type:<10}')

# ========== 4. fsQCA (简化版) ==========
print('\n' + '='*60)
print('4. fsQCA模糊集分析')
print('='*60)

# 将指标转换为模糊集 (0-1)
df['fs_api'] = df['has_api']
df['fs_search'] = df['has_search']
df['fs_download'] = df['has_download']
df['fs_vis'] = df['has_visualization']
df['fs_dataset'] = df['dataset_norm']

# 定义结果变量: TOPSIS得分高 = 1
df['fs_outcome'] = (df['topsis_score'] > df['topsis_score'].median()).astype(int)

# 真值表分析 (简化)
print('fsQCA真值表 (前8条):')
print(f'{'API':<5} {'Search':<7} {'Download':<9} {'Vis':<5} {'Dataset':<8} {'Outcome':<8} {'N':<5}')
print('-' * 55)

# 组合计数
from itertools import product
for combo in product([0, 1], repeat=5):
    api, search, download, vis, dataset = combo
    subset = df[(df['fs_api'] == api) & (df['fs_search'] == search) & 
                (df['fs_download'] == download) & (df['fs_vis'] == vis)]
    # dataset模糊化: >0.5为1
    subset = subset[(subset['fs_dataset'] > 0.5) == bool(dataset)]
    
    if len(subset) > 0:
        outcome = subset['fs_outcome'].mean()
        print(f'{api:<5} {search:<7} {download:<9} {vis:<5} {dataset:<8} {outcome:<8.2f} {len(subset):<5}')

# 保存所有结果
print('\n' + '='*60)
print('保存结果...')
df[['code', 'name', 'province', 'dataset_count', 'topsis_score', 'topsis_rank',
    'efficiency', 'dea_rank', 'func_sum']].to_csv('data/v3_all_methods_results.csv', index=False, encoding='utf-8-sig')
print('已保存: data/v3_all_methods_results.csv')

# 输出最终排名对比
print('\n' + '='*60)
print('最终排名对比')
print('='*60)
print(f'{'平台':<10} {'数据集':<10} {'TOPSIS':<8} {'DEA':<8} {'功能':<8}')
print('-' * 50)
for _, row in df.sort_values('topsis_score', ascending=False).iterrows():
    print(f'{row["name"]:<10} {row["dataset_count"]:<10,} {row["topsis_score"]:.4f}  {row["efficiency"]:.4f}  {row["func_sum"]:<8}')
