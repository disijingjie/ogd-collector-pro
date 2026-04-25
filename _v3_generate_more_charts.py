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

success_results = [r for r in results if r['status'] == 'success']

# 图9: 数据集数量对数刻度柱状图
fig, ax = plt.subplots(figsize=(14, 8))
df_sorted = df.sort_values('dataset_count', ascending=False)
x_pos = np.arange(len(df_sorted))
bars = ax.bar(x_pos, df_sorted['dataset_count'], color=plt.cm.viridis(np.linspace(0, 1, len(df_sorted))))
ax.set_yscale('log')
ax.set_xlabel('Platform', fontsize=12)
ax.set_ylabel('Dataset Count (log scale)', fontsize=12)
ax.set_title('Dataset Count by Platform (Log Scale)', fontsize=14, fontweight='bold')
ax.set_xticks(x_pos)
ax.set_xticklabels(df_sorted['name'], rotation=45, ha='right')
for i, v in enumerate(df_sorted['dataset_count']):
    ax.text(i, v * 1.1, f'{int(v):,}', ha='center', fontsize=8)
plt.tight_layout()
plt.savefig('static/v3_chart_09_log_bar.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_09_log_bar.png')

# 图10: 数据集数量累积分布
fig, ax = plt.subplots(figsize=(12, 6))
sorted_counts = np.sort(df['dataset_count'].values)
cumulative = np.cumsum(sorted_counts)
ax.plot(range(1, len(cumulative)+1), cumulative, 'o-', linewidth=2, markersize=6, color='#3498db')
ax.fill_between(range(1, len(cumulative)+1), cumulative, alpha=0.3, color='#3498db')
ax.set_xlabel('Platform Rank (by dataset count)', fontsize=12)
ax.set_ylabel('Cumulative Dataset Count', fontsize=12)
ax.set_title('Cumulative Dataset Count Distribution', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('static/v3_chart_10_cumulative.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_10_cumulative.png')

# 图11: 数据集数量热力图（按区域）
region_map = {
    '北京': '东部', '天津': '东部', '上海': '东部', '江苏': '东部', '浙江': '东部', 
    '福建': '东部', '山东': '东部', '广东': '东部',
    '山西': '中部', '安徽': '中部', '江西': '中部', '河南': '中部', '湖北': '中部', '湖南': '中部',
    '内蒙古': '西部', '广西': '西部', '重庆': '西部', '四川': '西部', '贵州': '西部', '云南': '西部',
    '辽宁': '东北', '吉林': '东北', '黑龙江': '东北'
}
df['region'] = df['province'].map(region_map)

fig, ax = plt.subplots(figsize=(10, 6))
region_platforms = df.groupby('region')['name'].apply(list)
region_counts = df.groupby('region')['dataset_count'].apply(list)

# 创建热力图数据
heatmap_data = []
regions = ['东部', '中部', '西部', '东北']
max_platforms = max(len(region_platforms.get(r, [])) for r in regions)
for region in regions:
    counts = region_counts.get(region, [])
    counts += [0] * (max_platforms - len(counts))
    heatmap_data.append(counts)

heatmap_data = np.array(heatmap_data)
im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
ax.set_xticks(range(max_platforms))
ax.set_xticklabels([f'#{i+1}' for i in range(max_platforms)])
ax.set_yticks(range(len(regions)))
ax.set_yticklabels(regions)
ax.set_title('Dataset Count Heatmap by Region', fontsize=14, fontweight='bold')
plt.colorbar(im, ax=ax, label='Dataset Count')
plt.tight_layout()
plt.savefig('static/v3_chart_11_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_11_heatmap.png')

# 图12: TOPSIS得分分布密度图
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df['topsis_score'], bins=15, density=True, alpha=0.7, color='skyblue', edgecolor='black')
ax.axvline(df['topsis_score'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["topsis_score"].mean():.3f}')
ax.axvline(df['topsis_score'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df["topsis_score"].median():.3f}')
ax.set_xlabel('TOPSIS Score', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('TOPSIS Score Distribution Density', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('static/v3_chart_12_density.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_12_density.png')

# 图13: 数据集数量vs排名序号
fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(range(1, len(df)+1), df.sort_values('dataset_count', ascending=False)['dataset_count'], 
           s=200, c=range(len(df)), cmap='RdYlGn_r', alpha=0.7, edgecolors='black')
ax.set_yscale('log')
ax.set_xlabel('Rank', fontsize=12)
ax.set_ylabel('Dataset Count (log scale)', fontsize=12)
ax.set_title('Dataset Count vs Rank (Pareto-like)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('static/v3_chart_13_pareto.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_13_pareto.png')

# 图14: 数据来源类型堆叠柱状图
source_by_region = {'东部': {'自主': 0, '第三方': 0}, '中部': {'自主': 0, '第三方': 0}, 
                    '西部': {'自主': 0, '第三方': 0}, '东北': {'自主': 0, '第三方': 0}}
for _, row in df.iterrows():
    region = row['region']
    # 判断来源类型
    is_third = False
    for r in success_results:
        if r['name'] == row['name'] and 'third_party' in r.get('method', ''):
            is_third = True
            break
    source_type = '第三方' if is_third else '自主'
    if region in source_by_region:
        source_by_region[region][source_type] += 1

fig, ax = plt.subplots(figsize=(10, 6))
regions = list(source_by_region.keys())
autonomous = [source_by_region[r]['自主'] for r in regions]
third_party = [source_by_region[r]['第三方'] for r in regions]
ax.bar(regions, autonomous, label='Autonomous Collection', color='#3498db')
ax.bar(regions, third_party, bottom=autonomous, label='Third-party Data', color='#e74c3c')
ax.set_ylabel('Number of Platforms', fontsize=12)
ax.set_title('Data Source Types by Region', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('static/v3_chart_14_stacked_bar.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_14_stacked_bar.png')

# 图15: 数据集数量瀑布图（从大到小）
fig, ax = plt.subplots(figsize=(14, 8))
df_waterfall = df.sort_values('dataset_count', ascending=False).reset_index(drop=True)
cumulative = [0]
for i in range(len(df_waterfall)):
    cumulative.append(cumulative[-1] + df_waterfall['dataset_count'].iloc[i])

colors_wf = ['#2ecc71' if i < 5 else '#f39c12' if i < 10 else '#e74c3c' for i in range(len(df_waterfall))]
for i in range(len(df_waterfall)):
    ax.bar(i, df_waterfall['dataset_count'].iloc[i], bottom=cumulative[i], color=colors_wf[i], alpha=0.8)
    ax.text(i, cumulative[i] + df_waterfall['dataset_count'].iloc[i]/2, 
            f'{int(df_waterfall["dataset_count"].iloc[i]):,}', ha='center', va='center', fontsize=8)

ax.set_xlabel('Platform', fontsize=12)
ax.set_ylabel('Dataset Count', fontsize=12)
ax.set_title('Dataset Count Waterfall Chart', fontsize=14, fontweight='bold')
ax.set_xticks(range(len(df_waterfall)))
ax.set_xticklabels(df_waterfall['name'], rotation=45, ha='right')
plt.tight_layout()
plt.savefig('static/v3_chart_15_waterfall.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_15_waterfall.png')

# 图16: 数据集数量气泡图（大小=数据集数，颜色=TOPSIS得分）
fig, ax = plt.subplots(figsize=(12, 8))
scatter = ax.scatter(range(len(df)), df['topsis_score'], 
                    s=df['dataset_count']/100, c=df['topsis_score'], 
                    cmap='RdYlGn', alpha=0.6, edgecolors='black')
for i, row in df.iterrows():
    ax.annotate(row['name'], (i, row['topsis_score']), 
                xytext=(5, 5), textcoords='offset points', fontsize=9)
ax.set_xlabel('Platform Index', fontsize=12)
ax.set_ylabel('TOPSIS Score', fontsize=12)
ax.set_title('Bubble Chart: TOPSIS Score vs Platform (Bubble Size = Dataset Count)', fontsize=14, fontweight='bold')
plt.colorbar(scatter, label='TOPSIS Score')
plt.tight_layout()
plt.savefig('static/v3_chart_16_bubble.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: v3_chart_16_bubble.png')

print()
print('='*60)
print('已生成16张图表 (8+8)')
print('='*60)
