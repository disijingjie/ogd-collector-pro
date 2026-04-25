"""
生成剩余的理论框架和对策建议图表
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from pathlib import Path

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

COLORS = {
    'primary': '#1f4e79', 'secondary1': '#c0504d', 'secondary2': '#9bbb59',
    'secondary3': '#4bacc6', 'secondary4': '#f79646', 'secondary5': '#8064a2',
    'light_gray': '#e0e0e0', 'dark_gray': '#666666', 'bg': '#ffffff'
}

OUTPUT_DIR = Path('static/thesis_charts')
OUTPUT_DIR.mkdir(exist_ok=True)

def save_fig(name):
    path = OUTPUT_DIR / f'{name}.png'
    plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'[OK] {name}.png')

print('=== 生成剩余图表 ===')

# 图3-7: 数据要素价值化价值链模型
fig, ax = plt.subplots(figsize=(14, 5))
stages = ['数据资源化', '数据资产化', '数据资本化']
sub_stages = [
    ['数据采集', '数据清洗', '数据整合'],
    ['质量评估', '元数据标注', '目录发布'],
    ['开放共享', '授权运营', '价值变现']
]
colors_stage = [COLORS['secondary3'], COLORS['secondary2'], COLORS['primary']]
for i, (stage, subs, color) in enumerate(zip(stages, sub_stages, colors_stage)):
    x = i * 4 + 1
    # 主阶段框
    rect = FancyBboxPatch((x, 0.5), 3, 2.5, boxstyle="round,pad=0.05", 
                           facecolor=color, edgecolor='white', alpha=0.85, linewidth=2)
    ax.add_patch(rect)
    ax.text(x+1.5, 2.5, stage, ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    # 子阶段
    for j, sub in enumerate(subs):
        ax.text(x+1.5, 1.8-j*0.4, f'• {sub}', ha='center', va='center', fontsize=10, color='white')
    # 箭头
    if i < 2:
        ax.annotate('', xy=(x+3.2, 1.75), xytext=(x+3, 1.75),
                    arrowprops=dict(arrowstyle='->', color=COLORS['dark_gray'], lw=3))
ax.set_xlim(0, 13)
ax.set_ylim(0, 3.5)
ax.axis('off')
ax.set_title('图3-7  数据要素价值化三阶段价值链模型', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
save_fig('图3-7')

# 图3-8: "评估-归因-组态"递进分析逻辑
fig, ax = plt.subplots(figsize=(12, 4))
steps = ['绩效评估\n(TOPSIS/DEA)', '归因分析\n(DEMATEL)', '组态路径\n(fsQCA)', '对策建议\n(分类施策)']
outputs = ['绩效得分与排名', '因果结构与关键驱动', '多重等效路径', '差异化优化策略']
colors_step = [COLORS['secondary3'], COLORS['secondary2'], COLORS['secondary4'], COLORS['primary']]
for i, (step, out, color) in enumerate(zip(steps, outputs, colors_step)):
    x = i * 2.8 + 0.5
    rect = FancyBboxPatch((x, 0.3), 2.2, 2.2, boxstyle="round,pad=0.05",
                           facecolor=color, edgecolor='white', alpha=0.85, linewidth=2)
    ax.add_patch(rect)
    ax.text(x+1.1, 1.8, step, ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    ax.text(x+1.1, 0.9, out, ha='center', va='center', fontsize=9, color='white', alpha=0.9)
    if i < 3:
        ax.annotate('', xy=(x+2.4, 1.4), xytext=(x+2.2, 1.4),
                    arrowprops=dict(arrowstyle='->', color=COLORS['dark_gray'], lw=2))
ax.set_xlim(0, 12)
ax.set_ylim(0, 3)
ax.axis('off')
ax.set_title('图3-8  "评估-归因-组态"递进分析逻辑框架', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
save_fig('图3-8')

# 图7-1: 成熟度模型（五级阶梯）
fig, ax = plt.subplots(figsize=(12, 7))
levels = [
    ('引领级', 'Level 5', '数据要素价值化\n模式输出', COLORS['primary']),
    ('优化级', 'Level 4', '数据利用生态\n应用孵化', COLORS['secondary3']),
    ('规范级', 'Level 3', '质量保障体系\n用户反馈机制', COLORS['secondary2']),
    ('发展级', 'Level 2', 'API接口\n数据可视化', COLORS['secondary4']),
    ('基础级', 'Level 1', '数据目录发布\n文件下载', COLORS['dark_gray']),
]
for i, (name, level, desc, color) in enumerate(levels):
    y = i * 1.2
    width = 8 - i * 1.2
    x = (10 - width) / 2
    rect = FancyBboxPatch((x, y), width, 1, boxstyle="round,pad=0.02",
                           facecolor=color, edgecolor='white', alpha=0.85, linewidth=2)
    ax.add_patch(rect)
    ax.text(5, y+0.7, f'{name} ({level})', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    ax.text(5, y+0.3, desc, ha='center', va='center', fontsize=9, color='white', alpha=0.9)
    # 左侧百分比标注
    pct = ['约11%', '约25%', '约64%', '', ''][i] if i < 3 else ''
    if pct:
        ax.text(x-0.3, y+0.5, pct, ha='right', va='center', fontsize=10, color=color, fontweight='bold')
ax.set_xlim(0, 10)
ax.set_ylim(-0.3, 6.5)
ax.axis('off')
ax.set_title('图7-1  政府数据开放平台五级成熟度模型', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
save_fig('图7-1')

# 图7-2: SWOT策略矩阵
fig, ax = plt.subplots(figsize=(10, 8))
ax.axhline(y=0.5, color=COLORS['dark_gray'], linestyle='--', alpha=0.3)
ax.axvline(x=0.5, color=COLORS['dark_gray'], linestyle='--', alpha=0.3)
# 四个象限
quadrants = {
    '标杆型平台\n(SO策略)': {
        'pos': (0.75, 0.75), 'color': COLORS['primary'],
        'items': ['发挥优势抓住机遇', '推进数据要素价值化', '输出模式经验']
    },
    '潜力型平台\n(WO策略)': {
        'pos': (0.25, 0.75), 'color': COLORS['secondary3'],
        'items': ['克服劣势抓住机遇', '优化资源配置效率', '提升平台服务能力']
    },
    '节约型平台\n(ST策略)': {
        'pos': (0.75, 0.25), 'color': COLORS['secondary2'],
        'items': ['发挥优势规避威胁', '适度增加资源投入', '强化质量管控']
    },
    '困境型平台\n(WT策略)': {
        'pos': (0.25, 0.25), 'color': COLORS['secondary4'],
        'items': ['克服劣势规避威胁', '外部支援系统帮扶', '逐步改善基础条件']
    }
}
for name, info in quadrants.items():
    x, y = info['pos']
    color = info['color']
    ax.text(x, y+0.12, name, ha='center', fontsize=12, fontweight='bold', color=color)
    for j, item in enumerate(info['items']):
        ax.text(x, y+0.05-j*0.04, item, ha='center', fontsize=9, color=COLORS['dark_gray'])
# 轴标签
ax.text(0.5, 0.95, '机会 →', ha='center', fontsize=11, color=COLORS['dark_gray'])
ax.text(0.5, 0.05, '威胁 →', ha='center', fontsize=11, color=COLORS['dark_gray'])
ax.text(0.05, 0.5, '劣势\n↓', ha='center', fontsize=11, color=COLORS['dark_gray'], rotation=0)
ax.text(0.95, 0.5, '优势\n↓', ha='center', fontsize=11, color=COLORS['dark_gray'], rotation=0)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_title('图7-2  四类平台SWOT差异化策略矩阵', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
save_fig('图7-2')

# 图7-5: 分级分类施策方案
fig, ax = plt.subplots(figsize=(12, 8))
# 树状结构
# 根节点
rect_root = FancyBboxPatch((4, 7), 4, 1, boxstyle="round,pad=0.05",
                            facecolor=COLORS['primary'], edgecolor='white', alpha=0.9)
ax.add_patch(rect_root)
ax.text(6, 7.5, '平台绩效提升', ha='center', va='center', fontsize=14, fontweight='bold', color='white')
# 第一层
level1 = ['标杆型', '潜力型', '节约型', '困境型']
level1_colors = [COLORS['secondary3'], COLORS['secondary2'], COLORS['secondary4'], COLORS['secondary1']]
level1_x = [1.5, 4.5, 7.5, 10.5]
for name, color, x in zip(level1, level1_colors, level1_x):
    rect = FancyBboxPatch((x-1, 5), 2, 0.8, boxstyle="round,pad=0.03",
                           facecolor=color, edgecolor='white', alpha=0.85)
    ax.add_patch(rect)
    ax.text(x, 5.4, name, ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    # 连接线
    ax.plot([x, 6], [5.8, 7], color=COLORS['dark_gray'], alpha=0.3, lw=1.5)
# 第二层措施
measures = [
    ['国际标准对接', '模式输出推广', '生态引领作用'],
    ['资源配置优化', '服务能力提升', '制度环境改善'],
    ['质量管控强化', '投入结构优化', '特色优势培育'],
    ['基础条件改善', '外部帮扶引入', '渐进式提升']
]
for i, (name, color, x, m_list) in enumerate(zip(level1, level1_colors, level1_x, measures)):
    for j, m in enumerate(m_list):
        y = 3.5 - j * 0.9
        rect = FancyBboxPatch((x-1.2, y-0.3), 2.4, 0.6, boxstyle="round,pad=0.02",
                               facecolor=color, edgecolor='white', alpha=0.5, linewidth=1)
        ax.add_patch(rect)
        ax.text(x, y, m, ha='center', va='center', fontsize=9, color=COLORS['dark_gray'])
        # 连接线
        ax.plot([x, x], [y+0.3, 5], color=COLORS['dark_gray'], alpha=0.2, lw=1)
ax.set_xlim(0, 12)
ax.set_ylim(0, 8.5)
ax.axis('off')
ax.set_title('图7-5  平台分级分类施策方案', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
save_fig('图7-5')

# 图8-1: 研究主要发现总结
fig, ax = plt.subplots(figsize=(12, 8))
findings = {
    '绩效评估发现': [
        '22个平台绩效呈显著分层',
        '四川(0.852)显著领先',
        '华北区域均值最高(0.739)'
    ],
    '效率分析发现': [
        '11个平台DEA非有效',
        '北京(0.62)效率偏低',
        '投入产出转化待优化'
    ],
    '因果分析发现': [
        '供给保障是最强原因因素',
        '利用效果是最终产出端',
        '传导链条：供给→服务→质量→效果'
    ],
    '组态分析发现': [
        '"全面均衡型"是主路径(64%)',
        '4条高绩效等效路径',
        '多重因果机制成立'
    ]
}
colors_find = [COLORS['primary'], COLORS['secondary1'], COLORS['secondary3'], COLORS['secondary2']]
positions = [(2, 6), (8, 6), (2, 2.5), (8, 2.5)]
for (title, items), color, (x, y) in zip(findings.items(), colors_find, positions):
    rect = FancyBboxPatch((x-2.5, y-2), 5, 3.5, boxstyle="round,pad=0.05",
                           facecolor=color, edgecolor='white', alpha=0.15, linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y+1.2, title, ha='center', fontsize=12, fontweight='bold', color=color)
    for j, item in enumerate(items):
        ax.text(x, y+0.6-j*0.5, f'{j+1}. {item}', ha='center', fontsize=10, color=COLORS['dark_gray'])
# 中心连接
ax.text(5, 4.2, '核心结论', ha='center', fontsize=13, fontweight='bold', color=COLORS['primary'])
ax.text(5, 3.7, '"供给保障是绩效改善的首要驱动力"', ha='center', fontsize=11, color=COLORS['secondary1'], style='italic')
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('图8-1  研究主要发现总结', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
save_fig('图8-1')

# 图8-2: 研究贡献
fig, ax = plt.subplots(figsize=(10, 6))
contributions = [
    ('理论贡献', ['效果导向评估范式', '多重并发因果机制', '"数据口径幻觉"概念'], COLORS['primary']),
    ('方法贡献', ['自动化采集系统', 'AHP-熵权组合赋权', '多方法三角验证'], COLORS['secondary3']),
    ('实践贡献', ['分类施策方案', '成熟度模型', '优先级矩阵'], COLORS['secondary2']),
]
for i, (title, items, color) in enumerate(contributions):
    x = i * 3.3 + 1.5
    rect = FancyBboxPatch((x-1.3, 1), 2.6, 3.5, boxstyle="round,pad=0.05",
                           facecolor=color, edgecolor='white', alpha=0.85, linewidth=2)
    ax.add_patch(rect)
    ax.text(x, 4, title, ha='center', fontsize=12, fontweight='bold', color='white')
    for j, item in enumerate(items):
        ax.text(x, 3.2-j*0.6, f'• {item}', ha='center', fontsize=10, color='white')
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')
ax.set_title('图8-2  研究三维贡献体系', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
save_fig('图8-2')

print('\n=== 完成 ===')
import os
files = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')])
print(f'thesis_charts 目录共 {len(files)} 张图表')
