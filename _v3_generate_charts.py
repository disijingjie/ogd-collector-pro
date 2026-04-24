import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 加载TOPSIS结果
df = pd.read_csv('data/v3_topsis_results.csv', encoding='utf-8-sig')

# 图1: TOPSIS排名柱状图
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#2ecc71' if s > 0.7 else '#f39c12' if s > 0.5 else '#e74c3c' for s in df['topsis_score']]
bars = ax.barh(df['name'][::-1], df['topsis_score'][::-1], color=colors[::-1])
ax.set_xlabel('TOPSIS Score', fontsize=12)
ax.set_title('V3 TOPSIS Ranking - 15 Provincial OGD Platforms', fontsize=14, fontweight='bold')
ax.axvline(x=0.7, color='green', linestyle='--', alpha=0.5, label='High (>0.7)')
ax.axvline(x=0.5, color='orange', linestyle='--', alpha=0.5, label='Medium (>0.5)')
ax.legend()
plt.tight_layout()
plt.savefig('static/v3_topsis_ranking.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: static/v3_topsis_ranking.png')

# 图2: 数据集数量分布
fig, ax = plt.subplots(figsize=(12, 6))
df_sorted = df.sort_values('dataset_count', ascending=True)
colors2 = plt.cm.viridis(df_sorted['dataset_count'] / df_sorted['dataset_count'].max())
bars = ax.barh(df_sorted['name'], df_sorted['dataset_count'], color=colors2)
ax.set_xlabel('Dataset Count', fontsize=12)
ax.set_title('V3 Dataset Count Distribution - 15 Provincial OGD Platforms', fontsize=14, fontweight='bold')
# 添加数值标签
for i, (name, count) in enumerate(zip(df_sorted['name'], df_sorted['dataset_count'])):
    ax.text(count + 1000, i, f'{count:,}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('static/v3_dataset_count_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: static/v3_dataset_count_distribution.png')

# 图3: 数据集数量 vs TOPSIS得分散点图
fig, ax = plt.subplots(figsize=(10, 7))
scatter = ax.scatter(df['dataset_count'], df['topsis_score'], 
                    s=200, c=df['topsis_score'], cmap='RdYlGn', alpha=0.7, edgecolors='black')
for i, row in df.iterrows():
    ax.annotate(row['name'], (row['dataset_count'], row['topsis_score']), 
                xytext=(5, 5), textcoords='offset points', fontsize=9)
ax.set_xlabel('Dataset Count (log scale)', fontsize=12)
ax.set_ylabel('TOPSIS Score', fontsize=12)
ax.set_xscale('log')
ax.set_title('Dataset Count vs TOPSIS Score', fontsize=14, fontweight='bold')
plt.colorbar(scatter, label='TOPSIS Score')
plt.tight_layout()
plt.savefig('static/v3_dataset_vs_topsis.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved: static/v3_dataset_vs_topsis.png')

# 生成Markdown表格
print()
print('=== 论文表格：TOPSIS排名 ===')
print()
print('| 排名 | 平台 | TOPSIS得分 | 数据集数量 | 数据类型 |')
print('|:---:|:---|:---:|:---:|:---|')
for _, row in df.iterrows():
    print(f"| {int(row['topsis_rank'])} | {row['name']} | {row['topsis_score']:.4f} | {int(row['dataset_count']):,} | 数据集/目录 |")

print()
print('图表已保存到 static/ 目录')
