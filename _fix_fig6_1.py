# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import json

# 加载DEMATEL数据
with open('data/verified_dataset/dematel_results_20260426_003903.json','r',encoding='utf-8') as f:
    dematel = json.load(f)

dims = dematel['dimension_names']
centers_list = dematel['center']
causes_list = dematel['cause']
centers = {dims[i]: centers_list[i] for i in range(len(dims))}
causes = {dims[i]: causes_list[i] for i in range(len(dims))}

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(14, 14))
colors_d = ['#D9534F', '#5CB85C', '#5BC0DE', '#F0AD4E']
markers = ['o', 's', '^', 'D']

for i, dim in enumerate(dims):
    ax.scatter(centers[dim], causes[dim], s=800, c=colors_d[i], marker=markers[i],
               edgecolors='white', linewidth=2, alpha=0.85, zorder=5)
    # 调整标签偏移避免重叠
    x_off, y_off = 18, 18
    if i == 0:  # C1 供给保障 - 在右上，向左下偏移
        x_off, y_off = -18, -18
    elif i == 1:  # C2 平台服务 - 在中上，向右下偏移
        x_off, y_off = 18, -10
    elif i == 2:  # C3 数据质量 - 在左中，向右上偏移
        x_off, y_off = 18, 10
    elif i == 3:  # C4 利用效果 - 在右下，向左上偏移
        x_off, y_off = -18, 18
    ax.annotate(f'{dim}', (centers[dim], causes[dim]),
                textcoords='offset points', xytext=(x_off, y_off),
                fontsize=16, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=colors_d[i], alpha=0.9))

# 象限标签
ax.text(0.98, 0.98, '原因因素\n（高中心度+正原因度）', transform=ax.transAxes,
        fontsize=13, ha='right', va='top', style='italic',
        bbox=dict(boxstyle='round', facecolor='#FFF3CD', alpha=0.8))
ax.text(0.02, 0.98, '独立因素\n（低中心度+正原因度）', transform=ax.transAxes,
        fontsize=13, ha='left', va='top', style='italic',
        bbox=dict(boxstyle='round', facecolor='#D4EDDA', alpha=0.8))
ax.text(0.98, 0.02, '核心因素\n（高中心度+负原因度）', transform=ax.transAxes,
        fontsize=13, ha='right', va='bottom', style='italic',
        bbox=dict(boxstyle='round', facecolor='#F8D7DA', alpha=0.8))
ax.text(0.02, 0.02, '结果因素\n（低中心度+负原因度）', transform=ax.transAxes,
        fontsize=13, ha='left', va='bottom', style='italic',
        bbox=dict(boxstyle='round', facecolor='#D1ECF1', alpha=0.8))

ax.axhline(y=0, color='gray', linestyle='-', linewidth=1.5, alpha=0.5)
ax.axvline(x=np.mean(list(centers.values())), color='gray', linestyle='-', linewidth=1.5, alpha=0.5)
ax.set_xlabel('中心度（影响度+被影响度）', fontsize=16, fontweight='bold')
ax.set_ylabel('原因度（影响度-被影响度）', fontsize=16, fontweight='bold')
ax.set_title('图6-1  DEMATEL中心度-原因度因果分类图', fontsize=20, fontweight='bold', pad=20)
ax.tick_params(axis='both', labelsize=14)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)
ax.set_xlim(4.0, 7.2)
ax.set_ylim(-7.5, 7.5)

fig.savefig('static/thesis_charts_v3/图6-1.png', dpi=400, bbox_inches='tight', pad_inches=0.3)
plt.close(fig)
print('图6-1 已重新生成')
