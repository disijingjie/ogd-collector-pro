"""
基于最新真实数据重绘论文图表（V3最终版）
数据源：data/verified_dataset/2026-04-26最新计算结果
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 加载最新数据
RESULT_DATE = '20260426_003903'

with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
    collection_results = json.load(f)

topsis = pd.read_csv(f'data/verified_dataset/table_topsis_binary_{RESULT_DATE}.csv')
dea = pd.read_csv(f'data/verified_dataset/table_dea_{RESULT_DATE}.csv')

with open(f'data/verified_dataset/dematel_results_{RESULT_DATE}.json', 'r', encoding='utf-8') as f:
    dematel = json.load(f)

with open(f'data/verified_dataset/fsqca_results_{RESULT_DATE}.json', 'r', encoding='utf-8') as f:
    fsqca = json.load(f)

with open(f'data/verified_dataset/analysis_report_{RESULT_DATE}.json', 'r', encoding='utf-8') as f:
    analysis = json.load(f)

print('=' * 60)
print('基于真实数据重绘论文图表')
print('=' * 60)

# ========== 图1: 22省数据集数量排名（横向条形图） ==========
fig, ax = plt.subplots(figsize=(12, 10))

# 准备数据
df_plot = pd.DataFrame(collection_results)
df_plot = df_plot[df_plot['dataset_count'].notna()].copy()
df_plot = df_plot.sort_values('dataset_count', ascending=True)

y_pos = np.arange(len(df_plot))
colors_bar = ['#e74c3c' if c >= 50000 else '#f39c12' if c >= 10000 else '#3498db' if c >= 1000 else '#95a5a6' 
              for c in df_plot['dataset_count']]

bars = ax.barh(y_pos, df_plot['dataset_count'], color=colors_bar, edgecolor='black', alpha=0.85, height=0.7)
ax.set_yticks(y_pos)
ax.set_yticklabels(df_plot['name'], fontsize=11)
ax.set_xlabel('数据集/数据目录数量（个）', fontsize=13, fontweight='bold')
ax.set_title('图5-1  22个省级平台数据集数量排名', fontsize=15, fontweight='bold', pad=15)
ax.grid(axis='x', alpha=0.3, linestyle='--')

# 添加数值标签
for i, (idx, row) in enumerate(df_plot.iterrows()):
    ax.text(row['dataset_count'] + max(df_plot['dataset_count']) * 0.01, i, 
            f"{row['dataset_count']:,}", va='center', fontsize=9, fontweight='bold')

# 添加图例说明
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#e74c3c', label='≥50,000'),
                   Patch(facecolor='#f39c12', label='10,000-49,999'),
                   Patch(facecolor='#3498db', label='1,000-9,999'),
                   Patch(facecolor='#95a5a6', label='<1,000')]
ax.legend(handles=legend_elements, loc='lower right', fontsize=10)

plt.tight_layout()
plt.savefig('static/fig5_1_dataset_ranking.png', dpi=300, bbox_inches='tight')
plt.close()
print('[OK] fig5_1_dataset_ranking.png')

# ========== 图2: TOPSIS得分排名 ==========
fig, ax = plt.subplots(figsize=(12, 10))

topsis_sorted = topsis.sort_values('topsis_score', ascending=True)
y_pos = np.arange(len(topsis_sorted))

colors_topsis = ['#27ae60' if s >= 0.4 else '#f39c12' if s >= 0.18 else '#e74c3c' 
                 for s in topsis_sorted['topsis_score']]

bars = ax.barh(y_pos, topsis_sorted['topsis_score'], color=colors_topsis, edgecolor='black', alpha=0.85, height=0.7)
ax.set_yticks(y_pos)
ax.set_yticklabels(topsis_sorted['name'], fontsize=11)
ax.set_xlabel('TOPSIS综合绩效得分', fontsize=13, fontweight='bold')
ax.set_title('图5-2  基于熵权TOPSIS的省级平台绩效评估排名', fontsize=15, fontweight='bold', pad=15)
ax.grid(axis='x', alpha=0.3, linestyle='--')

# 添加阈值线
ax.axvline(x=0.18, color='gray', linestyle='--', alpha=0.7, linewidth=1.5)
ax.axvline(x=0.4, color='gray', linestyle='--', alpha=0.7, linewidth=1.5)
ax.text(0.18, len(topsis_sorted) - 0.5, '绩效门槛', fontsize=9, color='gray', ha='center')
ax.text(0.4, len(topsis_sorted) - 0.5, '高分门槛', fontsize=9, color='gray', ha='center')

# 数值标签
for i, (idx, row) in enumerate(topsis_sorted.iterrows()):
    ax.text(row['topsis_score'] + 0.01, i, f"{row['topsis_score']:.3f}", 
            va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('static/fig5_2_topsis_ranking.png', dpi=300, bbox_inches='tight')
plt.close()
print('[OK] fig5_2_topsis_ranking.png')

# ========== 图3: DEA效率值排名 ==========
fig, ax = plt.subplots(figsize=(12, 10))

dea_sorted = dea.sort_values('dea_efficiency', ascending=True)
y_pos = np.arange(len(dea_sorted))

colors_dea = ['#27ae60' if e >= 0.9 else '#f39c12' if e >= 0.7 else '#e74c3c' 
              for e in dea_sorted['dea_efficiency']]

bars = ax.barh(y_pos, dea_sorted['dea_efficiency'], color=colors_dea, edgecolor='black', alpha=0.85, height=0.7)
ax.set_yticks(y_pos)
ax.set_yticklabels(dea_sorted['name'], fontsize=11)
ax.set_xlabel('DEA-BCC效率值', fontsize=13, fontweight='bold')
ax.set_title('图5-3  省级平台DEA-BCC效率评估排名', fontsize=15, fontweight='bold', pad=15)
ax.grid(axis='x', alpha=0.3, linestyle='--')

# 有效前沿线
ax.axvline(x=1.0, color='red', linestyle='-', alpha=0.7, linewidth=2, label='效率前沿')
ax.legend(loc='lower right', fontsize=10)

# 数值标签
for i, (idx, row) in enumerate(dea_sorted.iterrows()):
    ax.text(row['dea_efficiency'] + 0.01, i, f"{row['dea_efficiency']:.3f}", 
            va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('static/fig5_3_dea_ranking.png', dpi=300, bbox_inches='tight')
plt.close()
print('[OK] fig5_3_dea_ranking.png')

# ========== 图4: DEMATEL因果关系图 ==========
fig, ax = plt.subplots(figsize=(10, 8))

center = np.array(dematel['center'])
cause = np.array(dematel['cause'])
dim_names = dematel['dimension_names']
colors_dematel = ['#e74c3c', '#3498db', '#f39c12', '#27ae60']

scatter = ax.scatter(cause, center, s=800, c=colors_dematel, alpha=0.7, edgecolors='black', linewidth=2, zorder=5)

for i, name in enumerate(dim_names):
    ax.annotate(name, (cause[i], center[i]), fontsize=12, fontweight='bold',
                ha='center', va='center', zorder=6)

# 添加象限分割线
ax.axhline(y=center.mean(), color='gray', linestyle='--', alpha=0.5, linewidth=1.5)
ax.axvline(x=cause.mean(), color='gray', linestyle='--', alpha=0.5, linewidth=1.5)

# 象限标注
ax.text(cause.min() - 0.5, center.max(), '原因因素\n（高影响度）', fontsize=10, ha='center', 
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax.text(cause.max() + 0.5, center.max(), '结果因素\n（高被影响度）', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

ax.set_xlabel('原因度（R - C）', fontsize=13, fontweight='bold')
ax.set_ylabel('中心度（R + C）', fontsize=13, fontweight='bold')
ax.set_title('图5-4  DEMATEL影响因素因果关系图', fontsize=15, fontweight='bold', pad=15)
ax.grid(alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('static/fig5_4_dematel_cause_effect.png', dpi=300, bbox_inches='tight')
plt.close()
print('[OK] fig5_4_dematel_cause_effect.png')

# ========== 图5: 区域对比箱线图 ==========
fig, ax = plt.subplots(figsize=(10, 7))

# 区域分组
regions = {
    '东部': ['beijing', 'shanghai', 'jiangsu', 'zhejiang', 'fujian', 'shandong', 'guangdong', 'hainan', 'tianjin'],
    '中部': ['shanxi', 'henan', 'hubei', 'hunan', 'jiangxi', 'anhui'],
    '西部': ['chongqing', 'sichuan', 'guizhou', 'yunnan', 'guangxi', 'gansu'],
    '东北': ['liaoning', 'jilin', 'heilongjiang']
}

region_data = []
region_labels = []
for region, codes in regions.items():
    vals = []
    for code in codes:
        row = topsis[topsis['code'] == code]
        if len(row) > 0:
            vals.append(row['topsis_score'].values[0])
    if vals:
        region_data.append(vals)
        region_labels.append(f"{region}\n(n={len(vals)})")

bp = ax.boxplot(region_data, labels=region_labels, patch_artist=True, 
                notch=True, showmeans=True, meanline=True)
colors_box = ['#3498db', '#e74c3c', '#f39c12', '#27ae60']
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

ax.set_ylabel('TOPSIS综合绩效得分', fontsize=13, fontweight='bold')
ax.set_title('图5-5  四大区域省级平台绩效对比', fontsize=15, fontweight='bold', pad=15)
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('static/fig5_5_region_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print('[OK] fig5_5_region_comparison.png')

# ========== 图6: 功能完善度雷达图（TOP5平台） ==========
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

top5 = topsis.nlargest(5, 'topsis_score')
indicators = ['has_api', 'has_bulk_download', 'has_search', 'has_download', 
              'has_visualization', 'has_update_info', 'has_metadata', 'has_feedback']
labels_cn = ['API接口', '批量下载', '搜索功能', '数据下载', 
             '可视化', '更新信息', '元数据', '用户反馈']

angles = np.linspace(0, 2 * np.pi, len(indicators), endpoint=False).tolist()
angles += angles[:1]

colors_radar = ['#e74c3c', '#3498db', '#f39c12', '#27ae60', '#9b59b6']
for idx, (_, row) in enumerate(top5.iterrows()):
    values = [row[ind] for ind in indicators]
    values += values[:1]
    ax.plot(angles, values, 'o-', linewidth=2, label=row['name'], color=colors_radar[idx])
    ax.fill(angles, values, alpha=0.1, color=colors_radar[idx])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels_cn, fontsize=11)
ax.set_ylim(0, 1.1)
ax.set_title('图5-6  TOPSIS绩效TOP5平台功能完善度雷达图', fontsize=15, fontweight='bold', pad=30)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)

plt.tight_layout()
plt.savefig('static/fig5_6_radar_top5.png', dpi=300, bbox_inches='tight')
plt.close()
print('[OK] fig5_6_radar_top5.png')

print()
print('=' * 60)
print('图表生成完成！共6张高质量图表')
print('保存位置: static/')
print('=' * 60)
