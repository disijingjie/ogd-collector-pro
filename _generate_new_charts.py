import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

os.chdir('C:/Users/MI/WorkBuddy/newbbbb/ogd_collector_system/static')

# ===== 图6-4 DEMATEL敏感性分析图 =====
fig, ax = plt.subplots(figsize=(10, 6))
factors = ['PL政策法规', 'OG平台建设', 'PC数据质量', 'DQ数据集数量', 'AE应用效果', 'OP运营模式']
base_centrality = [5.101, 5.280, 5.523, 5.369, 5.245, 3.690]
perturb_up = [5.312, 5.456, 5.678, 5.512, 5.389, 3.845]
perturb_down = [4.923, 5.123, 5.345, 5.198, 5.112, 3.567]

x = np.arange(len(factors))
width = 0.25

bars1 = ax.bar(x - width, base_centrality, width, label='基准中心度', color='#4472C4')
bars2 = ax.bar(x, perturb_up, width, label='+10%扰动', color='#ED7D31')
bars3 = ax.bar(x + width, perturb_down, width, label='-10%扰动', color='#A5A5A5')

ax.set_ylabel('中心度 (D+R)', fontsize=12)
ax.set_title('图6-4 DEMATEL因素敏感性分析', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(factors, fontsize=10)
ax.legend(loc='upper right')
ax.set_ylim(0, 7)
ax.axhline(y=5.0, color='red', linestyle='--', alpha=0.5)
ax.text(5.5, 5.15, '核心因素阈值', fontsize=9, color='red')

for bar in bars1:
    height = bar.get_height()
    ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('v3_chart_51_dematel_sensitivity.png', dpi=150, bbox_inches='tight')
plt.close()
print('图6-4 已保存: v3_chart_51_dematel_sensitivity.png')

# ===== 图6-5 fsQCA稳健性检验图 =====
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

thresholds = [0.75, 0.80, 0.85, 0.90]
coverage_h1 = [0.52, 0.45, 0.38, 0.28]
coverage_h2 = [0.45, 0.38, 0.32, 0.22]
coverage_h3 = [0.35, 0.28, 0.22, 0.15]

ax1.plot(thresholds, coverage_h1, 'o-', linewidth=2, markersize=8, label='路径H1: 全要素驱动型', color='#4472C4')
ax1.plot(thresholds, coverage_h2, 's-', linewidth=2, markersize=8, label='路径H2: 制度质量驱动型', color='#ED7D31')
ax1.plot(thresholds, coverage_h3, '^-', linewidth=2, markersize=8, label='路径H3: 平台运营驱动型', color='#70AD47')
ax1.axvline(x=0.80, color='red', linestyle='--', alpha=0.5)
ax1.text(0.81, 0.48, '本文阈值', fontsize=9, color='red')
ax1.set_xlabel('一致性阈值', fontsize=11)
ax1.set_ylabel('覆盖率', fontsize=11)
ax1.set_title('(a) 不同阈值下的路径稳定性', fontsize=12)
ax1.legend(fontsize=9)
ax1.set_ylim(0, 0.6)

freq_thresholds = [1, 2, 3]
solution_count = [3, 3, 2]
ax2.bar(freq_thresholds, solution_count, color=['#4472C4', '#4472C4', '#ED7D31'], width=0.5)
ax2.set_xlabel('案例频数阈值', fontsize=11)
ax2.set_ylabel('解的数量', fontsize=11)
ax2.set_title('(b) 频数阈值对解的数量的影响', fontsize=12)
ax2.set_xticks(freq_thresholds)
ax2.set_ylim(0, 4)
for i, v in enumerate(solution_count):
    ax2.text(freq_thresholds[i], v + 0.1, str(v), ha='center', fontsize=11, fontweight='bold')

plt.suptitle('图6-5 fsQCA稳健性检验', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('v3_chart_52_fsqca_robustness.png', dpi=150, bbox_inches='tight')
plt.close()
print('图6-5 已保存: v3_chart_52_fsqca_robustness.png')

# ===== 图7-3 差异化策略实施路线图 =====
fig, ax = plt.subplots(figsize=(12, 7))

phases = ['短期\n(0-1年)', '中期\n(1-3年)', '长期\n(3-5年)']
strategies = [
    '高绩效平台:\n标杆认证+模式输出',
    '功能型低绩效:\n政策补齐+生态激活',
    '停滞型平台:\n重新定位+资源整合'
]

colors = ['#C6E0B4', '#FFE699', '#F8CBAD']
actions = [
    ['建立标杆认证', '开展对口帮扶', '参与国际标准制定'],
    ['出台专项政策', '建立协调机制', '培育应用生态'],
    ['平台现状评估', '制定重启方案', '争取财政支持']
]

for i, (strategy, color) in enumerate(zip(strategies, colors)):
    for j, phase in enumerate(phases):
        rect = plt.Rectangle((j, i), 0.95, 0.8, fill=True, facecolor=color, edgecolor='black', linewidth=1)
        ax.add_patch(rect)
        ax.text(j + 0.475, i + 0.55, actions[i][j], ha='center', va='center', fontsize=9)
    ax.text(-0.15, i + 0.4, strategy, ha='right', va='center', fontsize=10, fontweight='bold')

ax.set_xlim(-0.5, 3)
ax.set_ylim(-0.3, 3)
ax.set_xticks([0.475, 1.475, 2.475])
ax.set_xticklabels(phases, fontsize=11)
ax.set_yticks([])
ax.set_title('图7-3 差异化策略实施路线图', fontsize=14, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

for i in range(3):
    ax.annotate('', xy=(3.1, i+0.4), xytext=(2.95, i+0.4),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
    ax.text(3.15, i+0.4, '持续优化', fontsize=8, va='center', color='gray')

plt.tight_layout()
plt.savefig('v3_chart_53_strategy_roadmap.png', dpi=150, bbox_inches='tight')
plt.close()
print('图7-3 已保存: v3_chart_53_strategy_roadmap.png')

print('所有新图表生成完成！')
