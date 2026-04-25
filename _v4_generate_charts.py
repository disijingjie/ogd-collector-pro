"""
V4 配套图表生成脚本
生成论文所需的全套可视化图表
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 加载数据
with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
    collection_results = json.load(f)

topsis = pd.read_csv('data/v3_topsis_results_v2.csv')
dea = pd.read_csv('data/v3_dea_results.csv')
dematel = pd.read_csv('data/v3_dematel_results.csv')
fsqca = pd.read_csv('data/v3_fsqca_results.csv')

# 设置图表风格
plt.style.use('seaborn-v0_8-whitegrid')

# ========== 图表1: 31省平台类型分布饼图 ==========
fig, ax = plt.subplots(figsize=(10, 8))
labels = ['独立平台\n(正常运行18个)', '独立平台\n(维护/转型3个)', '登记/运营平台\n(2个)', '无独立平台\n(8个)']
sizes = [18, 3, 2, 8]
colors = ['#3b82f6', '#f59e0b', '#10b981', '#ef4444']
explode = (0.05, 0, 0, 0)
ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
       shadow=True, startangle=90, textprops={'fontsize': 12})
ax.set_title('图5-1 31个省级行政区数据开放平台建设状态分布', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('static/thesis_01_platform_types.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ thesis_01_platform_types.png")

# ========== 图表2: 22省标准化数据集数量条形图 ==========
fig, ax = plt.subplots(figsize=(14, 8))
topsis_sorted = topsis.sort_values('standardized_count', ascending=True)
colors_bar = ['#3b82f6' if s >= 10000 else '#60a5fa' if s >= 5000 else '#93c5fd' 
              for s in topsis_sorted['standardized_count']]
bars = ax.barh(range(len(topsis_sorted)), topsis_sorted['standardized_count'], color=colors_bar)
ax.set_yticks(range(len(topsis_sorted)))
ax.set_yticklabels(topsis_sorted['name'], fontsize=10)
ax.set_xlabel('标准化数据集数量', fontsize=12)
ax.set_title('图5-2 22个省级平台标准化数据集数量排名', fontsize=14, fontweight='bold')
ax.axvline(x=topsis_sorted['standardized_count'].median(), color='red', linestyle='--', 
           label=f'中位数: {topsis_sorted["standardized_count"].median():.0f}')
ax.legend()
plt.tight_layout()
plt.savefig('static/thesis_02_dataset_ranking.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ thesis_02_dataset_ranking.png")

# ========== 图表3: TOPSIS得分排名 ==========
fig, ax = plt.subplots(figsize=(14, 8))
topsis_score_sorted = topsis.sort_values('topsis_score', ascending=True)
colors_topsis = ['#ef4444' if s < 0.18 else '#f59e0b' if s < 0.4 else '#22c55e' 
                 for s in topsis_score_sorted['topsis_score']]
ax.barh(range(len(topsis_score_sorted)), topsis_score_sorted['topsis_score'], color=colors_topsis)
ax.set_yticks(range(len(topsis_score_sorted)))
ax.set_yticklabels(topsis_score_sorted['name'], fontsize=10)
ax.set_xlabel('TOPSIS得分', fontsize=12)
ax.set_title('图5-3 TOPSIS绩效评估排名', fontsize=14, fontweight='bold')
ax.axvline(x=0.18, color='gray', linestyle='--', alpha=0.7, label='绩效门槛(0.18)')
ax.axvline(x=0.4, color='gray', linestyle='--', alpha=0.7, label='高分门槛(0.4)')
ax.legend()
plt.tight_layout()
plt.savefig('static/thesis_03_topsis_ranking.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ thesis_03_topsis_ranking.png")

# ========== 图表4: 四大区域对比 ==========
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 区域均值
regions = {'东部': ['guangdong', 'shandong', 'zhejiang', 'hainan', 'shanghai', 'fujian', 'jiangsu', 'tianjin', 'beijing'],
           '中部': ['hubei', 'hunan', 'jiangxi', 'henan', 'shanxi', 'anhui'],
           '西部': ['chongqing', 'sichuan', 'guizhou', 'guangxi', 'yunnan', 'gansu'],
           '东北': ['liaoning', 'jilin', 'heilongjiang']}

region_data = {}
for region, codes in regions.items():
    region_vals = []
    for code in codes:
        row = topsis[topsis['code'] == code]
        if len(row) > 0:
            region_vals.append(row['topsis_score'].values[0])
    region_data[region] = region_vals

ax1 = axes[0]
box_data = [region_data[r] for r in ['东部', '中部', '西部', '东北']]
bp = ax1.boxplot(box_data, labels=['东部', '中部', '西部', '东北'], patch_artist=True)
for patch, color in zip(bp['boxes'], ['#3b82f6', '#f59e0b', '#10b981', '#ef4444']):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax1.set_ylabel('TOPSIS得分', fontsize=12)
ax1.set_title('(a) 四大区域TOPSIS得分箱线图', fontsize=12)

ax2 = axes[1]
region_means = {r: np.mean(v) if v else 0 for r, v in region_data.items()}
ax2.bar(region_means.keys(), region_means.values(), 
        color=['#3b82f6', '#f59e0b', '#10b981', '#ef4444'], alpha=0.8)
ax2.set_ylabel('平均TOPSIS得分', fontsize=12)
ax2.set_title('(b) 四大区域平均绩效对比', fontsize=12)

plt.suptitle('图5-4 省级平台绩效的区域差异', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('static/thesis_04_region_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ thesis_04_region_comparison.png")

# ========== 图表5: DEMATEL因果图 ==========
fig, ax = plt.subplots(figsize=(10, 8))
factors = ['政策法规\n(PL)', '组织保障\n(OG)', '平台建设\n(PC)', '数据质量\n(DQ)', '应用效果\n(AE)']
centrality = [-2.916, -2.783, -2.767, -2.986, -3.034]
causality = [0.000, -0.000, 0.000, -0.000, 0.000]  # 近似值
colors_dematel = ['#22c55e' if c >= 0 else '#f59e0b' for c in causality]

ax.scatter(centrality, causality, s=500, c=colors_dematel, alpha=0.7, edgecolors='black', linewidth=2)
for i, factor in enumerate(factors):
    ax.annotate(factor, (centrality[i], causality[i]), 
                xytext=(10, 10), textcoords='offset points', fontsize=11, fontweight='bold')

ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax.axvline(x=np.mean(centrality), color='black', linestyle='-', linewidth=0.5)
ax.set_xlabel('中心度 (Centrality)', fontsize=12)
ax.set_ylabel('原因度 (Causality)', fontsize=12)
ax.set_title('图6-1 DEMATEL因素因果关系图', fontsize=14, fontweight='bold')

# 添加象限标签
ax.text(-2.8, 0.5, '原因因素\n(驱动力)', fontsize=10, ha='center', 
        bbox=dict(boxstyle='round', facecolor='#22c55e', alpha=0.3))
ax.text(-2.8, -0.5, '结果因素\n(被动响应)', fontsize=10, ha='center',
        bbox=dict(boxstyle='round', facecolor='#f59e0b', alpha=0.3))

plt.tight_layout()
plt.savefig('static/thesis_05_dematel_causal.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ thesis_05_dematel_causal.png")

# ========== 图表6: fsQCA组态热力图 ==========
fig, ax = plt.subplots(figsize=(12, 8))

# 准备热力图数据
fsqca_sorted = fsqca.sort_values('topsis_score', ascending=False)
conditions = ['pl', 'og', 'pc', 'dq', 'ae', 'op']
condition_labels = ['政策法规\n(PL)', '组织保障\n(OG)', '平台建设\n(PC)', 
                    '数据质量\n(DQ)', '应用效果\n(AE)', '开放程度\n(OP)']

heatmap_data = []
for _, row in fsqca_sorted.iterrows():
    heatmap_data.append([row[c] for c in conditions])

im = ax.imshow(heatmap_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
ax.set_xticks(range(len(conditions)))
ax.set_xticklabels(condition_labels, fontsize=10)
ax.set_yticks(range(len(fsqca_sorted)))
ax.set_yticklabels(fsqca_sorted['name'], fontsize=9)

# 添加数值标注
for i in range(len(fsqca_sorted)):
    for j in range(len(conditions)):
        text = ax.text(j, i, int(heatmap_data[i][j]), ha="center", va="center", 
                      color="black" if heatmap_data[i][j] == 1 else "gray", fontsize=8)

ax.set_title('图6-2 fsQCA组态分析热力图', fontsize=14, fontweight='bold', pad=20)
plt.colorbar(im, ax=ax, label='条件状态 (0=缺失, 1=存在)')
plt.tight_layout()
plt.savefig('static/thesis_06_fsqca_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ thesis_06_fsqca_heatmap.png")

# ========== 图表7: 数据集数量分布直方图 ==========
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(topsis['standardized_count'], bins=15, color='#3b82f6', alpha=0.7, edgecolor='black')
ax.axvline(x=topsis['standardized_count'].mean(), color='red', linestyle='--', 
           label=f'均值: {topsis["standardized_count"].mean():.0f}')
ax.axvline(x=topsis['standardized_count'].median(), color='green', linestyle='--',
           label=f'中位数: {topsis["standardized_count"].median():.0f}')
ax.set_xlabel('标准化数据集数量', fontsize=12)
ax.set_ylabel('平台数量', fontsize=12)
ax.set_title('图5-5 数据集数量分布直方图', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('static/thesis_07_distribution_hist.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ thesis_07_distribution_hist.png")

# ========== 图表8: DEA效率 vs TOPSIS得分 散点图 ==========
fig, ax = plt.subplots(figsize=(10, 8))
merged = pd.merge(topsis[['code', 'name', 'topsis_score']], 
                  dea[['code', 'dea_efficiency']], on='code')
ax.scatter(merged['dea_efficiency'], merged['topsis_score'], s=200, alpha=0.6, c='#3b82f6', edgecolors='black')

for _, row in merged.iterrows():
    ax.annotate(row['name'], (row['dea_efficiency'], row['topsis_score']),
                xytext=(5, 5), textcoords='offset points', fontsize=8)

ax.set_xlabel('DEA效率', fontsize=12)
ax.set_ylabel('TOPSIS得分', fontsize=12)
ax.set_title('图5-6 DEA效率与TOPSIS得分关系', fontsize=14, fontweight='bold')

# 添加趋势线
z = np.polyfit(merged['dea_efficiency'], merged['topsis_score'], 1)
p = np.poly1d(z)
ax.plot(merged['dea_efficiency'].sort_values(), p(merged['dea_efficiency'].sort_values()), 
        "r--", alpha=0.8, label=f'趋势线')
ax.legend()
plt.tight_layout()
plt.savefig('static/thesis_08_dea_topsis_scatter.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ thesis_08_dea_topsis_scatter.png")

# ========== 图表9: 绩效梯队分布 ==========
fig, ax = plt.subplots(figsize=(10, 6))
topsis['tier'] = topsis['topsis_score'].apply(lambda x: '第一梯队(>0.4)' if x > 0.4 
                                              else '第二梯队(0.18-0.4)' if x >= 0.18 
                                              else '第三梯队(<0.18)')
tier_counts = topsis['tier'].value_counts()
colors_tier = ['#22c55e', '#f59e0b', '#ef4444']
wedges, texts, autotexts = ax.pie(tier_counts.values, labels=tier_counts.index, 
                                   colors=colors_tier, autopct='%1.1f%%',
                                   startangle=90, textprops={'fontsize': 11})
ax.set_title('图5-7 平台绩效梯队分布', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('static/thesis_09_tier_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ thesis_09_tier_distribution.png")

# ========== 图表10: 8省替代开放形式 ==========
fig, ax = plt.subplots(figsize=(12, 6))
provinces_no_platform = ['甘肃省', '河北省', '黑龙江省', '宁夏回族自治区', 
                         '青海省', '陕西省', '新疆维吾尔自治区', '西藏自治区']
forms = ['政务服务网', '数据局官网', '登记平台', '数据条例', 
         '政务服务网', '数据局官网', '政务服务网', '无']
colors_form = ['#3b82f6', '#60a5fa', '#10b981', '#f59e0b', 
               '#3b82f6', '#60a5fa', '#3b82f6', '#9ca3af']
bars = ax.bar(range(len(provinces_no_platform)), [1]*8, color=colors_form, alpha=0.8)
ax.set_xticks(range(len(provinces_no_platform)))
ax.set_xticklabels(provinces_no_platform, rotation=45, ha='right', fontsize=9)
ax.set_ylabel('是否有替代开放形式', fontsize=12)
ax.set_title('图5-8 8个无独立平台省份的替代开放形式', fontsize=14, fontweight='bold')
ax.set_yticks([])

# 添加标签
for i, (province, form) in enumerate(zip(provinces_no_platform, forms)):
    ax.text(i, 0.5, form, ha='center', va='center', fontsize=9, fontweight='bold', color='white')

plt.tight_layout()
plt.savefig('static/thesis_10_alternative_forms.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ thesis_10_alternative_forms.png")

print("\n🎉 全部10张论文配套图表生成完成！")
print("📁 保存位置: static/thesis_01~10.png")
