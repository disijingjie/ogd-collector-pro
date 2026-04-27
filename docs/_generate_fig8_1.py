#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成图8-1：政府数据开放平台四阶段质量提升路径
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# 字体设置
plt.rcParams['font.family'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# 标题
ax.text(7, 9.5, '政府数据开放平台四阶段质量提升路径', fontsize=18, fontweight='bold',
        ha='center', va='center', color='#1a1a2e')
ax.text(7, 9.1, '数据资源化 → 数据资产化 → 数据要素化 → 数据价值化', fontsize=12,
        ha='center', va='center', color='#4a4a6a', style='italic')

# 四阶段框
stages = [
    {'name': '第一阶段\n数据资源化', 'x': 2, 'y': 6.5, 'w': 2.5, 'h': 1.8,
     'color': '#e8f4f8', 'edge': '#2196F3', 'dim': '供给保障维度',
     'tasks': '• 制定开放管理办法\n• 建立质量标准体系\n• 完善更新维护机制',
     'target': '目标：数据集>1000个\n口径一致性>0.15'},
    {'name': '第二阶段\n数据资产化', 'x': 5.5, 'y': 6.5, 'w': 2.5, 'h': 1.8,
     'color': '#fff3e0', 'edge': '#FF9800', 'dim': '平台服务维度',
     'tasks': '• 优化检索预览功能\n• 开放标准化API\n• 建立用户反馈机制',
     'target': '目标：功能完备度>0.70\nAPI开放度>0.60'},
    {'name': '第三阶段\n数据要素化', 'x': 9, 'y': 6.5, 'w': 2.5, 'h': 1.8,
     'color': '#e8f5e9', 'edge': '#4CAF50', 'dim': '数据质量维度',
     'tasks': '• 建立质量审核机制\n• 推行结构化格式\n• 元数据标准化管理',
     'target': '目标：质量指数>0.80\n结构化格式>90%'},
    {'name': '第四阶段\n数据价值化', 'x': 12.5, 'y': 6.5, 'w': 2.5, 'h': 1.8,
     'color': '#fce4ec', 'edge': '#E91E63', 'dim': '利用效果维度',
     'tasks': '• 举办数据创新大赛\n• 培育开发者社区\n• 探索授权运营模式',
     'target': '目标：应用成果>50个\nAPI调用>10万次/月'},
]

for i, s in enumerate(stages):
    # 主框
    box = FancyBboxPatch((s['x']-s['w']/2, s['y']-s['h']/2), s['w'], s['h'],
                          boxstyle="round,pad=0.05,rounding_size=0.15",
                          facecolor=s['color'], edgecolor=s['edge'],
                          linewidth=2.5, alpha=0.95)
    ax.add_patch(box)

    # 阶段名称
    ax.text(s['x'], s['y']+0.5, s['name'], fontsize=11, fontweight='bold',
            ha='center', va='center', color=s['edge'])
    # 维度标签
    ax.text(s['x'], s['y']+0.05, s['dim'], fontsize=9,
            ha='center', va='center', color='#666666')

    # 关键举措
    ax.text(s['x'], s['y']-0.55, s['tasks'], fontsize=8,
            ha='center', va='center', color='#333333', linespacing=1.4)

    # 阶段目标（下方）
    goal_box = FancyBboxPatch((s['x']-s['w']/2+0.1, s['y']-s['h']/2-1.3), s['w']-0.2, 1.1,
                               boxstyle="round,pad=0.02,rounding_size=0.1",
                               facecolor='#f5f5f5', edgecolor=s['edge'],
                               linewidth=1, linestyle='--', alpha=0.8)
    ax.add_patch(goal_box)
    ax.text(s['x'], s['y']-s['h']/2-0.75, s['target'], fontsize=8,
            ha='center', va='center', color=s['edge'], fontweight='bold')

    # 箭头（阶段之间）
    if i < len(stages) - 1:
        next_x = stages[i+1]['x'] - stages[i+1]['w']/2
        curr_x = s['x'] + s['w']/2
        ax.annotate('', xy=(next_x, s['y']), xytext=(curr_x, s['y']),
                    arrowprops=dict(arrowstyle='->', color='#666666', lw=2))

# 底部说明
ax.text(7, 1.8, '注：四阶段路径为螺旋上升循环，非线性递进。不同发展阶段平台可从不同阶段切入。',
        fontsize=9, ha='center', va='center', color='#888888', style='italic')

# 左侧平台类型标注
ax.text(0.3, 6.5, '平台类型\n切入阶段', fontsize=10, fontweight='bold',
        ha='center', va='center', color='#1a1a2e',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#e3f2fd', edgecolor='#1976D2'))

# 平台类型箭头
platform_types = [
    {'name': '全面领先型', 'y': 8.3, 'color': '#E91E63', 'stage': 4},
    {'name': '质量优先型', 'y': 7.7, 'color': '#4CAF50', 'stage': 2},
    {'name': '全面匮乏型', 'y': 7.1, 'color': '#2196F3', 'stage': 1},
    {'name': '服务缺失型', 'y': 6.5, 'color': '#FF9800', 'stage': 2},
    {'name': '利用缺失型', 'y': 5.9, 'color': '#9C27B0', 'stage': 4},
]

for pt in platform_types:
    ax.text(0.3, pt['y'], pt['name'], fontsize=8, ha='center', va='center',
            color=pt['color'], fontweight='bold')

plt.tight_layout()
plt.savefig('static/thesis_charts_v6/图8-1.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("[OK] 图8-1已生成: static/thesis_charts_v6/图8-1.png")
