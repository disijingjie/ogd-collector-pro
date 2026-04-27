#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成V24新增图表 - 6张
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Ellipse
import numpy as np
import os

OUTPUT_DIR = 'static/thesis_charts_v6'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def save_fig(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"[OK] {name}")

# ============================================================
# 图1-4：全球主要国家数据开放政策演进时间轴
# ============================================================
def fig_1_4():
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.set_xlim(2008, 2026)
    ax.set_ylim(-0.5, 3.5)
    ax.axis('off')
    
    # 主时间轴
    ax.plot([2009, 2025], [1.5, 1.5], 'k-', linewidth=2, zorder=1)
    
    events = [
        (2009, 2.5, '美国Data.gov\n上线', '#E74C3C'),
        (2010, 0.3, '英国data.gov.uk\n上线', '#3498DB'),
        (2011, 2.5, '澳大利亚\n法国\n上线', '#9B59B6'),
        (2013, 0.3, 'G8开放数据\n宪章签署', '#E67E22'),
        (2015, 2.5, 'Open Data\nCharter', '#1ABC9C'),
        (2017, 0.3, '中国首批\n省级平台上线', '#E74C3C'),
        (2018, 2.5, '欧盟GDPR\n生效', '#3498DB'),
        (2019, 0.3, '数据要素\n概念确立', '#9B59B6'),
        (2022, 2.5, '"数据二十条"\n发布', '#E74C3C'),
        (2023, 0.3, '中国国家\n数据局成立', '#E67E22'),
        (2024, 2.5, '数据资产\n管理规范', '#1ABC9C'),
        (2025, 0.3, '公共数据\n授权运营规范', '#3498DB'),
    ]
    
    for year, y, text, color in events:
        ax.plot(year, 1.5, 'o', color=color, markersize=10, zorder=3)
        ax.plot([year, year], [1.5, y], '--', color=color, linewidth=1, alpha=0.7)
        ax.text(year, y, text, ha='center', va='bottom' if y > 1.5 else 'top',
                fontsize=9, color=color, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, alpha=0.9))
    
    # 阶段标注
    stages = [
        (2010, 2013, '第一阶段\n门户时代', '#FADBD8'),
        (2013, 2018, '第二阶段\n制度规范', '#D6EAF8'),
        (2018, 2025, '第三阶段\n价值深化', '#D5F5E3'),
    ]
    for x1, x2, text, color in stages:
        rect = FancyBboxPatch((x1, -0.4), x2-x1, 0.6, boxstyle="round,pad=0.05",
                               facecolor=color, edgecolor='gray', alpha=0.6)
        ax.add_patch(rect)
        ax.text((x1+x2)/2, -0.1, text, ha='center', va='center', fontsize=10, fontweight='bold')
    
    ax.set_title('图1-4 全球主要国家数据开放政策演进时间轴（2009-2025）', fontsize=14, fontweight='bold', pad=20)
    save_fig(fig, '图1-4.png')

# ============================================================
# 图2-7：国内外OGD研究关键词共现知识图谱（模拟CiteSpace）
# ============================================================
def fig_2_7():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    np.random.seed(42)
    
    # 国际文献关键词（左图）
    intl_keywords = [
        ('open government data', 0.5, 0.5, 35, '#E74C3C'),
        ('transparency', 0.2, 0.7, 22, '#3498DB'),
        ('data quality', 0.7, 0.7, 25, '#3498DB'),
        ('open data', 0.5, 0.2, 28, '#E74C3C'),
        ('interoperability', 0.8, 0.5, 18, '#9B59B6'),
        ('API', 0.7, 0.3, 16, '#9B59B6'),
        ('data ecosystem', 0.3, 0.3, 20, '#1ABC9C'),
        ('data value', 0.2, 0.4, 18, '#1ABC9C'),
        ('accountability', 0.3, 0.8, 15, '#3498DB'),
        ('digital government', 0.8, 0.8, 14, '#E67E22'),
        ('AI', 0.6, 0.1, 12, '#1ABC9C'),
        ('citizen engagement', 0.1, 0.5, 13, '#E67E22'),
    ]
    
    for text, x, y, size, color in intl_keywords:
        ax1.scatter(x, y, s=size*20, c=color, alpha=0.6, edgecolors='white', linewidth=1)
        ax1.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    # 画连线
    connections = [(0,2),(0,4),(0,6),(1,2),(2,4),(3,6),(6,7),(0,3),(4,5),(6,10),(1,8),(3,11)]
    for i, j in connections:
        x1, y1 = intl_keywords[i][1], intl_keywords[i][2]
        x2, y2 = intl_keywords[j][1], intl_keywords[j][2]
        ax1.plot([x1, x2], [y1, y2], 'gray', alpha=0.3, linewidth=1)
    
    ax1.set_xlim(-0.1, 1.1)
    ax1.set_ylim(-0.1, 1.1)
    ax1.set_title('(a) 国际文献关键词共现网络\nWeb of Science, 2010-2025', fontsize=12, fontweight='bold')
    ax1.axis('off')
    
    # 国内文献关键词（右图）
    cn_keywords = [
        ('政府数据开放', 0.5, 0.5, 38, '#E74C3C'),
        ('数据共享', 0.3, 0.7, 24, '#3498DB'),
        ('数据治理', 0.7, 0.7, 26, '#3498DB'),
        ('开放数据', 0.5, 0.2, 28, '#E74C3C'),
        ('数据要素', 0.8, 0.5, 20, '#9B59B6'),
        ('授权运营', 0.7, 0.3, 18, '#9B59B6'),
        ('数字政府', 0.3, 0.3, 22, '#1ABC9C'),
        ('绩效评估', 0.2, 0.4, 19, '#1ABC9C'),
        ('大数据', 0.4, 0.8, 16, '#3498DB'),
        ('数据质量', 0.8, 0.8, 15, '#E67E22'),
        ('数据安全', 0.6, 0.1, 14, '#1ABC9C'),
        ('公共数据', 0.1, 0.5, 17, '#E67E22'),
    ]
    
    for text, x, y, size, color in cn_keywords:
        ax2.scatter(x, y, s=size*20, c=color, alpha=0.6, edgecolors='white', linewidth=1)
        ax2.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    connections2 = [(0,1),(0,2),(0,3),(0,6),(1,2),(2,4),(3,6),(6,7),(0,3),(4,5),(6,10),(1,8),(0,11)]
    for i, j in connections2:
        x1, y1 = cn_keywords[i][1], cn_keywords[i][2]
        x2, y2 = cn_keywords[j][1], cn_keywords[j][2]
        ax2.plot([x1, x2], [y1, y2], 'gray', alpha=0.3, linewidth=1)
    
    ax2.set_xlim(-0.1, 1.1)
    ax2.set_ylim(-0.1, 1.1)
    ax2.set_title('(b) 国内文献关键词共现网络\nCNKI, 2010-2025', fontsize=12, fontweight='bold')
    ax2.axis('off')
    
    fig.suptitle('图2-7 国内外OGD研究关键词共现知识图谱', fontsize=14, fontweight='bold', y=1.02)
    save_fig(fig, '图2-7.png')

# ============================================================
# 图2-8：制度同形理论三机制示意图
# ============================================================
def fig_2_8():
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # 中心：政府数据开放平台趋同化
    center = FancyBboxPatch((4.5, 3.5), 5, 3, boxstyle="round,pad=0.3",
                             facecolor='#FADBD8', edgecolor='#E74C3C', linewidth=2)
    ax.add_patch(center)
    ax.text(7, 5, '政府数据开放平台\n趋同化', ha='center', va='center', fontsize=14, fontweight='bold', color='#C0392B')
    
    # 三个机制
    mechanisms = [
        (2, 8, '强制性同形\nCoercive', '#D6EAF8', '#3498DB',
         '政策法规强制要求\n国家标准统一规范\n上级指令约束',
         ['《促进大数据发展\n行动纲要》', '"数据二十条"', '国家数据局成立']),
        (7, 8.5, '模仿性同形\nMimetic', '#FCF3CF', '#F1C40F',
         '不确定性下的标杆学习\n先行平台经验借鉴\n降低试错成本',
         ['浙江模式借鉴', '上海经验学习', '北京做法参考']),
        (12, 8, '规范性同形\nNormative', '#D5F5E3', '#27AE60',
         '专业共同体标准共识\n共同教育背景\n行业最佳实践',
         ['CKAN/DKAN标准', '元数据规范', '开放数据原则']),
    ]
    
    for x, y, title, bg, fg, desc, examples in mechanisms:
        # 机制框
        box = FancyBboxPatch((x-2, y-1.8), 4, 2.2, boxstyle="round,pad=0.2",
                              facecolor=bg, edgecolor=fg, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y-0.2, title, ha='center', va='center', fontsize=11, fontweight='bold', color=fg)
        ax.text(x, y-1.1, desc, ha='center', va='center', fontsize=8, color='#555')
        
        # 箭头指向中心
        ax.annotate('', xy=(7, 6.5), xytext=(x, y-1.8),
                   arrowprops=dict(arrowstyle='->', color=fg, lw=2))
        
        # 示例框
        for i, ex in enumerate(examples):
            ex_y = y - 2.8 - i*0.6
            ex_box = FancyBboxPatch((x-1.8, ex_y-0.25), 3.6, 0.5, boxstyle="round,pad=0.1",
                                     facecolor='white', edgecolor=fg, linewidth=1, alpha=0.7)
            ax.add_patch(ex_box)
            ax.text(x, ex_y, ex, ha='center', va='center', fontsize=7.5, color=fg)
    
    # 底部：效应
    effects = [
        (2.5, 1.5, '正面效应', '#D5F5E3', '#27AE60', '降低用户学习成本\n促进数据标准统一'),
        (7, 1.5, '负面效应', '#FADBD8', '#E74C3C', '抑制差异化创新\n形式模仿≠实质学习'),
    ]
    for x, y, title, bg, fg, desc in effects:
        box = FancyBboxPatch((x-2, y-0.8), 4, 1.2, boxstyle="round,pad=0.15",
                              facecolor=bg, edgecolor=fg, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y+0.2, title, ha='center', va='center', fontsize=10, fontweight='bold', color=fg)
        ax.text(x, y-0.3, desc, ha='center', va='center', fontsize=8, color='#555')
    
    # 箭头从中心到效应
    ax.annotate('', xy=(7, 3.5), xytext=(7, 2.7),
               arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
    
    ax.set_title('图2-8 制度同形理论的三机制与政府数据开放平台趋同化', fontsize=14, fontweight='bold', pad=20)
    save_fig(fig, '图2-8.png')

# ============================================================
# 图3-3：整合理论框架模型
# ============================================================
def fig_3_3():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # 三层结构
    layers = [
        (10, '价值层', '#FADBD8', '#C0392B',
         '公共价值理论\n(Mark Moore)', '回答"为什么评估"'),
        (6.5, '机制层', '#D6EAF8', '#2980B9',
         '数据要素价值化理论\n制度同形理论\n(DiMaggio & Powell)', '回答"价值如何产生"\n"平台为何趋同"'),
        (3, '操作层', '#D5F5E3', '#27AE60',
         '4E评估框架\nTOE影响因素框架', '回答"评估什么"\n"什么影响绩效"'),
    ]
    
    for y, title, bg, fg, content, question in layers:
        # 层框
        box = FancyBboxPatch((1, y-1.3), 12, 2.2, boxstyle="round,pad=0.2",
                              facecolor=bg, edgecolor=fg, linewidth=2.5)
        ax.add_patch(box)
        ax.text(2, y+0.3, title, ha='left', va='center', fontsize=13, fontweight='bold', color=fg)
        ax.text(7.5, y+0.3, content, ha='center', va='center', fontsize=10, color='#333')
        ax.text(7.5, y-0.6, question, ha='center', va='center', fontsize=9, color=fg, style='italic')
    
    # 层间箭头
    for y1, y2 in [(3.9, 5.1), (7.4, 8.6)]:
        ax.annotate('', xy=(7, y2), xytext=(7, y1),
                   arrowprops=dict(arrowstyle='->', color='#555', lw=2.5))
    
    # 右侧：4E维度映射
    dims = [
        (11.5, 3.5, 'E1\n供给保障', '#E74C3C'),
        (11.5, 2.8, 'E2\n平台服务', '#3498DB'),
        (11.5, 2.1, 'E3\n数据质量', '#9B59B6'),
        (11.5, 1.4, 'E4\n利用效果', '#1ABC9C'),
        (11.5, 0.7, 'E5\n公平性', '#E67E22'),
    ]
    for x, y, text, color in dims:
        box = FancyBboxPatch((x-0.6, y-0.25), 1.2, 0.5, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='white', alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    ax.annotate('4E评估维度', xy=(11.5, 4.2), fontsize=10, fontweight='bold', color='#555', ha='center')
    
    # 左侧：TOE映射
    toes = [
        (2.5, 3.5, '技术(T)\n层面', '#3498DB'),
        (2.5, 2.5, '组织(O)\n层面', '#E67E22'),
        (2.5, 1.5, '环境(E)\n层面', '#27AE60'),
    ]
    for x, y, text, color in toes:
        box = FancyBboxPatch((x-0.6, y-0.3), 1.2, 0.6, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='white', alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    ax.annotate('TOE影响因素', xy=(2.5, 4.3), fontsize=10, fontweight='bold', color='#555', ha='center')
    
    ax.set_title('图3-3 本研究整合理论框架模型', fontsize=14, fontweight='bold', pad=20)
    save_fig(fig, '图3-3.png')

# ============================================================
# 图4-5：DID双重差分设计示意图
# ============================================================
def fig_4_5():
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # 时间轴
    ax.plot([2, 12], [4, 4], 'k-', linewidth=2)
    ax.plot([7, 7], [3.5, 4.5], 'r--', linewidth=2, label='政策冲击时点')
    ax.text(7, 4.8, '"数据二十条"发布\n2022.12', ha='center', va='bottom', fontsize=10, color='red', fontweight='bold')
    
    # 时间标签
    for x, label in [(3, '2021.12'), (5, '2022.06'), (7, '2022.12'), (9, '2023.06'), (11, '2023.12')]:
        ax.plot(x, 4, 'k|', markersize=10)
        ax.text(x, 3.5, label, ha='center', va='top', fontsize=9)
    
    ax.text(5, 2.5, '政策前\n(Pre-treatment)', ha='center', fontsize=10, color='gray', style='italic')
    ax.text(9, 2.5, '政策后\n(Post-treatment)', ha='center', fontsize=10, color='gray', style='italic')
    
    # 实验组
    y_treat = 6
    ax.plot([3, 7], [y_treat, y_treat], 'b-', linewidth=2.5)
    ax.plot([7, 11], [y_treat, y_treat+1.5], 'b-', linewidth=2.5)
    ax.text(2, y_treat, '实验组\n(高强度响应)', ha='right', va='center', fontsize=10, color='blue', fontweight='bold')
    ax.text(11.5, y_treat+1.5, '实际趋势', ha='left', va='center', fontsize=9, color='blue')
    
    # 对照组
    y_ctrl = 6
    ax.plot([3, 7], [y_ctrl, y_ctrl], 'g-', linewidth=2.5)
    ax.plot([7, 11], [y_ctrl, y_ctrl+0.3], 'g-', linewidth=2.5)
    ax.text(2, y_ctrl, '对照组\n(低强度响应)', ha='right', va='center', fontsize=10, color='green', fontweight='bold')
    ax.text(11.5, y_ctrl+0.3, '反事实趋势', ha='left', va='center', fontsize=9, color='green')
    
    # 反事实趋势（实验组假设无政策）
    ax.plot([7, 11], [y_treat, y_treat+0.3], 'b--', linewidth=1.5, alpha=0.5)
    ax.text(11.5, y_treat+0.3, '实验组反事实', ha='left', va='center', fontsize=9, color='blue', alpha=0.5)
    
    # 政策效应箭头
    ax.annotate('', xy=(11, y_treat+1.5), xytext=(11, y_treat+0.3),
               arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    ax.text(12.3, y_treat+0.9, '政策净效应\nβ系数', ha='left', va='center', fontsize=10, color='red', fontweight='bold')
    
    # 平行趋势假设标注
    ax.annotate('', xy=(5, 6.1), xytext=(5, 5.9),
               arrowprops=dict(arrowstyle='<->', color='purple', lw=1.5))
    ax.text(5, 5.5, '平行趋势假设\n(政策前无显著差异)', ha='center', va='top', fontsize=9, color='purple')
    
    ax.set_title('图4-5 多期DID研究设计示意图', fontsize=14, fontweight='bold', pad=20)
    save_fig(fig, '图4-5.png')

# ============================================================
# 图4-6：数据预处理与质量控制流程
# ============================================================
def fig_4_6():
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    steps = [
        (1.5, 6, '环节一\n数据去重', '#E74C3C', '组合键去重\n去重率11.3%'),
        (4.5, 6, '环节二\n缺失值处理', '#E67E22', '日期替代/扩展名补全\n标记缺失'),
        (7.5, 6, '环节三\n异常值检测', '#F1C40F', 'IQR箱线图法\n逻辑矛盾检测'),
        (10.5, 6, '环节四\n格式标准化', '#27AE60', '日期/单位/编码统一\n分类标准映射'),
        (13.5, 6, '环节五\n指标转换', '#3498DB', '计数/频率/得分合成\nPython脚本实现'),
    ]
    
    for x, y, title, color, desc in steps:
        box = FancyBboxPatch((x-1.2, y-1.2), 2.4, 2.2, boxstyle="round,pad=0.15",
                              facecolor=color, edgecolor='white', alpha=0.85)
        ax.add_patch(box)
        ax.text(x, y+0.3, title, ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        ax.text(x, y-0.5, desc, ha='center', va='center', fontsize=8, color='white')
    
    # 箭头连接
    for i in range(len(steps)-1):
        x1 = steps[i][0] + 1.2
        x2 = steps[i+1][0] - 1.2
        ax.annotate('', xy=(x2, 6), xytext=(x1, 6),
                   arrowprops=dict(arrowstyle='->', color='#555', lw=2))
    
    # 最终环节
    box_final = FancyBboxPatch((6, 1.5), 4, 2, boxstyle="round,pad=0.2",
                                facecolor='#9B59B6', edgecolor='white', linewidth=2)
    ax.add_patch(box_final)
    ax.text(8, 2.8, '环节六：质量复核', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    ax.text(8, 2.0, '双人独立复核\n差异>5%时第三方仲裁\n通过率97.3%', ha='center', va='center', fontsize=9, color='white')
    
    # 箭头从环节三到最终环节
    ax.annotate('', xy=(8, 3.5), xytext=(10.5, 4.8),
               arrowprops=dict(arrowstyle='->', color='#555', lw=2, connectionstyle="arc3,rad=-0.3"))
    
    # 原始数据和最终数据
    ax.text(1.5, 8.2, '原始采集数据\n287,456条', ha='center', va='center', fontsize=10, 
            color='#555', bbox=dict(boxstyle='round', facecolor='#ECF0F1'))
    ax.text(14.5, 8.2, '可用分析数据\n254,832条', ha='center', va='center', fontsize=10,
            color='#555', bbox=dict(boxstyle='round', facecolor='#D5F5E3'))
    
    ax.annotate('', xy=(1.5, 7.2), xytext=(1.5, 8),
               arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
    ax.annotate('', xy=(14.5, 7.2), xytext=(14.5, 8),
               arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
    
    ax.set_title('图4-6 数据预处理与质量控制流程', fontsize=14, fontweight='bold', pad=20)
    save_fig(fig, '图4-6.png')

# ============================================================
# 主程序
# ============================================================
if __name__ == '__main__':
    print("="*50)
    print("生成V24新增图表")
    print("="*50)
    
    fig_1_4()
    fig_2_7()
    fig_2_8()
    fig_3_3()
    fig_4_5()
    fig_4_6()
    
    print("\n全部6张图表生成完成！")
