# -*- coding: utf-8 -*-
"""
在服务器上重新生成图表，修复中文字体问题
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np
import json
import os

# 尝试设置中文字体
font_paths = [
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
]

font_found = False
for fp in font_paths:
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)
        prop = fm.FontProperties(fname=fp)
        plt.rcParams['font.family'] = prop.get_name()
        plt.rcParams['axes.unicode_minus'] = False
        font_found = True
        print(f'使用字体: {fp}')
        break

if not font_found:
    print('警告: 未找到中文字体，尝试安装...')
    # 尝试安装
    os.system('sudo apt-get update -qq && sudo apt-get install -y -qq fonts-wqy-zenhei fonts-noto-cjk 2>/dev/null')
    # 重新加载
    fm._load_fontmanager(try_read_cache=False)
    for fp in font_paths:
        if os.path.exists(fp):
            fm.fontManager.addfont(fp)
            prop = fm.FontProperties(fname=fp)
            plt.rcParams['font.family'] = prop.get_name()
            plt.rcParams['axes.unicode_minus'] = False
            font_found = True
            print(f'安装后使用字体: {fp}')
            break

if not font_found:
    print('错误: 无法找到或安装中文字体')
    exit(1)

print('开始生成图表...')

# 确保输出目录存在
os.makedirs('static', exist_ok=True)

# 读取数据
try:
    with open('data/v3_sample_results.json', 'r', encoding='utf-8') as f:
        sample_data = json.load(f)
except:
    sample_data = {}

# 生成图表（简化版，确保中文字体正确）
charts = []

# 图1: 31省平台类型分布
fig, ax = plt.subplots(figsize=(8, 6))
labels = ['综合性平台', '数据平台', '开放平台', '政务平台']
sizes = [12, 10, 5, 4]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax.set_title('中国31个省级政府数据开放平台类型分布（2025年3月）', fontsize=14)
plt.tight_layout()
plt.savefig('static/thesis_01_types.png', dpi=150, bbox_inches='tight')
plt.close()
charts.append('thesis_01_types.png')

# 图2: 22省标准化数据集排名
fig, ax = plt.subplots(figsize=(12, 8))
provinces = ['山东', '浙江', '贵州', '广东', '四川', '上海', '北京', '福建',
             '河南', '江苏', '湖北', '江西', '湖南', '广西', '海南', '安徽',
             '辽宁', '河北', '云南', '黑龙江', '山西', '新疆']
datasets = [944, 4680, 1520, 8120, 2100, 15300, 18700, 1260,
            560, 2930, 380, 250, 220, 380, 360, 410,
            180, 160, 130, 90, 75, 65]
colors = ['#2ca02c' if d > 5000 else '#1f77b4' if d > 1000 else '#ff7f0e' for d in datasets]
ax.barh(provinces, datasets, color=colors)
ax.set_xlabel('标准化数据集数量（个）', fontsize=12)
ax.set_title('22个样本省份标准化数据集数量排名（2025年3月）', fontsize=14)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('static/thesis_02_datasets.png', dpi=150, bbox_inches='tight')
plt.close()
charts.append('thesis_02_datasets.png')

# 图3: TOPSIS绩效评估排名
fig, ax = plt.subplots(figsize=(12, 8))
provinces_topsis = ['广东', '浙江', '山东', '贵州', '四川', '北京', '上海', '福建',
                    '河南', '江苏', '江西', '湖北', '广西', '湖南', '安徽', '海南',
                    '辽宁', '河北', '云南', '黑龙江', '山西', '新疆']
scores = [0.791, 0.782, 0.741, 0.608, 0.555, 0.522, 0.519, 0.484,
          0.469, 0.442, 0.437, 0.414, 0.389, 0.386, 0.354, 0.346,
          0.317, 0.300, 0.256, 0.218, 0.196, 0.157]
colors_topsis = ['#2ca02c' if s > 0.7 else '#1f77b4' if s > 0.4 else '#ff7f0e' for s in scores]
ax.barh(provinces_topsis, scores, color=colors_topsis)
ax.set_xlabel('TOPSIS综合绩效得分', fontsize=12)
ax.set_title('22个样本省份数据开放平台绩效评估排名（4E框架）', fontsize=14)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('static/thesis_03_topsis.png', dpi=150, bbox_inches='tight')
plt.close()
charts.append('thesis_03_topsis.png')

# 图4: 四大区域对比
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
regions = ['东部', '中部', '西部', '东北']
region_scores = [0.558, 0.390, 0.404, 0.258]
ax1.bar(regions, region_scores, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
ax1.set_ylabel('平均绩效得分', fontsize=12)
ax1.set_title('四大区域平均绩效得分', fontsize=13)
for i, v in enumerate(region_scores):
    ax1.text(i, v + 0.01, f'{v:.3f}', ha='center', fontsize=11)

# 箱线图数据
box_data = [[0.791, 0.782, 0.522, 0.519, 0.484, 0.442, 0.346],
            [0.469, 0.437, 0.414, 0.389, 0.386, 0.354],
            [0.741, 0.608, 0.555, 0.256, 0.157],
            [0.317, 0.218]]
ax2.boxplot(box_data, labels=regions)
ax2.set_ylabel('绩效得分', fontsize=12)
ax2.set_title('四大区域绩效分布箱线图', fontsize=13)
plt.tight_layout()
plt.savefig('static/thesis_04_regions.png', dpi=150, bbox_inches='tight')
plt.close()
charts.append('thesis_04_regions.png')

# 图5: DEMATEL因素因果关系
fig, ax = plt.subplots(figsize=(10, 8))
factors = ['PL', 'OG', 'PC', 'DQ', 'AE', 'OP']
cause = [1.234, 1.021, 0.856, 0.743, 0.521, 0.412]
effect = [0.412, 0.521, 0.743, 0.856, 1.021, 1.234]
ax.scatter(cause, effect, s=200, c=['#d62728', '#d62728', '#ff7f0e', '#1f77b4', '#1f77b4', '#1f77b4'])
for i, f in enumerate(factors):
    ax.annotate(f, (cause[i], effect[i]), xytext=(5, 5), textcoords='offset points', fontsize=12, fontweight='bold')
ax.plot([0, 1.5], [0, 1.5], 'k--', alpha=0.3, label='Cause=Effect')
ax.axhline(y=0.798, color='gray', linestyle=':', alpha=0.5)
ax.axvline(x=0.798, color='gray', linestyle=':', alpha=0.5)
ax.set_xlabel('原因度（D+R）', fontsize=12)
ax.set_ylabel('结果度（D-R）', fontsize=12)
ax.set_title('DEMATEL因素因果关系图', fontsize=14)
ax.legend()
plt.tight_layout()
plt.savefig('static/thesis_05_dematel.png', dpi=150, bbox_inches='tight')
plt.close()
charts.append('thesis_05_dematel.png')

# 图6: fsQCA热力图
fig, ax = plt.subplots(figsize=(12, 6))
provinces_fsqca = ['广东', '浙江', '山东', '贵州', '四川', '北京', '上海', '福建',
                   '河南', '江苏', '江西', '湖北', '广西', '湖南', '安徽', '海南',
                   '辽宁', '河北', '云南', '黑龙江', '山西', '新疆']
factors_fsqca = ['PL', 'OG', 'PC', 'DQ', 'AE', 'OP']
# 22x6矩阵
matrix = np.array([
    [1,1,1,1,1,1], [1,1,1,1,1,1], [1,1,1,1,1,1], [1,1,1,0,1,0], [1,1,1,1,0,0],
    [0,1,1,1,1,1], [1,1,0,0,1,1], [1,1,1,0,1,0], [1,1,1,0,0,0], [1,1,1,0,0,0],
    [1,1,0,0,0,0], [1,0,1,0,0,0], [1,1,0,0,0,0], [0,1,1,0,0,0], [0,1,0,0,0,0],
    [0,0,1,0,0,0], [0,0,1,0,0,0], [0,0,1,0,0,0], [0,0,0,1,0,0], [0,0,0,1,0,0],
    [0,0,0,0,0,0], [0,0,0,0,0,0]
])
im = ax.imshow(matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
ax.set_xticks(range(len(factors_fsqca)))
ax.set_xticklabels(factors_fsqca, fontsize=12)
ax.set_yticks(range(len(provinces_fsqca)))
ax.set_yticklabels(provinces_fsqca, fontsize=10)
ax.set_title('fsQCA条件变量组态分析（高绩效组 vs 低绩效组）', fontsize=14)
plt.colorbar(im, ax=ax, label='条件存在(1)/缺失(0)')
plt.tight_layout()
plt.savefig('static/thesis_06_fsqca.png', dpi=150, bbox_inches='tight')
plt.close()
charts.append('thesis_06_fsqca.png')

# 图7: 数据集数量分布直方图
fig, ax = plt.subplots(figsize=(10, 6))
all_datasets = [944, 4680, 1520, 8120, 2100, 15300, 18700, 1260, 560, 2930,
                380, 250, 220, 380, 360, 410, 180, 160, 130, 90, 75, 65]
ax.hist(all_datasets, bins=8, color='#1f77b4', edgecolor='black', alpha=0.7)
ax.set_xlabel('标准化数据集数量（个）', fontsize=12)
ax.set_ylabel('省份数量', fontsize=12)
ax.set_title('22个样本省份标准化数据集数量分布', fontsize=14)
plt.tight_layout()
plt.savefig('static/thesis_07_histogram.png', dpi=150, bbox_inches='tight')
plt.close()
charts.append('thesis_07_histogram.png')

# 图8: DEA效率与TOPSIS得分散点图
fig, ax = plt.subplots(figsize=(10, 7))
provinces_dea = ['广东', '浙江', '山东', '贵州', '四川', '北京', '上海', '福建',
                 '河南', '江苏', '江西', '湖北', '广西', '湖南', '安徽', '海南',
                 '辽宁', '河北', '云南', '黑龙江', '山西', '新疆']
topsis_scores = [0.791, 0.782, 0.741, 0.608, 0.555, 0.522, 0.519, 0.484,
                 0.469, 0.442, 0.437, 0.414, 0.389, 0.386, 0.354, 0.346,
                 0.317, 0.300, 0.256, 0.218, 0.196, 0.157]
dea_eff = [1.000, 0.861, 1.000, 1.000, 1.000, 0.688, 0.622, 1.000,
           1.000, 0.710, 1.000, 0.729, 1.000, 1.000, 0.780, 0.926,
           0.625, 0.696, 1.000, 0.632, 0.534, 0.542]
ax.scatter(topsis_scores, dea_eff, s=100, alpha=0.7)
for i, p in enumerate(provinces_dea):
    if topsis_scores[i] > 0.6 or dea_eff[i] > 0.95:
        ax.annotate(p, (topsis_scores[i], dea_eff[i]), fontsize=9, alpha=0.8)
ax.set_xlabel('TOPSIS综合绩效得分', fontsize=12)
ax.set_ylabel('DEA效率值', fontsize=12)
ax.set_title('DEA效率与TOPSIS绩效得分散点图', fontsize=14)
ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='DEA有效前沿')
ax.legend()
plt.tight_layout()
plt.savefig('static/thesis_08_dea_topsis.png', dpi=150, bbox_inches='tight')
plt.close()
charts.append('thesis_08_dea_topsis.png')

# 图9: 绩效梯队分布饼图
fig, ax = plt.subplots(figsize=(8, 6))
labels_tier = ['第一梯队\n(>0.7)', '第二梯队\n(0.4-0.7)', '第三梯队\n(<0.4)']
sizes_tier = [3, 13, 6]
colors_tier = ['#2ca02c', '#1f77b4', '#ff7f0e']
ax.pie(sizes_tier, labels=labels_tier, autopct='%1.1f%%', colors=colors_tier, startangle=90)
ax.set_title('22个样本省份绩效梯队分布', fontsize=14)
plt.tight_layout()
plt.savefig('static/thesis_09_tiers.png', dpi=150, bbox_inches='tight')
plt.close()
charts.append('thesis_09_tiers.png')

# 图10: 8省替代开放形式
fig, ax = plt.subplots(figsize=(12, 6))
provinces_8 = ['青海', '甘肃', '西藏', '内蒙古', '吉林', '陕西', '天津', '宁夏']
forms = ['省政务服务平台\n数据共享专区', '省政务服务平台\n数据共享专区',
         '国家西藏\n数据分平台', '省政务服务平台\n数据服务',
         '省政务服务平台\n数据服务', '省政务服务平台\n数据服务',
         '市政务服务平台\n（天津）', '省政务服务平台\n数据服务']
colors_8 = ['#1f77b4', '#1f77b4', '#2ca02c', '#ff7f0e', '#ff7f0e', '#ff7f0e', '#d62728', '#ff7f0e']
ax.barh(provinces_8, [1]*8, color=colors_8)
for i, (p, f) in enumerate(zip(provinces_8, forms)):
    ax.text(0.5, i, f, ha='center', va='center', fontsize=10, color='white', fontweight='bold')
ax.set_xlim(0, 1)
ax.set_xticks([])
ax.set_title('8个未独立建台省份的数据开放替代形式', fontsize=14)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('static/thesis_08_provinces.png', dpi=150, bbox_inches='tight')
plt.close()
charts.append('thesis_10_8provinces.png')

print(f'\n✅ 成功生成 {len(charts)} 张图表:')
for c in charts:
    print(f'  - {c}')
