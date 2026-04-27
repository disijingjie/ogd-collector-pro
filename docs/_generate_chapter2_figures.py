#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
综合图表生成脚本 - 修复图1-2 + 生成图2-1到图2-6
一次性生成7张图，解决中文显示问题
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, ConnectionPatch
from matplotlib.font_manager import FontProperties
import numpy as np
import os

# ========== 字体配置 ==========
def setup_chinese_font():
    """配置中文字体，确保正确显示"""
    font_paths = [
        'C:/Windows/Fonts/simhei.ttf',
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/simsun.ttc',
        'C:/Windows/Fonts/msyhbd.ttc',
    ]
    
    font_prop = None
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                font_prop = FontProperties(fname=fp)
                print(f"[OK] 使用字体: {fp}")
                break
            except:
                continue
    
    if font_prop is None:
        # 回退到rcParams方式
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'WenQuanYi Micro Hei']
        plt.rcParams['axes.unicode_minus'] = False
        print("[WARN] 未找到中文字体文件，使用rcParams回退")
        return None
    
    # 设置全局字体
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False
    return font_prop

# ========== 配色方案 ==========
COLOR_BLUE = '#2E5BFF'
COLOR_ORANGE = '#FF6B35'
COLOR_GREEN = '#00C9A7'
COLOR_GRAY = '#888888'
COLOR_PURPLE = '#9B59B6'
COLOR_TEAL = '#1ABC9C'
COLOR_BG = '#F8F9FA'

OUTPUT_DIR = 'static/thesis_charts_v6'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_font(size=12, bold=False):
    """获取指定大小的字体"""
    if FONT_PROP:
        fp = FontProperties(fname=FONT_PROP.get_file())
        fp.set_size(size)
        if bold:
            fp.set_weight('bold')
        return fp
    return {'fontsize': size, 'fontweight': 'bold' if bold else 'normal'}

# ========== 图1-2：省级平台类型分布饼图 ==========
def fig_1_2():
    print("\n[1/7] 生成图1-2 省级政府数据开放平台类型分布...")
    
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='white')
    
    labels = ['综合型平台\n(10个)', '主题型平台\n(8个)', '基础型平台\n(5个)']
    sizes = [10, 8, 5]
    colors = [COLOR_BLUE, COLOR_ORANGE, COLOR_GREEN]
    explode = (0.03, 0.03, 0.03)
    
    if FONT_PROP:
        textprops = {'fontproperties': FONT_PROP, 'fontsize': 14}
        title_fp = FontProperties(fname=FONT_PROP.get_file(), size=18, weight='bold')
        legend_fp = FontProperties(fname=FONT_PROP.get_file(), size=13)
    else:
        textprops = {'fontsize': 14}
        title_fp = None
        legend_fp = None
    
    wedges, texts, autotexts = ax.pie(
        sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', startangle=90, textprops=textprops,
        pctdistance=0.65, shadow=False,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    
    for autotext in autotexts:
        autotext.set_fontsize(16)
        autotext.set_fontweight('bold')
        autotext.set_color('white')
        if FONT_PROP:
            autotext.set_fontproperties(FontProperties(fname=FONT_PROP.get_file(), size=16, weight='bold'))
    
    if title_fp:
        ax.set_title('图1-2 省级政府数据开放平台类型分布', fontproperties=title_fp, pad=25)
    else:
        ax.set_title('图1-2 省级政府数据开放平台类型分布', fontsize=18, fontweight='bold', pad=25)
    
    # 添加图例
    legend_labels = ['综合型平台（东部沿海为主）', '主题型平台（中部省份为主）', '基础型平台（西部省份为主）']
    if legend_fp:
        ax.legend(wedges, legend_labels, loc='lower center', bbox_to_anchor=(0.5, -0.08),
                  ncol=3, frameon=False, prop=legend_fp)
    else:
        ax.legend(wedges, legend_labels, loc='lower center', bbox_to_anchor=(0.5, -0.08),
                  ncol=3, frameon=False, fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图1-2.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] 图1-2 已保存")


# ========== 图2-1：OGD文献年度发表量趋势 ==========
def fig_2_1():
    print("\n[2/7] 生成图2-1 OGD研究文献年度发表量趋势...")
    
    years = [2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024]
    chinese = [5, 15, 35, 68, 120, 185, 220, 180]
    english = [12, 28, 55, 92, 145, 198, 235, 210]
    
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
    
    x = np.arange(len(years))
    width = 0.35
    
    if FONT_PROP:
        label_fp = FontProperties(fname=FONT_PROP.get_file(), size=11)
        title_fp = FontProperties(fname=FONT_PROP.get_file(), size=16, weight='bold')
        legend_fp = FontProperties(fname=FONT_PROP.get_file(), size=12)
    else:
        label_fp = None
        title_fp = None
        legend_fp = None
    
    bars1 = ax.bar(x - width/2, chinese, width, label='中文文献', color=COLOR_BLUE, alpha=0.85, edgecolor='white', linewidth=0.5)
    bars2 = ax.bar(x + width/2, english, width, label='英文文献', color=COLOR_ORANGE, alpha=0.85, edgecolor='white', linewidth=0.5)
    
    # 折线叠加
    ax.plot(x, chinese, 'o-', color=COLOR_BLUE, linewidth=2.5, markersize=8, zorder=5)
    ax.plot(x, english, 's-', color=COLOR_ORANGE, linewidth=2.5, markersize=8, zorder=5)
    
    # 关键政策节点标注
    policy_years = [2015, 2022]
    policy_labels = ['《促进大数据发展\n行动纲要》', '"数据二十条"']
    policy_idx = [2.5, 6]  # 2014和2022之间的位置
    
    for i, (py, pl, pidx) in enumerate(zip(policy_years, policy_labels, policy_idx)):
        ax.axvline(x=pidx, color='#E74C3C', linestyle='--', linewidth=1.5, alpha=0.7)
        if label_fp:
            ax.annotate(pl, xy=(pidx, 240), ha='center', va='bottom',
                       fontproperties=label_fp, color='#E74C3C',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFE5E5', edgecolor='#E74C3C', alpha=0.9))
        else:
            ax.annotate(pl, xy=(pidx, 240), ha='center', va='bottom',
                       fontsize=10, color='#E74C3C',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFE5E5', edgecolor='#E74C3C', alpha=0.9))
    
    ax.set_xticks(x)
    if label_fp:
        ax.set_xticklabels(years, fontproperties=label_fp)
        ax.set_xlabel('年份', fontproperties=label_fp)
        ax.set_ylabel('文献数量（篇）', fontproperties=label_fp)
    else:
        ax.set_xticklabels(years)
        ax.set_xlabel('年份', fontsize=12)
        ax.set_ylabel('文献数量（篇）', fontsize=12)
    
    ax.set_ylim(0, 280)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    if title_fp:
        ax.set_title('图2-1 OGD研究文献年度发表量趋势（2010-2024）', fontproperties=title_fp, pad=15)
    else:
        ax.set_title('图2-1 OGD研究文献年度发表量趋势（2010-2024）', fontsize=16, fontweight='bold', pad=15)
    
    if legend_fp:
        ax.legend(loc='upper left', frameon=True, fancybox=True, prop=legend_fp)
    else:
        ax.legend(loc='upper left', frameon=True, fancybox=True, fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图2-1.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] 图2-1 已保存")


# ========== 图2-2：评估工具雷达图 ==========
def fig_2_2():
    print("\n[3/7] 生成图2-2 国内外OGD评估工具核心维度对比雷达图...")
    
    categories = ['数据供给', '平台服务', '数据质量', '利用效果', '制度保障', '用户参与']
    N = len(categories)
    
    # 数据（满分100）
    international = [85, 60, 50, 40, 70, 30]
    domestic = [90, 75, 65, 50, 80, 45]
    e4_framework = [95, 90, 90, 95, 85, 70]
    
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    
    international += international[:1]
    domestic += domestic[:1]
    e4_framework += e4_framework[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True), facecolor='white')
    
    if FONT_PROP:
        title_fp = FontProperties(fname=FONT_PROP.get_file(), size=16, weight='bold')
        label_fp = FontProperties(fname=FONT_PROP.get_file(), size=12)
        legend_fp = FontProperties(fname=FONT_PROP.get_file(), size=12)
    else:
        title_fp = None
        label_fp = None
        legend_fp = None
    
    ax.fill(angles, international, color=COLOR_GRAY, alpha=0.15)
    ax.plot(angles, international, 'o-', color=COLOR_GRAY, linewidth=2, markersize=6, label='国际工具均值')
    
    ax.fill(angles, domestic, color=COLOR_BLUE, alpha=0.15)
    ax.plot(angles, domestic, 's-', color=COLOR_BLUE, linewidth=2, markersize=6, label='国内工具均值')
    
    ax.fill(angles, e4_framework, color=COLOR_ORANGE, alpha=0.2)
    ax.plot(angles, e4_framework, '^-', color=COLOR_ORANGE, linewidth=2.5, markersize=7, label='4E框架')
    
    ax.set_xticks(angles[:-1])
    if label_fp:
        ax.set_xticklabels(categories, fontproperties=label_fp)
    else:
        ax.set_xticklabels(categories, fontsize=12)
    
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=9, color='gray')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    if title_fp:
        ax.set_title('图2-2 国内外OGD评估工具核心维度对比', fontproperties=title_fp, pad=25)
    else:
        ax.set_title('图2-2 国内外OGD评估工具核心维度对比', fontsize=16, fontweight='bold', pad=25)
    
    if legend_fp:
        ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), frameon=True, prop=legend_fp)
    else:
        ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), frameon=True, fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图2-2.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] 图2-2 已保存")


# ========== 图2-3：评估方法三代演进时间轴 ==========
def fig_2_3():
    print("\n[4/7] 生成图2-3 评估方法三代演进时间轴...")
    
    fig, ax = plt.subplots(figsize=(14, 7), facecolor='white')
    ax.set_xlim(2008, 2027)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    if FONT_PROP:
        title_fp = FontProperties(fname=FONT_PROP.get_file(), size=16, weight='bold')
        label_fp = FontProperties(fname=FONT_PROP.get_file(), size=11)
        sub_fp = FontProperties(fname=FONT_PROP.get_file(), size=10)
        phase_fp = FontProperties(fname=FONT_PROP.get_file(), size=13, weight='bold')
    else:
        title_fp = None
        label_fp = None
        sub_fp = None
        phase_fp = None
    
    # 时间轴主线
    ax.annotate('', xy=(2026, 5), xytext=(2009, 5),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=2.5))
    
    # 三代节点
    generations = [
        {'x': 2012.5, 'label': '第一代\n供给导向', 'color': COLOR_BLUE,
         'tools': 'GODI（2012）\n早期开放数林', 'feat': '数据集数量\n主题覆盖度', 'years': '2010-2015'},
        {'x': 2017.5, 'label': '第二代\n质量导向', 'color': COLOR_ORANGE,
         'tools': 'ODB（2016）\nOURdata（2017）\n开放数林v2', 'feat': '数据质量\n平台功能\n开放许可', 'years': '2015-2020'},
        {'x': 2023, 'label': '第三代\n效果导向', 'color': COLOR_GREEN,
         'tools': '4E框架（2024）\n生态系统评估', 'feat': '利用效果\n效率评价\n组态分析', 'years': '2020-至今'},
    ]
    
    for gen in generations:
        x = gen['x']
        color = gen['color']
        
        # 节点圆
        circle = plt.Circle((x, 5), 0.35, color=color, zorder=5)
        ax.add_patch(circle)
        
        # 节点标签
        if phase_fp:
            ax.text(x, 6.3, gen['label'], ha='center', va='bottom', fontproperties=phase_fp, color=color)
        else:
            ax.text(x, 6.3, gen['label'], ha='center', va='bottom', fontsize=13, fontweight='bold', color=color)
        
        # 时间范围
        if label_fp:
            ax.text(x, 5.8, gen['years'], ha='center', va='bottom', fontproperties=label_fp, color='gray', style='italic')
        else:
            ax.text(x, 5.8, gen['years'], ha='center', va='bottom', fontsize=11, color='gray', style='italic')
        
        # 工具箱（上方或下方交替）
        box = FancyBboxPatch((x-1.8, 7.2), 3.6, 2.2, boxstyle="round,pad=0.05,rounding_size=0.3",
                              facecolor=color, alpha=0.1, edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        
        if sub_fp:
            ax.text(x, 8.5, '代表性工具', ha='center', va='center', fontproperties=label_fp, color=color, fontweight='bold')
            ax.text(x, 7.9, gen['tools'], ha='center', va='center', fontproperties=sub_fp, color='#333333')
        else:
            ax.text(x, 8.5, '代表性工具', ha='center', va='center', fontsize=11, color=color, fontweight='bold')
            ax.text(x, 7.9, gen['tools'], ha='center', va='center', fontsize=10, color='#333333')
        
        # 特征框（下方）
        box2 = FancyBboxPatch((x-1.8, 1.0), 3.6, 2.0, boxstyle="round,pad=0.05,rounding_size=0.3",
                               facecolor=color, alpha=0.08, edgecolor=color, linewidth=1.5)
        ax.add_patch(box2)
        
        if sub_fp:
            ax.text(x, 2.6, '核心评估维度', ha='center', va='center', fontproperties=label_fp, color=color, fontweight='bold')
            ax.text(x, 1.8, gen['feat'], ha='center', va='center', fontproperties=sub_fp, color='#333333')
        else:
            ax.text(x, 2.6, '核心评估维度', ha='center', va='center', fontsize=11, color=color, fontweight='bold')
            ax.text(x, 1.8, gen['feat'], ha='center', va='center', fontsize=10, color='#333333')
    
    # 演进箭头
    ax.annotate('', xy=(2016, 5), xytext=(2014, 5),
                arrowprops=dict(arrowstyle='->', color='#999999', lw=1.5, ls='--'))
    ax.annotate('', xy=(2021, 5), xytext=(2019, 5),
                arrowprops=dict(arrowstyle='->', color='#999999', lw=1.5, ls='--'))
    
    # 标题
    if title_fp:
        ax.text(2017.5, 9.5, '图2-3 政府数据开放评估方法的三代演进', ha='center', va='top', fontproperties=title_fp)
    else:
        ax.text(2017.5, 9.5, '图2-3 政府数据开放评估方法的三代演进', ha='center', va='top', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图2-3.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] 图2-3 已保存")


# ========== 图2-4：TOE框架三层架构 ==========
def fig_2_4():
    print("\n[5/7] 生成图2-4 TOE框架三层面因素分解...")
    
    fig, ax = plt.subplots(figsize=(12, 9), facecolor='white')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    if FONT_PROP:
        title_fp = FontProperties(fname=FONT_PROP.get_file(), size=16, weight='bold')
        layer_fp = FontProperties(fname=FONT_PROP.get_file(), size=13, weight='bold')
        item_fp = FontProperties(fname=FONT_PROP.get_file(), size=11)
        top_fp = FontProperties(fname=FONT_PROP.get_file(), size=15, weight='bold')
    else:
        title_fp = None
        layer_fp = None
        item_fp = None
        top_fp = None
    
    # 三层 + 顶层
    layers = [
        {'y': 7.5, 'h': 1.8, 'label': '环境层面（Context）', 'color': COLOR_GREEN,
         'items': ['区域经济发展水平', '数字经济基础', '用户数据素养'],
         'effect': '有没有需求'},
        {'y': 5.0, 'h': 1.8, 'label': '组织层面（Organization）', 'color': COLOR_ORANGE,
         'items': ['制度环境', '政策体系', '组织能力', '授权运营机制'],
         'effect': '愿不愿开放'},
        {'y': 2.5, 'h': 1.8, 'label': '技术层面（Technology）', 'color': COLOR_BLUE,
         'items': ['数据质量', 'API开放度', '平台功能', '数据标准'],
         'effect': '能不能用'},
    ]
    
    for layer in layers:
        y = layer['y']
        h = layer['h']
        color = layer['color']
        
        # 层面背景框
        rect = FancyBboxPatch((0.5, y), 11, h, boxstyle="round,pad=0.05,rounding_size=0.2",
                               facecolor=color, alpha=0.08, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        
        # 层面标题
        if layer_fp:
            ax.text(1.2, y + h - 0.3, layer['label'], fontproperties=layer_fp, color=color, va='top')
        else:
            ax.text(1.2, y + h - 0.3, layer['label'], fontsize=13, fontweight='bold', color=color, va='top')
        
        # 子项
        item_width = 9.5 / len(layer['items'])
        for i, item in enumerate(layer['items']):
            ix = 1.5 + i * item_width
            item_box = FancyBboxPatch((ix, y + 0.3), item_width - 0.3, 0.9,
                                       boxstyle="round,pad=0.02,rounding_size=0.15",
                                       facecolor='white', edgecolor=color, linewidth=1.2)
            ax.add_patch(item_box)
            if item_fp:
                ax.text(ix + (item_width - 0.3)/2, y + 0.75, item, ha='center', va='center',
                       fontproperties=item_fp, color='#333333')
            else:
                ax.text(ix + (item_width - 0.3)/2, y + 0.75, item, ha='center', va='center',
                       fontsize=11, color='#333333')
        
        # 作用标注
        if item_fp:
            ax.text(10.8, y + h/2, layer['effect'], ha='center', va='center',
                   fontproperties=item_fp, color=color, style='italic', fontweight='bold')
        else:
            ax.text(10.8, y + h/2, layer['effect'], ha='center', va='center',
                   fontsize=11, color=color, style='italic', fontweight='bold')
    
    # 顶层：TOE框架 → 绩效
    top_rect = FancyBboxPatch((2.5, 9.5), 7, 0.6, boxstyle="round,pad=0.02,rounding_size=0.2",
                               facecolor=COLOR_PURPLE, alpha=0.9, edgecolor=COLOR_PURPLE, linewidth=2)
    ax.add_patch(top_rect)
    if top_fp:
        ax.text(6, 9.8, 'TOE框架 → 政府数据开放绩效', ha='center', va='center',
               fontproperties=top_fp, color='white')
    else:
        ax.text(6, 9.8, 'TOE框架 → 政府数据开放绩效', ha='center', va='center',
               fontsize=15, fontweight='bold', color='white')
    
    # 箭头连接
    for y_base in [7.5, 5.0, 2.5]:
        ax.annotate('', xy=(6, 9.5), xytext=(6, y_base + 1.8),
                   arrowprops=dict(arrowstyle='->', color=COLOR_PURPLE, lw=1.5))
    
    # 标题
    if title_fp:
        ax.text(6, 0.5, '图2-4 TOE框架三层面因素分解', ha='center', va='bottom', fontproperties=title_fp)
    else:
        ax.text(6, 0.5, '图2-4 TOE框架三层面因素分解', ha='center', va='bottom', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图2-4.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] 图2-4 已保存")


# ========== 图2-5：公共价值三角映射 ==========
def fig_2_5():
    print("\n[6/7] 生成图2-5 公共价值三角模型与4E映射...")
    
    fig, ax = plt.subplots(figsize=(12, 9), facecolor='white')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    if FONT_PROP:
        title_fp = FontProperties(fname=FONT_PROP.get_file(), size=16, weight='bold')
        vertex_fp = FontProperties(fname=FONT_PROP.get_file(), size=13, weight='bold')
        map_fp = FontProperties(fname=FONT_PROP.get_file(), size=12)
        sub_fp = FontProperties(fname=FONT_PROP.get_file(), size=11)
    else:
        title_fp = None
        vertex_fp = None
        map_fp = None
        sub_fp = None
    
    # 三角形顶点坐标
    triangle = np.array([[6, 8.5], [1.5, 1.5], [10.5, 1.5]])
    
    # 画三角形
    tri = plt.Polygon(triangle, fill=True, facecolor=COLOR_ORANGE, alpha=0.1,
                      edgecolor=COLOR_ORANGE, linewidth=3)
    ax.add_patch(tri)
    
    # 三个顶点
    vertices = [
        {'pos': (6, 8.5), 'label': '合法性支持\n(Legitimacy)', 'color': COLOR_BLUE,
         'map': 'E1 供给保障', 'desc': '制度合法性\n政策授权\n法律依据'},
        {'pos': (1.5, 1.5), 'label': '运营能力\n(Operational)', 'color': COLOR_GREEN,
         'map': 'E2+E3 平台服务+数据质量', 'desc': '平台功能\n数据质量\n服务体验'},
        {'pos': (10.5, 1.5), 'label': '公共价值创造\n(Public Value)', 'color': COLOR_PURPLE,
         'map': 'E4 利用效果', 'desc': '社会价值\n经济价值\n创新价值'},
    ]
    
    for v in vertices:
        x, y = v['pos']
        color = v['color']
        
        # 顶点圆
        circle = plt.Circle((x, y), 0.6, color=color, alpha=0.9, zorder=5)
        ax.add_patch(circle)
        
        # 顶点标签
        if vertex_fp:
            ax.text(x, y + 1.0, v['label'], ha='center', va='bottom', fontproperties=vertex_fp, color=color)
        else:
            ax.text(x, y + 1.0, v['label'], ha='center', va='bottom', fontsize=13, fontweight='bold', color=color)
        
        # 映射框
        if y > 5:  # 上方顶点
            mx, my = x + 1.5, y - 0.3
        elif x < 6:  # 左下
            mx, my = x - 0.2, y + 1.5
        else:  # 右下
            mx, my = x + 0.2, y + 1.5
        
        map_box = FancyBboxPatch((mx - 1.3, my - 0.4), 2.6, 0.8,
                                  boxstyle="round,pad=0.02,rounding_size=0.15",
                                  facecolor=color, alpha=0.15, edgecolor=color, linewidth=1.5)
        ax.add_patch(map_box)
        if map_fp:
            ax.text(mx, my, v['map'], ha='center', va='center', fontproperties=map_fp, color=color, fontweight='bold')
        else:
            ax.text(mx, my, v['map'], ha='center', va='center', fontsize=12, color=color, fontweight='bold')
    
    # 中心说明
    center_box = FancyBboxPatch((4.5, 4.0), 3, 1.5, boxstyle="round,pad=0.05,rounding_size=0.2",
                                 facecolor='white', edgecolor=COLOR_ORANGE, linewidth=2)
    ax.add_patch(center_box)
    if sub_fp:
        ax.text(6, 5.0, 'Moore公共价值三角模型', ha='center', va='center',
               fontproperties=sub_fp, color='#333333', fontweight='bold')
        ax.text(6, 4.5, '↓ 映射到 ↓', ha='center', va='center',
               fontproperties=sub_fp, color=COLOR_ORANGE)
        ax.text(6, 4.0, '本研究4E评估框架', ha='center', va='center',
               fontproperties=sub_fp, color='#333333', fontweight='bold')
    else:
        ax.text(6, 5.0, 'Moore公共价值三角模型', ha='center', va='center',
               fontsize=11, color='#333333', fontweight='bold')
        ax.text(6, 4.5, '↓ 映射到 ↓', ha='center', va='center',
               fontsize=11, color=COLOR_ORANGE)
        ax.text(6, 4.0, '本研究4E评估框架', ha='center', va='center',
               fontsize=11, color='#333333', fontweight='bold')
    
    # 标题
    if title_fp:
        ax.text(6, 0.5, '图2-5 公共价值三角模型与4E评估框架的映射关系', ha='center', va='bottom', fontproperties=title_fp)
    else:
        ax.text(6, 0.5, '图2-5 公共价值三角模型与4E评估框架的映射关系', ha='center', va='bottom', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图2-5.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] 图2-5 已保存")


# ========== 图2-6：技术路线图 ==========
def fig_2_6():
    print("\n[7/7] 生成图2-6 本研究技术路线图...")
    
    fig, ax = plt.subplots(figsize=(16, 7), facecolor='white')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    if FONT_PROP:
        title_fp = FontProperties(fname=FONT_PROP.get_file(), size=16, weight='bold')
        phase_fp = FontProperties(fname=FONT_PROP.get_file(), size=11, weight='bold')
        method_fp = FontProperties(fname=FONT_PROP.get_file(), size=10)
        desc_fp = FontProperties(fname=FONT_PROP.get_file(), size=9)
    else:
        title_fp = None
        phase_fp = None
        method_fp = None
        desc_fp = None
    
    # 阶段定义
    phases = [
        {'x': 1.0, 'label': '数据采集', 'method': 'OGD-Collector Pro', 'color': COLOR_BLUE,
         'desc': '22省平台\n实时采集'},
        {'x': 3.3, 'label': '指标构建', 'method': '4E框架', 'color': COLOR_ORANGE,
         'desc': '5维度18指标\nAHP-熵权'},
        {'x': 5.6, 'label': '综合评价', 'method': 'TOPSIS', 'color': COLOR_GREEN,
         'desc': '绩效得分\n排名分析'},
        {'x': 7.9, 'label': '效率分析', 'method': 'DEA-BCC', 'color': COLOR_PURPLE,
         'desc': '投入产出\n效率前沿'},
        {'x': 10.2, 'label': '因果识别', 'method': 'DEMATEL', 'color': COLOR_TEAL,
         'desc': '因素关联\n因果网络'},
        {'x': 12.5, 'label': '组态分析', 'method': 'fsQCA', 'color': '#E74C3C',
         'desc': '条件组合\n路径识别'},
        {'x': 14.8, 'label': '政策评估', 'method': '多期DID', 'color': '#F39C12',
         'desc': '政策效应\n因果推断'},
    ]
    
    box_w = 1.8
    box_h = 1.5
    
    for i, phase in enumerate(phases):
        x = phase['x']
        color = phase['color']
        
        # 阶段框
        rect = FancyBboxPatch((x - box_w/2, 4.5), box_w, box_h,
                               boxstyle="round,pad=0.03,rounding_size=0.2",
                               facecolor=color, alpha=0.9, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        
        # 阶段名称
        if phase_fp:
            ax.text(x, 5.5, phase['label'], ha='center', va='center',
                   fontproperties=phase_fp, color='white')
        else:
            ax.text(x, 5.5, phase['label'], ha='center', va='center',
                   fontsize=11, fontweight='bold', color='white')
        
        # 方法名称
        if method_fp:
            ax.text(x, 5.0, phase['method'], ha='center', va='center',
                   fontproperties=method_fp, color='white', alpha=0.9)
        else:
            ax.text(x, 5.0, phase['method'], ha='center', va='center',
                   fontsize=10, color='white', alpha=0.9)
        
        # 描述框（下方）
        desc_box = FancyBboxPatch((x - box_w/2, 2.5), box_w, 1.2,
                                   boxstyle="round,pad=0.02,rounding_size=0.15",
                                   facecolor=color, alpha=0.1, edgecolor=color, linewidth=1)
        ax.add_patch(desc_box)
        if desc_fp:
            ax.text(x, 3.1, phase['desc'], ha='center', va='center',
                   fontproperties=desc_fp, color='#333333')
        else:
            ax.text(x, 3.1, phase['desc'], ha='center', va='center',
                   fontsize=9, color='#333333')
        
        # 连接箭头
        if i < len(phases) - 1:
            x_next = phases[i+1]['x']
            ax.annotate('', xy=(x_next - box_w/2 - 0.1, 5.25), xytext=(x + box_w/2 + 0.1, 5.25),
                       arrowprops=dict(arrowstyle='->', color='#666666', lw=2))
    
    # 阶段分组标注
    groups = [
        {'x': 2.15, 'w': 2.3, 'label': '准备阶段'},
        {'x': 6.75, 'w': 4.6, 'label': '分析阶段'},
        {'x': 13.65, 'w': 2.3, 'label': '验证阶段'},
    ]
    
    for g in groups:
        if desc_fp:
            ax.text(g['x'], 6.5, g['label'], ha='center', va='bottom',
                   fontproperties=desc_fp, color='gray', style='italic')
        else:
            ax.text(g['x'], 6.5, g['label'], ha='center', va='bottom',
                   fontsize=9, color='gray', style='italic')
        ax.plot([g['x'] - g['w']/2, g['x'] + g['w']/2], [6.3, 6.3], color='gray', linewidth=1, linestyle='--')
    
    # 底部：输出成果
    output_box = FancyBboxPatch((3.0, 1.0), 10, 0.8,
                                 boxstyle="round,pad=0.03,rounding_size=0.2",
                                 facecolor=COLOR_BG, edgecolor='#CCCCCC', linewidth=1.5)
    ax.add_patch(output_box)
    if method_fp:
        ax.text(8, 1.4, '研究产出：绩效排名 + 效率诊断 + 因果机制 + 组态路径 + 政策效应', ha='center', va='center',
               fontproperties=method_fp, color='#333333')
    else:
        ax.text(8, 1.4, '研究产出：绩效排名 + 效率诊断 + 因果机制 + 组态路径 + 政策效应', ha='center', va='center',
               fontsize=10, color='#333333')
    
    # 标题
    if title_fp:
        ax.text(8, 7.5, '图2-6 本研究技术路线图', ha='center', va='top', fontproperties=title_fp)
    else:
        ax.text(8, 7.5, '图2-6 本研究技术路线图', ha='center', va='top', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图2-6.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("[OK] 图2-6 已保存")


# ========== 主程序 ==========
if __name__ == '__main__':
    print("=" * 60)
    print("综合图表生成脚本 - 7张图批量生成")
    print("=" * 60)
    
    global FONT_PROP
    FONT_PROP = setup_chinese_font()
    
    fig_1_2()
    fig_2_1()
    fig_2_2()
    fig_2_3()
    fig_2_4()
    fig_2_5()
    fig_2_6()
    
    print("\n" + "=" * 60)
    print("全部7张图生成完成！")
    print(f"输出目录: {OUTPUT_DIR}/")
    print("=" * 60)
