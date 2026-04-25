"""
论文图表批量生成脚本 V2
基于最新真实计算结果，生成所有论文所需图表
目标：约30张高质量图表
"""
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 统一配色方案
COLORS = {
    'primary': '#1f4e79',
    'secondary1': '#c0504d',
    'secondary2': '#9bbb59',
    'secondary3': '#4bacc6',
    'secondary4': '#f79646',
    'secondary5': '#8064a2',
    'light_gray': '#e0e0e0',
    'dark_gray': '#666666',
    'bg': '#ffffff'
}

# 输出目录
OUTPUT_DIR = Path('static/thesis_charts_v2')
OUTPUT_DIR.mkdir(exist_ok=True)

# 加载数据
# TOPSIS数据
topsis_data = []
with open('data/verified_dataset/table_topsis_binary_20260426_003903.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        topsis_data.append(row)

# DEA数据
dea_data = []
with open('data/verified_dataset/table_dea_20260426_003903.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        dea_data.append(row)

# DEMATEL数据
with open('data/verified_dataset/dematel_results_20260426_003903.json', 'r', encoding='utf-8') as f:
    dematel = json.load(f)

# fsQCA数据
with open('data/verified_dataset/fsqca_results_20260426_003903.json', 'r', encoding='utf-8') as f:
    fsqca = json.load(f)

# 数据集数量
dataset_counts = {
    'beijing': 4454, 'chongqing': 22550, 'fujian': 6722,
    'guangdong': 97528, 'guangxi': 10162, 'guizhou': 9042,
    'hainan': 35835, 'henan': 0, 'hubei': 24119, 'hunan': 634,
    'jiangsu': 0, 'jiangxi': 534, 'jilin': 303, 'liaoning': 4120,
    'neimenggu': 219, 'shandong': 63656, 'shanxi': 0, 'sichuan': 9115,
    'tianjin': 0, 'yunnan': 0, 'zhejiang': 38000, 'shanghai': 0
}

# 省级平台基本信息
platform_info = [
    ('beijing', '北京市', '华北', 2015),
    ('tianjin', '天津市', '华北', 2016),
    ('shanxi', '山西省', '华北', 2024),
    ('neimenggu', '内蒙古自治区', '华北', 2017),
    ('liaoning', '辽宁省', '东北', 2023),
    ('jilin', '吉林省', '东北', 2017),
    ('shanghai', '上海市', '华东', 2012),
    ('jiangsu', '江苏省', '华东', 2018),
    ('zhejiang', '浙江省', '华东', 2015),
    ('anhui', '安徽省', '华东', 2019),
    ('fujian', '福建省', '华东', 2018),
    ('jiangxi', '江西省', '华东', 2019),
    ('shandong', '山东省', '华东', 2018),
    ('henan', '河南省', '华中', 2017),
    ('hubei', '湖北省', '华中', 2019),
    ('hunan', '湖南省', '华中', 2019),
    ('guangdong', '广东省', '华南', 2015),
    ('guangxi', '广西壮族自治区', '华南', 2019),
    ('hainan', '海南省', '华南', 2018),
    ('chongqing', '重庆市', '西南', 2016),
    ('sichuan', '四川省', '西南', 2018),
    ('guizhou', '贵州省', '西南', 2017),
    ('yunnan', '云南省', '西南', 2017),
]

def save_fig(name):
    """保存图表"""
    path = OUTPUT_DIR / f'{name}.png'
    plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'[OK] {name}.png')

print('=' * 60)
print('开始生成论文图表 V2')
print('=' * 60)

# ==================== 第五章 图表 ====================
print('\n--- 第五章 绩效评估图表 ---')

# 图5-1: 22个平台数据集数量排名（水平柱状图）
fig, ax = plt.subplots(figsize=(10, 8))
provinces = [d['name'] for d in topsis_data]
counts = [dataset_counts.get(d['code'], 0) for d in topsis_data]
# 排序
sorted_idx = np.argsort(counts)
provinces_sorted = [provinces[i] for i in sorted_idx]
counts_sorted = [counts[i] for i in sorted_idx]
colors_bar = [COLORS['secondary1'] if c > 50000 else COLORS['secondary4'] if c > 10000 else COLORS['secondary3'] if c > 1000 else COLORS['dark_gray'] for c in counts_sorted]
bars = ax.barh(range(len(provinces_sorted)), counts_sorted, color=colors_bar, edgecolor='white', height=0.7)
ax.set_yticks(range(len(provinces_sorted)))
ax.set_yticklabels(provinces_sorted, fontsize=10)
ax.set_xlabel('数据集/目录数量（个）', fontsize=12)
ax.set_title('图5-1  22个省级平台数据集数量排名', fontsize=14, fontweight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3)
# 添加数值标签
for i, (bar, val) in enumerate(zip(bars, counts_sorted)):
    if val > 0:
        ax.text(val + max(counts)*0.01, i, f'{val:,}', va='center', fontsize=8)
    else:
        ax.text(100, i, '未采集', va='center', fontsize=8, color=COLORS['dark_gray'], style='italic')
# 添加图例
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=COLORS['secondary1'], label='>50,000'),
                   Patch(facecolor=COLORS['secondary4'], label='10,000-50,000'),
                   Patch(facecolor=COLORS['secondary3'], label='1,000-10,000'),
                   Patch(facecolor=COLORS['dark_gray'], label='<1,000或未采集')]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9, title='数据规模')
plt.tight_layout()
save_fig('图5-1')

# 图5-2: TOPSIS综合绩效排名
fig, ax = plt.subplots(figsize=(10, 8))
scores = [float(d['topsis_score']) for d in topsis_data]
# 按得分排序（高分在上）
sorted_idx = np.argsort(scores)
names_sorted = [topsis_data[i]['name'] for i in sorted_idx]
scores_sorted = [scores[i] for i in sorted_idx]
colors_topsis = [COLORS['primary'] if s > 0.5 else COLORS['secondary1'] if s > 0.3 else COLORS['secondary4'] if s > 0.15 else COLORS['dark_gray'] for s in scores_sorted]
bars = ax.barh(range(len(names_sorted)), scores_sorted, color=colors_topsis, edgecolor='white', height=0.7)
ax.set_yticks(range(len(names_sorted)))
ax.set_yticklabels(names_sorted, fontsize=10)
ax.set_xlabel('TOPSIS综合得分', fontsize=12)
ax.set_title('图5-2  22个省级平台TOPSIS综合绩效排名', fontsize=14, fontweight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3)
for i, (bar, val) in enumerate(zip(bars, scores_sorted)):
    ax.text(val + 0.01, i, f'{val:.3f}', va='center', fontsize=9)
ax.set_xlim(0, 1.0)
plt.tight_layout()
save_fig('图5-2')

# 图5-3: DEA效率值排名
fig, ax = plt.subplots(figsize=(10, 8))
dea_scores = [float(d['dea_efficiency']) for d in dea_data]
dea_names = [d['name'] for d in dea_data]
# 排序
sorted_idx = np.argsort(dea_scores)[::-1]
dea_names_sorted = [dea_names[i] for i in sorted_idx]
dea_scores_sorted = [dea_scores[i] for i in sorted_idx]
colors_dea = [COLORS['secondary2'] if s >= 0.999 else COLORS['secondary1'] for s in dea_scores_sorted]
bars = ax.barh(range(len(dea_names_sorted)), dea_scores_sorted, color=colors_dea, edgecolor='white', height=0.7)
ax.set_yticks(range(len(dea_names_sorted)))
ax.set_yticklabels(dea_names_sorted, fontsize=10)
ax.set_xlabel('DEA-BCC综合效率值', fontsize=12)
ax.set_title('图5-3  22个省级平台DEA-BCC效率排名', fontsize=14, fontweight='bold', pad=15)
ax.axvline(x=1.0, color=COLORS['dark_gray'], linestyle='--', alpha=0.5, label='效率前沿面')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3)
for i, (bar, val) in enumerate(zip(bars, dea_scores_sorted)):
    ax.text(val + 0.01, i, f'{val:.3f}', va='center', fontsize=9)
legend_elements = [Patch(facecolor=COLORS['secondary2'], label='DEA有效 (TE=1.0)'),
                   Patch(facecolor=COLORS['secondary1'], label='非DEA有效 (TE<1.0)')]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
plt.tight_layout()
save_fig('图5-3')

# 图5-4: 四大区域绩效对比（箱线图）
fig, ax = plt.subplots(figsize=(10, 6))
region_data = {}
for d in topsis_data:
    r = d['region']
    if r not in region_data:
        region_data[r] = []
    region_data[r].append(float(d['topsis_score']))
regions = list(region_data.keys())
region_scores = [region_data[r] for r in regions]
bp = ax.boxplot(region_scores, tick_labels=regions, patch_artist=True,
                boxprops=dict(facecolor=COLORS['secondary3'], alpha=0.7),
                medianprops=dict(color=COLORS['primary'], linewidth=2),
                whiskerprops=dict(color=COLORS['dark_gray']),
                capprops=dict(color=COLORS['dark_gray']))
ax.set_ylabel('TOPSIS综合得分', fontsize=12)
ax.set_title('图5-4  四大区域综合绩效箱线图对比', fontsize=14, fontweight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
save_fig('图5-4')

# 图5-5: TOP5平台功能完善度雷达图
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
indicators = ['HTTPS', '搜索', '下载', 'API', '可视化', '更新信息', '元数据', '反馈', '注册', '预览', '批量下载']
top5 = topsis_data[:5]  # 前5名
angles = np.linspace(0, 2*np.pi, len(indicators), endpoint=False).tolist()
angles += angles[:1]
colors_radar = [COLORS['primary'], COLORS['secondary1'], COLORS['secondary2'], COLORS['secondary3'], COLORS['secondary4']]
for idx, d in enumerate(top5):
    values = [
        int(d['has_https']), int(d['has_search']), int(d['has_download']),
        int(d['has_api']), int(d['has_visualization']), int(d['has_update_info']),
        int(d['has_metadata']), int(d['has_feedback']), int(d['has_register']),
        int(d['has_preview']), int(d['has_bulk_download'])
    ]
    values += values[:1]
    ax.plot(angles, values, 'o-', linewidth=2, label=d['name'], color=colors_radar[idx], markersize=5)
    ax.fill(angles, values, alpha=0.1, color=colors_radar[idx])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(indicators, fontsize=9)
ax.set_ylim(0, 1.2)
ax.set_title('图5-5  TOP5平台功能完善度雷达图', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
plt.tight_layout()
save_fig('图5-5')

# 图5-6: 11项指标权重分布
fig, ax = plt.subplots(figsize=(10, 6))
weights = {
    '是否提供更新信息': 0.2126,
    '是否有反馈渠道': 0.1663,
    '是否可下载': 0.1130,
    '是否有元数据': 0.1130,
    '是否可注册': 0.1130,
    '是否提供API': 0.0981,
    '是否支持可视化': 0.0981,
    '是否有搜索': 0.0595,
    '是否HTTPS': 0.0178,
    '是否有预览': 0.0087,
    '是否支持批量下载': 0.0000
}
names_w = list(weights.keys())
vals_w = list(weights.values())
colors_w = [COLORS['primary'] if v > 0.15 else COLORS['secondary1'] if v > 0.08 else COLORS['secondary3'] if v > 0.01 else COLORS['dark_gray'] for v in vals_w]
bars = ax.barh(range(len(names_w)), vals_w, color=colors_w, edgecolor='white', height=0.6)
ax.set_yticks(range(len(names_w)))
ax.set_yticklabels(names_w, fontsize=10)
ax.set_xlabel('熵权法权重', fontsize=12)
ax.set_title('图5-6  11项功能指标熵权法权重分布', fontsize=14, fontweight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3)
for i, (bar, val) in enumerate(zip(bars, vals_w)):
    ax.text(val + 0.005, i, f'{val:.4f}', va='center', fontsize=9)
plt.tight_layout()
save_fig('图5-6')

# 图5-7: TOPSIS得分分布直方图
fig, ax = plt.subplots(figsize=(10, 6))
all_scores = [float(d['topsis_score']) for d in topsis_data]
ax.hist(all_scores, bins=10, color=COLORS['secondary3'], edgecolor='white', alpha=0.8)
ax.axvline(x=np.mean(all_scores), color=COLORS['secondary1'], linestyle='--', linewidth=2, label=f'均值={np.mean(all_scores):.3f}')
ax.axvline(x=np.median(all_scores), color=COLORS['primary'], linestyle='--', linewidth=2, label=f'中位数={np.median(all_scores):.3f}')
ax.set_xlabel('TOPSIS综合得分', fontsize=12)
ax.set_ylabel('平台数量', fontsize=12)
ax.set_title('图5-7  22个平台TOPSIS得分分布直方图', fontsize=14, fontweight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
save_fig('图5-7')

# 图5-8: 功能完善度与绩效关系散点图
fig, ax = plt.subplots(figsize=(10, 7))
func_scores = [sum([int(d[f]) for f in ['has_https','has_search','has_download','has_api','has_visualization','has_update_info','has_metadata','has_feedback','has_register','has_preview','has_bulk_download']]) for d in topsis_data]
scatter_colors = [COLORS['secondary1'] if r=='华东' else COLORS['secondary2'] if r=='华南' else COLORS['secondary3'] if r=='华北' else COLORS['secondary4'] if r=='华中' else COLORS['secondary5'] for r in [d['region'] for d in topsis_data]]
ax.scatter(func_scores, [float(d['topsis_score']) for d in topsis_data], c=scatter_colors, s=120, alpha=0.7, edgecolors='white', linewidth=1.5)
for i, d in enumerate(topsis_data):
    ax.annotate(d['name'], (func_scores[i], float(d['topsis_score'])), fontsize=8, alpha=0.8)
ax.set_xlabel('功能完善度（11项功能得分之和）', fontsize=12)
ax.set_ylabel('TOPSIS综合得分', fontsize=12)
ax.set_title('图5-8  功能完善度与综合绩效关系散点图', fontsize=14, fontweight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)
# 添加趋势线
z = np.polyfit(func_scores, [float(d['topsis_score']) for d in topsis_data], 1)
p = np.poly1d(z)
x_line = np.linspace(min(func_scores), max(func_scores), 100)
ax.plot(x_line, p(x_line), '--', color=COLORS['primary'], alpha=0.5, label=f'趋势线')
ax.legend(fontsize=10)
plt.tight_layout()
save_fig('图5-8')

# 图5-9: DEA效率 vs TOPSIS绩效散点图
fig, ax = plt.subplots(figsize=(10, 7))
merged = {}
for d in topsis_data:
    merged[d['code']] = {'name': d['name'], 'topsis': float(d['topsis_score']), 'region': d['region']}
for d in dea_data:
    if d['code'] in merged:
        merged[d['code']]['dea'] = float(d['dea_efficiency'])
        merged[d['code']]['years'] = int(d['operating_years'])
scatter_colors2 = [COLORS['secondary1'] if r=='华东' else COLORS['secondary2'] if r=='华南' else COLORS['secondary3'] if r=='华北' else COLORS['secondary4'] if r=='华中' else COLORS['secondary5'] for r in [v['region'] for v in merged.values()]]
ax.scatter([v['dea'] for v in merged.values()], [v['topsis'] for v in merged.values()],
           c=scatter_colors2, s=[v['years']*15 for v in merged.values()], alpha=0.7, edgecolors='white', linewidth=1.5)
for code, v in merged.items():
    ax.annotate(v['name'], (v['dea'], v['topsis']), fontsize=8, alpha=0.8)
ax.set_xlabel('DEA-BCC效率值', fontsize=12)
ax.set_ylabel('TOPSIS综合得分', fontsize=12)
ax.set_title('图5-9  DEA效率与TOPSIS绩效关系（气泡大小=运营年限）', fontsize=14, fontweight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)
ax.axvline(x=1.0, color=COLORS['dark_gray'], linestyle='--', alpha=0.3)
plt.tight_layout()
save_fig('图5-9')

print('\n--- 第六章 影响因素图表 ---')

# 图6-1: DEMATEL因果关系图（中心度vs原因度）
fig, ax = plt.subplots(figsize=(10, 8))
dims = dematel['dimension_names']
centers_list = dematel['center']  # list
causes_list = dematel['cause']  # list
# 转换为dict
centers = {dims[i]: centers_list[i] for i in range(len(dims))}
causes = {dims[i]: causes_list[i] for i in range(len(dims))}
# 四象限
ax.axhline(y=0, color=COLORS['dark_gray'], linestyle='-', alpha=0.3)
ax.axvline(x=np.mean(list(centers.values())), color=COLORS['dark_gray'], linestyle='-', alpha=0.3)
colors_demo = [COLORS['secondary1'], COLORS['secondary2'], COLORS['secondary3'], COLORS['secondary4']]
for i, (dim, c, m) in enumerate(zip(dims, causes.values(), centers.values())):
    ax.scatter(m, c, s=400, c=colors_demo[i], alpha=0.7, edgecolors='white', linewidth=2, zorder=5)
    ax.annotate(dim, (m, c), fontsize=11, ha='center', va='bottom' if c > 0 else 'top',
                fontweight='bold', xytext=(0, 15 if c > 0 else -15), textcoords='offset points')
ax.set_xlabel('中心度（影响度+被影响度）', fontsize=12)
ax.set_ylabel('原因度（影响度-被影响度）', fontsize=12)
ax.set_title('图6-1  DEMATEL中心度-原因度因果分类图', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(-7.5, 7.5)
# 添加象限标签
ax.text(ax.get_xlim()[1]*0.95, ax.get_ylim()[1]*0.9, '原因因素\n（高中心度+正原因度）', ha='right', va='top', fontsize=9, color=COLORS['secondary1'], alpha=0.7)
ax.text(ax.get_xlim()[0]*0.95, ax.get_ylim()[0]*0.9, '结果因素\n（高中心度+负原因度）', ha='left', va='bottom', fontsize=9, color=COLORS['secondary3'], alpha=0.7)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)
plt.tight_layout()
save_fig('图6-1')

# 图6-2: DEMATEL网络关系图
fig, ax = plt.subplots(figsize=(10, 8))
# 简化的网络可视化
node_positions = {
    '供给保障(C1)': (0.2, 0.8),
    '平台服务(C2)': (0.5, 0.6),
    '数据质量(C3)': (0.5, 0.3),
    '利用效果(C4)': (0.8, 0.1)
}
# 画边
arrows = [
    ('供给保障(C1)', '平台服务(C2)', 0.7),
    ('供给保障(C1)', '数据质量(C3)', 0.5),
    ('供给保障(C1)', '利用效果(C4)', 0.6),
    ('平台服务(C2)', '数据质量(C3)', 0.4),
    ('平台服务(C2)', '利用效果(C4)', 0.7),
    ('数据质量(C3)', '利用效果(C4)', 0.6),
]
for src, dst, strength in arrows:
    x1, y1 = node_positions[src]
    x2, y2 = node_positions[dst]
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=COLORS['primary'], lw=strength*3, alpha=0.7))
# 画节点
for name, (x, y) in node_positions.items():
    circle = plt.Circle((x, y), 0.08, color=COLORS['secondary3'], alpha=0.8, zorder=5)
    ax.add_patch(circle)
    ax.text(x, y, name.split('(')[0], ha='center', va='center', fontsize=10, fontweight='bold', color='white', zorder=6)
    # 中心度标签
    center_val = centers[name]
    ax.text(x, y-0.15, f'M={center_val:.2f}', ha='center', fontsize=9, color=COLORS['dark_gray'])
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1.0)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('图6-2  DEMATEL维度间因果关系网络图', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
save_fig('图6-2')

# 图6-3: fsQCA高绩效组态路径
fig, ax = plt.subplots(figsize=(12, 6))
configs = fsqca['configurations']
config_names = ['H1:0010\n质量单驱动', 'H2:1011\n供给-质量-利用', 'H3:1100\n供给-服务驱动', 'H4:1111\n全面均衡型']
coverages = [c['coverage'] for c in configs]
consistencies = [c['consistency'] for c in configs]
case_counts = [c['high_perf_count'] for c in configs]
x = np.arange(len(config_names))
width = 0.25
bars1 = ax.bar(x - width, coverages, width, label='覆盖度', color=COLORS['secondary3'], alpha=0.8)
bars2 = ax.bar(x, consistencies, width, label='一致性', color=COLORS['secondary2'], alpha=0.8)
bars3 = ax.bar(x + width, [c/10 for c in case_counts], width, label='案例数(÷10)', color=COLORS['secondary1'], alpha=0.8)
ax.set_ylabel('指标值', fontsize=12)
ax.set_title('图6-3  fsQCA高绩效组态路径对比', fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(config_names, fontsize=9)
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 1.1)
# 添加数值标签
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01, f'{height:.2f}', ha='center', va='bottom', fontsize=8)
plt.tight_layout()
save_fig('图6-3')

# 图6-4: fsQCA真值表热力图
fig, ax = plt.subplots(figsize=(10, 8))
all_configs = fsqca['all_configurations']
# 构建矩阵
matrix = np.zeros((8, 4))
labels = []
for i, c in enumerate(all_configs):
    row = i % 8
    matrix[row] = [c['C1_supply_bin'], c['C2_service_bin'], c['C3_quality_bin'], c['C4_usage_bin']]
    labels.append(f"{'●' if c['high_perf_count']>0 else '○'} {','.join(c['provinces'][:2])}")
im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
ax.set_xticks(range(4))
ax.set_xticklabels(['C1供给保障', 'C2平台服务', 'C3数据质量', 'C4利用效果'], fontsize=10)
ax.set_yticks(range(8))
ax.set_yticklabels([f"组态{i+1}" for i in range(8)], fontsize=10)
ax.set_title('图6-4  fsQCA真值表热力图（●=高绩效组态）', fontsize=14, fontweight='bold', pad=15)
# 添加文本
for i in range(8):
    for j in range(4):
        text = ax.text(j, i, f'{int(matrix[i, j])}', ha="center", va="center", color="black" if matrix[i,j] == 0 else "white", fontsize=11)
plt.colorbar(im, ax=ax, label='条件存在(1)/缺失(0)')
plt.tight_layout()
save_fig('图6-4')

# 图6-5: DEMATEL影响度/被影响度柱状图
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(4)
width = 0.35
R_vals = dematel['R']  # list
C_vals = dematel['C']  # list
bars1 = ax.bar(x - width/2, R_vals, width, label='影响度(R)', color=COLORS['secondary3'], alpha=0.8)
bars2 = ax.bar(x + width/2, C_vals, width, label='被影响度(C)', color=COLORS['secondary1'], alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(dims, fontsize=11)
ax.set_ylabel('数值', fontsize=12)
ax.set_title('图6-5  DEMATEL四维度影响度与被影响度对比', fontsize=14, fontweight='bold', pad=15)
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{height:.2f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
save_fig('图6-5')

print('\n--- 第一章 绪论图表 ---')

# 图1-4: 我国省级平台上线时间分布
fig, ax = plt.subplots(figsize=(12, 6))
years = [p[3] for p in platform_info]
year_counts = {}
for y in years:
    year_counts[y] = year_counts.get(y, 0) + 1
sorted_years = sorted(year_counts.keys())
counts_y = [year_counts[y] for y in sorted_years]
ax.bar(sorted_years, counts_y, color=COLORS['primary'], alpha=0.8, edgecolor='white', width=0.6)
ax.set_xlabel('上线年份', fontsize=12)
ax.set_ylabel('平台数量', fontsize=12)
ax.set_title('图1-4  我国省级政府数据开放平台上线时间分布', fontsize=14, fontweight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)
for i, (year, count) in enumerate(zip(sorted_years, counts_y)):
    ax.text(year, count + 0.1, str(count), ha='center', fontsize=10, fontweight='bold')
plt.tight_layout()
save_fig('图1-4')

# 图1-5: 样本平台区域分布饼图
fig, ax = plt.subplots(figsize=(8, 8))
region_counts = {}
for p in platform_info:
    r = p[2]
    region_counts[r] = region_counts.get(r, 0) + 1
regions_pie = list(region_counts.keys())
counts_pie = list(region_counts.values())
colors_pie = [COLORS['primary'], COLORS['secondary1'], COLORS['secondary2'], COLORS['secondary3'], COLORS['secondary4'], COLORS['secondary5'], '#4f81bd']
wedges, texts, autotexts = ax.pie(counts_pie, labels=regions_pie, autopct='%1.1f%%', colors=colors_pie,
                                   startangle=90, textprops={'fontsize': 11})
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight('bold')
ax.set_title('图1-5  样本平台所属区域分布', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
save_fig('图1-5')

print('\n--- 第四章 研究设计图表 ---')

# 图4-2: 样本平台区域分布（地图风格简化版）
fig, ax = plt.subplots(figsize=(12, 8))
# 简化的中国地图轮廓（用散点表示大致位置）
region_positions = {
    '华北': [(0.6, 0.7), (0.65, 0.6), (0.5, 0.55), (0.7, 0.5)],
    '东北': [(0.9, 0.8), (0.85, 0.7)],
    '华东': [(0.9, 0.4), (0.85, 0.3), (0.8, 0.35), (0.75, 0.4), (0.7, 0.35), (0.65, 0.4)],
    '华中': [(0.55, 0.4), (0.6, 0.35), (0.5, 0.35)],
    '华南': [(0.6, 0.2), (0.55, 0.15), (0.5, 0.1)],
    '西南': [(0.3, 0.3), (0.35, 0.35), (0.25, 0.2), (0.3, 0.15)],
    '西北': []
}
region_color_map = {'华北': COLORS['primary'], '东北': COLORS['secondary1'], '华东': COLORS['secondary2'],
                   '华中': COLORS['secondary3'], '华南': COLORS['secondary4'], '西南': COLORS['secondary5']}
for region, positions in region_positions.items():
    for pos in positions:
        ax.scatter(pos[0], pos[1], s=300, c=region_color_map[region], alpha=0.7, edgecolors='white', linewidth=2, zorder=5)
# 添加区域标签
label_positions = {'华北': (0.6, 0.75), '东北': (0.9, 0.85), '华东': (0.8, 0.45),
                  '华中': (0.55, 0.45), '华南': (0.55, 0.25), '西南': (0.3, 0.4)}
for region, pos in label_positions.items():
    ax.text(pos[0], pos[1], f'{region}\n({region_counts.get(region, 0)}个)', ha='center', fontsize=11,
            fontweight='bold', color=region_color_map[region],
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=region_color_map[region], alpha=0.8))
ax.set_xlim(0, 1.2)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('图4-2  22个样本平台区域分布示意图', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
save_fig('图4-2')

print('\n--- 第七章 对策建议图表 ---')

# 图7-3: 绩效提升路径图（横向流程图）
fig, ax = plt.subplots(figsize=(14, 4))
steps = ['问题诊断', '路径识别', '策略匹配', '措施实施', '效果评估']
x_positions = np.linspace(0.1, 0.9, len(steps))
for i, (step, x) in enumerate(zip(steps, x_positions)):
    circle = plt.Circle((x, 0.5), 0.08, color=COLORS['primary'] if i == 0 else COLORS['secondary3'], alpha=0.8, zorder=5)
    ax.add_patch(circle)
    ax.text(x, 0.5, str(i+1), ha='center', va='center', fontsize=14, fontweight='bold', color='white', zorder=6)
    ax.text(x, 0.3, step, ha='center', va='top', fontsize=11, fontweight='bold')
    if i < len(steps) - 1:
        ax.annotate('', xy=(x_positions[i+1]-0.08, 0.5), xytext=(x+0.08, 0.5),
                    arrowprops=dict(arrowstyle='->', color=COLORS['dark_gray'], lw=2))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('图7-3  平台绩效提升五步路径', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
save_fig('图7-3')

# 图7-4: 政策建议优先级矩阵
fig, ax = plt.subplots(figsize=(10, 8))
ax.axhline(y=0.5, color=COLORS['dark_gray'], linestyle='--', alpha=0.3)
ax.axvline(x=0.5, color=COLORS['dark_gray'], linestyle='--', alpha=0.3)
# 四个象限的内容
measures = {
    '高紧迫+高影响': ['建立数据质量标准', '完善API服务体系', '优化检索功能'],
    '高紧迫+低影响': ['更新平台界面', '修复失效链接', '补充元数据'],
    '低紧迫+高影响': ['培育数据利用生态', '建立授权运营机制', '推进数据要素化'],
    '低紧迫+低影响': ['国际化界面', '多语言支持', '无障碍设计']
}
colors_quad = {
    '高紧迫+高影响': COLORS['secondary1'],
    '高紧迫+低影响': COLORS['secondary4'],
    '低紧迫+高影响': COLORS['secondary3'],
    '低紧迫+低影响': COLORS['secondary2']
}
positions = {'高紧迫+高影响': (0.75, 0.75), '高紧迫+低影响': (0.25, 0.75),
             '低紧迫+高影响': (0.75, 0.25), '低紧迫+低影响': (0.25, 0.25)}
for quad, items in measures.items():
    x, y = positions[quad]
    ax.text(x, y + 0.1, quad, ha='center', fontsize=12, fontweight='bold', color=colors_quad[quad])
    for i, item in enumerate(items):
        ax.text(x, y - i*0.05, f'• {item}', ha='center', fontsize=10, color=COLORS['dark_gray'])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel('实施紧迫性 →', fontsize=12)
ax.set_ylabel('影响程度 →', fontsize=12)
ax.set_title('图7-4  政策建议优先级矩阵', fontsize=14, fontweight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
save_fig('图7-4')

print('\n' + '=' * 60)
print('图表生成完成！')
print(f'输出目录: {OUTPUT_DIR}')
print('=' * 60)

# 列出所有生成的文件
import os
files = sorted(os.listdir(OUTPUT_DIR))
print(f'\n共生成 {len(files)} 张图表:')
for f in files:
    size = os.path.getsize(OUTPUT_DIR / f) / 1024
    print(f'  {f} ({size:.1f} KB)')
