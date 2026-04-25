"""
V3 全套计算方法（基于22个有效样本+标准化数据）
TOPSIS + DEA + DEMATEL + fsQCA
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime

# 加载采集结果
with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# 过滤成功平台
success_results = [r for r in results if r['status'] == 'success']
print(f'成功平台: {len(success_results)}个')

# 构建标准化数据
data = []
for r in success_results:
    code = r['code']
    name = r['name']
    original_count = r['dataset_count']
    data_type = r['type']
    
    # 转换系数
    conversion_map = {
        '数据集': 1.0,
        '数据目录': 0.8,
        '目录': 0.8,
        '开放目录': 0.8,
        '开放数据目录': 0.8,
        '数据产品': 0.5,
        '数据登记': 0.3,
        '数据目录(首批)': 0.5,
        '公共数据集': 1.0,
    }
    
    coef = conversion_map.get(data_type, 0.5)
    
    # 时间调整系数
    if '2023' in r.get('note', ''):
        time_coef = 0.8
    else:
        time_coef = 1.0
    
    standardized_count = original_count * coef * time_coef
    
    data.append({
        'code': code,
        'name': name,
        'original_count': original_count,
        'data_type': data_type,
        'conversion_coef': coef,
        'time_coef': time_coef,
        'standardized_count': standardized_count,
        'confidence': r['confidence'],
        'method': r['method'],
        'source_url': r['source_url'],
        'note': r['note']
    })

df = pd.DataFrame(data)

print('\n=== 标准化数据 ===')
print(f'{"排名":<4} {"平台":<12} {"原始数量":<10} {"类型":<12} {"转换系数":<8} {"标准化数量":<10}')
print('-' * 60)
for idx, row in df.sort_values('standardized_count', ascending=False).iterrows():
    rank_num = idx + 1
    name = row["name"]
    orig = row["original_count"]
    dtype = row["data_type"]
    coef = row["conversion_coef"]
    std = row["standardized_count"]
    print(f'{rank_num:<4} {name:<12} {orig:<10,} {dtype:<12} {coef:<8.1f} {std:<10.0f}')

# ============================================================
# TOPSIS计算
# ============================================================
print('\n\n=== TOPSIS计算 ===')

# 构建指标矩阵
# 指标1: 标准化数据集数量（效益型）
# 指标2: 置信度评分（高=1.0, 中=0.7, 低=0.4）
# 指标3: 平台类型评分（独立平台=1.0, 转型平台=0.7, 替代形式=0.4）

confidence_map = {'high': 1.0, 'medium': 0.7, 'low': 0.4}
platform_type_map = {
    'confirmed:homepage': 1.0,
    'confirmed:dataset_page': 1.0,
    'third_party:官方统计': 0.9,
    'third_party:政府发布会': 0.9,
    'third_party:官方报告': 0.9,
    'third_party:首批清单(2023年7月)': 0.6,
    'dataset_page:产品中心': 0.7,
    'dataset_page:登记中心': 0.7,
    'homepage:新URL访问': 1.0,
}

df['confidence_score'] = df['confidence'].map(confidence_map)
df['platform_type_score'] = df['method'].map(platform_type_map).fillna(0.5)

# 指标矩阵
indicators = ['standardized_count', 'confidence_score', 'platform_type_score']
X = df[indicators].values

# 标准化
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

print(f'{"排名":<4} {"平台":<12} {"TOPSIS得分":<12} {"标准化数量":<12} {"置信度":<8} {"平台类型":<10}')
print('-' * 60)
for idx, row in df.iterrows():
    rank = row["topsis_rank"]
    name = row["name"]
    score = row["topsis_score"]
    std = row["standardized_count"]
    conf = row["confidence"]
    ptype = row["platform_type_score"]
    print(f'{rank:<4} {name:<12} {score:<12.4f} {std:<12.0f} {conf:<8} {ptype:<10.1f}')

# 保存结果
df[['code', 'name', 'original_count', 'standardized_count', 'topsis_score', 'topsis_rank']].to_csv('data/v3_topsis_results_v2.csv', index=False, encoding='utf-8-sig')
print('\nTOPSIS结果已保存: data/v3_topsis_results_v2.csv')

# ============================================================
# DEA计算（简化版）
# ============================================================
print('\n\n=== DEA效率分析（简化版）===')

# 投入指标
# 投入1: 平台类型评分（作为建设投入代理变量）
# 投入2: 标准化数据集数量（作为数据归集投入）
# 产出指标
# 产出1: TOPSIS得分（作为开放效果代理变量）

df['dea_input1'] = df['platform_type_score']
df['dea_input2'] = df['standardized_count'] / df['standardized_count'].max()  # 归一化
df['dea_output'] = df['topsis_score']

# 简化DEA效率 = 产出 / (投入1 + 投入2)
df['dea_efficiency'] = df['dea_output'] / (df['dea_input1'] + df['dea_input2'] + 0.01)
df['dea_rank'] = df['dea_efficiency'].rank(ascending=False).astype(int)

print(f'{"排名":<4} {"平台":<12} {"DEA效率":<12} {"投入1":<8} {"投入2":<8} {"产出":<8}')
print('-' * 60)
for idx, row in df.sort_values('dea_efficiency', ascending=False).iterrows():
    rank = row["dea_rank"]
    name = row["name"]
    eff = row["dea_efficiency"]
    inp1 = row["dea_input1"]
    inp2 = row["dea_input2"]
    out = row["dea_output"]
    print(f'{rank:<4} {name:<12} {eff:<12.4f} {inp1:<8.2f} {inp2:<8.2f} {out:<8.4f}')

# 保存DEA结果
df[['code', 'name', 'dea_input1', 'dea_input2', 'dea_output', 'dea_efficiency', 'dea_rank']].to_csv('data/v3_dea_results.csv', index=False, encoding='utf-8-sig')
print('\nDEA结果已保存: data/v3_dea_results.csv')

# ============================================================
# DEMATEL计算（简化版）
# ============================================================
print('\n\n=== DEMATEL因果关系分析（简化版）===')

# 影响因素
factors = ['政策法规', '组织保障', '平台建设', '数据质量', '应用效果']

# 构建直接影响矩阵（基于专家打分简化版）
# 使用平台数据作为代理变量
n_factors = len(factors)

# 简化：使用相关性构建关系矩阵
corr_matrix = np.corrcoef(df[['standardized_count', 'confidence_score', 'platform_type_score', 'topsis_score', 'dea_efficiency']].values.T)

# 归一化到0-1
direct_matrix = (corr_matrix + 1) / 2
np.fill_diagonal(direct_matrix, 0)

# 计算综合影响矩阵
I = np.eye(n_factors)
T = direct_matrix @ np.linalg.inv(I - direct_matrix)

# 计算中心度和原因度
R = T.sum(axis=1)  # 影响度
C = T.sum(axis=0)  # 被影响度
D = R + C  # 中心度
E = R - C  # 原因度

print(f'{"因素":<12} {"中心度":<10} {"原因度":<10} {"类型":<10}')
print('-' * 50)
for i, factor in enumerate(factors):
    factor_type = '原因因素' if E[i] > 0 else '结果因素'
    print(f'{factor:<12} {D[i]:<10.4f} {E[i]:<10.4f} {factor_type:<10}')

# 保存DEMATEL结果
dematel_results = pd.DataFrame({
    'factor': factors,
    'centrality': D,
    'causality': E,
    'type': ['原因因素' if e > 0 else '结果因素' for e in E]
})
dematel_results.to_csv('data/v3_dematel_results.csv', index=False, encoding='utf-8-sig')
print('\nDEMATEL结果已保存: data/v3_dematel_results.csv')

# ============================================================
# fsQCA计算（简化版）
# ============================================================
print('\n\n=== fsQCA组态分析（简化版）===')

# 条件变量校准
df['pl'] = (df['standardized_count'] > df['standardized_count'].median()).astype(int)  # 政策法规代理
df['og'] = (df['platform_type_score'] > 0.7).astype(int)  # 组织保障代理
df['pc'] = (df['platform_type_score'] > 0.7).astype(int)  # 平台建设代理
df['dq'] = (df['confidence_score'] > 0.7).astype(int)  # 数据质量代理
df['ae'] = (df['topsis_score'] > df['topsis_score'].median()).astype(int)  # 应用效果代理

# 结果变量
df['op'] = (df['topsis_score'] > df['topsis_score'].median()).astype(int)  # 开放绩效

# 组态分析
configs = df[['pl', 'og', 'pc', 'dq', 'ae', 'op']].values

# 统计各组态
from itertools import product
all_configs = list(product([0, 1], repeat=5))

print('高绩效组态（OP=1）:')
high_perf = df[df['op'] == 1][['name', 'pl', 'og', 'pc', 'dq', 'ae', 'topsis_score']]
print(high_perf.to_string(index=False))

print('\n低绩效组态（OP=0）:')
low_perf = df[df['op'] == 0][['name', 'pl', 'og', 'pc', 'dq', 'ae', 'topsis_score']]
print(low_perf.to_string(index=False))

# 保存fsQCA结果
df[['code', 'name', 'pl', 'og', 'pc', 'dq', 'ae', 'op', 'topsis_score']].to_csv('data/v3_fsqca_results.csv', index=False, encoding='utf-8-sig')
print('\nfsQCA结果已保存: data/v3_fsqca_results.csv')

print('\n\n=== 所有计算完成 ===')
print(f'有效样本: {len(df)}个平台')
print(f'TOPSIS排名TOP3: {df.sort_values("topsis_score", ascending=False).head(3)["name"].tolist()}')
print(f'DEA效率TOP3: {df.sort_values("dea_efficiency", ascending=False).head(3)["name"].tolist()}')
