"""
V3 最终版可视化图表（基于22个样本+标准化数据+31省分类）
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 加载数据
with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# 加载TOPSIS结果
topsis_df = pd.read_csv('data/v3_topsis_results_v2.csv', encoding='utf-8-sig')

# 31省分类数据
province_categories = {
    '独立平台（正常运行）': ['北京', '上海', '江苏', '浙江', '福建', '江西', '山东', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '辽宁', '吉林', '内蒙古'],
    '独立平台（维护/转型）': ['河南', '云南', '安徽'],
    '登记/运营平台': ['河北', '山西'],
    '无独立平台（政务网）': ['黑龙江', '西藏', '陕西', '甘肃', '青海', '新疆'],
    '曾有平台（现关闭）': ['宁夏'],
}

# 颜色方案
colors = ['#2ecc71', '#f39c12', '#e74c3c', '#95a5a6', '#34495e']

print('开始生成图表...')

# 图1: 31省平台类型分布饼图
fig, ax = plt.subplots(figsize=(10, 8))
sizes = [len(v) for v in province_categories.values()]
labels = list(province_categories.keys())
explode = (0.05, 0.05, 0.05, 0.05, 0.05)

wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                    autopct='%1.1f%%', startangle=90, textprops={'fontsize': 11})
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax.set_title('31省数据平台建设类型分布', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('static/v3_final_01_province_types.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_final_01_province_types.png')

# 图2: 22省标准化数据集数量排名
fig, ax = plt.subplots(figsize=(14, 10))
df_sorted = topsis_df.sort_values('standardized_count', ascending=True)
y_pos = np.arange(len(df_sorted))

bars = ax.barh(y_pos, df_sorted['standardized_count'], color='#3498db', edgecolor='black', alpha=0.8)
ax.set_yticks(y_pos)
ax.set_yticklabels(df_sorted['name'], fontsize=10)
ax.set_xlabel('Standardized Dataset Count', fontsize=12)
ax.set_title('22省标准化数据集数量排名', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# 添加数值标签
for i, (idx, row) in enumerate(df_sorted.iterrows()):
    ax.text(row['standardized_count'] + 1000, i, f"{row['standardized_count']:,.0f}", 
            va='center', fontsize=9)

plt.tight_layout()
plt.savefig('static/v3_final_02_standardized_ranking.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_final_02_standardized_ranking.png')

# 图3: TOPSIS排名与标准化数量对比
fig, ax1 = plt.subplots(figsize=(14, 8))

df_plot = topsis_df.sort_values('topsis_score', ascending=False)
x_pos = np.arange(len(df_plot))

# 柱状图：标准化数量
bars = ax1.bar(x_pos, df_plot['standardized_count'], color='#3498db', alpha=0.7, label='Standardized Count')
ax1.set_xlabel('Province Rank', fontsize=12)
ax1.set_ylabel('Standardized Dataset Count', fontsize=12, color='#3498db')
ax1.tick_params(axis='y', labelcolor='#3498db')

# 折线图：TOPSIS得分
ax2 = ax1.twinx()
line = ax2.plot(x_pos, df_plot['topsis_score'], color='#e74c3c', marker='o', linewidth=2, markersize=6, label='TOPSIS Score')
ax2.set_ylabel('TOPSIS Score', fontsize=12, color='#e74c3c')
ax2.tick_params(axis='y', labelcolor='#e74c3c')
ax2.set_ylim(0, 1.1)

ax1.set_xticks(x_pos)
ax1.set_xticklabels(df_plot['name'], rotation=45, ha='right', fontsize=9)
ax1.set_title('TOPSIS排名与标准化数据集数量对比', fontsize=14, fontweight='bold')

# 图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.tight_layout()
plt.savefig('static/v3_final_03_topsis_vs_count.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_final_03_topsis_vs_count.png')

# 图4: 区域分布对比
region_map = {
    '北京': '东部', '天津': '东部', '上海': '东部', '江苏': '东部', '浙江': '东部', 
    '福建': '东部', '山东': '东部', '广东': '东部',
    '山西': '中部', '安徽': '中部', '江西': '中部', '河南': '中部', '湖北': '中部', '湖南': '中部',
    '内蒙古': '西部', '广西': '西部', '重庆': '西部', '四川': '西部', '贵州': '西部', '云南': '西部',
    '西藏': '西部', '陕西': '西部', '甘肃': '西部', '青海': '西部', '宁夏': '西部', '新疆': '西部',
    '辽宁': '东北', '吉林': '东北', '黑龙江': '东北', '河北': '东部'
}

topsis_df['region'] = topsis_df['name'].map(region_map)
region_stats = topsis_df.groupby('region').agg({
    'standardized_count': ['mean', 'sum', 'count'],
    'topsis_score': 'mean'
}).round(2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 左图：区域平均标准化数量
regions = region_stats.index
means = region_stats[('standardized_count', 'mean')]
ax1.bar(regions, means, color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'], edgecolor='black')
ax1.set_ylabel('Average Standardized Count', fontsize=12)
ax1.set_title('区域平均标准化数据集数量', fontsize=13, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# 右图：区域平台数量
counts = region_stats[('standardized_count', 'count')]
ax2.pie(counts.values, labels=counts.index, autopct='%1.0f%%', startangle=90,
        colors=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'])
ax2.set_title('区域平台数量分布', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('static/v3_final_04_region_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_final_04_region_comparison.png')

# 图5: 平台类型与绩效关系
fig, ax = plt.subplots(figsize=(12, 8))

# 根据平台类型着色
type_colors = []
for _, row in topsis_df.iterrows():
    if row['name'] in ['河南', '云南']:
        type_colors.append('#f39c12')  # 转型平台
    elif row['name'] in ['河北', '山西']:
        type_colors.append('#e74c3c')  # 登记平台
    else:
        type_colors.append('#2ecc71')  # 正常运行

scatter = ax.scatter(topsis_df['standardized_count'], topsis_df['topsis_score'], 
                    c=type_colors, s=100, alpha=0.7, edgecolors='black')

# 添加标签
for _, row in topsis_df.iterrows():
    ax.annotate(row['name'], (row['standardized_count'], row['topsis_score']), 
                xytext=(5, 5), textcoords='offset points', fontsize=9)

ax.set_xlabel('Standardized Dataset Count', fontsize=12)
ax.set_ylabel('TOPSIS Score', fontsize=12)
ax.set_title('平台类型与绩效关系散点图', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# 图例
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#2ecc71', label='正常运行平台'),
                   Patch(facecolor='#f39c12', label='转型平台'),
                   Patch(facecolor='#e74c3c', label='登记/运营平台')]
ax.legend(handles=legend_elements, loc='lower right')

plt.tight_layout()
plt.savefig('static/v3_final_05_type_vs_performance.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_final_05_type_vs_performance.png')

# 图6: DEA效率排名
fig, ax = plt.subplots(figsize=(14, 8))
dea_df = pd.read_csv('data/v3_dea_results.csv', encoding='utf-8-sig')
dea_sorted = dea_df.sort_values('dea_efficiency', ascending=False)

x_pos = np.arange(len(dea_sorted))
bars = ax.bar(x_pos, dea_sorted['dea_efficiency'], color='#9b59b6', edgecolor='black', alpha=0.8)
ax.set_xticks(x_pos)
ax.set_xticklabels(dea_sorted['name'], rotation=45, ha='right', fontsize=9)
ax.set_ylabel('DEA Efficiency', fontsize=12)
ax.set_title('22省DEA效率排名', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 0.6)

# 添加数值标签
for i, (idx, row) in enumerate(dea_sorted.iterrows()):
    ax.text(i, row['dea_efficiency'] + 0.01, f"{row['dea_efficiency']:.3f}", 
            ha='center', fontsize=8)

plt.tight_layout()
plt.savefig('static/v3_final_06_dea_ranking.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_final_06_dea_ranking.png')

# 图7: fsQCA组态分析
fig, ax = plt.subplots(figsize=(12, 8))

fsqca_df = pd.read_csv('data/v3_fsqca_results.csv', encoding='utf-8-sig')

# 构建热力图
conditions = ['pl', 'og', 'pc', 'dq', 'ae']
condition_labels = ['政策法规', '组织保障', '平台建设', '数据质量', '应用效果']

# 排序：高绩效在前
fsqca_sorted = fsqca_df.sort_values('op', ascending=False)

heatmap_data = fsqca_sorted[conditions].values
im = ax.imshow(heatmap_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)

ax.set_xticks(np.arange(len(conditions)))
ax.set_xticklabels(condition_labels, fontsize=11)
ax.set_yticks(np.arange(len(fsqca_sorted)))
ax.set_yticklabels(fsqca_sorted['name'], fontsize=10)

# 添加数值标签
for i in range(len(fsqca_sorted)):
    for j in range(len(conditions)):
        text = ax.text(j, i, heatmap_data[i, j], ha="center", va="center", 
                      color="black" if heatmap_data[i, j] == 1 else "white", fontsize=10)

ax.set_title('fsQCA条件组态分析（绿色=1，红色=0）', fontsize=14, fontweight='bold')
plt.colorbar(im, ax=ax, label='Condition Value')
plt.tight_layout()
plt.savefig('static/v3_final_07_fsqca_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_final_07_fsqca_heatmap.png')

# 图8: 综合仪表盘
fig = plt.figure(figsize=(16, 12))

# 子图1: 样本概况
ax1 = plt.subplot(3, 3, 1)
ax1.text(0.5, 0.7, '31', ha='center', va='center', fontsize=40, fontweight='bold', color='#2ecc71')
ax1.text(0.5, 0.4, '省级行政区', ha='center', va='center', fontsize=14)
ax1.text(0.5, 0.2, '22个有效样本', ha='center', va='center', fontsize=12, color='#e74c3c')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')
ax1.set_title('样本概况', fontsize=12, fontweight='bold')

# 子图2: 平台类型分布
ax2 = plt.subplot(3, 3, 2)
type_counts = [18, 3, 2, 6, 1]
type_labels = ['正常运行', '维护/转型', '登记/运营', '无独立平台', '已关闭']
ax2.pie(type_counts, labels=type_labels, autopct='%1.0f%%', startangle=90,
        colors=['#2ecc71', '#f39c12', '#e74c3c', '#95a5a6', '#34495e'])
ax2.set_title('平台类型分布', fontsize=12, fontweight='bold')

# 子图3: TOP3排名
ax3 = plt.subplot(3, 3, 3)
top3 = topsis_df.sort_values('topsis_score', ascending=False).head(3)
ax3.barh(range(3), top3['topsis_score'], color=['#FFD700', '#C0C0C0', '#CD7F32'])
ax3.set_yticks(range(3))
ax3.set_yticklabels(top3['name'])
ax3.set_xlabel('TOPSIS Score')
ax3.set_title('TOP3绩效排名', fontsize=12, fontweight='bold')
ax3.invert_yaxis()

# 子图4: 数据口径分布
ax4 = plt.subplot(3, 3, 4)
# 从原始数据获取口径分布
with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
    all_results = json.load(f)
success_results = [r for r in all_results if r['status'] == 'success']
type_dist = pd.Series([r['type'] for r in success_results]).value_counts()
ax4.pie(type_dist.values, labels=type_dist.index, autopct='%1.0f%%', startangle=90)
ax4.set_title('数据口径分布', fontsize=12, fontweight='bold')

# 子图5: 区域分布
ax5 = plt.subplot(3, 3, 5)
region_dist = topsis_df['region'].value_counts()
ax5.bar(region_dist.index, region_dist.values, color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'])
ax5.set_ylabel('Count')
ax5.set_title('区域分布', fontsize=12, fontweight='bold')
ax5.grid(axis='y', alpha=0.3)

# 子图6: 置信度分布
ax6 = plt.subplot(3, 3, 6)
conf_dist = pd.Series([r['confidence'] for r in success_results]).value_counts()
ax6.pie(conf_dist.values, labels=conf_dist.index, autopct='%1.0f%%', startangle=90,
        colors=['#2ecc71', '#f39c12', '#e74c3c'])
ax6.set_title('数据置信度分布', fontsize=12, fontweight='bold')

# 子图7: 标准化数量箱线图
ax7 = plt.subplot(3, 3, 7)
ax7.boxplot([topsis_df['standardized_count']], labels=['Standardized Count'])
ax7.set_ylabel('Count')
ax7.set_title('标准化数量分布', fontsize=12, fontweight='bold')
ax7.grid(axis='y', alpha=0.3)

# 子图8: TOPSIS vs DEA
ax8 = plt.subplot(3, 3, 8)
merged_df = topsis_df.merge(dea_df[['code', 'dea_efficiency']], on='code')
ax8.scatter(merged_df['topsis_score'], merged_df['dea_efficiency'], s=80, alpha=0.7, edgecolors='black')
ax8.set_xlabel('TOPSIS Score')
ax8.set_ylabel('DEA Efficiency')
ax8.set_title('TOPSIS vs DEA', fontsize=12, fontweight='bold')
ax8.grid(True, alpha=0.3)

# 子图9: 关键发现
ax9 = plt.subplot(3, 3, 9)
findings = [
    '1. 广东/山东/浙江领先',
    '2. 平台转型趋势明显',
    '3. 西部省份相对落后',
    '4. 数据口径差异大',
    '5. 18个平台正常运行'
]
ax9.text(0.1, 0.9, '关键发现:', fontsize=14, fontweight='bold', transform=ax9.transAxes)
for i, finding in enumerate(findings):
    ax9.text(0.1, 0.75 - i*0.12, finding, fontsize=11, transform=ax9.transAxes)
ax9.set_xlim(0, 1)
ax9.set_ylim(0, 1)
ax9.axis('off')
ax9.set_title('研究结论', fontsize=12, fontweight='bold')

plt.suptitle('OGD-Collector Pro V3 综合仪表盘', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('static/v3_final_08_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_final_08_dashboard.png')

print('\n所有图表生成完成！')
