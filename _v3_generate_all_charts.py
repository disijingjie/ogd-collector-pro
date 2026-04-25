import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 加载数据
with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

df = pd.read_csv('data/v3_topsis_results.csv', encoding='utf-8-sig')

# 只保留成功采集的平台
success_results = [r for r in results if r['status'] == 'success']

print(f'生成图表: {len(success_results)}个平台')

# 图1: 数据集数量排名柱状图（横向）
fig, ax = plt.subplots(figsize=(14, 8))
df_sorted = df.sort_values('dataset_count', ascending=True)
colors = plt.cm.Spectral(np.linspace(0.1, 0.9, len(df_sorted)))
bars = ax.barh(df_sorted['name'], df_sorted['dataset_count'], color=colors)
ax.set_xlabel('Dataset Count', fontsize=12)
ax.set_title('V3 Provincial OGD Platforms - Dataset Count Ranking (18 Platforms)', fontsize=14, fontweight='bold')
for i, (name, count) in enumerate(zip(df_sorted['name'], df_sorted['dataset_count'])):
    ax.text(count + 1000, i, f'{int(count):,}', va='center', fontsize=9)
ax.set_xlim(0, max(df_sorted['dataset_count']) * 1.15)
plt.tight_layout()
plt.savefig('static/v3_chart_01_dataset_ranking.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_01_dataset_ranking.png')

# 图2: TOPSIS得分排名
fig, ax = plt.subplots(figsize=(14, 8))
df_sorted2 = df.sort_values('topsis_score', ascending=True)
colors2 = ['#2ecc71' if s > 0.7 else '#f39c12' if s > 0.5 else '#e74c3c' for s in df_sorted2['topsis_score']]
bars = ax.barh(df_sorted2['name'], df_sorted2['topsis_score'], color=colors2)
ax.set_xlabel('TOPSIS Score', fontsize=12)
ax.set_title('V3 TOPSIS Score Ranking (17 Platforms)', fontsize=14, fontweight='bold')
ax.axvline(x=0.7, color='green', linestyle='--', alpha=0.5)
ax.axvline(x=0.5, color='orange', linestyle='--', alpha=0.5)
for i, (name, score) in enumerate(zip(df_sorted2['name'], df_sorted2['topsis_score'])):
    ax.text(score + 0.01, i, f'{score:.3f}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('static/v3_chart_02_topsis_ranking.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_02_topsis_ranking.png')

# 图3: 数据集数量分布箱线图
fig, ax = plt.subplots(figsize=(10, 6))
ax.boxplot([df['dataset_count']], labels=['Dataset Count'])
ax.set_ylabel('Count', fontsize=12)
ax.set_title('Dataset Count Distribution (Box Plot)', fontsize=14, fontweight='bold')
ax.set_yscale('log')
plt.tight_layout()
plt.savefig('static/v3_chart_03_boxplot.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_03_boxplot.png')

# 图4: 数据集数量饼图（前5+其他）
fig, ax = plt.subplots(figsize=(10, 10))
df_pie = df.sort_values('dataset_count', ascending=False)
top5 = df_pie.head(5)
others = pd.DataFrame([{'name': 'Others', 'dataset_count': df_pie.iloc[5:]['dataset_count'].sum()}])
pie_data = pd.concat([top5[['name', 'dataset_count']], others])
colors_pie = plt.cm.Set3(np.linspace(0, 1, len(pie_data)))
wedges, texts, autotexts = ax.pie(pie_data['dataset_count'], labels=pie_data['name'], autopct='%1.1f%%', 
                                   colors=colors_pie, startangle=90)
ax.set_title('Dataset Count Share - Top 5 + Others', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('static/v3_chart_04_pie.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_04_pie.png')

# 图5: 区域对比（东部/中部/西部/东北）
region_map = {
    '北京': '东部', '天津': '东部', '上海': '东部', '江苏': '东部', '浙江': '东部', '福建': '东部', '山东': '东部', '广东': '东部',
    '山西': '中部', '安徽': '中部', '江西': '中部', '河南': '中部', '湖北': '中部', '湖南': '中部',
    '内蒙古': '西部', '广西': '西部', '重庆': '西部', '四川': '西部', '贵州': '西部', '云南': '西部',
    '辽宁': '东北', '吉林': '东北', '黑龙江': '东北'
}
df['region'] = df['province'].map(region_map)
region_stats = df.groupby('region').agg({
    'dataset_count': ['mean', 'sum', 'count']
}).round(0)
region_stats.columns = ['avg', 'total', 'count']
region_stats = region_stats.reset_index()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
ax1.bar(region_stats['region'], region_stats['avg'], color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'])
ax1.set_ylabel('Average Dataset Count', fontsize=12)
ax1.set_title('Average Dataset Count by Region', fontsize=12, fontweight='bold')
for i, v in enumerate(region_stats['avg']):
    ax1.text(i, v + 500, f'{int(v):,}', ha='center', fontsize=10)

ax2.bar(region_stats['region'], region_stats['total'], color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'])
ax2.set_ylabel('Total Dataset Count', fontsize=12)
ax2.set_title('Total Dataset Count by Region', fontsize=12, fontweight='bold')
for i, v in enumerate(region_stats['total']):
    ax2.text(i, v + 2000, f'{int(v):,}', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('static/v3_chart_05_region_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_05_region_comparison.png')

# 图6: 数据来源类型饼图
source_types = {'自主采集': 0, '第三方数据': 0}
for r in success_results:
    if 'third_party' in r.get('method', ''):
        source_types['第三方数据'] += 1
    else:
        source_types['自主采集'] += 1

fig, ax = plt.subplots(figsize=(8, 8))
colors_src = ['#3498db', '#e74c3c']
ax.pie(source_types.values(), labels=source_types.keys(), autopct='%1.1f%%', 
       colors=colors_src, startangle=90, explode=(0.05, 0.05))
ax.set_title('Data Source Types (18 Platforms)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('static/v3_chart_06_source_types.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_06_source_types.png')

# 图7: 数据集数量vs排名散点图（带趋势线）
fig, ax = plt.subplots(figsize=(12, 8))
scatter = ax.scatter(df['dataset_count'], df['topsis_score'], 
                    s=300, c=df['topsis_score'], cmap='RdYlGn', 
                    alpha=0.7, edgecolors='black', linewidth=1)
# 添加趋势线
z = np.polyfit(np.log10(df['dataset_count']), df['topsis_score'], 1)
p = np.poly1d(z)
x_trend = np.logspace(np.log10(df['dataset_count'].min()), np.log10(df['dataset_count'].max()), 100)
ax.plot(x_trend, p(np.log10(x_trend)), "r--", alpha=0.5, label='Trend Line')
for i, row in df.iterrows():
    ax.annotate(row['name'], (row['dataset_count'], row['topsis_score']), 
                xytext=(5, 5), textcoords='offset points', fontsize=9)
ax.set_xlabel('Dataset Count (log scale)', fontsize=12)
ax.set_ylabel('TOPSIS Score', fontsize=12)
ax.set_xscale('log')
ax.set_title('Dataset Count vs TOPSIS Score (with Trend)', fontsize=14, fontweight='bold')
ax.legend()
plt.colorbar(scatter, label='TOPSIS Score')
plt.tight_layout()
plt.savefig('static/v3_chart_07_scatter_trend.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_07_scatter_trend.png')

# 图8: 数据集数量分布直方图
fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(df['dataset_count'], bins=10, color='skyblue', edgecolor='black', alpha=0.7)
ax.set_xlabel('Dataset Count', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Dataset Count Distribution Histogram', fontsize=14, fontweight='bold')
ax.axvline(df['dataset_count'].mean(), color='red', linestyle='--', label=f'Mean: {df["dataset_count"].mean():.0f}')
ax.axvline(df['dataset_count'].median(), color='green', linestyle='--', label=f'Median: {df["dataset_count"].median():.0f}')
ax.legend()
plt.tight_layout()
plt.savefig('static/v3_chart_08_histogram.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_08_histogram.png')

print()
print('='*60)
print('已生成8张核心图表')
print('='*60)
print('图表列表:')
for i in range(1, 9):
    print(f'  v3_chart_{i:02d}_*.png')
