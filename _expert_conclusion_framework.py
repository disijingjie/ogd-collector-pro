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

def draw_conclusion_framework():
    """图8-X：研究结论核心发现框架图"""
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # 中心核心发现
    center_circle = patches.Circle((50, 50), 12, facecolor=COLORS['primary'], edgecolor='white', linewidth=3, zorder=5)
    ax.add_patch(center_circle)
    ax.text(50, 50, "中国省级政府\n数据开放平台\n绩效研究", ha='center', va='center', color='white', fontsize=14, fontweight='bold', zorder=6)
    
    # 四个象限的结论框
    boxes = [
        {"pos": (15, 65), "title": "1. 评估框架构建", "content": "• 突破单一数据视角\n• 引入4E公共价值框架\n• 5维9子维24指标\n• 兼顾供给侧与需求侧", "color": COLORS['secondary']},
        {"pos": (60, 65), "title": "2. 绩效特征识别", "content": "• 整体呈现“东强西弱”\n• “数据口径幻觉”普遍存在\n• 识别出五大类型平台\n• 效率与绩效存在错位", "color": COLORS['accent']},
        {"pos": (15, 15), "title": "3. 影响机制揭示", "content": "• 政策环境是核心驱动力\n• 数据质量是关键中介\n• 发现3条高绩效等效路径\n• 殊途同归的组态效应", "color": COLORS['danger']},
        {"pos": (60, 15), "title": "4. 优化路径设计", "content": "• 提出五级成熟度演进模型\n• 构建差异化策略矩阵\n• 制定短中长期实施路线\n• 推动向“价值共创”转型", "color": COLORS['neutral']}
    ]
    
    for box in boxes:
        x, y = box["pos"]
        # 绘制带圆角的矩形框
        rect = patches.FancyBboxPatch((x, y), 25, 20, boxstyle="round,pad=1", 
                                      facecolor='white', edgecolor=box["color"], linewidth=2, zorder=3)
        ax.add_patch(rect)
        
        # 标题区域背景
        title_bg = patches.FancyBboxPatch((x, y+15), 25, 5, boxstyle="round,pad=1", 
                                          facecolor=box["color"], edgecolor=box["color"], linewidth=2, zorder=3)
        # 将下半部分变为直角，使其与内容区无缝连接
        rect_hide = patches.Rectangle((x-1, y+15), 27, 2, facecolor=box["color"], edgecolor='none', zorder=4)
        ax.add_patch(title_bg)
        ax.add_patch(rect_hide)
        
        # 文本
        ax.text(x+12.5, y+17.5, box["title"], ha='center', va='center', color='white', fontsize=12, fontweight='bold', zorder=5)
        ax.text(x+2, y+13, box["content"], ha='left', va='top', color=COLORS['text_main'], fontsize=11, linespacing=1.8, zorder=5)
        
        # 绘制连接线到中心
        cx, cy = 50, 50
        bx, by = x+12.5, y+10
        
        # 计算连接点，使其不穿过圆心
        if bx < cx and by > cy: # 左上
            end_pt = (cx-8.5, cy+8.5)
        elif bx > cx and by > cy: # 右上
            end_pt = (cx+8.5, cy+8.5)
        elif bx < cx and by < cy: # 左下
            end_pt = (cx-8.5, cy-8.5)
        else: # 右下
            end_pt = (cx+8.5, cy-8.5)
            
        # 绘制带箭头的线
        ax.annotate('', xy=end_pt, xytext=(bx, by), 
                    arrowprops=dict(arrowstyle="->", color=box["color"], lw=2, shrinkA=5, shrinkB=5))

    # 添加标题
    plt.title("研究结论核心发现框架图", fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('static/thesis_charts_expert/新增_核心发现框架图.png', dpi=300, bbox_inches='tight')
    print("生成: 新增_核心发现框架图.png")

if __name__ == '__main__':
    draw_conclusion_framework()
