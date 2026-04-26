import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 统一配色方案
COLORS = {
    'primary': '#1f77b4',     # 学术蓝
    'secondary': '#ff7f0e',   # 活力橙
    'accent': '#2ca02c',      # 增长绿
    'danger': '#d62728',      # 警示红
    'neutral': '#7f7f7f',     # 中性灰
    'bg_light': '#f8f9fa',    # 浅灰背景
    'text_main': '#333333',   # 主文本
    'text_sub': '#666666'     # 次文本
}

def draw_nested_logic():
    """图4-X：混合方法嵌套逻辑图"""
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # 绘制外层大框 (DEMATEL)
    outer_box = patches.FancyBboxPatch((5, 5), 90, 85, boxstyle="round,pad=2", 
                                       facecolor='#e6f2ff', edgecolor=COLORS['primary'], 
                                       linewidth=2, linestyle='--')
    ax.add_patch(outer_box)
    ax.text(50, 93, "第一阶段：DEMATEL (决策试验和评价实验室法)", ha='center', va='center', 
            fontsize=14, fontweight='bold', color=COLORS['primary'])
    ax.text(50, 88, "目标：揭示12个影响因素间的复杂因果网络，识别关键原因因素与结果因素", 
            ha='center', va='center', fontsize=11, color=COLORS['text_sub'])
    
    # 绘制内层大框 (fsQCA)
    inner_box = patches.FancyBboxPatch((20, 15), 60, 55, boxstyle="round,pad=2", 
                                       facecolor='#fff0e6', edgecolor=COLORS['secondary'], 
                                       linewidth=2)
    ax.add_patch(inner_box)
    ax.text(50, 73, "第二阶段：fsQCA (模糊集定性比较分析)", ha='center', va='center', 
            fontsize=14, fontweight='bold', color=COLORS['secondary'])
    ax.text(50, 68, "目标：探索前因条件（由DEMATEL筛选）如何组合导致高绩效结果", 
            ha='center', va='center', fontsize=11, color=COLORS['text_sub'])
    
    # 绘制流程箭头与节点
    # 1. 初始因素池
    ax.text(50, 80, "24个初始影响因素\n(基于4E框架与文献提取)", ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=COLORS['neutral']))
    
    # 箭头向下
    ax.annotate('', xy=(50, 75), xytext=(50, 77), arrowprops=dict(facecolor=COLORS['neutral'], width=2, headwidth=8))
    
    # 2. 筛选后的核心条件
    ax.text(50, 55, "6个核心前因条件\n(政策环境、数据质量、平台功能等)", ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=COLORS['secondary'], lw=2))
    
    # 箭头向下
    ax.annotate('', xy=(50, 48), xytext=(50, 52), arrowprops=dict(facecolor=COLORS['secondary'], width=2, headwidth=8))
    
    # 3. 组态分析过程
    ax.text(50, 40, "真值表构建与逻辑最小化\n(一致性阈值0.8，频数阈值1)", ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=COLORS['neutral']))
    
    # 箭头向下
    ax.annotate('', xy=(50, 33), xytext=(50, 37), arrowprops=dict(facecolor=COLORS['secondary'], width=2, headwidth=8))
    
    # 4. 组态结果
    ax.text(35, 25, "路径1：改革引领型\n(政策*平台*环境)", ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.5", fc=COLORS['accent'], ec="white", alpha=0.8))
    ax.text(65, 25, "路径2：制度保障型\n(~政策*制度*质量)", ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.5", fc=COLORS['accent'], ec="white", alpha=0.8))
    
    # 连接线 (从3到4)
    ax.plot([50, 50], [33, 30], color=COLORS['secondary'], lw=2)
    ax.plot([35, 65], [30, 30], color=COLORS['secondary'], lw=2)
    ax.annotate('', xy=(35, 27), xytext=(35, 30), arrowprops=dict(facecolor=COLORS['secondary'], width=2, headwidth=8))
    ax.annotate('', xy=(65, 27), xytext=(65, 30), arrowprops=dict(facecolor=COLORS['secondary'], width=2, headwidth=8))
    
    # 添加"降维与聚焦"说明
    ax.annotate('降维与聚焦\n(提供科学的条件选择依据)', xy=(50, 75), xytext=(75, 80),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2", color=COLORS['primary']),
                fontsize=11, color=COLORS['primary'], ha='center',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COLORS['primary'], alpha=0.8))

    # 添加标题
    plt.title("DEMATEL-fsQCA混合方法嵌套逻辑模型", fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('static/thesis_charts_expert/新增_混合方法嵌套逻辑图.png', dpi=300, bbox_inches='tight')
    print("生成: 新增_混合方法嵌套逻辑图.png")

if __name__ == '__main__':
    draw_nested_logic()
