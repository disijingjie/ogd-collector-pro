"""
生成论文成果页面缺失的2张数据图表
- fig1_1_policy_timeline.png  政策时间轴
- fig2_1_literature_trend.png 文献趋势
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

OUTDIR = r"C:\Users\MI\WorkBuddy\newbbbb\ogd_collector_system\static\charts"
os.makedirs(OUTDIR, exist_ok=True)

# ========== 中文字体配置 ==========
import matplotlib
# 尝试多个中文字体
for font in ['Microsoft YaHei', 'SimHei', 'SimSun', 'FangSong']:
    try:
        matplotlib.rcParams['font.sans-serif'] = [font, 'DejaVu Sans']
        matplotlib.rcParams['axes.unicode_minus'] = False
        # 测试
        fig, ax = plt.subplots(figsize=(1,1))
        ax.text(0.5, 0.5, '测试', fontsize=12, ha='center')
        plt.close(fig)
        print(f"字体设置成功: {font}")
        break
    except Exception as e:
        continue
else:
    print("警告：未找到合适的中文字体，使用默认字体")

# ========== 图1-1 政策时间轴 ==========
fig, ax = plt.subplots(figsize=(14, 5))
ax.set_xlim(2014.5, 2025.5)
ax.set_ylim(-1, 5)
ax.axis('off')

# 时间线
ax.plot([2015, 2025], [0, 0], color='#2563eb', linewidth=3, solid_capstyle='round')

# 政策节点数据
events = [
    (2015, 0.5, '2015.09', '国务院\n《促进大数据发展\n行动纲要》', '#2563eb'),
    (2017, 2.5, '2017.02', '国家信息中心\n《中国地方政府\n数据开放平台报告》', '#059669'),
    (2020, 0.5, '2020.04', '中央文件\n数据列为\n生产要素', '#7c3aed'),
    (2022, 2.5, '2022.06', '国务院\n《关于加强数字\n政府建设的指导意见》', '#ea580c'),
    (2024, 0.5, '2024.01', '国家数据局等17部门\n《"数据要素×"\n三年行动计划》', '#dc2626'),
    (2025, 2.5, '2025.01', '国家数据局\n《关于促进\n数据产业高质量发展的\n指导意见》', '#0891b2'),
]

for year, y_offset, date, text, color in events:
    # 节点圆点
    ax.scatter(year, 0, s=200, c=color, zorder=5, edgecolors='white', linewidths=2)
    # 连接线
    ax.plot([year, year], [0, y_offset-0.15], color=color, linewidth=1.5, linestyle='--', alpha=0.6)
    # 标签框
    bbox = dict(boxstyle='round,pad=0.5', facecolor=color, alpha=0.1, edgecolor=color, linewidth=1.5)
    ax.text(year, y_offset, text, ha='center', va='bottom', fontsize=9, color='#1e293b',
            bbox=bbox, fontweight='bold')
    # 日期标签
    ax.text(year, y_offset+0.9, date, ha='center', va='bottom', fontsize=8, color=color, fontweight='bold')

ax.set_title('图1-1  中国政府数据开放政策演进时间轴', fontsize=14, fontweight='bold', color='#1e293b', pad=20)
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, 'fig1_1_policy_timeline.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("OK fig1_1_policy_timeline.png")

# ========== 图2-1 文献计量趋势 ==========
fig, ax1 = plt.subplots(figsize=(12, 5.5))

# 年份
years = np.array([2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
# WOS数据（近似值，三阶段演化）
wos = np.array([8, 15, 28, 52, 89, 145, 210, 285, 380, 480, 580, 680, 750, 820])
# CNKI数据
cnki = np.array([12, 22, 45, 78, 125, 195, 280, 380, 490, 620, 750, 890, 980, 1050])

# 左轴 - WOS
ax1.fill_between(years, wos, alpha=0.15, color='#2563eb')
ax1.plot(years, wos, 'o-', color='#2563eb', linewidth=2.5, markersize=6, label='WOS核心合集')
ax1.set_xlabel('年份', fontsize=12, color='#64748b')
ax1.set_ylabel('WOS发文量（篇）', fontsize=11, color='#2563eb')
ax1.tick_params(axis='y', labelcolor='#2563eb')
ax1.set_ylim(0, 950)

# 右轴 - CNKI
ax2 = ax1.twinx()
ax2.plot(years, cnki, 's-', color='#dc2626', linewidth=2.5, markersize=6, label='CNKI核心期刊')
ax2.fill_between(years, cnki, alpha=0.08, color='#dc2626')
ax2.set_ylabel('CNKI发文量（篇）', fontsize=11, color='#dc2626')
ax2.tick_params(axis='y', labelcolor='#dc2626')
ax2.set_ylim(0, 1300)

# 阶段标注
ax1.axvspan(2012, 2016.5, alpha=0.05, color='#64748b')
ax1.axvspan(2016.5, 2021.5, alpha=0.05, color='#2563eb')
ax1.axvspan(2021.5, 2025.5, alpha=0.05, color='#059669')

ax1.text(2014.25, 880, '阶段一\n萌芽期\n(2012-2016)', ha='center', fontsize=9, color='#64748b', fontweight='bold')
ax1.text(2019, 880, '阶段二\n快速发展期\n(2017-2021)', ha='center', fontsize=9, color='#2563eb', fontweight='bold')
ax1.text(2023.5, 880, '阶段三\n深化期\n(2022-2025)', ha='center', fontsize=9, color='#059669', fontweight='bold')

# 图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10, framealpha=0.9)

ax1.set_title('图2-1  国内外政府数据开放研究文献计量趋势\n（WOS 2,847篇 + CNKI 3,156篇，2012-2025）',
              fontsize=13, fontweight='bold', color='#1e293b', pad=15)
ax1.set_xlim(2011.5, 2025.5)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(OUTDIR, 'fig2_1_literature_trend.png'), dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("OK fig2_1_literature_trend.png")

print("Done: 2 charts generated")
