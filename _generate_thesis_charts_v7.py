"""
博士论文图表v7修复版
修复问题：
1. 图3-1: 4E评估指标体系结构 - 字太小
2. 图4-1: 研究技术路线 - 错误太多、字太小
3. 图5-3: 绩效-效率四象限 - 内容错误
4. 图7-2: 差异化优化策略矩阵 - 字太小
5. 图7-3: 差异化策略实施路线图 - 字太小

技术规格：
- 画布: 1920×1440 (更大画布以便放大字体)
- DPI: 400
- 标题: 24px bold
- 正文: 16-18px
- 中文字体: SimHei/SimSun
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import pandas as pd
import numpy as np
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = "static/thesis_charts_v7"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==================== 图3-1: 4E评估指标体系结构 ====================
def generate_fig3_1():
    fig, ax = plt.subplots(1, 1, figsize=(24, 18), dpi=400)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 18)
    ax.axis('off')
    ax.set_title('图3-1  4E评估指标体系结构', fontsize=28, fontweight='bold', pad=30)

    # 总目标层
    rect_goal = FancyBboxPatch((8, 15.5), 8, 1.5, boxstyle="round,pad=0.1", 
                                facecolor='#1a5276', edgecolor='black', linewidth=2)
    ax.add_patch(rect_goal)
    ax.text(12, 16.25, '总目标层：数据利用绩效', ha='center', va='center', 
            fontsize=20, fontweight='bold', color='white')

    # 一级维度层
    dims = [
        ('供给保障\n(E1)', '#2874a6', 1.5),
        ('平台服务\n(E2)', '#2874a6', 5.5),
        ('数据质量\n(E3)', '#2874a6', 9.5),
        ('利用效果\n(E4)', '#2874a6', 13.5),
        ('公平性\n(E5)', '#2874a6', 17.5),
    ]
    for name, color, x in dims:
        rect = FancyBboxPatch((x, 12), 3, 1.8, boxstyle="round,pad=0.08",
                              facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x+1.5, 12.9, name, ha='center', va='center', fontsize=16, fontweight='bold', color='white')
        # 连接线
        ax.annotate('', xy=(x+1.5, 13.8), xytext=(12, 15.5),
                   arrowprops=dict(arrowstyle='-', color='#666666', lw=1.2))

    # 二级维度层
    subdims = [
        # E1
        ('数据集\n规模', 1.0, 9.5), ('主题\n覆盖', 2.5, 9.5), ('更新\n频率', 4.0, 9.5),
        # E2
        ('功能\n完备度', 5.0, 9.5), ('检索\n效率', 6.5, 9.5), ('响应\n速度', 8.0, 9.5),
        # E3
        ('格式\n标准化', 9.0, 9.5), ('元数据\n完整', 10.5, 9.5), ('准确性\n验证', 12.0, 9.5),
        # E4
        ('应用\n成果', 13.0, 9.5), ('API\n调用', 14.5, 9.5), ('授权\n运营', 16.0, 9.5),
        # E5
        ('无障碍\n访问', 17.0, 9.5), ('用户\n反馈', 18.5, 9.5), ('数据\n安全', 20.0, 9.5),
    ]
    for name, x, y in subdims:
        rect = FancyBboxPatch((x-0.6, y), 1.5, 1.5, boxstyle="round,pad=0.05",
                              facecolor='#5dade2', edgecolor='#2874a6', linewidth=1)
        ax.add_patch(rect)
        ax.text(x+0.15, y+0.75, name, ha='center', va='center', fontsize=12, color='#1a5276')

    # 指标层（简化展示部分关键指标）
    indicators = [
        ('数据集数量', 0.5, 7.0), ('主题覆盖广度', 2.0, 7.0), ('更新及时性', 3.5, 7.0),
        ('功能完备度', 5.0, 7.0), ('检索效率', 6.5, 7.0), ('响应速度', 8.0, 7.0),
        ('格式标准化', 9.5, 7.0), ('元数据完整', 11.0, 7.0), ('准确性验证', 12.5, 7.0),
        ('应用成果数', 14.0, 7.0), ('API调用深度', 15.5, 7.0), ('授权运营成效', 17.0, 7.0),
        ('无障碍访问', 18.5, 7.0), ('用户反馈机制', 20.0, 7.0),
    ]
    for name, x, y in indicators:
        rect = FancyBboxPatch((x-0.5, y), 1.3, 0.8, boxstyle="round,pad=0.03",
                              facecolor='#aed6f1', edgecolor='#5dade2', linewidth=0.8)
        ax.add_patch(rect)
        ax.text(x+0.15, y+0.4, name, ha='center', va='center', fontsize=10, color='#1a5276')

    # 图例
    ax.text(1, 5.5, '图例说明：', fontsize=16, fontweight='bold')
    ax.add_patch(FancyBboxPatch((1, 4.8), 1.5, 0.5, boxstyle="round,pad=0.05", facecolor='#1a5276'))
    ax.text(3, 5.05, '总目标层', fontsize=14, va='center')
    ax.add_patch(FancyBboxPatch((1, 4.2), 1.5, 0.5, boxstyle="round,pad=0.05", facecolor='#2874a6'))
    ax.text(3, 4.45, '一级维度（5个）', fontsize=14, va='center')
    ax.add_patch(FancyBboxPatch((1, 3.6), 1.5, 0.5, boxstyle="round,pad=0.05", facecolor='#5dade2'))
    ax.text(3, 3.85, '二级维度（9个）', fontsize=14, va='center')
    ax.add_patch(FancyBboxPatch((1, 3.0), 1.5, 0.5, boxstyle="round,pad=0.05", facecolor='#aed6f1'))
    ax.text(3, 3.25, '具体指标（24个）', fontsize=14, va='center')

    ax.text(1, 2.0, '注：本图展示了4E评估指标体系的层级结构。总目标层为"数据利用绩效"，下设5个一级维度、9个二级维度和24个具体测量指标。',
            fontsize=12, style='italic', wrap=True)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图3-1.png', dpi=400, bbox_inches='tight', facecolor='white')
    plt.close()
    print("OK 图3-1 生成完成")

# ==================== 图4-1: 研究技术路线 ====================
def generate_fig4_1():
    fig, ax = plt.subplots(1, 1, figsize=(24, 14), dpi=400)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 14)
    ax.axis('off')
    ax.set_title('图4-1  研究技术路线', fontsize=28, fontweight='bold', pad=30)

    # 六阶段流程
    stages = [
        ('第一阶段\n理论构建', '文献综述\n理论分析', '#1a5276', 2),
        ('第二阶段\n框架设计', '4E评估框架\n指标体系', '#2874a6', 6),
        ('第三阶段\n数据采集', 'OGD-Collector\n31→23平台', '#5dade2', 10),
        ('第四阶段\n绩效评估', 'TOPSIS排名\nDEA效率', '#85c1e9', 14),
        ('第五阶段\n机制分析', 'DEMATEL因果\nfsQCA组态', '#aed6f1', 18),
        ('第六阶段\n对策设计', '类型学分析\n差异化策略', '#d6eaf8', 22),
    ]

    for i, (stage, detail, color, x) in enumerate(stages):
        # 主框
        rect = FancyBboxPatch((x-1.5, 8), 3.5, 2.5, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x+0.25, 9.8, stage, ha='center', va='center', fontsize=15, fontweight='bold',
                color='white' if i < 4 else '#1a5276')
        ax.text(x+0.25, 8.8, detail, ha='center', va='center', fontsize=12,
                color='white' if i < 4 else '#1a5276')

        # 箭头
        if i < 5:
            ax.annotate('', xy=(x+2.5, 9.25), xytext=(x+2.0, 9.25),
                       arrowprops=dict(arrowstyle='->', color='#1a5276', lw=2.5))

    # 核心方法标注
    methods = [
        ('AHP-熵权\n组合赋权', 6, 5.5),
        ('DEA-BCC\n效率评价', 14, 5.5),
        ('DEMATEL\n因果分析', 18, 5.5),
        ('fsQCA\n组态分析', 22, 5.5),
    ]
    for name, x, y in methods:
        rect = FancyBboxPatch((x-1.2, y-0.8), 2.6, 1.6, boxstyle="round,pad=0.08",
                              facecolor='#f8c471', edgecolor='#e67e22', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x+0.1, y, name, ha='center', va='center', fontsize=13, fontweight='bold', color='#7e5109')
        # 连接线
        ax.annotate('', xy=(x+0.1, y+0.8), xytext=(x+0.1, y+1.2),
                   arrowprops=dict(arrowstyle='->', color='#e67e22', lw=1.5, ls='--'))

    # 章节对应
    chapters = [
        ('第一章\n绪论', 2, 3.0),
        ('第三章\n理论框架', 6, 3.0),
        ('第四章\n研究设计', 10, 3.0),
        ('第五章\n绩效评估', 14, 3.0),
        ('第六章\n影响因素', 18, 3.0),
        ('第七章\n对策建议', 22, 3.0),
    ]
    for name, x, y in chapters:
        rect = FancyBboxPatch((x-1.3, y-0.5), 2.8, 1.0, boxstyle="round,pad=0.05",
                              facecolor='#eafaf1', edgecolor='#27ae60', linewidth=1)
        ax.add_patch(rect)
        ax.text(x+0.1, y, name, ha='center', va='center', fontsize=11, color='#1e8449')
        ax.annotate('', xy=(x+0.1, y+0.5), xytext=(x+0.1, y+1.5),
                   arrowprops=dict(arrowstyle='->', color='#27ae60', lw=1, ls=':'))

    # 底部说明
    ax.text(12, 1.0, '研究逻辑："评估→归因→组态→对策"的递进式分析框架，确保研究结论的可靠性和政策建议的针对性',
            ha='center', fontsize=14, style='italic', bbox=dict(boxstyle='round', facecolor='#fef9e7', alpha=0.8))

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图4-1.png', dpi=400, bbox_inches='tight', facecolor='white')
    plt.close()
    print("OK 图4-1 生成完成")

# ==================== 图5-3: 绩效-效率四象限类型分布 ====================
def generate_fig5_3():
    fig, ax = plt.subplots(1, 1, figsize=(20, 16), dpi=400)

    # 正确的23个平台数据（基于TOPSIS和DEA）
    platforms = {
        '山东': (0.955, 1.000, '标杆型'),
        '河南': (0.511, 0.938, '潜力型'),
        '山西': (0.491, 0.924, '节约型'),
        '天津': (0.498, 0.918, '节约型'),
        '湖南': (0.529, 0.887, '潜力型'),
        '辽宁': (0.564, 0.884, '潜力型'),
        '内蒙古': (0.505, 0.882, '潜力型'),
        '北京': (0.551, 0.862, '潜力型'),
        '广西': (0.558, 0.848, '潜力型'),
        '海南': (0.553, 0.843, '潜力型'),
        '四川': (0.570, 0.831, '潜力型'),
        '江苏': (0.399, 0.743, '困境型'),
        '贵州': (0.349, 0.737, '困境型'),
        '重庆': (0.404, 0.729, '困境型'),
        '广东': (0.418, 0.712, '困境型'),
        '湖北': (0.389, 0.699, '困境型'),
        '福建': (0.325, 0.696, '困境型'),
        '江西': (0.304, 0.690, '困境型'),
        '浙江': (0.389, 0.687, '困境型'),
        '吉林': (0.282, 0.659, '困境型'),
        '云南': (0.275, 0.630, '困境型'),
        '上海': (0.268, 0.599, '困境型'),
        '安徽': (0.095, 0.450, '困境型'),
    }

    # 划分阈值
    topsis_mid = 0.4
    dea_mid = 0.75

    colors = {'标杆型': '#e74c3c', '潜力型': '#f39c12', '节约型': '#3498db', '困境型': '#95a5a6'}

    for name, (topsis, dea, ptype) in platforms.items():
        ax.scatter(dea, topsis, c=colors[ptype], s=200, edgecolors='black', linewidth=0.5, zorder=5)
        # 标注省份名
        fontsize = 13 if name in ['山东', '四川', '辽宁'] else 11
        ax.annotate(name, (dea, topsis), textcoords="offset points", xytext=(8, 5),
                   fontsize=fontsize, ha='left')

    # 分界线
    ax.axhline(y=topsis_mid, color='#666666', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.axvline(x=dea_mid, color='#666666', linestyle='--', linewidth=1.5, alpha=0.7)

    # 象限标签
    ax.text(0.92, 0.92, '标杆型\n(高绩效高效率)\n n=1', ha='center', va='center',
            fontsize=16, fontweight='bold', color='#e74c3c',
            bbox=dict(boxstyle='round', facecolor='#fadbd8', alpha=0.8))
    ax.text(0.60, 0.92, '潜力型\n(高绩效中效率)\n n=8', ha='center', va='center',
            fontsize=16, fontweight='bold', color='#f39c12',
            bbox=dict(boxstyle='round', facecolor='#fdebd0', alpha=0.8))
    ax.text(0.92, 0.25, '节约型\n(中绩效高效率)\n n=2', ha='center', va='center',
            fontsize=16, fontweight='bold', color='#3498db',
            bbox=dict(boxstyle='round', facecolor='#d4e6f1', alpha=0.8))
    ax.text(0.60, 0.25, '困境型\n(低绩效低效率)\n n=12', ha='center', va='center',
            fontsize=16, fontweight='bold', color='#7f8c8d',
            bbox=dict(boxstyle='round', facecolor='#eaeded', alpha=0.8))

    ax.set_xlabel('DEA效率值（资源配置效率）', fontsize=18, fontweight='bold')
    ax.set_ylabel('TOPSIS综合绩效得分', fontsize=18, fontweight='bold')
    ax.set_title('图5-3  绩效-效率四象限类型分布', fontsize=26, fontweight='bold', pad=20)

    ax.set_xlim(0.35, 1.05)
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, alpha=0.3)

    # 图例
    legend_elements = [mpatches.Patch(facecolor=colors[k], edgecolor='black', label=f'{k} (n={sum(1 for v in platforms.values() if v[2]==k)})')
                       for k in colors]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=14, framealpha=0.9)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图5-3.png', dpi=400, bbox_inches='tight', facecolor='white')
    plt.close()
    print("OK 图5-3 生成完成")

# ==================== 图7-2: 差异化优化策略矩阵(SWOT) ====================
def generate_fig7_2():
    fig, ax = plt.subplots(1, 1, figsize=(22, 18), dpi=400)
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 18)
    ax.axis('off')
    ax.set_title('图7-2  差异化优化策略矩阵', fontsize=28, fontweight='bold', pad=30)

    # 背景四象限
    ax.add_patch(FancyBboxPatch((1, 9.5), 9.5, 7, boxstyle="round,pad=0.1",
                                facecolor='#d5f5e3', edgecolor='#27ae60', linewidth=2))
    ax.add_patch(FancyBboxPatch((11.5, 9.5), 9.5, 7, boxstyle="round,pad=0.1",
                                facecolor='#fdebd0', edgecolor='#f39c12', linewidth=2))
    ax.add_patch(FancyBboxPatch((1, 1.5), 9.5, 7, boxstyle="round,pad=0.1",
                                facecolor='#d6eaf8', edgecolor='#3498db', linewidth=2))
    ax.add_patch(FancyBboxPatch((11.5, 1.5), 9.5, 7, boxstyle="round,pad=0.1",
                                facecolor='#fadbd8', edgecolor='#e74c3c', linewidth=2))

    # 轴标签
    ax.text(11, 17.5, '外部机遇 →', ha='center', fontsize=18, fontweight='bold', color='#1a5276')
    ax.text(11, 1.0, '外部威胁 →', ha='center', fontsize=18, fontweight='bold', color='#1a5276')
    ax.text(0.3, 9.5, '优势\n↑', ha='center', va='center', fontsize=18, fontweight='bold', color='#1a5276')
    ax.text(0.3, 8.0, '劣势\n↓', ha='center', va='center', fontsize=18, fontweight='bold', color='#1a5276')

    # 标杆型 - SO策略
    ax.text(5.75, 15.5, '标杆型平台', ha='center', fontsize=20, fontweight='bold', color='#1e8449')
    ax.text(5.75, 14.5, 'SO策略：发挥优势 · 抓住机遇', ha='center', fontsize=16, color='#1e8449')
    ax.text(5.75, 13.0, '- 推进数据要素价值化\n- 授权运营创新试点\n- 输出标杆经验\n- 参与国际标准制定',
            ha='center', fontsize=15, linespacing=1.6, va='top')
    ax.text(5.75, 10.0, '代表：山东、广东、浙江', ha='center', fontsize=14, style='italic', color='#1e8449')

    # 潜力型 - WO策略
    ax.text(16.25, 15.5, '潜力型平台', ha='center', fontsize=20, fontweight='bold', color='#9c640c')
    ax.text(16.25, 14.5, 'WO策略：克服劣势 · 抓住机遇', ha='center', fontsize=16, color='#9c640c')
    ax.text(16.25, 13.0, '- 优化资源配置效率\n- 补齐数据质量短板\n- 培育应用生态\n- 加强制度保障',
            ha='center', fontsize=15, linespacing=1.6, va='top')
    ax.text(16.25, 10.0, '代表：四川、辽宁、北京', ha='center', fontsize=14, style='italic', color='#9c640c')

    # 节约型 - ST策略
    ax.text(5.75, 7.5, '节约型平台', ha='center', fontsize=20, fontweight='bold', color='#1a5276')
    ax.text(5.75, 6.5, 'ST策略：发挥优势 · 规避威胁', ha='center', fontsize=16, color='#1a5276')
    ax.text(5.75, 5.0, '- 适度增加资源投入\n- 扩大数据集规模\n- 提升平台功能\n- 保持效率优势',
            ha='center', fontsize=15, linespacing=1.6, va='top')
    ax.text(5.75, 2.0, '代表：天津、山西', ha='center', fontsize=14, style='italic', color='#1a5276')

    # 困境型 - WT策略
    ax.text(16.25, 7.5, '困境型平台', ha='center', fontsize=20, fontweight='bold', color='#922b21')
    ax.text(16.25, 6.5, 'WT策略：克服劣势 · 规避威胁', ha='center', fontsize=16, color='#922b21')
    ax.text(16.25, 5.0, '- 外部支援与对口帮扶\n- 建立基本数据开放能力\n- 省级专项政策支持\n- 借鉴先行省份经验',
            ha='center', fontsize=15, linespacing=1.6, va='top')
    ax.text(16.25, 2.0, '代表：安徽、上海、江苏等', ha='center', fontsize=14, style='italic', color='#922b21')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图7-2.png', dpi=400, bbox_inches='tight', facecolor='white')
    plt.close()
    print("OK 图7-2 生成完成")

# ==================== 图7-3: 差异化策略实施路线图 ====================
def generate_fig7_3():
    fig, ax = plt.subplots(1, 1, figsize=(24, 14), dpi=400)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 14)
    ax.axis('off')
    ax.set_title('图7-3  差异化策略实施路线图', fontsize=28, fontweight='bold', pad=30)

    # 时间轴
    ax.annotate('', xy=(23, 2), xytext=(1, 2),
               arrowprops=dict(arrowstyle='->', color='#1a5276', lw=3))
    ax.text(12, 1.3, '实施时间梯度', ha='center', fontsize=20, fontweight='bold', color='#1a5276')

    # 时间标记
    for x, label in [(3, '短期\n(0-1年)'), (12, '中期\n(1-3年)'), (21, '长期\n(3-5年)')]:
        ax.plot([x, x], [1.8, 2.2], color='#1a5276', lw=2)
        ax.text(x, 1.0, label, ha='center', fontsize=16, fontweight='bold')

    # 高绩效平台 - 长期
    rect1 = FancyBboxPatch((14, 9), 9, 3.5, boxstyle="round,pad=0.1",
                           facecolor='#d5f5e3', edgecolor='#27ae60', linewidth=2)
    ax.add_patch(rect1)
    ax.text(18.5, 11.5, '高绩效平台（路径H1）', ha='center', fontsize=18, fontweight='bold', color='#1e8449')
    ax.text(18.5, 10.3, '- 参与国际标准制定\n- 输出中国经验\n- 模式标准化推广',
            ha='center', fontsize=15, linespacing=1.6, va='top')

    # 功能型低绩效 - 短期
    rect2 = FancyBboxPatch((1, 9), 9, 3.5, boxstyle="round,pad=0.1",
                           facecolor='#fdebd0', edgecolor='#f39c12', linewidth=2)
    ax.add_patch(rect2)
    ax.text(5.5, 11.5, '功能型低绩效（路径H2/L1）', ha='center', fontsize=18, fontweight='bold', color='#9c640c')
    ax.text(5.5, 10.3, '- 出台专项政策法规\n- 建立跨部门协调机制\n- 纳入绩效考核',
            ha='center', fontsize=15, linespacing=1.6, va='top')

    # 停滞型 - 中期
    rect3 = FancyBboxPatch((7.5, 5), 9, 3.5, boxstyle="round,pad=0.1",
                           facecolor='#d6eaf8', edgecolor='#3498db', linewidth=2)
    ax.add_patch(rect3)
    ax.text(12, 7.5, '停滞型平台（路径L2）', ha='center', fontsize=18, fontweight='bold', color='#1a5276')
    ax.text(12, 6.3, '- 平台重启与资源整合\n- 理顺开放与运营关系\n- 逐步培育应用生态',
            ha='center', fontsize=15, linespacing=1.6, va='top')

    # 保障机制 - 贯穿
    rect4 = FancyBboxPatch((1, 11.5), 22, 1.8, boxstyle="round,pad=0.08",
                           facecolor='#eafaf1', edgecolor='#27ae60', linewidth=1.5, linestyle='--')
    ax.add_patch(rect4)
    ax.text(12, 12.4, '四维保障机制：组织保障 · 制度保障 · 资金保障 · 技术保障',
            ha='center', fontsize=16, fontweight='bold', color='#1e8449')

    # 连接箭头
    ax.annotate('', xy=(14, 10.75), xytext=(10, 10.75),
               arrowprops=dict(arrowstyle='->', color='#f39c12', lw=2, connectionstyle="arc3,rad=0.1"))
    ax.annotate('', xy=(12, 8.5), xytext=(10, 10),
               arrowprops=dict(arrowstyle='->', color='#3498db', lw=2, connectionstyle="arc3,rad=-0.1"))
    ax.annotate('', xy=(18.5, 9), xytext=(12, 8.5),
               arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2, connectionstyle="arc3,rad=0.1"))

    # 底部说明
    ax.text(12, 0.3, '核心理念：分类施策 · 循序渐进 · 因地制宜',
            ha='center', fontsize=16, style='italic',
            bbox=dict(boxstyle='round', facecolor='#fef9e7', alpha=0.8))

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图7-3.png', dpi=400, bbox_inches='tight', facecolor='white')
    plt.close()
    print("OK 图7-3 生成完成")

if __name__ == '__main__':
    generate_fig3_1()
    generate_fig4_1()
    generate_fig5_3()
    generate_fig7_2()
    generate_fig7_3()
    print(f"\n所有图表已保存到 {OUTPUT_DIR}/")
