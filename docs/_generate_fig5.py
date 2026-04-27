#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成图5-1（TOPSIS排名）和图5-2（DEA效率散点图）
"""

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import os

# 字体配置
font_path = 'C:/Windows/Fonts/simhei.ttf'
if os.path.exists(font_path):
    FONT_PROP = FontProperties(fname=font_path)
    TITLE_FP = FontProperties(fname=font_path, size=16, weight='bold')
    LABEL_FP = FontProperties(fname=font_path, size=11)
    LEGEND_FP = FontProperties(fname=font_path, size=10)
else:
    FONT_PROP = None
    TITLE_FP = None
    LABEL_FP = None
    LEGEND_FP = None

OUTPUT_DIR = 'static/thesis_charts_v6'
os.makedirs(OUTPUT_DIR, exist_ok=True)

COLOR_BLUE = '#2E5BFF'
COLOR_ORANGE = '#FF6B35'
COLOR_GREEN = '#00C9A7'
COLOR_GRAY = '#888888'

# ========== 图5-1：TOPSIS综合得分排名 ==========
def fig_5_1():
    print("[1/2] 生成图5-1 TOPSIS综合得分排名...")
    
    # 数据来自论文表4-1a（按排名排序）
    platforms = ['山东', '四川', '辽宁', '广西', '海南', '北京', '湖南', '河南', 
                 '内蒙古', '天津', '山西', '广东', '重庆', '江苏', '湖北', '浙江',
                 '贵州', '福建', '江西', '吉林', '云南', '上海', '安徽']
    scores = [0.955, 0.570, 0.564, 0.558, 0.553, 0.551, 0.529, 0.511,
              0.505, 0.498, 0.491, 0.418, 0.404, 0.399, 0.389, 0.389,
              0.349, 0.325, 0.304, 0.282, 0.275, 0.268, 0.095]
    
    # 梯队颜色
    colors = []
    for s in scores:
        if s >= 0.7:
            colors.append(COLOR_BLUE)
        elif s >= 0.4:
            colors.append(COLOR_ORANGE)
        else:
            colors.append(COLOR_GREEN)
    
    fig, ax = plt.subplots(figsize=(14, 7), facecolor='white')
    
    y_pos = np.arange(len(platforms))
    bars = ax.barh(y_pos, scores, color=colors, height=0.7, edgecolor='white', linewidth=0.3)
    
    # 数值标注
    for bar, score in zip(bars, scores):
        width = bar.get_width()
        ax.text(width + 0.015, bar.get_y() + bar.get_height()/2, 
                f'{score:.3f}', va='center', ha='left', fontsize=9, color='#333')
    
    ax.set_yticks(y_pos)
    if FONT_PROP:
        ax.set_yticklabels(platforms, fontproperties=FONT_PROP, fontsize=11)
        ax.set_xlabel('TOPSIS综合得分', fontproperties=LABEL_FP)
    else:
        ax.set_yticklabels(platforms, fontsize=11)
        ax.set_xlabel('TOPSIS综合得分', fontsize=12)
    
    ax.invert_yaxis()
    ax.set_xlim(0, 1.1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # 梯队分界线
    ax.axvline(x=0.7, color=COLOR_BLUE, linestyle='--', linewidth=1, alpha=0.5)
    ax.axvline(x=0.4, color=COLOR_ORANGE, linestyle='--', linewidth=1, alpha=0.5)
    
    # 梯队标注
    if FONT_PROP:
        ax.text(0.85, 22.5, '第一梯队', fontproperties=LABEL_FP, color=COLOR_BLUE, ha='center', fontweight='bold')
        ax.text(0.55, 22.5, '第二梯队', fontproperties=LABEL_FP, color=COLOR_ORANGE, ha='center', fontweight='bold')
        ax.text(0.20, 22.5, '第三梯队', fontproperties=LABEL_FP, color=COLOR_GREEN, ha='center', fontweight='bold')
    else:
        ax.text(0.85, 22.5, '第一梯队', fontsize=11, color=COLOR_BLUE, ha='center', fontweight='bold')
        ax.text(0.55, 22.5, '第二梯队', fontsize=11, color=COLOR_ORANGE, ha='center', fontweight='bold')
        ax.text(0.20, 22.5, '第三梯队', fontsize=11, color=COLOR_GREEN, ha='center', fontweight='bold')
    
    # 图例
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COLOR_BLUE, label='第一梯队（≥0.7）'),
                       Patch(facecolor=COLOR_ORANGE, label='第二梯队（0.4-0.7）'),
                       Patch(facecolor=COLOR_GREEN, label='第三梯队（<0.4）')]
    if LEGEND_FP:
        ax.legend(handles=legend_elements, loc='lower right', frameon=True, prop=LEGEND_FP)
    else:
        ax.legend(handles=legend_elements, loc='lower right', frameon=True, fontsize=10)
    
    if TITLE_FP:
        ax.set_title('图5-1 省级政府数据开放平台TOPSIS综合得分排名', fontproperties=TITLE_FP, pad=15)
    else:
        ax.set_title('图5-1 省级政府数据开放平台TOPSIS综合得分排名', fontsize=16, fontweight='bold', pad=15)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图5-1.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] 图5-1 已保存")


# ========== 图5-2：DEA效率散点图 ==========
def fig_5_2():
    print("[2/2] 生成图5-2 DEA效率散点图...")
    
    # 数据来自v3_dea_results.csv
    # input1, input2, output, efficiency
    provinces = ['广东', '山东', '浙江', '海南', '重庆', '湖北', '上海', '贵州',
                 '广西', '四川', '北京', '福建', '辽宁', '江苏', '湖南', '江西',
                 '吉林', '内蒙古', '天津', '河南', '云南', '山西']
    effs = [0.4975, 0.3524, 0.3194, 0.2583, 0.2311, 0.2172, 0.1947, 0.1807,
            0.1723, 0.1716, 0.1715, 0.1702, 0.1702, 0.1690, 0.1690, 0.1690,
            0.1691, 0.1691, 0.1768, 0.1156, 0.1156, 0.0]
    
    # 综合投入 = input1 + input2（简化）
    inputs = [2.0, 1.522, 1.290, 1.294, 1.231, 1.198, 1.010, 1.093,
              1.052, 1.047, 1.046, 1.034, 1.034, 1.005, 1.005, 1.004,
              1.002, 1.002, 1.027, 0.705, 0.701, 0.601]
    
    # 产出
    outputs = [1.0, 0.540, 0.415, 0.337, 0.287, 0.262, 0.199, 0.199,
               0.183, 0.181, 0.181, 0.178, 0.178, 0.172, 0.172, 0.171,
               0.171, 0.171, 0.166, 0.083, 0.082, 0.0]
    
    fig, ax = plt.subplots(figsize=(11, 8), facecolor='white')
    
    # 效率前沿面（理想情况：efficiency=1）
    x_frontier = np.linspace(0, 2.5, 100)
    y_frontier = x_frontier * 0.5  # 简化前沿面
    ax.plot(x_frontier, y_frontier, 'k--', linewidth=1.5, alpha=0.4, label='效率前沿面（参考）')
    
    # 散点颜色：按效率分层
    colors = []
    for e in effs:
        if e >= 0.4:
            colors.append(COLOR_BLUE)
        elif e >= 0.2:
            colors.append(COLOR_ORANGE)
        else:
            colors.append(COLOR_GREEN)
    
    sizes = [80 + e * 200 for e in effs]
    
    scatter = ax.scatter(inputs, outputs, c=colors, s=sizes, alpha=0.75, edgecolors='white', linewidth=1.5, zorder=5)
    
    # 标注部分关键平台
    key_indices = [0, 1, 2, 4, 6, 14, 19]  # 广东、山东、浙江、重庆、上海、湖南、河南
    for idx in key_indices:
        offset_x = 0.05 if idx % 2 == 0 else -0.05
        offset_y = 0.02 if idx % 3 == 0 else -0.03
        ha = 'left' if idx % 2 == 0 else 'right'
        if FONT_PROP:
            ax.annotate(provinces[idx], (inputs[idx], outputs[idx]),
                       xytext=(offset_x, offset_y), textcoords='offset points',
                       fontsize=9, fontproperties=FONT_PROP, ha=ha, color='#333')
        else:
            ax.annotate(provinces[idx], (inputs[idx], outputs[idx]),
                       xytext=(offset_x, offset_y), textcoords='offset points',
                       fontsize=9, ha=ha, color='#333')
    
    if FONT_PROP:
        ax.set_xlabel('综合投入（标准化）', fontproperties=LABEL_FP)
        ax.set_ylabel('综合产出（标准化）', fontproperties=LABEL_FP)
    else:
        ax.set_xlabel('综合投入（标准化）', fontsize=12)
        ax.set_ylabel('综合产出（标准化）', fontsize=12)
    
    ax.set_xlim(0, 2.5)
    ax.set_ylim(0, 1.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 图例
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COLOR_BLUE, label='高效率（≥0.4）'),
                       Patch(facecolor=COLOR_ORANGE, label='中效率（0.2-0.4）'),
                       Patch(facecolor=COLOR_GREEN, label='低效率（<0.2）')]
    if LEGEND_FP:
        ax.legend(handles=legend_elements, loc='upper left', frameon=True, prop=LEGEND_FP)
    else:
        ax.legend(handles=legend_elements, loc='upper left', frameon=True, fontsize=10)
    
    if TITLE_FP:
        ax.set_title('图5-2 DEA-BCC效率分析散点图', fontproperties=TITLE_FP, pad=15)
    else:
        ax.set_title('图5-2 DEA-BCC效率分析散点图', fontsize=16, fontweight='bold', pad=15)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图5-2.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] 图5-2 已保存")


if __name__ == '__main__':
    fig_5_1()
    fig_5_2()
    print("\n全部完成！")
